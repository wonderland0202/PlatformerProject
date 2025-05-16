import pygame
import os

from player import Player
from menuButton import MenuButton
from gameObject import collisionObject

pygame.init()

# Global constants
WIDTH, HEIGHT = 1450, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
FPS = 144
gameState = "startScreen"
font = pygame.font.SysFont("Consolas", 24)
running = True

# Player's current level and screen
with open("Player-Data\\CurrentPlayerLevel.txt") as level:
    playerLevel = int(level.read())

with open("Player-Data\\CurrentPlayerScreen.txt") as currScreen:
    playerScreen = int(currScreen.read())


def openStartScreen():
    global gameState
    startScreenRunning = True
    menuIndex = 0

    # Buttons
    menuContinueButton = MenuButton(WIDTH / 2, HEIGHT / 3, WIDTH / 5, HEIGHT / 5,
                                    "Images\\Buttons\\placeholderButton.png",
                                    "Images\\Buttons\\placeholderButton-Selected.png")
    menuLevelsButton = MenuButton(WIDTH / 2, 7 * HEIGHT / 12, WIDTH / 7, HEIGHT / 7,
                                  "Images\\Buttons\\placeholderButton.png",
                                  "Images\\Buttons\\placeholderButton-Selected.png")
    menuQuitButton = MenuButton(WIDTH / 2, 9 * HEIGHT / 12, WIDTH / 8, HEIGHT / 8,
                                "Images\\Buttons\\placeholderButton.png",
                                "Images\\Buttons\\placeholderButton-Selected.png")
    menuSettingsButton = MenuButton(12 * WIDTH / 13, HEIGHT / 13, WIDTH / 10, WIDTH / 10,
                                    "Images\\Buttons\\placeholderButton.png",
                                    "Images\\Buttons\\placeholderButton-Selected.png")

    menuContinueButton.highlight()
    buttonGroup = pygame.sprite.Group(menuContinueButton, menuLevelsButton, menuQuitButton, menuSettingsButton)
    bgMenuImage = pygame.image.load("Images\\Backgrounds\\BGPH.png").convert_alpha()
    bgMenuImage = pygame.transform.scale(bgMenuImage, (WIDTH, HEIGHT))

    while startScreenRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                startScreenRunning = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameState = "endGame"
                    startScreenRunning = False
                    continue
                if event.key == pygame.K_DOWN:
                    if menuIndex == 0:
                        menuIndex += 1
                        menuSettingsButton.unhighlight()
                        menuContinueButton.highlight()
                    elif menuIndex == 1:
                        menuIndex += 1
                        menuContinueButton.unhighlight()
                        menuLevelsButton.highlight()
                    elif menuIndex == 2:
                        menuIndex += 1
                        menuLevelsButton.unhighlight()
                        menuQuitButton.highlight()
                if event.key == pygame.K_UP:
                    if menuIndex == 3:
                        menuIndex -= 1
                        menuQuitButton.unhighlight()
                        menuLevelsButton.highlight()
                    elif menuIndex == 2:
                        menuIndex -= 1
                        menuLevelsButton.unhighlight()
                        menuContinueButton.highlight()
                    elif menuIndex == 1:
                        menuIndex -= 1
                        menuContinueButton.unhighlight()
                        menuSettingsButton.highlight()
                if event.key == pygame.K_SPACE:
                    if menuIndex == 0:
                        gameState = "settingsMenu"
                    elif menuIndex == 1:
                        gameState = "gamePlay"
                    elif menuIndex == 2:
                        gameState = "levelsMenu"
                    elif menuIndex == 3:
                        gameState = "endGame"
                    startScreenRunning = False
                    continue

        screen.blit(bgMenuImage, (0, 0))
        buttonGroup.draw(screen)
        clock.tick(FPS)
        pygame.display.update()


