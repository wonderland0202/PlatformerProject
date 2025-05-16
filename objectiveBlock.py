import pygame.sprite

class collisionObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()

        self.x = x
        self.y = y

        self.width = width
        self.height = height


        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)