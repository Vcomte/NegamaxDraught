from Position import Position
from Negamax import get_best_move


def determine_winner(pos):
    if pos.w_pawns == [] and pos.w_kings == []:
        return [False, "black"]
    if pos.b_pawns == [] and pos.b_kings == []:
        return [False, "white"]
    else:
        return [True, ""]

def main():
    print "Welcome to this game of draught"
    pos = Position()
    winner = determine_winner(pos)
    choice = input("If you wish to play against yourself enter 1, if you wish " \
          "to play against an AI, please enter 2")
    if(choice == 1):
        while winner[0]:
            pos.print_position()
            positions = pos.generate_positions()
            validate = False
            move = ""
            while not validate:
                print "Opponent just played: {}".format(pos.message)
                move = input("Enter your move for this turn (as a string please):")
                if move in positions.keys():
                    validate = True
                else:
                    print "Wrong input"
            pos = positions[move]
            winner = determine_winner(pos)
    elif(choice == 2):
        print "you will now play as the white player"
        while winner[0]:
            pos.print_position()
            positions = pos.generate_positions()
            validate = False
            move = ""
            if pos.turn == "white":
                while not validate:
                    print "Opponent just played: {}".format(pos.message)
                    move = input("Enter your move for this turn (as a string please: position + direction e.g. se for south east):")
                    if move in positions.keys():
                        validate = True
                    else:
                        print "Wrong input"
            else:
                move = get_best_move(pos, 2)
            pos = positions[move]
            winner = determine_winner(pos)
    else:
        while winner[0]:
            pos.print_position()
            positions = pos.generate_positions()
            validate = False
            move = ""
            if pos.turn == "white":
                move = get_best_move(pos, 2)
                "White has played : {}".format(move)
            else:
                move = get_best_move(pos, 2)
                "Black has played : {}".format(move)
            pos = positions[move]
            winner = determine_winner(pos)
    print "The winner is: {} player".format(winner[1])


if __name__ == '__main__':
    main()
