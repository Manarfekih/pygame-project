import pygame
#s the sound module of Pygame. 
from pygame import mixer 
import os
import random
import csv
import button

mixer.init()
pygame.init()


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


# Create the screen window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


#limit  the game speed (set framerate)
clock = pygame.time.Clock()
FPS = 60

#define game variables 
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False


#define player action variables
moving_left = False 
moving_right = False 
shoot = False 
grenade = False 
grenade_thrown = False

#load music and sounds 
#pygame.mixer.music.load('audio/music2.mp3')
#pygame.mixer.music.set_volume(0.3)
#pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('sounds/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('sounds/grenade.wav')
grenade_fx.set_volume(0.05)


#button image 
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
#upload images
pine1_img = pygame.image.load('background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('background/mountain.png').convert_alpha()
sky_img = pygame.image.load('background/sky_cloud.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES) :
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img ,(TILE_SIZE,TILE_SIZE))
    img_list.append(img)
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade image 
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
#pick up boxes 
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
#dict to save pic boxes
item_boxes = {
    'Health' : health_box_img,
    'Ammo' : ammo_box_img ,
    'Grenade' : grenade_box_img 
}


#define colors
BG = (144 ,201 ,120)
RED= (255,0,0)
WHITE= (255,255,255)
GREEN= (0 , 255, 0)
BLACK = (0 ,0 , 0)
PINK = (235, 65, 54)



#define font
font = pygame.font.SysFont('Futura', 30)
#display texts
def draw_text(text, font ,text_col , x, y):
    #turn text into image
    img = font.render(text, True, text_col)
    #display the image
    screen.blit(img, (x ,y))
def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#function to reset level
def reset_level():
    #delete all the instance of the sprites
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    #reset world data reloaded from beginning 
    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data





# Define the Soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed , ammo , grenades):
        pygame.sprite.Sprite.__init__(self)
        #playing some action only when the player is alive
        self.alive = True
        #player or enemi use to load the relevant image
        self.char_type = char_type
        #assign the variable to the instance (for all players)
        self.speed = speed
        self.ammo = ammo #will be reduced evrytime i shoot 
        self.start_ammo = ammo #how many times i can shoot 
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100 #for health 
        self.max_health = self.health 
         #win m9bal lplayer 1=right
        self.direction = 1
        #velocity of the jump
        self.vel_y = 0
        self.jump = False
        #the player is in the air
        self.in_air = True
        #tekleb lplayer ki yemshi aal isar
        self.flip = False
        #pictures list animated
        self.animation_list = []
        #index of list
        self.frame_index = 0 
        self.action = 0 
        self.update_time = pygame.time.get_ticks()
        #ai variables
        self.move_counter = 0
        self.vision = pygame.Rect(0 ,0 ,150 ,20)
        self.idling = False
        self.idling_counter = 0


        #load all images for player
        animation_types =['idle' , 'Run' , 'jump' , 'death']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #how many pic in folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                #acces the relevant photo if it is enemy or player
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img= pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                #to not overright the picture you just passed and store it 
                #store img in temproray list
                temp_list.append(img)
                #create a list of list to put idle and run
            self.animation_list.append(temp_list)
        #starting with the first image/define which list you need to access run or idle
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    
    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0
    # To move the player, moving the rectangle position with speed var
    # Reset movement variables
        if moving_left:
            dx = -self.speed
            self.flip = True     
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        #avoid double jump
        if self.jump == True and self.in_air == False:
            #negative because the y coord when you jump you go in - y direction
            self.vel_y = -11
            #after jump
            self.jump = False
            self.in_air = True
        #apply gravity
        self.vel_y += GRAVITY
        #limit velocity
        if self.vel_y > 10:
            self.vel_y 
        dy += self.vel_y
        #check for collision 
        for tile in world.obstacle_list:
            #check collision in x direction 
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #if the ai has hit a wall then make it turn around
            if self.char_type == 'enemy':
                self.direction *= -1
                self.move_counter = 0
            #check collision in y direction 
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below ground, i.e jumping 
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above ground , i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        #check for collision with water 
        #allows to check between sprite and a grp
        if pygame.sprite.spritecollide(self, water_group , False):
            self.health = 0 

        #check for collision with exit
        #collide with icon for the next level
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group , False):
           level_complete = True

        #check iffallen of the map
         #player coordinates goes beyond screen height
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0 



        #check if going off the edges of the screen 
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0 

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
            or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll , level_complete

   

          

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction) #change player to self so it works for player and enemy 
            bullet_group.add(bullet)
            self.ammo -= 1 #ammo reduced by one 
            shot_fx.play()
    #make the enemies move
    def ai(self):
        if self.alive and player.alive:
            #stop a bit after running
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#idle
                self.idling = True
                #idle only for certain amount of time
                self.idling_counter = 50 
            #check if the enemy see the player
            if self.vision.colliderect(player.rect):
                #stop running face the player
                self.update_action(0)#0:idle 
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    #facing to the right
                    if self.direction == 1 :
                        ai_moving_right =True
                    else:
                        ai_moving_right =False
                        #avoid error of moving different directio at the same time
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left,ai_moving_right)
                    self.update_action(1)#1:run
                    #make enemies move in distance
                    self.move_counter += 1
                    #update ai vision as the enmy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    #if it gets to a certain place it goes back in the othe rdirection
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    #reduce the counter if it is idling
                    self.idling_counter -= 1 
                    if self.idling_counter <= 0:
                        self.idling = False
        #scroll
        self.rect.x += screen_scroll



        #move to the next animation pic after a specified time
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image =self.animation_list[self.action][self.frame_index]
        #know what time has passed by checking the current time put the last update time into now
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() 
            self.frame_index += 1
            #reset animation back to the start after 5 images(don't go beyon the list)
        #check if the frames exist
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
               self.frame_index = len(self.animation_list[self.action]) - 1
            else:
               self.frame_index = 0
 



    #see if there is new action and update correctly example run idle death
    def update_action(self,new_action):
        #check if the current action is different from the previous one 
        if new_action != self.action:
            #(if the current action is different from new action then we update it)
            self.action = new_action
            #update the animation settings (make sure animation starts from start not halfway)
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
 


    def draw(self):
        #define self.flip on the x axe ,false for y axe
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        #to look for collision with obstacles seperatly
        self.obstacle_list = []
        #data is world data
    def process_data(self ,data):
        self.level_length = len(data[0])
        #iterate each value in level file
        for y , row in enumerate(data):
            for x ,tile in enumerate(row):
                #-1 means no pic empty
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    #tile size help if you change the size of the screen you(ll still find the same rectangles)
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    #tuple storing pirticular tile
                    tile_data = (img, img_rect)
                    #dirt blocks are obstacles
                    #tile data is the tuple 
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img,x * TILE_SIZE, y * TILE_SIZE )
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img,x * TILE_SIZE, y * TILE_SIZE )
                        decoration_group.add(decoration)
                    elif tile == 15 :#create player
                        # Create player instances
                        player = Soldier('player',x * TILE_SIZE, y * TILE_SIZE, 1.65 , 5 , 20 , 5)
                        health_bar = HealthBar(10,10 , player.health ,player.health)
                    elif tile == 16 :
                        enemy = Soldier('enemy',x * TILE_SIZE, y * TILE_SIZE, 1.65 , 2 , 20 , 0)
                        #add enemy to enemy group
                        enemy_group.add(enemy)
                    elif tile == 17:#create ammo box
                        item_box = ItemBox('Ammo',x * TILE_SIZE, y * TILE_SIZE )
                        item_box_group.add(item_box)
                    elif tile == 18:#create ammo box
                        item_box = ItemBox('Grenade',x * TILE_SIZE, y * TILE_SIZE )
                        item_box_group.add(item_box)
                    elif tile == 19:#create ammo box
                        item_box = ItemBox('Health',x * TILE_SIZE, y * TILE_SIZE )
                        item_box_group.add(item_box)
                    elif tile == 20 :#exit
                        exit = Exit(img,x * TILE_SIZE, y * TILE_SIZE )
                        exit_group.add(exit)
        return player , health_bar
            
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

            #0 image 1 rect
            screen.blit(tile[0],tile[1])    

