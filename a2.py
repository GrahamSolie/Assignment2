import util as u



def main():
    i = 0
    prog = u.util('D')
    prog.printBoard()
    test = prog.argmax([((0,2),[((0,3),100),((10,4),2),((0,5),5)]),((1,2),[((0,1),-2),((1,0),0)])])
    print(test)
    print("Please provide input (type help for more options):", end="")

    while turn(prog):

        i = 1 + i

    print("You played ", i, " number of turns!")

def turn(prog):

    while (True):
        uin = input()
        if (uin == "help" or uin == "Help"):
            print("Valid Commands:")
            print("help: prints out help menu")
            print("kill: ends the game")
            print("quit: ends the game")
            print("play #: plays # number of games")
            print("play: plays a single game")
            print("move: for testing. Manually move pieces")
            print("test: toggles the testing flag")

        elif(uin == "test" or uin == "Test"):

            print("Testing toggled to", prog.toggleTesting())

        elif(uin == "move" or uin == "Move" or uin == "move2" or uin == "Move2"):

            loop = True

            while (loop):

                loop = False
                prog.printLocation()
                print("input piece location(in form of tuple):", end="")
                pin = input()
                if(pin == "quit" or pin == "Quit" or pin == "kill" or pin == "Kill"):
                    break;
                gp = tuple(int(x) for x in pin[1:-1].split(','))

                if not (prog.validPiece(gp)):
                    loop = True
                    print("Invalid Selection")
                else:
                    print("input end location(in form of tuple):", end="")
                    ein = input()
                    if(ein == "quit" or ein == "Quit" or ein == "kill" or ein == "Kill"):
                        break;
                    el = tuple(int(x) for x in ein[1:-1].split(','))
                    if not (prog.legalMove(el, gp)):
                        loop = True
                        print("Invalid Selection")
                    else:
                        if(uin == "move" or uin == "Move"):
                            prog.board = prog.move(el, gp)
                        else:
                            prog.board = prog.move2(el, gp)
        elif(uin == 'trogdor' or uin == 'Trogdor'):
            print("BURNINATING THE COUNTRY SIDE!!")
        elif(uin == "quit" or uin == "Quit" or uin == "kill" or uin == "Kill"):
            break;
        elif(uin == "play" or uin == "Play"):
            play(prog)
        print("Please provide input (type help for more options):", end="")

def play(prog):
    startTurn = 0
    i = 0
    while prog.utility() == 0 and i < 50:
            print("===========START OF TURN", i+1,"===========")
            mmResult = prog.minimax(startTurn)
            mmResult = mmResult[0]
            prog.printBoard()
            print("mmResult for turn:", i+1, "is", mmResult[0][0],  mmResult[0][1][0][0])
            prog.move(mmResult[0][0], mmResult[0][1][0][0])
            print("===========END OF TURN", i+1,"===========")
            prog.printBoard()
            print("")


            i = i+1
            prog.togglePlayer()
    if prog.utility() == 1:
        print("Humans Win!")
    elif prog.utility() == -1:
        print("Dragons Win!")
    else:
        print("Draw")

main()
