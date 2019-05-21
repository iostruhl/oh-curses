import curses
from curses import panel

# this jankiness shouldn't be needed later
import sys
sys.path.append('../server')
from gameboard import GameBoard

padding = 0
v_spacing = 1
h_spacing = 5
c_height = 11
c_width = 13

class Board:

    def __init__(self, stdscreen, g: GameBoard, active: str):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(True)
        # Only support drawing 4-player games for now
        assert(len(g.players) == 4)
        self.g = g
        self.active = active
        self.active_position = g.players.index(active)
        self.hand_position = 0
        self.hand_windows = [[] for player in g.players]
        self.hand_panels = [[] for player in g.players]

    def hand_navigate(self, n):
        hand_len = len(self.g.hands[self.active])
        self.clear_hand_card(self.active, self.hand_position)
        self.hand_windows[0][self.hand_position].mvwin((3*padding)+(c_height)+(12*v_spacing)+c_height, (2*padding)+c_width+(self.hand_position*h_spacing))
        self.hand_position = (self.hand_position + n) % len(self.g.hands[self.active])
        self.hand_windows[0][self.hand_position].mvwin((3*padding)+(c_height)+(12*v_spacing)+c_height-2, (2*padding)+c_width+(self.hand_position*h_spacing))
        if (n < 0 and self.hand_position == 12):
            self.draw_hand_above(0)
        else:
            self.draw_hand_above(self.hand_position - 1)

    def new_hand(self, hand: int):
        for i in range(len(self.g.players)):
            if i == self.active_position:
                self.hand_windows[0] = [curses.newwin(11, 13, (3*padding)+(c_height)+(12*v_spacing)+c_height, (2*padding)+c_width+(j*h_spacing))
                                        for j in range(hand)]
                self.hand_panels[0] = [panel.new_panel(self.hand_windows[0][j])
                                       for j in range(hand)]
                # For testing
                for card in self.g.hands[self.g.players[i]]:
                    card.show()

                # Initially select first card
                self.hand_windows[0][self.hand_position].mvwin((3*padding)+(c_height)+(12*v_spacing)+c_height-2, (2*padding)+c_width+(self.hand_position*h_spacing))
            elif i == (self.active_position + 1) % 4:
                self.hand_windows[1] = [curses.newwin(11, 13, (2*padding)+c_height+(j*v_spacing), padding)
                                        for j in range(hand)]
                self.hand_panels[1] = [panel.new_panel(self.hand_windows[1][j])
                                       for j in range(hand)]
            elif i == (self.active_position + 2) % 4:
                self.hand_windows[2] = [curses.newwin(11, 13, padding, (2*padding)+c_width+(j*h_spacing))
                                        for j in range(hand)]
                self.hand_panels[2] = [panel.new_panel(self.hand_windows[2][j])
                                       for j in range(hand)]
            elif i == (self.active_position + 3) % 4:
                self.hand_windows[3] = [curses.newwin(11, 13, (2*padding)+c_height+(j*v_spacing), (3*padding)+(c_width)+(12*h_spacing)+c_width)
                                        for j in range(hand)]
                self.hand_panels[3] = [panel.new_panel(self.hand_windows[3][j])
                                       for j in range(hand)]

    def input(self):
        while (True):
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                # TODO: play card
                exit()

            elif key == curses.KEY_LEFT or key == curses.KEY_UP:
                self.hand_navigate(-1)

            elif key == curses.KEY_RIGHT or key == curses.KEY_DOWN:
                self.hand_navigate(1)

    def draw_hand_card(self, player, card):
        player_position = (self.g.players.index(player) - self.active_position) % 4
        self.hand_windows[player_position][card].erase()
        self.hand_windows[player_position][card].addstr(
            self.g.hands[player][card].ascii_rep())
        self.hand_windows[player_position][card].refresh()

    def clear_hand_card(self, player, card):
        player_position = (self.g.players.index(player) - self.active_position) % 4
        self.hand_windows[player_position][card].erase()
        self.hand_windows[player_position][card].refresh()

    def draw_hand(self, player):
        for card in range(len(self.g.hands[player])):
            self.draw_hand_card(player, card)

    def draw_hand_above(self, position):
        for card in range(position, len(self.g.hands[self.active])):
            self.draw_hand_card(self.active, card)

    def init_display(self):
        self.window.erase()
        self.window.refresh()

        for player in self.g.players:
            self.draw_hand(player)

        self.input()



class App:
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        g = GameBoard()
        board = Board(self.screen, g, "Alex")
        g.deal_hand(13)
        board.new_hand(13)
        board.init_display()

if __name__ == "__main__":
    curses.wrapper(App)
