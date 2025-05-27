import pygame.sprite

class kickUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, objectiveBlock, itterMax):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(bottomleft=(x,y))

        self.objectiveBlock = objectiveBlock
        self.itterMax = itterMax

    def update(self):
        oBG = pygame.sprite.Group(self.objectiveBlock)
        collisions = pygame.sprite.spritecollide(self, oBG, False)
        if len(collisions) > 0:
            self.objectiveBlock.rect.y += self.objectiveBlock.pushHeight