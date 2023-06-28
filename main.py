import pygame, time, math
from utils import * #utils is a file created for this project, it contains some basic utility functions
pygame.font.init() #initalise font


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

#Font object
MAIN_FONT = pygame.font.SysFont("Verdana", 44)

#Setting FPS
FPS = 60

#Computer car path
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

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
        self.vel = -self.vel/2
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150,200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
    
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (0,255,0), point, 5)
        
    def draw(self,win):
        super().draw(win)
        #self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
        
        if target_y > self.y:
            desired_radian_angle += math.pi
        
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360
        
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            self.rotate(right=True)

        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
            self.rotate(left=True)
        
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level-1)*0.2
        self.current_point = 0

    def move(self):
        if self.current_point >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

#Drawing the images on the screen
def draw(win, imgs, player_car, computer_car):
    for img, pos in imgs:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (255,255,255))
    win.blit(level_text, (10,HEIGHT-level_text.get_height()-70))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255,255,255))
    win.blit(time_text, (10,HEIGHT-time_text.get_height()-40))

    vel_text = MAIN_FONT.render(f"Velocity: {round(player_car.vel, 1)}px/s", 1, (255,255,255))
    win.blit(vel_text, (10,HEIGHT-vel_text.get_height()-10))

    player_car.draw(win)
    computer_car.draw(win)
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

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POS)
    if computer_finish_poi_collide !=None:
        blit_text_center(WIN,MAIN_FONT, f"You lost! ")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if player_finish_poi_collide !=None: # The asterisk is used to unpack the tuple
        if player_finish_poi_collide[1] ==0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)

run = True
clock = pygame.time.Clock()
imgs =[(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(4, 3)
computer_car = ComputerCar(2, 3, PATH)
game_info = GameInfo()
while run:
    clock.tick(FPS)

    draw(WIN, imgs, player_car, computer_car)

    while not game_info.started:
        blit_text_center(WIN,MAIN_FONT, f"Press any key to start level {game_info.level}")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    computer_car.move()
    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN,MAIN_FONT, f"You won! ")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()


pygame.quit()