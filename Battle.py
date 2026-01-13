import pygame
import os
import sys
import time
import random
from pygame.locals import *
import socket
import threading
import json

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
    moveName = pokemonList[moveNumber + 3].lower() + '.txt'
    movePath = os.path.join("data", moveName)
    with open(movePath, 'r') as f:
        fileList = f.read().split('\n')
    moveList = []
    for i in range(6):
        moveList.append(fileList[i])
    return moveList

def PokemonStrip(targetFile):
    file_path = os.path.join("data", targetFile)
    with open(file_path, 'r') as f:
        fileString = f.read()
        fileList = fileString.split('\n')
    targetList = []
    for i in range(11):
        targetList.append(fileList[i])
    return targetList

def drawText(text, font, surface, x, y, color):
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

def displayMessage(message, pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList):
    drawText(message, font, DISPLAYSURF, 10, 400, BLACK)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
    time.sleep(1)
    DISPLAYSURF.blit(background, (0, 0))

def pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList,
                button1, button2, button3, button4, cPokemon):
    global Move
    DISPLAYSURF.blit(background, (0, 0))
    drawText("What will " + pPokemon[0] + " do?", font, DISPLAYSURF, 10, 400, BLACK)
    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)
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
                if button1.pressed(mouse):
                    Move = pMoveList[0]
                    picked = 1
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
    def __init__(self):
        self.position = None
        self.negDimensions = None
        self.posDimensions = None
    def init(self, x, y):
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
        pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
        pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
        pygame.display.update()

class Button():
    def __init__(self):
        self.rect = None
        self.image = None
    def assignImage(self, picture):
        self.rect = picture.get_rect()
        self.image = picture
    def setCoords(self, x, y):
        self.rect.topleft = x, y
    def drawButton(self, picture=None):
        if picture is None:
            picture = self.image
        DISPLAYSURF.blit(picture, self.rect)
    def pressed(self, mouse):
        return self.rect.collidepoint(mouse)

def PlayerChoice(targetFile):
    pPokemon = PokemonStrip(targetFile)
    moveNumber = 1
    pAttackList = []
    while moveNumber < 5:
        pAttackList.append(MoveStrip(pPokemon, moveNumber))
        moveNumber += 1
    return [pPokemon, pAttackList]

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

def Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList, playerBar, computerBar, sock=None,
           server=None):
    global winner
    pStats = [6, 6] 
    cStats = [6, 6]
    fainted = False
    winner = None

    redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    while not fainted:
        pMove = pMoveSelect(pMoveList, pPokemon, playerBar, computerBar, playerImgList, computerImgList, button1,
                            button2, button3, button4, cPokemon)

        if sock and server:
                move_index = pMoveList.index(pMove)
                sock.sendto(f"MOVE:{move_index}".encode(), server)
                drawText("Waiting for opponent's move...", font, DISPLAYSURF, 10, 400, BLACK)
                
                sock.settimeout(10.0)
                while True:
                    data, _ = sock.recvfrom(1024)
                    msg = data.decode()
                    if msg.startswith("OPPONENT_MOVE:"):
                        opp_move_idx = int(msg.split(":")[1])
                        cMove = cMoveList[opp_move_idx]
                        break
                sock.settimeout(None)
        else:
            cMove = random.choice(cMoveList)

        if int(pPokemon[2]) >= int(cPokemon[2]):
            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList, computerImgList)
            if int(cPokemon[1]) <= 0:
                fainted = True
                winner = "Player"
                break
        
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar, computerImgList, playerImgList)
            if int(pPokemon[1]) <= 0:
                fainted = True
                winner = "Opponent"
                break
        else:
            cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar, computerImgList, playerImgList)
            if int(pPokemon[1]) <= 0:
                fainted = True
                winner = "Opponent"
                break

            pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats, playerBar, computerBar, playerImgList, computerImgList)
            if int(cPokemon[1]) <= 0:
                fainted = True
                winner = "Player"
                break
    
        redraw(pPokemon, playerBar, computerImgList, cPokemon, computerBar, playerImgList)

    if int(pPokemon[1]) <= 0 and int(cPokemon[1]) <= 0:
        winner = "Draw"

    DISPLAYSURF.blit(endBackground, (0, 0))
    if winner == "Player":
        DISPLAYSURF.blit(playerImgList[0], (100, 375))
        drawText("Victory! " + pPokemon[0] + " won!", font, DISPLAYSURF, 120, 100, BLACK)
    elif winner == "Opponent":
        DISPLAYSURF.blit(computerImgList[0], (100, 375))
        drawText(cPokemon[0] + " is the winner!", font, DISPLAYSURF, 120, 100, BLACK)
    else:
        drawText("It's a DRAW!", font, DISPLAYSURF, 150, 100, BLACK)

    pygame.display.update()
    time.sleep(3)

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
        pStats = StatMod(pMove, pStats, pPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar,
                         playerImgList)
    elif mode == "22":
        cStats = StatMod(pMove, cStats, cPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar,
                         playerImgList)

