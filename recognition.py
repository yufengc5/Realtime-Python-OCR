from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import cv2
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

processor_hw = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model_hw = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
).to(device)

processor_pr = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model_pr = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-printed"
).to(device)

def is_printed(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = edges.mean() / 255.0
    return edge_ratio > 0.05

def recognize_with_trocr(crop, processor, model):
    # BGR -> RGB -> PIL
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)

    pixel_values = processor(images=pil_img, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    with torch.no_grad():
        generated_ids = model.generate(pixel_values)

    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text


def recognize(crop):
    if is_printed(crop):
        print("Printed text detected.")
        return recognize_with_trocr(crop, processor_pr, model_pr)
    else:
        print("Handwritten text detected.")
        return recognize_with_trocr(crop, processor_hw, model_hw)


img = cv2.imread("temp/merged_crop_2.jpg")
text = recognize(img)
print(f"Recognized text: {text}")
