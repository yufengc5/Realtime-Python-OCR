from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from PIL import Image
import glob
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
latest_text_value = "No text yet..."

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    """
    Main interface of the application.
    """
    return HTMLResponse(open("static/camera.html").read())


@app.get("/text", response_class=PlainTextResponse)
def get_latest_text():
    """
    Returns the latest OCR text. Falls back to scanning the directory if needed.
    """
    global latest_text_value, latest_text_path

    # try fetching the latest cached text
    if latest_text_value and latest_text_value != "No text yet...":
        return latest_text_value

    # get the latest text file from the directory
    directory = TEXT_DIR
    if not os.path.exists(directory):
        return "No text yet..."
    
    # get all the files and find the latest one
    list_of_files = glob.glob(os.path.join(directory, "*.txt"))
    if not list_of_files:
        return "No text yet..."
    latest_file = max(list_of_files, key=os.path.getmtime)

    # read the latest text file
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
            latest_text_path = latest_file
            latest_text_value = text if text else "No text found in this frame."
            return latest_text_value
    except Exception as e:
        logger.exception(f"Failed reading latest text file: {latest_file}")
        return f"Error reading text: {e}"


@app.post("/frame")
async def process_frame(file: UploadFile = File(...)):
    """
    Receives the video frame and runs the pipeline.
    """
    global frame_count, latest_text_path, latest_text_value

    frame_count += 1
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(img)

    # convert to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    recognized_text = latest_text_value

    # Save every 2nd frame to reduce load and run OCR on it
    if frame_count % 2 == 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{SAVE_DIR}/frame_{timestamp}.jpg"
        cv2.imwrite(filename, img)

        try:
            # Run text detection and recognition on the saved frame
            cropped_images, final_boxes = extract_and_merge_text_regions(filename, show_result=False)

            recognized_texts = []
            for crop in cropped_images:
                text = recognize(crop)
                if text and text.strip():
                    recognized_texts.append(text.strip())

            recognized_text = "\n".join(recognized_texts).strip()
            if not recognized_text:
                recognized_text = "No text found in this frame."

            # Save recognized texts to a file
            text_filename = f"{TEXT_DIR}/text_{timestamp}.txt"
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(recognized_text)

            latest_text_path = text_filename
            latest_text_value = recognized_text

        except Exception as e:
            logger.exception("OCR processing failed")
            recognized_text = latest_text_value if latest_text_value else f"Error: {e}"

    h, w = img.shape[:2]
    return {
        "width": w,
        "height": h,
        "text": recognized_text,
        "latest_text_path": latest_text_path
    }