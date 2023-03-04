import pygame


class Floor:
    def __init__(self, pos, dimensions):
        self.pos = pos
        self.dimensions = dimensions

    def rect(self):
        return pygame.Rect(self.pos, (self.dimensions[0], self.dimensions[1]))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect())
