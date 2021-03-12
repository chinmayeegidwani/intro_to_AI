"""
An AI player for Othello. 
"""

import random
import sys
import time

min_dic = dict()
max_dic = dict()
alpha_dic = dict()
beta_dic = dict()

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    dark, light = get_score(board)
    if(color == 1): #dark
        return dark - light
    if(color == 2): #light
        return light - dark
     #change this!

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    score = 0
    dark, light = get_score(board)
    if(color == 1): #dark
        score = dark - light
    if(color == 2): #light
        score = light - dark

    if(board[0][0] == color):
        score += 50
    if(board[len(board) - 1][0] == color):
        score += 50
    if(board[0][len(board) - 1] == color):
        score += 50
    if(board[len(board) - 1][len(board) - 1] == color):
        score += 50

    return score


def other_player(player):
    if player == 2:
        return 1
    else:
        return 2

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # if it's already been computed and in the dict, return that
    if caching:
        if (board, color) in min_dic:
            return min_dic[(board, color)]

    # you want to select move that minimizes utility
    possible_moves = get_possible_moves(board, other_player(color))

    # -1 or 1? might be -1 since good for min is bad for max, which is our player
    if len(possible_moves) == 0 or limit == 0:  # game ends with no possible moves left
        res = (None, -1 * compute_utility(board, other_player(color)))  # if we reach end of depth limit, use func to compute non-terminal utility value
        if caching:
            min_dic[(board, other_player(color))] = res
        return res

    min_util = float("inf")
    optimal = possible_moves[0]

    for move in possible_moves:
        test_move = play_move(board, other_player(color), move[0], move[1])
        util = minimax_max_node(test_move, color, limit-1, caching)[1]
        if util < min_util:
            optimal = move
            min_util = util

    if caching:
        min_dic[(board, color)] = (optimal, min_util)

    return (optimal, min_util)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    # if it's already been computed and in the dict, return that
    if caching:
        if (board, color) in max_dic:
            return max_dic[(board, color)]
    
    possible_moves = get_possible_moves(board, color)

    if len(possible_moves) == 0 or limit == 0:  # game ends with no possible moves left
        res = (None, 1 * compute_utility(board, color))  # if we reach end of depth limit, use func to compute non-terminal utility value
        if caching:
            max_dic[(board, color)] = res
        return res
    max_util = float("-inf")
    optimal = possible_moves[0]

    for move in possible_moves:
        test_move = play_move(board, color, move[0], move[1])
        util = minimax_min_node(test_move, color, limit-1, caching)[1]
        if util > max_util:
            optimal = move
            max_util = util

    if caching:
        max_dic[(board, color)] = (optimal, max_util)


    return (optimal, max_util)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    return minimax_max_node(board, color, limit, caching)[0] #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if caching:
        if (board, color) in beta_dic:
            return beta_dic[(board, color)]

    # you want to select move that minimizes utility
    possible_moves = get_possible_moves(board, other_player(color))

    # -1 or 1? might be -1 since good for min is bad for max, which is our player
    if len(possible_moves) == 0 or limit == 0:  # game ends with no possible moves left
        res = (None, -1 * compute_utility(board, other_player(color)))  # if we reach end of depth limit, use func to compute non-terminal utility value
        if caching:
            beta_dic[(board, color)] = res
        return res
    min_util = float("inf")
    optimal = possible_moves[0]
    next_states = []

    for move in possible_moves:
        # play next move and populate states
        # if min plays a move
        test_move = play_move(board, other_player(color), move[0], move[1])
        next_states.append(test_move)

    if ordering:
        # order next states in decreasing utility function value
        next_states.sort(key = lambda board: compute_utility(board, color), reverse = True)
    i = 0
    for state in next_states:
        util = alphabeta_max_node(state, color, alpha, beta, limit-1, caching, ordering)[1]
        if util < min_util:
            optimal = possible_moves[i]
            min_util = util
        beta = min(beta, min_util)
        i += 1
        if beta <= alpha:
            break

    if caching:
        beta_dic[(board, color)] = (optimal, min_util)


    return (optimal, min_util)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if caching:
        if (board, color) in alpha_dic:
            return alpha_dic[(board, color)]

    possible_moves = get_possible_moves(board, color)

    if len(possible_moves) == 0 or limit == 0:  # game ends with no possible moves left
        res = (None, 1 * compute_utility(board, color))  # if we reach end of depth limit, use func to compute non-terminal utility value
        if caching:
            alpha_dic[(board, color)] = res
        return res
    max_util = float("-inf")
    optimal = possible_moves[0]

    next_states = []

    for move in possible_moves:
        # play next move and populate states
        test_move = play_move(board, color, move[0], move[1])
        next_states.append(test_move)

    if ordering:
        # order next states in decreasing utility function value
        next_states.sort(key = lambda board: compute_utility(board, color), reverse = True)
    i = 0
    for state in next_states:
        util = alphabeta_min_node(state, color, alpha, beta, limit-1, caching, ordering)[1]
        if util > max_util:
            optimal = possible_moves[i]
            max_util = util

        alpha = max(alpha, max_util)
        i += 1
        if beta <= alpha:
            break

    if caching:
        alpha_dic[(board, color)] = (optimal, max_util)

    return (optimal, max_util)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    return alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching, ordering)[0] #change this!

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
