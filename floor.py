import pygame


class Floor:
    def __init__(self, pos, dimensions):
        self.pos = pos
        self.dimensions = dimensions
        self.img = pygame.image.load("assets/floor_img.png")
        self.img = pygame.transform.scale(self.img, (self.dimensions))

    def rect(self):
        return pygame.Rect(self.pos, (self.dimensions[0], self.dimensions[1]))

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.rect())
        screen.blit(self.img, (self.rect().x, self.rect().y))
