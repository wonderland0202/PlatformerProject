import pygame
import math

from player import Player
from menuButton import MenuButton
from collisionObject import collisionObject

pygame.init()

# Global constants
scrSize = pygame.display.Info()
WIDTH, HEIGHT = scrSize.current_w, scrSize.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
FPS = 144
gameState = "startScreen"
font = pygame.font.SysFont("Consolas", 24)
running = True
needBuild = True
prevT = None

# Player's current level and screen
with open("Player-Data\\CurrentPlayerLevel.txt") as level:
    playerLevel = int(level.read())

with open("Player-Data\\CurrentPlayerScreen.txt") as currScreen:
    playerScreen = int(currScreen.read())


def openStartScreen():
    global gameState, needBuild
    startScreenRunning = True
    mainMenuIndex = 0

    titleImage = pygame.image.load("Images\\TitleScreen\\TitleImage.png").convert_alpha()
    titleImage = pygame.transform.scale(titleImage, (WIDTH / 3, HEIGHT / 10))
    titlePos = 0
    titlePosMult = 1

    # Buttons
    mainMenuContinueButton = MenuButton(WIDTH / 2, HEIGHT / 3, WIDTH / 5, HEIGHT / 5,
                                    "Images\\Buttons\\placeholderButton.png",
                                    "Images\\Buttons\\placeholderButton-Selected.png")
    mainMenuLevelsButton = MenuButton(WIDTH / 2, 7 * HEIGHT / 12, WIDTH / 7, HEIGHT / 7,
                                  "Images\\Buttons\\placeholderButton.png",
                                  "Images\\Buttons\\placeholderButton-Selected.png")
    mainMenuQuitButton = MenuButton(WIDTH / 2, 9 * HEIGHT / 12, WIDTH / 8, HEIGHT / 8,
                                "Images\\Buttons\\placeholderButton.png",
                                "Images\\Buttons\\placeholderButton-Selected.png")
    mainMenuSettingsButton = MenuButton(12 * WIDTH / 13, HEIGHT / 13, WIDTH / 10, WIDTH / 10,
                                    "Images\\Buttons\\placeholderButton.png",
                                    "Images\\Buttons\\placeholderButton-Selected.png")

    mainMenuContinueButton.highlight()
    mainMenuButtonGroup = pygame.sprite.Group(mainMenuContinueButton, mainMenuLevelsButton, mainMenuQuitButton, mainMenuSettingsButton)
    bgMenuImage = pygame.image.load("Images\\Backgrounds\\BGPH.png").convert_alpha()
    bgMenuImage = pygame.transform.scale(bgMenuImage, (WIDTH, HEIGHT))


    while startScreenRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                startScreenRunning = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    gameState = "endGame"
                    startScreenRunning = False
                    continue
                if event.key == pygame.K_DOWN:
                    if mainMenuIndex == 0:
                        mainMenuIndex += 1
                        mainMenuSettingsButton.unhighlight()
                        mainMenuContinueButton.highlight()
                    elif mainMenuIndex == 1:
                        mainMenuIndex += 1
                        mainMenuContinueButton.unhighlight()
                        mainMenuLevelsButton.highlight()
                    elif mainMenuIndex == 2:
                        mainMenuIndex += 1
                        mainMenuLevelsButton.unhighlight()
                        mainMenuQuitButton.highlight()
                if event.key == pygame.K_UP:
                    if mainMenuIndex == 3:
                        mainMenuIndex -= 1
                        mainMenuQuitButton.unhighlight()
                        mainMenuLevelsButton.highlight()
                    elif mainMenuIndex == 2:
                        mainMenuIndex -= 1
                        mainMenuLevelsButton.unhighlight()
                        mainMenuContinueButton.highlight()
                    elif mainMenuIndex == 1:
                        mainMenuIndex -= 1
                        mainMenuContinueButton.unhighlight()
                        mainMenuSettingsButton.highlight()
                if event.key == pygame.K_SPACE:
                    if mainMenuIndex == 0:
                        gameState = "settingsMenu"
                    elif mainMenuIndex == 1:
                        needBuild = True
                        gameState = "gamePlay"
                    elif mainMenuIndex == 2:
                        gameState = "levelsMenu"
                    elif mainMenuIndex == 3:
                        gameState = "endGame"
                    startScreenRunning = False
                    continue

        if titlePos >= 1:
            titlePosMult = -1
        elif titlePos <= -1:
            titlePosMult = 1

        titlePos += 0.02 * titlePosMult

        screen.blit(bgMenuImage, (0, 0))
        screen.blit(titleImage, ((WIDTH / 2 - (titleImage.get_width() / 2)), 30 * math.sin(titlePos) + (HEIGHT / 15)))
        mainMenuButtonGroup.draw(screen)
        clock.tick(FPS)
        pygame.display.update()


