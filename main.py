import pygame
import time
import random
import math
pygame.init()
width, height = 900, 1600
screen = pygame.display.set_mode((width, height))

global_downwards = 0
global_gravity = -10

# MAIN CHARACTER


high_score = 0
class HeroCharacter:
    def __init__(self):
        global high_score
        self.high_score = high_score
        self.size = 150
        self.movingIMG = pygame.image.load('movingHero.png')
        self.movingIMG = pygame.transform.scale(self.movingIMG, (self.size, self.size))
        self.stationaryIMG = pygame.image.load('stationaryHero.png')
        self.stationaryIMG = pygame.transform.scale(self.stationaryIMG, (self.size, self.size))
        self.IMG = self.stationaryIMG
        self.velocity_y = 0
        self.velocity_x = 0
        self.acceleration_y = global_gravity
        self.in_motion = False
        self.width = self.IMG.get_rect().width
        self.height = self.IMG.get_rect().height
        self.starting_y = height - 600
        self.x = width - 100 - self.width
        self.y = self.starting_y
        self.pointer_angle = 0
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.score = 0

    def show(self):
        screen.blit(self.IMG, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self, dx, dy):
        self.velocity_y += dy / 6
        self.velocity_x += dx / 6
        self.in_motion = True

    def update_variables(self):
        self.y += global_downwards
        self.velocity_y -= self.acceleration_y
        self.y += self.velocity_y
        self.x += self.velocity_x
        self.score -= int(self.velocity_y/(self.width/2))
        if self.high_score < self.score:
            self.high_score = self.score

    def show_pointer(self, end_pos):
        pygame.draw.line(screen, (255, 255, 255), (self.x + self.width/2, self.y + self.height/2), end_pos)

    def hit_wall(self, side):
        self.velocity_y = 0
        self.velocity_x = 0
        self.in_motion = False
        if side == 1:
            self.x = 100
            self.IMG = pygame.transform.flip(self.stationaryIMG, True, False)
        else:
            self.x = width - 100 - self.width
            self.IMG = self.stationaryIMG

    def show_score(self):
        font_type = pygame.font.Font('freesansbold.ttf', 32)
        score_show = font_type.render('Height: ' + str(self.score), True, (255, 255, 255))
        high_score_show = font_type.render('High Score: ' + str(self.high_score), True, (255, 255, 255))
        hs_width = high_score_show.get_rect().width
        screen.blit(score_show, (50, 50))
        screen.blit(high_score_show, (width - 50 - hs_width, 50))


ob_img_list = ['balcony.png', 'balcony1.png', 'balcony2.png', 'balcony3.png']


class Obstacle:
    def __init__(self):
        self.img_place = random.randint(0, len(ob_img_list))
        self.IMG = pygame.image.load(ob_img_list[self.img_place - 1])
        self.side = random.randint(1, 2)
        self.width = random.randint(100, 200)
        self.height = random.randint(200, 500)
        self.y = -self.height
        self.x = width - 100 - self.width if self.side == 1 else 100
        self.hitbox = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)
        self.deploy_ready = True

    def show(self):
        self.IMG = pygame.transform.scale(self.IMG, (self.width, self.height))
        screen.blit(self.IMG, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += global_downwards


class Lava:
    def __init__(self):
        self.IMG = pygame.image.load('lava.png')
        self.IMG = pygame.transform.scale(self.IMG, (width, height))
        self.x = 0
        self.y = height
        self.width = self.IMG.get_rect().width
        self.height = self.IMG.get_rect().height
        self.velocity = -5
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height) 

    def move(self):
        self.y -= self.velocity
        self.y += global_downwards
        if self.y > height + 200:
            self.y = height + 200

    def show(self):
        screen.blit(self.IMG, (self.x, self.y))


class Wall:
    def __init__(self, side_left, y):
        self.IMG = pygame.image.load('wall.png')
        self.side_left = side_left
        if side_left:
            self.x = 100 - 512
        else:
            self.x = width - 100
        self.y = y
        self.deploy_ready = True

    def move(self):
        self.y += global_downwards

    def show(self):
        screen.blit(self.IMG, (self.x, self.y))

gaming = True
while gaming:
    # CREATE WALLS
    wall_list = [Wall(True, height - 512), Wall(False, height - 512)]

    # CREATE LAVA
    lava = Lava()

    # CRATE OBSTACLES
    ob_list = [Obstacle()]

    # INITIATE MAIN CHARACTER AS man
    try: 
        high_score = man.high_score
    except NameError:
        pass
    man = HeroCharacter()
    
    running = True
    while running:
        time.sleep(.02)
        # SHOW FROM PREVIOUS ITERATION
        # GENERAL SCREEN
        screen.fill((0, 50, 30))
        pygame.draw.rect(screen, (0, 0, 0), (width - 100, 0, 100, height))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, height))
        for i in wall_list:
            i.show()
        # SHOW OBSTACLES
        for i in ob_list:
            i.show()
        # CALCULATE LAVA VELOCITY
        lava.velocity = math.log(man.score + 1) * 4 
        # LAVA MOVEMENT
        lava.move()
        lava.show()
        # SHOW MAN
        man.show()
        # SHOW SCORE
        man.show_score()
        # MOUSE PLACE AND SHOW POINTER
        mouse_pos = pygame.mouse.get_pos()
        if not man.in_motion:
            man.show_pointer(mouse_pos)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # QUITTING GAME
                running = False
                gaming = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # QUITTING GAME
                    running = False
                    gaming = False
        # CLICKING MOUSE
        if pygame.mouse.get_pressed()[0] == 1 and not man.in_motion:
            if (man.x == 100 and mouse_pos[0] > 100 + man.width/2) or (width - 100 - man.width == man.x > mouse_pos[0] - man.width/2):
                man.jump(mouse_pos[0] - (man.x + man.width/2), mouse_pos[1] - (man.y + man.height/2))

        # WALL UPDATE
        for i in wall_list:
            if i.y > 0 and i.deploy_ready:
                wall_list.append(Wall(i.side_left, i.y - 512))
                i.deploy_ready = False
            i.move()

        # OBSTACLES UPDATE
        for i in ob_list:
            # MOVE AND PREPARE NEXT OBJECT IF NEEDED
            i.move()
            if i.y > height:
                ob_list.remove(i)
            elif i.y > 500 and i.deploy_ready:
                ob_list.append(Obstacle())
                i.deploy_ready = False
            # COLLISION
            if man.hitbox.colliderect(i.hitbox):
                running = False

        # MAIN CHARACTER UPDATE
        man.update_variables()
        # LAVA DETETCION
        if (man.y + man.height) >= lava.y:
            running = False
        # WALL DETECTION
        if man.x < 100:
            man.hit_wall(1)
        elif man.x > width - 100 - man.width:
            man.hit_wall(0)
        if not(height - man.height > man.y > 0):
            running = False
        if man.in_motion:
            man.acceleration_y = global_gravity
            man.IMG = man.movingIMG
            if man.velocity_x < 0:
                man.IMG = pygame.transform.flip(man.IMG, True, False)
        else:
            man.acceleration_y = 0
            man.velocity_y = 0
            man.velocity_x = 0


        # "CAMERA" MOVEMENT
        camera_off = man.starting_y - man.y
        global_downwards = camera_off / 5 if camera_off > 0 else 0

        pygame.display.update()
