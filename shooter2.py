import pygame

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


# Create the screen window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# Define the Soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

# Create player instances
player = Soldier(200, 200, 3)
player2 = Soldier(400, 200, 3)

# Clock for frame rate
clock = pygame.time.Clock()

# Game loop
run = True
while run:
    clock.tick(60)  # Set FPS to 60

    # Fill the screen with a background color (black here)
    screen.fill((0, 0, 0))

    # Draw players
    player.draw()
    player2.draw()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the display
    pygame.display.update()

pygame.quit()
