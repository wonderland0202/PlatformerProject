import pygame.sprite

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

        self.speed = speed

        self.gravity = gravity

        #dash
        self.dashDist = dashDist
        self.dashNum = dashNum
        self.dashCooldown = dashCooldown


        self.climbLen = climbLen

        self.speedY = 0

        self.onGround = False


    def update(self, screenHeight):
        keys = pygame.key.get_pressed()
        self.speedY += self.gravity
        if self.onGround == False:
            self.rect.y += self.speedY
        if self.rect.y - self.height > screenHeight:
            self.rect.y = screenHeight - self.height
            self.onGround = True
        self.move(keys)

    def move(self, keys):
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            if self.onGround:
                self.speedY = -1 * self.jumpHeight
                self.onGround = False