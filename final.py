from rich.console import Console
from rich.table import Column, Table
import numpy as np
import copy
import pickle

console = Console()



class Node:
    def __init__(self,type=None):
        '''
        It represent a class that has no functions can be considered as a structure
        it is to represent a player and current of state of the board
        in the turn of that player and the game it holds values as
        -Type: max or min 
        -the value of this node if it is a max then it is alpha value if min then the value is beta 
        -it stores current alpha and beta    
        -It stores a list (childs) which are the state that can be reached from curr state of game (all -possible moves for that player) 
        -It stores the state which of type class board 
        -It stores the way to get to this state from previous state 
        '''
        
        #holds type of player
        self.type = type
        #the value of evaluation function
        self.value = None
        # value alpha set to -5000
        self.alpha = -5000
        # value alpha set to 5000
        self.beta = 5000
        # possible moves from this state 
        self.childs = []
        # state of board
        self.state = None
        # how to reach this state from prevoius state 
        self.how_to_get_here = None



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
                    if value_in_cell == 0:
                        if self.check_game():
                            return 0
                        else:
                            return 2

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
                    if value_in_cell == 0:
                        if self.check_game():
                            return 0
                        else:
                            return 2
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

        if self.check_game():
            return 0
        else:
            return 1

    def check_game(self):
        if np.sum(self.board[0,:]) == 0:
            for i in range(6):
                self.score_1 += self.board[1,i]
            self.game_still_going = False
            self.board[1, :] = 0
            #print('game ended')
            return True

        if np.sum(self.board[1,:]) == 0:
            for i in range(6):
                self.score_2 += self.board[0,i]
            self.game_still_going = False
            self.board[0,:] = 0
            #print('game ended')
            return True
        return False

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
       
      
      
def get_value2(board):
    """ This function is used as an evaluation function, to get the best next move based on the current cell values and scores,
    where it iterates over the cell values, and checks which cell if played will make the last pebble fall in the large pocket
    (mancala) of the second player in order to play again, then increases the score by one.

    board (Board class): An object of the Board class

    (int): The score of the second player
    """
    v = board.score_2
    for i in range(6):
        if board.board[0,i] > i :
            v += 1

    return v


def get_value1(board):
    """ This function is used as an evaluation function, to get the best next move based on the current cell values and scores,
    where it iterates over the cell values, and checks which cell if played will make the last pebble fall in the large pocket
    (mancala) of both players, then increases the player's score by one.

    board (Board class): An object of the Board class

    (int): The score of the second player minus the score of the first player
    """
    v = board.score_2
    for i in range(6):
        if board.board[0, i] > i:
            v += 1
    s = board.score_1
    for i in range(6):
        if board.board[1,i] > (5-i):
            s += 1

def traverse_tree(node, depth):
    """ This function is a recursive function that is used to traverse the tree based on the current state,
    where it iterates over the nodes/states, where the children of each node are the legal moves for the current state/node.

    node (Node class): An object of the Node class

    depth (int) : The depth of the tree
    """
    # Base condition: if the node is a terminal node (has no children)
    if len(node.childs) == 0:
        # To draw the state/board
        node.state.draw()
        print("value is  " , node.value)
        print("curr depth is  " , depth)
        return

    node.state.draw()
    print("curr depth is  ", depth)
    for i in range(len(node.childs)):
        traverse_tree(node.childs[i],depth+1)
        node.state.draw()
        print("curr depth is  ", depth)

    return
    return v - s
