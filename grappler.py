import pygame.sprite

class Grappler(pygame.sprite.Sprite):
    def __init__(self, GrapplerProjectile, direc, itteration, playerFacingDirection):
        super().__init__()
        self.grapProj = GrapplerProjectile

        self.width = 35
        self.height = 70
        self.x = self.grapProj.player.rect.centerx
        self.y = self.grapProj.player.rect.centery
        self.direc = direc
        self.itteration = itteration
        self.pFD = playerFacingDirection

        if self.pFD == [0,-10]:
            self.angle = 0
        elif self.pFD == [10,-10]:
            self.angle = -45
        elif self.pFD == [10,0]:
            self.angle = -90
        elif self.pFD == [10,10]:
            self.angle = -135
        elif self.pFD == [0,10]:
            self.angle = 180
        elif self.pFD == [-10,10]:
            self.angle = 135
        elif self.pFD == [-10,0]:
            self.angle = 90
        elif self.pFD == [-10,-10]:
            self.angle = 45
        else:
            print("BRUH WHAT")
            self.angle = 0



        if self.itteration <= 1:
            self.imageVal = "Images\\Player\\Grappler\\empty.png"
        elif self.itteration < self.grapProj.travelDist:
            self.imageVal = "Images\\Player\\Grappler\\linkk.png"
        else:
            self.imageVal = "Images\\Player\\Grappler\\endd.png"
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.imageVal).convert_alpha(), (self.width, self.height)), self.angle)
        self.rect = self.image.get_rect(center=(self.x + self.itteration * (self.direc[0] * 2.5), self.y + self.itteration * (self.direc[1] * 2.5)))

    def update(self, playerCoord):
        self.rect.center = playerCoord[0] + self.itteration * (self.direc[0] * 2.5), playerCoord[1] + self.itteration * (self.direc[1] * 2.5)




class GrapplerProjectile(pygame.sprite.Sprite):
    def __init__(self, player, tileGroup, objectiveBlockGroup, moveList, screenSizeList, maxDist):
        super().__init__()
        self.player = player
        self.screenList = screenSizeList
        self.image = pygame.Surface((10, 10))
        self.image.fill((255,255,255))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=(player.rect.centerx, player.rect.centery))
        self.maxDist = maxDist

        self.tileGroup = tileGroup

        self.collidedObj = ""
        self.objectiveBlockGroup = objectiveBlockGroup

        self.travelDist = 0

        self.moveList = moveList

    def update(self):
        if self.collidedObj == "":
            self.rect.x += 2.5 * self.moveList[0]
            self.rect.y += 2.5 * self.moveList[1]
        self.doCollision()

    def doCollision(self):
        collisions = pygame.sprite.spritecollide(self, self.tileGroup, False)
        if len(collisions) == 0:
            collisions = pygame.sprite.spritecollide(self, self.objectiveBlockGroup, False)
            if len(collisions) == 0:
                self.travelDist += 1
                self.collidedObj = ""
            else:
                self.collidedObj = collisions
        else:
            self.collidedObj = collisions

        if self.rect.x > self.screenList[0] or self.rect.x < 0 or self.rect.y > self.screenList[1] or self.rect.y < 0:
            self.travelDist = self.maxDist + 1
            self.collidedObj = " "