def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats, playerBar, computerBar, computerImgList, playerImgList):
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
        cStats = StatMod(cMove, cStats, cPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar,
                         playerImgList)
    elif mode == "22":
        pStats = StatMod(cMove, pStats, pPokemon[0], pPokemon, playerBar, computerImgList, cPokemon, computerBar,
                         playerImgList)

def DamageMod(attacker, attack, target, attackerStats, targetStats):
    typeAdvantage = AdvantageCalc(attack, target)
    DMG = int(attack[2])
    aATK = StatIndex(attackerStats, "A")
    tDEF = StatIndex(targetStats, "D")
    effect = DMG * (aATK / tDEF) * typeAdvantage
    target[1] = int(target[1]) - effect
    print(attacker[0] + " dealt", effect, "damage!")
    print("")
    return target

def StatMod(move, targetStats, defenderName, pPokemon, playerBar, computerImgList, cPokemon, computerBar,
            playerImgList):
    targetStat = move[4]
    effect = move[3]
    if targetStat == "A":
        if effect == "-":
            if targetStats[0] > -5:
                targetStats[0] -= 1
                displayMessage(defenderName + "'s Attack fell.", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            else:
                displayMessage(defenderName + "'s Attack won't go lower!", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            return targetStats
        else:
            if targetStats[0] < 7:
                targetStats[0] += 1
                displayMessage(defenderName + "'s Attack rose.", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            else:
                displayMessage(defenderName + "'s Attack won't go higher!", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            return targetStats
    else:
        if effect == "-":
            if targetStats[1] > -5:
                targetStats[1] -= 1
                displayMessage(defenderName + "'s Defense fell.", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            else:
                displayMessage(defenderName + "'s Defense won't go lower!", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            return targetStats
        else:
            if targetStats[1] < 7:
                targetStats[1] += 1
                displayMessage(defenderName + "'s Defense rose.", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            else:
                displayMessage(defenderName + "'s Defense won't go higher!", pPokemon, playerBar, computerImgList, cPokemon,
                               computerBar, playerImgList)
            return targetStats

def StatIndex(stats, statType):
    statIndex = [(1.0 / 4), (2.0 / 7), (1.0 / 3), (2.0 / 5), (1.0 / 2), (2.0 / 3), 1, 1.5, 2, 2.5, 3, 3.5, 4]
    if statType == "A":
        statInQuestion = stats[0]
    else:
        statInQuestion = stats[1]
    trueStat = statIndex[statInQuestion + 5]
    return trueStat

def AdvantageCalc(attack, target):
    global typeAdvantage
    combo = attack[1] + target[3]
    if attack[1] == target[3]:
        return 1
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
    return typeAdvantage

def main(sock=None, server=None):
    global DISPLAYSURF, TEXTSURF, font, background, endBackground, playerImgList, choice
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
    if sock and server:
        # Pošleme náš výber
        sock.sendto(f"PICK:{choice}".encode(), server)
        drawText("Waiting for opponent...", font, DISPLAYSURF, 10, 450, BLACK)

        opp_choice = None
        sock.settimeout(None)
        while opp_choice is None:
            try:
                # Nastavíme malý timeout na čítanie, aby sme mohli spracovať eventy okna
                sock.settimeout(0.1)
                data, _ = sock.recvfrom(1024)
                msg = data.decode()
                if msg.startswith("OPPONENT_PICK:"):
                    opp_choice = msg.split(":")[1]
            except socket.timeout:
                # Ak nič neprišlo, skontrolujeme, či používateľ nezavrel okno
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                continue
        sock.settimeout(None) # Vrátime do normálu
    else:
        opp_choice = "Bulbasaur" if choice != "Bulbasaur" else "Squirtle"
    if opp_choice == "Charmander":
        computerImgList = charImages
    elif opp_choice == "Bulbasaur":
        computerImgList = bulbImages
    else:
        computerImgList = squirtImages
    pPokemon, pMoveList = PlayerChoice(choice.lower() + ".txt")
    cPokemon, cMoveList = PlayerChoice(opp_choice.lower() + ".txt")
    playerBar = HealthBar()
    playerBar.init(200, 305)
    computerBar = HealthBar()
    computerBar.init(10, 35)
    button1 = Button()
    button1.assignImage(button_img)
    button1.setCoords(2, 468)
    button2 = Button()
    button2.assignImage(button_img)
    button2.setCoords(202, 468)
    button3 = Button()
    button3.assignImage(button_img)
    button3.setCoords(2, 535)
    button4 = Button()
    button4.assignImage(button_img)
    button4.setCoords(202, 535)
    Battle(
        pPokemon, pMoveList,
        cPokemon, cMoveList,
        playerImgList, computerImgList,
        playerBar, computerBar,
        sock, server
    )

def wait_for_start():
    server_ip = input("Server IP: ")
    server = (server_ip, 5678)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    sock.sendto("JOIN".encode(), server)
    print("Waiting for second player...")
    while True:
        data, _ = sock.recvfrom(1024)
        msg = data.decode()
        if msg == "START":
            print("Battle starting!")
            break

if __name__ == "__main__":
    wait_for_start()
    main()
