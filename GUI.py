import pygame
import os
import random
import math
import time
import sys
import pygame_menu
pygame.font.init()


class GameBoard:
    def __init__(self, rows, columns, width, height, bombs):
        self.board = []
        self.rows = rows
        self.columns = columns

        for i in range(self.rows):
            col_list = []
            for j in range(self.columns):
                col_list.append(0)
            self.board.append(col_list)


        bomb_list = []
        
        #randomly assigning grid placements that will have a bomb
        for i in range(bombs):
            random_val = random.randint(0, self.rows*self.columns-1)
            
            #making sure the bombs aren't on the same square
            while random_val in bomb_list:
                random_val = random.randint(0, self.rows*self.columns-1)

            bomb_list.append(random_val)

        #changing the value in the board to 9 if bomb
        for num_bombs in bomb_list:

            divRem = divmod(num_bombs, columns)
            self.board[divRem[0]][divRem[1]] = 9


        self.clicked_bomb = False
        self.all_flags = 0
        self.you_won = False
        self.bombs = bombs
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.squares = [[Square(self.board[i][j], i, j) 
            for j in range(columns)] for i in range(rows)]

        # setting the number for each square
        for i in range(rows):
            for j in range(columns):
                if (self.board[i][j] == 9):
                    #check square directly left of bomb
                    if (j - 1 >= 0) and (self.board[i][j-1] != 9):
                        self.squares[i][j-1].number+= 1
                    #check square directly right of bomb
                    if (j + 1 <= (self.columns - 1)) and (self.board[i][j+1] != 9):
                        self.squares[i][j+1].number+= 1
                    #check square directly above bomb
                    if (i - 1 >= 0) and (self.board[i-1][j] != 9):
                        self.squares[i-1][j].number+= 1
                    #check square directly below bomb
                    if (i + 1 <= (self.rows - 1)) and (self.board[i+1][j] != 9):
                        self.squares[i+1][j].number+= 1
                    #check square left up of bomb
                    if (j - 1 >= 0) and (i - 1 >= 0) and (self.board[i-1][j-1] != 9):
                        self.squares[i-1][j-1].number+= 1
                    #check square left down of bomb
                    if (j - 1 >= 0) and (i + 1 <= (self.rows - 1)) and (self.board[i+1][j-1] != 9):
                        self.squares[i+1][j-1].number+= 1
                    #check square right up of bomb
                    if (j + 1 <= (self.columns - 1)) and (i - 1 >= 0) and (self.board[i-1][j+1] != 9):
                        self.squares[i-1][j+1].number+= 1
                    #check square right down of bomb
                    if (j + 1 <= (self.columns - 1)) and (i + 1 <= (self.rows - 1)) and (self.board[i+1][j+1] != 9):
                        self.squares[i+1][j+1].number+= 1                    

    
    def leftClick(self, width, height, gameboard):
        #finds the column and row
        if (WINDOW.get_height() > WINDOW.get_width()):
            findingCol = math.floor(width/(WINDOW.get_width()/self.columns))
            findingRow = math.floor(height/(WINDOW.get_width()/self.columns))
        else:
            findingCol = math.floor(width/(WINDOW.get_height()/self.rows))
            findingRow = math.floor(height/(WINDOW.get_height()/self.rows))
        if (findingCol < gameboard.columns) and (findingRow < gameboard.rows):
        # If there is no flag
            if (self.squares[findingRow][findingCol].flag == False):
                #If there is a cover
                if (self.squares[findingRow][findingCol].cover == True):
                    self.squares[findingRow][findingCol].cover = False
                    #If the click is a bomb you lose
                    if (self.board[findingRow][findingCol] == 9):
                        self.squares[findingRow][findingCol].win = False
                        self.clicked_bomb = True
                    else:
                        self.coverAlgo(findingRow, findingCol, gameboard) 


        # # If there is no flag
        # if (self.squares[findingRow][findingCol].flag == False):
        #     #If there is a cover
        #     if (self.squares[findingRow][findingCol].cover == True):
        #         self.squares[findingRow][findingCol].cover = False
        #         #If the click is a bomb you lose
        #         if (self.board[findingRow][findingCol] == 9):
        #             self.squares[findingRow][findingCol].win = False
        #             self.clicked_bomb = True
        #         else:
        #             self.coverAlgo(findingRow, findingCol, gameboard) 


    #algorithm that will uncover the squares that need to be uncovered in minesweeper
    def coverAlgo(self, row, column, gameboard):
        self.squares[row][column].recurse = True
        if (self.squares[row][column].number != 0):
            self.squares[row][column].cover = False
            return
        elif (self.squares[row][column].number == 0):
            self.squares[row][column].cover = False
            #left up
            if (column - 1 >= 0) and (row - 1 >= 0):
                if (self.squares[row-1][column-1].recurse != True):
                    self.squares[row-1][column-1].recurse = True
                    self.coverAlgo(row-1, column-1, gameboard)
            #left down
            if (column - 1 >= 0) and (row + 1 <= (gameboard.rows - 1)):
                if (self.squares[row+1][column-1].recurse != True):
                    self.squares[row+1][column-1].recurse = True                
                    self.coverAlgo(row+1, column-1, gameboard)
            #right up
            if (column + 1 <= (gameboard.columns - 1)) and (row - 1 >= 0):
                if (self.squares[row-1][column+1].recurse != True):
                    self.squares[row-1][column+1].recurse = True                
                    self.coverAlgo(row-1, column+1, gameboard)
            #right down
            if (column +1 <= (gameboard.columns - 1)) and (row + 1 <= (gameboard.rows - 1)):
                if (self.squares[row+1][column+1].recurse != True):
                    self.squares[row+1][column+1].recurse = True                
                    self.coverAlgo(row+1, column+1, gameboard)
            #direct left
            if (column - 1 >= 0):
                if (self.squares[row][column-1].recurse != True):
                    self.squares[row][column-1].recurse = True                
                    self.coverAlgo(row, column-1, gameboard)
            #direct right
            if (column + 1 <= (gameboard.columns - 1)):
                if (self.squares[row][column+1].recurse != True):
                    self.squares[row][column+1].recurse = True                
                    self.coverAlgo(row, column+1, gameboard)
            #direct up
            if (row - 1 >= 0):
                if (self.squares[row-1][column].recurse != True):
                    self.squares[row-1][column].recurse = True                
                    self.coverAlgo(row-1, column, gameboard)
            #direct down
            if (row + 1 <= (gameboard.rows - 1)):
                if (self.squares[row+1][column].recurse != True):
                    self.squares[row+1][column].recurse = True                
                    self.coverAlgo(row+1, column, gameboard)


    def rightClick(self, width, height, gameboard):

        if (WINDOW.get_height() > WINDOW.get_width()):
            findingCol = math.floor(width/(WINDOW.get_width()/self.columns))
            findingRow = math.floor(height/(WINDOW.get_width()/self.columns))
        else:
            findingCol = math.floor(width/(WINDOW.get_height()/self.rows))
            findingRow = math.floor(height/(WINDOW.get_height()/self.rows))

        if (findingCol < gameboard.columns) and (findingRow < gameboard.rows):
            if not self.squares[findingRow][findingCol].flag:
                self.squares[findingRow][findingCol].flag = True
                self.all_flags += 1
            else:
                self.squares[findingRow][findingCol].flag = False
                self.all_flags -= 1

