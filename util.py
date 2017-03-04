#file containing utility functions
import networkx as nx

class util:

    def __init__(self, player):
        self.whoseTurn = player
        self.board = self.initializeBoard()
        self.teamHuman = self.initializeHuman()
        self.teamDragon = self.initializeDragon()
        self.transpositionTable = dict()
        self.cachedWin = False  # set to True in winFor() if
        self.cachedWinner = None
        self.depthLimit = 4

#------------------------------------------------------------------------------------------------------------
#                                           START OF MINIMAX FUNCTIONS
#------------------------------------------------------------------------------------------------------------
 # The search space is a tree, but the state space is a graph: there may be several different ways to
# reach a given game state.  The transposition table is a dictionary (hash table) that remembers if
# a game state was seen before, and it it was, what its minimax value is.
# Warning: The transposition table can fill up quickly!
# ** SKELETON OF FUNCTIONS TAKEN FROM CODE SUPPLIED BY MICHAEL HORSCH **
    def minimax(self, depth):
        origTurn = self.whoseTurn
        origBoard = self.board
        print("Depth is :", depth)
        if self.isMaxNode():
            origHuman = self.teamHuman # OG Dict
            maxMoves = [len(self.teamHuman)]
            moveValue = [len(self.teamHuman)] # for util

            for i in range(0, len(maxMoves)):
                #NEEDS TO BE CREATED allLegalMoves
                # make allLegalMoves return a list, for loop through the returned list and add to maxMove
                maxMoves[i] = self.allLegalMoves(self.teamHuman[i]['location'])

            for i in range(0, len(maxMoves)):
                if depth == self.depthLimit:
                    #NEEDS TO BE CREATED getUtility()
                    moveValue[i] = self.getUtility(self.teamHuman[i]['type'], maxMoves[i][0])
                    print("The Util was found to be:", self.getUtility(self.teamHuman[i]['type'], maxMoves[i][0]))

                else:
                    for n in range(0, len(maxMoves[i])):
                        self.move(maxMoves[i][n], self.teamHuman[i]['location'])
                        self.togglePlayer()
                        moveValue[i] = self.minimax(depth+1)[i]
                        self.board = origBoard

            maxMovePair = list(zip(maxMoves, moveValue))
            return [self.argmax(maxMovePair)]

        elif self.isMinNode():
            origDragon = self.teamDragon
            origTurn = self.whoseTurn
            minMoves = [len(self.teamDragon)]
            moveValue = [len(self.teamDragon)]

            for i in range(0, len(minMoves)):
                #NEEDS TO BE CREATED allLegalMoves
                minMoves[i] = self.allLegalMoves(self.teamDragon[i]['location'])

            for i in range(0, len(minMoves)):
                print("Depth Being Checked:", depth, "Found to be", depth == self.depthLimit)
                if depth == self.depthLimit:
                    #NEEDS TO BE CREATED getUtility()
                    moveValue[i] = self.getUtility(self.teamDragon[i]['type'], minMoves[i][0])

                else:
                    for n in range(0, len( minMoves[i])):
                        self.move(minMoves[i][n], self.teamDragon[i]['location'])
                        self.togglePlayer()
                        moveValue[i] = self.minimax(depth+1)[i]
                        self.board = origBoard

            minMovePair = list(zip(minMoves, moveValue))
            return [self.argmin(minMovePair)]

        else:
            print("The unthinkable has happened. Minimax is broken.")
            return None

    def allLegalMoves(self, gamePiece):
        validMoves = []
        gs = self.board

        #check the kings moves
        if (gs[gamePiece] == 'K'):
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] + 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] + 1)) # can move right
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] - 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] - 1)) # can move left
            if (self.legalMove(((gamePiece[0] + 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] + 1, gamePiece[1] + 0)) # can move down
            if (self.legalMove(((gamePiece[0] - 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] - 1, gamePiece[1] + 0)) # can move up
            #check king jumps
            try:
                if (gs[(gamePiece[0] + 0), (gamePiece[1] + 1)] == 'G' and gs[(gamePiece[0] + 0), (gamePiece[0] + 2)] == ' '):
                    validMoves.append((gamePiece[0] + 0, gamePiece[1] + 1)) # can move right
            except KeyError: # if out of range
                print("")

            try:
                if (gs[(gamePiece[0] + 0), (gamePiece[1] - 1)] == 'G' and gs[(gamePiece[0] + 0), (gamePiece[0] - 2)] == ' '):
                    validMoves.append((gamePiece[0] + 0, gamePiece[1] - 1)) # can move left
            except KeyError: # if out of range
                print("")

            try:
                if (gs[(gamePiece[0] + 1), (gamePiece[1] + 0)] == 'G' and gs[(gamePiece[0] + 2), (gamePiece[0] + 0)] == ' '):
                    validMoves.append((gamePiece[0] + 1, gamePiece[1] + 0)) # can move down
            except KeyError: # if out of range
                print("")

            try:
                if (gs[(gamePiece[0] - 1), (gamePiece[1] + 0)] == 'G' and gs[(gamePiece[0] - 2), (gamePiece[0] + 0)] == ' '):
                    validMoves.append((gamePiece[0] - 1, gamePiece[1] + 0)) # can move up
            except KeyError: # if out of range
                print("")

        #check a guards moves
        elif (gs[gamePiece] == 'G'):
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] + 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] + 1)) # can move right
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] - 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] - 1)) # can move left
            if (self.legalMove(((gamePiece[0] + 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] + 1, gamePiece[1] + 0)) # can move down
            if (self.legalMove(((gamePiece[0] - 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] - 1, gamePiece[1] + 0)) # can move up
        #check a dragon moves
        elif (gs[gamePiece] == 'D'):
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] + 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] + 1)) # can move right
            if (self.legalMove(((gamePiece[0] + 0), (gamePiece[1] - 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 0, gamePiece[1] - 1)) # can move left
            if (self.legalMove(((gamePiece[0] + 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] + 1, gamePiece[1] + 0)) # can move down
            if (self.legalMove(((gamePiece[0] - 1), (gamePiece[1] + 0)), gamePiece)):
                validMoves.append((gamePiece[0] - 1, gamePiece[1] + 0)) # can move up
            #diagonal alley
            if (self.legalMove(((gamePiece[0] + 1), (gamePiece[1] + 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 1, gamePiece[1] + 1))
            if (self.legalMove(((gamePiece[0] + 1), (gamePiece[1] - 1)), gamePiece)):
                validMoves.append((gamePiece[0] + 1, gamePiece[1] - 1))
            if (self.legalMove(((gamePiece[0] - 1), (gamePiece[1] - 1)), gamePiece)):
                validMoves.append((gamePiece[0] - 1, gamePiece[1] - 1))
            if (self.legalMove(((gamePiece[0] - 1), (gamePiece[1] + 1)), gamePiece)):
                validMoves.append((gamePiece[0] - 1, gamePiece[1] + 1))
        return validMoves

    def argmax(self, ns):
        """
        find the highest utility,move pair
        :param ns: a list of utility,move pairs
        :return:  the utility,move pair with the highest utility
        """
        maxv,maxm = ns[0]
        for v,m in ns:
            if v > maxv:
                maxv,maxm = v,m
        return maxv,maxm


    def argmin(self, ns):
        """
        find the lowest utility,move pair
        :param ns: a list of utility,move pairs
        :return:  the utility,move pair with the lowest utility
        """
        minv,minm = ns[0]
        for v,m in ns:
            if v < minv:
                minv,minm = v,m
        return minv,minm

    def isMinNode(self):
        """ *** needed for search ***
        :return: True if it's Min's turn to play
        """
        return self.whoseTurn == 'D'


    def isMaxNode(self):
        """ *** needed for search ***
        :return: True if it's Max's turn to play
        """
        return self.whoseTurn == 'H'


    def isTerminal(self):
        """ *** needed for search ***
        :param node: a game tree node with stored game state
        :return: a boolean indicating if node is terminal
        """
        return self.winFor('dragons') or self.winFor('humans')

    def successors(self):
        """ *** needed for search ***
        :param node:  a game tree node with stored game state
        :return: a list of move,state pairs that are the next possible states
        """
        blanks = self.allBlanks()
        next = self.togglePlayer()
        states = map(lambda v: self.move(v,self.whoseTurn), blanks)
        nodes = [(m,TicTacToe(s,next)) for m,s in states]  # create move,state pairs!
        return nodes


    def utility(self):
        """ *** needed for search ***
        :return: 1 if win for X, -1 for win for O, 0 for draw
        """
        if self.winFor('H'):
            return 1
        elif self.winFor('D'):
            return -1
        else:
            return 0


    # all remaining methods are to assist in the calculatiosn

    def winFor(self, player):
        """
        Check if it's a win for player.
        Note the use of a cache.  This prevents re-computation in functions isTerminal() and utility()
        :param player: either 'H' or 'D'
        :return: True if king is killed or king is in 4th row
        """
        if self.cachedWin is False:
            # rows columns diagonals
            won = (not self.teamHuman[0]['status']) or (self.teamHuman[0]['location'][0] == 4)
            if won:
                self.cachedWin = True
                self.cachedWinner = player
                return True
            else:
                return False
        else:
            return player == self.cachedWinner

    def togglePlayer(self):
        """
        :param p: either 'H' or 'D'
        :return:  the other player's symbol
        """
        if self.whoseTurn == 'H':
            self.whoseTurn = 'D'
            return 'D'
        else:
            self.whoseTurn = 'D'
            return 'H'

#------------------------------------------------------------------------------------------------------------
#                                           START OF UTIL FUNCTIONS
#------------------------------------------------------------------------------------------------------------
    def getUtility(self, gamePiece, local):

        if (gamePiece == 'K'):
            return self.gaurdUtil(gamePiece, local)
        elif (gamePiece == 'G'):
            return self.guardUtil(gamePiece, local)
        elif (gamePiece == 'D'):
            return self.dragonUtil(gamePiece, local)

    def guardUtil(self, gamePiece, local):
        maxUtil = 0
        enemyUtil = self.enemiesAround(gamePiece, local) * -10
        allyUtil = self.alliesAround(gamePiece, local) * 10
        if (allyUtil > enemyUtil and allyUtil > 1):
            maxUtil = allyUtil - enemyUtil
        else:
            maxUtil = enemyUtil - allyUtil
        return(maxUtil)

    def dragonUtil(self, gamePiece, local):
        minUtil = 0
        enemyUtil = self.enemiesAround(gamePiece, local) * 10
        allyUtil = self.alliesAround(gamePiece, local)	* -10
        minUtil = enemyUtil + allyUtil
        return(minUtil)

    def kingUtil(self, gamePiece, local):
        maxUtil1 = self.guardUtil(gamePiece, local)
        maxUtil2 = self.endUtil(gamePiece, local)
        if (maxUtil1 > maxUtil2 and maxUtil1 > 0) or maxUtil2 < 0:
            return maxUtil1
        elif maxUtil2 > maxUtil1 and maxUtil2 > 0 or maxUtil1 < 0:
            return maxUtil2
        else:
            print("error in kingUtil")
            return 0;

    def enemiesAround(self, gamePiece, local):
        gs = self.board
        if (gamePiece == 'K' or gamePiece == 'G'):
            count = 0
            for i in range (0,len(self.teamHuman)):
                if (self.teamHuman[i]['status'] == True):
                    locationY = local[0]
                    locationX = local[1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'D'):
                            count +=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY -1, locationX]) == 'D'):
                            count +=1

                    if (locationX + 1 > 4):
                        locationX = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'D'):
                            count +=1

                    if (locationY + 1 > 4):
                        locationY = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'D'):
                            count +=1
            return(count)

        if (gamePiece == 'D'):
            count = 0
            for i in range (0,len(self.teamDragon)):
                if (self.teamDragon[i]['status'] == True):
                    locationY = local[0]
                    locationX = local[1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            if (gs[locationY, locationX] == 'K'):
                                count-=100
                            else:
                                count-=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'G' or (gs[locationY, locationX - 1]) == 'K'):
                            if (gs[locationY, locationX - 1] == 'K'):
                                count-=100
                            else:
                                count-=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            if (gs[locationY, locationX] == 'K'):
                                count-=100
                            else:
                                count-=1
                    else:
                        if ((gs[locationY - 1, locationX]) == 'G' or (gs[locationY - 1, locationX]) == 'K'):
                            if (gs[locationY - 1 , locationX] == 'K'):
                                count-=100
                            else:
                                count-=1

                    if (locationX + 1 > 4):
                        locationX = 4
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            if (gs[locationY, locationX] == 'K'):
                                count-=100
                            else:
                                count-=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'G' or (gs[locationY, locationX + 1]) == 'K'):
                            if (gs[locationY, locationX + 1] == 'K'):
                                count-=100
                            else:
                                count-=1

                    if (locationY + 1 > 4):
                        locationY = 4
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            if (gs[locationY, locationX] == 'K'):
                                count-=100
                            else:
                                count-=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'G' or (gs[locationY + 1, locationX]) == 'K'):
                            if (gs[locationY + 1, locationX] == 'K'):
                                count-=100
                            else:
                                count-=1
            return(count)


    def alliesAround(self, gamePiece, local):
        gs = self.board
        count = 0
        if (gamePiece == 'K' or gamePiece == 'G'):
            for i in range (0,len(self.teamHuman)):
                if (self.teamHuman[i]['status'] == True):
                    locationY = local[0]
                    locationX = local[1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'G' or (gs[locationY, locationX - 1]) == 'K'):
                            count +=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY - 1, locationX]) == 'G' or (gs[locationY - 1, locationX]) == 'K'):
                            count +=1

                    if (locationX + 1 > 4):
                        locationX = 4
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'G' or (gs[locationY, locationX + 1]) == 'K'):
                            count +=1

                    if (locationY + 1 > 4):
                        locationY = 4
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'G' or (gs[locationY + 1, locationX]) == 'K'):
                            count +=1
            return(count)

        if (gamePiece == 'D'):
            count = 0
            for i in range (0,len(self.teamDragon)):
                if (self.teamDragon[i]['status'] == True):
                    locationY = local[0]
                    locationX = local[1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'D'):
                            count +=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY -1, locationX]) == 'D'):
                            count +=1

                    if (locationX + 1 > 4):
                        locationX = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'D'):
                            count +=1

                    if (locationY + 1 > 4):
                        locationY = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'D'):
                            count +=1
            return(count)

    def endUtil(self, gamePiece, local):
        gs = self.board
        if (gamePiece == 'K'):
            locationY = local[0]
            distanceFromEnd = 4 - locationY

            if (distanceFromEnd == 1):
                return(100)
            if (distanceFromEnd == 2):
                return(60)
            if (distanceFromEnd == 3):
                return(40)
            if (distanceFromEnd == 4):
                return(20)