def openGamePlay(level):
    global gameState
    gameLoopRunning = True

    if level == 1:
        bgImage, playerCharacter, levelData, playerGroup = levelOneData()
    elif level == 2:
        bgImage, playerCharacter, levelData = levelTwoData()

    xValPixelated = 0
    yValPixelated = 0
    gameTileGroup = pygame.sprite.Group()
    collisionObjects = pygame.sprite.Group()

    for i in range(len(levelData)):
        collisionVal = True
        char = levelData[i]
        objectIdentity = {
            " ": "Levels/LevelMakeup/EmptyTile.png",
            "W": "Levels/LevelMakeup/LeftWallLine.png",
            "F": "Levels/LevelMakeup/FloorLine.png",
            "Q": "Levels/LevelMakeup/RightWallLine.png",
            "A": "Levels/LevelMakeup/InnerBuilding.png",
            "C": "Levels/LevelMakeup/CeilingLine.png",
            "V": "Levels/LevelMakeup/WallToFloor-Up.png",
            "M": "Levels/LevelMakeup/FloorToWall-Down.png",
            "N": "Levels/LevelMakeup/FloorToWall-Up.png",
            "P": "Levels/LevelMakeup/CeilingToWall-Up.png",
            "I": "Levels/LevelMakeup/WallToCeiling-Up.png",
            "B": "Levels/LevelMakeup/FacingUpFan.png"
        }.get(char, "Levels/LevelMakeup/EmptyTile.png")

        if char == " ":
            collisionVal = False

        newGameTile = collisionObject(xValPixelated * WIDTH / 14, yValPixelated * HEIGHT / 9,
                                      WIDTH / 14, HEIGHT / 9, objectIdentity, collisionVal, char)
        gameTileGroup.add(newGameTile)
        if collisionVal:
            collisionObjects.add(newGameTile)

        if char != 'O':
            xValPixelated += 1
        if xValPixelated > 14:
            xValPixelated = 0
            yValPixelated += 1

    while gameLoopRunning:
        playerCharacter.holdPos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                gameLoopRunning = False
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gameState = "endGame"
                gameLoopRunning = False
                continue

        fps = int(clock.get_fps())
        fpsText = font.render(f"FPS: {fps}", True, (0, 0, 0))

        playerCharacter.update(HEIGHT, WIDTH, collisionObjects, playerCharacter)

        screen.blit(bgImage, (0, 0))
        gameTileGroup.draw(screen)
        screen.blit(playerCharacter.image, playerCharacter.rect)
        screen.blit(fpsText, (WIDTH / 145, HEIGHT / 90))

        clock.tick(FPS)
        pygame.display.update()


def levelOneData():
    playerGroup = pygame.sprite.Group()
    bgLevel1Image = pygame.image.load("Images\\Backgrounds\\l1bgph.png").convert_alpha()
    bgLevel1Image = pygame.transform.scale(bgLevel1Image, (WIDTH, HEIGHT))
    playerCharacter = Player(WIDTH / 14, 7 * HEIGHT / 9, 100 / 3, 50,
                             "Images\\Player\\placeholderPlayer.png", 20, 2, 5, 50, 1, 30, 500, 0.9)
    playerGroup.add(playerCharacter)
    levelData = makeLevel("1", str(playerScreen))
    return bgLevel1Image, playerCharacter, levelData, playerGroup


def levelTwoData():
    bgLevel2Image = pygame.image.load("Images\\Backgrounds\\BGPH.png").convert_alpha()
    bgLevel2Image = pygame.transform.scale(bgLevel2Image, (WIDTH, HEIGHT))
    playerCharacter = Player(10, 860, 20, 50,
                             "Images\\Player\\placeholderPlayer.png", 20, 2, 5, 50, 1, 30, 500, 0.9)
    levelData = makeLevel("2", str(playerScreen))
    return bgLevel2Image, playerCharacter, levelData


def makeLevel(levelNum, screenNum):
    with open(f"Levels/Level1Screens/Level{levelNum}Screen{screenNum}.txt") as levelToLoad:
        return levelToLoad.read()


def incrementLevel():
    with open("Player-Data\\CurrentPlayerLevel.txt", "r+") as currLevel:
        level = int(currLevel.read())
        currLevel.seek(0)
        currLevel.write(str(level + 1))
        currLevel.truncate()


def incrementScreen():
    with open("Player-Data\\CurrentPlayerScreen.txt", "r+") as currScreen:
        screen = int(currScreen.read())
        currScreen.seek(0)
        currScreen.write(str(screen + 1))
        currScreen.truncate()


def openPauseMenu():
    pass


def openLoseScreen():
    pass


def openLevelsMenu():
    print("Levels menu not implemented yet.")


def openSettingsMenu():
    print("Settings menu not implemented yet.")


while running:
    if gameState == "startScreen":
        openStartScreen()
    elif gameState == "gamePlay":
        with open("Player-Data\\CurrentPlayerLevel.txt") as level:
            playerLevel = int(level.read())
        openGamePlay(playerLevel)
    elif gameState == "paused":
        openPauseMenu()
    elif gameState == "loseScreen":
        openLoseScreen()
    elif gameState == "levelsMenu":
        openLevelsMenu()
    elif gameState == "settingsMenu":
        openSettingsMenu()
    elif gameState == "endGame":
        running = False

pygame.quit()
