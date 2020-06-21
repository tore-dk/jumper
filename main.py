import pygame
import time
import random
pygame.init()
width, height = 900, 1600
screen = pygame.display.set_mode((width, height))

global_downwards = 5

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
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def show(self):
        screen.blit(self.IMG, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

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

    def get_rect(self):
        return self.get_rect()


class Obstacle:
    def __init__(self):
        self.side = random.randint(1, 2)
        self.width = random.randint(100, 200)
        self.height = random.randint(50, 100)
        self.y = -self.height
        self.x = width - 100 - self.width if self.side == 1 else 100
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def show(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += global_downwards


class Score:
    def __init__(self):
        self.score_val = 0
        self.high_score = self.score_val

    def add_score(self):
        self.score_val += global_downwards/5
        if self.score_val > self.high_score:
            self.high_score = self.score_val

    def show(self):
        font_type = pygame.font.Font('freesansbold.ttf', 32)
        showing = font_type.render('Height: ' + str(self.score_val), True, (255, 255, 255))
        screen.blit(showing, (50, 50))


# CRATE OBSTACLES
ob_list = [Obstacle()]

# CREATE SCORE SYSTEM
score = Score()

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
    # CLICKING MOUSE
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1 and not man.in_motion:
        if (man.x == 100 and mouse_pos[0] > 100 + man.width/2) or (mouse_pos[0] < man.x == width - 100 - man.width):
            man.jump(mouse_pos[0] - man.x, mouse_pos[1] - man.y)
    # GENERAL SCREEN
    screen.fill((0, 10, 10))
    pygame.draw.rect(screen, (0, 0, 0), (width - 100, 0, 100, height))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, height))
    # OBSTACLES UPDATE
    for i in ob_list:
        # MOVE AND PREPARE NEXT OBJECT IF NEEDED
        i.move()
        if i.y > height:
            ob_list.remove(i)
        elif 100 + global_downwards >= i.y > 100:
            ob_list.append(Obstacle())
        # COLLISION
        if man.hitbox.colliderect(i.hitbox):
            running = False
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
    # SHOW SCORE
    score.add_score()
    score.show()

    pygame.display.update()
