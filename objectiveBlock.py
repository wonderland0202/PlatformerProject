import pygame.sprite

class objectiveBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, gravity, pushHeight, pushSpeed):
        super().__init__()

        self.x = x
        self.y = y

        self.offScreen = False

        self.width = width
        self.height = height


        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect(center=(x, y))

        self.gravity = gravity
        self.pushHeight = pushHeight

        self.speed = 0
        self.speedY = 0

        self.pushSpeed = pushSpeed

        self.origPos = self.rect.center

    def update(self, screenHeight, screenWidth, playerCharacter, tileGroup, fanAirGroup, playerGroup):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.rect.center = self.origPos

        if not self.offScreen:

            # Horizontal movement
            self.rect.x += self.speed
            self.doGameTileCollision(tileGroup, axis="x")

            # Vertical movement (gravity)
            self.speedY += self.gravity
            self.rect.y += self.speedY
            self.doGameTileCollision(tileGroup, axis="y")

            self.doPlayerCollision(playerCharacter, playerGroup)

        # Input and position update
        # FanAir push
            fanCollisions = pygame.sprite.spritecollide(self, fanAirGroup, False)
            if fanCollisions:
                self.speedY = -playerCharacter.jumpHeight / 2  # Adjust push strength as desired

        self.boundCheck(screenWidth, screenHeight)

        self.x, self.y = self.rect.topleft

    def doGameTileCollision(self, tileGroup, axis):
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

                elif self.speedY < 0:  # Jumping
                    self.rect.top = collider.rect.bottom
                    self.speedY = 0

    def doPlayerCollision(self, player, playerGroup):
        collidedPlayers = pygame.sprite.spritecollide(self, playerGroup, False)
        if len(collidedPlayers) > 0:
            if player.rect.centerx > self.rect.centerx:
                self.speed -= self.pushSpeed
            elif player.rect.centerx < self.rect.centerx:
                self.speed += self.pushSpeed
        else:
            self.speed = 0


    def boundCheck(self, screenWidth, screenHeight):
        if self.rect.right > screenWidth - 0.1:
            self.rect.left = screenWidth + 1
            self.offScreen = True

        if self.rect.left < 0:
            self.rect.right = screenWidth - 2
            self.transitionVal = "SCREENDOWN"

        if self.rect.bottom > screenHeight:
            self.rect.center = self.origPos

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.left > 0 and self.rect.right < screenWidth - 0.1:
            self.offScreen = False

        print(self.offScreen)