def openGamePlay(level):
    global gameState, playerScreen, needBuild, prevT

    playerCharacter = Player(2 * WIDTH / 14, 7 * HEIGHT / 9, WIDTH / 28, HEIGHT / 14,
                             "Images\\Player\\placeholderPlayer.png", HEIGHT / 100, WIDTH / 200, WIDTH / 5,  500, HEIGHT / 4000, WIDTH / 400)

    gameLoopRunning = True

    while gameLoopRunning:
        if needBuild:
            collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter)
            needBuild = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("Player-Data/CurrentPlayerScreen.txt", "w") as screenNumHolder:
                    screenNumHolder.write(str(playerScreen))
                with open("Player-Data/CurrentPlayerLevel.txt", "w") as levelNumHolder:
                    levelNumHolder.write(str(level))
                gameState = "endGame"
                gameLoopRunning = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    gameState = "endGame"
                    gameLoopRunning = False
                    continue
                if event.key == pygame.K_ESCAPE:
                    gameState = "paused"
                    gameLoopRunning = False
                    continue

        fps = int(clock.get_fps())
        fpsText = font.render(f"FPS: {fps}", True, (0, 0, 0))

        playerCharacter.update(HEIGHT, WIDTH, collisionObjects, playerCharacter, fanAirGroup)
        transition = playerCharacter.boundCheck(WIDTH, HEIGHT)


        if prevT != transition:

            # Handle screen transition
            if transition == "SCREENUP":
                print("scrUP")
                playerScreen += 1
                playerCharacter.currScreen = playerScreen
                print(playerScreen, playerCharacter.currScreen)
                collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter)
                needBuild = True
                playerCharacter.origPos = playerCharacter.rect.center
                playerCharacter.transitionVal = None

            elif transition == "SCREENDOWN":
                if playerScreen > 1:
                    playerScreen -= 1
                    playerCharacter.currScreen = playerScreen
                    collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter)
                    playerCharacter.origPos = playerCharacter.rect.center
                else:
                    # Prevent screen change on screen 1
                    playerCharacter.rect.left = 0
                playerCharacter.transitionVal = None


        prevT = transition

        screen.blit(bgImage, (0, 0))
        gameTileGroup.draw(screen)
        screen.blit(playerCharacter.image, playerCharacter.rect)
        screen.blit(fpsText, (WIDTH / 145, HEIGHT / 90))

        clock.tick(FPS)
        pygame.display.update()



def buildLevel(level, screen, playerCharacter):
    if level == 1:
        bgImage, levelData = levelOneData(screen, playerCharacter)
    elif level == 2:
        bgImage, playerCharacter, levelData = levelTwoData(screen)

    xValPixelated = 0
    yValPixelated = 0
    gameTileGroup = pygame.sprite.Group()
    collisionObjects = pygame.sprite.Group()
    fanAirGroup = pygame.sprite.Group()
    gameTileGroup.empty()

    for i in range(len(levelData)):
        collisionVal = True
        char = levelData[i]
        x = xValPixelated * WIDTH / 14
        y = yValPixelated * HEIGHT / 9

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
            "B": "Levels/LevelMakeup/FacingUpFan.png",
            "T": "Levels/LevelMakeup/WallToFloor-Down.png"
        }.get(char, "Levels/LevelMakeup/EmptyTile.png")

        if char == " " or char == "O":
            collisionVal = False



        if char == "B":
            for offset in range(1, 4):  # 3 tiles above
                airY = y - offset * (HEIGHT / 9)
                fanAir = collisionObject(x, airY, WIDTH / 14, HEIGHT / 9, "Levels/LevelMakeup/FanAir.png", False, "fanAir")
                fanAirGroup.add(fanAir)
                gameTileGroup.add(fanAir)
        newGameTile = collisionObject(x, y, WIDTH / 14, HEIGHT / 9, objectIdentity, collisionVal, char)
        gameTileGroup.add(newGameTile)
        if collisionVal:
            collisionObjects.add(newGameTile)
        if char != 'O':
            xValPixelated += 1
        if xValPixelated > 14:
            xValPixelated = 0
            yValPixelated += 1



    return collisionObjects, fanAirGroup, bgImage, gameTileGroup


