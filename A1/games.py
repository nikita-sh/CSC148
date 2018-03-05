"""
Contains Game superclass with Chopsticks and Subtract Square subclasses as well
as GameState superclass with Chopsticks and Subtract Square state subclasses.
"""

from typing import *


class Game:
    """
    Initializes a zero-sum, perfect information, two player, sequential game and
    keeps track of the state of the game. This is a superclass not meant for
    instantiating any games but rather gathering attributes/methods
    common to all types of similar games.

    ===Attributes===
    current_state: current state of the game
    instructions: instructions of how to play game
    player1_start: True if player 1 is the first to make a turn, false if not
    """
    current_state: Any
    instructions: str
    player1_start: bool

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes an instance of a zero-sum, perfect information,
        two player, sequential game. Extended in Chopsticks and SubSquare.
        """
        self.player1_start = player1_start

    def __str__(self) -> str:
        """
        Returns a string representation of Game.
        """
        raise NotImplementedError("Override this.")

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether Game self is equal to other
        """
        raise NotImplementedError("Override this.")

    def get_instructions(self) -> str:
        """
        Returns instructions for the game being played.

        >>> g = Game(True)
        >>> g.instructions = "abc"
        >>> g.get_instructions()
        'abc'
        """
        return self.instructions

    def is_over(self, current_state: 'Game') -> bool:
        """
        Returns whether or not Game is over based on current_state.
        """
        raise NotImplementedError("Override this.")

    def is_winner(self, player: str) -> bool:
        """
        Returns whether or not player is the winner of a finished game.
        """
        raise NotImplementedError("Override this.")

    def str_to_move(self, string: str) -> Any:
        """
        Returns a valid move based on string.
        """
        raise NotImplementedError("Override this.")


class Chopsticks(Game):
    """
    Initializes a game state of an instance of the game Chopsticks. A subclass
    of Game. Overrides is_over, is_winner, __eq__, __str__, and str_to_move
    methods. Extends __init__.

    ===Attributes===
    current_state: current state of the game
    instructions: instructions of how to play game
    player1_start: whether or not player 1 is the first to make a turn
    """
    current_state: 'ChopState'
    instructions: str
    player1_start: bool

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes a new game of Chopsticks

        >>> c = Chopsticks(True)
        """
        Game.__init__(self, player1_start)
        self.current_state = ChopState(player1_start)
        self.instructions = "Each two players begin with one finger " \
                            "pointed up on each of their hands. Player " \
                            "A touches one hand to one of Player B’s " \
                            "hands, increasing the number of fingers " \
                            "pointing up on Player B’s hand by the number " \
                            "on Player A’s hand. The number pointing up " \
                            "on Player A’s hand remains the same. If Player " \
                            "B now has five fingers up, that hand becomes " \
                            "‘dead’ or unplayable. If the number of fingers " \
                            "should exceed five, subtract five from the " \
                            "sum. Now Player B touches one hand to one of " \
                            "Player A’s hands, and the distribution of " \
                            "fingers proceeds as above, including the " \
                            "possibility of a ‘dead’ hand. Play repeats " \
                            "until some player has two ‘dead’ hands, " \
                            "thus losing."

    def __str__(self) -> str:
        """
        Returns a string representation of Game.

        >>> c = Chopsticks(True)
        >>> print(c)
        Player 1: Left 1 - 1 Right; Player 2: Left 1 - 1 Right
        """
        return str(self.current_state)

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether a Game self is equal to other.

        >>> c = Chopsticks(True)
        >>> c1 = Chopsticks(True)
        >>> c2 = Chopsticks(False)
        >>> c == c1
        True
        >>> c == c2
        False
        """
        return (type(self) == type(other) and
                self.current_state == other.current_state)

    def is_over(self, current_state: 'ChopState') -> bool:
        """
        Returns whether or not Game is over based on current_state.

        >>> c = Chopsticks(True)
        >>> c.is_over(c.current_state)
        False
        """
        if current_state.p1_left == 0 and current_state.p1_right == 0:
            return True
        elif current_state.p2_left == 0 and current_state.p2_right == 0:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Returns whether or not player is the winner of a finished game.

        >>> c = Chopsticks(True)
        >>> c.is_winner('p1')
        False
        """
        if not self.is_over(self.current_state):
            return False
        elif self.current_state.current_player == player:
            return False
        else:
            return True

    def str_to_move(self, string: str) -> Any:
        """
        Returns string converted to a valid move.

        >>> c = Chopsticks(True)
        >>> print(c.str_to_move('ll'))
        ll
        """
        return string


class SubSquare(Game):
    """
    Initializes a game state of an instance of the game Subtract Square. A
    subclass of Game. Overrides is_over, is_winner, __eq__, __str__, and
    str_to_move methods. Extends __init__.

    ===Attributes===
    current_state: current state of the game
    instructions: instructions of how to play game
    player1_start: True if player 1 is the first to make a turn, false if not
    """
    current_state: 'SubSquareState'
    instructions: str
    player1_start: bool

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes a new game of Subtract Square

        ~No Docstests provided as they rely on input~
        """
        Game.__init__(self, player1_start)
        self.current_state = SubSquareState(player1_start)
        self.current_state.current_val = int(input("Enter a starting value:"))
        self.instructions = "A positive whole number is chosen as " \
                            "the starting value by some entity. In " \
                            "our case, one of the players will pick a " \
                            "number. The player whose turn it is chooses " \
                            "some square of a positive whole number (such " \
                            "as 1, 4, 9, 16) to subtract from the value, " \
                            "provided the chosen square is not larger. " \
                            "After subtracting, we have a new value and " \
                            "the next player chooses a square to subtract " \
                            "from it. Play continues to alternate between " \
                            "the two players until no moves are possible. " \
                            "Whoever is about to play at that point loses."

    def __str__(self) -> str:
        """
        Returns a string representation of Game.

        ~No Docstests provided as they rely on input~
        """
        return str(self.current_state)

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether a Game self is equal to other.

        ~No Docstests provided as they rely on input~
        """
        return (type(self) == type(other) and
                self.current_state == other.current_state)

    def is_over(self, current_state: "SubSquareState") -> bool:
        """
        Returns whether or not a Game is over based on current_state.

        ~No Docstests provided as they rely on input~
        """
        if current_state.current_val == 0:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Returns whether or not player is the winner of a finished game.

        ~No Docstests provided as they rely on input~
        """
        if not self.is_over(self.current_state):
            return False
        elif self.current_state.current_player == player:
            return False
        else:
            return True

    def str_to_move(self, string: str) -> Any:
        """
        Returns string converted to a valid move.

        ~No Docstests provided as they rely on input~
        """
        return int(string)


