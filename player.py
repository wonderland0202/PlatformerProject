from tty import ISPEED

import pygame.sprite
from pygame.sprite import groupcollide


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, jumpHeight, jumpNum, speed, dashDist, dashNum, dashCooldown, climbLen, gravity):
        super().__init__()

        # Position

        self.x = x
        self.y = y

        # Look

        self.width = width
        self.height = height
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))

        # Movement

        #jump
        self.jumpHeight = jumpHeight
        self.jumpNum = jumpNum

        self.speed = 0
        self.lSpeed = speed * -1
        self.rSpeed = speed

        self.gravity = gravity

        #dash
        self.dashDist = dashDist
        self.dashNum = dashNum
        self.dashCooldown = dashCooldown


        self.climbLen = climbLen

        self.speedY = 0

        self.onGround = False

        self.lastPos = self.rect.center

        self.origPos = self.rect.center

        self.tileOffset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


    def update(self, screenHeight, screenWidth, tileGroup, playerCharacter):
        keys = pygame.key.get_pressed()
        self.speedY += self.gravity
        #if not self.onGround:
        #    self.rect.y += self.speedY
        self.rect.y += self.speedY
        if self.rect.y - self.height > screenHeight:
            self.rect.y = screenHeight - self.height
            self.onGround = True

        self.x = self.rect.x
        self.y = self.rect.y

        self.rect.x += self.speed
        self.move(keys, tileGroup, playerCharacter)
        self.boundCheck(screenWidth, screenHeight)

    def move(self, keys):
        if keys[pygame.K_d]:
            self.speed = self.rSpeed
        else:
            self.rSpeed = 0
        if keys[pygame.K_a]:
            self.speed = self.lSpeed
        if keys[pygame.K_SPACE]:
            if self.onGround:
                self.speedY = -1 * self.jumpHeight
                self.onGround = False
        if keys[pygame.K_r]:
            self.rect.center = self.origPos
            print("reset")

    def doCollision(self, tileGroup, playerCharacter):
        collided = pygame.sprite.spritecollide(playerCharacter, tileGroup, False)
        if collided:
            collider = pygame.sprite.spritecollideany(playerCharacter, tileGroup)
            colliderLetter = collider.letterValue
            if colliderLetter == "F":
                self.rect.bottom = collider.rect.top
                self.onGround = True
            '''
            elif colliderLetter == "W":
                self.rect.right = collider.rect.left
            elif colliderLetter == "Q":
                self.rect.left = collider.rect.right
            elif colliderLetter == "C":
                self.rect.top = collider.rect.bottom
            elif colliderLetter == "A":
                self.rect.bottom = collider.rect.top - collider.height
            '''

    def holdPos(self):
        self.lastPos = self.rect.center

    def boundCheck(self, screenWidth, screenHeight):
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight