import sys, pygame
from pygame.locals import *
pygame.init()
import math
from queue import PriorityQueue
width=500
screen = pygame.display.set_mode((width, width))

pygame.display.set_caption("A* Path Finding Visualizer")
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Block: #class of each block that we are going to visit, paint
  def __init__(self, row, col, size_of_block, no_of_rows):
    self.x=row*size_of_block
    self.y=col*size_of_block
    self.row=row
    self.col=col
    self.color=WHITE
    self.size_of_block=size_of_block
    self.no_of_rows=no_of_rows

  def get_position(self): #position of the block
    return self.row, self.col

  def is_visited(self): 
    return self.color == RED

  def not_visited(self):
    return self.color == GREEN

  def is_obstacle(self):
    return self.color == BLACK

  def is_start(self):
    return self.color == ORANGE

  def is_end(self):
    return self.color == TURQUOISE

  def reset(self):
    self.color = WHITE

  def make_close(self):
    self.color = RED

  def make_open(self):
    self.color = GREEN
  
  def make_obstacle(self):
    self.color = BLACK

  def make_start(self):
    self.color = ORANGE

  def make_end(self):
    self.color = TURQUOISE

  def make_path(self):
    self.color = PURPLE

  def paint_block(self, window):
    pygame.draw.rect(window, self.color, (self.x, self.y, self.size_of_block, self.size_of_block))
  
  def neighbors(self, grid):
    self.neighbors = []

  
    if self.row < self.no_of_rows-1 and not grid[self.row+1][self.col].is_obstacle(): #  down neighbor
      self.neighbors.append(grid[self.row+1][self.col])

    if self.row > 0 and not grid[self.row-1][self.col].is_obstacle(): # up neigbor 
      self.neighbors.append(grid[self.row-1][self.col])
    
    if self.col < self.no_of_rows-1 and not grid[self.row][self.col+1].is_obstacle(): # right neighbor
      self.neighbors.append(grid[self.row][self.col+1])

    if self.col > 0 and not grid[self.row][self.col-1].is_obstacle(): # left neighbor
      self.neighbors.append(grid[self.row][self.col-1])
  
  def __lt__(self, other):
    return False
  
  ########





def make_grid(no_of_rows, width): #creating positions/memory for the blocks in the grid
  grid = []
  size_of_block = width // no_of_rows

  for i in range(no_of_rows):
    grid.append([])
    for j in range(no_of_rows):
      block = Block(i, j, size_of_block, no_of_rows)
      grid[i].append(block)
  
  return grid
  

def grid_lines(window, no_of_rows, width): #creating grid lines
  size_of_block = width // no_of_rows

  for i in range(no_of_rows):
    pygame.draw.line(window, BLACK, (0, i*size_of_block), (width, i*size_of_block))
    for j in range(no_of_rows):
      pygame.draw.line(window, BLACK, (j*size_of_block, 0), (j*size_of_block, width))


def paint_grid(window, grid, no_of_rows, width):
  window.fill(WHITE)
  
  for row in grid:
    for block in row:
      block.paint_block(window)

  grid_lines(window, no_of_rows, width)
  pygame.display.update()


def get_clicked_position(mouse_position, no_of_rows, width):
  y, x = mouse_position
  size_of_block = width // no_of_rows
  row = y // size_of_block
  col = x // size_of_block
  return row, col

def heuristic(point1, point2):  #Manhattan Distance between point1 and point2
  x1, y1 = point1
  x2, y2 = point2
  distance = abs(x1-x2) + abs(y1-y2)
  return distance

def path(parent, current_block, paint_grid):
  while current_block in parent:
    current_block=parent[current_block]
    current_block.make_path()
    paint_grid()

def algorithm(paint_grid, grid, start_block, end_block):
  level=0 # the block with lower level value will be prioritize in case two f scores are equal
  open = PriorityQueue()
  parent={}
  g_score={}
  f_score={}

  open.put((0, level, start_block))
  for row in grid:
    for block in row:
      g_score[block] = float("+inf")

  g_score[start_block]=0

  for row in grid:
    for block in row:
      f_score[block] = float("+inf")
  
  f_score[start_block] = heuristic(start_block.get_position(), end_block.get_position())

  open_set=set([start_block])

  while not open.empty():
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
    
    current_block=open.get()[2]
    open_set.remove(current_block)

    if current_block == end_block: # if found the end point
      path(parent, end_block, paint_grid)
      end_block.make_end()
      return True

    for neighbor in current_block.neighbors:

      current_g_score = g_score[current_block]+1
      if current_g_score < g_score[neighbor]:
        g_score[neighbor] = current_g_score
        f_score[neighbor] = current_g_score + heuristic(neighbor.get_position(), end_block.get_position())
        parent[neighbor]=current_block
        if neighbor not in open_set:
          open_set.add(neighbor)
          level+=1
          open.put((f_score[neighbor], level, neighbor))
          neighbor.make_open()
    
    paint_grid()
    
    if current_block != start_block:
      current_block.make_close()
    
  return False  
            

def main(window, width):
  no_of_rows = 50
  grid = make_grid(no_of_rows, width)

  start_block = None
  end_block = None

  run = True #if we r running the main loop or not
  started = False #if we started the algorithm or not

  while run:
    paint_grid(window, grid, no_of_rows, width)
    for event in pygame.event.get(): #looping through each event present in pygame
      if event.type == QUIT:
        run = False

      if started:
        continue #so that after algorithm starts user won,t be able to do anything

      if pygame.mouse.get_pressed()[0]: #left button
        mouse_position = pygame.mouse.get_pos()
        row, col = get_clicked_position(mouse_position, no_of_rows, width)
        block = grid[row][col]

        if not start_block and block != end_block:
          start_block = block
          start_block.make_start()

        elif not end_block and block != start_block:
          end_block=block 
          end_block.make_end()
        
        elif block != start_block and block != end_block:
          block.make_obstacle()

      elif pygame.mouse.get_pressed()[2]: #right button
        mouse_position = pygame.mouse.get_pos()
        row, col = get_clicked_position(mouse_position, no_of_rows, width)
        block = grid[row][col]
        block.reset()
        if block == start_block:
          start_block= None
        if block == end_block:
          end_block = None

      if event.type == KEYDOWN:
        if event.key == K_SPACE and not started: #if we press space key and algorithm is not already running
          for row in grid:
            for block in row:
              block.neighbors(grid)

          algorithm(lambda: paint_grid(window, grid, no_of_rows, width), grid, start_block, end_block )
  
  pygame.quit()

    
main(screen, width)