# -*- coding: utf-8 -*-

'''
@author: Valentin Comte
student_number: 15201982
'''

number_evaluation_ab = 0
total_evaluation_ab = 0


#def negamax(position, height, achievable, hope):
#    positions = position.generate_positions()
#    if height == 0 or len(positions.keys()) == 0:
#        return position.evaluate(len(position.w_pawns), len(position.w_kings), len(position.b_pawns),
#                                 len(position.b_kings))
#    else:
#        tmp = 0
#        for pos in positions:
#            tmp = -negamax(positions[pos], height-1, -hope, -achievable)
#            if tmp >= hope:
#                return tmp
#            achievable = max(tmp, achievable)
#    return achievable

def negamax(position, height):
    #print "Negamaxing at height: {}".format(height)
    achievable = 0
    if height == 0:
        return position.evaluate(len(position.w_pawns), len(position.w_kings), len(position.b_pawns), len(position.b_kings))
    else:
        tmp = 0
        positions = position.generate_positions()
        for pos in positions:
            tmp = -negamax(positions[pos], height - 1)
            achievable = max(tmp, achievable)
    return achievable

def get_best_move(position, height):
    positions = position.generate_positions()
    ranks = []
    #print len(positions.keys())
    for pos in positions:
        ranks.append([negamax(positions[pos], height), pos])
        print "Appending result"
        #ranks.append([pos, negamax(positions[pos], height, -99999,99999)])
    ranks.sort()
    print ranks
    return ranks[len(ranks)-1][1]

