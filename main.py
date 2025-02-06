import pygame
from art import create_random_shapes
from shapes import Circle, Rectangle
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 600, 600

# Colors
BACKGROUND_COLOR = (0, 0, 0)

# Create the Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Generative Art")

# Generate Random Shapes
shapes = create_random_shapes(20, WIDTH, HEIGHT)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Interactivity: Change shape color on click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for shape in shapes:
                if isinstance(shape, Circle):
                    # Check if click is within the circle
                    if (shape.x - x) ** 2 + (shape.y - y) ** 2 <= shape.radius ** 2:
                        shape.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif isinstance(shape, Rectangle):
                    # Check if click is within the rectangle
                    if shape.x <= x <= shape.x + shape.width and shape.y <= y <= shape.y + shape.height:
                        shape.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw all shapes
    for shape in shapes:
        shape.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


from data_processor import DataProcessor
from visualization import Visualizer

# Load and preprocess data
data_file = "weather.csv"  # Replace with your dataset file
processor = DataProcessor(data_file)
processor.load_data()
processor.preprocess_data()

# Generate visualizations
if processor.data is not None:
    visualizer = Visualizer(processor.data)
    visualizer.generate_heatmap("uploads/artistic_heatmap.png")


from image_manipulation import (
    load_image,
    show_image,
    grayscale_image,
    rotate_image,
    flip_image,
    save_image,
)
from audio_manipulation import (
    load_audio,
    play_audio,
    change_speed,
    reverse_audio,
    save_audio,
)

def image_menu():
    """Menu for image manipulation."""
    image_path = input("Enter the path to your image file: ")
    img = load_image(image_path)
    if not img:
        return

    while True:
        print("\nImage Manipulation Options:")
        print("1. Display Image")
        print("2. Convert to Grayscale")
        print("3. Rotate Image")
        print("4. Flip Image")
        print("5. Save Image")
        print("6. Exit Image Manipulation")

        choice = input("Enter your choice: ")
        if choice == "1":
            show_image(img)
        elif choice == "2":
            img = grayscale_image(img)
            print("Image converted to grayscale.")
        elif choice == "3":
            angle = int(input("Enter the rotation angle (e.g., 90, 180): "))
            img = rotate_image(img, angle)
            print(f"Image rotated by {angle} degrees.")
        elif choice == "4":
            direction = input("Enter flip direction ('horizontal' or 'vertical'): ")
            img = flip_image(img, direction)
            print(f"Image flipped {direction}.")
        elif choice == "5":
            output_path = input("Enter the output file path (e.g., output.jpg): ")
            save_image(img, output_path)
        elif choice == "6":
            print("Exiting Image Manipulation.")
            break
        else:
            print("Invalid choice. Please try again.")

