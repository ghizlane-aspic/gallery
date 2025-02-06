import pygame


class Shape:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        pass


class Circle(Shape):
    def __init__(self, color, x, y, radius):
        super().__init__(color, x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Rectangle(Shape):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y)
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
