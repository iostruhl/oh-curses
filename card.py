class Card:
    rank_values = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }

    suit_ascii = {
        "clubs": '♣',
        "diamonds": '♦',
        "spades": '♠',
        "hearts": '♥'
    }
    def __init__(self, rank: str, suit: str):
        assert(rank in self.rank_values)
        self.rank = rank
        assert(suit in self.suit_ascii)
        self.suit = suit
        self.visible = False

    def set_visible(self):
        self.visible = True

    def set_hidden(self):
        self.visible = False

    def ascii_rep(self) -> str:
        if (self.visible):
            return (
                "\
┌─────────┐\n\
│{}       │\n\
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

    def color(self) -> int:
        colors = {
            "spades": 0,
            "hearts": 1,
            "clubs": 2,
            "diamonds": 4
        }
        return colors[self.suit]


