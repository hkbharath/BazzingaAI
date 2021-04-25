# Simulation to test the game 
# This makes fully random moves till the game ends

from game import GameManager 
from game import Moves

import random
from statistics import mean, variance, stdev, mode
import time
import sys

T=2

def simulation_random_move(sim_gm, depth, h_score):
    tot_score = 0

    if sim_gm.isOver():
        return tot_score

    empty_cell_list = sim_gm.getEmptyCells()
    pcell = 1/len(empty_cell_list)

    for pos in empty_cell_list:
        #Try assigning 4 in current empty slot
        grid = sim_gm.getCurrentState()
        grid[pos[0]][pos[1]] = 4
        tot_score = tot_score + 0.1*pcell*expectimax(grid, depth-1, False, h_score)

        grid[pos[0]][pos[1]] = 2
        tot_score = tot_score + 0.9*pcell*expectimax(grid, depth-1, False, h_score)
    return tot_score

def heuristic(sim_gm, h_score):
    return h_score # + some mroe calculation from sim_gm

def expectimax(grid, depth, is_random, h_score):
    sim_gm = GameManager(grid)
    # sim_gm.enableRandomTile(False) # May not be needed
    if depth == 0 or sim_gm.isOver():
        return heuristic(sim_gm, h_score)
    elif is_random:
        return simulation_random_move(sim_gm, depth, h_score)    
    else:
        # our move
        max_score = -999999
        moves = sim_gm.getAvailableMoves()
        for game_move in moves:
            current_grid, current_score = sim_gm.tryMove(grid, game_move)
            mscore = max(max_score, expectimax(current_grid, depth-1, True, h_score + current_score))
            if mscore > max_score:
                max_score = mscore
        return max_score
    return -1        
                
def run():
    game = GameManager()
    gt = game.getGameTracker()
    depth = 4

    while not game.isOver():
    
        moves = game.getAvailableMoves()
        best_move = moves[0]
        best_sc = 0

        for move in moves:
            current_sc = expectimax(game.getCurrentState(), depth, False, 0)
            if current_sc > best_sc:
                best_move = move
                best_sc = current_sc
        
        game.makeMove(best_move)

    print("Final Score: %d"%(game.getScore()))
    print("Max Tile: %d"%(gt.getMaxTile()))
    print("No. Of Moves: %d"%(gt.getNoOfMoves()))
    print("Time per  move: %0.5f"%(gt.getTimePerMove()))
    return gt

if __name__ == "__main__":
    print("Expectimax Bot")
    t_scores = []
    ex_times = []
    max_tile = []
    num_moves = []
    while T > 0:
        gt = run()
        t_scores.append(gt.getScore())
        ex_times.append(gt.getTimePerMove())
        max_tile.append(gt.getMaxTile())
        num_moves.append(gt.getNoOfMoves())
        T = T-1
    print("Final Analysis:")
    print("Mean Score: %.3f"%(mean(t_scores)))
    print("Max Score: %d"%(max(t_scores)))
    print("Std Deviation of Scores: %.3f"%(stdev(t_scores)))
    print("Average Time taken per move(sec): %.4f"%(mean(ex_times)))
    print("Average No. of moves: %.4f"%(mean(num_moves)))
    print("Most common Max Tile reached: %d"%(mode(max_tile)))