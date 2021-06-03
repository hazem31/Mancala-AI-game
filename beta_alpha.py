def beta_alpha(node):

    curr_beta = node.beta
    curr_alpha = node.alpha
	
    for n in node.childs:
    
        value = beta_alpha(n)  
        n.aplha = curr_alpha
        n.beta = curr_beta
        if value is None: 
            continue
        if node.type == 'max':    
            if value > curr_alpha:  
                curr_alpha = value
        else:  
            if value < curr_beta: 
                curr_beta = value
        if curr_alpha >= curr_beta:     
            return None

    return node.value
