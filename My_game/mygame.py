import pygame
import random
from pygame.locals import *
from sys import exit

pygame.init()

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Collector")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

background_img = pygame.image.load("bg.jpg")
player_img = pygame.image.load("player_still.jpg")
coin_imgs = [pygame.image.load("coin.jpg"), pygame.image.load("coin1.jpg"), pygame.image.load("coin2.jpg"), pygame.image.load("coin3.jpg")]

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images_still = [pygame.image.load("player_still.jpg")]
        self.images_right = [pygame.image.load("player_right2.jpg"), pygame.image.load("player_right.jpg")]
        self.images_left = [pygame.image.load("player_left2.jpg"), pygame.image.load("player_left.jpg")]
        self.images_up = [pygame.image.load("player_up.jpg"), pygame.image.load("player_up2.jpg")]
        self.images_down = [pygame.image.load("player_down.jpg"), pygame.image.load("player_down2.jpg")]
        self.index = 0
        self.image = self.images_still[self.index]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.index = (self.index + 1) % len(self.images_left)
            self.image = self.images_left[self.index]
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.index = (self.index + 1) % len(self.images_right)
            self.image = self.images_right[self.index]
        elif keys[pygame.K_UP]:
            self.rect.y -= 5
            self.index = (self.index + 1) % len(self.images_up)
            self.image = self.images_up[self.index]
        elif keys[pygame.K_DOWN]:
            self.rect.y += 5
            self.index = (self.index + 1) % len(self.images_down)

        self.rect.clamp_ip(screen.get_rect())


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.image = coin_imgs[self.index]
        self.rect = self.image.get_rect(center=(random.randint(0, screen_width), random.randint(0, screen_height)))
        self.last_image_change = pygame.time.get_ticks()
        self.image_change_delay = 200  

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_image_change > self.image_change_delay:
            self.index = (self.index + 1) % len(coin_imgs)
            self.image = coin_imgs[self.index]
            self.last_image_change = current_time


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30)) 
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.speed = 5  
    def update(self):
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)
        self.rect.clamp_ip(screen.get_rect())


class Game:
    def __init__(self):
        self.player = Player()
        self.coins = pygame.sprite.Group()
        self.coins.add(Coin())
        self.enemies = pygame.sprite.Group() 
        for _ in range(3):
            self.enemies.add(Enemy()) 
        self.score = 0
        self.win = False
        self.game_over = False
        self.end_time = None

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

    def update(self, keys):
        if not self.win and not self.game_over:
            self.player.update(keys)

            self.coins.update()

            self.enemies.update()

            collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in collisions:
                self.score += 1
                self.coins.add(Coin())  

            if pygame.sprite.spritecollideany(self.player, self.enemies):
                self.game_over = True
                self.end_time = pygame.time.get_ticks()

            if self.score >= 15:
                self.win = True
                self.end_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(background_img, (0, 0))
        self.coins.draw(screen)
        self.enemies.draw(screen)
        screen.blit(self.player.image, self.player.rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.win:
            win_text = font.render("YOU WIN!", True, WHITE)
            screen.blit(win_text, (screen_width // 2 - 70, screen_height // 2))
        elif self.game_over:
            lose_text = font.render("YOU LOSE!", True, WHITE)
            screen.blit(lose_text, (screen_width // 2 - 70, screen_height // 2))

    def run(self):
        while True:
            self.process_events()

            keys = pygame.key.get_pressed()
            self.update(keys)

            self.draw(screen)
            pygame.display.flip()

            if self.win or self.game_over:
                if pygame.time.get_ticks() - self.end_time >= 2000:
                    pygame.quit()
                    exit()

            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
