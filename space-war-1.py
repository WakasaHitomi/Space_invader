# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Neko War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LAVENDER = (195, 141, 239)
PINK = (255, 186, 233)
PURPLE = (99, 45, 226)

# Images

ship_img = pygame.image.load('images/player_ship-1.png')
laser_img = pygame.image.load('images/miku_bullets.png')
mob_img = pygame.image.load('images/squid-1.png')
bomb_img = pygame.image.load('images/tenticle-1.png')



# Sounds
'''EXPLOSION = pygame.mixer.Sound('sounds/explosion.ogg')'''

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 3
        self.shield = 5

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        print("POOM!")

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True,pygame.sprite.collide_mask)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)

        if len(hit_list) > 0:
            self.shield

        if self.shield == 0:
            '''EXPLOSION.play()'''
            self.kill()

class Laser(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5      

    def update(self):
        self.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self, laser):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            '''EXPLOSION.play()'''
            self.kill()
            


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()


    
# Make game objects

ship = Ship(384, 536, ship_img)
mob1 = Mob(128, 64, mob_img)
mob2 = Mob(128, 64, mob_img)
mob3 = Mob(128, 64, mob_img)


# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)

lasers = pygame.sprite.Group()

mobs = pygame.sprite.GroupSingle()
mobs.add(mob1, mob2, mob3)

bombs = pygame.sprite.Group()



fleet = Fleet(mobs)



# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        ship.move_left()
    elif pressed[pygame.K_RIGHT]:
        ship.move_right()

    
    closed = pressed[pygame.K_x]

    if closed:
        exit()
        


    # Game logic (Check for collisions, update points, etc.)
    player.update(bombs)
    lasers.update()   
    mobs.update(lasers)
    bombs.update()
    fleet.update()

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
