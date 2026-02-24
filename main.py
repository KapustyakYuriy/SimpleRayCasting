import pygame
import math

class Player:
    def __init__(self, x, y, fov, angle, ren_dis, speed, turning_speed, height):
        self.x = x
        self.y = y
        self.fov = fov
        self.angle = angle
        self.ren_dis = ren_dis
        self.speed = speed
        self.turning_speed = turning_speed
        self.height = height

class Wall:
    def __init__(self, x1, y1, x2, y2, color, height):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.height = height

class Settings:
    def __init__(self, screen_height, screen_width, sky_color, floor_color, delta, accuracy, caption, gamma):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.sky_color = sky_color
        self.floor_color = floor_color
        self.delta = delta
        self.accuracy = accuracy
        self.caption = caption
        self.gamma = gamma

running = True
DEFAULT_WALL_COLOR = (255, 0, 0)
GREEN = (20, 225, 80)
RED = (255, 20, 20)
DEFAULT_WALL_HEIGHT = 700
#WALLS = [
#            Wall(-30.0, 0.0, 20.0, 30.0, GREEN, DEFAULT_WALL_HEIGHT),
#            Wall(20.0, 30.0, 40.0, -20.0, (52, 151, 228), DEFAULT_WALL_HEIGHT / 2 + 100),
#            Wall(40.0, -20.0, -30.0, -30.0, RED, DEFAULT_WALL_HEIGHT / 2 + 200),
#            Wall(-30.0, -30.0, -30.0, 0.0, RED, DEFAULT_WALL_HEIGHT / 2 + 300)
#        ]

WALLS = [
            Wall (0.0, 0.0, 200.0, 0.0, (255, 0, 0), 1000),
            Wall (200.0, 0.0, 200.0, 30.0, (0, 255, 0), 1100),
            Wall (200.0, 30.0, 30.0, 30.0, (0, 0, 255), 1200),
            Wall (30.0, 30.0, 30.0, 200.0, (255, 255, 0), 1100),
            Wall (30.0, 200.0, 60.0, 200.0, (255, 0, 255), 900),
            Wall (60.0, 200.0, 60.0, 60.0, (0, 255, 255), 950),
            Wall (60.0, 60.0, 180.0, 60.0, (128, 128, 0), 850),
            Wall (180.0, 60.0, 180.0, 120.0, (128, 0, 128), 900),
            Wall (180.0, 120.0, 100.0, 120.0, (0, 128, 128), 1000),
            Wall (100.0, 120.0, 100.0, 90.0, (128, 128, 128), 950),
            Wall (100.0, 90.0, 150.0, 90.0, (200, 100, 50), 900),
            Wall (150.0, 90.0, 150.0, 150.0, (50, 100, 200), 1100),
            Wall (150.0, 150.0, 10.0, 150.0, (100, 200, 100), 950),
            Wall (10.0, 150.0, 10.0, 10.0, (100, 50, 150), 800),
            Wall (10.0, 10.0, 0.0, 10.0, (255, 100, 50), 700)
        ]

pygame.init()
player = Player(0, 0, 90, 0, 30, 0.5, 1, 350)
settings = Settings(700, 1000, (0, 96, 128), (255, 204, 0), 100, 0.000001, "Ray casting", 0.3)
screen = pygame.display.set_mode((settings.screen_width - 1, settings.screen_height - 1))
clock = pygame.time.Clock()
pygame.display.set_caption(settings.caption)

def getAngle(alpha):
    return normalize(player.angle + player.fov / 2 - (player.fov * alpha) / settings.screen_width)

def PythagorasTheorem(x, y):
    dist = math.sqrt(x * x + y * y)
    return dist

def normalize(angle):
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle

def isForward(x, y, alpha):
    #calculate scalar product of (x - p.x, y - p.x) and (1, 0) vectors
    scalar = (x - player.x) * 1 + (y - player.y) * 0
    #if it is too near to player
    if PythagorasTheorem(x - player.x, y - player.y) == 0:
        return True
    beta = math.degrees(math.acos(scalar / (1 * PythagorasTheorem(x - player.x, y - player.y))))
    if min(beta, 360 - beta) == 90:
        if alpha == 90:
            return y > player.y
        else:
            return y < player.y
    elif min(abs(beta - alpha), abs(360 - beta - alpha)) < settings.accuracy:
        return True
    else:
        return False

