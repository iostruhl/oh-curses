import sys
from time import sleep
from sys import stdin, exit
from common.card import Card
from common.boardstate import ClientBoard
import common.graphics_board as graphics_board

from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    def __init__(self, host, port, name = "ANON"):
        self.Connect((host, port))
        print("Oh Hell client started")
        print("Ctrl-C to exit")
        self.name = name
        # get a nickname from the user before starting
        connection.Send({"action": "name", "name": name})

    def Loop(self):
        connection.Pump()
        self.Pump()

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_users(self, data):
        print("*** users: " + ", ".join([p for p in data['users']]))

    def Network_pause(self, data):
        print("*** USER HAS DISCONNECTED, BAD BAD BAD\nFAILS SILENTLY FOR NOW, WILL BLOW UP LATER")

    def Network_start(self, data):
        self.cb = ClientBoard(data['players'], self.name)
        self.grb = graphics_board.GraphicsBoard(self.cb)

    def Network_hand_dealt(self, data):
        self.cb.get_hand(data['hand'])
        self.cb.trump_card = Card(data['trump_card'][0], data['trump_card'][1])
        self.cb.trump_card.show()
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
        print(data['player'], "won the trick")

    def Network_start_hand(self, data):
        self.grb.start_hand()

    def Network_broadcast_hand_done(self, data):
        print("Hand is over.")


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
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port name")
        print("e.g.", sys.argv[0], "localhost:8080 Isaac")
    else:
        host, port = sys.argv[1].split(":")
        c = Client(host, int(port), sys.argv[2])
        while 1:
            c.Loop()
            sleep(0.001)
