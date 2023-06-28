import pygame, time, math
from utils import * #utils is a file created for this project, it contains some basic utility functions

#Setting Imgs for bg and characters
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"),0.9)
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"),0.55)
#Setting up display
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() #gets width and height of track img
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

#Setting FPS
FPS = 60

#abstract class for cars that act as parent class
class AbstractCar:
    IMG = RED_CAR
    START_POS = (180, 200)


    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS

    def rotate(self, left=False, right=False): #pass direction of rotation and then the rotation_vel withh change
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_img(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

class PlayerCar(AbstractCar):
    IMG = RED_CAR

def draw(win, imgs, player_car):
    for img, pos in imgs:
        win.blit(img, pos)
    player_car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
imgs =[(GRASS, (0,0)), (TRACK, (0,0))]
player_car = PlayerCar(4, 4)
while run:
    clock.tick(FPS)

    draw(WIN, imgs, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)