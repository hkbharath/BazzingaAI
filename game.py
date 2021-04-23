# Used the code from
# Copyright 2014 Google Inc. All rights reserved.

import random
import sys
import time

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
    if grid:
      self.board = gird
      self.is_custom_board = True  
    else:
      self.board = [[None] * N for i in range(N)]
      self.is_custom_board = False
    
    self.randomTile()
    self.randomTile()
    
    self.score = 0
    self.over = (len(self.get_next_moves()) == 0)


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

  def show(self):
    for i in range(N):
      for j in range(N):
        if self.board[j][i]:
          print ('%4d' % self.board[j][i]),
        else:
          print ('   .'),
      print("")

class GameManager():
  def __init__(self):
    self.board = Board()

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
  
  def tryMove(self, gird, direction):
    if not self.board.canMove(direction, gird=grid):
      return grid, 0
    return self.board.to_move(grid, direction)
    
  def printState(self):
    self.board.show()

  def getGameTracker(self):
    return self.board.gt