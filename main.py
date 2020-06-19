import pygame
import time
import math

pygame.init()
width, height = 900, 1600
screen = pygame.display.set_mode((width, height))

# MAIN CHARACTER


class HeroCharacter:
    def __init__(self, img='ball.png', x=None, y=None):
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
        self.velocity_y += dy/4
        self.velocity_x += dx/4

    def update_variables(self):
        self.velocity_y -= self.acceleration_y
        self.y += self.velocity_y
        self.x += self.velocity_x

    def show_pointer(self, end_pos):
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), end_pos)

    def hit_wall(self, side):
        self.velocity_y = 0
        self.velocity_x = 0
        self.in_motion = False
        if side == 1:
            self.x = 100
        else:
            self.x = width - 100 - self.width


# INITIATE MAIN CHARACTER AS MAN
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
        print('Hi')
        if (man.x == 100 and mouse_pos[0] > 100 + man.width) or (mouse_pos[0] < man.x == width - 100 - man.width):
            man.in_motion = True
            man.jump(mouse_pos[0] - man.x, mouse_pos[1] - man.y)
    # GENERAL SCREEN
    screen.fill((0, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), (width-100, 0, 100, height))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, height))
    # MAIN CHARACTER UPDATE
    # RESTART IF TOO LOW
    if man.y > height:
        man.__init__()
    if man.in_motion:
        man.update_variables()
    else:
        man.show_pointer(mouse_pos)
    # WALL DETECTION
    if man.x < 100:
        man.hit_wall(1)
    elif man.x > width - 100 - man.width:
        man.hit_wall(0)
    # SLOWLY FALLING
    man.y += 2
    man.show()

    pygame.display.update()

