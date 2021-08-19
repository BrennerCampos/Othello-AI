import random
import time


#           OTHELLO AI PLAYERS
#           JUST RUN AND ENTER DESIRED SETTINGS FOR EACH PLAYER
#           PROGRAM WILL RUN BY ITSELF AND PIT THE AI PLAYERS AGAINST EACH OTHER


# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are the two colors, 0 are empty squares
class Board:
    # make a starting board.  There are four pieces in the center
    def __init__(self):
        self.state = [0] * 100
        self.state[44] = 1
        self.state[45] = -1
        self.state[54] = -1
        self.state[55] = 1

    # Returns the score as the difference between the number of 1s and the number of -1s (From Player X's point of view)
    def evaluate(self):
        value = 0
        for i in range(100):
            if self.state[i] == 1:
                value = value + 1
            elif self.state[i] == -1:
                value = value - 1
        return value

    # Returns the score as a tuple of individual scores for both X and O
    def evaluate_pieces(self):
        X_score = 0
        O_score = 0
        for i in range(100):
            if self.state[i] == 1:
                X_score += 1
            elif self.state[i] == -1:
                O_score += 1
        # Creates tuple with both separate scores
        individual_scores = (X_score, O_score)
        return individual_scores

        # returns a new board that is a copy of the current board (makes a deep copy)

    def copy(self):
        board = Board()
        for i in range(100):
            board.state[i] = self.state[i]
        return board

    # given a x,y position, returns the tile within the 1d list
    def index(self, x, y):
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            return self.state[x + y * 10]
        else:
            # out of bounds, return -2 for error
            return -2

    # FIX <<--
    def score(self, player, heuristic):

        value = 0
        # Getting the number of points we would gain with move
        score = self.evaluate()

        if heuristic == True:

            # the more pieces you can capture at a time the bigger the bonus
            if score == 1:
                value += 1
            if score == 2:
                value += 2
            if score == 3:
                value += 4
            if score == 4:
                value += 7
            if score > 5:
                value += 10

            corner_bonus = 10
            edge_bonus = 5

            # Giving a good bonus for corners
            # Top Left
            if player == self.index(0, 0):      # self.state[0]
                value *= corner_bonus
            # Top Right
            if player == self.index(0, 9):      # self.state[9]
                value *= corner_bonus
            # Bottom Left
            if player == self.index(9, 0):      # self.state[90]
                value *= corner_bonus
            # Bottom Right
            if player == self.index(9, 9):      # self.state[99]
                value *= corner_bonus

            # Giving the edges a bonus as well
            for x in range(8):
                # Top Edge
                if self.index(x + 1, 0):
                    value *= edge_bonus
                # Left Edge
                if self.index(x + 1, 9):
                    value *= edge_bonus
            for y in range(8):
                # Right Edge
                if self.index(0, y + 1):
                    value *= edge_bonus
                # Bottom Edge
                if self.index(9, y + 1):
                    value *= edge_bonus
        # total summed value = score
        score += value
        if player != 1:
           score = -score
        return score

    # given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
    def canplace(self, x, y, id):
        # square is not empty? return false
        if self.index(x, y) != 0:
            return False
        # these functions compute the 8 different directions
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # for each direction...
        for xop, yop in dirs:
            # move one space.  is the piece the opponent's color?
            i, j = xop(x), yop(y)
            if self.index(i, j) != -id:
                # no, then we'll move on to the next direction
                continue
            # keep going until we hit our own piece
            i, j = xop(i), yop(j)
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                return True
        # if I can't capture in any direction, I can't place here
        return False

    # returns a list of all valid x,y moves for a given id (player)
    def validmoves(self, id):
        moves = []
        for x in range(10):
            for y in range(10):
                if self.canplace(x, y, id):
                    moves = moves + [(x, y)]
        return moves

    # Giving board objects instead of numbers like validmoves
    def allmoves(self, id):
        boards = []
        for move in self.validmoves(id):
            newboard = self.copy()
            newboard.place(move[0], move[1], id)
            boards.append(newboard)
        return boards

    # print out the board.  1 is X, -1 is O
    def printboard(self):
        for y in range(10):
            line = ""
            for x in range(10):
                if self.index(x, y) == 1:
                    line = line + "X"
                elif self.index(x, y) == -1:
                    line = line + "O"
                else:
                    line = line + "."
            print(line)

    # state is an end game if there are no empty places
    def end(self):
        if len(self.validmoves(1)) == 0 and len(self.validmoves(-1)) == 0:
            return True
        return not 0 in self.state

    def place(self, x, y, id):
        # don't bother if it isn't a valid move
        if not self.canplace(x, y, id):
            return
        # place your piece at x,y
        self.state[x + y * 10] = id
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # go through each direction
        for xop, yop in dirs:
            i, j = xop(x), yop(y)
            # move one space - is the piece the opponent's color?
            if self.index(i, j) != -id:
                # if no, then we cant capture in this direction
                continue
            # keep going until we hit our own piece
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
                # if we found a piece of our own color, then this is a v....
                if self.index(i, j) == id:
                    k, l = xop(x), yop(y)
                    # go back and flip all the pieces to my color
                    while k != i or l != j:
                        self.state[k + l * 10] = id  # mutates my existing board - one change from canplace
                        k, l = xop(k), yop(l)


