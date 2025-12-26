import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Multimodal Math Mentor",
    layout="wide"
)

st.title("🧮 Multimodal Math Mentor")
st.caption("JEE-style math problem solver with RAG + Agents + HITL")

st.divider()

# Input Mode Selector
mode = st.radio(
    "Select input mode",
    ["Text", "Image", "Audio"],
    horizontal=True
)

if mode == "Text":
    user_text = st.text_area(
        "Enter your math problem",
        height=150,
        placeholder="Example: Find the derivative of x^2 + 3x"
    )

    if st.button("Solve"):
        if user_text.strip() == "":
            st.warning("Please enter a math problem.")
        else:
            st.success("Input received successfully!")
            st.write("### Raw Input")
            st.write(user_text)

elif mode == "Image":
    st.info("Image input will be enabled in Phase 2")

elif mode == "Audio":
    st.info("Audio input will be enabled in Phase 2")
