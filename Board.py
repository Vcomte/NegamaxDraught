import sys


class Board:

    def __init__(self, board="", positions=""):
        self.current_player = "white"
        self.message = "It is {}'s turn to play".format(self.current_player)

        if (board != ""):
            self.board = board
        else:
            self.board = [[0, 0, 0, 0, 0, 1, 3, 3, 3, 2],
                          [0, 0, 0, 0, 5, 8, 8, 8, 8, 2],
                          [0, 0, 0, 5, 8, 8, 7, 8, 8, 2],
                          [0, 0, 5, 8, 7, 8, 8, 7, 8, 2],
                          [0, 5, 7, 7, 7, 7, 7, 7, 7, 2],
                          [4, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                          [4, 7, 7, 7, 7, 7, 7, 7, 0, 0],
                          [4, 10, 7, 10, 10, 7, 10, 0, 0, 0],
                          [4, 10, 10, 7, 10, 10, 0, 0, 0, 0],
                          [4, 10, 10, 10, 10, 0, 0, 0, 0, 0]]

        if (positions != ""):
            self.positions = positions
        else:
            self.positions = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 8, 8, 8, 8, 0],
                              [0, 0, 0, 0, 8, 8, 1, 8, 8, 0],
                              [0, 0, 0, 8, 1, 8, 8, 1, 8, 0],
                              [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                              [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                              [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                              [0, 10, 1, 10, 10, 1, 10, 0, 0, 0],
                              [0, 10, 10, 1, 10, 10, 0, 0, 0, 0],
                              [0, 10, 10, 10, 10, 0, 0, 0, 0, 0]]

    def move(self, initial_position, target_position):
        self.positions[target_position[0]][target_position[1]] = self.positions[initial_position[0]][initial_position[1]]
        self.positions[initial_position[0]][initial_position[0]] = 1
        self.board[target_position[0]][target_position[1]] = self.board[initial_position[0]][initial_position[1]]
        self.board[initial_position[0]][initial_position[0]] = 7

    def destroy(self, target_position):
        self.positions[target_position[0]][target_position[1]] = 1
        self.board[target_position[0]][target_position[1]] = 7

    def check_king(self, target_position):
        if (self.positions[target_position[0]][target_position[1]] == 8 and target_position[0] == 9):
            self.positions[target_position[0]][target_position[1]] == 9
        elif (self.positions[target_position[0]][target_position[1]] == 10 and target_position[0] == 1):
            self.positions[target_position[0]][target_position[1]] == 11


    # Will return 2 booleans, 1t telling if move is valid, 2nd telling if move has eaten
    def check_move(self, initial_position, target_position):
        # Checking if target is right
        if (self.positions[target_position[0]][target_position[1]] != 1):
            return [False, False]
        # Checking if pawn/king is of the good player and then checking if move is legal
        # WHITE
        if (self.current_player == "white"):
            # PAWN WHITE
            if (self.positions[initial_position[0]][initial_position[1]] == 8):
                # Checking if move is eating
                if (initial_position[0] - target_position[0] == 2):
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]+1][initial_position[1]] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    elif (initial_position[1] - target_position[1] == 2):
                        if(self.positions[initial_position[0]+1][initial_position[1] - 1] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1] - 1])
                            self.check_king(target_position)
                            return [True, True]
                # Checking simple move
                elif (initial_position[0] - target_position[0] == -1):
                    if (initial_position[1] == target_position[1] or initial_position[1] - target_position[1] == 1):
                        self.move(initial_position, target_position)
                        self.check_king(target_position)
                        return [True, False]
            # KING WHITE
            elif (self.positions[initial_position[0]][initial_position[1]] == 9):
                # checking if the move is eating
                # Botom
                if (initial_position[0] - target_position[0] == -2):
                    # Right
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]+1][initial_position[1]] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    # Left
                    elif (initial_position[1] - target_position[1] == 2):
                        if(self.positions[initial_position[0]+1][initial_position[1] - 1] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1] - 1])
                            self.check_king(target_position)
                            return [True, True]
                # Up
                elif (initial_position[0] - target_position[0] == 2):
                    # Left
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]-1][initial_position[1]] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    # Right
                    elif (initial_position[1] - target_position[1] == -2):
                        if(self.positions[initial_position[0]-1][initial_position[1] + 1] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1] + 1])
                            self.check_king(target_position)
                            return [True, True]
                # Checking simple move
                elif (initial_position[0] - target_position[0] == 1 or initial_position[0] - target_position[0] == -1):
                    if (initial_position[1] == target_position[1] or initial_position[1] - target_position[1] == 1):
                        self.move(initial_position, target_position)
                        self.check_king(target_position)
                        return [True, False]
        # BLACK
        elif (self.current_player == "black"):
            # PAWN BLACK
            if (self.positions[initial_position[0]][initial_position[1]] == 10):
                # Checking if move is eating
                if (initial_position[0] - target_position[0] == 2):
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]-1][initial_position[1]] in [8, 9]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    elif (initial_position[1] - target_position[1] == -2):
                        if(self.positions[initial_position[0]-1][initial_position[1] - 1] in [10, 11]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1] - 1])
                            self.check_king(target_position)
                            return [True, True]
                # Checking simple move
                elif (initial_position[0] - target_position[0] == 1):
                    if (initial_position[1] == target_position[1] or initial_position[1] - target_position[1] == -1):
                        self.move(initial_position, target_position)
                        self.check_king(target_position)
                        return [True, False]
            # KING WHITE
            elif (self.positions[initial_position[0]][initial_position[1]] == 11):
                # checking if the move is eating
                # Botom
                if (initial_position[0] - target_position[0] == -2):
                    # Right
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]+1][initial_position[1]] in [8, 9]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    # Left
                    elif (initial_position[1] - target_position[1] == 2):
                        if(self.positions[initial_position[0]+1][initial_position[1] - 1] in [8, 9]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]+1, initial_position[1] - 1])
                            self.check_king(target_position)
                            return [True, True]
                # Up
                elif (initial_position[0] - target_position[0] == 2):
                    # Left
                    if (initial_position[1] == target_position[1]):
                        if(self.positions[initial_position[0]-1][initial_position[1]] in [8, 9]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1]])
                            self.check_king(target_position)
                            return [True, True]
                    # Right
                    elif (initial_position[1] - target_position[1] == -2):
                        if(self.positions[initial_position[0]-1][initial_position[1] + 1] in [8, 9]):
                            self.move(initial_position, target_position)
                            self.destroy([initial_position[0]-1, initial_position[1] + 1])
                            self.check_king(target_position)
                            return [True, True]
                # Checking simple move
                elif (initial_position[0] - target_position[0] == 1 or initial_position[0] - target_position[0] == -1):
                    if (initial_position[1] == target_position[1] or initial_position[1] - target_position[1] == 1):
                        self.move(initial_position, target_position)
                        self.check_king(target_position)
                        return [True, False]
        return [False, False]

    def print_board(self):
        seq = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
        level = 0
        indent = ''
        for line in self.board:
            sys.stdout.write(seq[level])
            sys.stdout.write(indent)
            sys.stdout.write('  ')
            level += 1

            for cell in line:
                #print character or blank
                if cell == 8:
                    sys.stdout.write('o')
                elif cell == 9:
                    sys.stdout.write('O')
                elif cell == 10:
                    sys.stdout.write('x')
                elif cell == 11:
                    sys.stdout.write('X')
                else:
                    sys.stdout.write(' ')
                sys.stdout.write(' ')
                if(cell in [4, 5, 6, 7, 8, 9, 10, 11]):
                    sys.stdout.write('|')
                else:
                    sys.stdout.write(' ')
                sys.stdout.write(' ')
            sys.stdout.write('\n  ')
            sys.stdout.write(indent)

            for cell in line:
                if(cell in [2, 3, 6, 7, 8, 9, 10, 11]):
                    sys.stdout.write('\\')
                else:
                    sys.stdout.write(' ')
                sys.stdout.write(' ')
                if(cell in [1, 3, 5, 7, 8, 9, 10, 11]):
                    sys.stdout.write('/')
                else:
                    sys.stdout.write(' ')
                sys.stdout.write(' ')
            sys.stdout.write('\n')
            indent += '  '
        sys.stdout.write("\t\t ")
        sys.stdout.write("a b c d e f g h i j k l m n o")
        sys.stdout.write("\n\t\t{}\n".format(self.message))
