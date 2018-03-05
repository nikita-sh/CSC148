"""
A module for strategies.
"""
from typing import Union
from a2_tree import MinimaxTree
from a2_stack import Stack
from game import Game
from game_state import GameState


def interactive_strategy(game: Game) -> Union[str, int]:
    """
    Return a move for game through interactively asking the user for input.

    ~Doctests omitted due to use of input~
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Game) -> Union[str, int]:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_minimax_strategy(game: Game, game_state: GameState = None)\
                                            -> Union[str, int]:
    """
    Returns move from given game state recursively using minimax strategy.
    """
    # checking for optional parameter game_state
    if game_state:
        # checking if game is over
        if game.is_over(game_state):
            curr_player = game_state.get_current_player_name()
            orig_state = game.current_state
            # set current state to game_state to make use of is_over(), reset
            # state to original to assure current_state isnt changed before
            # return
            game.current_state = game_state
            # getting score of finished state
            if game.is_winner(curr_player):
                game.current_state = orig_state
                return 1
            elif game.is_winner("p1" if curr_player == "p2" else "p2"):
                game.current_state = orig_state
                return -1
            game.current_state = orig_state
            return 0
        # returning tuple of maximum score, and move made to achieve it
        moves = game_state.get_possible_moves()
        states = [game_state.make_move(i) for i in moves]
        return max([-1 * recursive_minimax_strategy(game, states[x])
                    for x in range(len(moves))])

    # checking if game is over
    if game.is_over(game.current_state):
        curr_player = game.current_state.get_current_player_name()
        orig_state = game.current_state
        # set current state to game_state to make use of is_over(), reset state
        # to original to assure current_state isnt changed before return
        game.current_state = game_state
        # setting score of finished game
        if game.is_winner(curr_player):
            game.current_state = orig_state
            return 1
        elif game.is_winner("p1" if curr_player == "p2" else "p2"):
            game.current_state = orig_state
            return -1
        game.current_state = orig_state
        return 0
    # returning tuple of maximum score and move made and passing optional states
    # parameter on recursive call
    moves = game.current_state.get_possible_moves()
    states = [game.current_state.make_move(i) for i in moves]
    return max([(-1 * recursive_minimax_strategy(game, states[x]), moves[x])
                for x in range(len(moves))])[1]


def iterative_minimax_strategy(game: Game) -> Union[str, int]:
    """
    Returns move from given game state iteratively using minimax strategy.
    """
    # initializing stack to hold states and tree with root current state
    states = Stack()
    game_tree = MinimaxTree(game.current_state)
    orig_state = game.current_state
    ret = None
    # add root to stack
    states.add(game_tree)
    while not states.is_empty():
        curr = states.remove()
        # gets all possible states stemming from root, adding them to
        # appropriate children lists, and adding them back to the stack
        if not curr.children and curr.value.get_possible_moves():
            # re-add root state first to be able to satisfy terminal condition
            # after weve added all states
            states.add(curr)
            for move in curr.value.get_possible_moves():
                new_root = MinimaxTree(curr.value.make_move(move), move)
                curr.children.append(new_root)
                states.add(new_root)
        # after states have been added, checks that the game is over at that
        # node by evaluating children and get_possible_moves()
        elif not curr.children and not curr.value.get_possible_moves():
            game.current_state = curr.value
            curr_player = curr.value.get_current_player_name()
            # sets score of MinimaxTree
            if game.is_winner(curr_player):
                curr.score = 1
            elif game.is_winner("p1" if curr_player == "p2" else "p2"):
                curr.score = -1
            else:
                curr.score = 0
        # if states is empty, we've reached the root, i.e. the original state;
        # evaluate this states score and best possible move by looking at the
        # scores of its children and return appropriate move
        else:
            if states.is_empty():
                ret = max([(-1 * i.score, i.move) for i in curr.children])[1]
            else:
                curr.score = max([-1 * j.score for j in curr.children])
    # assuring that root state is not changed by minimax simulation
    game.current_state = orig_state
    return ret

