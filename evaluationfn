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
