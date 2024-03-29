#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    board, last_row = initial_tenner_board
    var_array = [[] for i in range(len(board))]
    var_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    nrows = len(board)
    #print("array: \n")
    #print(var_array)
    # init variables
    for i in range(nrows):
      for j in range(10):
        if board[i][j] == -1: # if empty, have all of domain in variable
          var_array[i].append(Variable("{},{}".format(i, j), var_domain))
        else: # if given, save to variable array
          var_array[i].append(Variable('V{},{}'.format(i,j), [board[i][j]]))

    # construct model
    model_vars = []
    for row in var_array:
      for v in row:
        model_vars.append(v)

    model1 = CSP("Model1", model_vars)

    for row in range(nrows):
      for col in range(10):
        for x in itertools.combinations(var_array[row], 2):
          # row constraints, all combinations of two variables in a row are different
          c = Constraint('C:V{}xV{}'.format(x[0].name, x[1].name), x)

          domains = []
          for var in x:
            domains.append(var.domain())

          s = []
          for i in itertools.product(*domains):
            if i[0] != i[1]:
              s.append(i)
          c.add_satisfying_tuples(s)
          model1.add_constraint(c)


        # special cases + contiguous constraints
        if row == 0:
          if col == 0:
            con = [var_array[row+1][col+1], var_array[row+1][col]]
          elif col == 9:
            con = [var_array[row+1][col-1], var_array[row+1][col]]
          else:
            con = [var_array[row+1][col-1], var_array[row+1][col], var_array[row+1][col+1]]
        elif row == nrows-1:
          if col == 0:
            con = [var_array[row-1][col], var_array[row-1][col+1]]
          elif col == 9:
            con = [var_array[row-1][col], var_array[row-1][col-1]]
          else:
            con = [var_array[row-1][col-1], var_array[row-1][col], var_array[row-1][col+1]]
        elif col == 9:
          con = [var_array[row+1][col], var_array[row+1][col-1], var_array[row-1][col-1], var_array[row-1][col]]
        elif col == 0:
          con = [var_array[row+1][col], var_array[row+1][col+1], var_array[row-1][col+1], var_array[row-1][col]]
        else:
          con = [var_array[row+1][col], var_array[row+1][col-1], var_array[row+1][col+1], var_array[row-1][col], var_array[row-1][col-1], var_array[row-1][col+1]]
        # construct the constraints, add to model for each variable pair
        for v in con:
          x = [var_array[row][col], v]
          # vars, model1
          c = Constraint('C:V{}xV{}'.format(x[0].name, x[1].name), x)

          domains = []
          for var in x:
            domains.append(var.domain())

          s = []
          for i in itertools.product(*domains):
            if i[0] != i[1]:
              s.append(i)
          c.add_satisfying_tuples(s)
          model1.add_constraint(c)

    for i in range(10):
      domains = [var_array[x][i].cur_domain() for x in range(nrows)]
      #print("domains: \n")
      #print(domains)
      c = Constraint("sum{}".format(i), [var_array[x][i] for x in range(nrows)])
      for j in itertools.product(*domains):
        if sum(j) == last_row[i]:
          c.add_satisfying_tuples([j])
      model1.add_constraint(c)


#IMPLEMENT
    return model1, var_array #CHANGE THIS
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

    board, last_row = initial_tenner_board
    var_array = [[] for i in range(len(board))]
    var_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    nrows = len(board)
    #print("array: \n")
    #print(var_array)
    # init variables
    for i in range(nrows):
      for j in range(10):
        if board[i][j] == -1: # if empty, have all of domain in variable
          var_array[i].append(Variable("{},{}".format(i, j), var_domain))
        else: # if given, save to variable array
          var_array[i].append(Variable('V{},{}'.format(i,j), [board[i][j]]))

    # construct model
    model_vars = []
    for row in var_array:
      for v in row:
        model_vars.append(v)

    model1 = CSP("Model1", model_vars)

    # row constraints
    for i in range(nrows):
      for j in range(10):
        for k in range(j+1, 10):
          c = Constraint("rows",[var_array[i][j],var_array[i][k]])

          all_tuples = []
          for v1 in var_array[i][j].domain():
            for v2 in var_array[i][k].domain():
              if (v1 != v2):
                all_tuples.append((v1, v2))
          c.add_satisfying_tuples(all_tuples)
          model1.add_constraint(c)


    # everything else is same as model1
    for row in range(nrows):
      for col in range(10):
        # special cases + contiguous constraints
        # same as model1
        if row == 0:
          if col == 0:
            con = [var_array[row+1][col+1], var_array[row+1][col]]
          elif col == 9:
            con = [var_array[row+1][col-1], var_array[row+1][col]]
          else:
            con = [var_array[row+1][col-1], var_array[row+1][col], var_array[row+1][col+1]]
        elif row == nrows-1:
          if col == 0:
            con = [var_array[row-1][col], var_array[row-1][col+1]]
          elif col == 9:
            con = [var_array[row-1][col], var_array[row-1][col-1]]
          else:
            con = [var_array[row-1][col-1], var_array[row-1][col], var_array[row-1][col+1]]
        elif col == 9:
          con = [var_array[row+1][col], var_array[row+1][col-1], var_array[row-1][col-1], var_array[row-1][col]]
        elif col == 0:
          con = [var_array[row+1][col], var_array[row+1][col+1], var_array[row-1][col+1], var_array[row-1][col]]
        else:
          con = [var_array[row+1][col], var_array[row+1][col-1], var_array[row+1][col+1], var_array[row-1][col], var_array[row-1][col-1], var_array[row-1][col+1]]
        # construct the constraints, add to model for each variable pair
        for v in con:
          x = [var_array[row][col], v]
          # vars, model1
          c = Constraint('C:V{}xV{}'.format(x[0].name, x[1].name), x)

          domains = []
          for var in x:
            domains.append(var.domain())

          s = []
          for i in itertools.product(*domains):
            if i[0] != i[1]:
              s.append(i)
          c.add_satisfying_tuples(s)
          model1.add_constraint(c)
    
    # same as model1
    for i in range(10):
      domains = [var_array[x][i].cur_domain() for x in range(nrows)]
      #print("domains: \n")
      #print(domains)
      c = Constraint("sum{}".format(i), [var_array[x][i] for x in range(nrows)])
      for j in itertools.product(*domains):
        if sum(j) == last_row[i]:
          c.add_satisfying_tuples([j])
      model1.add_constraint(c)


#IMPLEMENT
    return model1, var_array #CHANGE THIS
