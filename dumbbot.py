# Simulation to test the game 
# This makes fully random moves till the game ends

from game import GameManager 
from game import Moves

import random
from statistics import mean, variance, stdev, mode
import time

T=100

def run():
    game = GameManager()
    step_time = []
    while not game.isOver():
        # print(game.getAvailableMoves())
        
        st = time.time()
        # Measure time taken to decide and make a move

        # Implement your logic of selecting a move
        move = game.getAvailableMoves()[0]

        game.makeMove(move)
        #end timer
        et = time.time()
        step_time.append(et-st)

    gt = game.getGameTracker()
    # print("Final Score: %d"%(game.getScore()))
    # print("Max Tile: %d"%(gt.getMaxTile()))
    # print("No. Of Moves: %d"%(gt.getNoOfMoves()))
    # print("Time per  move: %0.5f"%(gt.getTimePerMove()))
    return gt

if __name__ == "__main__":
    print("I am dubm, but don't underestimate me!")
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