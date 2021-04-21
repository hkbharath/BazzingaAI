# Simulation to test the game 
# This makes fully random moves till the game ends

from game import GameManager 
from game import Moves

import random
from statistics import mean, variance, stdev
import time

T=100

def run():
    game = GameManager()
    step_time = []
    while not game.isOver():
        # print(game.getAvailableMoves())
        
        st = time.time()
        # Measure time taken to decide and make a move

        # move = random.choice(game.getAvailableMoves())
        move = game.getAvailableMoves()[0]
        game.makeMove(move)

        #end timer
        et = time.time()
        step_time.append(et-st)

    # print("Final Score: %d"%(game.getScore()))
    return game.getScore(), mean(step_time)

if __name__ == "__main__":
    print("I am dubm, but don't underestimate me!")
    t_scores = []
    ex_times = []
    while T > 0:
        sc, et = run()
        t_scores.append(sc)
        ex_times.append(et)
        T = T-1
    print("Final Analysis:")
    print("Mean Score: %.3f"%(mean(t_scores)))
    print("Max Score: %d"%(max(t_scores)))
    print("Std Deviation of Scores: %.3f"%(stdev(t_scores)))
    print("Average Time taken per move(sec): %.4f"%(mean(ex_times)))