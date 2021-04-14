import pygame
import os
import random
import math
import time
pygame.font.init()


class GameBoard:
    # #40 bomb 16x16 game of minesweeper

    # bomb_list = []
    
    # #randomly assigning grid placements that will have a bomb
    # for i in range(self.bombs):
    #     random_val = random.randint(0, 255)
        
    #     #making sure the bombs aren't on the same square
    #     while random_val in bomb_list:
    #         random_val = random.randint(0, 255)

    #     bomb_list.append(random_val)

    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # #changing the value in the board to 9 if bomb
    # for num_bombs in bomb_list:
    #     divRem = divmod(num_bombs, 16)
    #     board[divRem[0]][divRem[1]] = 9

    def __init__(self, rows, columns, width, height, bombs):
        bomb_list = []
        
        #randomly assigning grid placements that will have a bomb
        for i in range(bombs):
            random_val = random.randint(0, 255)
            
            #making sure the bombs aren't on the same square
            while random_val in bomb_list:
                random_val = random.randint(0, 255)

            bomb_list.append(random_val)

        #changing the value in the board to 9 if bomb
        for num_bombs in bomb_list:
            divRem = divmod(num_bombs, 16)
            self.board[divRem[0]][divRem[1]] = 9
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
                    if (j + 1 <= 15) and (self.board[i][j+1] != 9):
                        self.squares[i][j+1].number+= 1
                    #check square directly above bomb
                    if (i - 1 >= 0) and (self.board[i-1][j] != 9):
                        self.squares[i-1][j].number+= 1
                    #check square directly below bomb
                    if (i + 1 <= 15) and (self.board[i+1][j] != 9):
                        self.squares[i+1][j].number+= 1
                    #check square left up of bomb
                    if (j - 1 >= 0) and (i - 1 >= 0) and (self.board[i-1][j-1] != 9):
                        self.squares[i-1][j-1].number+= 1
                    #check square left down of bomb
                    if (j - 1 >= 0) and (i + 1 <= 15) and (self.board[i+1][j-1] != 9):
                        self.squares[i+1][j-1].number+= 1
                    #check square right up of bomb
                    if (j + 1 <= 15) and (i - 1 >= 0) and (self.board[i-1][j+1] != 9):
                        self.squares[i-1][j+1].number+= 1
                    #check square right down of bomb
                    if (j + 1 <= 15) and (i + 1 <= 15) and (self.board[i+1][j+1] != 9):
                        self.squares[i+1][j+1].number+= 1                    

    
    def leftClick(self, width, height):
        #finds the column and row
        if (WINDOW.get_height() > WINDOW.get_width()):
            findingCol = math.floor(width/(WINDOW.get_width()/16))
            findingRow = math.floor(height/(WINDOW.get_width()/16))
        else:
            findingCol = math.floor(width/(WINDOW.get_height()/16))
            findingRow = math.floor(height/(WINDOW.get_height()/16))
        print(self.board)

        # if ((findingCol > 16) or (findingRow > 16)):
        # If there is no flag
        if (self.squares[findingRow][findingCol].flag == False):
            #If there is a cover
            if (self.squares[findingRow][findingCol].cover == True):
                self.squares[findingRow][findingCol].cover = False
                #If the click is a bomb you lose
                if (self.board[findingRow][findingCol] == 9):
                    self.squares[findingRow][findingCol].win = False
                else:
                    print((findingRow, findingCol))
                    #self.squares[findingRow][findingCol].recurse = False
                    self.coverAlgo(findingRow, findingCol) 


    #algorithm that will uncover the squares that need to be uncovered in minesweeper
    def coverAlgo(self, row, column):
        print("hi")
        self.squares[row][column].recurse = True
        if (self.squares[row][column].number != 0):
            print("uncover")
            self.squares[row][column].cover = False
            return
        elif (self.squares[row][column].number == 0):
            self.squares[row][column].cover = False
            #left up
            if (column - 1 >= 0) and (row - 1 >= 0):
                if (self.squares[row-1][column-1].recurse != True):
                    self.squares[row-1][column-1].recurse = True
                    self.coverAlgo(row-1, column-1)
            #left down
            if (column - 1 >= 0) and (row + 1 <= 15):
                if (self.squares[row+1][column-1].recurse != True):
                    self.squares[row+1][column-1].recurse = True                
                    self.coverAlgo(row+1, column-1)
            #right up
            if (column + 1 <= 15) and (row - 1 >= 0):
                if (self.squares[row-1][column+1].recurse != True):
                    self.squares[row-1][column+1].recurse = True                
                    self.coverAlgo(row-1, column+1)
            #right down
            if (column +1 <= 15) and (row + 1 <= 15):
                if (self.squares[row+1][column+1].recurse != True):
                    self.squares[row+1][column+1].recurse = True                
                    self.coverAlgo(row+1, column+1)
            #direct left
            if (column - 1 >= 0):
                if (self.squares[row][column-1].recurse != True):
                    self.squares[row][column-1].recurse = True                
                    self.coverAlgo(row, column-1)
            #direct right
            if (column + 1 <= 15):
                if (self.squares[row][column+1].recurse != True):
                    self.squares[row][column+1].recurse = True                
                    self.coverAlgo(row, column+1)
            #direct up
            if (row - 1 >= 0):
                if (self.squares[row-1][column].recurse != True):
                    self.squares[row-1][column].recurse = True                
                    self.coverAlgo(row-1, column)
            #direct down
            if (row + 1 <= 15):
                if (self.squares[row+1][column].recurse != True):
                    self.squares[row+1][column].recurse = True                
                    self.coverAlgo(row+1, column)


    def rightClick(self, width, height):
        if (WINDOW.get_height() > WINDOW.get_width()):
            findingCol = math.floor(width/(WINDOW.get_width()/16))
            findingRow = math.floor(height/(WINDOW.get_width()/16))
        else:
            findingCol = math.floor(width/(WINDOW.get_height()/16))
            findingRow = math.floor(height/(WINDOW.get_height()/16))
        print(self.board)
        print(findingRow, findingCol)

        if not self.squares[findingRow][findingCol].flag:
            self.squares[findingRow][findingCol].flag = True
            self.all_flags += 1
            print(self.squares[findingRow][findingCol].flag)
        else:
            self.squares[findingRow][findingCol].flag = False
            self.all_flags -= 1
            print(self.squares[findingRow][findingCol].flag)

    # def finished(self):
    #     counter = 0 
    #     for row in range(16):
    #         for col in range(16):
    #             if (self.squares[row][col].cover == True):
    #                 counter += 1
    #     if (counter == 40):
    #         return True




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


    def location():
        #returns (a, b, c, d) where a, b is (width, width) 
        #and c, d is (height, height) of the square

        final_val = [width1, width2, height1, height2]

        #If window width > height
        if (WINDOW.get_width() > WINDOW.get_height()):
            #If on the first row we need to 
            width1 = (WINDOW.get_height()/16)*self.col
            width2 = row1 + (WINDOW.get_height()/16)
            height1 = (WINDOW.get_height()/16)*self.row
            height2 = height2 + (WINDOW.get_height()/16)
        else:
            width1 = (WINDOW.get_width()/16)*self.col
            width2 = row1 + (WINDOW.get_width()/16)
            height1 = (WINDOW.get_width()/16)*self.row
            height2 = height2 + (WINDOW.get_width()/16)
        return final_val






