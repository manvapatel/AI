"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function
from util import INFINITY, NEG_INFINITY


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

#STUDENT_ID = 20815074
#AGENT_NAME = Connectplay
# COMPETE = False

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000 - board.num_tokens_on_board()
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10 
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col) 
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score

    #raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alphabeta_find_board_value(alpha, beta, board, depth, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        #print("move is:",move)
        val = -1 * alphabeta_find_board_value(-beta, -alpha, new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        #print("val is", val)
        if best_val is None or val > best_val:
            best_val = val
            alpha = max(alpha, best_val)
            if alpha>=beta:
              break

    return best_val

def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """

    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alphabeta_find_board_value(NEG_INFINITY, INFINITY, new_board, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if best_val is None or val > best_val[0]:
            best_val = (val, move, new_board)
            
    return best_val[1]
#raise NotImplementedError


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=better_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

      


def better_evaluate(board):
    #print("inside better_evaluate")
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000 
    else:

      #calculate the number of chains for current player
      l = []
      my_list = []
      #stores the list of chains
      chain_groups = list(board.chain_cells(board.get_current_player_id()))
      #counts the lenght of each chain and stores them in a list l
      for x in range(len(chain_groups)):
          l.append(len(chain_groups[x]))
      #counts the number of chains of 1's, 2's and 3's and stores them in a list called my_list. 
      my_list.append(l.count(1))
      my_list.append(l.count(2))
      my_list.append(l.count(3))

      #similarly calculate the number of chains of the opposite player
      lp = []
      opp_list = []
      opp_chain_groups = list(board.chain_cells(board.get_other_player_id()))
      for x in range(len(opp_chain_groups)):
          lp.append(len(opp_chain_groups[x]))
      opp_list.append(lp.count(1))
      opp_list.append(lp.count(2))
      opp_list.append(lp.count(3))

      #assign a weight of 1 to series of 1's, a weight of 2 to series of 2's and a weight of 3 to series of 3's
      weights = [1,2,3]
      my_score = sum([s*w for s,w in zip(my_list, weights)])
      opp_score = sum([s*w for s,w in zip(opp_list, weights)])
      score = my_score - opp_score
      #print("score",score)
    return score  


    #raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
