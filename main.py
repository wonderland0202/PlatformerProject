import pygame

from player import Player
from menuButton import MenuButton
from gameObject import collisionObject

pygame.init()

#Always Global

WIDTH, HEIGHT = 1450, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
FPS = 144
gameState = "startScreen"
font = pygame.font.SysFont("Consolas", 24)


running = True

#Player's current level
with open("Player-Data\CurrentPlayerLevel.txt") as level:
    playerLevel = int(level.read())

with open("Player-Data\CurrentPlayerScreen.txt") as currScreen:
    playerScreen = int(currScreen.read())

def openStartScreen():
    global WIDTH, HEIGHT, screen, clock, FPS, gameState, pygame
    startScreenRunning = True
    menuIndex = 0

    menuContinueButton = MenuButton(WIDTH / 2, HEIGHT / 3, WIDTH / 5, HEIGHT / 5, "Images\Buttons\placeholderButton.png", "Images\Buttons\placeholderButton-Selected.png") #h: 1/3
    menuLevelsButton = MenuButton(WIDTH / 2, 7 * HEIGHT / 12, WIDTH / 7, HEIGHT / 7, "Images\Buttons\placeholderButton.png", "Images\Buttons\placeholderButton-Selected.png") #h: 7/12
    menuQuitButton = MenuButton(WIDTH / 2, 9 * HEIGHT / 12, WIDTH / 8, HEIGHT / 8, "Images\Buttons\placeholderButton.png", "Images\Buttons\placeholderButton-Selected.png") #h: 9 / 12
    menuSettingsButton = MenuButton(12 * WIDTH / 13, HEIGHT / 13, WIDTH / 10, WIDTH / 10, "Images\Buttons\placeholderButton.png","Images\Buttons\placeholderButton-Selected.png")

    # So menuContinueButton starts highlighted
    menuContinueButton.highlight()

    buttonGroup = pygame.sprite.Group()

    buttonGroup.add(menuContinueButton)
    buttonGroup.add(menuLevelsButton)
    buttonGroup.add(menuQuitButton)
    buttonGroup.add(menuSettingsButton)

    bgMenuImage = pygame.image.load("Images\Backgrounds\BGPH.png").convert_alpha()
    bgMenuImage = pygame.transform.scale(bgMenuImage, (WIDTH, HEIGHT))

    while startScreenRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                startScreenRunning = False
                continue
            # Key Checks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameState = "endGame"
                    startScreenRunning = False
                    continue

                # Menu Highlight / Selection Change
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
                #---

                # Menu Selection Interactions
                if event.key == pygame.K_SPACE:
                    if menuIndex == 0:
                        gameState = "settingsMenu"
                        startScreenRunning = False
                        continue

                    elif menuIndex == 1:
                        gameState = "gamePlay"
                        startScreenRunning = False
                        continue

                    elif menuIndex == 2:
                        gameState = "levelsMenu"
                        startScreenRunning = False
                        continue

                    elif menuIndex == 3:
                        gameState = "endGame"
                        startScreenRunning = False
                        continue
                #---

        screen.blit(bgMenuImage, (0, 0))

        buttonGroup.draw(screen)

        clock.tick(FPS)
        pygame.display.update()


