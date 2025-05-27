import pygame.sprite

class kickUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, itterMax):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.itterMax = itterMax

    def update(self, oBG, objectiveBlock):
        collisions = pygame.sprite.spritecollide(self, oBG, False)
        if len(collisions) > 0:
            objectiveBlock.speedY = -objectiveBlock.pushHeight