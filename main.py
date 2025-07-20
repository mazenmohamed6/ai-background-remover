from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from PIL import Image
import re
import io

app = FastAPI()

def parse_rgba_color(rgba_string):
    match = re.match(r'rgba\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', rgba_string)
    if not match:
        raise ValueError(f"Invalid color format: {rgba_string}")
    r, g, b, a = map(float, match.groups())
    return (int(r), int(g), int(b))

@app.post("/remove-bg/")
async def remove_background(
    file: UploadFile = File(...),
    color: str = Form("rgba(255,255,255,1.0)")  # default: white background
):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")

        # Remove background
        image_no_bg = remove(image)

        # Apply background color
        color_rgb = parse_rgba_color(color)
        bg = Image.new("RGB", image_no_bg.size, color_rgb)
        bg.paste(image_no_bg, (0, 0), image_no_bg)

        output_io = io.BytesIO()
        bg.save(output_io, format="PNG")
        output_io.seek(0)

        return StreamingResponse(output_io, media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
