"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """    
    #print "Entering mm_move"
    #print board    
    current_scores = []
    if len(board.get_empty_squares()) == 0:
        result = board.check_win()
        if result == provided.PLAYERX:
            current_scores.append((1, (-1,-1)))
            return 1, (-1,-1)
        elif result == provided.PLAYERO:
            current_scores.append((-1, (-1,-1)))
            return -1, (-1, -1)
        else:
            current_scores.append((0, (-1,-1)))
            return 0, (-1, -1)
    else:        
        empty_squares = board.get_empty_squares()        
        for square in empty_squares:
            board_clone = board.clone()
            board_clone.move(square[0], square[1], player)  
            if board.check_win() != None:
                result = board.check_win()
                if result == provided.PLAYERX:
                    current_scores.append((1, square))
                    return 1, square
                elif result == provided.PLAYERO:
                    current_scores.append((-1, square))
                    return -1, square
                else:
                    current_scores.append((0, square))
                    return 0, square 
            if player == provided.PLAYERX:
                outcome = mm_move(board_clone, provided.PLAYERO)
                current_scores.append((outcome[0], square))
                #print "Score1 = " + str(outcome)  
                #print current_scores
            else:
                outcome = mm_move(board_clone, provided.PLAYERX)
                current_scores.append((outcome[0], square))
                #print "Score2 = " + str((outcome[0], square))                
                #print current_scores
            
        max1 = None
        if player == provided.PLAYERX:
            max1 = -1
        else:
            max1 = 1
        pair = (-1,-1)
        #print "End of level " + str(player)
        #print current_scores
        for val in current_scores:
            if player == provided.PLAYERX:
                if val[0]>=max1 and val[1] != (-1,-1):
                    max1 = val[0]
                    pair = val[1]
            else:
                if val[0]<=max1 and val[1] != (-1,-1):
                    max1 = val[0]
                    pair = val[1]
        #print "Max: " + str(max1) + " Pair: " + str(pair)
        return max1, pair

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)
#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#print mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#print "Final"