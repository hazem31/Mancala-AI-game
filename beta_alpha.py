
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
