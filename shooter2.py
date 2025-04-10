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

#game variables
GRAVITY = 0.75

#define player action variables
moving_left = False 
moving_right = False 

#define colors
BG = (144 ,201 ,120)
RED= (255,0,0)
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED , (0, 300),(SCREEN_WIDTH, 300) )


# Define the Soldier class
class Soldier(pygame.sprite.Sprite):
    #speed is the speed of player
    def __init__(self,char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        #playing some action only when the player is alive
        self.alive = True
        #player or enemi use to load the relevant image
        self.char_type = char_type
        #assign the variable to the instance (for all players)
        self.speed = speed
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
        animation_types =['idle' , 'Run' , 'jump']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #how many pic in folder
            num_of_frames = len(os.listdir(f'{self.char_type}\{animation}'))
            for i in range(num_of_frames):
                #acces the relevant photo if it is enemy or player
                img = pygame.image.load(f'{self.char_type}\{animation}\{i}.png')
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
            #reset the frames to 0
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
            
    def draw(self):
        #define self.flip on the x axe ,false for y axe
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Create player instances
player = Soldier('player',200, 200, 3 , 5)
enemy = Soldier('enemy',400, 200, 3 , 5)


# Clock for frame rate
clock = pygame.time.Clock()

# Game loop
run = True
while run:
    clock.tick(FPS)  # Set FPS to 60
    
    draw_bg()

   
    player.update_animation()
    # Draw players
    player.draw()
    enemy.draw()
    if player.alive:
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
            



    # Update the display
    pygame.display.update()

pygame.quit()
