# tic tac toe game
import numpy as np
import random


class TicTacToe(object):
    lost = 0
    ipr = 0.5
    tie = 0.499999
    won = 1

    blank = 0.5
    player1 = 1
    player2 = 0

    def __init__(self):
        self.board = np.array([[self.blank for _ in range(3)] for _ in range(3)])
        self.status = self.ipr

    def get_status(self):
        return self.status

    def get_state(self):
        return tuple(self.board.flatten())

    def get_possible_moves(self, state=None):
        """ get possible moves """

        if state is None:
            # get coordinates of blank spots
            blanks = np.array(np.nonzero(self.board == self.blank))

            # convert each to square num:
            blanks[0, :] *= 3
            square_nums = blanks.sum(0) + 1

            return square_nums

        else:
            t = TicTacToe()
            t.board = np.reshape(state, (3, 3))
            return t.get_possible_moves()

    def gen_move(self):
        """ generate random move """
        moves = self.get_possible_moves()
        return moves[random.randint(0, len(moves) - 1)]

    @staticmethod
    def square_num_to_coords(square_num):
        return ((square_num - 1) // 3, (square_num - 1) % 3)

    @staticmethod
    def coords_to_square_num((rowi, coli)):
        return rowi * 3 + coli

    @staticmethod
    def get_next_state(s, a):
        t = TicTacToe()
        t.board = np.reshape(s, (3, 3))
        t.move(a)
        return t.get_state(), t.status

    def _move_player(self, square_num, player):
        assert 1 <= square_num <= 9
        assert self.status == self.ipr

        rowi, coli = self.square_num_to_coords(square_num)
        assert self.board[rowi][coli] == self.blank

        self.board[rowi][coli] = player
        self._update_status()

    def _update_status(self):
        if np.sum(self.board != self.blank) == 9:
            self.status = self.tie
            return

        p1 = self.board == self.player1
        p2 = self.board == self.player2

        p1_result = np.concatenate((p1.sum(0), p1.sum(1), np.array([p1.trace()]), np.array([np.fliplr(p1).trace()])))
        p2_result = np.concatenate((p2.sum(0), p2.sum(1), np.array([p2.trace()]), np.array([np.fliplr(p2).trace()])))

        if any(p1_result == 3):
            self.status = self.won
        elif any(p2_result == 3):
            self.status = self.lost

    def move(self, square_num):
        self._move_player(square_num, self.player1)
        if self.get_status() == self.ipr:
            self._move_player(self.gen_move(), self.player2)
