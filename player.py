import pygame.sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, jumpHeight, speed, jumpNum, dashDist, dashNum, climbLen):
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

        #dash
        self.dashDist = dashDist
        self.dashNum = dashNum

        self.climbLen = climbLen