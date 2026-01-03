import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        color = self.hovering_color if self.rect.collidepoint(position) else self.base_color
        self.text = self.font.render(self.text_input, True, color)

class Card:
    def __init__(self, name, stats, rect):
        self.name = name
        self.stats = stats
        self.rect = pygame.Rect(rect)
        self.selected = False

        self.base_color = (200, 200, 200)
        self.hover_color = (170, 220, 170)
        self.color = self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        pygame.draw.rect(screen, "black", self.rect, 2, border_radius=12)

        name_text = get_font(26).render(self.name, True, "black")
        screen.blit(name_text, name_text.get_rect(center=(self.rect.centerx, self.rect.y + 30)))

        y = 70
        for stat, value in self.stats.items():
            stat_text = get_font(20).render(f"{stat}: {value}", True, "black")
            screen.blit(stat_text, (self.rect.x + 15, self.rect.y + y))
            y += 28

        if self.selected:
            pygame.draw.rect(screen, "green", self.rect, 4, border_radius=12)

    def update(self, mouse_pos):
        self.color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class TeamSlot:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.card = None

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=12)
        pygame.draw.rect(screen, "black", self.rect, 2, border_radius=12)

        if self.card:
            name = get_font(22).render(self.card.name, True, "black")
            screen.blit(name, name.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# team slots
slot_w, slot_h = 160, 200
slot_spacing = 30
slot_x = (SCREEN_WIDTH - (4 * slot_w + 3 * slot_spacing)) // 2
slot_y = 100

deck_slots = [
    TeamSlot((slot_x + i * (slot_w + slot_spacing), slot_y, slot_w, slot_h))
    for i in range(4)
]

# cards
card_w, card_h = 260, 280
card_spacing = 40
card_x = (SCREEN_WIDTH - (4 * card_w + 3 * card_spacing)) // 2
card_y = SCREEN_HEIGHT // 2.8

cards = [
    Card("J.Knut", {"HP": 250, "ATK": 50, "Abilities": "", "1": "the rich"},
         (card_x + 0 * (card_w + card_spacing), card_y, card_w, card_h)),

    Card("Michal", {"HP": 150, "ATK": 69, "Abilities": "", "1": "halfling"},
         (card_x + 1 * (card_w + card_spacing), card_y, card_w, card_h)),

    Card("Rome", {"HP": 250, "ATK": 69, "Abilities": "", "1": "steal"},
         (card_x + 2 * (card_w + card_spacing), card_y, card_w, card_h)),

    Card("Squirtle", {"HP": 44, "ATK": 48, "Abilities": "", "1": "squirt"},
         (card_x + 3 * (card_w + card_spacing), card_y, card_w, card_h)),

    Card("Pikachu", {"HP": 35, "ATK": 55, "Abilities": "", "1": "shock"},
         (card_x + 0 * (card_w + card_spacing), card_y + SCREEN_HEIGHT // 3.6, card_w, card_h)),

    Card("Eevee", {"HP": 55, "ATK": 55, "Abilities": "", "1": "Adapt"},
         (card_x + 1 * (card_w + card_spacing), card_y + SCREEN_HEIGHT // 3.6, card_w, card_h)),

    Card("Bulbasaur", {"HP": 45, "ATK": 49, "Abilities": "", "1": "Poison"},
         (card_x + 2 * (card_w + card_spacing), card_y + SCREEN_HEIGHT // 3.6, card_w, card_h)),

    Card("Charmander", {"HP": 39, "ATK": 52, "Abilities": "", "1": "Burn"},
         (card_x + 3 * (card_w + card_spacing), card_y + SCREEN_HEIGHT // 3.6, card_w, card_h)),
]

#list of selected cards
team_cards = []
MAX_TEAM_SIZE = 4

#team menu
def options():
    while True:
        SCREEN.fill("white")
        mouse_pos = pygame.mouse.get_pos()

        title = get_font(55).render("Build Your Team", True, "black")
        SCREEN.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 40)))

        for slot in deck_slots:
            slot.draw(SCREEN)

        for card in cards:
            card.update(mouse_pos)
            card.draw(SCREEN)

        BACK_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
            text_input="BACK",
            font=get_font(60),
            base_color="black",
            hovering_color="orange"
        )

        BACK_BUTTON.changeColor(mouse_pos)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(mouse_pos):
                    return

                # add card
                for card in cards:
                    if card.clicked(mouse_pos) and not card.selected:
                        if len(team_cards) < MAX_TEAM_SIZE:
                            for slot in deck_slots:
                                if slot.card is None:
                                    slot.card = card
                                    card.selected = True
                                    team_cards.append(card)
                                    break

                # remove card
                for slot in deck_slots:
                    if slot.clicked(mouse_pos) and slot.card:
                        slot.card.selected = False
                        if slot.card in team_cards:
                            team_cards.remove(slot.card)
                        slot.card = None

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title = get_font(100).render("Pokemon ;)", True, "#b68f40")
        SCREEN.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)))

        NEW_GAME = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40),
                          "NEW GAME", get_font(50), "black", "orange")

        TEAM = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
                      "TEAM", get_font(50), "black", "orange")

        QUIT = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120),
                      "QUIT", get_font(50), "black", "orange")

        for btn in [NEW_GAME, TEAM, QUIT]:
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if TEAM.checkForInput(mouse_pos):
                    options()
                if QUIT.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
