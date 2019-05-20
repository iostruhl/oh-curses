import sys
import gameboard
from time import sleep, localtime

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        super().__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
    
    def Network_nickname(self, data):
        self.name = data['nickname']
        self._server.SendPlayers()

class OHServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.users = []
        self.gb = None
        print("Server launched")
    
    def Connected(self, channel, addr):
        self.add_player(channel)
    
    def add_player(self, player):
        print("New Player" + str(player.addr))
        self.users[player] = player.name
        self.send_players()
        print("players", [p for p in self.players])
        if (len(self.players) == 4):
            if (self.gb):
                self.resume_game()
            else:
                self.start_game()
    
    def remove_player(self, player):
        print("Remove Player" + str(player.addr))
        self.players.remove(player)
        if (self.gb):
            self.send_pause()

    def send_pause(self):
        self.send_all({"action": "pause"})
    
    def send_players(self):
        self.send_all({"action": "players", "players": [p.nickname for p in self.players]})
    
    def send_all(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = ChatServer(localaddr=(host, int(port)))
    s.Launch()