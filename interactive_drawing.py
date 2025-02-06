import pygame
import random
import io
from flask import Response
from PIL import Image

# Initialize Pygame (without opening a window)
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))  # ✅ Off-screen surface (no display)

WHITE = (255, 255, 255)
shapes = []

class Shape:
    """Base class for all shapes."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        """Draw method to be implemented by subclasses."""
        raise NotImplementedError

class Circle(Shape):
    """Circle shape class."""
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Triangle(Shape):
    """Triangle shape class."""
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color)
        self.size = size

    def draw(self, surface):
        points = [
            (self.x, self.y - self.size),  # Top point
            (self.x - self.size, self.y + self.size),  # Bottom left
            (self.x + self.size, self.y + self.size),  # Bottom right
        ]
        pygame.draw.polygon(surface, self.color, points)

class Rectangle(Shape):
    """Rectangle shape class."""
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

def add_shape(x, y):
    """Adds a completely random shape at (x, y)."""
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    size = random.randint(20, 50)
    shape_type = random.choice(["circle", "triangle", "rectangle"])
    
    if shape_type == "circle":
        shape = Circle(x, y, color, size)
    elif shape_type == "triangle":
        shape = Triangle(x, y, color, size)
    else:
        width = random.randint(30, 70)
        height = random.randint(30, 70)
        shape = Rectangle(x, y, color, width, height)

    shapes.append(shape)

def draw_shapes():
    """Draws all shapes."""
    screen.fill(WHITE)
    for shape in shapes:
        shape.draw(screen)

def get_frame():
    """Generates a Pygame frame as an image for streaming."""
    draw_shapes()
    img_data = pygame.image.tostring(screen, "RGB")  # Convert to raw data
    img = Image.frombytes("RGB", (WIDTH, HEIGHT), img_data)  # Convert to PIL image

    img_io = io.BytesIO()
    img.save(img_io, format="JPEG")  # Convert to JPEG
    img_io.seek(0)
    return img_io.getvalue()

def generate():
    """Flask video streaming function."""
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def save_generated_art():
    """Save the generated interactive art to the uploads folder."""
    file_path = os.path.join("uploads", f"generated_art_{random.randint(1000, 9999)}.png")
    pygame.image.save(screen, file_path)
    print(f"Generated Art Saved: {file_path}")
    return file_path
