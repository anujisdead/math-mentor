import easyocr
import numpy as np
from PIL import Image

# Load OCR model once
reader = easyocr.Reader(["en"], gpu=False)


def extract_text(uploaded_file):
    """
    Takes a Streamlit UploadedFile and returns (text, confidence)
    """

    # Convert uploaded file → PIL Image
    image = Image.open(uploaded_file).convert("RGB")

    # PIL → NumPy
    img_np = np.array(image)

    # Run OCR
    results = reader.readtext(img_np)

    if not results:
        return "", 0.0

    texts = []
    confidences = []

    for bbox, text, conf in results:
        texts.append(text)
        confidences.append(conf)

    full_text = " ".join(texts)
    avg_conf = sum(confidences) / len(confidences)

    return full_text, round(avg_conf, 2)
