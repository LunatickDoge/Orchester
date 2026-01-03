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
        "ability": "the rich",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Michal": {
        "health": 150,
        "attack": 69,
        "ability": "halfling",
        "ability_cooldown": 1,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Rome": {
        "health": 250,
        "attack": 69,
        "ability": "steal",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Squirtle": {
        "health": 44,
        "attack": 48,
        "ability": "squirt",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Pikachu": {
        "health": 35,
        "attack": 55,
        "ability": "shock",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Eevee": {
        "health": 55,
        "attack": 55,
        "ability": "Adapt",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Bulbasaur": {
        "health": 45,
        "attack": 49,
        "ability": "Poison",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
    "Charmander": {
        "health": 39,
        "attack": 52,
        "ability": "Burn",
        "ability_cooldown": 2,
        "image": pygame.image.load("assets/knut.png"),
    },
}