def game_settings(player):
    n_depth = 0
    heuristic = False
    seenlist_bool = False

    # Initiallizing identifier for the mode to be chosen for current player
    master_mode = -1

    # Distiguishing what player we're working with
    if player == 1:
        player_piece = "X"
    else:
        player_piece = "O"

    print(" //--- SETTINGS for PLAYER '" + player_piece + "'----------//")
    print()

    # Asking user for ai mode to implement for current player...
    while True:
        print("What AI mode for Player " + player_piece + " ?    1/2")
        print("(Greedy = 1,      MiniMax = 2)")
        response = input(">")
        response = response.lower().replace(" ", "")

        # ai_mode "1" = Greedy
        if response == "1":
            ai_mode = 1
            break

        # ai_mode "2" = Minimax
        elif response == "2":
            ai_mode = 2
            break
        else:
            print("Invalid response, try again!")

    # If ai_mode is "2", Minimax
    if ai_mode == 2:
        # Ask user for "n" depth
        while True:
            print("What depth minimax?    Type a number from 1 up to 5")
            response = input(">")
            response = response.lower().replace(" ", "")
            # Assigning n-depth and master_mode depending on the player
            if response == "1":
                n_depth, master_mode = 1, 1
                break
            elif response == "2":
                n_depth, master_mode = 2, 2
                break
            elif response == "3":
                n_depth, master_mode = 3, 3
                break
            elif response == "4":
                n_depth, master_mode = 4, 4
                break
            elif response == "5":
                n_depth, master_mode = 5, 5
                break
            else:
                print("Invalid response, try again!")



        # Ask user if they want to implement a seen-list for current player
        while True:
            print("Use seen list?   Y/N")
            response = input(">")
            response = response.lower().replace(" ", "")
            # User response to seen-list
            if response == "y":
                seenlist_bool = True
                break
            elif response == "n":
                seenlist_bool = False
                break
            else:
                print("Invalid response, try again!")

    # Ask user if they want to implement heuristics for current player
    while True:
        print("Use heuristics?   Y/N")
        response = input(">")
        response = response.lower().replace(" ", "")
        # User response to heuristics
        if response == "y":
            heuristic = True
            break
        elif response == "n":
            heuristic = False
            break
        else:
            print("Invalid response, try again!")

    # PRINTING SETTINGS --------------------------------------------------------
    # --------------------------------------------------------------------------

    print()
    print("--- SETTING SUMMARY for PLAYER '" + player_piece + "' --- //")
    print()

    if ai_mode == 1:
        master_mode = 0
        if player == 1:
            print("Ai Mode:  Greedy  for 'X'")
        else:
            print("Ai Mode:  Greedy  for 'O'")
    else:
        # If it's player 1 ('X')
        if player == 1:
            print("Ai Mode: Minimax (Depth of " + str(n_depth) + ") for 'X'")
            if heuristic:
                print("Heuristics for 'X' : enabled")
            else:
                print("Heuristics for 'X' : disabled")

            if seenlist_bool:
                print("Seen list for 'X' : enabled")
            else:
                print("Seen list for 'X' : disabled")

        # If it's player -1 ('O')
        else:
            print("Ai Mode: Minimax (Depth of " + str(n_depth) + ") for 'O'")
            if heuristic:
                print("Heuristics for 'O' : enabled")
            else:
                print("Heuristics for 'O' : disabled")

            if seenlist_bool:
                print("Seen list for 'O' : enabled")
            else:
                print("Seen list for 'O' : disabled")
        print()
        print()
        print("---")
        print()
        print()

    list_thing = (master_mode, n_depth, heuristic, seenlist_bool)

    return list_thing


