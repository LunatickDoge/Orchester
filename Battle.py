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


def MoveStrip(pokemonList, moveNumber):
    # Function for stripping data from a move file and into a list.
    moveName = pokemonList[moveNumber + 3].lower() + '.txt'
    with open(moveName, 'r') as f:
        fileString = f.read()
        fileList = fileString.split('\n')
        i = 0
        moveList = []
        while i < 6:
            moveList.append(fileList[i])
            i += 1
        f.close()
    return moveList


def PokemonStrip(targetFile):
    # Function for stripping data from a pokemon file and into a list.
    with open(targetFile, 'r') as f:
        fileString = f.read()
        fileList = fileString.split('\n')
        i = 0
        targetList = []
        while i < 11:
            targetList.append(fileList[i])
            i += 1
        f.close()
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


def displayMessage(message):
    drawText(message, font, DISPLAYSURF, 10, 400, BLACK)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    time.sleep(1)
    DISPLAYSURF.blit(background, (0, 0))


def cMoveSelect(cMoveList):
    cMove = cMoveList[random.randint(0, 3)]
    return cMove


def pMoveSelect(pMoveList, pPokemon, button1, button2, button3, button4):
    # The player move select function. This function draws the instructions and the
    # buttons necessary to guide the player in selecting a move for their pokemon.

    # Redrawing background image to clear text
    DISPLAYSURF.blit(background, (0, 0))
    # Drawing the prompt in the text section
    drawText("What will " + pPokemon[0] + " do?", font, DISPLAYSURF, 10, 400, BLACK)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    # Drawing buttons for use in the move selection process. Buttons are separate
    # from the text on the button to allow the system to be completely modular
    button1.drawButton(button)
    drawMoveText(pMoveList[0][5], font, DISPLAYSURF, 100, 499, BLACK)
    button2.drawButton(button)
    drawMoveText(pMoveList[1][5], font, DISPLAYSURF, 300, 499, BLACK)
    button3.drawButton(button)
    drawMoveText(pMoveList[2][5], font, DISPLAYSURF, 100, 566, BLACK)
    button4.drawButton(button)
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

    def assignImage(self, picture):
        self.rect = picture.get_rect()

    def setCoords(self, x, y):
        self.rect.topleft = x, y

    def drawButton(self, picture):
        DISPLAYSURF.blit(picture, self.rect)

    def pressed(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


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
        pMove = pMoveSelect(pMoveList, button1, button2, button3, button4, button4)
        cMove = cMoveSelect(cMoveList)

        # If player stat is faster, player attack sequence executes before computer
        # attack sequence. Else, computer attack sequence attacks first.
        if pPokemon[2] < cPokemon[2]:
            # Execute attack sequence for player
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
            # Update the health bar if any changes have occured
            computerBar.updateBar(cPokemon)
            computerBar.drawRects()
            pygame.display.update()
            if cPokemon[1] <= 0:
                fainted = True
                winner = "Player"
                break  # break loop to end program
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if pPokemon[1] <= 0:
                fainted = True
                winner = "Computer"
                break
        else:
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
            playerBar.updateBar(pPokemon)
            playerBar.drawRects()
            pygame.display.update()
            if pPokemon[1] <= 0:
                fainted = True
                winner = "Computer"
                break
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
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


def pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats):
    # Function for applying the series of steps in the player attack sequence. Function
    # simply decides which move function to apply based on the mode of attack being used.
    # Mode 1 is a damage attack, 21 is a stat mod aimed at self, 22 is a stat mod aimed
    # at a target.
    DISPLAYSURF.blit(background, (0, 0))
    displayMessage(pPokemon[0] + " used " + pMove[5])
    time.sleep(1)
    mode = pMove[0]
    if mode == "1":
        cPokemon = DamageMod(pPokemon, pMove, cPokemon, pStats, cStats)
    elif mode == "21":
        pStats = StatMod(pMove, pStats, pPokemon[0])
    elif mode == "22":
        cStats = StatMod(pMove, cStats, cPokemon[0])


def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats):
    # Function handling the application of steps in computer attack. Only difference
    # from player attack sequence is that the parameters for target are aimed at the
    # player
    DISPLAYSURF.blit(background, (0, 0))
    displayMessage(cPokemon[0] + " used " + cMove[5] + ".")
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    # Pygame initialization statments. Defining basic attributes of game window
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 600))
    TEXTSURF = pygame.display.set_mode((400, 600))
    pygame.display.set_caption('Pokemon')
    fpsClock = pygame.time.Clock()
    FPS = 15
    font = pygame.font.SysFont(None, 20)

    bulbImages = BulbImages()  # Functions for loading each set of pokemon images
    bulbFront = bulbImages[0]
    bulbBack = bulbImages[1]
    squirtImages = SquirtImages()
    squirtFront = squirtImages[0]
    squirtBack = squirtImages[1]
    charImages = CharImages()
    charFront = charImages[0]
    charBack = charImages[1]
    button = pygame.image.load("assets/button.png")
    background = pygame.image.load("assets/background.png")
    endBackground = pygame.image.load("assets/background.png")

    charButton = Button()
    charButton.assignImage(charFront)
    charButton.setCoords(0, 200)
    squirtButton = Button()
    squirtButton.assignImage(squirtFront)
    squirtButton.setCoords(200, 200)
    bulbButton = Button()
    bulbButton.assignImage(bulbFront)
    bulbButton.setCoords(100, 400)

    # Drawing background and buttons for Pokemon selection screen
    DISPLAYSURF.blit(background, (0, 0))
    charButton.drawButton(charFront)
    squirtButton.drawButton(squirtFront)
    bulbButton.drawButton(bulbFront)

    animateText("Choose your Pokemon...", font, TEXTSURF, 120, 100, BLACK)
    pygame.display.update()

    picked = 0
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
                    picked = 1
                if squirtButton.pressed(mouse):
                    choice = "Squirtle"
                    playerImgList = squirtImages
                    picked = 1
                if bulbButton.pressed(mouse):
                    choice = "Bulbasaur"
                    playerImgList = bulbImages
                    picked = 1

    choices = ['Charmander', 'Squirtle', 'Bulbasaur']
    targetFile = choice.lower() + '.txt'
    choices.remove(choice)  # player choice is removed from the list so that the computer
    # cannot select a duplicate Pokemon.

    # This next block of code uses the player choice and a simple random choice
    # function to draw the stats of the pokemon selected for the computer and player.
    # More detail about the functions called in this block and be found in the Utility
    # functions section.
    playerChoice = PlayerChoice(targetFile)
    pPokemon = playerChoice[0]
    pMoveList = playerChoice[1]
    computerChoice = ComputerChoice(choices, bulbImages, squirtImages, charImages)
    cPokemon = computerChoice[0]
    cMoveList = computerChoice[1]
    computerImgList = computerChoice[2]
    button = pygame.image.load("button.png")

    playerBar = HealthBar()
    playerBar.init(200, 305)
    computerBar = HealthBar()
    computerBar.init(10, 35)

    button1 = Button()
    button1.assignImage(button)
    button1.setCoords(2, 468)
    button2 = Button()
    button2.assignImage(button)
    button2.setCoords(202, 468)
    button3 = Button()
    button3.assignImage(button)
    button3.setCoords(2, 535)
    button4 = Button()
    button4.assignImage(button)
    button4.setCoords(202, 535)

    Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList, playerBar, computerBar)