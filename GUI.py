import pygame
from test_boards import board_3
import Solver
import time
from copy import deepcopy

pygame.font.init()

BOARD = board_3     #change value to board_n for nth test board(n = 1,2,3,4,5,6)

# unhash bottom two lines of code to import random board from sudokuweb.org:
# import online_board
# BOARD = online_board.main()

BOARD_COPY = deepcopy(BOARD)
WIDTH, HEIGHT = 450,500
WHITE = (255,255,255)
GREY = (100,100,100)
BLACK =(0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
SIZE = 50
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FONT = pygame.font.SysFont('comicsans', 20)
SCORE = 0
SOLVE_BUTTON = pygame.Rect(0,450,100,50)
pygame.display.set_caption("Sudoku")


GRID_GRID = []
filled_labels = False
SOLVED_BOARD = Solver.sudoku(BOARD_COPY)

VALUE_DICT = {}

#BACKTRACKING ALGORITHM STARTS
#For a more detailed explanation of the algorithm check Solver.py
def empty(puzzle):
    for x in range(9):
        for y in range(9):
            if puzzle[x][y].value == 0:
                return (x,y)
    return False

def valid(puzzle, num, coord):
    for x in range(len(puzzle[0])):
        if puzzle[coord[0]][x].value == num and coord[1] != x:
            return False

    for x in range(len(puzzle)):
        if puzzle[x][coord[1]].value == num and coord[0] != x:
            return False

    for x in range((coord[0]//3)*3, (coord[0]//3)*3 + 3):
        for y in range((coord[1]//3)*3, (coord[1]//3)*3 + 3):
            if num == puzzle[x][y].value and (x,y) != coord:
                return False
            
    return True
        

def solver_gui(puzzle):

    if not empty(puzzle):
        return True
    
    else:
        i, j = empty(puzzle)
        
    for m in range(1,10):
        if valid(puzzle, m, (i,j)):
            puzzle[i][j].value = m
            puzzle[i][j].font_color = RED
            time.sleep(0.05)
            draw_window()
            if solver_gui(puzzle):
                return True
            
            puzzle[i][j].value = 0
            puzzle[i][j].font_color = RED
            draw_window()  

    return False
#BACKTRACKING ALGORITHM ENDS


class Grid():
    selected_box = None

    def __init__(self, label, position, value, fixed, font_color, box_color):
        self.label = label
        self.position = position
        self.value = value
        self.fixed = fixed
        self.font_color = font_color
        self.box_color = box_color
        

    def change_box_color(self):
        if not Grid.selected_box:
            Grid.selected_box = self
            self.box_color = RED

        if self.label != Grid.selected_box.label:
            Grid.selected_box.box_color = BLACK
            Grid.selected_box = self
            self.box_color = RED

    def change_value(self,new_value):
        self.value = new_value
        

def score_update(right):
    global SCORE

    if right:
        SCORE += 100
        
    else:
        if SCORE != 0:
            SCORE -= 100

def game_over():
    GAME_OVER_FONT = pygame.font.SysFont('comicsans', 50)
    text = GAME_OVER_FONT.render('GAME OVER!',1,BLACK)
    WIN.blit(text,(80,200))
    pygame.display.update()

def draw_window():
    global filled_labels, VALUE_DICT, BOARD, GRID_GRID, SCORE

    WIN.fill(WHITE)
    i,j = 0,0
    grid_list = []

    for x in range(0,WIDTH,SIZE):
        for y in range(0,450,SIZE):
            BOX = pygame.Rect(x,y,SIZE,SIZE) 

            if not filled_labels:   #Filling up GRID_GRID, which is the board in the form of Grid class objects
                if BOARD[j][i]:
                    VALUE_DICT[str(BOX)] = Grid(BOX,(j,i),BOARD[j][i],True,BLACK,BLACK)
                else:
                    VALUE_DICT[str(BOX)] = Grid(BOX,(j,i),0,False,GREY,BLACK)

                i += 1
                
                grid_list.append(VALUE_DICT[str(BOX)])

                if len(grid_list) == 9:
                    GRID_GRID.append(grid_list)
                    i = 0
                    j += 1
                    grid_list = []
                
                if len(VALUE_DICT) == 81:
                    filled_labels = True

            if VALUE_DICT[str(BOX)].value:  #Drawing only the values which are not zero on GUI
                value_font = FONT.render(str(VALUE_DICT[str(BOX)].value), 1, VALUE_DICT[str(BOX)].font_color)
                WIN.blit(value_font, (BOX.x+20, BOX.y+10))

            
            pygame.draw.rect(WIN,VALUE_DICT[str(BOX)].box_color,BOX,1)
            
            

    #SOLVE BUTTON
    pygame.draw.rect(WIN,BLACK,SOLVE_BUTTON,1)
    solve_button_font = FONT.render('SOLVE', 1, BLACK)
    WIN.blit(solve_button_font, (SOLVE_BUTTON.x+20, SOLVE_BUTTON.y+10))

    #SCORE KEEPING
    score_button_font = FONT.render(f'SCORE:{SCORE}',1,BLACK)
    WIN.blit(score_button_font,(300,460))

    pygame.display.update()


def main():
    global VALUE_DICT, SOLVE_BUTTON, BOARD, GRID_GRID, SOLVED_BOARD, SCORE

    clock = pygame.time.Clock()
    solved = False

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                pos = pygame.mouse.get_pos()

                #Solve button clicked
                if SOLVE_BUTTON.collidepoint(pos):
                    for box in VALUE_DICT.values():
                        if not box.fixed:
                            box.value = 0
                    solved = True
                    solver_gui(GRID_GRID)
                    game_over()
                    time.sleep(3)
                    pygame.quit()

                #Random box clicked
                else:
                    for value in VALUE_DICT.values():
                        square = value.label
                        if square.collidepoint(pos):
                            if not value.fixed:
                                value.change_box_color()

            #Input value
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_value = 1

                if event.key == pygame.K_2:
                    new_value = 2

                if event.key == pygame.K_3:
                    new_value = 3

                if event.key == pygame.K_4:
                    new_value = 4

                if event.key == pygame.K_5:
                    new_value = 5

                if event.key == pygame.K_6:
                    new_value = 6

                if event.key == pygame.K_7:
                    new_value = 7

                if event.key == pygame.K_8:
                    new_value = 8

                if event.key == pygame.K_9:
                    new_value = 9

                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    new_value = 0

                if not Grid.selected_box.fixed:
                    Grid.selected_box.change_value(new_value)

            #Confirm input value
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    j,i = Grid.selected_box.position
                    if Grid.selected_box.value == SOLVED_BOARD[j][i]:
                        Grid.selected_box.font_color = GREEN
                        Grid.selected_box.fixed = True
                        score_update(True)
                    else:
                        Grid.selected_box.value = 0
                        score_update(False)

        draw_window()



if __name__ == '__main__':
    main()