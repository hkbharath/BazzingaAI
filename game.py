# Used the code from
# Copyright 2014 Google Inc. All rights reserved.

import random
import sys
import time
import math

# board size
N = 4

class Moves:
  MOVE_LEFT = 'left'
  MOVE_UP = 'up'
  MOVE_RIGHT = 'right'
  MOVE_DOWN = 'down'

class GameTracker:
  def __init__(self):
    self.no_moves = 0
    self.st_time = time.time()
    self.end_time = 0
    self.max_tile = 2
    self.score = 0

  def getTimePerMove(self):
    return (self.end_time - self.st_time)/self.no_moves

  def getMaxTile(self):
    return self.max_tile
  
  def getNoOfMoves(self):
    return self.no_moves

  def getScore(self):
    return self.score

class Board(object):
  def __init__(self, grid=None):
    
    self.over = False
    self.gt = GameTracker()
    self.enableRandomTile = True

    if grid:
      self.board = grid
      self.is_custom_board = True 
      # check if the game is already over
      if len(self.get_next_moves()) == 0:
        self.over = True 
    else:
      self.board = [[None] * N for i in range(N)]
      self.is_custom_board = False
      self.randomTile()
      self.randomTile()

  #Would be needed for Deep RL
  def startGame():
    if self.gt.score == 0 and not self.over:
      self.gt = GameTracker()

  #Would be needed for Deep RL
  def startGame():
    if self.gt.score == 0 and not self.over:
      self.gt = GameTracker()

  def rotateLeft(self, grid):
    out = self.emptyGrid()
    for c in range(N):
      for r in range(N):
        out[r][N-1-c] = grid[c][r]
    return out

  def rotateRight(self, grid):
    out = self.emptyGrid()
    for c in range(N):
      for r in range(N):
        out[N-1-r][c] = grid[c][r]
    return out

  def emptyGrid(self):
    out = list()
    for x in range(N):
      col = list()
      for y in range(N):
        col.append(None)
      out.append(col)
    return out

  def to_move(self, grid, direction):
    
    out = self.emptyGrid()

    if direction == Moves.MOVE_UP:
      rot = 1
    elif direction == Moves.MOVE_RIGHT:
      rot = 2
    elif direction == Moves.MOVE_DOWN:
      rot = 3
    else:
      rot = 0

    for i in range(rot):
      grid = self.rotateLeft(grid)

    score = 0
    for r in range(N):
      oc = 0
      ic = 0
      while ic < N:
        if grid[ic][r] is None:
          ic += 1
          continue
        out[oc][r] = grid[ic][r]
        oc += 1
        ic += 1

      ic = 0
      oc = 0
      while ic < N:
        if out[ic][r] is None:
          break
        if ic == N-1:
          out[oc][r] = out[ic][r]
          oc += 1
          break
        if out[ic][r] == out[ic+1][r]:
          #out[oc][r] *= 2
          out[oc][r] = 2*out[ic][r]
          score += out[oc][r]
          if self.gt.max_tile < out[oc][r]:
            self.gt.max_tile = out[oc][r]
          ic += 1
        else:
          out[oc][r] = out[ic][r]
        ic += 1
        oc += 1
      while oc < N:
        out[oc][r] = None
        oc += 1

    for i in range(rot):
      out = self.rotateRight(out)

    return out, score

  def move(self, direction):
    #print 'move', direction
    next_board, got_score = self.to_move(self.board, direction)
    moved = (next_board != self.board)

    self.board = next_board
    self.gt.score += got_score

    if moved:
      self.gt.no_moves = self.gt.no_moves + 1
      if not self.randomTile() or len(self.get_next_moves()) == 0:
        self.over = True
        self.gt.end_time = time.time()

  def canMove(self, direction, grid=None):
    if not grid:
      grid = self.board
    return self.board != self.to_move(grid, direction)[0]

  def get_empty_cells(self):
    for i in range(N):
      for j in range(N):
        if self.board[i][j] is None:
          yield i, j

  def get_next_moves(self):
    moves = []
    if self.over:
      return moves
    for move in [Moves.MOVE_LEFT, Moves.MOVE_DOWN, Moves.MOVE_RIGHT, Moves.MOVE_UP]:
      if self.canMove(move):
        moves.append(move)
    return moves

  def randomTile(self):
    if not self.enableRandomTile:
      return True
    cells = list(self.get_empty_cells())
    if not cells:
      return False
    #print 'cells', cells


    if random.random() < 0.9:
      v = 2
    else:
      v = 4

    cid = random.choice(cells)
    #print cid
    self.board[cid[0]][cid[1]] = v
    return True

  def enableRandomTile(rtile):
    self.enableRandomTile = rtile

  def show(self):
    for i in range(N):
      print ('|', end='')
      for j in range(N):
        if self.board[j][i]:
          print (' %4d |' % self.board[j][i], end='')
        else:
          print ('    . |', end='')
      print("")

