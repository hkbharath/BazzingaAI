from game import GameManager 
from game import Moves
import random
from statistics import mean, variance, stdev, mode
import time
from collections import defaultdict


# Constants
alpha=.1
discount=.1
reward=1
#q_scores={}
#best_moves={}
q_values = {}

def encode(grid):
    glist = list(set([0 if tile is None else tile for row in grid for tile in row]))
    glist.sort()
    key = ','.join([str(glist.index(tile if tile else 0)) for row in grid for tile in row])
    # smgm = GameManager(grid)
    # all_moves = [Moves.MOVE_LEFT, Moves.MOVE_DOWN, Moves.MOVE_RIGHT, Moves.MOVE_UP]
    # scl = []
    # sc_min = float("inf")
    # sc_max = 0
    # for move in all_moves:
    #   ng, ns = smgm.tryMove(grid, move)
    #   if ng == grid:
    #     scl.append(-1)
    #   else:
    #     scl.append(ns)
    #     sc_min = min(sc_min, ns)
    #     sc_max = max(sc_max, ns)
    
    # for i in range(len(scl)):
    #   if scl[i] == -1:
    #     scl[i] = str(scl[i])
    #     continue
    #   div = 1
    #   if sc_max != sc_min:
    #     div = sc_max - sc_min
    #   scl[i] = str((scl[i] - sc_min)/div)
        
    # key = ','.join(scl)
    # print(grid)
    # print(key)
    return key



def simulation():
    #iteration=10
    #score_list = []
    global q_values
    #global best_moves
    
    sim_game = GameManager()
    
    while not sim_game.isOver():
        current_State_Score=sim_game.getScore()
        key_currentstate = encode(sim_game.getCurrentState())
        moves = sim_game.getAvailableMoves()
        all_moves = [Moves.MOVE_LEFT, Moves.MOVE_DOWN, Moves.MOVE_RIGHT, Moves.MOVE_UP]
        Score=0
        move=random.choice(moves)
        sim_game.makeMove(move)
        
        key_nextstate = encode(sim_game.getCurrentState())
        #print(key_nextstate)
        next_State_Score=sim_game.getScore()
        Qvalue_nextstate=[]
        #Score=current_State_Score+alpha*(next_State_Score+discount*next_State_Score)
        for movement in all_moves:
          #print(movement)
          nextKey = key_nextstate+'|'+movement
          if nextKey not in q_values.keys():
            Qvalue_nextstate.append(0)
          else:
            Qvalue_nextstate.append(q_values[nextKey])
        max_Qvalue_nextstate=max(Qvalue_nextstate)
        curr_key = key_currentstate+'|'+move
        reward = sim_game.getScore()
        #print(curr_key)
        if curr_key not in q_values.keys():
          q_values[curr_key] =alpha*(reward+discount*max_Qvalue_nextstate)
            
        else:
          Score=q_values[curr_key]+alpha*(reward+discount*max_Qvalue_nextstate)
          if q_values[curr_key]<Score:
            q_values[curr_key] =Score
            #print(q_values)
        
    

def qlearning(iteration):
    while iteration>0:
        simulation()
        iteration=iteration-1

def run():
    global q_values
    used_qvals = 0
    random_moves = 0

    game = GameManager()
    gt = game.getGameTracker()
    
    
    while not game.isOver():
        current_state=game.getCurrentState()
        moves=game.getAvailableMoves()
        #print(moves)

        max_score = 0
        max_move = None
        for move in moves:
          
          checkKey = encode(current_state)+'|'+move
          if checkKey in q_values.keys():
            if max_score<q_values[checkKey]:
              max_score=q_values[checkKey]
              max_move=move
        if not max_move:
          max_move=random.choice(moves)
          random_moves += 1
        else:
          used_qvals += 1
        game.makeMove(max_move)
        # print("Move %s: %d"%(game_move, cscore))
        
    print(move)
    game.printState()
    print(" ")
    
    print("Final Score: %d"%(game.getScore()))
    print("Max Tile: %d"%(gt.getMaxTile()))
    print("No. Of Moves: %d"%(gt.getNoOfMoves()))
    print("Time per  move: %0.5f"%(gt.getTimePerMove()))
    print("Random Moves: %d"%(random_moves))
    print("Q Table Access: %d"%(used_qvals))
    return gt

if __name__ == "__main__":
    print("I am agent 2048. The name is q learning!")
    t_scores = []
    ex_times = []
    max_tile = []
    num_moves = []
    T = 10

    tst = time.time()
    training = 100000
    qlearning(training)
    tend = time.time()
    print("Total Q values: %d"%(len(q_values.keys())))
    print("Training Time: %d"%(tend-tst))

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