# Simulation to test the game 
# This makes fully random moves till the game ends

from game import GameManager 
from game import Moves
import random
from statistics import mean, variance, stdev, mode
import time

T=10

def simulation( grid, start_move):
    iteration=25
    score_list = []

    while iteration > 0:
        sim_game = GameManager(grid)
        sim_game.makeMove(start_move)
        
        while not sim_game.isOver():
            move = random.choice(sim_game.getAvailableMoves())
            sim_game.makeMove(move) 

        gt = sim_game.getGameTracker()
        score_list.append(gt.getScore())
        iteration = iteration-1
    return mean(score_list)


def run():
    game = GameManager()
    gt = game.getGameTracker()
    while not game.isOver():
        max_score = 0
        max_move = None
        moves = game.getAvailableMoves()
        for game_move in moves:
            current_grid = game.getCurrentState()
            
            cscore = simulation( current_grid, game_move)
            if cscore > max_score:
                max_score = cscore
                max_move = game_move
            # print("Move %s: %d"%(game_move, cscore))
        game.makeMove(max_move)
        # print(max_move)
    game.printState()
    print(" ")

    print("Final Score: %d"%(game.getScore()))
    print("Max Tile: %d"%(gt.getMaxTile()))
    print("No. Of Moves: %d"%(gt.getNoOfMoves()))
    print("Time per  move: %0.5f"%(gt.getTimePerMove()))
    
    return gt

if __name__ == "__main__":
    print("I am agent 2048. The name is Monte Carlo!")
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