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


def make_tree(depth,type,board,how_to_get,level):
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
                n = make_tree(depth+1,'min',copy.deepcopy(b1),i,level)
                node.childs.append(n)
                continue
            # if the game is ok and play again then call function on it
            if stat == 2:
                n = make_tree(depth + 1, 'max', copy.deepcopy(b1),i,level)
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
                n = make_tree(depth + 1, 'max', copy.deepcopy(b1),i,level)
                node.childs.append(n)
                continue
            if stat == 2:
                n = make_tree(depth + 1, 'min', copy.deepcopy(b1),i,level)
                node.childs.append(n)
                continue
    return node 


def beta_alpha(node):
    """ This function is used to calculate beta & alpha values for a node of the tree recursively calling it's children until all children are traversed.
    node (Node class): An object of the Node class.
    (int): alpha value of maximizer node or beta value of minimizer node.
    """
        
        
    if len(node.childs) == 0:   #leaf node 
        return node.value

    curr_alpha = node.alpha   #parent alpha
    curr_beta = node.beta     #parent beta 

    for n in node.childs:
        n.aplha = curr_alpha   #init alpha from parent 
        n.beta = curr_beta     #init beta  from parent 
        value = beta_alpha(n)  #returned from childs (alpha from maximizer and beta from minimizer)
        if value is None: #cutoff happened -> no update 
            continue
        if node.type == 'max':    #current node is maximizer node 
            if value > curr_alpha:  #beta of child > alpha of current 
                curr_alpha = value   
        else:  #current node is minimzer node 
            if value < curr_beta: #alpha of child < beta of current 
                curr_beta = value
        if curr_alpha >= curr_beta: # cutoff      
            return None

    if node.type == 'max':  #maximizer return alpha 
        node.value = curr_alpha
    else:  #minimzer return beta
        node.value = curr_beta

    return node.value


def automate_play(node,board,player=2):
    value = beta_alpha(node)
    for i in range(len(node.childs)):
        if node.childs[i].value is None:
            continue

        if value == node.childs[i].value:
            stat = board.play(player,node.childs[i].how_to_get_here)
            return stat

    return 0

