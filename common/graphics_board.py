import curses
from curses import panel
from .boardstate import ClientBoard

PADDING = 1
V_SPACING = 1
H_SPACING = 5
C_HEIGHT = 11
C_WIDTH = 13
I_HEIGHT = 5
I_WIDTH = 11

class GraphicsBoard:

    def __init__(self, cb: ClientBoard):
        # Set up curses
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.window = self.stdscr.subwin(0,0)
        self.window.keypad(True)

        # Only support drawing 4-player games for now
        # self.g = cb
        # self.active = cb.active
        # self.active_position = cb.players.index(active)
        # self.hand_position = 0
        # self.hand_windows = [[] for player in cb.players]
        # self.hand_panels = [[] for player in cb.players]
        # self.played_windows = [None for player in cb.players]
        # self.trump_window = None
        # self.info_windows = [None for player in cb.players]
        self.window.addstr("SETUP SUCCESSFUL\n")
        self.window.refresh()

    def hand_navigate(self, n):
        hand_len = len(self.g.hands[self.active])
        self.clear_hand_card(self.active, self.hand_position)
        self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
        self.hand_position = (self.hand_position + n) % len(self.g.hands[self.active])
        self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT-2, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
        if (n < 0 and self.hand_position == 12):
            self.redraw_hand(0)
        else:
            self.redraw_hand(self.hand_position - 1)

    def draw_new_hand(self, hand: int):
        for i in range(len(self.g.players)):
            if i == self.active_position:
                self.hand_windows[0] = [curses.newwin(11, 13, (4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(j*H_SPACING))
                                        for j in range(hand)]
                self.hand_panels[0] = [panel.new_panel(self.hand_windows[0][j])
                                       for j in range(hand)]

                # For testing
                for card in self.g.hands[self.g.players[i]]:
                    card.show()

                # Initially select first card
                self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT-2, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
            elif i == (self.active_position + 1) % 4:
                self.hand_windows[1] = [curses.newwin(11, 13, (4*PADDING)+C_HEIGHT+(j*V_SPACING), PADDING)
                                        for j in range(hand)]
                self.hand_panels[1] = [panel.new_panel(self.hand_windows[1][j])
                                       for j in range(hand)]
            elif i == (self.active_position + 2) % 4:
                self.hand_windows[2] = [curses.newwin(11, 13, PADDING, (2*PADDING)+C_WIDTH+(j*H_SPACING))
                                        for j in range(hand)]
                self.hand_panels[2] = [panel.new_panel(self.hand_windows[2][j])
                                       for j in range(hand)]
            elif i == (self.active_position + 3) % 4:
                self.hand_windows[3] = [curses.newwin(11, 13, (4*PADDING)+C_HEIGHT+(j*V_SPACING), (3*PADDING)+(2*C_WIDTH)+(12*H_SPACING))
                                        for j in range(hand)]
                self.hand_panels[3] = [panel.new_panel(self.hand_windows[3][j])
                                       for j in range(hand)]

    def run(self):
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
        if (self.g.hands[player][card].visible):
            self.hand_windows[player_position][card].attron(
            curses.color_pair(self.g.hands[player][card].color()))
        else:
            self.hand_windows[player_position][card].attroff(
            curses.color_pair(self.g.hands[player][card].color()))
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

    def redraw_hand(self, position):
        for card in range(position, len(self.g.hands[self.active])):
            self.draw_hand_card(self.active, card)

    def test_draw_play(self):
        for i in range(len(self.g.players)):
            if i == self.active_position:
                self.played_windows[0] = curses.newwin(11, 13, (4*PADDING)+C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.played_windows[0].erase()
                self.played_windows[0].attron(
                    curses.color_pair(self.g.hands[self.active][0].color()))
                self.played_windows[0].addstr(
                    self.g.hands[self.active][0].ascii_rep())
                self.played_windows[0].refresh()
            elif i == (self.active_position + 1) % 4:
                self.played_windows[1] = curses.newwin(11, 13, (4*PADDING)+C_HEIGHT+(6*V_SPACING), (2*PADDING)+C_WIDTH+(3*H_SPACING))
                self.played_windows[1].erase()
                self.played_windows[1].attron(
                    curses.color_pair(self.g.hands[self.active][1].color()))
                self.played_windows[1].addstr(
                    self.g.hands[self.active][1].ascii_rep())
                self.played_windows[1].refresh()
            elif i == (self.active_position + 2) % 4:
                self.played_windows[2] = curses.newwin(11, 13, (4*PADDING)+C_HEIGHT, (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.played_windows[2].erase()
                self.played_windows[2].attron(
                    curses.color_pair(self.g.hands[self.active][2].color()))
                self.played_windows[2].addstr(
                    self.g.hands[self.active][2].ascii_rep())
                self.played_windows[2].refresh()
            elif i == (self.active_position + 3) % 4:
                self.played_windows[3] = curses.newwin(11, 13, (4*PADDING)+C_HEIGHT+(6*V_SPACING), (2*PADDING)+C_WIDTH+(9*H_SPACING))
                self.played_windows[3].erase()
                self.played_windows[3].attron(
                    curses.color_pair(self.g.hands[self.active][3].color()))
                self.played_windows[3].addstr(
                    self.g.hands[self.active][3].ascii_rep())
                self.played_windows[3].refresh()

    def test_draw_trump(self):
        self.trump_window = curses.newwin(11, 13, PADDING, PADDING)
        self.trump_window.erase()
        self.trump_window.attron(
            curses.color_pair(self.g.hands[self.active][12].color()))
        self.trump_window.addstr(
            self.g.hands[self.active][12].ascii_rep())
        self.trump_window.refresh()

    def test_draw_info_windows(self):
        for i in range(len(self.g.players)):
            if i == self.active_position:
                self.info_windows[0] = curses.newwin(I_HEIGHT, I_WIDTH, (2*PADDING)+(2*C_HEIGHT)+(12*V_SPACING), (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.info_windows[0].erase()
                self.info_windows[0].addstr('\n '+self.g.players[i]+'\n')
                self.info_windows[0].addstr(" Bid: 0\n")
                self.info_windows[0].addstr(" Won: 0\n")
                self.info_windows[0].box()
                self.info_windows[0].refresh()
            elif i == (self.active_position + 1) % 4:
                self.info_windows[1] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH)
                self.info_windows[1].erase()
                self.info_windows[1].addstr('\n '+self.g.players[i]+'\n')
                self.info_windows[1].addstr(" Bid: 0\n")
                self.info_windows[1].addstr(" Won: 0\n")
                self.info_windows[1].box()
                self.info_windows[1].refresh()
            elif i == (self.active_position + 2) % 4:
                self.info_windows[2] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT-PADDING, (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.info_windows[2].erase()
                self.info_windows[2].addstr('\n '+self.g.players[i]+'\n')
                self.info_windows[2].addstr(" Bid: 0\n")
                self.info_windows[2].addstr(" Won: 0\n")
                self.info_windows[2].box()
                self.info_windows[2].refresh()
                continue
            elif i == (self.active_position + 3) % 4:
                self.info_windows[3] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH+(12*H_SPACING))
                self.info_windows[3].erase()
                self.info_windows[3].addstr('\n '+self.g.players[i]+'\n')
                self.info_windows[3].addstr(" Bid: 0\n")
                self.info_windows[3].addstr(" Won: 0\n")
                self.info_windows[3].box()
                self.info_windows[3].refresh()
                continue

    def init_display(self):
        self.window.erase()
        self.window.refresh()

        for player in self.g.players:
            self.draw_hand(player)

        self.test_draw_play()
        self.test_draw_trump()
        self.test_draw_info_windows()

        self.run()
