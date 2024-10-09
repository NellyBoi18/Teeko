import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state):
        succ = list()

        for row in range(5):
            for col in range(5):
                if(state[row][col] == ' '):
                    succ.append((row,col))

        random.shuffle(succ) # CHECKKKKdhaf;anvraovn;ajnf;afeafdafaweo;nckj4boab[cj;ADFADSFNA;DSKFNAFEACN;AORNF]

        return succ

    def detectDropPhase(self, state):
        count = 0

        for row in state:
            count += row.count('b') + row.count('r')
            # print(count)
        
        if (count >= 8):
            return False

        return True

    """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
    """
    def make_move(self, state):
        drop_phase = self.detectDropPhase(state)

        if not drop_phase:
            succsNOT = self.succMove(state, self.my_piece)
            maxiNOT = -1234567890
            miniNOT = 1234567890
            nextMoveNOT = [(0, 0), (0, 0)]
            
            for succNOT in succsNOT:
                tempStateNOT = copy.deepcopy(state)
                tempStateNOT[succNOT[0][0]][succNOT[0][1]] = self.my_piece
                tempStateNOT[succNOT[1][0]][succNOT[1][1]] = ' '
                succValueNOT = self.min_value(tempStateNOT, 0, maxiNOT, miniNOT)
                # print(succValueNOT)

                if (maxiNOT < succValueNOT):
                    nextMoveNOT = succNOT
                    maxiNOT = succValueNOT
                    # print(maxiNOT)
                    # print(miniNOT)
                    
            moveNOT = nextMoveNOT
            # print("moveNOT: ", moveNOT)
            return moveNOT

        move = []
        succs = self.succ(state)
        maxi = -1234567890
        mini = 1234567890
        nextMove = [0, 0]

        for succ in succs:
            row = succ[0]
            col = succ[1]
            tempState = copy.deepcopy(state)
            tempState[row][col] = self.my_piece
            succValue = self.min_value(tempState, 0, maxi, mini)
            
            if (maxi <= succValue):
                nextMove = [row, col]
                maxi = succValue
                # print(maxi)

        move.insert(0, nextMove)
        # print(move)

        # print(type(move))
        # print(len(move))
        # print(type(move))
        # print("move: ", move)
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner
    """
    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # Check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if ((state[row][col] != ' ') and (state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3])):
                    return 1 if state[row][col] == self.my_piece else -1

        # Check / diagonal wins
        for row in range(2):
            for col in range(3, 5):
                if ((state[row][col] != ' ') and (state[row][col] == state[row + 1][col - 1] == state[row + 2][col - 2] == state[row + 3][col - 3])):
                    return 1 if state[row][col] == self.my_piece else -1

        # Check 2x2 wins
        for row in range(4):
            for col in range(4):
                if ((state[row][col] != ' ') and (state[row + 1][col] != ' ') and ((state[row + 1][col]) == (state[row][col]) == (state[row][col + 1]) == (state[row + 1][col + 1]))):
                    return 1 if state[row][col] == self.my_piece else -1
        
        return 0  # no winner yet

    def heuristic_game_value(self, state):
        gameValue = self.game_value(state)

        if (gameValue != 0 ):
            return gameValue

        minValue = 2    
        maxValue = -2

        # Horizontal
        for row in state:
            for col in range(2):
                temp = list()

                for x in range(4):
                    temp.append(row[col + x]) #CHECKKKKKKKKKKKKKKKKKKKA;ODFNAO;NFJOAENVJAERNRO NAD[OVMANIO[NFDJQOJI0JVOIA[NVI[N]]]]

                    tempOppCount = temp.count(self.opp) * (0.2) * (-1)
                    tempMyPieceCount = temp.count(self.my_piece) * (0.2)

                    minValue = min(minValue, tempOppCount)
                    maxValue = max(maxValue, tempMyPieceCount)

        # Vertical
        for col in range(5):
            for row in range(2):
                temp = list()

                for x in range(4):
                    temp.append(state[row + x][col])

                    tempOppCount = temp.count(self.opp) * (0.2) * (-1)
                    tempMyPieceCount = temp.count(self.my_piece) * (0.2)
                    
                    minValue = min(minValue, tempOppCount)
                    maxValue = max(maxValue, tempMyPieceCount)

        # \ Diagonal
        for row in range(2):
            for col in range(2):
                temp = list()

                for x in range(4):
                    if ((col + x < 5) and (row + x < 5)):
                        temp.append(state[row + x][col + x])

                        tempOppCount = temp.count(self.opp) * (0.2) * (-1)
                        tempMyPieceCount = temp.count(self.my_piece) * (0.2)
                        
                        minValue = min(minValue, tempOppCount)
                        maxValue = max(maxValue, tempMyPieceCount)

        # / Diagonal
        for row in range(2):
            for col in range(3, 5):
                temp = list()

                for x in range(4):
                    if ((col - x >= 0) and (row + x < 5)):
                        temp.append(state[row + x][col - x])

                        tempOppCount = temp.count(self.opp) * (0.2) * (-1)
                        tempMyPieceCount = temp.count(self.my_piece) * (0.2)
                        
                        minValue = min(minValue, tempOppCount)
                        maxValue = max(maxValue, tempMyPieceCount)

        # 2x2
        for row in range(1, 4):
            for col in range(1, 4):
                temp = list()
                temp.append(state[row + 1][col])
                temp.append(state[row][col + 1])
                temp.append(state[row - 1][col])
                temp.append(state[row][col - 1])

                tempOppCount = temp.count(self.opp) * (0.2) * (-1)
                tempMyPieceCount = temp.count(self.my_piece) * (0.2)
                
                minValue = min(minValue, tempOppCount)
                maxValue = max(maxValue, tempMyPieceCount)

        heuristic = maxValue + minValue
        # print(heuristic)
        return heuristic

    def succMove(self, state, currentPiece):
        moveRow = [-1, 0, 1]
        moveCol = [-1, 0, 1]
        succs = list()

        for row in range(5):
            for col in range(5):

                if (state[row][col] == currentPiece):
                    for rowMove in moveRow:
                        for colMove in moveCol:

                            if ((row + rowMove < 5) and (row + rowMove >= 0) and (col + colMove < 5) and (col + colMove >= 0) and (state[row + rowMove][col + colMove] == ' ')):
                                succs.append([(row + rowMove, col + colMove), (row, col)])
                                
        random.shuffle(succs)

        return succs

    def max_value(self, state, depth, maxi, mini):
        # Check
        gameValue = self.game_value(state)
        
        if (gameValue == 0):
            if (depth < 2):
                # print(depth)

                # Check drop phase
                if (self.detectDropPhase(state)):
                    succs = self.succ(state)

                    for row, col in succs:
                        tempState = copy.deepcopy(state)
                        tempState[row][col] = self.my_piece
                        maxi = max(maxi, self.min_value(tempState, depth + 1, maxi, mini))
                else:
                    succs = self.succMove(state, self.my_piece)

                    for succ in succs:
                        tempState = copy.deepcopy(state)
                        tempState[succ[0][0]][succ[0][1]] = self.my_piece
                        tempState[succ[1][0]][succ[1][1]] = ' '
                        maxi = max(maxi, self.min_value(tempState, depth + 1, maxi, mini))

                return maxi

            else: 
                # print("MAX VALUE DEPTH LIMIT")
                return self.heuristic_game_value(state)

        else: 
            return gameValue

    def min_value(self, state, depth, maxi, mini):
        gameValue = self.game_value(state)

        if (gameValue == 0):
            # print(gameValue)
            if (depth < 2):
                # print("MIN:", depth)
                
                # Drop Phase
                if (self.detectDropPhase(state)):
                    # print("MIN VALUE DROP PHASE")
                    succs = self.succ(state)

                    for row, col in succs:
                        tempState = copy.deepcopy(state)
                        tempState[row][col] = self.opp
                        mini = min(mini, self.max_value(tempState, depth + 1, maxi, mini))
                else:
                    succs = self.succMove(state, self.opp)

                    for succ in succs:
                        tempState = copy.deepcopy(state)
                        tempState[succ[0][0]][succ[0][1]] = self.opp
                        tempState[succ[1][0]][succ[1][1]] = ' '
                        mini = min(mini, self.max_value(tempState, depth + 1, maxi, mini))
                
                return mini

            else: 
                # print("MIN VALUE DEPTH LIMIT")
                return self.heuristic_game_value(state)

        else:
            return gameValue


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
