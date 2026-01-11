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


def drawText(text, font, surface, x, y, color):
    # Simple function for drawing text onto the screen. Function contains expression
    # for word wrap.
    if len(text) > 49:
        textLine1 = text[:48]
        textLine2 = text[48:]
    else:
        textLine1 = text
        textLine2 = ""

    textobj1 = font.render(textLine1, 1, color)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x, y)
    surface.blit(textobj1, textrect1)
    pygame.display.update()

    textobj2 = font.render(textLine2, 1, color)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x, y + 10)
    surface.blit(textobj2, textrect2)
    pygame.display.update()


def drawMoveText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    pygame.display.update()


def redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList):
    DISPLAYSURF.blit(playerImgList[1], (0, 195))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 315, BLACK)
    playerBar.updateBar(pPokemon)
    playerBar.drawRects()
    DISPLAYSURF.blit(computerImgList[0], (200, 0))
    drawText(cPokemon[0], font, DISPLAYSURF, 10, 45, BLACK)
    computerBar.updateBar(cPokemon)
    computerBar.drawRects()
    pygame.display.update()


def displayMessage(message, pPokemon=None, playerBar=None, computerImgList=None, cPokemon=None, computerBar=None, playerImgList=None):
    drawText(message, font, DISPLAYSURF, 10, 400, BLACK)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    time.sleep(1)
    DISPLAYSURF.blit(background, (0, 0))


def cMoveSelect(cMoveList):
    cMove = cMoveList[random.randint(0, 3)]
    return cMove


def pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList,
                button1, button2, button3, button4, cPokemon):
    # The player move select function. This function draws the instructions and the
    # buttons necessary to guide the player in selecting a move for their pokemon.

    # Redrawing background image to clear text
    DISPLAYSURF.blit(background, (0, 0))
    # Drawing the prompt in the text section
    drawText("What will " + pPokemon[0] + " do?", font, DISPLAYSURF, 10, 400, BLACK)
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

    def drawRects(self):
        # Function for drawing the actual rectangles that make up the health bar.
        # (x,y,width,height)
        pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
        pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
        pygame.display.update()

    def updateBar(self, pokemonList):
        maxHealth = pokemonList[8]
        currentHealth = pokemonList[1]
        healthProportion = int(currentHealth) / float(maxHealth)
        newDimension = healthProportion * self.negDimensions[0]
        self.posDimensions[0] = newDimension


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
    drawText(pPokemon[0].upper() + "! I choose you!", font, DISPLAYSURF, 10, 400, BLACK)
    time.sleep(2)
    DISPLAYSURF.blit(playerImgList[1], (0, 195))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, BLACK)
    playerBar.drawRects()
    time.sleep(2)
    DISPLAYSURF.blit(background, (0, 0))
    drawText("Computer sent out " + cPokemon[0] + "!", font, DISPLAYSURF, 10, 400, BLACK)
    DISPLAYSURF.blit(playerImgList[1], (0, 195))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, BLACK)
    playerBar.drawRects()
    time.sleep(2)
    DISPLAYSURF.blit(background, (0, 0))
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    # Main program loop. Loop terminates when one pokemon has fained.
    while fainted != True:
        # Executing the move selection functions for both the player and the computer
        pMove = pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList, button1, button2, button3, button4, cPokemon)
        cMove = cMoveSelect(cMoveList)

        # If player stat is faster, player attack sequence executes before computer
        # attack sequence. Else, computer attack sequence attacks first.
        if pPokemon[2] < cPokemon[2]:
            # Player goes first
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList,
                            computerImgList)
            computerBar.updateBar(cPokemon)
            computerBar.drawRects()
            pygame.display.update()
            if cPokemon[1] <= 0:
                fainted = True
                winner = "Player"
                break
            # Pass the missing arguments here
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerImgList, computerBar,
                            playerImgList)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if pPokemon[1] <= 0:
                fainted = True
                winner = "Computer"
                break
        else:
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerImgList, computerBar,
                            playerImgList)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if pPokemon[1] <= 0:
                fainted = True
                winner = "Computer"
                break
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList,
                            computerImgList)
            computerBar.updateBar(cPokemon)
            computerBar.drawRects()
            pygame.display.update()
            if cPokemon[1] <= 0:
                fainted = True
                winner = "Player"
                break
        redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    if winner == "Player":
        DISPLAYSURF.blit(endBackground, (0, 0))
        DISPLAYSURF.blit(playerImgList[0], (100, 375))
        drawText("The winner is " + pPokemon[0] + "!", font, TEXTSURF, 120, 100, BLACK)
        pygame.display.update()
        time.sleep(2)
    # If the computer won, computer pokemon is displayed on the victory screen
    else:
        DISPLAYSURF.blit(endBackground, (0, 0))
        DISPLAYSURF.blit(computerImgList[0], (100, 375))
        drawText("The winner is " + cPokemon[0] + "!", font, TEXTSURF, 120, 100, BLACK)
        pygame.display.update()
        time.sleep(2)


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
        pStats = StatMod(pMove, pStats, pPokemon[0])
    elif mode == "22":
        cStats = StatMod(pMove, cStats, cPokemon[0])


