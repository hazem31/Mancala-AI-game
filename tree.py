
from rich.console import Console
from rich.table import Column, Table
import numpy as np
import copy

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


        def make_tree(depth,type,board,how_to_get):
    '''
    This is a recursive function that build the tree in depth first order to a certain given 
    depth the base case for this recursive function is that if the value of depth reaches the level of the game or 
    the current node is the end of game and set a value for the leaf node
    It starts to loop over the possible moves from current state and calls it self again on the child in depth first order 

-depth: current depth in tree
-type of current node max or min
-the board to start building the tree from
-how_to_get: which play to play to reach this node

    :param depth: current depth in tree
    :param type: type of current node max or min 
    :param board: the board to start building the tree from
    :param how_to_get: 
    :return: 
    '''
    
    # base condition a leaf node just calculate evaluation function 
    if depth == level:
        n = Node(type)
        n.state = board
        n.how_to_get_here = how_to_get
        # max is player 2
        n.value = get_value1(copy.deepcopy(board))#(n.state.score_2 - n.state.score_1) #+ (np.sum(n.state.board[0,:]) - np.sum(n.state.board[1:]))
        return n

    #if not board.game_still_going


    node = Node(type)
    node.state = board
    node.how_to_get_here = how_to_get
    
    # in case it a end node another base condition 
    if not board.game_still_going:
        node.value = get_value1(board)
        return node

    # looping all possible moves
    for i in range(6):
        b1 = copy.deepcopy(node.state)
        # if first node is max then 
        if type == 'max':
            # try the move
            stat = b1.play(2,i)
            #b1.draw()
            # if the game ended in this move
            if stat == 0:
                n = Node(type='min')
                value = get_value1(copy.deepcopy(b1))
                n.state = b1
                n.value = value
                n.how_to_get_here = i
                node.childs.append(n)
                # add this leaf node to the childs
                continue
            # if inavlid move
            if stat == 3:
                continue
            # if the game is ok but not a play again then call function on it 
            if stat == 1:
                n = make_tree(depth+1,'min',copy.deepcopy(b1),i)
                node.childs.append(n)
                continue
            # if the game is ok and play again then call function on it
            if stat == 2:
                n = make_tree(depth + 1, 'max', copy.deepcopy(b1),i)
                node.childs.append(n)
                continue
        else:
            # if min node
            stat = b1.play(1,i)
            #b1.draw()
            if stat == 0:
                n = Node(type='max')
                value = get_value1(copy.deepcopy(b1))
                n.state = b1
                n.value = value
                n.how_to_get_here = i
                node.childs.append(n)
                continue
            if stat == 3:
                continue
            if stat == 1:
                n = make_tree(depth + 1, 'max', copy.deepcopy(b1),i)
                node.childs.append(n)
                continue
            if stat == 2:
                n = make_tree(depth + 1, 'min', copy.deepcopy(b1),i)
                node.childs.append(n)
                continue
    return node
