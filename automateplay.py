def automate_play(node,board,player=2):
    value = beta_alpha(node)
    for i in range(len(node.childs)):
        if node.childs[i].value is None:
            continue

        if value == node.childs[i].value:
            stat = board.play(player,node.childs[i].how_to_get_here)
            return stat

    return 0
