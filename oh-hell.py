import sys
from time import sleep
from sys import stdin, exit
from common.card import Card
from common.boardstate import ClientBoard
import common.graphics_board as graphics_board
import shutil

from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    def __init__(self, host, port, name = "ANON", sort_hand_ascending = False):
        self.Connect((host, port))
        print("Oh Hell client started")
        print("Ctrl-C to exit")
        self.name = name
        self.sort_hand_ascending = sort_hand_ascending
        # get a nickname from the user before starting
        connection.Send({"action": "name", "name": name})

    def Loop(self):
        connection.Pump()
        self.Pump()

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_users(self, data):
        print("*** users:", ', '.join([p for p in data['users']]), "***")

    def Network_server_name(self, data):
        print("Server set name to", data['name'])
        self.name = data['name']
        connection.Send({
                'action': "ready",
                'name': self.name
            })

    def Network_pause(self, data):
        print("*** USER HAS DISCONNECTED, FATAL ***")
        exit(1)

    def Network_resume(self, data):
        self.cb = ClientBoard(data['players'], self.name)
        for player in self.cb.players:
            self.cb.scores[player] = data['scores'][player]
        self.cb.running_scores = data['running_scores']
        self.grb = graphics_board.GraphicsBoard(self.cb)

    def Network_start(self, data):
        self.cb = ClientBoard(data['players'], self.name)
        self.grb = graphics_board.GraphicsBoard(self.cb)

    def Network_hand_dealt(self, data):
        # Reverse hand order if player wants to sort it backwards.
        if self.sort_hand_ascending:
            data['hand'] = data['hand'][::-1]
        self.cb.get_hand(data['hand'])
        if data['trump_card']:
            self.cb.trump_card = Card(data['trump_card'][0], data['trump_card'][1])
            self.cb.trump_card.show()
        else:
            self.cb.trump_card = None
        self.grb.draw_new_hand(len(data['hand']))

    def Network_bid(self, data):
        bid = self.grb.get_bid(data['hand'], data['dealer'])
        connection.Send({'action': "bid", 'bid': bid})

    def Network_broadcast_bid(self, data):
        self.cb.bids[data['player']] = data['bid']
        self.grb.receive_bid(data['player'], data['bid'])

    def Network_play_card(self, data):
        card = self.grb.get_card()
        connection.Send({'action': 'play', 'card': card.to_array(), 'lead': data['lead']})

    def Network_broadcast_played_card(self, data):
        card = Card(data['card'][0], data['card'][1])
        card.show()
        self.cb.in_play[data['player']] = card
        if data['lead']:
            self.cb.lead_card = card
        self.grb.play_card(data['player'])

    def Network_broadcast_trick_winner(self, data):
        self.cb.in_play = {player:None for player in self.cb.players}
        self.cb.lead_card = None
        self.cb.won[data['player']] += 1
        sleep(2)
        self.grb.finish_trick(data['player'])

    def Network_start_hand(self, data):
        self.grb.start_hand()

    def Network_broadcast_hand_done(self, data):
        self.cb.bids = dict()
        for player in self.cb.players:
            self.cb.won[player] = 0
            self.cb.scores[player] = data['scores'][player]
            self.cb.running_scores[player].append(data['scores'][player])
        self.grb.clean_board()

    def Network_broadcast_dealer(self, data):
        self.cb.dealer = data['dealer']

    def Network_broadcast_current_actor(self, data):
        self.cb.actor = data['actor']
        self.grb.refresh_all_info_windows()
        self.grb.refresh_hand_info_window(data['hand_num'])

    def Network_broadcast_end_game(self, data):
        self.cb.winner = data['winner']
        self.grb.end_game()

    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

# Run the client
if __name__ == "__main__":
    if len(sys.argv) not in [3,4]:
        print("Usage:", sys.argv[0], "host:port name [--sort_hand_ascending]")
        print("e.g.", sys.argv[0], "localhost:8080 Isaac")
    else:
        size = shutil.get_terminal_size()
        assert (size.columns >= 181 and size.lines >= 58), "Resize terminal to at least 181x58"
        host, port = sys.argv[1].split(":")
        c = Client(host, int(port), name = sys.argv[2], sort_hand_ascending = (len(sys.argv) == 4))
        while 1:
            c.Loop()
            sleep(0.001)