def openGamePlay(level):
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState, font
    gameLoopRunning = True

    if level == 1:
        bgImage, playerCharacter, levelData = levelOneData()
        print(level)
    elif level == 2:
        bgImage, playerCharacter, levelData = levelTwoData()
        print(level)

    print(levelData)
    xValPixelated = 0
    yValPixelated = 0
    gameTileGroup = pygame.sprite.Group()
    for i in range(len(levelData)):
        collisionVal = True
        if levelData[i] == " ":
            objectIdentity = "Levels/LevelMakeup/EmptyTile.png"
            collisionVal = False
        elif levelData[i] == "W":
            objectIdentity = "Levels/LevelMakeup/LeftWallLine.png"
        elif levelData[i] == "F":
            objectIdentity = "Levels/LevelMakeup/FloorLine.png"
        elif levelData[i] == "Q":
            objectIdentity = "Levels/LevelMakeup/RightWallLine.png"
        elif levelData[i] == "A":
            objectIdentity = "Levels/LevelMakeup/InnerBuilding.png"
        elif levelData[i] == "C":
            objectIdentity = "Levels/LevelMakeup/CeilingLine.png"
        elif levelData[i] == "V":
            objectIdentity = "Levels/LevelMakeup/WallToFloor-Up.png"
        elif levelData[i] == "M":
            objectIdentity = "Levels/LevelMakeup/FloorToWall-Down.png"
        elif levelData[i] == "N":
            objectIdentity = "Levels/LevelMakeup/FloorToWall-Up.png"
        elif levelData[i] == "P":
            objectIdentity = "Levels/LevelMakeup/CeilingToWall-Up.png"
        elif levelData[i] == "I":
            objectIdentity = "Levels/LevelMakeup/WallToCeiling-Up.png"
        elif levelData[i] == "B":
            objectIdentity = "Levels/LevelMakeup/FacingUpFan.png"

        newGameTile = collisionObject(xValPixelated * WIDTH / 14, yValPixelated * HEIGHT / 9, WIDTH / 14, HEIGHT / 9,objectIdentity, collisionVal)
        print(f"Done: {i}")

        gameTileGroup.add(newGameTile)

        if levelData[i] != 'O':
            xValPixelated += 1
        if xValPixelated > 14:
            xValPixelated = 0
            yValPixelated += 1

    while gameLoopRunning:
        Player.holdPos(Player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "endGame"
                gameLoopRunning = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameState = "endGame"
                    gameLoopRunning = False
                    continue





        fps = int(clock.get_fps())
        fpsText = font.render(f"FPS: {fps}", True, (255, 255, 255))

        playerCharacter.update(HEIGHT)
        playerCharacter.doCollision(gameTileGroup)

        screen.blit(bgImage, (0, 0))

        gameTileGroup.draw(screen)

        screen.blit(playerCharacter.image, playerCharacter.rect)
        screen.blit(fpsText, (WIDTH / 145, HEIGHT / 90))

        clock.tick(FPS)
        pygame.display.update()




def levelOneData():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState, playerScreen
    bgLevel1Image = pygame.image.load("Images\Backgrounds\l1bgph.png").convert_alpha()
    bgLevel1Image = pygame.transform.scale(bgLevel1Image, (WIDTH, HEIGHT))
    playerCharacter = Player(WIDTH / 14, 8 * HEIGHT / 9, 100 / 3, 50, "Images\Player\placeholderPlayer.png", 20, 2, 5, 50, 1, 30, 500, 0.9)
    levelData = makeLevel("1", str(playerScreen))
    return bgLevel1Image, playerCharacter, levelData

def levelTwoData():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState, playerScreen
    bgLevel2Image = pygame.image.load("Images\Backgrounds\BGPH.png").convert_alpha()
    bgLevel2Image = pygame.transform.scale(bgLevel2Image, (WIDTH, HEIGHT))
    playerCharacter = Player(10, 860, 20, 50, "Images\Player\placeholderPlayer", 20, 2, 5, 50, 1, 30, 500, 0.9)
    levelData = makeLevel("2", str(playerScreen))
    return bgLevel2Image, playerCharacter, levelData

def makeLevel(levelNum, screenNum):
    with open(f"Levels/Level1Screens/Level{levelNum}Screen{screenNum}.txt") as levelToLoad:
        levelData = levelToLoad.read()
    return levelData

def incrementLevel():
    with open("Player-Data\CurrentPlayerLevel.txt") as currLevel:
        currLevel.write(str(int(currLevel.read()) + 1))

def incrementScreen():
    with open("Player-Data\CurrentPlayerScreen.txt") as currScreen:
        currScreen.write(str(int(currScreen.read()) + 1))

def openPauseMenu():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState


def openLoseScreen():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState


def openLevelsMenu():
    print()

def openSettingsMenu():
    print()

while running:
    if gameState == "startScreen":
        openStartScreen()
    elif gameState == "gamePlay":
        with open("Player-Data\CurrentPlayerLevel.txt") as level:
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