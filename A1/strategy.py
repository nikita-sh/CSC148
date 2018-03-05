"""
Contains strategies for players in game_interface.
"""

from games import *
import random


def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def random_strategy(game: Game) -> Any:
    """
    Returns a random strategy from available strategies, based on the state.

    ~No Docstests provided as they rely on input/random factors~
    """
    game_st = game.current_state
    poss = game_st.get_possible_moves()
    return random.choice(poss)
