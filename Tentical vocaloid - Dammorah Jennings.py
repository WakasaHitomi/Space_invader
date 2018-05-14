# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Tentical Tactics"
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

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font('images/athena_of_the_ocean/Athena.ttf', 96)
FONT_XL = pygame.font.Font('images/teenage_fantasy_romance_novel/TEENAGEROMANCENOVEL.ttf', 96)

# Images

ship_img = pygame.image.load('images/player_ship-1.png')
laser_img = pygame.image.load('images/miku_bullets-1.png')
mob_img = pygame.image.load('images/squid-1.png')
bomb_img = pygame.image.load('images/tenticle-1.png')
mob2_img = pygame.image.load('images/octo-1.png')
bg_image = pygame.image.load('images/bg-1.png')




# Sounds
EXPLOSION = pygame.mixer.Sound('images/explosion.ogg')
ZAP = pygame.mixer.Sound('images/player-zap.ogg')
EW = pygame.mixer.Sound('images/squish.ogg')
SPLAT = pygame.mixer.Sound('images/splat.ogg')


L1_MUSIC = pygame.mixer.Sound('images/ia_am_theme.ogg')
START_MUSIC = pygame.mixer.Sound('images/ranma.ogg')
END_MUSIC = pygame.mixer.Sound('images/in_lull.ogg')

L1_MUSIC.play(-1)
# Stages
START = 0
PLAYING = 1
END = 2


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
        ZAP.play()

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            SPLAT.play()
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)

        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 910:
            self.rect.x = 910




class Laser(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5      

    def update(self):
        self.rect.y -= self.speed

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
        EW.play()

        

    def update(self, laser, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 150
            self.kill()
            


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()

        
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 3
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






class Fleet2:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 3
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

screen.blit(bg_image,(0, 0))

# Make game objects


ship = Ship(384, 536, ship_img)

mob1 = Mob(128, 64, mob_img)
mob2 = Mob(228, 64, mob_img)
mob3 = Mob(328, 64, mob_img)
mob4 = Mob(428, 64, mob_img)
mob5 = Mob(528, 64, mob_img)
mob6 = Mob(128, -64, mob_img)
mob7 = Mob(228, -64, mob_img)
mob8 = Mob(328, -64, mob_img)
mob9 = Mob(428, -64, mob_img)
mob10 = Mob(528, -64, mob_img)
mob11 = Mob(128, -164, mob2_img)
mob12 = Mob(228, -164, mob2_img)
mob13 = Mob(328, -164, mob2_img)
mob14 = Mob(428, -164, mob2_img)
mob15 = Mob(528, -164, mob2_img)
mob16 = Mob(128, -164, mob2_img)
mob17 = Mob(228, -164, mob2_img)
mob18 = Mob(328, -164, mob2_img)
mob19 = Mob(428, -164, mob2_img)
mob20 = Mob(528, -164, mob2_img)



mob20 = Mob(128, -220, mob2_img)
mob21 = Mob(228, -220, mob2_img)
mob22 = Mob(328, -220, mob2_img)
mob23 = Mob(428, -220, mob2_img)
mob24 = Mob(528, -220, mob2_img)
mob25 = Mob(628, -220, mob2_img)




# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15, mob16, mob17, mob18, mob19, mob20)

bombs = pygame.sprite.Group()
mobs.add(mob20, mob21, mob22, mob23, mob24, mob25)



fleet = Fleet(mobs)
fleet2 = Fleet2(mobs)


# set stage
stage = START

#Game Helper functions
def show_title_screen():
    screen.blit(bg_image,(0, 0))
    title_text = FONT_LG.render("Tentical Tactics!!!", 1, WHITE)
    screen.blit(title_text, [428, 204])
    

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

# Game loop



done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()


    
        closed = pressed[pygame.K_x]

        if closed:
            exit()
        


    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
        

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
       
    screen.blit(bg_image,(0, 0)) 
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
        
    
    # Update screen (Actually draw the picture in the window.)

    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