def levelOneData(screen, playerCharacter):
    playerCharacter.currLevel = 1
    playerCharacter.currScreen = screen
    bgLevel1Image = pygame.image.load("Images\\Backgrounds\\l1bgph.png").convert_alpha()
    bgLevel1Image = pygame.transform.scale(bgLevel1Image, (WIDTH, HEIGHT))
    levelData = makeLevel("1", str(screen))
    return bgLevel1Image, levelData


def levelTwoData(screen):
    playerCharacter = Player(4 * WIDTH / 14, 7 * HEIGHT / 9, 100 / 3, 50,
                             "Images\\Player\\placeholderPlayer.png", 15, 5, 50, 1, 30, 500, 0.9, 5)
    playerCharacter.currLevel = 2
    playerCharacter.currScreen = screen
    bgLevel2Image = pygame.image.load("Images\\Backgrounds\\BGPH.png").convert_alpha()
    bgLevel2Image = pygame.transform.scale(bgLevel2Image, (WIDTH, HEIGHT))
    levelData = makeLevel("2", str(screen))
    return bgLevel2Image, playerCharacter, levelData



def makeLevel(levelNum, screenNum):
    with open(f"Levels/Level{levelNum}Screens/Level{levelNum}Screen{screenNum}.txt") as levelToLoad:
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
    global gameState, needBuild
    pauseMenuRunning = True
    pauseMenuIndex = 0

    pauseMenuContinueButton = MenuButton(WIDTH / 2, HEIGHT / 3, WIDTH / 5, HEIGHT / 5,
                                        "Images\\Buttons\\placeholderButton.png",
                                        "Images\\Buttons\\placeholderButton-Selected.png")
    pauseMenuMainMenuButton = MenuButton(WIDTH / 2, 7 * HEIGHT / 12, WIDTH / 7, HEIGHT / 7,
                                      "Images\\Buttons\\placeholderButton.png",
                                      "Images\\Buttons\\placeholderButton-Selected.png")

    pauseMenuContinueButton.highlight()
    mainMenuButtonGroup = pygame.sprite.Group(pauseMenuContinueButton, pauseMenuMainMenuButton)

    while pauseMenuRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                pauseMenuRunning = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    gameState = "endGame"
                    pauseMenuRunning = False
                    continue
                if event.key == pygame.K_DOWN:
                    if pauseMenuIndex == 0:
                        pauseMenuIndex += 1
                        pauseMenuContinueButton.unhighlight()
                        pauseMenuMainMenuButton.highlight()
                if event.key == pygame.K_UP:
                    if pauseMenuIndex == 1:
                        pauseMenuIndex -= 1
                        pauseMenuMainMenuButton.unhighlight()
                        pauseMenuContinueButton.highlight()
                if event.key == pygame.K_SPACE:
                    if pauseMenuIndex == 0:
                        needBuild = True
                        gameState = "gamePlay"
                    elif pauseMenuIndex == 1:
                        gameState = "startScreen"
                    pauseMenuRunning = False
                    continue

        mainMenuButtonGroup.draw(screen)
        clock.tick(FPS)
        pygame.display.update()


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
    elif gameState == "levelsMenu":
        openLevelsMenu()
    elif gameState == "settingsMenu":
        openSettingsMenu()
    elif gameState == "endGame":
        running = False

pygame.quit()