#------------------------------------------------------------------------------------------------------------
#                                           END OF MINIMAX/UTIL FUNCTIONS
#------------------------------------------------------------------------------------------------------------

    def printLocation(self):
        """
        A pleasant view of the current game state
        :return: nothing
        """
        for r in range(0, 5):
            print("+---------+---------+---------+---------+---------+")
            print("|", end="")
            for c in range(0, 4):
                print("(", r, ",",c, ")",  end="")
                print("|",end="")
            print("(", r, ",",4, ")", end="")
            print("|")
            print("|", end="")
            for c in range(0, 4):
                print("   ", self.board[r,c], "   ", end="")
                print("|",end="")
            print("   ", self.board[r,4], "   ", end="")
            print("|")
        print("+---------+---------+---------+---------+---------+")

    def getBoard(self):
        """ *** needed for search ***
        Translate the board description into a string.  Could be used as for a hash table...
        :return: A string that describes the board in the current state.
        """
        s=""
        for r in range(0, 5):
            for c in range(0, 4):
                s+=self.board[r,c]
        return s

    def printBoard(self):
        """
        A pleasant view of the current game state
         :return: nothing
        """
        for r in range(0, 5):
            print("+-+-+-+-+-+")
            print("|", end="")
            for c in range(0, 4):
                print(self.board[r,c], end="")
                print("|",end="")
            print(self.board[r,4], end="")
            print("|")
        print("+-+-+-+-+-+")

    def initializeBoard(self):
        """
        :return: an initialized dictonary representing the game board with all
                 pieces in starting placement
        """
        boardDict = dict()
        for r in range(0,5):
            for c in range(0,5):
                    boardDict[r,c] = ' '
        boardDict[0,2] = 'K' # place king
        boardDict[1,1] = 'G' # place guards
        boardDict[1,2] = 'G'
        boardDict[1,3] = 'G'
        boardDict[3,0] = 'D' # place dragons
        boardDict[3,1] = 'D'
        boardDict[3,2] = 'D'
        boardDict[3,3] = 'D'
        boardDict[3,4] = 'D'
        print("Initialized Board")
        return boardDict

    def initializeHuman(self):
        """
        :return: an initialized dictonary of all current and possible humans
        """
        humanDict = dict()
        humanDict[0] = {'type' : 'K', 'location' : (0,2), 'status' : True} # place king
        humanDict[1] = {'type' : 'G', 'location' : (1,1), 'status' : True}
        humanDict[2] = {'type' : 'G', 'location' : (1,2), 'status' : True}
        humanDict[3] = {'type' : 'G', 'location' : (1,3), 'status' : True}
        return humanDict

    def initializeDragon(self):
        """
        :return: an initialized dictonary of all current and possible dragons
        """
        dragonDict = dict()
        dragonDict[0] = {'type' : 'D', 'location' : (3,0), 'status' : True}
        dragonDict[1] = {'type' : 'D', 'location' : (3,1), 'status' : True}
        dragonDict[2] = {'type' : 'D', 'location' : (3,2), 'status' : True}
        dragonDict[3] = {'type' : 'D', 'location' : (3,3), 'status' : True}
        dragonDict[4] = {'type' : 'D', 'location' : (3,4), 'status' : True}
        dragonDict[5] = {'type' : 'D', 'location' : None, 'status' : False}
        dragonDict[6] = {'type' : 'D', 'location' : None, 'status' : False}
        dragonDict[7] = {'type' : 'D', 'location' : None, 'status' : False}
        dragonDict[8] = {'type' : 'D', 'location' : None, 'status' : False}
        dragonDict[9] = {'type' : 'D', 'location' : None, 'status' : False}
        return dragonDict

    def updateDictLocale(self, where, who):
        """
        :param where: location to be updated in piece dictionary
        :param who: location of game piece needing to be updated
        :return: No return used. For testing: 1 for success, 0 for falure
        """
        for i in range(0, len(self.teamHuman)):
            if (self.teamHuman[i]['location'] == who and self.teamHuman[i]['status']):
                self.teamHuman[i]['location'] = where
                return 1

        for i in range(0, len(self.teamDragon)):
            if (self.teamDragon[i]['location'] == who and self.teamDragon[i]['status']):
                self.teamDragon[i]['location'] = where
                return 1
        return 0


    def move(self, where, who):
        """
        :param where: end location of place to be moved to by piece
        :param who: location of game piece to be moved
        :return: the new state of the game board
        """
        gs = self.board
        if (self.legalMove(where, who)):
            gs[where] = gs[who]
            gs[who] = ' '
            self.updateDictLocale(where, who)
           # gs = gameState.copy()
        self.takeOver(where)
        return gs

    def move2(self, where, who):
        """
        :param where: end location of place to be moved to by piece
        :param who: location of game piece to be moved
        :return: the new state of the game board
        """
        gs = self.board
        gs[where] = gs[who]
        gs[who] = ' '
        self.updateDictLocale(where, who)
        # gs = gameState.copy()
        self.takeOver(where)
        return gs

    def validPiece(self, gamePiece):
        """
        :param gamePiece: location of gamePiece to be checked for validity
        :return: True if provided location holds a live gamePiece
        """
        for i in range(0, len(self.teamHuman)):
            if (self.teamHuman[i]['location'] == gamePiece and self.teamHuman[i]['status']):
                #print(gamePiece)
                #print(self.teamHuman[i]['location'])
                return True
        for i in range(0, len(self.teamDragon)):
            if (self.teamDragon[i]['location'] == gamePiece and self.teamDragon[i]['status']):
                #print(gamePiece)
                #print(self.teamDragon[i]['location'])
                return True
        return False

    def legalMove(self, location, gamePiece):
        """
        :param location: location to be moved to by piece
        :param gamePiece: location of piece to be moved
        :return: True if is legal move, False otherwise
        """
        gs = self.board

        try:
            gs[location] == ' '
        except KeyError: # if out of range
            return False

        #moving to a blank space
        if (gs[location] == ' '):
            #moving the guard (humanoid player)
            if (gs[gamePiece] == 'G'):
                if (location == ((gamePiece[0] + 0), (gamePiece[1] + 1)) or     #move right
                    location == ((gamePiece[0] + 0), (gamePiece[1] - 1)) or     #move left
                    location == ((gamePiece[0] + 1), (gamePiece[1] + 0)) or     #move up
                    location == ((gamePiece[0] - 1), (gamePiece[1] + 0))):      # move down
                        return True
            #move the king over the guard -- how most players would try (humanoid player)
            elif (gs[gamePiece] == 'K'):
                if (location == ((gamePiece[0] + 0), (gamePiece[1] + 1)) or     #move right 1 space
                    location == ((gamePiece[0] + 0), (gamePiece[1] - 1)) or     #move left 1 space
                    location == ((gamePiece[0] + 1), (gamePiece[1] + 0)) or     #move up 1 space
                    location == ((gamePiece[0] - 1), (gamePiece[1] + 0))):    # move down 1 space
                        return True
            #moving the dragons (dragon player)
            elif (gs[gamePiece] == 'D'):
                if (location == ((gamePiece[0] + 0), (gamePiece[1] + 1)) or     #move right
                    location == ((gamePiece[0] + 0), (gamePiece[1] - 1)) or     #move left
                    location == ((gamePiece[0] + 1), (gamePiece[1] + 0)) or     #move up
                    location == ((gamePiece[0] - 1), (gamePiece[1] + 0)) or     #move down
                    location == ((gamePiece[0] + 1), (gamePiece[1] + 1)) or     #move diagonal back right
                    location == ((gamePiece[0] + 1), (gamePiece[1] - 1)) or     #move diagonal back let
                    location == ((gamePiece[0] - 1), (gamePiece[1] - 1)) or     #move diagonal up left
                    location == ((gamePiece[0] - 1), (gamePiece[1] + 1))):      #move diagonal up right
                        return True
            else:
                #print("\n" + "Illegal Move")
                return False
        #jumping a guard with the king -- this will use a recursive call to check an additional space
        #**If a player tries to jump a guard by moving the king onto the guard -- Slighty redundant.
        elif (gs[gamePiece] == 'K' and gs[location] == 'G'):
            if (location == ((gamePiece[0] + 0), (gamePiece[1] + 1))):   #check move right
                  if (self.legalJump(((gamePiece[0] + 0), (gamePiece[1] + 2)),gamePiece)):
                    self.move2(((gamePiece[0] + 0), (gamePiece[1] + 2)),gamePiece)
                    return False
            elif (location == ((gamePiece[0] + 0), (gamePiece[1] - 1))): #check move left
                  if (self.legalJump(((gamePiece[0] + 0), (gamePiece[1] - 2)),gamePiece)):
                    self.move2(((gamePiece[0] + 0), (gamePiece[1] - 2)),gamePiece)
                    return False
            elif (location == ((gamePiece[0] + 1), (gamePiece[1] + 0))): #check move down
                if (self.legalJump(((gamePiece[0] + 2), (gamePiece[1] + 0)),gamePiece)):
                    self.move2(((gamePiece[0] + 2), (gamePiece[1] + 0)),gamePiece)
                    return False
            elif (location == ((gamePiece[0] - 1), (gamePiece[1] + 0))): #check move up
                  if (self.legalJump(((gamePiece[0] - 2), (gamePiece[1] + 0)),gamePiece)):
                    self.move2(((gamePiece[0] - 2), (gamePiece[1] + 0)),gamePiece)
                    return False
        #illegal movement
        else:
            #print("\n" + "Illegal Move")
            return False

    def legalJump(self, location, gamePiece):
        """
        :param location: location to be moved to by piece
        :param gamePiece: location of piece to be moved
        :return: True if is legal move, False otherwise
        """
        gs = self.board
        try:
            gs[location] == ' '
        except KeyError: # if out of range
            return False

        #moving to a blank space
        if (gs[location] == ' '):
            #move the king over the guard -- how most players would try (humanoid player)
            if (gs[gamePiece] == 'K'):
                if (location == ((gamePiece[0] + 0), (gamePiece[1] + 1)) or     #move right 1 space
                    location == ((gamePiece[0] + 0), (gamePiece[1] - 1)) or     #move left 1 space
                    location == ((gamePiece[0] + 1), (gamePiece[1] + 0)) or     #move up 1 space
                    location == ((gamePiece[0] - 1), (gamePiece[1] + 0)) or
                    location == ((gamePiece[0] + 0), (gamePiece[1] + 2)) or     #move right 1 space
                    location == ((gamePiece[0] + 0), (gamePiece[1] - 2)) or     #move left 1 space
                    location == ((gamePiece[0] + 2), (gamePiece[1] + 0)) or     #move up 1 space
                    location == ((gamePiece[0] - 2), (gamePiece[1] + 0))):    # move down 1 space
                        return True
            else:
                print("\n" + "Illegal Move")
                return False
        else:
            print("\n" + "Illegal Move")
            return False

    def takeOver(self, gamePiece):
        """
        :param gamePiece: the piece being moved
        :return: 1 if win for X, -1 for win for O, 0 for draw
        """
        gs = self.board
        if (gs[gamePiece] == 'D'):
            for i in range (1,len(self.teamHuman)):
                if (self.teamHuman[i]['status'] == True):
                    count = 0
                    locationY = self.teamHuman[i]['location'][0]
                    locationX = self.teamHuman[i]['location'][1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'D'):
                            count +=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY -1, locationX]) == 'D'):
                            count +=1

                    if (locationX + 1 > 4):
                        locationX = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'D'):
                            count +=1

                    if (locationY + 1 > 4):
                        locationY = 4
                        if ((gs[locationY, locationX]) == 'D'):
                            count +=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'D'):
                            count +=1
                    if (count >2):
                        print("Taken")
                        self.teamHuman[i]['status'] = False;
                        change = self.teamHuman[i]['location']
                        min = 0
                        for i in range (0, len(self.teamDragon)):
                            if (self.teamDragon[i]['status'] == False):
                                min = i
                                if (i < min):
                                    min = i
                        self.teamDragon[min]['status'] = True
                        self.teamDragon[min]['location'] = change
                        gs[change] = 'D'

        if (gs[gamePiece] == 'G' or gs[gamePiece] == 'K'):
            for i in range (0,len(self.teamDragon)):
                if (self.teamDragon[i]['status'] == True):
                    count = 0
                    locationY = self.teamDragon[i]['location'][0]
                    locationX = self.teamDragon[i]['location'][1]
                    if (locationX - 1 < 0):
                        locationX = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX - 1]) == 'G' or (gs[locationY, locationX - 1]) == 'K'):
                            count +=1

                    if (locationY - 1 < 0):
                        locationY = 0
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY - 1, locationX]) == 'G' or (gs[locationY - 1, locationX]) == 'K'):
                            count +=1

                    if (locationX + 1 > 3):
                        locationX = 3
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY, locationX + 1]) == 'G' or (gs[locationY, locationX + 1]) == 'K'):
                            count +=1

                    if (locationY + 1 > 3):
                        locationY = 3
                        if ((gs[locationY, locationX]) == 'G' or (gs[locationY, locationX]) == 'K'):
                            count +=1
                    else:
                        if ((gs[locationY + 1, locationX]) == 'G' or (gs[locationY + 1, locationX]) == 'K'):
                            count +=1

                    if (count >1):
                        print("Taken")
                        self.teamDragon[i]['status'] = False;
                        change = self.teamDragon[i]['location']
                        gs[change] = ' '

        if (gs[gamePiece] == 'D'):
             if (self.teamHuman[0]['status'] == True):
                count = 0
                locationY = self.teamHuman[0]['location'][0]
                locationX = self.teamHuman[0]['location'][1]
                print(gs[locationX, locationY])
                if (locationX - 1 < 0):
                    locationX = 0
                    if ((gs[locationY, locationX]) == 'D'):
                        count +=1
                else:
                    if ((gs[locationY, locationX - 1]) == 'D'):
                        count +=1

                if (locationY - 1 < 0):
                    locationY = 0
                    if ((gs[locationY, locationX]) == 'D'):
                        count +=1
                else:
                    if ((gs[locationY -1, locationX]) == 'D'):
                        count +=1

                if (locationX + 1 > 3):
                    locationX = 3
                    if ((gs[locationY, locationX]) == 'D'):
                        count +=1
                else:
                    if ((gs[locationY, locationX + 1]) == 'D'):
                        count +=1

                if (locationY + 1 > 3):
                    locationY = 3
                    if ((gs[locationY, locationX]) == 'D'):
                        count +=1
                else:
                    if ((gs[locationY + 1, locationX]) == 'D'):
                        print(count)
                        count +=1
                print(count)
                if (count > 3):
                    print("PLAYER 2 WINS")
                    self.teamHuman[i]['status'] = False;
                    change = self.teamHuman[0]['location']
                    min = 0
                    for i in range (0, len(self.teamDragon)):
                        if (self.teamDragon[i]['status'] == False):
                            min = i
                            if (i < min):
                                min = i
                    self.teamDragon[min]['status'] = True
                    self.teamDragon[min]['location'] = change
                    gs[change] = 'PLAYER 2 WINS'
        return gs