def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerImgList, computerBar, playerImgList):
    displayMessage(
        cPokemon[0] + " used " + cMove[5] + ".",
        pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList
    )
    DISPLAYSURF.blit(background, (0, 0))
    time.sleep(1)
    mode = cMove[0]
    if mode == "1":
        pPokemon = DamageMod(cPokemon, cMove, pPokemon, cStats, pStats)
    elif mode == "21":
        cStats = StatMod(cMove, cStats, cPokemon[0])
    elif mode == "22":
        pStats = StatMod(cMove, pStats, pPokemon[0])


def DamageMod(attacker, attack, target, attackerStats, targetStats):
    typeAdvantage = AdvantageCalc(attack, target)  # Determine type advantage
    # Get values for calculation from stat lists
    DMG = int(attack[2])
    aATK = StatIndex(attackerStats, "A")
    tDEF = StatIndex(targetStats, "D")
    effect = DMG * (aATK / tDEF) * typeAdvantage  # Calculate actual damage effect
    target[1] = int(target[1]) - effect  # apply effect to the stat list for the target pokemon
    print(attacker[0] + " dealt", effect, "damage!")
    print("")
    # Return the stat list containing the new value for health after application of
    # damage effect.
    return target


def StatMod(move, targetStats, defenderName):
    targetStat = move[4]
    effect = move[3]
    if targetStat == "A":  # If target stat is attack...
        if effect == "-":  # And the effect is negative...
            targetStats[0] -= 1  # target's attack is lowered
            displayMessage(defenderName + "'s" + " Attack fell.")
            return targetStats
        else:  # and the ffect is positive...
            targetStats[0] += 1  # target's atack is raised
            displayMessage(defenderName + "'s" + " Attack rose.")
            return targetStats
    else:  # if target stat is defense...
        if effect == "-":  # and effect is negative...
            targetStats[1] -= 1  # target's defense is lowered
            displayMessage(defenderName + "'s" + " Defense fell.")
            return targetStats
        else:  # and the effect is positive...
            targetStats[1] += 1  # target's defense is raised
            displayMessage(defenderName + "'s" + " Defense rose.")
            # Function returns the new stat levels for the target pokemon
            return targetStats


def StatIndex(stats, statType):
    # The attack and defense stats in pokemon are dictated by a hard scale, running
    # from 1/4 to 4. The exact scale can be seen represented in the list in this function.
    # Unfortunately, there is no way to easily track the stats of a pokemon accurately
    # throughout the course of a battle. The purpose of this function is to transform a
    # much easier form of stat tracking into the real stat for the pokemon. The stats
    # are tracked in the battle as whole integer levels. Those levels are used as the
    # index location when this is called, allowing the tracking stat to correspond to
    # the true stat value.

    statIndex = [(1.0 / 4), (2.0 / 7), (1.0 / 3), (2.0 / 5), (1.0 / 2), (2.0 / 3), 1, 1.5, 2, 2.5, 3, 3.5, 4]
    # If statement simply directs the function to the correct tracking value when
    # quereied. One of the parameters is stat type, the conditional for the if statement.
    if statType == "A":
        statInQuestion = stats[0]
    else:
        statInQuestion = stats[1]
    # assigning the trueStat variable a value.
    trueStat = statIndex[statInQuestion + 5]
    # returns the true stat for use in the damage calculation
    return trueStat