class GameManager():
  def __init__(self, grid = None):
    self.board = Board(grid)

  def getCurrentState(self):
    return self.board.board

  def getScore(self):
    return self.board.gt.score

  def isOver(self):
    return self.board.over

  def getAvailableMoves(self):
    return self.board.get_next_moves()
  
  def makeMove(self, direction):
    if self.isOver() or not self.board.canMove(direction):
      return False
    self.board.move(direction)
    return True
  
  def tryMove(self, grid, direction):
    if not self.board.canMove(direction, grid=grid):
      return grid, 0
    return self.board.to_move(grid, direction)
    
  def printState(self):
    self.board.show()

  def getGameTracker(self):
    return self.board.gt

  def getNoOfEmptyCells(self):
    return len(list(self.board.get_empty_cells()))
  
  def getEmptyCells(self):
    return list(self.board.get_empty_cells())
  
  def evalSmoothness(self, grid=None):
    if grid is None:
      grid = self.board.board
    score_smooth = 0
    N = len(grid)
    for x in range(N-1):
        for y in range(N-1):
            s = 0
            # s += abs((grid[x][y] or 2) - (grid[x+1][y] or 2))
            # s += abs((grid[x][y] or 2) - (grid[x][y+1] or 2))
            if grid[x][y] and grid[x+1][y]:
              s += abs((math.log(grid[x][y])/math.log(2)) - (math.log(grid[x+1][y])/math.log(2)))
            if grid[x][y] and grid[x][y+1]:
              s += abs((math.log(grid[x][y])/math.log(2)) - (math.log(grid[x][y+1])/math.log(2)))
            score_smooth -= s
    return score_smooth
  
  def evalFreeCells(self, grid=None):
    if grid is None:
      grid = self.board.board

    empty_count = 0

    for row in grid:
      # one of them will be there
      empty_count += row.count(None)
      empty_count += row.count(0)
    
    # print(empty_count)
    # print(grid)
    # return (16-empty_count)**2
    if empty_count == 0:
      return 0
    return math.log(empty_count)
  
  def evalMaxTile(self, grid=None):
    if grid is None:
      grid = self.board.board
    
    return max([0 if tile is None else tile for row in grid for tile in row])


  def evalMonotone(self, grid=None):
    if grid is None:
      grid = self.board.board
    
    for x in range(N):
      for y in range(N):
        if grid[x][y] is None:
          grid[x][y] = 0

    L = R = U = D = 0
    LR = UD = 0
    for x in range(N):
      m = 0
      for y in range(N-1):
        if grid[x][y] and grid[x][y] >= grid[x][y+1]:
          m += 1
          L += m ** 2 * 4
        else:
          L -= abs((grid[x][y] or 0)- (grid[x][y+1] or 0)) * m ** 2
          m = 0

      m = 0
      for y in range(N-1):
        if grid[x][y] <= grid[x][y+1] and grid[x][y+1]:
          m += 1
          R += m ** 2 * 4
        else:
          R -= abs((grid[x][y] or 0)- (grid[x][y+1] or 0)) * m ** 2
          m = 0

    LR += min(L, R)
    L = R = 0

    for y in range(N):
      m = 0
      for x in range(N-1):
        if grid[x][y] and grid[x][y] >= grid[x+1][y]:
          m += 1
        else:
          #U -= abs(to_idx[grid[x][y]] - to_idx[grid[x+1][y]]) ** 2
          U -= abs((grid[x][y] or 0)- (grid[x+1][y] or 0)) * m ** 2
          m = 0

      m = 0
      for x in range(N-1):
        if grid[x][y] <= grid[x+1][y] and grid[x+1][y]:
          m += 1
          D += m ** 2 * 4
        else:
          D -= abs((grid[x][y] or 0)- (grid[x+1][y] or 0)) * m ** 2
          m = 0

    UD += min(U, D)

    return LR + UD

  def evalMonotone_simple(self, grid=None):
    if grid is None:
      grid = self.board.board
    
    for x in range(N):
      for y in range(N):
        if grid[x][y] is None:
          grid[x][y] = 0

    L = R = U = D = 0
    LR = UD = 0
    for x in range(N):
      for y in range(N-1):
        cval = math.log(grid[x][y])/math.log(2) if grid[x][y] else 0
        nval = math.log(grid[x][y+1])/math.log(2) if grid[x][y+1] else 0
        if cval > nval:
          L +=  nval - cval
        else:
          R += cval - nval

    LR = max(L, R)
    L = R = 0

    for y in range(N):
      for x in range(N-1):
        cval = math.log(grid[x][y])/math.log(2) if grid[x][y] else 0
        nval = math.log(grid[x+1][y])/math.log(2) if grid[x+1][y] else 0
        if cval > nval:
          U += nval - cval
        else:
          D += cval - nval
      
    UD = max(U, D)

    return (LR + UD)
    