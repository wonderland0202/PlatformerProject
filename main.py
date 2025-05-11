import pygame

from player import Player
from menuButton import MenuButton

pygame.init()

#Always Global

WIDTH, HEIGHT = 1450, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
FPS = 144
gameState = "startScreen"


running = True

#Player's current level
with open("Player-Data\CurrentPlayerLevel.txt") as level:
  playerLevel = int(level.read())

def openStartScreen():
    global WIDTH, HEIGHT, screen, clock, FPS, gameState, pygame
    continueButtonFont = pygame.font.SysFont(None, 24)
    levelsButtonFont = pygame.font.SysFont(None, 12)
    quitButtonFont = pygame.font.SysFont(None,10)
    startScreenRunning = True
    menuIndex = 0

    menuContinueButton = MenuButton(WIDTH / 2, HEIGHT / 3, WIDTH / 5, HEIGHT / 5, "CONTINUE", continueButtonFont) #h: 1/3
    menuLevelsButton = MenuButton(WIDTH / 2, 7 * HEIGHT / 12, WIDTH / 7, HEIGHT / 7, "LEVELS", levelsButtonFont) #h: 7/12
    menuQuitButton = MenuButton(WIDTH / 2, 9 * HEIGHT / 12, WIDTH / 8, HEIGHT / 8, "QUIT", quitButtonFont) #h: 9 / 12

    buttonGroup = pygame.sprite.Group()

    buttonGroup.add(menuContinueButton)
    buttonGroup.add(menuLevelsButton)
    buttonGroup.add(menuQuitButton)

    bgMenuImage = pygame.image.load("Images/Backgrounds/BGPH.png").convert_alpha()
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
                        menuContinueButton.unhighlight()
                        menuLevelsButton.highlight()

                    elif menuIndex == 1:
                        menuIndex += 1
                        menuLevelsButton.unhighlight()
                        menuQuitButton.highlight()

                if event.key == pygame.K_UP:
                    if menuIndex == 2:
                        menuIndex -= 1
                        menuQuitButton.unhighlight()
                        menuLevelsButton.highlight()

                    elif menuIndex == 1:
                        menuIndex -= 1
                        menuLevelsButton.unhighlight()
                        menuContinueButton.highlight()
                #---

                # Menu Selection Interactions
                if event.key == pygame.K_SPACE:
                    if menuIndex == 0:
                        gameState = "gamePlay"
                        startScreenRunning = False
                        continue
                    elif menuIndex == 1:
                        gameState = "levelsMenu"
                        startScreenRunning = False
                        continue
                    elif menuIndex == 2:
                        gameState = "endGame"
                        startScreenRunning = False
                        continue
                #---

        screen.blit(bgMenuImage, (0, 0))

        buttonGroup.draw(screen)


        clock.tick(FPS)
        pygame.display.update()


def openGamePlay(level):
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState

def incrementLevel():
    with open("Player-Data\CurrentPlayerLevel.txt") as currLevel:
        currLevel.write(str(int(currLevel.read())+1))

def openPauseMenu():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState


def openLoseScreen():
    global WIDTH, HEIGHT, screen, clock, FPS, running, gameState


def openLevelsMenu():
    print()

while running:
    if gameState == "startScreen":
        openStartScreen()
    elif gameState == "gamePlay":
        openGamePlay(playerLevel)
    elif gameState == "paused":
        openPauseMenu()
    elif gameState == "loseScreen":
        openLoseScreen()
    elif gameState == "levelsMenu":
        openLevelsMenu()
    elif gameState == "endGame":
        running = False

pygame.quit()