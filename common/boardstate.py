from .card import Card
from random import shuffle

class GameBoard:

    def __init__(self, players = ["Isaac", "Alex", "Ben", "Owen"]):
        shuffle(players) # decides dealer
        self.deck = [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values]
        self.players = players
        self.in_play = dict()
        self.hands = {player:[] for player in self.players}
        self.scores = {player:0 for player in self.players}
        self.bids = dict()
        self.cards_taken = {player:[] for player in self.players}
        self.trump_card = None
        self.led_suit = None

    # collect all cards back into deck
    # just reinitializes everything
    def collect_cards(self):
        self.deck = [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values]
        self.in_play = {}
        self.hands = {player:[] for player in self.players}
        self.bids = dict()
        self.cards_taken = {player:[] for player in self.players}
        self.trump_card = None
        self.led_suit = None

    # deals the specified hand
    def deal_hand(self, hand_num: int):
        print("Dealing hand...", end = "")
        # can only deal from a full deck
        assert (len(self.deck) == 52), "Not dealing from a full deck"
        shuffle(self.deck)

        for player in self.players:
            for _ in range(hand_num):
                self.hands[player].append(self.deck.pop())
        if (hand_num < 13):
            self.trump_card = self.deck[0]
        else:
            self.trump_card = None
        print("trump card is", self.trump_card)

    # assigns a bid to a player
    def bid(self, player: str, bid: int):
        print("Player", player, "bids", bid)
        assert (player not in self.bids), "Player has already bid"
        self.bids[player] = bid

    # put a card from a specifed player into play
    def play_card(self, player: str, card: Card, lead = False):
        # can only play a card if it's in your hand
        assert (card in self.hands[player]), "Card not in %s's hand" % player
        # player must not have already played a card
        assert (player not in self.in_play), "%s has already played a card" % player
        print("Playing card", card, "from player", player, "(trick lead)" if lead else "")
        if (lead):
            assert (self.led_suit is None), "Led suit is already set???"
            self.led_suit = card.suit

        self.in_play[player] = card
        self.hands[player].remove(card)

    # calculate the winner of the trick,
    # update trick piles, and
    # clear in_play
    def finish_trick(self) -> str:
        print("Finishing trick")
        # everyone must have played a card
        for player in self.in_play:
            assert (self.in_play[player] is not None), "Finish trick: not everyone has played a card"

        # calculate winner
        winner = max(self.in_play, key=lambda x: Card.trick_value(
            self.in_play[x], 
            self.led_suit, 
            self.trump_card.suit if self.trump_card else None))
        print("Winner is", winner)
        # move cards in play to the winner's pile
        self.cards_taken[winner].extend(self.in_play.values())
        # clear the cards in play
        self.in_play = {}
        self.led_suit = None
        return winner

    def update_scores(self) -> dict:
        handscores = dict()
        for player in self.players:
            if len(self.cards_taken[player]) / 4 == self.bids[player]: # made hand
                handscores[player] = int(10 + (self.bids[player] ** 2))
            else:
                diff = abs((len(self.cards_taken[player]) / 4) - self.bids[player])
                handscores[player] = int(-5 * (diff * (diff + 1)) / 2)
            # update aggreate scores
            self.scores[player] += handscores[player]

        return handscores


    # Unused - just asserts that nobody has any cards in their hand
    def assert_hand_done(self):
        for player in self.hands:
            assert (self.hands[player] == []), "Hand done: not everyone's hands are empty"


class ClientBoard:

    def __init__(self, players, active):
        self.players = players
        self.active = active
        self.active_position = players.index(active)
        self.hands = {player:[] for player in players}
        self.won = {player:0 for player in players}
        self.in_play = {player:None for player in players}
        self.scores = {player:0 for player in players}
        self.bids = dict()
        self.trump_card = None
        self.lead_card = None
        self.dealer = None
        self.actor = None

    def get_hand(self, dealt_hand):
        for player in self.hands.keys():
            if player == self.active:
                self.hands[player] = [Card(card[0], card[1]) for card in dealt_hand]
                for card in self.hands[player]:
                    card.show()
            else:
                self.hands[player] = [Card() for card in dealt_hand]

    def is_playable(self, card):
        # are you leading?
        if not self.lead_card:
            return True
        # are you following suit?
        if card.suit == self.lead_card.suit:
            return True
        # can you follow suit?
        for c in self.hands[self.active]:
            if c.suit == self.lead_card.suit:
                return False

        return True


# testing gameboard
if __name__ == "__main__":
    g = GameBoard()
    g.deal_hand(2)
    print("hands now are ", g.hands)
    for _ in range(2):
        print("playing trick")
        g.play_card(g.players[0], g.hands[g.players[0]][0], lead = True)
        g.play_card(g.players[1], g.hands[g.players[1]][0])
        g.play_card(g.players[2], g.hands[g.players[2]][0])
        g.play_card(g.players[3], g.hands[g.players[3]][0])
        print("hands now are ", g.hands)
        print("in play now is ", g.in_play)
        g.finish_trick()
        print("in play now is ", g.in_play)
        print("cards taken now are", g.cards_taken)
    g.assert_hand_done()

