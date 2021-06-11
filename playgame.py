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