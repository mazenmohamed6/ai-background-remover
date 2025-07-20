import gradio as gr
from PIL import Image
from rembg import remove
import re

def parse_rgba_color(rgba_string):
    # Extract numbers using regex
    match = re.match(r'rgba\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', rgba_string)
    if not match:
        raise ValueError(f"Invalid color format: {rgba_string}")
    r, g, b, a = map(float, match.groups())
    return (int(r), int(g), int(b))  # We ignore alpha channel here

def remove_and_replace_background(image, color):
    # Convert rgba string to RGB tuple
    if isinstance(color, str) and color.startswith('rgba'):
        color = parse_rgba_color(color)

    # Step 1: Remove background
    image_no_bg = remove(image)

    # Step 2: Apply new background color
    bg = Image.new("RGB", image_no_bg.size, color)
    bg.paste(image_no_bg, (0, 0), image_no_bg)

    return bg

# Launch Gradio interface
interface = gr.Interface(
    fn=remove_and_replace_background,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.ColorPicker(label="Background Color")
    ],
    outputs=gr.Image(type="pil", label="Image with New Background"),
    title="AI Background Remover",
    description="Upload an image and choose a background color. This tool uses AI to remove the background and apply your custom background color.",
)

if __name__ == "__main__":
    interface.launch()
