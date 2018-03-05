class StonehengeGame(Game):
    """
    Class to model Stonehenge Game.

    ===Attributes===
    p1_turn: whether or not it is currently Player 1's turn.
    current_state: current state of the game
    instructions: instructions for a game of Stonehenge
    """
    p1_turn: bool
    current_state: 'StonehengeState'
    instructions: str

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.

        ~Doctests omitted due to use of input~
        """
        self.p1_turn = p1_starts
        # retrieving size of board through input, dont put this into state class
        # since we return new states when a move is made and cant answer input
        # when it is constructed
        size = int(input("Enter the size of the game board:"))
        # creating state
        self.current_state = StonehengeState(self.p1_turn, size)
        # setting instructions
        self.instructions = "Stonehenge is played on a hexagonal grid formed " \
                            "by removing the corners of a triangular grid. \n" \
                            "Boards can have various sizes based on their " \
                            "side-length (the number of cells in the grid \n" \
                            "along the bottom), but are always formed in a " \
                            "similar manner: For side-length n, the first \n" \
                            "row has 2 cells, and each row after it has 1 " \
                            "additional cell up until there's a row with \n" \
                            "n+1 cells, after which the last row has only " \
                            "n cells in it. Players take turns claiming \n" \
                            "cells (abbreviated with a capital letter). " \
                            "When a player captures at least half of the \n" \
                            "cells in a ley-line (lines extending from " \
                            "each third of the hexagon to the other side),\n" \
                            " then the player captures that ley-line. The " \
                            "first player to capture at least half of the \n" \
                            "ley-lines is the winner. A ley-line, once " \
                            "claimed, cannot be taken by the other player."

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.

        ~Doctests omitted due to use of input~
        """
        return self.instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this game is over at state.

        ~Doctests omitted due to use of input~
        """
        count1, count2 = 0, 0
        # counting ley line markers to evaluate games ending condition
        for i in state.ley_lines:
            if i[0] == 1:
                count1 += 1
            elif i[0] == 2:
                count2 += 1
        # determining if counts are at least half of an even length of ley lines
        if len(state.ley_lines) % 2 == 0:
            if count1 >= (len(state.ley_lines) / 2):
                return True
            elif count2 >= (len(state.ley_lines) / 2):
                return True
            return False
        # determining if counts are at least half of an odd length of ley lines
        else:
            if count1 >= (len(state.ley_lines) // 2) + 1:
                return True
            elif count2 >= (len(state.ley_lines) // 2) + 1:
                return True
            return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        ~Doctests omitted due to use of input~
        """
        # assures that game is over before evaluating winner
        if not self.is_over(self.current_state):
            return False
        # if game is over and current player is player, the other player has won
        elif self.current_state.curr_player == player:
            return False
        return True

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.

        ~Doctests omitted due to use of input~
        """
        assert isinstance(string, str) and string.upper() in POSS_VAL, \
            "Move must be a letter of the alphabet"
        return string


class StonehengeState(GameState):
    """
    Game state for game of Stonehenge at a certain time.

    ===Attributes===
    curr_player: player whose turn it currently is
    size: size of the game board
    board: current cells of the game board
    ley_lines: ley line values of current state
    """
    curr_player: str
    size: int
    board: List[List[str]]
    ley_lines: List[List[str]]

    def __init__(self, is_p1_turn: bool, size: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> s = StonehengeState(True, 3)
        >>> s.board
        [['A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'H', 'I'], ['J', 'K', 'L']]
        """
        super().__init__(is_p1_turn)
        assert 5 >= size > 0, "Board size must be a positive integer and no " \
                              "greater than 5."
        self.curr_player = "p2"
        if is_p1_turn:
            self.curr_player = "p1"
        self.size = size
        # creating cells in Stonehenge board
        self.board = create_stonehenge_board(self.size, POSS_VAL)
        # creating ley lines
        self.ley_lines = get_ley_lines(self.board, self.size)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        ~Doctests omitted due to use of \n when representing string~
        """
        # copy of ley lines and board since we will be removing them after they
        # are added, logic is similar to getting ley lines
        ley_copy = copy.deepcopy(self.ley_lines)
        board_copy = gather_list(copy.deepcopy(self.board))
        # separating ley lines into horizontal, left diagonal and right diagonal
        index = int(len(self.ley_lines) / 3)
        horiz = ley_copy[:index]
        left = ley_copy[index:2 * index]
        right = ley_copy[2 * index:3 * index]
        spacing = (len(self.board) - 2) * 2
        # adding first two ley lines and their markers
        ret_str = ""
        ret_str += "\n{}{}   {}".format(" "*(spacing+6), left[0][0], left[1][0])
        ret_str += "\n{}/   /".format(" "*(spacing+5))
        # removing added vals, we will continue to do this to be able to access
        # them from the same index
        left = left[2:]
        n = 2
        while n <= self.size + 1:
            # creating newline and adding correct spacing and horizontal ley
            # line marker
            ret_str += "\n{}{} -".format(" " * spacing, horiz[0][0])
            horiz = horiz[1:]
            spacing -= 2
            for _i in range(n):
                if n == self.size + 1:
                    ret_str += " {} -".format(board_copy[0]) if _i != n-1 \
                        else " {} ".format(board_copy[0])
                    board_copy = board_copy[1:]
                # if we are on the last cell of the row, we add a ley line
                # marker and remove it from the ley lines
                elif _i == n - 1 and n != self.size + 2:
                    ret_str += " {}   {}".format(board_copy[0], left[0][0])
                    left = left[1:]
                    board_copy = board_copy[1:]
                else:
                    ret_str += " {} -".format(board_copy[0])
                    board_copy = board_copy[1:]
            n += 1
            # adding slashes
            if n == self.size + 2:
                ret_str += "\n{}  \\".format(" "*(spacing+5))
                ret_str += " {}".format("/ \\ "*(n-2))
            elif n > 2:
                ret_str += "\n{}{}".format(" "*(spacing+5), "/ \\ "*(n-1))
                ret_str += "/"
            else:
                ret_str += "\n{}{}".format(" "*(spacing+5), "/ \\ "*(n-1))
        # adding last row of cells, slashes and ley line markers after size+1
        # row
        spacing = 2
        ret_str += "\n{}{} - ".format(" "*spacing, horiz[0][0])
        for _j in range(self.size):
            if _j == self.size - 1:
                ret_str += "{}   {}".format(board_copy[0], right[0][0])
                right = right[1:]
            else:
                ret_str += "{} - ".format(board_copy[0])
                board_copy = board_copy[1:]
        ret_str += "\n{}{}".format(" "*(spacing+5), "\\   "*self.size)
        ret_str += "\n{}".format(" "*(spacing+6))
        for _k in range(len(right)):
            ret_str += "{}   ".format(right[-1][0])
            right = right[:-1]
        return ret_str

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.

        >>> s = StonehengeState(True, 1)
        >>> s.get_possible_moves()
        ['A', 'B', 'C']
        >>> s = StonehengeState(True, 2)
        >>> s.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        """
        # performing same count as in StonehengeGame.is_over() to return an
        # empty list if the game is over
        count1, count2 = 0, 0
        for i in self.ley_lines:
            if i[0] == 1:
                count1 += 1
            elif i[0] == 2:
                count2 += 1
        if len(self.ley_lines) % 2 == 0:
            if count1 >= (len(self.ley_lines) / 2):
                return []
            elif count2 >= (len(self.ley_lines) / 2):
                return []
            moves = []
            # returning available cells if game isnt over
            for cell in gather_list(self.board):
                if cell in POSS_VAL:
                    moves.append(cell)
            return moves
        else:
            if count1 >= (len(self.ley_lines) // 2) + 1:
                return []
            elif count2 >= (len(self.ley_lines) // 2) + 1:
                return []
            # returning available cells if game isnt over
            moves = []
            for cell in gather_list(self.board):
                if cell in POSS_VAL:
                    moves.append(cell)
            return moves

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.

        >>> s = StonehengeState(True, 2)
        >>> s.get_current_player_name()
        'p1'
        >>> s = StonehengeState(False, 2)
        >>> s.get_current_player_name()
        'p2'
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.

        >>> s = StonehengeState(True, 2)
        >>> s.get_current_player_name()
        'p1'
        >>> s2 = s.make_move("A")
        >>> s2.get_current_player_name()
        'p2'
        >>> s2.board
        [[1, 'B'], ['C', 'D', 'E'], ['F', 'G']]
        """
        if self.curr_player == "p1":
            # creating new state and copying current board
            new_state = StonehengeState(False, self.size)
            new_state.board = copy.deepcopy(self.board)
            # changing cells that have been taken by player
            update_board(new_state.board, move, "p1")
            # updating ley lines
            new_state.ley_lines = update_ley(self.ley_lines, move, True)
            return new_state

        # creating new state and copying current board
        new_state = StonehengeState(True, self.size)
        new_state.board = copy.deepcopy(self.board)
        # changing cells that have been taken by player
        update_board(new_state.board, move, "p2")
        # updating ley lines
        new_state.ley_lines = update_ley(self.ley_lines, move, False)
        return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.

        >>> s = StonehengeState(True, 2)
        >>> s.is_valid_move("A")
        True
        >>> s.is_valid_move("Z")
        False
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).

        ~Doctests omitted due to use of \n to represent attributes~
        """
        board = ""
        ley_lines = ""
        # adding new line for each row of board
        for i in self.board:
            board += "{}\n".format(i)
        # addding new line for each row of ley lines
        for j in self.ley_lines:
            ley_lines += "{}\n".format(j)
        # returning all attributes of StonehengeState
        return "Board:\n{}\nLey-Lines:\n{}\n" \
               "Size:\n{}\n\nCurrent Player:\n{}".format(board, ley_lines,
                                                             self.size,
                                                             self.curr_player)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> s = StonehengeState(True, 1)
        >>> s.rough_outcome()
        1
        """
        # checking if rough_outcome is called on a game that is already done
        if not self.get_possible_moves():
            count1, count2 = 0, 0
            for l in self.ley_lines:
                if l[0] == 1:
                    count1 += 1
                elif l[0] == 2:
                    count2 += 1
            if len(self.ley_lines) % 2 == 0:
                if count1 >= len(self.ley_lines) / 2:
                    return 1 if self.get_current_player_name() == "p1" else -1
                elif count2 >= len(self.ley_lines) / 2:
                    return 1 if self.get_current_player_name() == "p2" else -1
            else:
                if count1 >= (len(self.ley_lines) // 2) + 1:
                    return 1 if self.get_current_player_name() == "p1" else -1
                elif count2 >= (len(self.ley_lines) // 2) + 1:
                    return 1 if self.get_current_player_name() == "p2" else -1

        # creating states for next possible move and next possible move after
        # that
        nstates = [self.make_move(x) for x in self.get_possible_moves()]
        ostates = []
        for state in nstates:
            ostates.extend([state.make_move(y)
                            for y in state.get_possible_moves()])

        # checking if any of the first possible moves lead to an end state
        for state in nstates:
            if not state.get_possible_moves():
                if self.get_current_player_name() == "p1":
                    return 1 if state.get_current_player_name() != "p1" else -1
                return 1 if state.get_current_player_name() != "p2" else -1

        # checking if any of the next possible moves lead to an end state
        for ostate in ostates:
            if not ostate.get_possible_moves():
                if self.get_current_player_name() == "p1":
                    return 1 if ostate.get_current_player_name() != "p1" else -1
                return 1 if ostate.get_current_player_name() != "p2" else -1

        # returning a number in range in (WIN, LOSS) if none of the conditions
        # is satisfied
        count1, count2 = 0, 0
        for l in self.ley_lines:
            if l[0] == 1:
                count1 += 1
            elif l[0] == 2:
                count2 += 1
        return min(count1, count2) / max(count1, count2)