class Square:
    def __init__(self, value, row, col):
        self.win = True
        self.value = value
        self.row = row
        self.col = col
        self.flag = False
        self.number = 0
        self.bomb = False
        self.cover = True
        self.recurse = False







WIDTH, HEIGHT = 800, 1000
size = [WIDTH, HEIGHT]
WINDOW = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper!")

GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
FPS = 60

ONE = (0, 0, 255)
TWO = (0, 128, 0)
THREE = (255, 0, 0)
FOUR = (128, 0, 128)
FIVE = (128, 0, 0)
SIX = (64, 224, 208)
SEVEN = (0, 0, 0)
EIGHT = (255, 255, 0)

FONT = pygame.font.SysFont("Comic Sans", 32)

def numberGen(text, color, gameboard):
    font = pygame.font.SysFont("comicsans", int(WIDTH/gameboard.columns))
    number = font.render(str(text), 1, color)
    return number

def removeCover(gameboard):
    for rows in range(gameboard.rows):
        for cols in range(gameboard.columns):
            gameboard.squares[rows][cols].cover = False
            gameboard.squares[rows][cols].flag = False
            if (gameboard.board[rows][cols] == 9):
                gameboard.squares[rows][cols].win = False

def finished(gameboard):
    counter = 0 
    for row in range(gameboard.rows):
        for col in range(gameboard.columns):
            if (gameboard.squares[row][col].cover == True):
                counter += 1
    if (counter == gameboard.bombs):
        gameboard.you_won = True
        return True

