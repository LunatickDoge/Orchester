import pygame
import sys
import socket
import Battle

pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = SCREEN.get_size()
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(
    pygame.image.load("assets/background.png"),
    (W, H)
)

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def quit_game():
    pygame.quit()
    sys.exit()

class Button:
    def __init__(self, text, pos, size, base, hover):
        self.text = text
        self.font = get_font(size)
        self.base = base
        self.hover = hover
        self.pos = pos
        self.render()

    def render(self):
        self.image = self.font.render(self.text, True, self.base)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen, mouse):
        color = self.hover if self.rect.collidepoint(mouse) else self.base
        self.image = self.font.render(self.text, True, color)
        screen.blit(self.image, self.rect)

    def clicked(self, mouse):
        return self.rect.collidepoint(mouse)

def pokedex_index():
    pokemon_data = [
        {
            "name": "Charmander", 
            "hp": 40, "atk": 8, "type": "Fire",
            "color": (255, 100, 50),
            "img": pygame.transform.scale(pygame.image.load("assets/charmanderFront.png"), (150, 150))
        },
        {
            "name": "Bulbasaur", 
            "hp": 60, "atk": 4, "type": "Grass",
            "color": (100, 200, 100),
            "img": pygame.transform.scale(pygame.image.load("assets/bulbasaurFront.png"), (150, 150))
        },
        {
            "name": "Squirtle", 
            "hp": 50, "atk": 4, "type": "Water",
            "color": (100, 150, 255),
            "img": pygame.transform.scale(pygame.image.load("assets/squirtleFront.png"), (150, 150))
        }
    ]
    
    back_btn = Button("BACK", (W // 2, H - 80), 45, "black", "orange")

    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(70).render("POKEDEX", True, "orange")
        SCREEN.blit(title, title.get_rect(center=(W // 2, 80)))

        card_w, card_h = 450, 530
        spacing = 110
        start_x = (W - (3 * card_w + 2 * spacing)) // 2

        for i, p in enumerate(pokemon_data):
            rect = pygame.Rect(start_x + i * (card_w + spacing), 180, card_w, card_h)
            pygame.draw.rect(SCREEN, p["color"], rect, border_radius=20)
            pygame.draw.rect(SCREEN, "black", rect, 4, border_radius=20)

            img_rect = p["img"].get_rect(center=(rect.centerx, rect.y + 120))
            SCREEN.blit(p["img"], img_rect)

            name_txt = get_font(45).render(p["name"], True, "black")
            SCREEN.blit(name_txt, name_txt.get_rect(center=(rect.centerx, rect.y + 250)))
            
            type_txt = get_font(30).render(f"Type: {p['type']}", True, "black")
            SCREEN.blit(type_txt, type_txt.get_rect(center=(rect.centerx, rect.y + 310)))

            hp_txt = get_font(35).render(f"HP: {p['hp']}", True, "black")
            SCREEN.blit(hp_txt, hp_txt.get_rect(center=(rect.centerx, rect.y + 380)))

            atk_txt = get_font(35).render(f"ATK: {p['atk']}", True, "black")
            SCREEN.blit(atk_txt, atk_txt.get_rect(center=(rect.centerx, rect.y + 430)))

        back_btn.draw(SCREEN, mouse)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.clicked(mouse):
                    return

        pygame.display.update()

def server_ip_menu():
    clock = pygame.time.Clock()
    ip_text = ""
    back_btn = Button("BACK", (W // 2, H - 100), 45, "black", "orange")

    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        title = get_font(60).render("Enter Server IP", True, "orange")
        SCREEN.blit(title, title.get_rect(center=(W // 2, 150)))

        input_box = pygame.Rect(W // 2 - 305, 300, 605, 60)
        pygame.draw.rect(SCREEN, "white", input_box, border_radius=10)
        pygame.draw.rect(SCREEN, "black", input_box, 2, border_radius=10)

        text_surface = get_font(40).render(ip_text, True, "black")
        SCREEN.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        hint = get_font(30).render("Press ENTER to connect", True, "black")
        SCREEN.blit(hint, hint.get_rect(center=(W // 2, 420)))
        back_btn.draw(SCREEN, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return None, None
                if event.key == pygame.K_RETURN and ip_text:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind(("", 0))
                    server = (ip_text, 5678)
                    sock.sendto(b"JOIN", server)
                    return sock, server
                if event.key == pygame.K_BACKSPACE: ip_text = ip_text[:-1]
                else:
                    if len(ip_text) < 20 and event.unicode.isprintable():
                        ip_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.clicked(mouse): return None, None

        pygame.display.update()
        clock.tick(60)

def main_menu():
    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(90).render("Pokemon ;)", True, "#b68f40")
        SCREEN.blit(title, title.get_rect(center=(W//2, H//3)))

        new = Button("NEW GAME", (W//2, H//2), 50, "black", "orange")
        index_btn = Button("INDEX", (W//2, H//2 + 80), 50, "black", "orange")
        quit_btn = Button("QUIT", (W//2, H//2 + 160), 50, "black", "orange")

        for b in (new, index_btn, quit_btn):
            b.draw(SCREEN, mouse)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if new.clicked(mouse):
                    sock, server = server_ip_menu()
                    if sock:
                        Battle.main(sock, server)
                if index_btn.clicked(mouse):
                    pokedex_index()
                if quit_btn.clicked(mouse):
                    quit_game()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    def __init__(self, name, stats, rect):
        self.name = name
        self.stats = stats
        self.rect = pygame.Rect(rect)
        self.selected = False

    def draw(self, screen, mouse):
        color = (170, 220, 170) if self.rect.collidepoint(mouse) else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, "black", self.rect, 2, border_radius=12)

        title = get_font(26).render(self.name, True, "black")
        screen.blit(title, title.get_rect(center=(self.rect.centerx, self.rect.y + 28)))

        y = 60
        for k, v in self.stats.items():
            txt = get_font(20).render(f"{k}: {v}", True, "black")
            screen.blit(txt, (self.rect.x + 12, self.rect.y + y))
            y += 26

        if self.selected:
            pygame.draw.rect(screen, "green", self.rect, 4, border_radius=12)

    def clicked(self, mouse):
        return self.rect.collidepoint(mouse)

class TeamSlot:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.card = None

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=12)
        pygame.draw.rect(screen, "black", self.rect, 2, border_radius=12)

        if self.card:
            txt = get_font(22).render(self.card.name, True, "black")
            screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, mouse):
        return self.rect.collidepoint(mouse)

cards = []
team = []
MAX_TEAM = 4


slots = []
slot_w, slot_h = 160, 200
sx = (W - (4 * slot_w + 3 * 30)) // 2

for i in range(4):
    slots.append(TeamSlot((sx + i * (slot_w + 30), 100, slot_w, slot_h)))

def team_menu():
    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(50).render("Build Your Team", True, "orange")
        SCREEN.blit(title, title.get_rect(center=(W//2, 60)))

        for s in slots:
            s.draw(SCREEN)

        for c in cards:
            c.draw(SCREEN, mouse)

        back = Button("BACK", (W//2, H-40), 40, "black", "orange")
        back.draw(SCREEN, mouse)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

            if e.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked(mouse):
                    return

                for c in cards:
                    if c.clicked(mouse) and not c.selected and len(team) < MAX_TEAM:
                        for s in slots:
                            if not s.card:
                                s.card = c
                                c.selected = True
                                team.append(c)
                                break

                for s in slots:
                    if s.clicked(mouse) and s.card:
                        s.card.selected = False
                        team.remove(s.card)
                        s.card = None

        pygame.display.update()

def server_ip_menu():
    clock = pygame.time.Clock()
    ip_text = ""

    back_btn = Button(
        "BACK",
        (W // 2, H - 100),
        45,
        "black",
        "orange"
    )

    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(60).render("Enter Server IP", True, "orange")
        SCREEN.blit(title, title.get_rect(center=(W // 2, 150)))

        input_box = pygame.Rect(W // 2 - 305, 300, 605, 60)
        pygame.draw.rect(SCREEN, "white", input_box, border_radius=10)
        pygame.draw.rect(SCREEN, "black", input_box, 2, border_radius=10)

        text_surface = get_font(40).render(ip_text, True, "black")
        SCREEN.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        hint = get_font(30).render("Press ENTER to connect", True, "black")
        SCREEN.blit(hint, hint.get_rect(center=(W // 2, 420)))

        back_btn.draw(SCREEN, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None  # BACK

                if event.key == pygame.K_RETURN and ip_text:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind(("", 0))
                    server = (ip_text, 5678)
                    sock.sendto(b"JOIN", server)
                    return sock, server

                if event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                else:
                    if len(ip_text) < 20 and event.unicode.isprintable():
                        ip_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.clicked(mouse):
                    return None, None  # BACK

        pygame.display.update()
        clock.tick(60)

def main_menu(SCREEN_WIDTH, SCREEN_HEIGHT):
    while True:
        mouse = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(90).render("Pokemon ;)", True, "#b68f40")
        SCREEN.blit(title, title.get_rect(center=(W//2, H//3)))

        new = Button("NEW GAME", (W//2, H//2), 50, "black", "orange")
        index_btn = Button("INDEX", (W//2, H//2 + 80), 50, "black", "orange")
        quit_btn = Button("QUIT", (W//2, H//2 + 160), 50, "black", "orange")

        for b in (new, index_btn, quit_btn):
            b.draw(SCREEN, mouse)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if new.clicked(mouse):
                    sock, server = server_ip_menu()
                    if sock is None: continue
                    pygame.display.quit()
                    Battle.main(sock, server)
                    pygame.quit()
                    sys.exit()

                if index_btn.clicked(mouse):
                    pokedex_index()

                if quit_btn.clicked(mouse):
                    quit_game()

        pygame.display.update()