#  ===========  GREEDY ===========================================================
#  -------------------------------------------------------------------------------

# Greedy takes board and player
def greedy(board, player, heuristic):
    # Consider every possible move first
    moves = board.allmoves(player)

    # Now go through all the moves and score them
    for i in range(len(moves)):
        moves[i] = (moves[i].score(player, heuristic), moves[i])
    # Sorting them with biggest values first
    moves.sort(reverse=True, key=lambda x: x[
        0])  # for every "moves.sort(reverse=True)", replace  with "moves.sort(reverse=True,key=lambda x:x[0])"
    # index = 0
    # print moves
    # topscore = moves[0][0]

    # Choose_move becomes the board [ ][1] of one of the moves (randomly through pickone)
    chosen_move = pickone(moves)[1]
    # return that new board with chosen move
    return chosen_move


#  =========== MINI-MAX =======================================================
#  ____________________________________________________________________________

def minimax_n(board, player, n_depth, top, seen_list, heuristic):
    # print(player)
    # print(top)
    times = 0
    cons = 1
    # if player == 1 and top == True:
    # print(" --- Player 'X' is thinking --- ")
    # else:
    # print(" --- Player 'O' is thinking --- ")

    # Get all my moves
    moves = board.allmoves(player)

    # Go through all moves and score
    for i in range(len(moves)):
        value = moves[i].score(player, heuristic)
        # If end game, stop and use that score
        if moves[i].end():
            moves[i] = (value, moves[i])
        # OR if our opponent has no more valid moves, stop and use that score
        elif len(moves[i].validmoves(-player)) == 0:
            moves[i] = (value, moves[i])
        # Otherwise get all of opponent's countermoves
        else:
            # countermoves == allmoves[i](-player)
            # print countermoves

            # get a list of all counter moves
            countermoves = moves[i].allmoves(-player)
            if times == -player:
                cons = 1
                # cons - player+times

            # Score them....
            for j in range(len(countermoves)):
                # First, get the score of current opponent's move
                countervalue = countermoves[j].score(player, heuristic)

                # If that move ends game, stop and use that score
                if countermoves[j].end():
                    countermoves[j] = (countervalue, countermoves[j])
                # OR if our opponent has no more valid moves, stop and use that score
                elif len(countermoves[j].validmoves(player)) == 0:
                    countermoves[j] = (countervalue, countermoves[j])

                # OR if we've gone down all the depths in our scope (n_depth = 0), use that score
                elif n_depth == 0 or n_depth_O < 0:
                    countermoves[j] = (countervalue, countermoves[j])

                # Otherwise, do recursive call to MiniMax with countermoves[j], with n_depth-1 and top being False
                else:
                    # Store new returned value in a variable
                    countervalue = minimax_n(countermoves[j], player, n_depth - 1, top=False, seen_list=seen_list,
                                             heuristic=heuristic)  # **?
                    # countervalue = minimax_n(countermoves[j], player, n_depth - 1, top=False)

                times += 1
                checked = True
                # Then move that score to the front to be able to sort
                countermoves[j] = (countervalue, countermoves[j])

            # Sort it with minimal values at the top
            countermoves.sort(reverse=False, key=lambda x: x[0])

            # Get the worst one (top at [0][0]
            worst_score = countermoves[0][0]

            # Now evaluate given worst_score
            moves[i] = (worst_score, moves[i])

    # Sort again, this time with biggest values up top
    moves.sort(reverse=True, key=lambda x: x[0])

    # If not at top level, return first move board
    if not top:
        # check moves
        # return worst_score(moves)
        # while n_depth >0:
            #return moves[0][n_depth]
        return moves[0][0]

    # Choose a randomly picked board from moves
    chosen_move = pickone(moves)[cons]
    # return chosen board
    return chosen_move