def draw_window(width, height, board, gameboard, timer):
    WINDOW.fill(GRAY)
    total_flags = 0
    square_dist = WIDTH/gameboard.columns
    start_dist = (WIDTH/gameboard.columns)/4
    cover_dist = (WIDTH/gameboard.columns)/5
    for rows in range(gameboard.rows):
        for cols in range(gameboard.columns):
            pygame.draw.rect(WINDOW, BLACK, ((WINDOW.get_width()/gameboard.columns)*cols, (WINDOW.get_width()/gameboard.columns)*rows, 
                (WINDOW.get_width()/gameboard.columns), (WINDOW.get_width()/gameboard.columns)), 2)
            #Places the bombs
            if (board[rows][cols] == 9):
                WINDOW.blit(BOMB, (start_dist + square_dist*cols, start_dist + square_dist*rows))
            #Place the numbers
            if (gameboard.squares[rows][cols].number != 0):
                if (gameboard.squares[rows][cols].number == 1):
                    text = numberGen(1, ONE, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))
                elif (gameboard.squares[rows][cols].number == 2):
                    text = numberGen(2, TWO, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))
                elif (gameboard.squares[rows][cols].number == 3):
                    text = numberGen(3, THREE, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))  
                elif (gameboard.squares[rows][cols].number == 4):
                    text = numberGen(4, FOUR, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))
                elif (gameboard.squares[rows][cols].number == 5):
                    text = numberGen(5, FIVE, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))  
                elif (gameboard.squares[rows][cols].number == 6):
                    text = numberGen(6, SIX, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))  
                elif (gameboard.squares[rows][cols].number == 7):
                    text = numberGen(7, SEVEN, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows))     
                elif (gameboard.squares[rows][cols].number == 8):
                    text = numberGen(8, EIGHT, gameboard)
                    WINDOW.blit(text, (start_dist+square_dist*cols, start_dist+square_dist*rows)) 

            #hit bomb
            if (gameboard.squares[rows][cols].win == False):
                WINDOW.blit(LOSE, (start_dist+square_dist*cols, start_dist+square_dist*rows))
                removeCover(gameboard)

            #COVERS
            if (gameboard.squares[rows][cols].cover == True):
                WINDOW.blit(COVER, (cover_dist+square_dist*cols, cover_dist+square_dist*rows))

            #Places the flags
            if (gameboard.squares[rows][cols].flag == True):
                WINDOW.blit(FLAG, (start_dist+square_dist*cols, start_dist+square_dist*rows))
    #if win 
    if (finished(gameboard) == True):
        WINDOW.blit(WIN_PIC, ((WIDTH/2) - 100, WIDTH/2))  

    #reset button change
    if (gameboard.clicked_bomb == True):
        WINDOW.blit(DEAD, ((WIDTH/2) - 25, HEIGHT - 75))
    else:
        WINDOW.blit(SUNGLASSES, ((WIDTH/2) - 25, HEIGHT - 75))

    flag_count = FONT.render(str(gameboard.all_flags), 1, (0, 0, 0))
    WINDOW.blit(flag_count, (WIDTH - (WIDTH - 100), HEIGHT - 100))

    #Timer
    WINDOW.blit(timer, (WIDTH - 100, HEIGHT - 100))
    pygame.display.update()


