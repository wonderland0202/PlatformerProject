import pygame
import math

from player import Player
from menuButton import MenuButton
from collisionObject import collisionObject
from objectiveBlock import objectiveBlock
from kickUp import kickUp
from grappler import Grappler, GrapplerProjectile

pygame.init()

# Global constants
scrSize = pygame.display.Info()
WIDTH, HEIGHT = scrSize.current_w, scrSize.current_h
# screen size for debugging
WIDTH, HEIGHT = WIDTH / 2, HEIGHT / 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Lights")
clock = pygame.time.Clock()
FPS = 144
gameState = "startScreen"
font = pygame.font.SysFont("Consolas", 24)
running = True
needBuild = True
prevT = None
kickerExists = False
grapplerExists = False
rPressed = False
grapProjEx = False
grapEx = False
gravity = 0.15

# Player's current level and screen
with open("Player-Data\\CurrentPlayerLevel.txt") as level:
    playerLevel = int(level.read())

with open("Player-Data\\CurrentPlayerScreen.txt") as currScreen:
    playerScreen = int(currScreen.read())


def openStartScreen():
    global gameState, needBuild
    startScreenRunning = True
    mainMenuIndex = 1

    titleImage = pygame.image.load("Images/TitleScreen/TitleImage.png").convert_alpha()
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

        if titlePos >= 0.5:
            titlePosMult = -1
        elif titlePos <= -0.5:
            titlePosMult = 1

        titlePos += 0.02 * titlePosMult

        screen.blit(bgMenuImage, (0, 0))
        screen.blit(titleImage, ((WIDTH / 2 - (titleImage.get_width() / 2)), 10 * math.sin(titlePos) + (HEIGHT / 15)))
        mainMenuButtonGroup.draw(screen)
        clock.tick(FPS)
        pygame.display.update()


def openGamePlay(level):
    global gameState, playerScreen, needBuild, prevT, kickerExists, grapplerExists, rPressed, grapProjEx, grapEx, gravity

    playerCharacter = Player(2 * WIDTH / 14, 7 * HEIGHT / 9, WIDTH / 28, HEIGHT / 14,
                             "Images\\Player\\placeholderPlayer-right.png", "Images\\Player\\placeholderPlayer-left.png","Images\\Player\\playerwoj-right.png", "Images\\Player\\playerwoj-left.png", HEIGHT / 100, 2, WIDTH / 200, 500, gravity, WIDTH / 400)

    playerGroup = pygame.sprite.Group(playerCharacter)

    gameObjectiveBlock = objectiveBlock(2 * WIDTH / 14 + playerCharacter.width, 7 * HEIGHT / 9, WIDTH / 28, WIDTH / 28, "Images\\ObjectiveBlock\\ObjectiveBlockPH.jpg", gravity, playerCharacter.height / 10, playerCharacter.width / 30)

    objectiveBlockGroup = pygame.sprite.Group(gameObjectiveBlock)

    gameLoopRunning = True
    grapplerGroup = pygame.sprite.Group()
    while gameLoopRunning:
        if needBuild:
            collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter, gameObjectiveBlock)
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
                if event.key != pygame.K_SPACE:
                    playerCharacter.jumpPressed = False
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

        playerCharacter.update(HEIGHT, WIDTH, collisionObjects, fanAirGroup, gameObjectiveBlock)
        gameObjectiveBlock.update(HEIGHT, WIDTH, playerCharacter, collisionObjects, fanAirGroup, playerGroup)


        #---------------#
        #  KICKER CODE  #
        #---------------#

        if pygame.key.get_pressed()[pygame.K_UP] and not kickerExists:
            facingDir = playerCharacter.facingX
            if facingDir == "RIGHT":
                kicker = kickUp(playerCharacter.rect.x + playerCharacter.width, playerCharacter.rect.y + playerCharacter.height, 4 * playerCharacter.width / 5, playerCharacter.height / 2, 10)
                kickerExists = True
            else:
                kicker = kickUp(playerCharacter.rect.x - playerCharacter.width, playerCharacter.rect.y + playerCharacter.height, 4 * playerCharacter.width / 5, playerCharacter.height / 2, 10)
                kickerExists = True
            itterNum = 0
            itterMax = kicker.itterMax

        # ----------------#
        #  GRAPPLER CODE  #
        # ----------------#


        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if not rPressed:
                rPressed = True
                if not playerCharacter.grappling:
                    playerCharacter.setGrappleDir()
                    grapProj = GrapplerProjectile(playerCharacter, collisionObjects, objectiveBlockGroup, playerCharacter.grapDir)
                    grapProjEx = True
                    playerCharacter.grappling = True
                else:
                    grapEx = False
                    playerCharacter.grappling = False
                    grapplerGroup.empty()
        else:
            rPressed = False

        if grapProjEx:
            grapProj.update()

            if grapProj.collidedObj != "":
                if grapProj.travelDist <= 10:
                    for i in range(grapProj.travelDist + 1):
                        playerGrappler = Grappler(grapProj, grapProj.moveList, i, playerCharacter.grapDir)
                        grapplerGroup.add(playerGrappler)
                    grapEx = True
                grapProj.kill()
                grapProjEx = False


        transition = playerCharacter.boundCheck(WIDTH, HEIGHT, gameObjectiveBlock)

        if prevT != transition:
            # Handle screen transition
            if transition == "SCREENUP":
                playerScreen += 1
                playerCharacter.currScreen = playerScreen
                collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter, gameObjectiveBlock)
                needBuild = True
                playerCharacter.origPos = playerCharacter.rect.center
                gameObjectiveBlock.origPos = gameObjectiveBlock.rect.center
                playerCharacter.transitionVal = None

            elif transition == "SCREENDOWN":
                if playerScreen > 1:
                    playerScreen -= 1
                    playerCharacter.currScreen = playerScreen
                    collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter, gameObjectiveBlock)
                    playerCharacter.origPos = playerCharacter.rect.center
                    gameObjectiveBlock.origPos = gameObjectiveBlock.rect.center
                else:
                    # Prevent screen change on screen 1
                    playerCharacter.rect.left = 0
                playerCharacter.transitionVal = None

            elif transition == "LEVELUP":
                level += 1
                playerScreen = 1
                playerCharacter.currScreen = playerScreen
                collisionObjects, fanAirGroup, bgImage, gameTileGroup = buildLevel(level, playerScreen, playerCharacter, gameObjectiveBlock)
                playerCharacter.origPos = playerCharacter.rect.center
                gameObjectiveBlock.origPos = gameObjectiveBlock.rect.center

        prevT = transition

        screen.blit(bgImage, (0, 0))
        gameTileGroup.draw(screen)
        screen.blit(playerCharacter.image, playerCharacter.rect)
        screen.blit(gameObjectiveBlock.image, gameObjectiveBlock.rect)
        screen.blit(fpsText, (WIDTH / 145, HEIGHT / 90))
        if kickerExists:
            screen.blit(kicker.image, kicker.rect)

        if kickerExists:
            itterNum += 1
            kicker.update(objectiveBlockGroup, gameObjectiveBlock)
            if itterNum > itterMax:
                kickerExists = False
                kicker.kill()

        if playerCharacter.grappling:
            screen.blit(playerCharacter.image, (playerCharacter.rect.x + playerCharacter.grapDir[0], playerCharacter.rect.y + playerCharacter.grapDir[1]))
        if grapProjEx:
            screen.blit(grapProj.image, grapProj.rect)
        elif grapEx:
            try:
                grapplerGroup.draw(screen)
            except AttributeError:
                None
        clock.tick(FPS)
        pygame.display.update()



