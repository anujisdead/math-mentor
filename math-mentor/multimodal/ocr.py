import easyocr
from PIL import Image
import numpy as np

# Initialize once (slow otherwise)
reader = easyocr.Reader(["en"], gpu=False)

def extract_text(image_file):
    image = Image.open(image_file).convert("RGB")
    img_array = np.array(image)

    results = reader.readtext(img_array)

    text_lines = []
    confidences = []

    for bbox, text, conf in results:
        text_lines.append(text)
        confidences.append(conf)

    extracted_text = " ".join(text_lines)
    avg_confidence = round(sum(confidences) / len(confidences), 2) if confidences else 0.0

    return extracted_text, avg_confidence
