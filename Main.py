import time
import pygame
import sys
from button import Button


pygame.init()

SCREEN = pygame.display.set_mode((1008, 720))
pygame.display.set_caption("Space Invaders")
BG = pygame.image.load('assets/Background.png')
bg_game = pygame.image.load('assets/backstar2.jpg')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hudba = 1


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


# Print Delay
def delay_print(s):
    # 1pismeno naraz

    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


# Class


class Mon:
    def __init__(self, name, types, moves, ev, hp, health="===================="):
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = ev["ATTACK"]
        self.defense = ev["DEFENSE"]
        self.speed = ev["SPEED"]
        self.bars = 20
        self.health = health
        self.hp = hp
        self.max = hp
    def fight(self, pokemon2):
        global string_1_attack, supeff, string_2_attack
        print("BATTLE START")
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENCE/", self.defense)

        print("BATTLE START")
        print(f"\n{pokemon2.name}")
        print("TYPE/", pokemon2.types)
        print("ATTACK/", pokemon2.attack)
        print("DEFENCE/", pokemon2.defense)

        time.sleep(2)

        version = ["Fire", "Water", "Grass"]
        for i, k in enumerate(version):
            supeff = True
            if self.types == k:
                if pokemon2.types == k:
                    string_1_attack = "\nIt's not very effective..."
                    string_2_attack = "\nIt's not very effective..."
            # Pokemon 2 ma Type advantage
            elif pokemon2.types == version[(i + 2) % 3]:
                pokemon2.attack *= 2
                pokemon2.defense *= 2
                string_1_attack = "\nIt's not very effective!"
                string_2_attack = "\nIt's SUPER effective!"
            # self ma Type advantage
            elif pokemon2.types == version[(i + 1) % 3]:
                self.attack *= 2
                self.defense *= 2
                string_1_attack = "\nIt's SUPER effective!"
                string_2_attack = "\nIt's not very effective!"
            else:
                supeff = False

        # Fight:

        while (0 < self.hp) and (pokemon2.hp > 0):
            print(f"{self.name}\t\tHP\t{self.bars}")
            print(f"{pokemon2.name}\t\tHP\t{pokemon2.bars}")

            print(f"GO {self.name}!")
            for i, x in enumerate(self.moves):
                print(f"{i + 1}.", x)
            index = int(input("Pick a move:"))
            delay_print(f"{self.name} used {self.moves[index - 1]}!")
            time.sleep(1)
            if supeff:
                delay_print(string_1_attack)

            # Damage
            pokemon2.hp -= self.attack
            pokemon2.health = ""
            for j in range(int(pokemon2.hp / pokemon2.max * 20 + .1 * pokemon2.defense)):
                pokemon2.health += "="

            time.sleep(1)
            print(f"{self.name}\t\tHP\t{self.health}")
            print(f"{pokemon2.name}\t\tHP\t{pokemon2.health}")

            if pokemon2.bars <= 0:
                delay_print("\n..." + pokemon2.name + " fainted.")
                break

            # Poke2 turn
            print(f"GO {pokemon2.name}!")
            for i, x in enumerate(pokemon2.moves):
                print(f"{i + 1}.", x)
            index = int(input("Pick a move:"))
            delay_print(f"{pokemon2.name} used {pokemon2.moves[index - 1]}!")
            time.sleep(1)
            if supeff:
                delay_print(string_2_attack)

            self.bars -= pokemon2.attack
            self.health = ""
            for j in range(int(self.hp / self.max * 20 + .1 * self.defense)):
                self.health += "="

            time.sleep(1)
            print(f"\n{self.name}\t\tHP\t{self.health}")
            print(f"\n{pokemon2.name}\t\tHP\t{pokemon2.health}")

            if self.hp <= 0:
                delay_print("\n..." + self.name + " fainted.")
                break


if __name__ == "__main__":
    Charizard = Mon("Charizard", "Fire", ["Flamethrower", "Fly", "Blast Burn", "Firepunch"],
                    {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10}, 40)
    Blastoise = Mon("Blastoise", "Water", ["Bubblebeam", "Tackle", "Headbutt", "Surf"],
                    {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10}, 55)
    Venusaur = Mon("Venusaur", "Grass", ["Solar Beam", "Giga Drain", "Sleep Powder", "Leech Seed"],
                   {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10}, 70)


def play():
    pygame.mixer.music.play(-1)
    Charizard.fight(Blastoise)


def options():
    global hudba
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(35).render("Vyber si hudbu:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(504, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        ASGORE = Button(image=None, pos=(504, 360),
                        text_input="DEFAULT", font=get_font(75), base_color="Black", hovering_color="Green")

        TRUEHERO = Button(image=None, pos=(504, 460),
                          text_input="ALTERNATIVE", font=get_font(75), base_color="Black", hovering_color="Green")

        SANS = Button(image=None, pos=(504, 560),
                      text_input="MEME", font=get_font(75), base_color="Black", hovering_color="Green")

        ASGORE.changecolor(OPTIONS_MOUSE_POS)
        ASGORE.update(SCREEN)

        TRUEHERO.changecolor(OPTIONS_MOUSE_POS)
        TRUEHERO.update(SCREEN)

        SANS.changecolor(OPTIONS_MOUSE_POS)
        SANS.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ASGORE.checkforinput(OPTIONS_MOUSE_POS):
                    hudba = 1
                    main_menu()
                if TRUEHERO.checkforinput(OPTIONS_MOUSE_POS):
                    hudba = 2
                    main_menu()
                if SANS.checkforinput(OPTIONS_MOUSE_POS):
                    hudba = 3
                    main_menu()

        pygame.display.update()


def main_menu():
    if hudba == 1:
        pygame.mixer.music.load('../Mojahra/872882_Undertale-Asgore-Theme.mp3')
    if hudba == 2:
        pygame.mixer.music.load('../Mojahra/656569_Undertale-Undyne-the-Undyi.mp3')
    if hudba == 3:
        pygame.mixer.music.load('695513_-Megalovania--Remix.mp3')
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(504, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(504, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(504, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(504, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changecolor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkforinput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkforinput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkforinput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()


# import sys
#
# import pygame
#
# global active, i
# pygame.init()
#
# SCREEN = pygame.display.set_mode((1008, 720))
# pygame.display.set_caption("Mons")
# typ = ["ohen", "elektrina", "voda"]
# ability = ["sunny day"]
# moves = ["move1", "move2", "move3", "move4"]
# resistance = [typ[0]]
# weakness = [typ[1]]
# Charizard = ["Charizard", typ[0], ability[0], resistance[0], weakness[0], moves[0], moves[1], moves[2], moves[3]]
# mon = [Charizard, "Pikachu"]
# battlestart = True
# batle = False
#
#
# def battle():
#     print("Vyslal si " + active)
#     print(" ")
#     print("1. " + active[0][-4])
#     print("2. " + active[0][-3])
#     print("3. " + active[0][-2])
#     print("4. " + active[0][-1])
#     print("5. Vymen")
#     while True:
#         pass
#
#
# print("Vyber si mona:")
# print(" ")
# print("1" + " " + mon[0][0])
# print("2" + " " + mon[1])
# print("3")
# print("4")
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 active = mon[0][0]
#                 battle()
#             if event.key == pygame.K_2:
#                 active = mon[1]
#                 battle()
