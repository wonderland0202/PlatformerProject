import pygame.sprite

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font):
        super().__init__()

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.textPos = (self.width / 2, self.height / 2)
        self.textColour = (255, 255, 255)

        self.bgNoHighlightColour = (255,255,255, 0.2)
        self.bgHighlightColour = (255,255,255,1)

        self.currColour = self.bgNoHighlightColour

        self.text = text
        self.font = font

        self.image = pygame.Surface((width, height))
        self.image.fill(self.currColour)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def highlight(self):
        self.currColour = self.bgHighlightColour
        self.image.fill(self.currColour)

    def unhighlight(self):
        self.currColour = self.bgNoHighlightColour
        self.image.fill(self.currColour)