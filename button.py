import pygame

class Button:
    def __init__(self, colors, x, y, w, h):
        """`colors` - 0: normal, 1: hover, 2: selected"""
        self.colors = colors
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.selected_color = colors[0]
        self.is_clicked = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.selected_color, [self.x, self.y, self.w, self.h], 0, 20)
    
    def update(self, cx, cy, is_mouse_down, is_mouse_up):
        if self.is_clicked:
            return

        if cx > self.x \
            and cx < self.x + self.w \
            and cy > self.y \
            and cy < self.y + self.h:
            self.selected_color = self.colors[1]
            if is_mouse_down or is_mouse_up:
                self.selected_color = self.colors[2]
            if is_mouse_up:
                self.is_clicked = True
        else:
            self.selected_color = self.colors[0]