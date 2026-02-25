from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from PIL import Image
import io
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from group_bbox import extract_and_merge_text_regions
from recognition import recognize
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SAVE_DIR = "captured_frames"
TEXT_DIR = "recognized_texts"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

frame_count = 0
latest_text_path = None

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def home():
    return HTMLResponse(open("static/camera.html").read())

@app.get("/text", response_class=PlainTextResponse)
def get_latest_text():
    """
    Returns the content of the most recently written OCR text file.
    """
    global latest_text_path

    if not latest_text_path or not os.path.exists(latest_text_path):
        return "No text yet..."

    try:
        with open(latest_text_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.exception("Failed reading latest text file")
        return f"Error reading text: {e}"


@app.post("/frame")
async def process_frame(file: UploadFile = File(...)):
    global frame_count, latest_text_path
    frame_count += 1
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(img)

    # Convert RGB → BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if frame_count % 2 == 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SAVE_DIR}/frame_{timestamp}.jpg"
        cv2.imwrite(filename, img)
        
        # Run text detection and recognition on the saved frame
        cropped_images, final_boxes = extract_and_merge_text_regions(filename, show_result=False)
        recognized_texts = []
        for crop in cropped_images:
            recognized_texts.append(recognize(crop))

        # Save recognized texts to a file
        text_filename = f"{TEXT_DIR}/text_{timestamp}.txt"
        with open(text_filename, "w", encoding="utf-8") as f:
            for text in recognized_texts:
                f.write(text + "\n")

        latest_text_path = text_filename    

        #logger.info(f"Saved: {filename}, Recognized texts: {recognized_texts}")
        
    h, w = img.shape[:2]
    return {"width": w, "height": h}
