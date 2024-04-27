import pygame
from game import Game


if __name__ == "__main__":
    win = pygame.display.set_mode((800, 600))       # Cria a janela do display.
    rpg = Game(win)                                 # Cria o jogo, com a janela.
    pygame.init()                                   # Inicia o display.
    rpg.run()                                       # Loop infinito do jogo.
