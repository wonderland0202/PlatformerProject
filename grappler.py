import pygame.sprite

class Grappler(pygame.sprite.Sprite):
    def __init__(self, GrapplerProjectile, maxLen):
        super().__init__()
        self.grapProj = GrapplerProjectile
        self.linkImg = "Images\\Player\\Grappler\\link.jpg"
        self.endImg = "Images\\Player\\Grappler\\end.jpg"
        self.width = self.grapProj.player.width / 2
        self.height = self.grapProj.player.height / 2
        self.x = self.grapProj.player.rect.centerx
        self.y = self.grapProj.player.rect.centery

        if self.grapProj.travelDist <= maxLen:
            for i in range(len(self.grapProj.travelDist)):
                if i < self.grapProj.travelDist:
                    self.imageVal = self.linkImg
                else:
                    self.imageVal = self.endImg
                self.image = pygame.transform.scale(pygame.image.load(self.imageVal).convert_alpha(), (self.width, self.height))
                self.rect = self.image.get_rect(center=(self.x * i, self.y * i))




class GrapplerProjectile(pygame.sprite.Sprite):
    def __init__(self, player, tileGroup, objectiveBlockGroup, moveList):
        super().__init__()
        self.player = player

        self.image = pygame.Surface((10, 10))
        self.image.fill((255,255,255))
        #self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=(player.rect.centerx, player.rect.centery))

        self.tileGroup = tileGroup

        self.collidedObj = ""
        self.objectiveBlockGroup = objectiveBlockGroup

        self.travelDist = 0

        self.moveList = moveList

    def update(self):
        if self.collidedObj == "":
            self.rect.x += 5 * self.moveList[0]
            self.rect.y += 5 * self.moveList[1]
        self.doCollision()

    def doCollision(self):
        collisions = pygame.sprite.spritecollide(self, self.tileGroup, False)
        if len(collisions) == 0:
            self.travelDist += 1
            self.collidedObj = ""
        else:
            self.collidedObj = collisions
