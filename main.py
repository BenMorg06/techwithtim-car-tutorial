import pygame, time, math
from utils import * #utils is a file created for this project, it contains some basic utility functions

#Setting Imgs for bg and characters
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"),0.9)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_POS = (130,250)
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"),0.55)

#Setting up display
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() #gets width and height of track img
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

#Setting up masks for collision detection
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_MASK = pygame.mask.from_surface(FINISH)

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
        self.acceleration = 0.1

    def rotate(self, left=False, right=False): #pass direction of rotation and then the rotation_vel withh change
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_img(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) #min is used to prevent car from going over max vel; add self.acceleration to self.vel
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle) #converts degrees to radian
        vertical = math.cos(radians) * self.vel #calculates vertical movement
        horizontal = math.sin(radians) * self.vel #calculates horizontal movement
        self.y -= vertical
        self.x -= horizontal
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x),int(self.y-y)) #current x position minus x and y of other mask: This gets displacement between the masks
        poi = mask.overlap(car_mask, offset) #poi is the point of intersection
        return poi
    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
        
    def reduce_speed(self):
        self.vel = max(self.vel - 0.5*(self.acceleration), 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

#Drawing the images on the screen
def draw(win, imgs, player_car):
    for img, pos in imgs:
        win.blit(img, pos)
    player_car.draw(win)
    pygame.display.update()


#moving the car
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        player_car.move_forward()
        moved = True
    if keys[pygame.K_s]:
        player_car.move_backward()
        moved = True
    if not moved:
        player_car.reduce_speed()

run = True
clock = pygame.time.Clock()
imgs =[(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(8, 4)
while run:
    clock.tick(FPS)

    draw(WIN, imgs, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if finish_poi_collide !=None: # The asterisk is used to unpack the tuple
        if finish_poi_collide[1] ==0:
            player_car.bounce()
        else:
            print("finish")
            player_car.reset()

pygame.quit()