# Simple pygame program
# Import and initialize the pygame library
import random
from unittest import runner

from pygame.math import Vector2
import pygame
from PIL import Image, ImageFilter

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

pygame.init()


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Bowser.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.pos = Vector2(30, 10)
        self._layer = 2

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.pos += Vector2(0, -0.15)
        if pressed_keys[K_DOWN]:
            self.pos += Vector2(0, 0.15)
        if pressed_keys[K_LEFT]:
            self.pos += Vector2(-0.15, 0)
        if pressed_keys[K_RIGHT]:
            self.pos += Vector2(0.15, 0)
        # Keep player on the screen
        if self.pos.x < self.surf.get_width() / 2:
            self.pos.x = self.surf.get_width() / 2
        if self.pos.x > SCREEN_WIDTH - self.surf.get_width() / 2:
            self.pos.x = SCREEN_WIDTH - self.surf.get_width() / 2
        if self.pos.y < self.surf.get_height() / 2:
            self.pos.y = self.surf.get_height() / 2
        if self.pos.y > SCREEN_HEIGHT - self.surf.get_height() / 2:
            self.pos.y = SCREEN_HEIGHT - self.surf.get_height() / 2
        self.rect.center = self.pos


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self, sp_factor):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("mushroom.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.pos = Vector2(self.rect.center)
        self.speed = sp_factor * random.randint(1, 5)
        self._layer = 1

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.pos += Vector2(-self.speed, 0)
        self.rect.center = self.pos
        if self.rect.right < 0:
            self.kill()


# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.pos = Vector2(self.rect.center)
        self.speed = 0.1
        self._layer = 5

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.pos += Vector2(-self.speed, 0)
        self.rect.center = self.pos
        if self.rect.right < 0:
            self.kill()


def endScreen():
    global score
    # another game loop
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:  # if the user hits the mouse button
                    run = False

        # This will draw text displaying the score to the screen.
        largeFont = pygame.font.SysFont('comicsans', 80)  # creates a font object
        currentScore = largeFont.render('Score: ' + str(score), 1, (0, 0, 0))
        screen.blit(currentScore, (SCREEN_WIDTH / 2 - currentScore.get_width() / 2, 200))

        smallFont = pygame.font.SysFont('comicsans', 30)  # creates a font object
        playagain = smallFont.render('press space to play again', 1, (0, 0, 0))
        screen.blit(playagain, (SCREEN_WIDTH / 2 - playagain.get_width() / 2, 200 + currentScore.get_height()))
        pygame.display.update()
    score = 0


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create font for score
score = 0


def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, score
    font = pygame.font.SysFont('comicsans', 20, True)
    # Create a custom event for adding a new enemy
    respawn_timer = 1
    enemy_sp_factor = 0.03
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, int(600 - respawn_timer) + 1)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 2000)

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Variable to keep the main loop running
    running = True
    gameover = False

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    # Main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # print(pressed_keys[K_DOWN])
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(enemy_sp_factor)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                enemy_sp_factor = enemy_sp_factor * 1.01
                if respawn_timer < 200:
                    respawn_timer += 10
                elif respawn_timer < 449:
                    respawn_timer += 3
                pygame.time.set_timer(ADDENEMY, int(600 - respawn_timer))
                score += 1
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        # Update enemy position
        clouds.update()
        enemies.update()
        player.update(pressed_keys)

        text = font.render('Score: ' + str(score), 1, (0, 0, 0))
        # Fill the screen with white
        screen.fill((145, 90, 143))
        screen.blit(text, (SCREEN_WIDTH - 120, 10))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            gameover = True

        if gameover:
            pygame.time.set_timer(ADDENEMY, 0)
            running = False
            endScreen()
            main()
        pygame.display.flip()


main()
print(score)