def play_game():

    """Summary: The function is used to make game setup and start the game between two agents.
    game setup includes choosing the game mode weather single player ,multiplayer or two AI bots playing against each other
    choosing to play the game with or without the stealing feature.
    choosing the game difficulty
    and finally choosing which player has the first turn
    we can also load a saved game or start a new game inside this function

    """

    print('<<<<<<<<<<<<<<<##################>>>>>>>>>>>>>>>')
    print('---------------welcome to Mancala----------------')
    print('<<<<<<<<<<<<<<<###############>>>>>>>>>>>>>>>')

    while True:
        print('---------------------')
        print('next step')
        print('---------------------')
        type_of_game = 0                   #determine wether you want to start new game or load old one
        while True:
            print('for a new game: enter 1')
            print('for loading a game: enter 2')
            try:
                type_of_game = int(input('enter : '))
                if type_of_game == 1 or type_of_game == 2:
                    break
                else:
                    print('xxxxxxxxxxxx')
                    print('invalid input')
                    continue
            except:
                print('xxxxxxxxxxxx')
                print('invalid input')
                continue
        board = None     # These parameters are used for game setup
        steal = False
        mode = None
        turn2 = None
        level = None
        if type_of_game == 1:
            print('---------------------')
            print('next step')
            print('---------------------')
            while True:
                print('choose mode of playing')
                print('for single player: enter 1')
                print('for multiplayer : enter 2')
                print('for 2 computers against each other: enter 3')
                try:
                    mode = int(input('enter : '))
                    if mode == 1 or mode == 2 or mode == 3:
                        break
                    else:
                        print('xxxxxxxxxxxx')
                        print('invalid input')
                        continue
                except:
                    print('xxxxxxxxxxxx')
                    print('invalid input')
                    continue

            if mode == 1 or mode == 3:
                print('---------------------')
                print('next step')
                print('---------------------')
                while True:
                    print('choose level of playing')
                    print('for easy : enter 1')
                    print('for medium : enter 2')
                    print('for hard : enter 3')
                    try:
                        level = int(input('enter : '))    #choosing difficulty note we use the same variable that represent the difficulty to represent the depth of the search tree
                        if level == 1 or level == 2 or level == 3:
                            if level == 1:
                                level = 4
                            elif level == 2:
                                level = 6
                            elif level == 3:
                                level = 7
                            break
                        else:
                            print('xxxxxxxxxxxx')
                            print('invalid input')
                            continue
                    except:
                        print('xxxxxxxxxxxx')
                        print('invalid input')
                        continue

            print('---------------------')
            print('next step')
            print('---------------------')
            while True:
                print('without stealing: enter 1')
                print('with stealing: enter 2')
                try:
                    steal = int(input('enter : ')) #choosing to play with or without stealing
                    if steal == 1 or steal == 2:
                        if steal == 1:
                            steal = False
                        else:
                            steal = True

                        break
                    else:
                        print('xxxxxxxxxxxx')
                        print('invalid input')
                        continue
                except:
                    print('xxxxxxxxxxxx')
                    print('invalid input')
                    continue
            print('---------------------')
            print('next step')
            print('---------------------')
            while True:
                print('who plays first')
                print('player 1 : enter 1')
                print('player 2: enter 2')
                try:
                    turn2 = int(input('enter : ')) #choosing your turn in the game
                    if turn2 == 1 or turn2 == 2:
                        if turn2 == 1:
                            turn2 = 0
                        else:
                            turn2 = 1
                        break
                    else:
                        print('xxxxxxxxxxxx')
                        print('invalid input')
                        continue
                except:
                    print('xxxxxxxxxxxx')
                    print('invalid input')
                    continue

            board = Board(steal=steal) #making an instance of the class board with stealing variable as a parameter
            start_game(board, turn2, mode, level) #calling the start game function to begin the actual game passing the game parameters set by the player
        else:
            print('---------------------')
            print('next step')
            print('---------------------')
            save = None
            while True:
                print('please enter path to saved file without the .pickle') # if the player chose to load a saved game the program asks for the path to the game without .pickle
                try:
                    pth = input('input path: ')
                    with open(pth+'.pickle', 'rb') as handle:
                        save = pickle.load(handle)
                        break
                except:
                    print('invalid error')

            start_game(save[0],save[1],save[2],save[3])#calling the start game function to begin the actual game passing the game parameters from the saved file array

        print('<<<<<<<<<<<<<<<##################>>>>>>>>>>>>>>>')
        print('------------------game ended----------------')
        print('<<<<<<<<<<<<<<<###############>>>>>>>>>>>>>>>')
        while True:
            print('play again : enter 1')
            print('exit game: enter 2')
            try:
                new = int(input('enter : '))
                if new == 1 or new == 2:
                    if new == 1:
                        break
                    else:
                        return
                else:
                    print('xxxxxxxxxxxx')
                    print('invalid input')
                    continue
            except:
                print('xxxxxxxxxxxx')
                print('invalid input')
                continue
   