def getDist(alpha):
    # y = k * x + b
    alpha = getAngle(alpha)
    k = math.tan(math.radians(alpha))
    b = player.y - player.x * k
    visible = []
    for i in range(len(WALLS)):
        x1 = WALLS[i].x1
        y1 = WALLS[i].y1
        x2 = WALLS[i].x2
        y2 = WALLS[i].y2
        x = 0
        y = 0
        if min(alpha, 360 - alpha) == 90 and x1 == x2:
            #if we need to draw edges of walls. Do something...
            x = player.ren_dis
            y = player.ren_dis
        elif min(alpha, 360 - alpha) == 90:
            c1 = (y1 * x2 - x1 * y2) / (x2 - x1)
            c2 = (y2 - y1) / (x2 - x1)
            x = player.x
            y = c2 * x + c1
        elif x1 == x2:
            x = x1
            y = k * x + b
        else:
            c1 = (y1 * x2 - x1 * y2) / (x2 - x1)
            c2 = (y2 - y1) / (x2 - x1)
            if(k == c2):
                #if we need to draw edges of walls. Do something...
                x = player.ren_dis
                y = player.ren_dis
            else:
                x = (c1 - b) / (k - c2)
                y = k * x + b
        if isForward(x, y, alpha) and PythagorasTheorem(x - x1, y - y1) + PythagorasTheorem(x - x2, y - y2) - PythagorasTheorem(x1 - x2, y1 - y2) < settings.accuracy:
            visible.append((PythagorasTheorem(x - player.x, y - player.y), WALLS[i]))
    visible.sort(key =  lambda x : x[0], reverse = True)
    return visible

def resize(dist):
    if dist >= player.ren_dis or dist < 1:
        return 0
    else:
        return 1 / dist

def recolor(resize, color):
    resize = settings.gamma + (1 - settings.gamma) * resize
    new_color = (color[0] * resize, color[1] * resize, color[2] * resize)
    return new_color

def gradiant(pos):
    coefficient = (pos - settings.screen_height / 2) / (settings.screen_height / 2) 
    return recolor(coefficient, settings.floor_color)

def drawFloor():
    y = settings.screen_height / 2
    while y < settings.screen_height:
        pygame.draw.rect(
            screen,
            gradiant(y),
            pygame.Rect(0, y, settings.screen_width, 1)
        )
        y += 1

def draw():
    drawFloor()
    x = 0
    while x < settings.screen_width:
        visibile_walls = getDist(x)
        for comp in visibile_walls:
            dist, wall = comp
            current_wall_color = wall.color
            current_wall_height = wall.height
            coefficient = resize(dist)

            top = settings.screen_height / 2 + coefficient * player.height - coefficient * wall.height

            pygame.draw.rect(
                screen, 
                recolor(coefficient, current_wall_color), 
                pygame.Rect(x, top, settings.screen_width / settings.delta, coefficient * current_wall_height)
            )

        
        x += settings.screen_width / settings.delta

def move():
    keys = pygame.key.get_pressed()  # This will give us a dictonary where each key has a value of 1 or 0. Where 1 is pressed and 0 is not pressed.

    #move left/right
    player.x += (keys[pygame.K_a] - keys[pygame.K_d]) * math.cos(math.radians(player.angle + 90)) * player.speed
    player.y += (keys[pygame.K_a] - keys[pygame.K_d]) * math.sin(math.radians(player.angle + 90)) * player.speed
    #move back/forth
    player.x += (keys[pygame.K_w] - keys[pygame.K_s]) * math.cos(math.radians(player.angle)) * player.speed
    player.y += (keys[pygame.K_w] - keys[pygame.K_s]) * math.sin(math.radians(player.angle)) * player.speed
    #turn around
    player.angle = normalize(player.angle + (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * player.turning_speed)



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    move()
    screen.fill(settings.sky_color)
    draw()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
