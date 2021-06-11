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
        while True:
            again = 0
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