def start_game(board,turn2,mode,level):
    """Summary: The function is used for actual gameplaying between two agents.
                   Parameters:
                   :param board: instance of a class containing board settings like board layout number of balls in each slot etc....
                   :param turn2: variable showing which player will go first.
                   :param mode: an integer value that shows the nature of the two agents playing the game.
                   :param level: an integer showing the depth of the search in the search tree which corresponds to the difficulty of the game.

    """
    board.draw()
    if mode == 1:  #single player mode
        again = 0
        while True:
            # board.draw()
            if turn2 == 1: #player two go first
                if again:
                    print('')
                    print('player 2 turn again')
                    print('')
                else:
                    print('')
                    print('player 2 turn')
                    print('')
                b = copy.deepcopy(board) #copy board stats
                n = make_tree(0, 'max', b, 0, level) # construct the search tree
                print('############################')
                print('previous state of board')
                board.draw() # draw board for display
                print('############################')
                stat = automate_play(n,board,2) #return the new board status after the computer play its move
                if stat == 0: # game over

                    board.check_game()
                    print('<<<<>>>>>')
                    print('<<<<>>>>>')
                    print('end of game')
                    print('score 1 ', board.score_1)
                    print('score 2 ', board.score_2)
                    board.draw()
                    break
                elif stat == 1:
                    # print('player 1 turn')
                    turn2 = 0
                    again = 0
                elif stat == 2:
                    # print('player 2 turn again')
                    turn2 = 1
                    again = 1
                print('############################')
                print('new state of board after player 2 plays')
                board.draw()
                print('############################')

            else:
                if again: # first player got another turn
                    print('')
                    print('player 1 turn again')
                    print('')
                else:
                    print('')
                    print('player 1 turn')
                    print('')
                print('enter cell number from (1-6) or enter 403 to quit game or 302 to save game')
                inp = input('enter number: ') #choose a slot to empty the balls in it
                try:
                    inp = int(inp)
                    inp -= 1
                    if inp == 301: # code to save current game
                        print('please enter path to save game as pickle file ')
                        try:
                            save = []
                            save.append(board)
                            save.append(turn2)
                            save.append(mode)
                            save.append(level)
                            pth = input('enter relative path and name of save with it: ')
                            with open(pth+'.pickle', 'wb') as handle:
                                pickle.dump(save, handle, protocol=pickle.HIGHEST_PROTOCOL)
                                continue

                        except:
                            #print('invalid path error')
                            pass

                except:
                    print('invalid')
                    continue
                values_allowed = range(6)


                if inp == 402:  # code to exit the game
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    print('quiting game')
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    return


                if inp in values_allowed: # play a move
                    print('############################')
                    print('previous state of board')
                    board.draw()
                    print('############################')
                    stat = board.play(1, inp)
                    if stat == 3:
                        print('invalid')
                        continue
                    elif stat == 0:
                        board.check_game()
                        print('<<<<>>>>>')
                        print('<<<<>>>>>')
                        print('end of game')
                        print('score 1 ', board.score_1)
                        print('score 2 ', board.score_2)
                        board.draw()
                        break
                        # board.draw()
                    elif stat == 2:
                        # print('player 1 turn again')
                        turn2 = 0
                        again = 1
                    else:
                        # print('player 2 turn')
                        turn2 = 1
                        again = 0

                    print('############################')
                    print('new state of board after player 1 plays')
                    board.draw()
                    print('############################')


                else:
                    print('invalid')
                    continue
                    # board.draw()

                    # board.draw()

    elif mode == 3:# to AI bots playing aganist each other
        again = 0
        while True:
            if turn2 == 1:
                if again:
                    print('')
                    print('player 2 turn again')
                    print('')
                else:
                    print('')
                    print('player 2 turn')
                    print('')
                b = copy.deepcopy(board)
                n = make_tree(0, 'max', b, 0, level)
                print('############################')
                print('previous state of board')
                board.draw()
                print('############################')
                stat = automate_play(n,board ,2)
                if stat == 0:
                    # print('i was here')
                    board.check_game()
                    print('<<<<>>>>>')
                    print('<<<<>>>>>')
                    print('end of game')
                    print('score 1 ', board.score_1)
                    print('score 2 ', board.score_2)
                    board.draw()
                    break
                elif stat == 1:
                    # print('player 1 turn')
                    turn2 = 0
                    again = 0
                elif stat == 2:
                    # print('player 2 turn again')
                    turn2 = 1
                    again = 1

                print('############################')
                print('new state of board after player 2 plays')
                board.draw()
                print('############################')

            else:
                if again:
                    print('')
                    print('player 1 turn again')
                    print('')
                else:
                    print('')
                    print('player 1 turn')
                    print('')

                b = copy.deepcopy(board)
                n = make_tree(0, 'min', b, 0, level)
                print('############################')
                print('previous state of board')
                board.draw()
                print('############################')
                stat = automate_play(n,board ,1)
                if stat == 0:
                    # print('i was here')
                    board.check_game()
                    print('end of game')
                    print('score 1 ', board.score_1)
                    print('score 2 ', board.score_2)
                    board.draw()
                    break
                elif stat == 1:
                    # print('player 2 turn')
                    turn2 = 1
                    again = 0
                elif stat == 2:
                    # print('player 1 turn again')
                    turn2 = 0
                    again = 1

                print('############################')
                print('new state of board after player 1 plays')
                board.draw()
                print('############################')

                # board.draw()

    elif mode == 2: # multiplayer mode
        again = 0
        while True:
            if turn2 == 1:
                if again:
                    print('')
                    print('player 2 turn again')
                    print('')
                else:
                    print('')
                    print('player 2 turn')
                    print('')
                print('enter cell number from (1-6) or enter 404 to quit game or 302 to save game')
                inp = input('enter number: ')
                try:
                    inp = int(inp)
                    inp -= 1
                    if inp == 301:
                        print('please enter path to save game as pickle file ')
                        try:
                            save = []
                            save.append(board)
                            save.append(turn2)
                            save.append(mode)
                            save.append(level)
                            pth = input('enter relative path and name of save with it: ')
                            with open(pth+'.pickle', 'wb') as handle:
                                pickle.dump(save, handle, protocol=pickle.HIGHEST_PROTOCOL)

                        except:
                            #print('invalid path error')
                            pass
                except:
                    print('invalid')
                    continue
                values_allowed = range(6)

                if inp == 402:
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    print('quiting game')
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    return


                if inp in values_allowed:
                    print('############################')
                    print('previous state of board')
                    board.draw()
                    print('############################')
                    stat = board.play(2, inp)
                    if stat == 3:
                        print('invalid')
                        continue
                    elif stat == 0:
                        board.check_game()
                        print('<<<<>>>>>')
                        print('<<<<>>>>>')
                        print('end of game')
                        print('score 1 ', board.score_1)
                        print('score 2 ', board.score_2)
                        board.draw()
                        break
                        # board.draw()
                    elif stat == 2:
                        # print('player 1 turn again')
                        turn2 = 1
                        again = 1
                    else:
                        # print('player 2 turn')
                        turn2 = 0
                        again = 0

                    print('############################')
                    print('new state of board after player 2 plays')
                    board.draw()
                    print('############################')

            else:
                if again:
                    print('')
                    print('player 1 turn again')
                    print('')
                else:
                    print('')
                    print('player 1 turn')
                    print('')
                print('enter cell number from (1-6) or enter 404 to quit game or 302 to save game')
                inp = input('enter number: ')
                try:
                    inp = int(inp)
                    inp -= 1
                    if inp == 301:
                        print('please enter path to save game as pickle file ')
                        try:
                            save = []
                            save.append(board)
                            save.append(turn2)
                            save.append(mode)
                            save.append(level)
                            pth = input('enter relative path and name of save with it: ')
                            with open(pth+'.pickle', 'wb') as handle:
                                pickle.dump(save, handle, protocol=pickle.HIGHEST_PROTOCOL)

                        except:
                            #print('invalid path error')
                            pass
                except:
                    print('invalid')
                    continue
                values_allowed = range(6)

                if inp == 402:
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    print('quiting game')
                    print('xxxxxxxxxxxxxxxxxxxxx')
                    return



                if inp in values_allowed:
                    print('############################')
                    print('previous state of board')
                    board.draw()
                    print('############################')
                    stat = board.play(1, inp)
                    if stat == 3:
                        print('invalid')
                        continue
                    elif stat == 0:
                        board.check_game()
                        print('<<<<>>>>>')
                        print('<<<<>>>>>')
                        print('end of game')
                        print('score 1 ', board.score_1)
                        print('score 2 ', board.score_2)
                        board.draw()
                        break
                        # board.draw()
                    elif stat == 2:
                        # print('player 1 turn again')
                        turn2 = 0
                        again = 1
                    else:
                        # print('player 2 turn')
                        turn2 = 1
                        again = 0

                    print('############################')
                    print('new state of board after player 1 plays')
                    board.draw()
                    print('############################')
