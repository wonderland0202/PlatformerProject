import pygame.sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, rImage, lImage, nojImgR, nojImgL, jumpHeight, jumpNum, speed, climbLen, gravity, speedBoost):
        super().__init__()

        self.x, self.y = x, y
        self.width, self.height = width, height

        # Load and scale all images once
        self.nojImgL = pygame.transform.scale(pygame.image.load(nojImgL).convert_alpha(), (width, height))
        self.nojImgR = pygame.transform.scale(pygame.image.load(nojImgR).convert_alpha(), (width, height))
        self.jImgL = pygame.transform.scale(pygame.image.load(lImage).convert_alpha(), (width, height))
        self.jImgR = pygame.transform.scale(pygame.image.load(rImage).convert_alpha(), (width, height))

        self.image = self.jImgR  # Default
        self.rect = self.image.get_rect(center=(x, y))

        # Facing direction split into X and Y
        self.facingX = "RIGHT"
        self.facingY = None

        # Movement
        self.jumpHeight = jumpHeight
        self.jumpNum = self.origJumpNum = jumpNum
        self.jumpPressed = False
        self.onGround = False

        self.speed = 0
        self.originalSpeed = speed
        self.speedBoost = speedBoost
        self.lSpeed = -speed
        self.rSpeed = speed

        self.gravity = gravity
        self.speedY = 0
        self.climbLen = climbLen

        self.lastPos = self.origPos = self.rect.center
        self.currLevel = 1
        self.currScreen = 1
        self.transitionVal = None
        self.scrUpDir = "right"

        self.grappling = False
        self.grapDir = [10, 0]  # X, Y

        self.rightPressed = False  # for grappling input tracking
        self.facingList = [self.facingX, self.facingY]

    def update(self, screenHeight, screenWidth, tileGroup, fanAirGroup, objectiveBlock):
        keys = pygame.key.get_pressed()

        if self.onGround:
            self.jumpNum = self.origJumpNum

        # Move and collide X
        if not self.grappling:
            self.rect.x += self.speed
        self.doCollision(tileGroup, axis="x")

        if self.grappling:
            self.speedY = 0

        # Apply gravity and collide Y
        if not self.grappling:
            self.speedY += self.gravity
            self.rect.y += self.speedY
        self.onGround = False
        self.doCollision(tileGroup, axis="y")

        # Handle input
        if not self.grappling:
            self.move(keys)
        self.boundCheck(screenWidth, screenHeight, objectiveBlock)

        # Fan effect
        if pygame.sprite.spritecollide(self, fanAirGroup, False):
            self.speedY = -self.jumpHeight / 2
            if self.jumpNum > 1:
                self.jumpNum = 1

        # Update facing direction
        if self.speed > 0:
            self.facingX = "RIGHT"
        elif self.speed < 0:
            self.facingX = "LEFT"

        if keys[pygame.K_w]:
            self.facingY = "UP"
        elif keys[pygame.K_s]:
            self.facingY = "DOWN"
        else:
            self.facingY = None

        self.facingList = [self.facingX, self.facingY]

        # Update image based on state
        if self.jumpNum <= 0:
            self.image = self.nojImgR if self.facingX == "RIGHT" else self.nojImgL
        else:
            self.image = self.jImgR if self.facingX == "RIGHT" else self.jImgL

        self.x, self.y = self.rect.topleft


    def reset(self):
        self.rect.center = self.origPos
        self.facingX = "LEFT" if self.currLevel % 2 == 0 else "RIGHT"
        self.grappling = False

    def move(self, keys):
        self.speed = 0
        if keys[pygame.K_d]:
            self.speed = self.rSpeed
        elif keys[pygame.K_a]:
            self.speed = self.lSpeed

        if keys[pygame.K_LSHIFT]:
            self.rSpeed = self.originalSpeed + self.speedBoost
            self.lSpeed = -(self.originalSpeed + self.speedBoost)
        else:
            self.rSpeed = self.originalSpeed
            self.lSpeed = -self.originalSpeed

        if keys[pygame.K_SPACE]:
            if self.jumpNum > 0 and not self.jumpPressed:
                self.speedY = -self.jumpHeight
                self.onGround = False
                self.jumpNum -= 1
            self.jumpPressed = True
        else:
            self.jumpPressed = False

        if keys[pygame.K_RIGHT]:
            if not self.rightPressed:
                self.rightPressed = True

        else:
            self.rightPressed = False


    def doCollision(self, tileGroup, axis):
        for collider in pygame.sprite.spritecollide(self, tileGroup, False):
            if axis == "x":
                if self.speed > 0:
                    self.rect.right = collider.rect.left
                elif self.speed < 0:
                    self.rect.left = collider.rect.right
            elif axis == "y":
                if self.speedY > 0:
                    self.rect.bottom = collider.rect.top
                    self.speedY = 0
                    self.onGround = True
                    self.jumpNum = self.origJumpNum
                elif self.speedY < 0:
                    self.rect.top = collider.rect.bottom
                    self.speedY = 0

    def boundCheck(self, screenWidth, screenHeight, objectiveBlock):
        if self.rect.right > screenWidth - 0.1 and objectiveBlock.offScreen:
            self.rect.left = 2
            self.transitionVal = "SCREENUP" if self.scrUpDir == "right" else "SCREENDOWN"
            objectiveBlock.rect.left = self.rect.right + 1 if self.scrUpDir == "right" else self.rect.right - 1

        if self.rect.left < 0 and objectiveBlock.offScreen:
            self.rect.right = screenWidth - 2
            self.transitionVal = "SCREENDOWN" if self.scrUpDir == "right" else "SCREENUP"
            objectiveBlock.rect.left = self.rect.right - 1
            objectiveBlock.rect.right = self.rect.left + 1

        if self.rect.bottom > screenHeight:
            self.rect.center = self.origPos
            objectiveBlock.rect.center = objectiveBlock.origPos

        if self.rect.top < 0 and objectiveBlock.offScreen:
            self.transitionVal = "LEVELUP"

        return self.transitionVal

    def setGrappleDir(self):
        if not self.grappling:
            self.facingY = self.facingList[1]
            self.facingX = self.facingList[0]
            if self.speed == 0 and self.facingY != None:
                self.grapDir = [
                    0,
                    -10 if self.facingY == "UP" else 10 if self.facingY == "DOWN" else 0
                ]
            else:
                self.grapDir = [
                    10 if self.facingX == "RIGHT" else -10 if self.facingX == "LEFT" else 0,
                    -10 if self.facingY == "UP" else 10 if self.facingY == "DOWN" else 0
                ]

    def pullToGrapEnd(self, endLink):
        self.rect.center = endLink.rect.center