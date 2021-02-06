#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    total_dist = 0
    for snowball in state.snowballs:
      total_dist += abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])

    return total_dist


#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    # General idea: Manhattan distance misses several specific cases that end up misleading the search
    # ie if the snowball is in the corner, and the destination is not that corner, it can't be moved to the destination


    total_dist = 0
    for snowball in state.snowballs:
      x = snowball[0]
      y = snowball[1]
      if snowball not in state.destination:
        # corner cases
        top_left = (0, state.height - 1)
        top_right = (state.width-1, state.height-1)
        bottom_left = (0, 0)
        bottom_right = (state.width, 0)
        if(snowball == top_left or snowball == top_right or snowball == bottom_left or snowball == bottom_right):
          if(state.destination != snowball):
            return float("inf")

        # wall cases
        if((y == 0 or y == state.height -1) and (y != state.destination[1])):
          return float("inf")
        elif((x == 0 or x == state.width -1) and (x != state.destination[0])):
          return float("inf")

        total_dist += abs(snowball[0] - state.destination[0]) + abs(snowball[1] - state.destination[1])
      else:
        return 0


    return total_dist

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return 0

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  return False

def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  start_time = os.times()[0]
  end_time = start_time + timebound

  # initialize search engine
  s = SearchEngine('best_first', 'full')
  s.init_search(initial_state, snowman_goal_state, heur_fn)

  # perform first search. No cost bound since there is no baseline yet
  result = s.search(timebound)
  cost_bound = (float("inf"), float("inf"), float("inf")) # g, h, g+h
  return_val = False
  #if(result):
    #print("here")
  while (start_time < end_time):
    if result:
      # pruning step
      if(result.gval < cost_bound[0]):
        cost_bound = (result.gval, result.gval, result.gval * 2)
        return_val = result
    else:
      #print("here2")
      return return_val
    # perform search
    result = s.search(timebound, cost_bound)

  return return_val
