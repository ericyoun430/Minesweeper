import pygame
import os
import random

#https://github.com/techwithtim/Sudoku-GUI-Solver

class Game:
    #40 bomb 16x16 game of minesweeper

    bomb_list = []
    
    #randomly assigning grid placements that will have a bomb
    for i in range(40):
        random_val = random.randint(0, 255)
        
        #making sure the bombs aren't on the same square
        while random_val in bomb_list:
            random_val = random.randint(0, 255)

        bomb_list.append(random_val)

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


    #changing the value in the board to 1 if bomb
    for bombs in bomb_list:
        divRem = divmod(bombs, 16)
        board[divRem[0]][divRem[1]] = 1




























WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper!")

GRAY = (128, 128, 128)
FPS = 60
BOX_DIM = 10
BOMB_IMAGE = pygame.image.load(os.path.join('Assets', 'bomb.png'))
FLAG_IMAGE = pygame.image.load(os.path.join('Assets', 'flag_icon.png'))
BOMB = pygame.transform.scale(BOMB_IMAGE, (BOX_DIM, BOX_DIM))
FLAG = pygame.transform.scale(FLAG_IMAGE, (BOX_DIM, BOX_DIM))

def draw_window():
    WINDOW.fill(GRAY)
    WINDOW.blit(BOMB, (100, 200))
    WINDOW.blit(FLAG, (300, 200))
    pygame.display.update()

def main():


    clock = pygame.time.Clock()
    on = True
    while on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #LEFT MOUSE BUTTON
                    print(event.pos)
                elif event.button == 3:
                    #RIGHT MOUSE BUTTON
                    print(event.pos)
        draw_window()

if __name__ == '__main__':
    main()
    pygame.quit()
