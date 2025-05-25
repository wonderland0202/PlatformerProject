import pygame.sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, jumpHeight, speed, dashDist, climbLen, gravity, speedBoost):
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
        self.speed = 0
        self.lSpeed = speed * -1
        self.rSpeed = speed
        self.originalSpeed = speed
        self.speedBoost = speedBoost
        self.gravity = gravity
        self.dashDist = dashDist
        self.dashNum = 1
        self.climbLen = climbLen
        self.speedY = 0
        self.onGround = False
        self.lastPos = self.rect.center
        self.origPos = self.rect.center
        self.tileOffset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.currLevel = 1
        self.currScreen = 1
        self.transitionVal = None
        self.dashSpeedX = 0
        self.dashSpeedY = 0
        self.dashDuration = 50  # Number of frames the dash lasts
        self.dashTimer = 0
        self.dashPressed = False

    def update(self, screenHeight, screenWidth, tileGroup, playerCharacter, fanAirGroup):
        keys = pygame.key.get_pressed()

        # Apply dash movement if dash is active


        # Horizontal movement
        self.rect.x += self.speed
        self.doCollision(tileGroup, playerCharacter, axis="x")

        # Vertical movement (gravity)
        if self.dashTimer <= 0:
            self.speedY += self.gravity
        self.rect.y += self.speedY
        self.onGround = False  # Assume airborne; will be corrected if grounded
        self.doCollision(tileGroup, playerCharacter, axis="y")

        # Input and position update
        if self.dashTimer <= 0:
            self.move(keys)
        self.boundCheck(screenWidth, screenHeight)
        # FanAir push
        fanCollisions = pygame.sprite.spritecollide(playerCharacter, fanAirGroup, False)
        if fanCollisions:
            self.speedY = -self.jumpHeight / 2  # Adjust push strength as desired

        if self.dashTimer > 0:
            self.rect.x += int(self.dashSpeedX)
            self.rect.y += int(self.dashSpeedY)
            self.dashTimer -= 1
        else:
            self.dashSpeedX = 0
            self.dashSpeedY = 0

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
            if self.onGround:
                self.speedY = -self.jumpHeight
                self.onGround = False

        if keys[pygame.K_UP]:
            if not self.dashPressed and self.dashNum > 0:
                self.dash(keys)
                self.dashPressed = True
        else:
            self.dashPressed = False

        if keys[pygame.K_r]:
            print(f"resetting\nPrevious Position: {self.rect.centerx, self.rect.centery}")
            self.rect.center = self.origPos
            print("reset")

    def doCollision(self, tileGroup, playerCharacter, axis):
        collisions = pygame.sprite.spritecollide(playerCharacter, tileGroup, False)
        for collider in collisions:
            colliderLetter = getattr(collider, "letterValue", None)

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
                    self.dashNum = 1
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


        print(self.transitionVal)
        #self.transitionVal = None
        return self.transitionVal

    def dash(self, keys):
        if self.dashNum <= 0:
            return

        dx = 0
        dy = 0

        if keys[pygame.K_w]:  # Up
            dy = -1
        if keys[pygame.K_s]:  # Down
            dy = 1
        if keys[pygame.K_a]:  # Left
            dx = -1
        if keys[pygame.K_d]:  # Right
            dx = 1

        if dx == 0 and dy == 0:
            return  # No direction pressed



        # Set dash velocity
        self.dashSpeedX = dx * self.dashDist / self.dashDuration
        self.dashSpeedY = dy * self.dashDist / self.dashDuration
        self.dashTimer = self.dashDuration

        self.dashNum -= 1
        print(f"Dash started: dx={dx}, dy={dy}, speedX={self.dashSpeedX}, speedY={self.dashSpeedY}")