def audio_menu():
    """Menu for audio manipulation."""
    audio_path = input("Enter the path to your audio file: ")
    audio = load_audio(audio_path)
    if not audio:
        return

    while True:
        print("\nAudio Manipulation Options:")
        print("1. Play Audio")
        print("2. Change Speed")
        print("3. Reverse Audio")
        print("4. Save Audio")
        print("5. Exit Audio Manipulation")

        choice = input("Enter your choice: ")
        if choice == "1":
            play_audio(audio)
        elif choice == "2":
            speed = float(input("Enter speed factor (e.g., 0.5 for half speed, 2 for double speed): "))
            audio = change_speed(audio, speed)
            print(f"Audio speed changed to {speed}x.")
        elif choice == "3":
            audio = reverse_audio(audio)
            print("Audio reversed.")
        elif choice == "4":
            output_path = input("Enter the output file path (e.g., output.wav): ")
            save_audio(audio, output_path)
        elif choice == "5":
            print("Exiting Audio Manipulation.")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main menu for the program."""
    while True:
        print("\nInteractive Art Gallery - Main Menu:")
        print("1. Image Manipulation")
        print("2. Audio Manipulation")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            image_menu()
        elif choice == "2":
            audio_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response, jsonify
import os
from image_manipulation import load_image, grayscale_image, rotate_image, flip_image, save_image
from audio_manipulation import load_audio, play_audio, change_speed, reverse_audio, save_audio 
from visualization import Visualizer 
from data_processor import DataProcessor 
import pygame
from art import create_random_shapes 
from interactive_drawing import add_shape, draw_shapes, get_frame, generate
from ai_art import apply_style_transfer  # Import AI function

app = Flask(__name__)


# ✅ Ensure 'uploads' folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

AUDIO_UPLOAD_FOLDER = os.path.join("uploads", "mp3")  # ✅ Matches your structure
os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)
app.config["AUDIO_UPLOAD_FOLDER"] = AUDIO_UPLOAD_FOLDER


# ✅ Home Page Route
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/gallery')
def gallery():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('png', 'jpg', 'jpeg'))]
    return render_template("gallery.html", images=images)


# ✅ Image Upload & Display Page (Fixes Duplicate Route)
@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        if "file" not in request.files:
            return "No file part", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        # ✅ Save file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # ✅ Redirect to include filename as a query parameter
        return redirect(url_for("image", filename=file.filename))

    # ✅ Ensure the filename is retrieved from the query parameter
    filename = request.args.get('filename', None)
    return render_template("image.html", image_path=filename)

# ✅ FIX: Add route for image manipulation
@app.route('/manipulate_image', methods=['POST'])
def manipulate_image():
    action = request.form['action']
    image_filename = request.form.get('image_path')

    if not image_filename:
        return "No image provided", 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
    img = load_image(image_path)
    
    if action == 'grayscale':
        img = grayscale_image(img)
    elif action == 'rotate':
        img = rotate_image(img, 90)
    elif action == 'flip':
        img = flip_image(img, 'horizontal')

    output_filename = "edited_" + image_filename
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)
    save_image(img, output_path)

    return redirect(url_for("image", filename=output_filename))


# ✅ Serve Uploaded Files
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/audio', methods=['GET', 'POST'])
def audio():
    if request.method == 'POST':
        if "audio" not in request.files:
            return "No audio file part", 400  # Prevents KeyError

        file = request.files["audio"]
        if file.filename == "":
            return "No selected file", 400

        file_path = os.path.join(app.config["AUDIO_UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        print(f"Uploaded audio: {file.filename}")

        # ✅ Pass the filename in the query string to show manipulation buttons
        return redirect(url_for("audio", filename=file.filename))

    filename = request.args.get('filename', None)  # Ensure filename is passed
    return render_template("audio.html", audio_path=filename)


@app.route('/manipulate_audio', methods=['POST'])
def manipulate_audio():
    action = request.form['action']
    audio_filename = request.form['audio_path']  # Keep the original filename
    audio_path = os.path.join(AUDIO_UPLOAD_FOLDER, audio_filename)  # Join correctly

    # Debugging to check if file exists
    print(f"🎵 Received Request to Manipulate: {audio_filename}")
    print(f"🔍 Looking for file at: {audio_path}")

    # Check if the audio file exists before proceeding
    if not os.path.exists(audio_path):
        print(f"❌ File Not Found: {audio_path}")
        return "Error: Audio file not found", 404

    # Load the audio file
    audio = load_audio(audio_path)
    if not audio:
        print("❌ Failed to load audio file.")
        return "Error: Unable to load audio file", 500

    # Perform the requested manipulation
    if action == 'reverse':
        print("🔄 Reversing audio...")
        audio = reverse_audio(audio)
    elif action == 'speed_up':
        print("⏩ Speeding up audio...")
        audio = change_speed(audio, 1.5)

    # Define the edited filename and path
    edited_filename = f"edited_{audio_filename}"
    edited_audio_path = os.path.join(AUDIO_UPLOAD_FOLDER, edited_filename)

    # Save the manipulated file
    save_audio(audio, edited_audio_path)
    print(f"✅ Saved Edited File at: {edited_audio_path}")

    # Return the new file to be displayed in audio.html
    return render_template("audio.html", audio_path=edited_filename)

@app.route('/uploads/mp3/<filename>')
def serve_uploaded_audio(filename):
    return send_from_directory(app.config["AUDIO_UPLOAD_FOLDER"], filename)

@app.route('/visualization')
def visualization():
    data_file = "weather.csv"
    processor = DataProcessor(data_file)
    processor.load_data()
    processor.preprocess_data()
    
    if processor.data is not None:
        visualizer = Visualizer(processor.data)
        visualizer.generate_heatmap("uploads/tic_heatmap.png")
    
    return render_template('visualization.html', image_path="uploads/artistic_heatmap.png")

@app.route('/interactive_art', methods=['GET', 'POST'])
def interactive_art():
    if request.method == "POST":
        generated_image = save_generated_art()
        return render_template("art.html", generated_image=generated_image)
    return render_template("art.html")

@app.route('/interactive_feed')
def interactive_feed():
    """Stream Pygame-generated images."""
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/add_shape', methods=['POST'])
def click_add_shape():
    """Add a shape when the user clicks the webpage."""
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))
    add_shape(x, y)
    return "Shape Added", 200

# ✅ Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
  

@app.route('/uploads/stylized/<filename>')
def serve_stylized_image(filename):
    return send_from_directory("uploads/stylized", filename)

@app.route('/ai_art')
def ai_art():
    return render_template("ai_art.html")

@app.route('/generate_ai_art', methods=['POST'])
def generate_ai_art():
    sample_image_path = "uploads/1.jpg"  # Replace this with a real image path
    generated_image_path = apply_style_transfer(sample_image_path, None)
    
    return render_template("ai_art.html", generated_image=generated_image_path)
from flask import send_from_directory



if __name__ == '__main__':
    app.run(debug=True)

