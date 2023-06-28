import pygame, time, math

#Setting Imgs for bg and characters
GRASS = pygame.image.load("imgs/grass.jpg")
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = pygame.image.load("imgs/red-car.png")
GREEN_CAR = pygame.image.load("imgs/green-car.png")
#Setting up display
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() #gets width and height of track img
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")
