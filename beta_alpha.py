
def beta_alpha(node):
	
    curr_alpha = node.alpha  
    curr_beta = node.beta    

    for n in node.childs:
	value = beta_alpha(n) 
        n.aplha = curr_alpha   
        n.beta = curr_beta     
        if node.type == 'max':    
            if value > curr_alpha:  
                curr_alpha = value   
        else:   
            if value < curr_beta: 
                curr_beta = value
        if curr_alpha >= curr_beta:       
            return None
    if node.type == 'max': 
        node.value = curr_alpha
    else:  #minimzer return beta
        node.value = curr_beta

    return node.value
