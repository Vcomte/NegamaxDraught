import sys
from Utils import *
from copy import copy


class Position:

    def __init__(self, zob=0, huffables=[], turn="white",
                 w_pawns=ini_w_p, b_pawns=ini_b_p,
                 w_kings=[], b_kings=[], message=""):
        self.huffables = huffables
        self.turn = turn
        self.w_pawns = w_pawns
        self.b_pawns = b_pawns
        self.w_kings = w_kings
        self.b_kings = b_kings
        self.zob = zob
        self.generated_huffables = []
        self.message = message
        self.evaluation = 0

    def generate_positions(self):
        positions = {}
        if self.turn == "white":
            for pawn in self.w_pawns:
                positions.update(self.generate_w_pawn_pos(pawn))
            for king in self.w_kings:
                positions.update(self.generate_w_king_pos(king))
        else:
            for pawn in self.b_pawns:
                positions.update(self.generate_b_pawn_pos(pawn))
            for king in self.b_kings:
                positions.update(self.generate_b_king_pos(king))
        return positions

    def generate_w_pawn_pos(self, loc, only_eat=False):
        new_positions = {}
        #Checking eat right then left
        for decal in [0, 2]:
            if only_eat:
                mov = self.message+" "
            else:
                mov = ""
            if(decal == 0):
                mov += "se"
            else:
                mov += "sw"
            if(loc[0]+2 < 11 and loc[1]-decal > -1):
                if(possibles_locations[loc[0]+2][loc[1]-decal] == 1 and possibles_locations[loc[0]+1][loc[1]-(decal/2)] == 1):
                    if([loc[0]+2, loc[1]-decal] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                        #Eating a b pawn
                        if([loc[0]+1, loc[1]-(decal/2)] in self.b_pawns):
                            n_b_pawns = copy(self.b_pawns)
                            n_b_pawns.remove([loc[0]+1, loc[1]-(decal/2)])
                            n_w_pawns = copy(self.w_pawns)
                            n_w_pawns.remove([loc[0], loc[1]])
                            n_w_pawns.append([loc[0]+2, loc[1]-decal])
                            if not only_eat:
                                mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            pos = Position(turn="black",w_pawns=n_w_pawns, b_pawns=n_b_pawns, b_kings=copy(self.b_kings),
                                           w_kings=copy(self.w_kings), message=mov)
                            pos.check_new_kings()
                            new_positions[mov] = pos
                            if loc[0]+2 == 9:
                                new_positions.update(pos.generate_w_king_pos([loc[0]+2, loc[1]-decal], True))
                            else:
                                new_positions.update(pos.generate_w_pawn_pos([loc[0]+2, loc[1]-decal], True))
                            if not only_eat:
                                self.generated_huffables.append([loc[0], loc[1]])
                        #Eating a b king
                        if([loc[0]+1, loc[1]-(decal/2)] in self.b_kings):
                            n_b_kings = copy(self.b_kings)
                            n_b_kings.remove([loc[0]+1, loc[1]-(decal/2)])
                            n_w_pawns = copy(self.w_pawns)
                            n_w_pawns.remove([loc[0], loc[1]])
                            n_w_pawns.append([loc[0]+2, loc[1]-decal])
                            if not only_eat:
                                mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            pos = Position(turn="black",w_pawns=n_w_pawns, b_kings=n_b_kings, b_pawns=copy(self.b_pawns),
                                           w_kings=copy(self.w_kings), message=mov)
                            pos.check_new_kings()
                            new_positions[mov] = pos
                            if loc[0]+2 == 9:
                                new_positions.update(pos.generate_w_king_pos([loc[0]+2, loc[1]-decal], True))
                            else:
                                new_positions.update(pos.generate_w_pawn_pos([loc[0]+2, loc[1]-decal], True))
                            if not only_eat:
                                self.generated_huffables.append([loc[0], loc[1]])

        #Checking simple move
        if not only_eat:
            for decal in [0, 1]:
                mov = ""
                if(decal == 0):
                    mov += "se"
                else:
                    mov += "sw"
                if(possibles_locations[loc[0]+1][loc[1]-decal] == 1):
                    if([loc[0]+1, loc[1]-decal] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                        n_w_pawns = copy(self.w_pawns)
                        n_w_pawns.remove([loc[0], loc[1]])
                        n_w_pawns.append([loc[0]+1, loc[1]-decal])
                        mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                        pos = Position(turn="black",w_pawns=n_w_pawns, b_pawns=copy(self.b_pawns),
                                       b_kings=copy(self.b_kings),w_kings=copy(self.w_kings), message=mov)
                        pos.check_new_kings()
                        new_positions[mov] = pos

        return new_positions


    def generate_b_pawn_pos(self, loc, only_eat=False):
        new_positions = {}
        #Checking eat left then right
        for decal in [0, 2]:
            if only_eat:
                mov = self.message+" "
            else:
                mov = ""
            if(decal == 0):
                mov += "nw"
            else:
                mov += "ne"
            if loc[0]-2 > -1 and loc[1]+decal < 11:
                if(possibles_locations[loc[0]-2][loc[1]+decal] == 1 and possibles_locations[loc[0]-1][loc[1]+(decal/2)] == 1):
                    if([loc[0]-2, loc[1]+decal] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                        #Eating a w pawn
                        if([loc[0]-1, loc[1]+(decal/2)] in self.w_pawns):
                            n_w_pawns = copy(self.w_pawns)
                            n_w_pawns.remove([loc[0]-1, loc[1]+(decal/2)])
                            n_b_pawns = copy(self.b_pawns)
                            n_b_pawns.remove([loc[0], loc[1]])
                            n_b_pawns.append([loc[0]-2, loc[1]+decal])
                            if not only_eat:
                                mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            pos = Position(turn="white",w_pawns=n_w_pawns, b_pawns=n_b_pawns, w_kings=copy(self.w_kings),
                                           b_kings=copy(self.b_kings), message=mov)
                            pos.check_new_kings()
                            new_positions[mov] = pos
                            if loc[0]-2 == 1:
                                new_positions.update(pos.generate_b_king_pos([loc[0]-2, loc[1]+decal], True))
                            else:
                                new_positions.update(pos.generate_b_pawn_pos([loc[0]-2, loc[1]+decal], True))
                            if not only_eat:
                                self.generated_huffables.append([loc[0], loc[1]])
                        #Eating a w king
                        if([loc[0]-1, loc[1]+(decal/2)] in self.w_kings):
                            n_w_kings = copy(self.w_kings)
                            n_w_kings.remove([loc[0]-1, loc[1]+(decal/2)])
                            n_b_pawns = copy(self.b_pawns)
                            n_b_pawns.remove([loc[0], loc[1]])
                            n_b_pawns.append([loc[0]-2, loc[1]+decal])
                            if not only_eat:
                                mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            pos = Position(turn="white",w_kings=n_w_kings, b_pawns=n_b_pawns, w_pawns=copy(self.w_pawns),
                                           b_kings=copy(self.b_kings), message=mov)
                            new_positions[mov] = pos
                            pos.check_new_kings()
                            if loc[0]+2 == 1:
                                new_positions.update(pos.generate_b_king_pos([loc[0]-2, loc[1]+decal], True))
                            else:
                                new_positions.update(pos.generate_b_pawn_pos([loc[0]-2, loc[1]+decal], True))
                            if not only_eat:
                                self.generated_huffables.append([loc[0], loc[1]])
        #Checking simple move
        if not only_eat:
            for decal in [0, 1]:
                mov = ""
                if(decal == 0):
                    mov += "nw"
                else:
                    mov += "ne"
                if(possibles_locations[loc[0]-1][loc[1]+decal] == 1):
                    if([loc[0]-1, loc[1]+decal] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                        n_b_pawns = copy(self.b_pawns)
                        n_b_pawns.remove([loc[0], loc[1]])
                        n_b_pawns.append([loc[0]-1, loc[1]+decal])
                        mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                        pos = Position(turn="white",b_pawns=n_b_pawns, w_pawns=copy(self.w_pawns),
                                       w_kings=copy(self.w_kings), b_kings=copy(self.b_kings), message=mov)
                        pos.check_new_kings()
                        new_positions[mov] = pos


        return new_positions

    def generate_w_king_pos(self, loc, only_eat=False):
        new_positions = {}
        #Checking eat right then left
        for hori in [0, 2]:
            for vert in [1, -1]:
                if only_eat:
                    mov = self.message+" "
                else:
                    mov = ""
                if(hori == 0 and vert == 1):
                    mov += "se"
                elif(hori == 0 and vert == -1):
                    mov += "nw"
                elif(hori == 2 and vert == 1):
                    mov += "sw"
                else:
                    mov += "ne"
                if loc[0]+2*vert < 11 and loc[0]-2*vert >-1 and loc[1]-2*vert > -1 and loc[1]+2*vert < 11:
                    if(possibles_locations[loc[0]+2*vert][loc[1]-hori*vert] == 1 and
                               possibles_locations[loc[0]+1*vert][loc[1]-(hori/2)*vert] == 1):
                        if([loc[0]+2*vert, loc[1]-hori*vert] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                            #Eating a b pawn
                            if([loc[0]+1*vert, loc[1]-(hori/2)*vert] in self.b_pawns):
                                n_b_pawns = copy(self.b_pawns)
                                n_b_pawns.remove([loc[0]+1*vert, loc[1]-(hori/2)*vert])
                                n_w_kings = copy(self.w_kings)
                                n_w_kings.remove([loc[0], loc[1]])
                                n_w_kings.append([loc[0]+2*vert, loc[1]-hori*vert])
                                if not only_eat:
                                    mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                                pos = Position(turn="black",w_kings=n_w_kings, b_pawns=n_b_pawns, b_kings=copy(self.b_kings),
                                               w_pawns=copy(self.w_pawns), message=mov)
                                new_positions[mov] = pos
                                new_positions.update(pos.generate_w_king_pos([loc[0]+2*vert, loc[1]-hori*vert], True))
                                if not only_eat:
                                    self.generated_huffables.append([loc[0], loc[1]])
                            #Eating a b king
                            if([loc[0]+1*vert, loc[1]-(hori/2)*vert] in self.b_kings):
                                n_b_kings = copy(self.b_kings)
                                n_b_kings.remove([loc[0]+1*vert, loc[1]-(hori/2)*vert])
                                n_w_kings = copy(self.w_kings)
                                n_w_kings.remove([loc[0], loc[1]])
                                n_w_kings.append([loc[0]+2*vert, loc[1]-hori*vert])
                                if not only_eat:
                                    mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                                pos = Position(turn="black",w_kings=n_w_kings, b_kings=n_b_kings, w_pawns=copy(self.w_pawns),
                                               b_pawns=copy(self.b_pawns), message=mov)
                                new_positions[mov] = pos
                                new_positions.update(pos.generate_w_king_pos([loc[0]+2*vert, loc[1]-hori*vert], True))
                                if not only_eat:
                                    self.generated_huffables.append([loc[0], loc[1]])
        #Checking simple move
        if not only_eat:
            for hori in [0, 1]:
                for vert in [1, -1]:
                    mov = ""
                    if(hori == 0 and vert == 1):
                        mov += "se"
                    elif(hori == 0 and vert == -1):
                        mov += "nw"
                    elif(hori == 1 and vert == 1):
                        mov += "sw"
                    else:
                        mov += "ne"
                    if(possibles_locations[loc[0]+1*vert][loc[1]-hori*vert] == 1):
                        if([loc[0]+1*vert, loc[1]-hori*vert] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                            n_w_kings = copy(self.w_kings)
                            n_w_kings.remove([loc[0], loc[1]])
                            n_w_kings.append([loc[0]+1*vert, loc[1]-hori*vert])
                            mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            new_positions[mov] = Position(turn="black",w_kings=n_w_kings, b_kings=copy(self.b_kings),
                                                          w_pawns=copy(self.w_pawns), b_pawns=copy(self.b_pawns),
                                                          message=mov)

        return new_positions

    def generate_b_king_pos(self, loc, only_eat=False):
        new_positions = {}
        #Checking eat right then left
        for hori in [0, 2]:
            for vert in [1, -1]:
                if only_eat:
                    mov = self.message+" "
                else:
                    mov = ""
                if(hori == 0 and vert == 1):
                    mov += "nw"
                elif(hori == 0 and vert == -1):
                    mov += "se"
                elif(hori == 2 and vert == 1):
                    mov += "ne"
                else:
                    mov += "sw"
                if loc[0]+2*vert < 11 and loc[0]-2*vert >-1 and loc[1]-2*vert > -1 and loc[1]+2*vert < 11:
                    if(possibles_locations[loc[0]-2*vert][loc[1]+hori*vert] == 1 and
                               possibles_locations[loc[0]-1*vert][loc[1]+(hori/2)*vert] == 1):
                        if([loc[0]-2*vert, loc[1]+hori*vert] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                            #Eating a w pawn
                            if([loc[0]-1*vert, loc[1]+(hori/2)*vert] in self.w_pawns):
                                n_w_pawns = copy(self.w_pawns)
                                n_w_pawns.remove([loc[0]-1*vert, loc[1]+(hori/2)*vert])
                                n_b_kings = copy(self.b_kings)
                                n_b_kings.remove([loc[0], loc[1]])
                                n_b_kings.append([loc[0]-2*vert, loc[1]+hori*vert])
                                if not only_eat:
                                    mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                                pos = Position(turn="white",w_pawns=n_w_pawns, b_kings=n_b_kings, b_pawns=copy(self.b_pawns),
                                               w_kings=copy(self.w_kings), message=mov)
                                new_positions[mov] = pos
                                new_positions.update(pos.generate_b_king_pos([loc[0]-2*vert, loc[1]+hori*vert], True))
                                if not only_eat:
                                    self.generated_huffables.append([loc[0], loc[1]])
                            #Eating a w king
                            if([loc[0]-1*vert, loc[1]+(hori/2)*vert] in self.w_kings):
                                n_w_kings = copy(self.w_kings)
                                n_w_kings.remove([loc[0]-1*vert, loc[1]+(hori/2)*vert])
                                n_b_kings = copy(self.b_kings)
                                n_b_kings.remove([loc[0], loc[1]])
                                n_b_kings.append([loc[0]-2*vert, loc[1]+hori*vert])
                                if not only_eat:
                                    mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                                pos = Position(turn="white",w_kings=n_w_kings, b_kings=n_b_kings, w_pawns=copy(self.w_pawns),
                                               b_pawns=copy(self.b_pawns), message=mov)
                                new_positions[mov] = pos
                                new_positions.update(pos.generate_b_king_pos([loc[0]-2*vert, loc[1]+hori*vert], True))
                                if not only_eat:
                                    self.generated_huffables.append([loc[0], loc[1]])
        #Checking simple move
        if not only_eat:
            for hori in [0, 1]:
                for vert in [1, -1]:
                    mov = ""
                    if(hori == 0 and vert == 1):
                        mov += "nw"
                    elif(hori == 0 and vert == -1):
                        mov += "se"
                    elif(hori == 2 and vert == 1):
                        mov += "ne"
                    else:
                        mov += "sw"
                    if(possibles_locations[loc[0]-1*vert][loc[1]+hori*vert] == 1):
                        if([loc[0]-1*vert, loc[1]+hori*vert] not in self.b_pawns+self.w_pawns+self.b_kings+self.w_kings):
                            n_b_kings = copy(self.b_kings)
                            n_b_kings.remove([loc[0], loc[1]])
                            n_b_kings.append([loc[0]-1*vert, loc[1]+hori*vert])
                            mov = str(corresp[loc[0]][loc[1]]) + " " + mov
                            new_positions[mov] = Position(turn="black",b_kings=n_b_kings, w_kings=copy(self.w_kings),
                                                          w_pawns=copy(self.w_pawns), b_pawns=copy(self.b_pawns),
                                                          message=mov)

        return new_positions

    def check_new_kings(self):
        for w_pawn in self.w_pawns:
            if w_pawn[0] == 9:
                self.w_pawns.remove(w_pawn)
                self.w_kings.append(w_pawn)
        for b_pawn in self.b_pawns:
            if b_pawn[0] == 1:
                self.b_pawns.remove(b_pawn)
                self.b_kings.append(b_pawn)

    def check_move_evaluation(self):
        if self.turn == "white":
            positions = {}
            for pawn in self.b_pawns:
                positions.update(self.generate_b_pawn_pos(pawn))
            for king in self.b_kings:
                positions.update(self.generate_b_king_pos(king))
            return len(positions.keys())
        if self.turn == "black":
            positions = {}
            for pawn in self.w_pawns:
                positions.update(self.generate_w_pawn_pos(pawn))
            for king in self.w_kings:
                positions.update(self.generate_w_king_pos(king))
            return len(positions.keys())

    # Here we consider the value for the previous player, not the current
    # because we will always evaluate future positions
    # The returned score is based on the number of possible moves and the possibility of capture
    # Capturing a king is more valued than capturing a pawn
    # The 4 first parameters are the numbers of kings/pawns for each player in the previous position
    # The last parameter is used to determine if the evaluation should continue on next positions or not
    def evaluate(self, no_w_p, no_w_k, no_b_p, no_b_k, opponent=True):
        # Checking if moves available for opponent
        positions = self.generate_positions()
        if len(positions.keys()) == 0:
            return 1000
        # Checking if moves are available for player if not returning bad value, else returning a score
        score = self.check_move_evaluation()
        if score == 0:
            return -1000
        if self.turn == "white":
            score += (no_w_k-len(self.w_kings))*10
            score += (no_w_p-len(self.w_pawns))*5
            score += (len(self.b_kings)-no_b_k)*5
        else:
            score += (no_b_k-len(self.b_kings))*10
            score += (no_b_p-len(self.b_pawns))*5
            score += (len(self.w_kings)-no_w_k)*5
        # Creating average evaluation for opponent's moves
        oppo = 0
        if opponent:
            for pos in positions:
                oppo += positions[pos].evaluate(len(self.w_pawns), len(self.w_kings),
                                                len(self.b_pawns), len(self.b_kings), False)
            oppo = oppo / len(positions.keys())
        return score - oppo

    def print_position(self):
        board = [[0, 0, 0, 0, 0, 1, 3, 3, 3, 2],
                 [0, 0, 0, 0, 5, 7, 7, 7, 7, 2],
                 [0, 0, 0, 5, 7, 7, 7, 7, 7, 2],
                 [0, 0, 5, 7, 7, 7, 7, 7, 7, 2],
                 [0, 5, 7, 7, 7, 7, 7, 7, 7, 2],
                 [4, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                 [4, 7, 7, 7, 7, 7, 7, 7, 0, 0],
                 [4, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                 [4, 7, 7, 7, 7, 7, 0, 0, 0, 0],
                 [4, 7, 7, 7, 7, 0, 0, 0, 0, 0]]

        for pos in self.w_pawns:
            board[pos[0]][pos[1]] = 8
        for pos in self.w_kings:
            board[pos[0]][pos[1]] = 9
        for pos in self.b_pawns:
            board[pos[0]][pos[1]] = 10
        for pos in self.b_kings:
            board[pos[0]][pos[1]] = 11
        seq = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
        level = 0
        indent = ''
        for line in board:
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
        sys.stdout.write("\n\t\tIt is {}'s turn to play\n".format(self.turn))
