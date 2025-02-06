from shapes import Circle, Rectangle
import pygame
import random


def create_random_shapes(num_shapes, width, height):
    shapes = []
    for _ in range(num_shapes):
        if random.choice(["circle", "rectangle"]) == "circle":
            shapes.append(Circle(
                color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                x=random.randint(0, width),
                y=random.randint(0, height),
                radius=random.randint(10, 50)
            ))
        else:
            shapes.append(Rectangle(
                color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                x=random.randint(0, width),
                y=random.randint(0, height),
                width=random.randint(20, 100),
                height=random.randint(20, 100)
            ))
    return shapes
