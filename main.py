# Tic Tac Toe using Q learning
from ttt import TicTacToe
import numpy as np
import random

Q = dict()
alpha = 0.2
gamma = 0.7
N_episodes = 10000
N_tests = 1000
epsilon = 0.9


def reward(s):
    t = TicTacToe()
    t.board = np.reshape(s, (3, 3))
    t._update_status()
    return t.status


def move(game, a):
    s = game.get_state()
    s2, status2 = TicTacToe.get_next_state(s, a)
    if status2 == TicTacToe.ipr:
        Q[(s, a)] = ((1 - alpha) * Q.get((s, a), 0)) + (
                alpha * (reward(s2) + (gamma * max([Q.get((s2, b), 0) for b in game.get_possible_moves(s2)]))))
    else:
        Q[(s, a)] = ((1 - alpha) * Q.get((s, a), 0)) + (
                alpha * reward(s2))
    game.move(a)


if __name__ == '__main__':

    # train
    for i in range(N_episodes):
        game = TicTacToe()
        while game.status == TicTacToe.ipr:
            s = game.get_state()
            if random.random() < epsilon:
                a = max([(Q.get((s, a_), 0), a_) for a_ in game.get_possible_moves()], key=lambda x: x[0])[1]
            else:
                a = random.choice(game.get_possible_moves())
            move(game, a)
        if i % 100 == 0:
            print i

    # test
    ties = 0.0
    wins = 0.0
    losses = 0.0

    for i in range(N_tests):
        game = TicTacToe()
        while game.status == TicTacToe.ipr:
            s = game.get_state()
            a = max([(Q.get((s, a_), 0), a_) for a_ in game.get_possible_moves()], key=lambda x: x[0])[1]
            game.move(a)
        ties += game.status == TicTacToe.tie
        wins += game.status == TicTacToe.won
        losses += game.status == TicTacToe.lost

    print 'ties: %.2f%%' % (ties * 100 / N_tests)
    print 'wins: %.2f%%' % (wins * 100 / N_tests)
    print 'losses: %.2f%%' % (losses * 100 / N_tests)