def set_difficulty(text, bombs, rows, columns):
    #set global 
    global BOMBS
    global ROWS
    global COLS
    global COVER
    global BOMB
    global FLAG
    global LOSE
    global WIN_PIC
    global SUNGLASSES
    global DEAD
    global DIM 

    BOMBS = bombs
    ROWS = rows
    COLS = columns


    BOX_DIM = int((WIDTH/COLS)/2)
    COVER_DIM = int((WIDTH/COLS)/1.5)
    DIM = 16


    bomb_image = pygame.image.load(os.path.join('Assets', 'bomb.png'))
    flag_image = pygame.image.load(os.path.join('Assets', 'flag_icon.png'))
    BOMB = pygame.transform.scale(bomb_image, (BOX_DIM, BOX_DIM))
    FLAG = pygame.transform.scale(flag_image, (BOX_DIM, BOX_DIM))
    cover_image = pygame.image.load(os.path.join('Assets', 'Capture.PNG'))
    COVER = pygame.transform.scale(cover_image, (COVER_DIM, COVER_DIM))
    lose_image = pygame.image.load(os.path.join('Assets', 'x.PNG'))
    LOSE = pygame.transform.scale(lose_image, (BOX_DIM, BOX_DIM))
    win_image = pygame.image.load(os.path.join('Assets', 'Win.jpg'))
    WIN_PIC = pygame.transform.scale(win_image, (200, 200))
    sunglasses_image = pygame.image.load(os.path.join('Assets', 'happy_smile.jpg'))
    SUNGLASSES = pygame.transform.scale(sunglasses_image, (50, 50))
    dead_image = pygame.image.load(os.path.join('Assets', 'dead_smile.png'))
    DEAD = pygame.transform.scale(dead_image, (50, 50))
    start()

def start():
    gameBoard = GameBoard(ROWS, COLS, WIDTH, HEIGHT, BOMBS)
    board = gameBoard.board
    clock = pygame.time.Clock()
    start_time = time.time()
    font = pygame.font.SysFont("Comic Sans", 32)
    on = True
    while on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #left MOUSE BUTTON
                    pos = event.pos
                    if ((pos[0] < ((WIDTH/2) + 25)) and (pos[0] > ((WIDTH/2) - 25))):
                        if (pos[1] > HEIGHT - 75) and (pos[1] < HEIGHT - 25):
                            main()
                    clicked = gameBoard.leftClick(pos[0], pos[1], gameBoard)

                elif event.button == 3:
                    #RIGHT MOUSE BUTTON
                    pos = event.pos
                    clicked = gameBoard.rightClick(pos[0], pos[1], gameBoard)

        if (gameBoard.you_won == False) and (gameBoard.clicked_bomb == False):
            timer = time.time() - start_time
            timer_text = FONT.render(str(int(timer)), 1, (0, 0, 0))
        draw_window(WIDTH, HEIGHT, board, gameBoard, timer_text)

def menu():
    menu = pygame_menu.Menu("Minesweeper", 500, 400)
    menu.add.selector("Difficulty:", [("Easy", 10, 10, 10), ("Intermediate", 40, 16, 16),
    ("Expert", 99, 16, 30)], onreturn = set_difficulty)
    menu.mainloop(WINDOW)

def main():
    
    WINDOW = pygame.display.set_mode(size)
    menu()

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
