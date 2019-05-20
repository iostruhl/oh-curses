import sys
from time import sleep
from sys import stdin, exit
from card import Card

from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    def __init__(self, host, port, name = "ANON"):
        self.Connect((host, port))
        print("Oh Hell client started")
        print("Ctrl-C to exit")
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

    def Network_hand_dealt(self, data):
        print("HAND DEALT, data is", data)
        print("Hand has been dealt, trump suit is", data['trump_suit'])
        print("Hand is", data['hand'])

    def Network_bid(self, data):
        bid = int(input("Enter your bid: "))
        connection.Send({'action': "bid", 'bid': bid})

    def Network_broadcast_bid(self, data):
        print(data['player'], "has bid", data['bid'])

    def Network_play_card(self, data):
        card = input("Enter card to play: ").split(',')
        connection.Send({'action': 'play', 'card': card})

    def Network_broadcast_played_card(self, data):
        print(data['player'], "played card", data['card'])

    def Network_broadcast_trick_winner(self, data):
        print(data['player', "won the trick"])

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

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "host:port name")
    print("e.g.", sys.argv[0], "localhost:8080 Isaac")
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port), sys.argv[2])
    while 1:
        c.Loop()
        sleep(0.001)