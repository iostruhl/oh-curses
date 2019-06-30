import sys
from common.boardstate import GameBoard
from time import sleep
from common.card import Card
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from common import sheets_logging
from fuzzywuzzy import process

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.name = "ANON"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.remove_player(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_name(self, data):
        print("Client", self.name, "sent", data)
        if self._server.untracked:
            self.name = data['name']
        else:
            # chooses the best matched full name, so that we can log easily at the end
            choices = ["Ben Harpe", "Alex Wulff", "Alex Mariona", "Owen Schafer", "Isaac Struhl"]
            self.name = process.extract(data['name'], choices, limit=1)[0][0]

        self._server.send_users()
        self.Send({
                'action': "server_name",
                'name': self.name
            })

    def Network_ready(self, data):
        print("Client", self.name, "sent", data)
        assert(self.name == data['name'])
        self._server.handle_ready()

    def Network_bid(self, data):
        print("Client", self.name, "sent", data)
        self._server.handle_bid(self.name, data['bid'])

    def Network_play(self, data):
        print("Client", self.name, "sent", data)
        self._server.handle_play_card(self.name, data['card'], data['lead'])


class OHServer(Server):
    channelClass = ClientChannel

    def __init__(self, untracked = False, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.users = []
        self.name_to_user = dict()
        self.ready_count = 0
        self.hand_num = 1
        self.scores = dict()
        self.next_to_play_idx = 0
        self.gb = None
        self.should_resume = False
        self.untracked = untracked
        print("Server launched")

    def Connected(self, channel, addr):
        self.add_user(channel)

    def add_user(self, user):
        print("New Player" + str(user.addr))
        self.users.append(user)

    def remove_player(self, player):
        print("Remove Player" + str(player.addr))
        self.users.remove(player)
        self.ready_count -= 1
        if (self.gb):
            self.gb.collect_cards()
            self.send_pause()

    def send_pause(self):
        self.send_all({'action': "pause"})

    def send_users(self):
        self.send_all({'action': "users", 'users': [u.name for u in self.users]})

    def send_all(self, data):
        print("Server: sending to ALL :", data)
        [u.Send(data) for u in self.users]

    def send_one(self, name, data, echo = True):
        if echo:
            print("Server: sending to", name, ":", data)
        self.name_to_user[name].Send(data)

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

    # --- Game Logic ---
    def handle_ready(self):
        self.ready_count += 1
        if (self.ready_count == 4):
            if (self.should_resume):
                self.resume_game() # SHOULD EVENTUALLY CALL RESUME, IDK WHY IT DOESN'T WORK RN
            else:
                self.start_game()

    def resume_game(self):
        for u in self.users:
            assert u.name in self.name_to_user
        self.name_to_user = {u.name:u for u in self.users}
        self.send_all({
            'action': "resume",
            'players': self.gb.players,
            'scores': self.gb.scores,
            'running_scores': self.gb.running_scores
            })
        self.start_hand()

    def start_game(self):
        print("Game starting.")
        self.gb = GameBoard(players = [u.name for u in self.users])
        self.name_to_user = {u.name:u for u in self.users}
        self.scores = {u.name:0 for u in self.users}

        self.send_all({
            'action': "start",
            'players': self.gb.players
            })

        self.should_resume = True
        self.start_hand()


    def start_hand(self):
        self.gb.deal_hand(self.hand_num)
        self.send_all({'action': "broadcast_dealer", 'dealer': self.gb.players[(self.hand_num + 2) % 4]})
        for player in self.gb.players:
            print("Sending to", player)

            self.send_one(player, {
                'action': "hand_dealt",
                'trump_card': self.gb.trump_card.to_array() if self.gb.trump_card else None,
                'hand': [c.to_array() for c in sorted(self.gb.hands[player])]
                }, echo = False)

        self.send_all({'action': "broadcast_current_actor", 'actor': self.gb.players[(self.hand_num - 1) % 4], 'hand_num': self.hand_num})
        self.send_one(self.gb.players[(self.hand_num - 1) % 4], {
            'action': "bid",
            'hand': self.hand_num,
            'dealer': False
            })


    def handle_bid(self, player: str, bid: int):
        self.send_all({'action': "broadcast_bid", 'player': player, 'bid': bid})
        self.gb.bid(player, bid)
        if (len(self.gb.bids) == 4):
            self.next_to_play_idx = (self.hand_num - 1) % 4 # set to dealer, incremented by handle_play
            self.send_all({'action': "start_hand"})
            self.send_all({'action': "broadcast_current_actor", 'actor': self.gb.players[self.next_to_play_idx], 'hand_num': self.hand_num})
            self.send_one(self.gb.players[self.next_to_play_idx], {'action': "play_card", 'lead': True})
        else:
            self.send_all({'action': "broadcast_current_actor", 'actor': self.gb.players[((self.hand_num - 1) + len(self.gb.bids)) % 4], 'hand_num': self.hand_num})
            self.send_one(self.gb.players[((self.hand_num - 1) + len(self.gb.bids)) % 4], {
                'action': "bid",
                'hand': self.hand_num, 'dealer': True if len(self.gb.bids) == 3 else False
                })


    def handle_play_card(self, player: str, card: list, lead = False):
        self.send_all({
            'action': "broadcast_played_card",
            'player': player,
            'card': card,
            'lead': lead
            })
        self.gb.play_card(player, Card(card[0], card[1]), lead = True if len(self.gb.in_play) == 0 else False)
        if (len(self.gb.in_play) != 4):
            self.next_to_play_idx = (self.next_to_play_idx + 1) % 4
            self.send_all({'action': "broadcast_current_actor", 'actor': self.gb.players[self.next_to_play_idx], 'hand_num': self.hand_num})
            self.send_one(self.gb.players[self.next_to_play_idx], {'action': "play_card", 'lead': False})
        else:
            self.finish_trick()


    def finish_trick(self):
        winner = self.gb.finish_trick()
        self.send_all({
            'action': "broadcast_trick_winner",
            'player': winner})
        if (len(self.gb.hands[winner]) == 0):
            self.gb.assert_hand_done()
            self.finish_hand()
        else:
            self.next_to_play_idx = self.gb.players.index(winner) # start with the prev winner
            self.send_all({'action': "broadcast_current_actor", 'actor': self.gb.players[self.next_to_play_idx], 'hand_num': self.hand_num})
            self.send_one(winner, {'action': "play_card", 'lead': True})


    def finish_hand(self):
        scores = self.gb.update_scores()
        self.send_all({
            'action': "broadcast_hand_done",
            'scores': self.gb.scores,
            'hand_num': self.hand_num
            })
        self.gb.collect_cards()
        self.hand_num += 1
        if (self.hand_num > 13):
            self.end_game()
        else:
            self.start_hand()


    def end_game(self):
        print("Game Complete!")
        print("Vars at end:", vars(self))
        print("Logging game, scores are", self.gb.scores)
        winner = max(self.gb.scores, key=lambda player: self.gb.scores[player])
        self.send_all({
            'action': "broadcast_end_game",
            'winner': winner,
            'scores': self.gb.scores
            })
        if not self.untracked:
            sheets_logging.log_game(self.gb.scores)

# Run the server
if __name__ == "__main__":
    # get command line argument of server, port
    if len(sys.argv) not in [2, 3]:
        print("Usage:", sys.argv[0], "host:port <untracked>")
        print("e.g.", sys.argv[0], "localhost:31425")
        print("or", sys.argv[0], "localhost:31425 untracked")
        exit(1)
    host, port = sys.argv[1].split(":")
    s = OHServer(untracked = (len(sys.argv) == 3), localaddr = (host, int(port)))
    try:
        s.Launch()
    except:
        print("\nServer killed by signal.")
