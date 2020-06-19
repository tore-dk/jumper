import pygame
import time
import random
pygame.init()
width, height = 900, 1600
screen = pygame.display.set_mode((width, height))

global_downwards = 2

# MAIN CHARACTER


class HeroCharacter:
    def __init__(self, img='manStationary.png', x=None, y=None):
        self.IMG = pygame.image.load(img)
        self.IMG = pygame.transform.scale(self.IMG, (100, 100))
        self.velocity_y = 0
        self.velocity_x = 0
        self.acceleration_y = -15
        self.in_motion = False
        self.width = self.IMG.get_rect().width
        self.height = self.IMG.get_rect().height
        self.x = width - 100 - self.width if x is None else x
        self.y = height - 300 if y is None else y
        self.pointer_angle = 0

    def show(self):
        screen.blit(self.IMG, (self.x, self.y))

    def jump(self, dx, dy):
        self.velocity_y += dy / 4
        self.velocity_x += dx / 4
        self.in_motion = True

    def update_variables(self):
        self.velocity_y -= self.acceleration_y
        self.y += self.velocity_y
        self.x += self.velocity_x

    def show_pointer(self, end_pos):
        pygame.draw.line(screen, (255, 255, 255), (self.x + self.width/2, self.y + self.height/2), end_pos)

    def hit_wall(self, side):
        self.velocity_y = 0
        self.velocity_x = 0
        self.in_motion = False
        if side == 1:
            self.x = 100
            temp_img = pygame.image.load('manStationary.png')
            temp_img = pygame.transform.scale(temp_img, (100, 100))
            self.IMG = pygame.transform.flip(temp_img, True, False)
        else:
            self.x = width - 100 - self.width
            self.IMG = pygame.image.load('manStationary.png')
            self.IMG = pygame.transform.scale(self.IMG, (100, 100))


class Obstacle:
    def __init__(self, side, wide, high, state=False):
        self.width = wide
        self.height = high
        self.y = -self.height
        self.state = state
        if side == 1:
            self.x = width - 100 - self.width
        else:
            self.x = 100

    def show(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += global_downwards


obstacle_count = 8
ob_list = []
for i in range(obstacle_count):
    ob_side = random.randint(1, 2)
    ob_width = random.randrange(10, 50)
    ob_height = random.randrange(50, 400)
    ob_list.append(Obstacle(ob_side, ob_width, ob_height))
ob_list[0].state = True

# INITIATE MAIN CHARACTER AS man
man = HeroCharacter()

running = True
while running:
    time.sleep(.05)
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1 and not man.in_motion:
        if (man.x == 100 and mouse_pos[0] > 100 + man.width) or (mouse_pos[0] < man.x == width - 100 - man.width):
            man.jump(mouse_pos[0] - man.x, mouse_pos[1] - man.y)
    # GENERAL SCREEN
    screen.fill((0, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), (width - 100, 0, 100, height))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, height))
    # OBSTACLES UPDATE
    for i in ob_list:
        # CHECK FOR COLLISION
        if i.state:
            i.move()
        if i.y > 100:
            temp = ob_list.index(i)
            ob_list[temp-1].state = True
        if i.x + i.width > man.x > i.x:
            if i.y + i.height > man.y > i.y:
                print('you lost')
        i.show()

    # MAIN CHARACTER UPDATE
    # RESTART IF TOO LOW
    if man.y > height:
        man.__init__()
    if man.in_motion:
        man.update_variables()
        man.IMG = pygame.image.load('manMotion.png')
        man.IMG = pygame.transform.scale(man.IMG, (100, 100))
        if man.velocity_x < 0:
            man.IMG = pygame.transform.flip(man.IMG, True, False)
    else:
        man.show_pointer(mouse_pos)
    # WALL DETECTION
    if man.x < 100:
        man.hit_wall(1)
    elif man.x > width - 100 - man.width:
        man.hit_wall(0)
    # SLOWLY FALLING
    man.y += global_downwards
    man.show()

    pygame.display.update()