WIDTH, HEIGHT = 800, 1000
size = [WIDTH, HEIGHT]
#WINDOW = pygame.display.set_mode(size, pygame.RESIZABLE)
WINDOW = pygame.display.set_mode(size)
COVER = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper!")

GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
FPS = 60
BOX_DIM = 30
DIM = 16

BOMB_IMAGE = pygame.image.load(os.path.join('Assets', 'bomb.png'))
FLAG_IMAGE = pygame.image.load(os.path.join('Assets', 'flag_icon.png'))
BOMB = pygame.transform.scale(BOMB_IMAGE, (BOX_DIM, BOX_DIM))
FLAG = pygame.transform.scale(FLAG_IMAGE, (BOX_DIM, BOX_DIM))
COVER_IMAGE = pygame.image.load(os.path.join('Assets', 'Capture.PNG'))
COVER = pygame.transform.scale(COVER_IMAGE, (BOX_DIM, BOX_DIM))
LOSE_IMAGE = pygame.image.load(os.path.join('Assets', 'x.PNG'))
LOSE = pygame.transform.scale(LOSE_IMAGE, (BOX_DIM, BOX_DIM))
WIN_IMAGE = pygame.image.load(os.path.join('Assets', 'Win.jpg'))
WIN = pygame.transform.scale(WIN_IMAGE, (200, 200))

ONE = (0, 0, 255)
TWO = (0, 128, 0)
THREE = (255, 0, 0)
FOUR = (128, 0, 128)
FIVE = (128, 0, 0)
SIX = (64, 224, 208)
SEVEN = (0, 0, 0)
EIGHT = (255, 255, 0)

CLOCK = pygame.time.Clock()
START_TIME = time.time()
PAUSED = False
FONT = pygame.font.SysFont("Comic Sans", 32)


