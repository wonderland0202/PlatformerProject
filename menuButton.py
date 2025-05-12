import pygame.sprite

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, unselectedImage, selectedImage):
        super().__init__()

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.textPos = (self.width / 2, self.height / 2)
        self.textColour = (255, 255, 255)

        self.unselectedImage = pygame.image.load(unselectedImage).convert_alpha()
        self.unselectedImage = pygame.transform.scale(self.unselectedImage, (self.width, self.height))

        self.selectedImage = pygame.image.load(selectedImage).convert_alpha()
        self.selectedImage = pygame.transform.scale(self.selectedImage, (self.width, self.height))

        self.image = self.unselectedImage

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def highlight(self):
        self.image = self.selectedImage

    def unhighlight(self):
        self.image = self.unselectedImage
