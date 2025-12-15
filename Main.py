import sys
import time


# Print Delay


def delay_print(s):
    # 1pismeno naraz

    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


# Class


class Mon:
    def __init__(self, name, types, moves, ev, health="===================="):
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = ev["ATTACK"]
        self.defense = ev["DEFENSE"]
        self.bars = 20
        self.health = health

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
                    string_1_attack = "It's not very effective..."
                    string_2_attack = "It's not very effective..."
            # Pokemon 2 ma Type advantage
            elif pokemon2.types == version[(i + 1) % 3]:
                pokemon2.attack *= 2
                pokemon2.defense *= 2
                string_1_attack = "It's not very effective"
                string_2_attack = "It's SUPER effective"
            # self ma Type advantage
            elif pokemon2.types == version[(i + 2) % 3]:
                self.attack *= 2
                self.defense *= 2
                string_1_attack = "It's SUPER effective"
                string_2_attack = "It's not very effective"
            else:
                supeff = False

        # Fight:

        while (0 < self.bars) and (pokemon2.bars > 0):
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
            pokemon2.bars -= self.attack
            pokemon2.health = ""
            for j in range(int(pokemon2.bars + .1 * pokemon2.defense)):
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
            for j in range(int(pokemon2.bars + .1 * pokemon2.defense)):
                self.health += "="

            time.sleep(1)
            print(f"{self.name}\t\tHP\t{self.health}")
            print(f"{pokemon2.name}\t\tHP\t{pokemon2.health}")

            if self.bars <= 0:
                delay_print("\n..." + self.name + " fainted.")
                break


if __name__ == "__main__":
    Charizard = Mon("Charizard", "Fire", ["Flamethrower", "Fly", "Blast Burn", "Firepunch"],
                    {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10})
    Blastoise = Mon("Blastoise", "Water", ["Bubblebeam", "Tackle", "Headbutt", "Surf"],
                    {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10})
    Venusaur = Mon("Venusaur", "Grass", ["Solar Beam", "Giga Drain", "Sleep Powder", "Leech Seed"],
                    {"ATTACK": 12, "DEFENSE": 6, "SPEED": 10})

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