# Takes a sorted list of board and picks one randomly
def pickone(moves):  # Same function as in Tic-Tac-Toe
    # Get sublist for all moves that are best
    index = 0
    # Extract the score from the score,board, tuple
    topscore = moves[0][0]
    while index < len(moves) and moves[index][0] == topscore:  # checking all equal moves
        index = index + 1
    # Moves now contains only best moves
    moves = moves[:index]
    # Picks one randmomly
    move = moves[random.randrange(0, len(moves))]
    #print(moves[0][0])
    #print("Move made at:    (" + str(moves[0][0]) + ", " + str(moves[0][1]) + ")")
    print()
    return move


# Linking the selected Mode chosen to a string for displaying
def mode_to_string(
        mode):  # 'Switch' in Python   -  https://jaxenter.com/implement-switch-case-statement-python-138315.html
    switcher = {
        0: "Greedy Mode",
        1: "Minimax Mode (Depth 1)",
        2: "Minimax Mode (Depth 2)",
        3: "Minimax Mode (Depth 3)",
        4: "Minimax Mode (Depth 4)",
        5: "Minimax Mode (Depth 5)",
    }
    return switcher.get(mode, "Invalid mode")


# --------------------------------------------------------------------- #
# ------------------------- Main Function ----------------------------- #
# --------------------------------------------------------------------- #
def game():
    # Setting some variables
    global n_depth_X, n_depth_O
    global heuristic_X, heuristic_O
    global seenlist_X_bool, seenlist_O_bool

    # make the starting board
    board = Board()
    # start with Player 1 (X)
    turn = 1
    turn_overall = 1

    print("\nWelcome to two computers playing Othello against each other!\n")

    # Game Settings for Player 'X'
    master_mode_X = game_settings(turn)
    n_depth_X = master_mode_X[1]
    heuristic_X = master_mode_X[2]
    seenlist_X_bool = master_mode_X[3]

    print()

    # Game Settings for Player 'O'
    master_mode_O = game_settings(-turn)
    n_depth_O = master_mode_O[1]
    heuristic_O = master_mode_O[2]
    seenlist_O_bool = master_mode_O[3]

    # Formatting
    print()
    print()
    print("~~~~~ Starting Game ~~~~~")
    print("Turn: Initial Board")
    # Printing out starting board
    board.printboard()

    # Setting start-point for calculating total game execution time
    tic_final = time.perf_counter()  # https://realpython.com/python-timer/

    # Converting the Mode int identifier to the respective name (for both players)
    mode_string_X = mode_to_string(n_depth_X)
    mode_string_O = mode_to_string(n_depth_O)

    # Starting main loop -------V
    while not board.end():
        # Get the moves for whomever's turn it is
        movelist = board.validmoves(turn)
        # If no moves, skip the turn
        if len(movelist) == 0:
            turn = -turn
            continue

        # pick a move totally at random
        # i = random.randint(0, len(movelist) - 1)
        # make a new board
        #  board = board.copy()
        # make the move
        # board.place(movelist[i][0], movelist[i][1], turn)
        # swap players

        # If it's Player X's move (1)
        if turn == 1:
            print()
            print("=-")
            print("=-=-")
            print(
                "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            if n_depth_X > 0:
                print("  TURN: " + str(
                    turn_overall) + "                               >>>   PLAYER X's TURN:   <<<                                            <" + mode_string_X + ">")
            else:
                print("  TURN: " + str(
                    turn_overall) + "                               >>>   PLAYER X's TURN:   <<<                                            <" + mode_string_X + ">")
            print(
                "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(" X's current valid moves:     " + str(movelist))
            print("'X' is thinking . . . ")
            print()
            # Set start time for current move execution time
            tic = time.perf_counter()


        # If not, must be Player 'O's turn
        else:
            print(
                "                                                                                                                                -=")
            print(
                "                                                                                                                              -=-=")
            print(
                "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            if n_depth_O > 0:
                print("  TURN: " + str(
                    turn_overall) + "                               >>>   PLAYER O's TURN:   <<<                                            <" + mode_string_O + ">")
            else:
                print("  TURN: " + str(
                    turn_overall) + "                               >>>   PLAYER O's TURN:   <<<                                            <" + mode_string_O + ">")
            print(
                "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(" O's current valid moves:     " + str(movelist))
            print("'O' is thinking . . . ")
            print()
            # Set start time for current move execution time
            tic = time.perf_counter()

        # If it's Player X's turn
        if turn == 1:

            # If Greedy...
            if n_depth_X == 0:
                board = greedy(board, turn, heuristic_X)

            # if master_mode_X == 1:
            # board = minimax_1(board, turn)

            # If not Greedy
            if n_depth_X > 0:
                board = minimax_n(board, turn, n_depth_X, top=True, seen_list={}, heuristic=heuristic_X)

        # If it's Player O's turn
        else:

            # If Greedy
            if n_depth_O == 0:
                board = greedy(board, turn, heuristic_O)

            # if master_mode_O == 1:
            # board = minimax_1(board, turn)

            # If not Greedy
            if n_depth_O > 0:
                board = minimax_n(board, turn, n_depth_O, top=True, seen_list={}, heuristic=heuristic_O)

        # Print board after move
        board.printboard()
        # Set end marker for time taken to calculate/execute move
        toc = time.perf_counter()
        # Display score so far
        print()
        print("Current score:     X's: ", board.evaluate_pieces()[0], "   |    O's: ", board.evaluate_pieces()[1])
        if turn_overall < 96:
            if board.evaluate_pieces()[0] > board.evaluate_pieces()[1]:
                print("Player 'X' is in the lead")
            else:
                print("Player 'O' is in the lead")
        print(f"Move calculated in: {toc - tic:0.5f} seconds")  # https://realpython.com/python-timer/
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print()

        # swap players
        turn = -turn
        turn_overall += 1

        # wait for user to press a key
        # input()
        # game over? stop.
        if board.end():
            break
    # Set end marker for end of program to calculate time taken to run full game
    toc_final = time.perf_counter()
    # Display some final results  (Score and total time taken)
    print()
    print("--------------------------------------------------------------------")
    print("|  FINAL SCORE:       X's: ", board.evaluate_pieces()[0], "   |    O's: ", board.evaluate_pieces()[1],
          "                   |")
    if board.evaluate_pieces()[0] > board.evaluate_pieces()[1]:
        print("|  PLAYER 'X' WINS!                                                |")
    elif board.evaluate_pieces()[0] == board.evaluate_pieces()[1]:
        print("|  IT'S A TIE!                                                     |")
    else:
        print("|  PLAYER 'O' WINS!                                                |")
    print(f"|  Total game time elapsed since game start:  {toc_final - tic_final:0.5f} seconds.     |")
    print("--------------------------------------------------------------------")

    print()
    print("---- SETTINGS for PLAYER 'X' : -----------------------/")
    print("|  Mode:  <" + mode_string_X + ">")
    if n_depth_X > 0:
        print("|  Seen-list: " + str(seenlist_X_bool))
    else:
        print("|  Seen-list:  N/A")
    print("|  Heuristics: " + str(heuristic_X))
    print("---------------------------------------------/")

    print()

    print("---- SETTINGS for PLAYER 'O' : -------------------\\")
    print("|  Mode:  <" + mode_string_O + ">")
    if n_depth_O > 0:
        print("|  Seen-list: " + str(seenlist_O_bool))
    else:
        print("|  Seen-list:  N/A")
    print("|  Heuristics: " + str(heuristic_O))
    print("-------------------------------------------------\\")


game()
