import pygame.sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, jumpHeight, jumpNum, speed, climbLen, gravity, speedBoost):
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
        self.jumpHeight = jumpHeight
        self.jumpNum = jumpNum
        self.origJumpNum = jumpNum
        self.jumpPressed = False
        self.onGround = False



        self.speed = 0
        self.lSpeed = speed * -1
        self.rSpeed = speed
        self.originalSpeed = speed

        self.speedBoost = speedBoost


        self.gravity = gravity
        self.speedY = 0

        self.climbLen = climbLen

        self.lastPos = self.rect.center
        self.origPos = self.rect.center
        self.currLevel = 1
        self.currScreen = 1
        self.transitionVal = None


    def update(self, screenHeight, screenWidth, tileGroup, fanAirGroup):
        keys = pygame.key.get_pressed()

        if self.onGround:
            self.jumpNum = self.origJumpNum

        if not self.onGround and self.jumpNum > 1:
            self.jumpNum = 1

        # Horizontal movement
        self.rect.x += self.speed
        self.doCollision(tileGroup, axis="x")

        # Vertical movement (gravity)
        self.speedY += self.gravity
        self.rect.y += self.speedY
        self.onGround = False  # Assume airborne; will be corrected if grounded
        self.doCollision(tileGroup, axis="y")

        # Input and position update
        self.move(keys)
        self.boundCheck(screenWidth, screenHeight)
        # FanAir push
        fanCollisions = pygame.sprite.spritecollide(self, fanAirGroup, False)
        if fanCollisions:
            self.speedY = -self.jumpHeight / 2  # Adjust push strength as desired

        self.x, self.y = self.rect.topleft

    def move(self, keys):
        if keys[pygame.K_d]:
            self.speed = self.rSpeed
        elif keys[pygame.K_a]:
            self.speed = self.lSpeed
        else:
            self.speed = 0

        if keys[pygame.K_LSHIFT]:
            self.rSpeed = self.speedBoost + self.originalSpeed
            self.lSpeed = self.speedBoost * -1 - self.originalSpeed
        else:
            self.rSpeed = self.originalSpeed
            self.lSpeed = self.originalSpeed * -1

        if keys[pygame.K_SPACE]:
            if self.jumpNum > 0 and not self.jumpPressed:
                self.speedY = -self.jumpHeight
                self.onGround = False
                self.jumpNum -= 1
            self.jumpPressed = True

        else:
            self.jumpPressed = False


        if keys[pygame.K_r]:
            self.rect.center = self.origPos

    def doCollision(self, tileGroup, axis):
        collisions = pygame.sprite.spritecollide(self, tileGroup, False)
        for collider in collisions:

            if axis == "x":
                if self.speed > 0:
                    self.rect.right = collider.rect.left
                elif self.speed < 0:
                    self.rect.left = collider.rect.right

            elif axis == "y":
                if self.speedY > 0:  # Falling
                    self.rect.bottom = collider.rect.top
                    self.speedY = 0
                    self.onGround = True
                    self.jumpNum = self.origJumpNum

                elif self.speedY < 0:  # Jumping
                    self.rect.top = collider.rect.bottom
                    self.speedY = 0

    def boundCheck(self, screenWidth, screenHeight):
        if self.rect.right > screenWidth - 0.1:
            self.rect.left = 2
            self.transitionVal = "SCREENUP"

        if self.rect.left < 0:
            self.rect.right = screenWidth - 2
            self.transitionVal = "SCREENDOWN"

        if self.rect.bottom > screenHeight:
            self.rect.center = self.origPos

        if self.rect.top < 0:
            self.transitionVal = "LEVELUP"


        #self.transitionVal = None
        return self.transitionVal




