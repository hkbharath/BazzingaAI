# Simulation to test the game 
# This makes fully random moves till the game ends

from game import GameManager 
from game import Moves

import random
from statistics import mean, variance, stdev, mode
import time
import sys

T=10
DEBUG = False

class ExpectimaxAgent():
    def __init__(self, N=4):
        self.scores = {}
        self.N = N
        self.depth = 2

    def encode(self, grid):
        key = ','.join([str(tile) for row in grid for tile in row])
        return key

    def simulation_random_move(self, sim_gm, depth, h_score):
        tot_score = 0

        if sim_gm.isOver():
            return tot_score

        empty_cell_list = sim_gm.getEmptyCells()
        pcell = 1/len(empty_cell_list)

        for pos in empty_cell_list:
            #Try assigning 4 in current empty slot
            grid = sim_gm.getCurrentState()
            grid[pos[0]][pos[1]] = 4
            tot_score = tot_score + 0.1*pcell*self.expectimax(grid, depth-1, False, h_score)
            grid[pos[0]][pos[1]] = 0

            grid[pos[0]][pos[1]] = 2
            tot_score = tot_score + 0.9*pcell*self.expectimax(grid, depth-1, False, h_score)
            grid[pos[0]][pos[1]] = 0
        return tot_score

    def heuristic(self, sim_gm, h_score):
        #set using trail and error
        w_freecell = 2.5
        w_monotone = 0.75
        w_maxtile = 1
        w_smooth = 0.5

        key = self.encode(sim_gm.getCurrentState())
        if key in self.scores:
            return self.scores[key]
        final_score = 0 #h_score
        final_score += w_freecell * sim_gm.evalFreeCells() 
        final_score += w_smooth * sim_gm.evalSmoothness()
        final_score += w_monotone*sim_gm.evalMonotone_simple()
        final_score += w_maxtile * sim_gm.evalMaxTile()
        # final_score += sim_gm.evalMonotone()

        if random.randint(0,100) == 0 and DEBUG == True:
            sim_gm.printState()
            print("Free Cell %.3f"%(sim_gm.evalFreeCells()))
            print("Smoothness %.3f"%(sim_gm.evalSmoothness()))
            print("Monotone Simple %.3f"%(sim_gm.evalMonotone_simple()))
            print("Max Tile %d"%(sim_gm.evalMaxTile()))
            print("Score %d"%(h_score))

        self.scores[key] = final_score
        return self.scores[key] 

    def expectimax(self, grid, depth, is_random, h_score):
        sim_gm = GameManager(grid)
        # sim_gm.enableRandomTile(False) # May not be needed
        if depth == 0 or sim_gm.isOver():
            return self.heuristic(sim_gm, h_score)
        elif is_random:
            return self.simulation_random_move(sim_gm, depth, h_score)    
        else:
            # our move
            max_score = float('-inf')
            moves = sim_gm.getAvailableMoves()
            for game_move in moves:
                current_grid, current_score = sim_gm.tryMove(grid, game_move)
                max_score = max(max_score, self.expectimax(current_grid, depth, True, h_score + current_score))
            return max_score
        return -1
    
    def getNextMove(self, grid, moves):
        best_move = moves[0]
        best_sc = float('-inf')
        sim_gm = GameManager(grid)

        for move in moves:
            current_grid, current_score = sim_gm.tryMove(grid, move)
            depth = self.depth
            if sim_gm.getNoOfEmptyCells() <= 2:
                depth += 1 
            current_score = self.expectimax(current_grid, depth, True, current_score)
            # print("Score %.3f:%s"%(current_score, move))
            if current_score > best_sc:
                best_move = move
                best_sc = current_score
        # print("")
        return best_move

def run():
    game = GameManager()
    gt = game.getGameTracker()

    ai = ExpectimaxAgent(4) # 4x4 tile game
    while not game.isOver():
    
        moves = game.getAvailableMoves()
        # random.shuffle(moves)
        next_move = ai.getNextMove(game.getCurrentState(), moves)
        game.makeMove(next_move)
        # print("Move made: %s"%(next_move))
        # if not DEBUG:
        #     game.printState()
    game.printState()
    print("Final Score: %d"%(game.getScore()))
    print("Max Tile: %d"%(gt.getMaxTile()))
    print("No. Of Moves: %d"%(gt.getNoOfMoves()))
    print("Time per  move: %0.5f"%(gt.getTimePerMove()))
    # print(ai.scores)
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
    