from pathlib import Path
import cv2
from mmocr.apis import TextDetInferencer

inferencer = TextDetInferencer(model="DB_r18")
print("DBNet loaded OK")

IMG_DIR = Path("data/dev_images")
OUT_DIR = Path("debug_out")
OUT_DIR.mkdir(exist_ok=True, parents=True)

def load_bgr(path: Path):
    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Failed to read: {path}")
    return img

def main():
    paths = sorted(list(IMG_DIR.glob("*.jpg")) + list(IMG_DIR.glob("*.png")))
    print("Found", len(paths), "images")

    for p in paths[:10]:
        img_bgr = load_bgr(p)
        # TODO: detector.detect(img_bgr) -> polys
        # TODO: crop/rectify polys -> crops
        # TODO: trocr(crops) -> texts
        print("OK:", p.name)

if __name__ == "__main__":
    main()
