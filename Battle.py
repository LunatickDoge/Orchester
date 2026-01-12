import pygame
import os
import sys
import time
import random
from pygame.locals import *

# COLORS
# R    G    B
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
NAVYBLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ALPHA = (255, 0, 255)
FPS = 15
fpsClock = pygame.time.Clock()


def safe_get_active(team, index):
    if index is None:
        return None, None
    if index < 0 or index >= len(team):
        return None, None
    return team[index]["pokemon"], team[index]["moves"]


def MoveStrip(pokemonList, moveNumber):
    # Build move filename
    moveName = pokemonList[moveNumber + 3].lower() + '.txt'
    movePath = os.path.join("data", moveName)

    with open(movePath, 'r') as f:
        fileList = f.read().split('\n')

    moveList = []
    for i in range(6):
        moveList.append(fileList[i])

    return moveList


def PokemonStrip(targetFile):
    # Build path to data folder
    file_path = os.path.join("data", targetFile)

    with open(file_path, 'r') as f:
        fileString = f.read()
        fileList = fileString.split('\n')

    targetList = []
    for i in range(11):
        targetList.append(fileList[i])

    return targetList


def ClearTerminal():
    # Clears terminal. Obselete, but took me forever to figure out, so I'll keep it
    # here as a trophy.
    os.system('cls' if os.name == 'nt' else 'clear')


def drawText(text, font, surf, x, y, color=WHITE):
    surf.blit(font.render(text, True, color), (x, y))


def drawMoveText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    pygame.display.update()


def redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList):
    DISPLAYSURF.blit(playerImgList[1], (0, 195))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 315, WHITE)
    playerBar.updateBar(pPokemon)
    playerBar.drawRects()
    DISPLAYSURF.blit(computerImgList[0], (200, 0))
    drawText(cPokemon[0], font, DISPLAYSURF, 10, 45, WHITE)
    computerBar.updateBar(cPokemon)
    computerBar.drawRects()
    pygame.display.update()


def displayMessage(message, pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList):
    drawText(message, font, DISPLAYSURF, 10, 400, WHITE)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    time.sleep(1)
    DISPLAYSURF.blit(background, (0, 0))


def get_active_pokemon(team, index):
    return team[index]["pokemon"], team[index]["moves"]


def cMoveSelect(cMoveList):
    cMove = cMoveList[random.randint(0, 3)]
    return cMove


def pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList,
                button1, button2, button3, button4, cPokemon):
    # The player move select function. This function draws the instructions and the
    # buttons necessary to guide the player in selecting a move for their pokemon.

    # Redrawing background image to clear text
    global Move
    DISPLAYSURF.blit(background, (0, 0))
    # Drawing the prompt in the text section
    drawText("What will " + pPokemon[0] + " do?", font, DISPLAYSURF, 10, 400, WHITE)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    # Drawing buttons for use in the move selection process. Buttons are separate
    # from the text on the button to allow the system to be completely modular
    button1.drawButton()
    drawMoveText(pMoveList[0][5], font, DISPLAYSURF, 100, 499, BLACK)
    button2.drawButton()
    drawMoveText(pMoveList[1][5], font, DISPLAYSURF, 300, 499, BLACK)
    button3.drawButton()
    drawMoveText(pMoveList[2][5], font, DISPLAYSURF, 100, 566, BLACK)
    button4.drawButton()
    drawMoveText(pMoveList[3][5], font, DISPLAYSURF, 300, 566, BLACK)
    pygame.display.update()

    picked = 0
    while picked == 0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button1.pressed(mouse):  # Is mouseclick on button?
                    Move = pMoveList[0]  # assigning corresponding move as pMove
                    picked = 1  # modifying conditional to break iteration of loop
                if button2.pressed(mouse):
                    Move = pMoveList[1]
                    picked = 1
                if button3.pressed(mouse):
                    Move = pMoveList[2]
                    picked = 1
                if button4.pressed(mouse):
                    Move = pMoveList[3]
                    picked = 1
    return Move


