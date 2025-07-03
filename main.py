import pygame
from Engine.chess import *
from Engine.AI.defaultAI import *


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
running = True
dt = 0

newGame = Game( screen, clock, font)
newGame.StartGame()
newGame.PlayGame()



