import numpy as np
from PIL import Image
import easyocr
import streamlit as st

# Cache OCR model so it loads only once
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(["en"], gpu=False)


def extract_text(uploaded_file):
    """
    Safe OCR for Streamlit UploadedFile
    Returns (text, confidence)
    """
    try:
        # IMPORTANT: reset file pointer
        uploaded_file.seek(0)

        # Convert to image
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)

        reader = load_ocr_reader()
        results = reader.readtext(img_np)

        if not results:
            return "", 0.0

        texts, confidences = [], []
        for _, text, conf in results:
            texts.append(text)
            confidences.append(conf)

        return " ".join(texts), round(sum(confidences) / len(confidences), 2)

    except Exception as e:
        # This prevents Streamlit hard crash
        st.error(f"OCR failed: {e}")
        return "", 0.0