################################################################################
# Image Initialization Functions
################################################################################

def BulbImages():
    fileNames = ["assets/bulbasaurFront.png", "assets/bulbasaurBack.png"]
    bulbArray = []
    for x in fileNames:
        newImg = pygame.image.load(x)
        bulbArray.append(newImg)
    return bulbArray


def CharImages():
    fileNames = ["assets/charmanderFront.png", "assets/charmanderBack.png"]
    charArray = []
    for x in fileNames:
        newImg = pygame.image.load(x)
        charArray.append(newImg)
    return charArray


def SquirtImages():
    fileNames = ["assets/squirtleFront.png", "assets/squirtleBack.png"]
    squirtArray = []
    for x in fileNames:
        newImg = pygame.image.load(x)
        squirtArray.append(newImg)
    return squirtArray


def ballp():
    global openball, closedball, background
    DISPLAYSURF.blit(closedball, (100, 250))
    DISPLAYSURF.blit(closedball, (300, 100))
    pygame.display.update()
    time.sleep(1.5)
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(openball, (300, 100))
    DISPLAYSURF.blit(openball, (100, 250))
    pygame.display.update()
    time.sleep(0.5)


class HealthBar():
    # Class for creating unique healthbar objects for the player and computer pokemon.
    def __init__(self):
        self.position = None
        self.negDimensions = None
        self.posDimensions = None

    def init(self, x, y):
        # Function for initializing the attributes of the healthbar. Location and healthbar
        # length.
        self.position = x, y
        self.negDimensions = (150, 5)
        self.posDimensions = [150, 5]

    def updateBar(self, pokemonList):
        maxHealth = pokemonList[8]
        currentHealth = pokemonList[1]
        healthProportion = int(currentHealth) / float(maxHealth)
        newDimension = healthProportion * self.negDimensions[0]
        self.posDimensions[0] = newDimension

    def drawRects(self):
        # Function for drawing the actual rectangles that make up the health bar.
        # (x,y,width,height)
        pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
        pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
        pygame.display.update()




class Button():
    def __init__(self):
        self.rect = None
        self.image = None  # store assigned image

    def assignImage(self, picture):
        self.rect = picture.get_rect()
        self.image = picture

    def setCoords(self, x, y):
        self.rect.topleft = x, y

    def drawButton(self, picture=None):
        # if no picture is passed, use the assigned image
        if picture is None:
            picture = self.image
        DISPLAYSURF.blit(picture, self.rect)

    def pressed(self, mouse):
        return self.rect.collidepoint(mouse)


def PlayerChoice(targetFile):
    # Function handling the stripping and value assignment for the player pokemon
    pPokemon = []
    pPokemon = PokemonStrip(targetFile)  # Strip values from player target file
    moveNumber = 1
    pAttackList = []
    # Create a separate list for every player move
    while moveNumber < 5:
        pAttackList.append(MoveStrip(pPokemon, moveNumber))
        moveNumber += 1
    return [pPokemon, pAttackList]


def ComputerChoice(choices, charImages, bulbImages, squirtImages):
    # Function for handling the random selection of pokemon for the computer.=
    global computerImgList
    choice = random.randint(0, 1)  # Pick at random one of the two remaining pokemon
    # Determine which pokemon has been selected and assign images to the computer
    if choices[choice] == "Charmander":
        computerImgList = charImages
    elif choices[choice] == "Bulbasaur":
        computerImgList = bulbImages
    elif choices[choice] == "Squirtle":
        computerImgList = squirtImages
    targetFile = choices[choice].lower() + '.txt'  # Generate filename for the strip
    # function to use as a target.
    cPokemon = []  # Create stat list for computer pokemon
    cPokemon = PokemonStrip(targetFile)  # Run strip function for target file
    moveNumber = 1
    cAttackList = []
    # Create a separate list for all computer attacks
    while moveNumber < 5:
        cAttackList.append(MoveStrip(cPokemon, moveNumber))
        moveNumber += 1
    return [cPokemon, cAttackList, computerImgList]


