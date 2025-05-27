import pygame.sprite

class Grappler(pygame.sprite.Sprite):
    def __init__(self, player, tileGroup, objectiveBlockGroup):
        super().__init__()
        self.grapplerLen = 1
        collided = True
        while not collided:
            self.image = pygame.Surface((10, 20 * self.grapplerLen))
            self.image.set_alpha(0)
            self.rect = self.image.get_rect(center=player.rect.center)

            tileCollisions = pygame.sprite.spritecollide(self, tileGroup, False)
            objectiveBlockCollisions = pygame.sprite.spritecollide(self, objectiveBlockGroup, False)

            if len(tileCollisions) <= 0 and len(objectiveBlockCollisions) <= 0:
                self.grapplerLen += 1
            else:
                collided = True

class GrapplerSegment(pygame.sprite.Sprite):
    def __init__(self, img, x, y, facingDir, linkNum):
        super().__init__()
        if facingDir == "RIGHT":
            width = 10
        elif facingDir == "LEFT":
            width = -10
        if img == "LINK":
            self.image = pygame.image.load("Images\\Player\\Grappler\\link.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (10, 20))
            self.rect = self.image.get_rect(center=(x + (width * linkNum), y))
        elif img == "END":
            self.image = pygame.image.load("Images\\Player\\Grappler\\end.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 10))
            self.rect = self.image.get_rect(center=(x + (width * linkNum), y))