def AdvantageCalc(attack, target):
    # Function that handles the calculation of the type advantage for any given attack.
    # Every move and every pokemon has a "Type". Some types are more effective against
    # others, leading to the addition of a multiplier to damage based moves. Function
    # makes a combination of the type keys for each move. The first letter in the combo
    # is the type of the attack, the second is the type key for the target recieving
    # the attack. A set of If statements takes the combo and determines the appropriate
    # type advantage.

    global typeAdvantage
    combo = attack[1] + target[3]  # Combinbing the type keys for the combo key

    # checking the combo key against known combinations.
    if combo == "FG":
        typeAdvantage = 2
    elif combo == "FW":
        typeAdvantage = .5
    elif combo == "FN":
        typeAdvantage = 1
    elif combo == "WF":
        typeAdvantage = 2
    elif combo == "WG":
        typeAdvantage = .5
    elif combo == "WN":
        typeAdvantage = 1
    elif combo == "GF":
        typeAdvantage = .5
    elif combo == "GW":
        typeAdvantage = 2
    elif combo == "GN":
        typeAdvantage = 1
    elif combo == "NF":
        typeAdvantage = 1
    elif combo == "NW":
        typeAdvantage = 1
    elif combo == "NG":
        typeAdvantage = 1
    # function returns the type advantage for use in the damage calculation
    return typeAdvantage

def main():
    global DISPLAYSURF, TEXTSURF, font, background, endBackground
    global button1, button2, button3, button4

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 600))
    TEXTSURF = pygame.display.set_mode((400, 600))
    pygame.display.set_caption('Pokemon')

    font = pygame.font.SysFont(None, 20)

    bulbImages = BulbImages()
    squirtImages = SquirtImages()
    charImages = CharImages()

    button_img = pygame.image.load("assets/button.png")
    background = pygame.image.load("assets/background.png")
    endBackground = pygame.image.load("assets/background.png")

    # --- Pokémon selection ---
    charButton = Button()
    charButton.assignImage(charImages[0])
    charButton.setCoords(0, 200)

    squirtButton = Button()
    squirtButton.assignImage(squirtImages[0])
    squirtButton.setCoords(200, 200)

    bulbButton = Button()
    bulbButton.assignImage(bulbImages[0])
    bulbButton.setCoords(100, 400)

    DISPLAYSURF.blit(background, (0, 0))
    charButton.drawButton(charImages[0])
    squirtButton.drawButton(squirtImages[0])
    bulbButton.drawButton(bulbImages[0])

    animateText("Choose your Pokemon...", font, TEXTSURF, 120, 100, BLACK)
    pygame.display.update()

    picked = False
    while not picked:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if charButton.pressed(mouse):
                    choice = "Charmander"
                    playerImgList = charImages
                    picked = True
                elif squirtButton.pressed(mouse):
                    choice = "Squirtle"
                    playerImgList = squirtImages
                    picked = True
                elif bulbButton.pressed(mouse):
                    choice = "Bulbasaur"
                    playerImgList = bulbImages
                    picked = True

    choices = ["Charmander", "Squirtle", "Bulbasaur"]
    choices.remove(choice)

    pPokemon, pMoveList = PlayerChoice(choice.lower() + ".txt")
    cPokemon, cMoveList, computerImgList = ComputerChoice(
        choices, charImages, bulbImages, squirtImages
    )

    playerBar = HealthBar()
    playerBar.init(200, 305)
    computerBar = HealthBar()
    computerBar.init(10, 35)

    button1 = Button(); button1.assignImage(button_img); button1.setCoords(2, 468)
    button2 = Button(); button2.assignImage(button_img); button2.setCoords(202, 468)
    button3 = Button(); button3.assignImage(button_img); button3.setCoords(2, 535)
    button4 = Button(); button4.assignImage(button_img); button4.setCoords(202, 535)

    Battle(
        pPokemon, pMoveList,
        cPokemon, cMoveList,
        playerImgList, computerImgList,
        playerBar, computerBar
    )

if __name__ == "__main__":
    main()
