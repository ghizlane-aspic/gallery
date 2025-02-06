from PIL import Image, ImageOps
import os

def load_image(image_path):
    """Load an image."""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        print(f"Image loaded successfully: {image_path}")
        return img
    else:
        print("Image file does not exist.")
        return None

def show_image(image):
    """Display the image."""
    if image:
        image.show()

def grayscale_image(image):
    """Convert the image to grayscale."""
    return ImageOps.grayscale(image)

def rotate_image(image, angle):
    """Rotate the image by a given angle."""
    return image.rotate(angle)

def flip_image(image, direction="horizontal"):
    """Flip the image horizontally or vertically."""
    if direction == "horizontal":
        return ImageOps.mirror(image)
    elif direction == "vertical":
        return ImageOps.flip(image)
    else:
        print("Invalid direction. Use 'horizontal' or 'vertical'.")
        return image

def save_image(image, output_path):
    """Save the manipulated image."""
    image.save(output_path)
    print(f"Image saved successfully: {output_path}")

# Example usage
if __name__ == "__main__":
    img = load_image("sample.jpg")  # Replace with your image file
    if img:
        show_image(img)

        # Apply transformations
        gray_img = grayscale_image(img)
        rotated_img = rotate_image(img, 90)
        flipped_img = flip_image(img, "horizontal")

        # Save transformed images
        save_image(gray_img, "grayscale_sample.jpg")
        save_image(rotated_img, "rotated_sample.jpg")
        save_image(flipped_img, "flipped_sample.jpg")
