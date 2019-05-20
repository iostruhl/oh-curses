from card import Card
from random import shuffle

class GameBoard:

    def __init__(self, players = ["Isaac", "Alex", "Ben", "Owen"]):
        self.deck = [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values]
        self.players = players
        self.in_play = {player:None for player in self.players}
        self.hands = {player:[] for player in self.players}
        self.cards_taken = {player:[] for player in self.players}
        self.trump_suit = None
        self.led_suit = None

    # collect all cards back into deck
    # just reinitializes everything
    def collect_cards(self):
        self.deck = [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values]
        self.in_play = {player:None for player in self.players}
        self.hands = {player:[] for player in self.players}
        self.cards_taken = {player:[] for player in self.players}

    # shuffles the deck
    def shuffle(self):
        # we can only shuffle a full deck
        assert(len(self.deck) == 52)
        shuffle(self.deck)

    # deals the specified hand
    def deal_hand(self, hand_num: int):
        print("Dealing hand...", end = "")
        # can only deal from a full deck
        assert(len(self.deck) == 52)
        for player in self.players:
            for _ in range(hand_num):
                self.hands[player].append(self.deck.pop())
        self.trump_suit = self.deck[0].suit
        print("trump suit is", self.trump_suit)

    # put a card from a specifed player into play
    def play_card(self, player: str, card: Card, lead = False):
        print("Playing card", card, "from player", player, "(trick lead)" if lead else "")
        # can only play a card if it's in your hand
        assert(card in self.hands[player])
        # player must not have already played a card
        assert(self.in_play[player] is None)
        if (lead):
            assert(self.led_suit is None)
            self.led_suit = card.suit

        self.in_play[player] = card
        self.hands[player].remove(card)

    # calculate the winner of the trick,
    # update trick piles, and
    # clear in_play
    def finish_trick(self):
        print("Finishing trick")
        # everyone must have played a card
        for player in self.in_play:
            assert(self.in_play[player] is not None)

        # calculate winner
        winner = max(self.in_play, key=lambda x: Card.trick_value(self.in_play[x], self.led_suit, self.trump_suit))
        print("Winner is", winner)
        # move cards in play to the winner's pile
        self.cards_taken[winner].extend(self.in_play.values())
        # clear the cards in play
        self.in_play = {player: None for player in self.players}
        self.led_suit = None


if __name__ == "__main__":
    g = GameBoard()
    g.shuffle()
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

