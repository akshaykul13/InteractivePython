"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 6    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Performs a random trial of the game
    """
    print "Dimensions:" + str(board.get_dim())
    player_temp = player
    size = board.get_dim()
    moves_list = range(size*size)
    random.shuffle(moves_list)    
    for move in moves_list:        
        print "Move : " + str(move)
        if board.square(move/size, move%size) == provided.EMPTY:
            board.move(move/size, move%size, player_temp)
            if board.check_win() != None:
                return
            if player_temp == provided.PLAYERX:
                player_temp = provided.PLAYERO
            else:
                player_temp = provided.PLAYERX
            #print board                 
    
def mc_update_scores(scores, board, player):
    """
    Updates the scores list of lists with the current board
    
    """
    if board.check_win() == provided.DRAW:
        return
        
    if board.check_win() == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += 1
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] -= 1                    
    else:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] -= 1
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                else:
                    scores[row][col] += 1
    print scores
    
def get_best_move(board, scores):
    """
    Based on the board and scores gives the best possible move
    """
    req_row = -1
    req_col = -1
    max_score = -9999999
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row,col) == provided.EMPTY:
                if req_row == -1:
                    req_row = row
                    req_col = col
                if scores[row][col] > max_score:
                    req_row = row
                    req_col = col
                    max_score = scores[row][col]
    print "Good move : " + str(req_row) + "," + str(req_col)
    return (req_row,req_col)
    
    
def mc_move(board, player, trials):
    """
    Makes trails number of trials and calculates best possible
    move. Then makes that move.
    """
    scores = [[0 for row in range(board.get_dim())] for col in range(board.get_dim())]    
    print scores
    row=0
    print row
    col=0
    print col
    for trial in range(trials):
        print trial
        board_clone = board.clone()
        #print board_clone
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#board1 = provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]])
#mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERX, NTRIALS) 
#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)