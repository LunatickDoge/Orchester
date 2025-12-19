import pygame
import sys
import Main

pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Team", True, "Green")
        OPTIONS_TEXT2 = get_font(30).render("1. 👅.", True, "Black")
        OPTIONS_TEXT3 = get_font(30).render("2. idk", True, "Black")
        OPTIONS_TEXT4 = get_font(30).render("3. ;)", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
        OPTIONS_RECT3 = OPTIONS_TEXT3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 150))
        OPTIONS_RECT4 = OPTIONS_TEXT4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 250))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)
        SCREEN.blit(OPTIONS_TEXT4, OPTIONS_RECT4)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()




def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Pokemon;)", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 - 50))

        button_width = 300
        button_height = 80
        play_rect = pygame.image.load("assets/Play_Rect.png")
        play_rect = pygame.transform.scale(play_rect, (450, button_height))
        options_rect = pygame.image.load("assets/Options_Rect.png")
        options_rect = pygame.transform.scale(options_rect, (400, button_height))
        quit_rect = pygame.image.load("assets/Quit_Rect.png")
        quit_rect = pygame.transform.scale(quit_rect, (button_width, button_height))

        button_spacing = 30
        start_y = SCREEN_HEIGHT // 2 - 50

        NEW_GAME_BUTTON = Button(image=play_rect, pos=(SCREEN_WIDTH // 2, start_y + button_height + button_spacing),
                                 text_input="NEW GAME", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        OPTIONS_BUTTON = Button(image=options_rect,
                                pos=(SCREEN_WIDTH // 2, start_y + (button_height + button_spacing) * 2),
                                text_input="TEAM", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=quit_rect, pos=(SCREEN_WIDTH // 2, start_y + (button_height + button_spacing) * 3),
                             text_input="QUIT", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
