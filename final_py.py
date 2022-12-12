# import modules
import pygame
import random

# imports pygame locals for key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# screen size
width = 800
height = 600
window = pygame.display.set_mode((width,height))

bg_img = pygame.image.load('background.jpg')
bg_img = pygame.transform.scale(bg_img,(width,height))



# creates player object
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.image.load("player.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # moves sprites based on key pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = height
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = width


# creates enemy object
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("rock.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
        self.speed = random.randint(4, 10)

# moves sprite based off speed and removes enemies when they reach the left
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

# creates screen
screen = pygame.display.set_mode((width, height))

# event to add enemy
AddEnemy = pygame.USEREVENT + 1
pygame.time.set_timer(AddEnemy, 250)

# player
player = Player1()

# groups to hold sprites
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# keeps our main loop running

running = True

# main loop
while running:
    window.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # ends loop if closed
        elif event.type == QUIT:
            running = False

        # adds new enemy
        elif event.type == AddEnemy:
            # creates new enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # gets user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update enemy position
    enemies.update()

    # draws sprite
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # if enemy collides with player, kills game
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # flips game display
    pygame.display.flip()
