import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
PLAYER_SIZE = 50
WHITE, GREEN, RED, ORANGE, LIGHT_BLUE, BLACK, GRAY = (255, 255, 255), (0, 255, 0), (255, 0, 0), (255, 165, 0), (
    0, 255, 255), (0, 0, 0), (128, 128, 128)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)



class Unit(pygame.sprite.Sprite):
    def __init__(self, group, u_type):
        super().__init__(group)
        self.unit = u_type
        stats = units.get(u_type)
        self.image = pygame.transform.scale(stats["image"], (250, 500))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.damage = stats["damage"]
        self.ability = stats["ability"]
        self.ability_cooldown = stats["ability_cooldown"]

    def attack(self, target):
        target.health -= self.damage




units = {
    "J.Knut": {
        "health": 250,
        "attack": 50,
        "ability": "millionaire",
        "ability_cooldown": 2,

    },
    "Michal": {
        "health": 150,
        "attack": 69,
        "ability": "giant slayer",
        "ability_cooldown": 1,

    },
    "Rome": {
        "health": 250,
        "attack": 69,
        "ability": "steal",
        "ability_cooldown": 2,

    }
}