def animateText(text, font, surface, x, y, color):
    if len(text) > 49:
        textLine1 = text[:49]
        textLine2 = text[48:]
    else:
        textLine1 = text
        textLine2 = ""
    i = 0
    for letter in textLine1:
        realLine1 = textLine1[:i]
        textobj1 = font.render(realLine1, 1, color)
        textrect1 = textobj1.get_rect()
        textrect1.topleft = (x, y)
        surface.blit(textobj1, textrect1)
        pygame.display.update()
        fpsClock.tick(FPS)
        i += 1
    j = 0
    for letter in textLine2:
        realLine2 = textLine2[:j]
        textobj2 = font.render(textLine2, 1, color)
        textrect2 = textobj2.get_rect()
        textrect2.topleft = (x, y + 10)
        surface.blit(textobj2, textrect2)
        pygame.display.update()
        j += 1


def Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList, playerBar, computerBar):
    global winner
    pStats = [1, 1]
    cStats = [1, 1]
    # Initializing the condition for iterating the main program loop
    fainted = False

    # Entire following block of code dedicated to drawing the battle screen for the
    # first time in the correct order, and with good readability
    DISPLAYSURF.blit(background, (0, 0))
    drawText(pPokemon[0].upper() + "! I choose you!", font, DISPLAYSURF, 10, 400, WHITE)
    time.sleep(2)
    ballp()
    for i in range(300):
        if i < 100:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (0 + i / 2, 195))
            pygame.display.update()
        elif i < 200:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (50 +  - i / 2, 195))
            pygame.display.update()
        else:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (-50 + i / 6, 195))
            pygame.display.update()
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, WHITE)
    playerBar.drawRects()
    time.sleep(2)
    DISPLAYSURF.blit(background, (0, 0))
    drawText("Computer sent out " + cPokemon[0] + "!", font, DISPLAYSURF, 10, 400, WHITE)
    for i in range(300):
        if i < 100:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (0, 195))
            DISPLAYSURF.blit(computerImgList[0], (200 + i / 2, 0))
            pygame.display.update()
        elif i < 200:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (0, 195))
            DISPLAYSURF.blit(computerImgList[0], (250 - i / 2, 0))
            pygame.display.update()
        else:
            DISPLAYSURF.blit(background, (0, 0))
            DISPLAYSURF.blit(playerImgList[1], (0, 195))
            DISPLAYSURF.blit(computerImgList[0], (150 + i / 6, 0))
            pygame.display.update()
    DISPLAYSURF.blit(playerImgList[1], (0, 195))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, WHITE)
    playerBar.drawRects()
    time.sleep(2)
    DISPLAYSURF.blit(background, (0, 0))
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    # Main program loop. Loop terminates when one pokemon has fained.
    while fainted != True:
        # Executing the move selection functions for both the player and the computer
        pMove = pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList, button1,
                            button2, button3, button4, cPokemon)
        cMove = cMoveSelect(cMoveList)

        # If player stat is faster, player attack sequence executes before computer
        # attack sequence. Else, computer attack sequence attacks first.
        if pPokemon[2] < cPokemon[2]:
            # Execute attack sequence for player
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList,
                            computerImgList)
            # Update the health bar if any changes have occured
            computerBar.updateBar(cPokemon)
            computerBar.drawRects()
            pygame.display.update()
            if int(cPokemon[1]) <= 0:
                fainted = True
                winner = "Player"
                break  # break loop to end program
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if int(pPokemon[1]) <= 0:
                fainted = True
                winner = "Computer"
                break
        else:
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if int(pPokemon[1]) <= 0:
                fainted = True
                winner = "Computer"
                break
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList, computerImgList)
            computerBar.updateBar(cPokemon)
            computerBar.drawRects()
            pygame.display.update()
            if int(cPokemon[1]) <= 0:
                fainted = True
                winner = "Player"
                break
        redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    if winner == "Player":
        DISPLAYSURF.blit(endBackground, (0, 0))
        DISPLAYSURF.blit(playerImgList[0], (100, 375))
        drawText("The winner is " + pPokemon[0] + "!", font, TEXTSURF, 120, 100, WHITE)
        pygame.display.update()
        time.sleep(2)
    # If the computer won, computer pokemon is displayed on the victory screen
    else:
        DISPLAYSURF.blit(endBackground, (0, 0))
        DISPLAYSURF.blit(computerImgList[0], (100, 375))
        drawText("The winner is " + cPokemon[0] + "!", font, TEXTSURF, 120, 100, WHITE)
        pygame.display.update()
        time.sleep(2)
    import Menu
    Menu.main_menu()