class GameState:
    """
    Class to model game states. Not meant for being instantiated, rather for
    gathering like methods and attributes.

    ===Attributes===
    current_player: the player
    """
    current_player: str

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes a new GameState. Extended in ChopState and SubSquareState.

        >>> g = GameState(True)
        >>> g.current_player
        'p1'
        """
        self.current_player = 'p2'
        if player1_start:
            self.current_player = 'p1'

    def __str__(self) -> str:
        """
        Returns a string representation of GameState.
        """
        raise NotImplementedError("Override this.")

    def __eq__(self, other: 'GameState') -> bool:
        """
        Returns whether or not GameState self is equal to other.
        """
        raise NotImplementedError("Override this.")

    def is_valid_move(self, move: str) -> bool:
        """
        Returns whether or not move is valid in the current state.
        """
        raise NotImplementedError("Override this.")

    def get_current_player_name(self) -> str:
        """
        Returns the name of the player whose current turn it is.

        >>> g = GameState(True)
        >>> g.get_current_player_name()
        'p1'
        """
        return self.current_player

    def make_move(self, move: int) -> object:
        """
        Returns a new GameState with move applied to it.
        """
        raise NotImplementedError("Override this.")

    def get_possible_moves(self) -> [object]:
        """
        Returns the possible moves based on the current game state.
        """
        raise NotImplementedError("Override this.")


class ChopState(GameState):
    """
    Keeps track of the game state of a game of Chopsticks. A subclass of
    GameState Overrides __eq__, __str__, is_valid_move, make_move, and
    get_possible_moves. Extends __init__.

    ===Attributes===
    p1_left: player 1's left hand value
    p1_right: player 1's right hand value
    p2_left: player 2's left hand value
    p2_right: player 2's right hand value
    current_player: the player whose turn it is
    """
    p1_left: int
    p1_right: int
    p2_left: int
    p2_right: int
    current_player: str

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes a Chopsticks game state.

        >>> cS = ChopState(True)
        >>> cS.p1_left
        1
        """
        GameState.__init__(self, player1_start)
        self.p1_left = 1
        self.p1_right = 1
        self.p2_left = 1
        self.p2_right = 1

    def __str__(self) -> str:
        """
        Returns a string representation of the ChopState

        >>> cS = ChopState(True)
        >>> print(cS)
        Player 1: Left 1 - 1 Right; Player 2: Left 1 - 1 Right
        """
        return 'Player 1: Left {} - {} Right; Player 2: Left {} - ' \
               '{} Right'.format(self.p1_left, self.p1_right,
                                 self.p2_left, self.p2_right)

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether or not Chopstate self is equal to other.

        >>> c = ChopState(True)
        >>> c1 = ChopState(True)
        >>> ran = 5
        >>> c1 == c
        True
        >>> c == ran
        False
        """
        return (type(self) == type(other) and self.p1_left == other.p1_left
                and self.p1_right == other.p1_right and self.p2_left ==
                other.p2_left and self.p2_right == other.p2_right and
                self.current_player == other.current_player)

    def is_valid_move(self, move: str) -> bool:
        """
        Returns whether or not move is valid in the current state.

        >>> cS = ChopState(True)
        >>> cS.is_valid_move('ll')
        True
        >>> cS.is_valid_move('abc')
        False
        """
        for m in self.get_possible_moves():
            if m == move:
                return True
        return False

    def make_move(self, move: str) -> object:
        """
        Returns a new game state with move applied to it.

        >>> cS = ChopState(True)
        >>> print(cS)
        Player 1: Left 1 - 1 Right; Player 2: Left 1 - 1 Right
        >>> print(cS.make_move('ll'))
        Player 1: Left 1 - 1 Right; Player 2: Left 2 - 1 Right
        """
        if self.current_player == 'p1':
            new_state = ChopState(False)
            new_state.p1_left = self.p1_left
            new_state.p1_right = self.p1_right
            new_state.p2_left = self.p2_left
            new_state.p2_right = self.p2_right

            if move == 'll':
                new_state.p2_left += new_state.p1_left

                if new_state.p2_left == 5:
                    new_state.p2_left = 0
                elif new_state.p2_left > 5:
                    new_state.p2_left %= 5
                return new_state
            elif move == 'lr':
                new_state.p2_right += new_state.p1_left

                if new_state.p2_right == 5:
                    new_state.p2_right = 0
                elif new_state.p2_right > 5:
                    new_state.p2_right %= 5
                return new_state
            elif move == 'rl':
                new_state.p2_left += new_state.p1_right

                if new_state.p2_left == 5:
                    new_state.p2_left = 0
                elif new_state.p2_left > 5:
                    new_state.p2_left %= 5
                return new_state
            else:
                new_state.p2_right += new_state.p1_right

                if new_state.p2_right == 5:
                    new_state.p2_right = 0
                elif new_state.p2_right > 5:
                    new_state.p2_right %= 5
                return new_state
        else:
            new_state = ChopState(True)
            new_state.p1_left = self.p1_left
            new_state.p1_right = self.p1_right
            new_state.p2_left = self.p2_left
            new_state.p2_right = self.p2_right

            if move == 'll':
                new_state.p1_left += new_state.p2_left

                if new_state.p1_left == 5:
                    new_state.p1_left = 0
                elif new_state.p1_left > 5:
                    new_state.p1_left %= 5
                return new_state
            elif move == 'lr':
                new_state.p1_right += new_state.p2_left

                if new_state.p1_right == 5:
                    new_state.p1_right = 0
                elif new_state.p1_right > 5:
                    new_state.p1_right %= 5
                return new_state
            elif move == 'rl':
                new_state.p1_left += new_state.p2_right

                if new_state.p1_left == 5:
                    new_state.p1_left = 0
                elif new_state.p1_left > 5:
                    new_state.p1_left %= 5
                return new_state
            else:
                new_state.p1_right += new_state.p2_right

                if new_state.p1_right == 5:
                    new_state.p1_right = 0
                elif new_state.p1_right > 5:
                    new_state.p1_right %= 5
                return new_state

    def get_possible_moves(self) -> [str]:
        """
        Returns list of possible moves based on current state.

        >>> cS = ChopState(True)
        >>> print(cS.get_possible_moves())
        ['ll', 'lr', 'rl', 'rr']
        >>> cS.p1_left = 0
        >>> cS.get_possible_moves()
        ['rl', 'rr']
        """
        if self.current_player == 'p1':
            if (self.p1_left != 0 and self.p1_right != 0 and self.p2_left != 0
                    and self.p2_right != 0):
                return ['ll', 'lr', 'rl', 'rr']
            elif (self.p1_left == 0 and self.p1_right != 0 and
                  self.p2_left != 0 and self.p2_right != 0):
                return ['rl', 'rr']
            elif (self.p1_left == 0 and self.p1_right != 0 and
                  self.p2_left == 0 and self.p2_right != 0):
                return ['rr']
            elif (self.p1_left == 0 and self.p1_right != 0 and
                  self.p2_left != 0 and self.p2_right == 0):
                return ['rl']
            elif (self.p1_left != 0 and self.p1_right == 0 and
                  self.p2_left != 0 and self.p2_right != 0):
                return ['ll', 'lr']
            elif (self.p1_left != 0 and self.p1_right == 0 and
                  self.p2_left == 0 and self.p2_right != 0):
                return ['lr']
            elif (self.p1_left != 0 and self.p1_right == 0 and
                  self.p2_left != 0 and self.p2_right == 0):
                return ['ll']
            elif (self.p1_left != 0 and self.p1_right != 0 and
                  self.p2_left == 0 and self.p2_right != 0):
                return ['lr', 'rr']
            elif (self.p1_left != 0 and self.p1_right != 0 and
                  self.p2_left != 0 and self.p2_right == 0):
                return ['ll', 'rl']
            return []
        elif self.current_player == 'p2':
            if (self.p2_left != 0 and self.p2_right != 0 and self.p1_left != 0
                    and self.p1_right != 0):
                return ['ll', 'lr', 'rl', 'rr']
            elif (self.p2_left == 0 and self.p2_right != 0 and
                  self.p1_left != 0 and self.p1_right != 0):
                return ['rl', 'rr']
            elif (self.p2_left == 0 and self.p2_right != 0 and
                  self.p1_left == 0 and self.p1_right != 0):
                return ['rr']
            elif (self.p2_left == 0 and self.p2_right != 0 and
                  self.p1_left != 0 and self.p1_right == 0):
                return ['rl']
            elif (self.p2_left != 0 and self.p2_right == 0 and
                  self.p1_left != 0 and self.p1_right != 0):
                return ['ll', 'lr']
            elif (self.p2_left != 0 and self.p2_right == 0 and
                  self.p1_left == 0 and self.p1_right != 0):
                return ['lr']
            elif (self.p2_left != 0 and self.p2_right == 0 and
                  self.p1_left != 0 and self.p1_right == 0):
                return ['ll']
            elif (self.p2_left != 0 and self.p2_right != 0 and
                  self.p1_left == 0 and self.p1_right != 0):
                return ['lr', 'rr']
            elif (self.p2_left != 0 and self.p2_right != 0 and
                  self.p1_left != 0 and self.p1_right == 0):
                return ['ll', 'rl']
            return []


class SubSquareState(GameState):
    """
    Keeps tracks of the game state of a game of Subtract Square. A subclass of
    GameState. Overrides __eq__, __str__, is_valid_move, make_move,
    get_possible_moves. Extends __init__.

    ===Attributes===
    current_val: current integer value being played
    current_player: player whose turn it currently is
    """
    current_val: int
    current_player: str

    def __init__(self, player1_start: bool) -> None:
        """
        Initializes a Subtract Square game state.

        >>> ss = SubSquareState(True)
        """
        GameState.__init__(self, player1_start)
        self.current_val = None

    def __eq__(self, other: 'SubSquareState') -> bool:
        """
        Returns if SubSquareState self is equal to other.

        >>> ss = SubSquareState(True)
        >>> ss1 = SubSquareState(True)
        >>> ran = 10
        >>> ss == ss1
        True
        >>> ss == ran
        False
        """
        return (type(self) == type(other) and
                self.current_val == other.current_val and
                self.current_player == other.current_player)

    def __str__(self) -> str:
        """
        Returns a string representation of self.
        """
        return "Current game value: {}".format(self.current_val)

    def is_valid_move(self, move: str) -> bool:
        """
        Returns whether or not move is valid in the current state.
        """
        for i in self.get_possible_moves():
            if move == i:
                return True
        return False

    def make_move(self, move: int) -> object:
        """
        Returns a new game state with move applied to it.
        """
        if self.current_player == 'p1':
            new_state = SubSquareState(False)
            new_state.current_val = self.current_val - move
            return new_state
        else:
            new_state = SubSquareState(True)
            new_state.current_val = self.current_val - move
            return new_state

    def get_possible_moves(self) -> [int]:
        """
        Returns list of possible moves based on the current game state.
        """
        i = 1
        poss = []
        while i ** 2 <= int(self.current_val):
            poss.append(i ** 2)
            i += 1
        return poss