def buildLevel(level, screen, playerCharacter, objectiveBlock):
    if level == 1:
        bgImage, levelData = levelOneData(screen, playerCharacter)
    elif level == 2:
        bgImage, playerCharacter, levelData = levelTwoData(screen, playerCharacter, objectiveBlock)

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
            " ": f"Levels/EmptyTile.png",
            "W": f"Levels/Level{level}/LevelMakeup/LeftWallLine.png",
            "F": f"Levels/Level{level}/LevelMakeup/FloorLine.png",
            "Q": f"Levels/Level{level}/LevelMakeup/RightWallLine.png",
            "A": f"Levels/Level{level}/LevelMakeup/InnerBuilding.png",
            "C": f"Levels/Level{level}/LevelMakeup/CeilingLine.png",
            "V": f"Levels/Level{level}/LevelMakeup/WallToFloor-Up.png",
            "M": f"Levels/Level{level}/LevelMakeup/FloorToWall-Down.png",
            "N": f"Levels/Level{level}/LevelMakeup/FloorToWall-Up.png",
            "P": f"Levels/Level{level}/LevelMakeup/CeilingToWall-Up.png",
            "I": f"Levels/Level{level}/LevelMakeup/WallToCeiling-Up.png",
            "B": f"Levels/Level{level}/LevelMakeup/FacingUpFan.png",
            "T": f"Levels/Level{level}/LevelMakeup/WallToFloor-Down.png"
        }.get(char, "Levels/EmptyTile.png")

        if char == " " or char == "O":
            collisionVal = False



        if char == "B":
            for offset in range(1, 4):  # 3 tiles above
                airY = y - offset * (HEIGHT / 9)
                fanAir = collisionObject(x, airY, WIDTH / 14, HEIGHT / 9, f"Levels/Level{level}/LevelMakeup/FanAir.png", False, "fanAir")
                fanAirGroup.add(fanAir)
                gameTileGroup.add(fanAir)
        newGameTile = collisionObject(x, y, WIDTH / 14 + WIDTH / 70, HEIGHT / 9 + HEIGHT / 45, objectIdentity, collisionVal, char)
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


def levelTwoData(screen, playerCharacter, objectiveBlock):
    playerCharacter.currLevel = 2
    playerCharacter.currScreen = screen
    playerCharacter.rect.bottom = 7 * HEIGHT / 9
    playerCharacter.scrUpDir = "left"
    objectiveBlock.rect.bottom = playerCharacter.rect.bottom
    objectiveBlock.rect.x = playerCharacter.rect.x - 1
    bgLevel2Image = pygame.image.load("Images\\Backgrounds\\l2bgph.png").convert_alpha()
    bgLevel2Image = pygame.transform.scale(bgLevel2Image, (WIDTH, HEIGHT))
    levelData = makeLevel("2", str(screen))
    return bgLevel2Image, playerCharacter, levelData



def makeLevel(levelNum, screenNum):
    with open(f"Levels/Level{levelNum}/Level{levelNum}Screens/Level{levelNum}Screen{screenNum}.txt") as levelToLoad:
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
    global gameState, needBuild, grapProjEx
    grapProjEx = False
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
