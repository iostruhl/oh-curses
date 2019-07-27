rank_map = dict()
rank_map['A'] = (
    "┌─────────┐\n"
    "│A        │\n"
    "│x        │\n"
    "│         │\n"
    "│    █    │\n"
    "│         │\n"
    "│        x│\n"
    "│        A│\n"
    "└─────────┘")
rank_map['2'] = (
    "┌─────────┐\n"
    "│2        │\n"
    "│x   x    │\n"
    "│         │\n"
    "│         │\n"
    "│         │\n"
    "│    x   x│\n"
    "│        2│\n"
    "└─────────┘")
rank_map['3'] = (
    "┌─────────┐\n"
    "│3        │\n"
    "│x   x    │\n"
    "│         │\n"
    "│    x    │\n"
    "│         │\n"
    "│    x   x│\n"
    "│        3│\n"
    "└─────────┘")
rank_map['4'] = (
    "┌─────────┐\n"
    "│4        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│         │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        4│\n"
    "└─────────┘")
rank_map['5'] = (
    "┌─────────┐\n"
    "│5        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│    x    │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        5│\n"
    "└─────────┘")
rank_map['6'] = (
    "┌─────────┐\n"
    "│6        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│   x x   │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        6│\n"
    "└─────────┘")
rank_map['7'] = (
    "┌─────────┐\n"
    "│7        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x  x│\n"
    "│        7│\n"
    "└─────────┘")
rank_map['8'] = (
    "┌─────────┐\n"
    "│8        │\n"
    "│x  x x   │\n"
    "│    x    │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x  x│\n"
    "│        8│\n"
    "└─────────┘")
rank_map['9'] = (
    "┌─────────┐\n"
    "│9        │\n"
    "│x  x x   │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x   │\n"
    "│   x x  x│\n"
    "│        9│\n"
    "└─────────┘")
rank_map['10'] = (
    "┌─────────┐\n"
    "│10       │\n"
    "│x  x x   │\n"
    "│   x x   │\n"
    "│   x x   │\n"
    "│   x x   │\n"
    "│   x x  x│\n"
    "│       10│\n"
    "└─────────┘")
rank_map['J'] = (
    "┌─────────┐\n"
    "│J        │\n"
    "│x █████  │\n"
    "│    █    │\n"
    "│    █    │\n"
    "│  █ █    │\n"
    "│  ███   x│\n"
    "│        J│\n"
    "└─────────┘")
rank_map['Q'] = (
    "┌─────────┐\n"
    "│Q        │\n"
    "│x  ███   │\n"
    "│  █   █  │\n"
    "│  █   █  │\n"
    "│  █  ██  │\n"
    "│   ██ █ x│\n"
    "│        Q│\n"
    "└─────────┘")
rank_map['K'] = (
    "┌─────────┐\n"
    "│K        │\n"
    "│x █   █  │\n"
    "│  █  █   │\n"
    "│  █ █    │\n"
    "│  █  █   │\n"
    "│  █   █ x│\n"
    "│        K│\n"
    "└─────────┘")

def individual_ascii_rep(rank: str, suit: str):
    return rank_map[rank].replace("x", suit)
