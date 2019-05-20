from pygase import GameState, Backend
from card import Card
import random

initial_game_state = GameState(
    deck = [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values],
    players = [],
    in_play = {}, # {player:None for player in self.players}
    hands = {}, #{player:[] for player in self.players}
    bids = {}, #{player:0 for player in self.players}
    cards_taken = {}, # {player:[] for player in self.players}
    trump_suit = None,
    led_suit = None,
    hand_num = 1,
    next_action = "Wait For Players"
)

# # this game is only handled in events, so nothing will ever be updated in time
# def time_step(gs, dt):
#     return {}

# b = Backend(initial_game_state, time_step)

# def on_join(player_name, game_state, client_address, **kwargs):
#     print(player_name, "joined.")
#     backend.server.dispatch_event("JOINED", resp = "SUCCESS", target_client = client_address)
#     if ()
#     return {
#         "players": game_state.players + [player_name]
#     }

# gs is the current game state, dt is unused
def time_step(gs, dt):
    if gs.next_action == "Wait For Players":
        if (len(gs.players) != 4):
            return {}
        # move on when we have 4 players
        return {"next_action": "Decide Dealer"}

    if gs.next_action == "Decide Dealer":
        shuffled_players = random.sample(gs.players, len(gs.players))
        shuffled_deck = random.sample(gs.deck, len(gs.deck))
        return {
            "deck": shuffled_deck, 
            "players": shuffled_players, 
            "next_action": "Deal Hand"
        }

    if gs.next_action == "Deal Hand":
        shuffled_deck = random.sample(gs.deck, len(gs.deck))
        hands = {player:[] for player in gs.players}

        for player in gs.players:
            for _ in range(gs.hand_num):
                hands[player].append(shuffled_deck.pop())
        trump_suit = shuffled_deck[0].suit

        return {
            "deck": shuffled_deck,
            "hands": hands,
            "trump_suit": trump_suit,
            "next_action": "Wait For Bids"
        }

    if gs.next_action == "Wait For Bids":
        if (len(gs.bids) != 4):
            return {}
        # move on when everyone has bid
        return {"next_action": "Wait For Trick Completion"}

    if gs.next_action == "Wait For Trick Completion":
        if (len (gs.in_play) != 4):
            return {}
        # move on when everyone has played
        return {"next_action": "Finish Trick"}

    if gs.next_action == "Finish Trick":
        winner = max(gs.in_play, key=lambda x: Card.trick_value(gs.in_play[x], gs.led_suit, gs.trump_suit))
        print("Winner is", winner)

        cards_taken = gs.cards_taken.copy()
        cards_taken[winner].extend(gs.in_play.values())

        next_action = "Wait For Trick Completion" if len(gs.hands.values()[0]) > 0 else "Finish Hand"
        return {
            "in_play": {},
            "cards_taken": cards_taken,
            "led_suit": None,
            "next_action": next_action
        }

    if gs.next_action == "Finish Hand":

        return {
            "deck": [Card(rank, suit) for suit in Card.suit_ascii for rank in Card.rank_values],
            "hands": {},
            "cards_taken": {},
            "trump_suit": None,
            "hand_num": gs.hand_num + 1,
            "next_action": "Deal Hand"
        }



