import curses
from curses import panel
from .boardstate import ClientBoard
import logging

PADDING = 1
V_SPACING = 1
H_SPACING = 5
C_HEIGHT = 11
C_WIDTH = 13
I_HEIGHT = 5
I_WIDTH = C_HEIGHT
B_HEIGHT = 3
B_WIDTH = 4

class GraphicsBoard:

    def __init__(self, cb: ClientBoard):
        # Set up curses
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.stdscr.erase()
        self.stdscr.refresh()

        self.cb = cb
        self.hand_position = 0
        self.bid_position = 0
        self.hand_windows = [[] for player in cb.players]
        self.hand_panels = [[] for player in cb.players]
        self.played_windows = [None for player in cb.players]
        self.trump_window = None
        self.info_windows = [None for player in cb.players]
        logging.basicConfig(filename="log.txt", level=logging.DEBUG)

    def hand_navigate(self, n):
        hand_len = len(self.cb.hands[self.cb.active])
        self.clear_hand_card(self.cb.active, self.hand_position)
        self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
        self.hand_position = (self.hand_position + n) % len(self.cb.hands[self.cb.active])
        self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT-2, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
        if (n < 0 and self.hand_position == (len(self.cb.hands[self.cb.active]) - 1)):
            self.redraw_hand(0)
        else:
            self.redraw_hand(self.hand_position - 1)

    def draw_new_hand(self, hand_size: int):
        for i in range(len(self.cb.players)):
            if i == self.cb.active_position:
                self.hand_windows[0] = [curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(j*H_SPACING))
                                        for j in range(hand_size)]
                self.hand_panels[0] = [panel.new_panel(self.hand_windows[0][j])
                                       for j in range(hand_size)]
            elif i == (self.cb.active_position + 1) % 4:
                self.hand_windows[1] = [curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT+(j*V_SPACING), PADDING)
                                        for j in range(hand_size)]
                self.hand_panels[1] = [panel.new_panel(self.hand_windows[1][j])
                                       for j in range(hand_size)]
            elif i == (self.cb.active_position + 2) % 4:
                self.hand_windows[2] = [curses.newwin(C_HEIGHT, C_WIDTH, PADDING, (2*PADDING)+C_WIDTH+(j*H_SPACING))
                                        for j in range(hand_size)]
                self.hand_panels[2] = [panel.new_panel(self.hand_windows[2][j])
                                       for j in range(hand_size)]
            elif i == (self.cb.active_position + 3) % 4:
                self.hand_windows[3] = [curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT+(j*V_SPACING), (3*PADDING)+(2*C_WIDTH)+(12*H_SPACING))
                                        for j in range(hand_size)]
                self.hand_panels[3] = [panel.new_panel(self.hand_windows[3][j])
                                       for j in range(hand_size)]
            self.draw_hand(self.cb.players[i])
        self.draw_new_info_window()

    def collapse_hand(self, player_position):
        for window in self.hand_windows[0]:
            window.erase()
            window.refresh()
        hand_size = len(self.cb.hands[self.cb.players[player_position]])
        self.hand_windows[0] = [curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(i*H_SPACING))
                                for i in range(hand_size)]
        self.hand_panels[0] = [panel.new_panel(self.hand_windows[0][i])
                               for i in range(hand_size)]
        self.draw_hand(self.cb.players[player_position])

    def refresh_info_window(self, player):
        player_position = (self.cb.players.index(player) - self.cb.active_position) % 4
        self.info_windows[player_position].erase()
        self.info_windows[player_position].addstr('\n '+player+'\n')
        self.info_windows[player_position].addstr(' '+f'Bid: {self.cb.bids[player]}'+'\n')
        self.info_windows[player_position].addstr(' '+f'Won: {self.cb.won[player]}')
        self.info_windows[player_position].box()
        self.info_windows[player_position].refresh()

    def draw_new_info_window(self):
        for i in range(len(self.cb.players)):
            if i == self.cb.active_position:
                self.info_windows[0] = curses.newwin(I_HEIGHT, I_WIDTH, (2*PADDING)+(2*C_HEIGHT)+(12*V_SPACING), (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.info_windows[0].erase()
                self.info_windows[0].addstr('\n '+self.cb.players[i]+'\n')
                self.info_windows[0].box()
                self.info_windows[0].refresh()
            elif i == (self.cb.active_position + 1) % 4:
                self.info_windows[1] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH)
                self.info_windows[1].erase()
                self.info_windows[1].addstr('\n '+self.cb.players[i]+'\n')
                self.info_windows[1].box()
                self.info_windows[1].refresh()
            elif i == (self.cb.active_position + 2) % 4:
                self.info_windows[2] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT-PADDING, (2*PADDING)+C_WIDTH+(6*H_SPACING))
                self.info_windows[2].erase()
                self.info_windows[2].addstr('\n '+self.cb.players[i]+'\n')
                self.info_windows[2].box()
                self.info_windows[2].refresh()
            elif i == (self.cb.active_position + 3) % 4:
                self.info_windows[3] = curses.newwin(I_HEIGHT, I_WIDTH, C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH+(12*H_SPACING))
                self.info_windows[3].erase()
                self.info_windows[3].addstr('\n '+self.cb.players[i]+'\n')
                self.info_windows[3].box()
                self.info_windows[3].refresh()

    def get_card(self):
        self.hand_windows[0][self.hand_position].mvwin((4*PADDING)+(2*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT-2, (2*PADDING)+C_WIDTH+(self.hand_position*H_SPACING))
        self.redraw_hand(0)
        while True:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, ord('\n')]:
                played_card = self.cb.hands[self.cb.active].pop(self.hand_position)
                self.collapse_hand(self.cb.active_position)
                return played_card
            elif key == curses.KEY_LEFT:
                self.hand_navigate(-1)
            elif key == curses.KEY_RIGHT:
                self.hand_navigate(1)

    def play_card(self, player, card):
        player_position = (self.cb.players.index(player) - self.cb.active_position) % 4
        if player_position == 0:
            self.played_windows[0] = curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT+(12*V_SPACING), (2*PADDING)+C_WIDTH+(6*H_SPACING))
        elif player_position == 1:
            self.played_windows[1] = curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT+(6*V_SPACING), (2*PADDING)+C_WIDTH+(3*H_SPACING))
        elif player_position == 2:
            self.played_windows[2] = curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT, (2*PADDING)+C_WIDTH+(6*H_SPACING))
        elif player_position == 3:
            self.played_windows[3] = curses.newwin(C_HEIGHT, C_WIDTH, (4*PADDING)+C_HEIGHT+(6*V_SPACING), (2*PADDING)+C_WIDTH+(9*H_SPACING))
        self.played_windows[player_position].erase()
        self.played_windows[player_position].attron(curses.color_pair(card.color()))
        self.played_windows[player_position].addstr(card.ascii_rep())
        self.played_windows[player_position].refresh()
        self.refresh_info_window(self.cb.active)

    def start_hand(self):
        for player in self.cb.players:
            self.refresh_info_window(player)

    def bid_navigate(self, n, hand_size, is_dealer):
        possible_bids = hand_size + 1
        self.bid_position = (self.bid_position + n) % possible_bids
        if is_dealer and ((hand_size - sum(self.cb.bids.values())) == self.bid_position):
            self.bid_position = (self.bid_position + n) % possible_bids

    def receive_bid(self, player, bid):
        player_position = (self.cb.players.index(player) - self.cb.active_position) % 4
        self.info_windows[player_position].addstr(" Bid: %i\n" % bid)
        self.info_windows[player_position].box()
        self.info_windows[player_position].refresh()

    def draw_bids(self, hand_size, is_dealer):
        self.bid_windows = [curses.newwin(B_HEIGHT, B_WIDTH, (3*PADDING)+(3*C_HEIGHT)+(12*V_SPACING)+I_HEIGHT, (2*PADDING)+C_WIDTH+(i*B_WIDTH))
                            for i in range(hand_size + 1)]

        for window in self.bid_windows:
            window.erase()
            if is_dealer and ((hand_size - sum(self.cb.bids.values())) == self.bid_windows.index(window)):
                continue
            window.addstr("\n %i" % self.bid_windows.index(window))
            if self.bid_windows.index(window) == self.bid_position:
                window.attron(curses.A_REVERSE)
            window.box()
            window.refresh()

    def get_bid(self, hand_size, is_dealer):
        while (True):
            self.draw_bids(hand_size, is_dealer)
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, ord('\n')]:
                for window in self.bid_windows:
                    window.erase()
                    window.refresh()
                return self.bid_position
            elif key == curses.KEY_LEFT:
                self.bid_navigate(-1, hand_size, is_dealer)
            elif key == curses.KEY_RIGHT:
                self.bid_navigate(1, hand_size, is_dealer)

    def draw_hand_card(self, player, card):
        player_position = (self.cb.players.index(player) - self.cb.active_position) % 4
        self.hand_windows[player_position][card].erase()
        if (self.cb.hands[player][card].visible):
            self.hand_windows[player_position][card].attron(
            curses.color_pair(self.cb.hands[player][card].color()))
        # else:
        #     self.hand_windows[player_position][card].attroff(
        #     curses.color_pair(self.cb.hands[player][card].color()))
        self.hand_windows[player_position][card].addstr(
            self.cb.hands[player][card].ascii_rep())
        self.hand_windows[player_position][card].refresh()

    def clear_hand_card(self, player, card):
        player_position = (self.cb.players.index(player) - self.cb.active_position) % 4
        self.hand_windows[player_position][card].erase()
        self.hand_windows[player_position][card].refresh()

    def draw_hand(self, player):
        for card in range(len(self.cb.hands[player])):
            self.draw_hand_card(player, card)

    def redraw_hand(self, position):
        for card in range(position, len(self.cb.hands[self.cb.active])):
            self.draw_hand_card(self.cb.active, card)

    def test_draw_trump(self):
        self.trump_window = curses.newwin(C_HEIGHT, C_WIDTH, PADDING, PADDING)
        self.trump_window.erase()
        self.trump_window.attron(
            curses.color_pair(self.cb.hands[self.cb.active][12].color()))
        self.trump_window.addstr(
            self.cb.hands[self.cb.active][12].ascii_rep())
        self.trump_window.refresh()
