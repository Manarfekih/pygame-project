
import pygame
import os

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
#define player action variables
moving_left = False 
moving_right = False 
shoot = False 
grenade = False 
grenade_thrown = False 
#upload images 
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#grenade image 
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

#define colors
BG = (144 ,201 ,120)
RED= (255,0,0)
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED , (0, 300),(SCREEN_WIDTH, 300))


# Define the Soldier class
class Soldier(pygame.sprite.Sprite):
    #speed is the speed of player
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
    

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    
    def move(self ,moving_left ,moving_right):
        #to move the player moving the rectangle position with speed var
        #reset mouvement variable
        #predict player position using dx dy
        dx = 0
        dy = 0
        #assign mouvement variables if moving left or right
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
        #check collision with floor
        if self.rect.bottom + dy > 300 :
            dy = 300 - self.rect.bottom
            self.in_air = False

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction) #change player to self so it works for player and enemy 
            bullet_group.add(bullet)
            self.ammo -= 1 #ammo reduced by one 

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

    def update(self): #(how i want the bullets to be )
        #move bullet 
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check collision with characters 
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive: 
                player.health -= 5
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
        self.direction = direction
    
    def update (self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
    # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.vel_y = 0

    # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

    # collision with enemy
        if pygame.sprite.spritecollide(enemy, bullet_group, False):

            if enemy.alive:
                enemy.health -= 25
                self.kill()


    
#create Sprite groups 
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()


# Create player instances
player = Soldier('player',200, 200, 3 , 5 , 20 , 5)
enemy = Soldier('enemy',400, 200, 3 , 5 , 20 , 0)
# Clock for frame rate
clock = pygame.time.Clock()
# Game loop
run = True
while run:
    clock.tick(FPS)  # Set FPS to 60
    draw_bg()

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    #update and draw groups 
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)



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
        player.move(moving_left , moving_right)
        player.update_animation()
    

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
