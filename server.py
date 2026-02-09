from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from PIL import Image
import io
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def home():
    return HTMLResponse(open("static/camera.html").read())

@app.post("/frame")
async def process_frame(file: UploadFile = File(...)):
    global frame_count
    frame_count += 1
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(img)

    # Convert RGB → BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # TEMP: just return image size
    h, w = img.shape[:2]
    if frame_count % 10 == 0:  # print every 10 frames
        print(f"[frame {frame_count}] {w}x{h}")
    return {"width": w, "height": h}