class Decoration (pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        self.rect.x += screen_scroll


class Water (pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        self.rect.x += screen_scroll



class Exit (pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.rect.topleft = (x, y)


class ItemBox (pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        #the rectangle is doing all the mouvement not the image
        self.rect = self.image.get_rect()
        #positioning on the x it's the center on y it's the top because the boxes are not big
        self.rect.midtop = (x + TILE_SIZE // 2 , y + (TILE_SIZE - self.image.get_height()))



    def update(self):
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self , player):
            #check what kind of box picked
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3 
            #delete item box after picked 
            self.kill()


class HealthBar():
    def __init__(self,x , y ,health , max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    #update health bar (draw rectangle) and update health if decreased on increased
    def draw(self , health):
        #update with new healt
        self.health = health
        #calculate ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen , BLACK , (self.x - 2 ,self.y - 2, 154 , 24))
        pygame.draw.rect(screen , RED , (self.x ,self.y , 150 , 20))
        #green bar
        #ratio =health / max health 
        pygame.draw.rect(screen , GREEN , (self.x ,self.y , 150 * ratio , 20))
        


#create bullet class and we need to use sprite classes
class Bullet (pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        #x,y to know the emplacement of the bullet (direction for left and right)
        pygame.sprite.Sprite.__init__(self)
        #define class variables 
        self.speed = 10 #we did not put speed in init because we do not want the speed to vary
        self.image = bullet_img
        self.rect=self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
    # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
    # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
    # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check collision with characters 
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive: 
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            # collision with enemy
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

        
class Grenade (pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7 
        self.image = grenade_img
        self.rect=self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
    
    def update (self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        #check collision with level 
        for tile in world.obstacle_list:
            #check with collision with walls 
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
             #check collision in y direction 
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below ground, i.e throw up 
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above ground , i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
    
    
        # update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        #countdown timer for explosion
        self.timer -= 1
        if self.timer <= 0:
            #to do explosion get rid first of the gerenade
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x,self.rect.y , 0.5)
            explosion_group.add(explosion)
            #do damage to anyone near by
            #count distance and see if the player in the radius damage it 
            #we subtract values of center of grenade and center of player compare it to the explosion radius (distance defined)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50



    

#do explosion at a certain time
class Explosion (pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1,6):
            #load images of exploision , convert alpha:preserve pic with transperncy keep like smoke glowing edges...
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img , (int(img.get_width() * scale),int(img .get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.center = (x,y)
        #controle the animation cool down and move to the second animation instead of time for sequences
        self.counter = 0    
    #handle the explosion
    def update(self):

        #scroll
        self.rect.x += screen_scroll
        #define the speed of animation
        EXPLOSION_SPEED = 4
        #update explosion animation 
        self.counter += 1 
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0 
            self.frame_index += 1
            #if the animation is complete then delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete

#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)
#create button
start_button = button.Button(SCREEN_WIDTH // 2 -130 ,SCREEN_HEIGHT // 2 - 150 , start_img , 1)
exit_button = button.Button(SCREEN_WIDTH // 2 -110 ,SCREEN_HEIGHT // 2 + 50 , exit_img , 1)
restart_button = button.Button(SCREEN_WIDTH // 2 -100 ,SCREEN_HEIGHT // 2 - 50 , restart_img , 2)
#create Sprite groups 
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


#create empty tile list 
world_data = []
#16 rows
for row in range(ROWS):
    #create a list with 150 entries of -1 (one row)
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    #extract indvidual tiles
    for x, row in enumerate(reader):
        for y , tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player,health_bar = world.process_data(world_data)



# Clock for frame rate
clock = pygame.time.Clock()
# Game loop
run = True
while run:
    

    clock.tick(FPS)  # Set FPS to 60
    if start_game == False :
        screen.fill(BG)
        #add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()
        #show player health 
        health_bar.draw(player.health)
        #show ammo
        draw_text('Ammo: ',font , WHITE , 10 , 35 )
        for x in range(player.ammo):
            #as x increases the bullet goes to the right side
            screen.blit(bullet_img, (90 + (x * 10), 40 ))
        draw_text('Grenades: ',font , WHITE , 10 , 60 )
        for x in range(player.grenades):
            #as x increases the bullet goes to the right side
            screen.blit(grenade_img, (135 + (x * 15), 60 ))
        
        player.update()
        player.draw()


        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        #update and draw groups 
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            #shoot bullet 
            if shoot:
                player.shoot()
            #throw grenades 
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
                grenade_group.add(grenade)
                #reduce grenades 
                player.grenades -= 1
                grenade_thrown = True 
            if player.in_air:
                player.update_action(2)#2:jump
            #update player action
            #if your clicking it runs else it's stable
            elif moving_left or moving_right:
                #action for run is 1 idle is 0
                player.update_action(1)
            else:
                player.update_action(0)
            #move players
            #player.move(moving_left , moving_right)
            screen_scroll , level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if player completed level
            if level_complete:
                start_intro = True
                level += 1 
                bg_scroll = 0 
                #delete instance and reload level
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        #extract indvidual tiles
                        for x, row in enumerate(reader):
                            for y , tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player,health_bar = world.process_data(world_data)
        else:
            #stop any kind scrolling when player dies
            screen_scroll = 0 
            if restart_button.draw(screen):
                #total amount of scroll/put everything to start
                death_fade.fade_counter = 0
                start_intro = True
                bg_scroll = 0 
                #delete instance and reload level
                world_data = reset_level()
                #load in level data and create world
                #run after restart
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    #extract indvidual tiles
                    for x, row in enumerate(reader):
                        for y , tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player,health_bar = world.process_data(world_data)



        

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #control if the player goes left or right
        #ketboard presses(pressing any key on the keyboard)
        #a left d right
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            #exit game thro escape button(not working yet)
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button release (ki tnahi sob3ek mel clavier)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False 
            



    # Update the display
    pygame.display.update()

pygame.quit()