def numberGen(text, color):
    font = pygame.font.SysFont("comicsans", 50)
    number = font.render(str(text), 1, color)
    return number

def removeCover(gameboard):
    for rows in range(16):
        for cols in range(16):
            gameboard.squares[rows][cols].cover = False
            gameboard.squares[rows][cols].flag = False
            if (gameboard.board[rows][cols] == 9):
                gameboard.squares[rows][cols].win = False

def finished(gameboard):
    counter = 0 
    for row in range(16):
        for col in range(16):
            if (gameboard.squares[row][col].cover == True):
                counter += 1
    if (counter == gameboard.bombs):
        gameboard.you_won = True
        return True

def draw_window(width, height, board, gameboard, timer):
    WINDOW.fill(GRAY)
    total_flags = 0
    for rows in range(16):
        for cols in range(16):
            #Creates gridlines
            if (WINDOW.get_width() > WINDOW.get_height()):
                pygame.draw.rect(WINDOW, BLACK, ((WINDOW.get_height()/DIM)*rows, (WINDOW.get_height()/DIM)*cols, 
                    (WINDOW.get_height()/DIM), (WINDOW.get_height()/DIM)), 2)
                continue
            else:
                pygame.draw.rect(WINDOW, BLACK, ((WINDOW.get_width()/DIM)*rows, (WINDOW.get_width()/DIM)*cols, 
                    (WINDOW.get_width()/DIM), (WINDOW.get_width()/DIM)), 2)
            #Places the bombs
            if (board[rows][cols] == 9):
                WINDOW.blit(BOMB, (12.5+50*cols, 12.5+50*rows))
            #Place the numbers
            if (gameboard.squares[rows][cols].number != 0):
                if (gameboard.squares[rows][cols].number == 1):
                    text = numberGen(1, ONE)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))
                elif (gameboard.squares[rows][cols].number == 2):
                    text = numberGen(2, TWO)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))
                elif (gameboard.squares[rows][cols].number == 3):
                    text = numberGen(3, THREE)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))  
                elif (gameboard.squares[rows][cols].number == 4):
                    text = numberGen(4, FOUR)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))
                elif (gameboard.squares[rows][cols].number == 5):
                    text = numberGen(5, FIVE)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))  
                elif (gameboard.squares[rows][cols].number == 6):
                    text = numberGen(6, SIX)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))  
                elif (gameboard.squares[rows][cols].number == 7):
                    text = numberGen(7, SEVEN)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows))     
                elif (gameboard.squares[rows][cols].number == 8):
                    text = numberGen(8, EIGHT)
                    WINDOW.blit(text, (14.5+50*cols, 12.5+50*rows)) 

            #hit bomb
            if (gameboard.squares[rows][cols].win == False):
                WINDOW.blit(LOSE, (12.5+50*cols, 12.5+50*rows))
                removeCover(gameboard)

            #COVERS
            if (gameboard.squares[rows][cols].cover == True):
                WINDOW.blit(COVER, (12.5+50*cols, 12.5+50*rows))

            #Places the flags
            if (gameboard.squares[rows][cols].flag == True):
                WINDOW.blit(FLAG, (12.5+50*cols, 12.5+50*rows))
    #if win 
    if (finished(gameboard) == True):
        WINDOW.blit(WIN, (300, 350))  

    flag_count = FONT.render(str(gameboard.all_flags), 1, (0, 0, 0))
    WINDOW.blit(flag_count, (100, 900))

    #Timer
    WINDOW.blit(timer, (700, 900))
    pygame.display.update()


def main():
    #WINDOW = pygame.display.set_mode(size, pygame.RESIZABLE)
    WINDOW = pygame.display.set_mode(size)
    gameBoard = GameBoard(16, 16, WIDTH, HEIGHT, 1)
    board = gameBoard.board
    clock = pygame.time.Clock()
    on = True
    while on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #left MOUSE BUTTON
                    pos = event.pos
                    clicked = gameBoard.leftClick(pos[0], pos[1])

                elif event.button == 3:
                    #RIGHT MOUSE BUTTON
                    pos = event.pos
                    clicked = gameBoard.rightClick(pos[0], pos[1])
            if event.type == pygame.VIDEORESIZE:
                old_window = WINDOW
                WINDOW = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)



        if not gameBoard.you_won:
            timer = time.time() - START_TIME
            timer_text = FONT.render(str(int(timer)), 1, (0, 0, 0))
        draw_window(WIDTH, HEIGHT, board, gameBoard, timer_text)
        

if __name__ == '__main__':
    main()
    pygame.quit()
