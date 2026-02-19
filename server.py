from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from PIL import Image
import io
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from group_bbox import extract_and_merge_text_regions
from recognition import recognize
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SAVE_DIR = "captured_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

frame_count = 0

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

    if frame_count % 10 == 0:
        filename = f"{SAVE_DIR}/frame_{frame_count}.jpg"
        cv2.imwrite(filename, img)
        
        # Run text detection and recognition on the saved frame
        cropped_images, final_boxes = extract_and_merge_text_regions(filename, show_result=False)
        recognized_texts = []
        for crop in cropped_images:
            recognized_texts.append(recognize(crop))

        logger.info(f"Saved: {filename}, Recognized texts: {recognized_texts}")
        
    h, w = img.shape[:2]
    return {"width": w, "height": h}
