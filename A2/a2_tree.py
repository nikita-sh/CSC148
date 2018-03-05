"""
Bare bones Tree ADT for iterative minimax.
"""

from typing import List, Union


class MinimaxTree:
    """
    Tree ADT that identifies the root with the entire tree. Has score and move
    attributes for iterative minimax simulation.

    ===Attributes===
    value: value of the root node
    move: move made to reach current state
    score: minimax score of move after evaluation
    children: children of the root
    """
    value: object
    move: Union[str, int]
    score: int
    children: List['MinimaxTree']

    def __init__(self, value: object = None, move: object = None,
                 score: int = None,
                 children: List['MinimaxTree'] = None) -> None:
        """
        Create Tree self with content value, 0 or more children, score and move.
        """
        self.value = value
        self.move = move
        self.score = score
        self.children = children.copy() if children else []


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