def LoadPlayerTeam(team_names):
    team = []
    for name in team_names:
        pokemon, moves = PlayerChoice(name.lower() + ".txt")
        pokemon[1] = int(pokemon[1])  # current HP
        pokemon.append(True)          # alive flag
        team.append({
            "pokemon": pokemon,
            "moves": moves
        })
    return team


def force_switch(team):
    for i, slot in enumerate(team):
        if slot["pokemon"][11]:
            return i
    return None


def choose_switch(team, screen, font, background):
    while True:
        screen.blit(background, (0, 0))
        drawText("Choose a Pokémon to switch to:", font, screen, 40, 50)

        y = 120
        for i, slot in enumerate(team):
            name = slot["pokemon"][0]
            alive = slot["pokemon"][11]
            color = GREEN if alive else RED
            drawText(f"{i+1}. {name}", font, screen, 60, y, color)
            y += 40

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                idx = event.key - pygame.K_1
                if 0 <= idx < len(team) and team[idx]["pokemon"][11]:
                    return idx


def pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats,
                    playerBar, computerBar, playerImgList, computerImgList):
    DISPLAYSURF.blit(background, (0, 0))
    displayMessage(pPokemon[0] + " used " + pMove[5],
                   pPokemon, playerBar, computerImgList,
                   cPokemon, computerBar, playerImgList)
    time.sleep(1)
    mode = pMove[0]
    if mode == "1":
        cPokemon = DamageMod(pPokemon, pMove, cPokemon, pStats, cStats)
    elif mode == "21":
        pStats = StatMod(pMove, pStats, pPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    elif mode == "22":
        cStats = StatMod(pMove, cStats, cPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)


def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar):
    # Function handling the application of steps in computer attack. Only difference
    # from player attack sequence is that the parameters for target are aimed at the
    # player
    DISPLAYSURF.blit(background, (0, 0))
    displayMessage(cPokemon[0] + " used " + cMove[5] + ".",
                   pPokemon, playerBar,
                   computerImgList, cPokemon,
                   computerBar, playerImgList)

    time.sleep(1)
    mode = cMove[0]
    if mode == "1":
        pPokemon = DamageMod(cPokemon, cMove, pPokemon, cStats, pStats)
    elif mode == "21":
        cStats = StatMod(cMove, cStats, cPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    elif mode == "22":
        pStats = StatMod(cMove, pStats, pPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)


def DamageMod(attacker, move, target, atk_stats, def_stats):
    if move[2] == "*" or move[0] != "1":
        return target
    dmg = int(move[2])
    multiplier = AdvantageCalc(move, target)
    atk = StatIndex(atk_stats, "A")
    defense = StatIndex(def_stats, "D")
    damage = int(dmg * (atk / defense) * multiplier)
    target[1] -= damage
    return target



def StatMod(move, targetStats, defenderName, pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList):
    targetStat = move[4]
    effect = move[3]
    if targetStat == "A":  # If target stat is attack...
        if effect == "-":  # And the effect is negative...
            targetStats[0] -= 1  # target's attack is lowered
            displayMessage(defenderName + "'s" + " Attack fell.", pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
            return targetStats
        else:  # and the ffect is positive...
            targetStats[0] += 1  # target's atack is raised
            displayMessage(defenderName + "'s" + " Attack rose.", pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
            return targetStats
    else:  # if target stat is defense...
        if effect == "-":  # and effect is negative...
            targetStats[1] -= 1  # target's defense is lowered
            displayMessage(defenderName + "'s" + " Defense fell.", pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
            return targetStats
        else:  # and the effect is positive...
            targetStats[1] += 1  # target's defense is raised
            displayMessage(defenderName + "'s" + " Defense rose.", pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
            # Function returns the new stat levels for the target pokemon
            return targetStats


def StatIndex(stats, stat):
    table = [0.25, 0.33, 0.5, 0.66, 1, 1.5, 2, 2.5, 3]
    return table[stats[0] + 4] if stat == "A" else table[stats[1] + 4]


def AdvantageCalc(attack, target):
    combo = attack[1] + target[3]
    chart = {
        "FG": 2, "FW": 0.5,
        "GF": 0.5, "GW": 2,
        "WF": 2, "WG": 0.5
    }
    return chart.get(combo, 1)



def main(team_names):
    global DISPLAYSURF, TEXTSURF, font, background, endBackground, playerImgList, choice
    global button1, button2, button3, button4, openball, closedball

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 600))
    TEXTSURF = pygame.display.set_mode((400, 600))
    pygame.display.set_caption('Pythonmon')

    font = pygame.font.SysFont(None, 22)

    background = pygame.image.load("assets/background.png").convert()
    endBackground = pygame.image.load("assets/background.png").convert()

    player_team = LoadPlayerTeam(team_names)
    computer_team = LoadPlayerTeam(["Charmander"])

    player_idx = 0
    comp_idx = 0

    pStats = [1, 1]
    cStats = [1, 1]

    openball = pygame.transform.scale(
        pygame.image.load('assets/open.png'), (20, 20)
    )
    closedball = pygame.transform.scale(
        pygame.image.load('assets/closed.png'), (20, 20)
    )

    animateText("Choose your Pokemon...", font, TEXTSURF, 120, 100, WHITE)
    pygame.display.update()
    while True:

        pPokemon, pMoves = safe_get_active(player_team, player_idx)
        cPokemon, cMoves = safe_get_active(computer_team, comp_idx)

        if pPokemon is None:
            import Menu
            drawText("YOU LOSE!", font, DISPLAYSURF, 150, 300)
            pygame.display.update()
            time.sleep(2)
            Menu.main_menu()
            return

        if cPokemon is None:
            import Menu
            drawText("YOU WIN!", font, DISPLAYSURF, 150, 300)
            pygame.display.update()
            time.sleep(2)
            Menu.main_menu()
            return

        DISPLAYSURF.blit(background, (0, 0))
        drawText(f"{pPokemon[0]} HP: {pPokemon[1]}", font, DISPLAYSURF, 40, 400)
        drawText(f"{cPokemon[0]} HP: {cPokemon[1]}", font, DISPLAYSURF, 40, 60)
        drawText("1–4: Attack | S: Switch", font, DISPLAYSURF, 40, 450)
        pygame.display.update()

        action = None
        while action is None:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        action = "SWITCH"
                    elif K_1 <= event.key <= K_4:
                        action = pMoves[event.key - K_1]

        if action == "SWITCH":
            player_idx = choose_switch(player_team, DISPLAYSURF, font, background)
            continue

        # ATTACK PHASE
        DamageMod(pPokemon, action, cPokemon, pStats, cStats)

        if cPokemon[1] <= 0:
            cPokemon[11] = False
            comp_idx = force_switch(computer_team)
            if comp_idx is None:
                drawText("YOU WIN!", font, DISPLAYSURF, 150, 300)
                pygame.display.update()
                time.sleep(2)
                return

        DamageMod(cPokemon, random.choice(cMoves), pPokemon, cStats, pStats)

        if pPokemon[1] <= 0:
            pPokemon[11] = False
            player_idx = force_switch(player_team)
            if player_idx is None:
                drawText("YOU LOSE!", font, DISPLAYSURF, 150, 300)
                pygame.display.update()
                time.sleep(2)
                return

        fpsClock.tick(FPS)
