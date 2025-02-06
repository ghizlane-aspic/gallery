import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import cv2
import numpy as np
import os

def generate_ai_art():
    sample_image = "static/sample.jpg"
    if not os.path.exists(sample_image):
        return "Error: Sample image not found!", 404
    
    generated_image_path = apply_style_transfer(sample_image, None)
    return render_template("ai_art.html", generated_image=generated_image_path)

def apply_style_transfer(content_path, style_path):
    if not os.path.exists(content_path):
        print(f"Error: {content_path} not found!")
        return None

    content_img = cv2.imread(content_path)
    
    # Simple effect (blur as a placeholder for style transfer)
    styled_img = cv2.GaussianBlur(content_img, (21, 21), 0)
    
  
    output_path = os.path.join("uploads/stylized", "styled_image.jpg")
    os.makedirs("uploads/stylized", exist_ok=True)
    cv2.imwrite(output_path, styled_img)

    return "stylized/styled_image.jpg"
