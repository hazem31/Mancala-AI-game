

# not tested completely

import numpy as np
from rich.console import Console
from rich.table import Column, Table

class Board:
    def __init__(self,steal = False):
        self.board = np.array([[ 4 ,4 ,4 ,4 , 4 , 4] , [ 4 ,4 ,4 ,4 , 4 , 4 ] ])
        # score[0] of player 1 score[1] of player 2
        self.score_1 = 0
        self.score_2 = 0
        self.game_still_going = True
        self.with_stealing = steal

        self.player_dic = {1 : 1 , 2 : 0}
    # 1 means ok 0 means game ended no moves 2 means play again 3 means invalid move
    def play(self,player,index):
        # index from 0 to 5

        #player2 = 2 and player1 = 1
        if not self.game_still_going:
            #print('game ended')
            return 0
        play_again = False
        curr_row = self.player_dic[player]
        curr_col = index
        value_in_cell = self.board[curr_row, curr_col]
        if value_in_cell == 0:
            return 3


        self.board[curr_row, curr_col] = 0
        v = value_in_cell
        while value_in_cell > 0:
            if curr_row == 1 and curr_col == 5:
                if player == 1:
                    self.score_1 += 1
                    value_in_cell -= 1

                    curr_row = 0
                    curr_col = 5
                    self.board[curr_row, curr_col] += 1
                    value_in_cell -= 1
                if player == 2:
                    curr_row = 0
                    curr_col = 5

                    if self.with_stealing and self.board[curr_row, curr_col] == 0 and value_in_cell == 1:
                        #print('stealing')
                        self.score_2 += value_in_cell + self.board[1, curr_col]
                        self.board[1, curr_col] = 0
                        value_in_cell -= 1
                    else:
                        self.board[curr_row, curr_col] += 1
                        value_in_cell -= 1
                continue
            if curr_row == 0 and curr_col == 0:
                if player == 1:
                    curr_row = 1
                    curr_col = 0
                    if self.with_stealing and self.board[curr_row, curr_col] == 0 and value_in_cell == 1:
                        #print('stealing')
                        self.score_1 += value_in_cell + self.board[0, curr_col]
                        self.board[0, curr_col] = 0
                        value_in_cell -= 1
                    else:
                        self.board[curr_row, curr_col] += 1
                        value_in_cell -= 1

                if player == 2:
                    self.score_2 += 1
                    value_in_cell -= 1
                    curr_row = 1
                    curr_col = 0
                    self.board[curr_row, curr_col] += 1
                    value_in_cell -= 1

                continue
            if curr_row == 1:
                curr_col += 1

                if self.with_stealing and self.board[curr_row, curr_col] == 0 and value_in_cell == 1 and player == 1:
                    #print('stealing')
                    self.score_1 += value_in_cell + self.board[0, curr_col]
                    self.board[0, curr_col] = 0
                    value_in_cell -= 1
                else:
                    self.board[curr_row,curr_col] += 1
                    value_in_cell -= 1
                continue
            if curr_row == 0:
                curr_col -= 1
                if self.with_stealing and self.board[curr_row, curr_col] == 0 and value_in_cell == 1 and player == 2:
                    #print('stealing')
                    self.score_2 += value_in_cell + self.board[1, curr_col]
                    self.board[1, curr_col] = 0
                    value_in_cell -= 1
                else:
                    self.board[curr_row,curr_col] += 1
                    value_in_cell -= 1
                continue

    def draw(self):
        table = Table(show_header=True)
        table.add_column("score 2")
        table.add_column("cell 1")
        table.add_column("cell 2")
        table.add_column("cell 3")
        table.add_column("cell 4")
        table.add_column("cell 5")
        table.add_column("cell 6")
        table.add_column("score 1")
        table.add_column("players")

        table.add_row(str(self.score_2) , str(self.board[0,0]) , str(self.board[0,1]) , str(self.board[0,2]) ,str(self.board[0,3]) , str(self.board[0,4]) , str(self.board[0,5]) ,'--' , 'player 2'  )

        table.add_row('--', str(self.board[1, 0]), str(self.board[1, 1]), str(self.board[1, 2]),
                      str(self.board[1, 3]), str(self.board[1, 4]), str(self.board[1, 5]), str(self.score_1) ,'player 1')

        console.print(table)
