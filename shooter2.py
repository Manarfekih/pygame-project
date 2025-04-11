
import pygame
import os
import random

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
TILE_SIZE = 40
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
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction) #change player to self so it works for player and enemy 
            bullet_group.add(bullet)
            self.ammo -= 1 #ammo reduced by one 
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
                    self.vision.center = (self.rect.centerx + 75 * self.direction , self.rect.centery)
                    #if it gets to a certain place it goes back in the othe rdirection
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    #reduce the counter if it is idling
                    self.idling_counter -+ 1 
                    if self.idling_counter <= 0:
                        self.idling = False 



            
            




    


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
        #countdown timer for explosion
        self.timer -= 1
        if self.timer <= 0:
            #to do explosion get rid first of the gerenade
            self.kill()
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


#create Sprite groups 
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temp are create item boxes
item_box = ItemBox('Health', 100 , 260 )
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400 , 260 )
item_box_group.add(item_box)
item_box = ItemBox('Grenade', 500 , 260 )
item_box_group.add(item_box)


# Create player instances
player = Soldier('player',200, 200, 1.65 , 5 , 20 , 5)
health_bar = HealthBar(10,10 , player.health ,player.health)
enemy = Soldier('enemy',500, 200, 1.65 , 2 , 20 , 0)
enemy2 = Soldier('enemy',300, 300, 1.65 , 2 , 20 , 0)
#add enemy to enemy group
enemy_group.add(enemy)
enemy_group.add(enemy2)

# Clock for frame rate
clock = pygame.time.Clock()
# Game loop
run = True
while run:
    clock.tick(FPS)  # Set FPS to 60
    draw_bg()
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
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)



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
