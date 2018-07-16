#!/usr/bin/env python
# encoding: utf-8
from setting import *
import numpy as np
import random


class Player:
    O = 1
    X = -1


class Stone(object):
    def __init__(self, pos, player):
        self.pos = pos
        self.player = player


class Board(object):
    def __init__(self):
        self.size = board_size
        self.win_num = win_num
        self.turn = Player.O
        self.init_board()

    def init_board(self):
        self.board = np.zeros((self.size, self.size))
        self.illegal_idx = []

    def do_turn(self):
        if self.turn == Player.O:
            self.turn = Player.X
        else:
            self.turn = Player.O

    def get_feature(self):
        ret = np.zeros(shape=(3, board_size, board_size))
        for i in range(board_size):
            for j in range(board_size):
                if self.turn == Player.O:
                    ret[2][i][j] = 0
                elif self.turn == Player.X:
                    ret[2][i][j] = 1
                if self.board[i][j] == Player.O:
                    ret[0][i][j] = 1
                elif self.board[i][j] == Player.X:
                    ret[1][i][j] = 1
        return ret.reshape((3, board_size, board_size))

    def is_legal(self, stone):
        if stone.player == self.turn and self.board[stone.pos[0]][stone.pos[1]] == 0:
            return True
        else:
            return False

    def add_stone(self, stone):
        if self.board[stone.pos[0]][stone.pos[1]] != 0:
            raise BaseException
        else:
            self.board[stone.pos[0]][stone.pos[1]] = stone.player

    def paint(self):
        strs = ''
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.board[i][j] == Player.O:
                    row.append('O')
                elif self.board[i][j] == Player.X:
                    row.append('X')
                else:
                    row.append('-')
            strs += ' '.join(row) + '\n'
        print(strs)

    def count_on_direction(self, stone, xdirection, ydirection):
        i, j = stone.pos
        color = stone.player
        count = 0
        for step in range(1, 5):  # 除当前位置外,朝对应方向再看4步
            if xdirection != 0 and (j + xdirection * step < 0 or j + xdirection * step >= self.size):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i + ydirection * step >= self.size):
                break
            if self.board[i + ydirection * step][j + xdirection * step] == color:
                count += 1
            else:
                break
        return count

    def step(self, stone):
        if not self.is_legal(stone):
            raise RuntimeError
        self.add_stone(stone)
        self.illegal_idx.append(stone.pos[0] * board_size + stone.pos[1])
        self.do_turn()
        return self

    def get_winer(self, stone):
        # 四个方向计数 竖 横 左斜 右斜
        directions = [[(-1, 0), (1, 0)],
                      [(0, -1), (0, 1)],
                      [(-1, 1), (1, -1)],
                      [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            for xdirection, ydirection in axis:
                axis_count += self.count_on_direction(stone, xdirection, ydirection)
                if axis_count >= self.win_num:
                    return stone.player
        return 0



if __name__ == "__main__":
    game = Game()
    game.run()
