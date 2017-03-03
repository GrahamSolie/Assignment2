import util as u



def main():
    i = 0
    prog = u.util('D')
    prog.printBoard()

    print('*DRUM ROLL*', prog.maxmini(0))
    '''
    prog.move((2,2),(1,2))
    prog.move((2,1),(3,1))
    prog.move((2,3),(3,3))
    prog.move((1,2),(2,2))
    prog.move((2,0),(3,0))
    prog.move((1,0),(2,0))
    prog.move((2,4),(3,4))
    prog.move((1,4),(2,4))
    '''
    """
    Test To capture a Guard

    prog.move((2,2),(1,2))
    prog.move((2,1),(3,1))
    prog.move((2,3),(3,3))
    prog.move((1,2),(2,2))
    prog.move((2,0),(3,0))
    prog.move((1,0),(2,0))
	"""

    #prog.move((2,4),(3,4))
    #prog.move((2,2),(1,2))
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
        print("Please provide input (type help for more options):", end="")

main()
