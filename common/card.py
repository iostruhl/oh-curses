class Card:
    rank_values = {
        "2"  : 2,
        "3"  : 3,
        "4"  : 4,
        "5"  : 5,
        "6"  : 6,
        "7"  : 7,
        "8"  : 8,
        "9"  : 9,
        "10" : 10,
        "J"  : 11,
        "Q"  : 12,
        "K"  : 13,
        "A"  : 14
    }

    suit_ascii = {
        "clubs"    : '♣',
        "diamonds" : '♦',
        "spades"   : '♠',
        "hearts"   : '♥'
    }

    colors = {
        "spades"   : 0,
        "hearts"   : 1,
        "clubs"    : 2,
        "diamonds" : 4
    }

    def __init__(self, rank: str = None, suit: str = None):
        self.rank = rank
        self.value = self.rank_values[rank] if rank else None
        self.suit = suit
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def color(self) -> int:
        return self.colors[self.suit]

    def trick_value(self, led_suit, trump_suit) -> int:
        if (self.suit == trump_suit):
            return 100 + self.value
        if (self.suit == led_suit):
            return self.value
        return 0

    def to_array(self) -> list:
        return [self.rank, self.suit]

    # ABSOLUTELY NEED THIS FOR LIST MEMBERSHIP
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return NotImplemented

    # Needed for hand sorting (i.e. organization)
    def __lt__(self, other):
        if isinstance(other, Card):
            if Card.colors[self.suit] == Card.colors[other.suit]:
                return self.value > other.value
            else:
                return Card.colors[self.suit] > Card.colors[other.suit]
        return NotImplemented

    # Makes printing cards nice (for debugging)
    def __repr__(self):
        return "{:s}{:s}".format(self.rank, self.suit_ascii[self.suit])

    # Prints the visual representation of the card, for curses graphics
    def ascii_rep(self) -> str:
        if (self.visible):
            return (
                "\
┌─────────┐\n\
│{}{}     │\n\
│         │\n\
│         │\n\
│    {}   │\n\
│         │\n\
│         │\n\
│       {}│\n\
└─────────┘\
                ".format(
                    format(self.rank, ' <2'),
                    format(self.suit_ascii[self.suit], ' ^2'),
                    format(self.suit_ascii[self.suit], ' ^2'),
                    format(self.rank, ' >2'),
                    )
                )
        else:
            return (
                "\
┌─────────┐\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
│░░░░░░░░░│\n\
└─────────┘\
")

# testing card
if __name__ == "__main__":
    c = Card("K", "clubs")
    d = Card("10", "diamonds")
    print(c.ascii_rep())
    c.set_visible()
    d.set_visible()
    print(c.ascii_rep())
    print(d.ascii_rep())
