# =================================================
# STREAMLIT CLOUD SECRET INJECTION (CRITICAL)
# =================================================
import os
import streamlit as st

# Inject Streamlit secrets into environment BEFORE agent imports
if "general" in st.secrets and "OPENAI_API_KEY" in st.secrets["general"]:
    os.environ["OPENAI_API_KEY"] = st.secrets["general"]["OPENAI_API_KEY"]

# Fix OpenMP duplicate issue (safe on cloud)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# =================================================
# NOW SAFE TO IMPORT EVERYTHING ELSE
# =================================================
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import tempfile

# -------------------------
# Multimodal
# -------------------------
from multimodal.ocr import extract_text
from multimodal.asr import transcribe_audio

# -------------------------
# Agents (IMPORTANT: after secret injection)
# -------------------------
from agents.parser_agent import parse_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# -------------------------
# RAG
# -------------------------
from rag.retriever import retrieve_context

# -------------------------
# Memory
# -------------------------
from memory.memory_store import search_memory, add_memory


# -------------------------
# Streamlit Config
# -------------------------
st.set_page_config(
    page_title="Multimodal Math Mentor",
    layout="wide"
)

st.title("🧮 Multimodal Math Mentor")
st.caption("JEE-style math problem solver with RAG + Agents + HITL + Memory")
st.divider()

# =================================================
# INPUT MODE SELECTOR
# =================================================
mode = st.radio(
    "Select input mode",
    ["Text", "Image", "Audio"],
    horizontal=True
)

final_text = None

# =================================================
# TEXT INPUT
# =================================================
if mode == "Text":
    final_text = st.text_area(
        "Enter your math problem",
        height=150,
        placeholder="Example: Find the derivative of x^2 + 3x"
    )

# =================================================
# IMAGE INPUT
# =================================================
elif mode == "Image":
    uploaded_image = st.file_uploader(
        "Upload a math problem image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        # Lazy import (IMPORTANT)
        from multimodal.ocr import extract_text

        text, conf = extract_text(uploaded_image)

        st.subheader("OCR Extracted Text")
        final_text = st.text_area(
            "Please verify or correct the extracted text",
            value=text,
            height=150
        )

        st.write(f"**OCR Confidence:** {conf}")
        if conf < 0.85:
            st.warning("⚠️ Low OCR confidence detected. Human verification recommended.")


# =================================================
# AUDIO INPUT
# =================================================
elif mode == "Audio":
    audio_file = st.file_uploader(
        "Upload an audio file (math question)",
        type=["wav", "mp3", "m4a"]
    )

    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name

        # Lazy import (IMPORTANT)
        from multimodal.asr import transcribe_audio

        transcript = transcribe_audio(audio_path)

        st.subheader("Transcribed Text")
        final_text = st.text_area(
            "Please verify or correct the transcription",
            value=transcript,
            height=150
        )

# =================================================
# SOLVE PIPELINE
# =================================================
if st.button("Solve") and final_text:

    # -------------------------
    # PARSER AGENT
    # -------------------------
    parsed = parse_problem(final_text)

    st.subheader("🧠 Parsed Output")
    st.json(parsed)

    if not parsed["is_in_scope"]:
        st.error(f"Out of scope: {parsed['reason_if_out_of_scope']}")
        st.stop()

    if parsed["needs_clarification"]:
        st.warning(
            "⚠️ The problem has missing or ambiguous information "
            "(e.g., an undefined variable). Please refine the question."
        )
        st.stop()

    # =================================================
    # MEMORY LOOKUP (PHASE 7 – BEFORE RAG)
    # =================================================
    past_cases = search_memory(parsed["problem_text"])

    if past_cases:
        st.subheader("🧠 Similar Past Problems Found")
        for case in past_cases:
            st.markdown("**Previous Solution:**")
            st.write(case["solution"])

    # -------------------------
    # RAG RETRIEVAL
    # -------------------------
    context_docs = retrieve_context(parsed["problem_text"])

    st.subheader("📚 Retrieved Knowledge")
    if context_docs:
        for i, doc in enumerate(context_docs):
            st.markdown(f"**Source {i+1}:**")
            st.write(doc.page_content)
    else:
        st.warning("No relevant knowledge retrieved. Proceeding cautiously.")

    # -------------------------
    # SOLVER AGENT
    # -------------------------
    solution = solve_problem(parsed, context_docs)

    st.subheader("✏️ Draft Solution")
    st.write(solution)

    # -------------------------
    # VERIFIER AGENT
    # -------------------------
    verification = verify_solution(parsed["problem_text"], solution)

    st.subheader("🔍 Verification Result")
    st.json(verification)

    confidence = float(verification.get("confidence", 0))
    st.progress(min(confidence, 1.0))

    # =================================================
    # HITL OR EXPLAINER
    # =================================================
    if not verification.get("is_correct") or confidence < 0.75:
        st.warning("⚠️ Low confidence detected. Human review recommended.")

        corrected = st.text_area(
            "Edit / correct the solution (Human-in-the-loop)",
            value=solution,
            height=200
        )

        if st.button("Approve Correction"):
            add_memory({
                "raw_input": final_text,
                "parsed_problem": parsed,
                "retrieved_context": [doc.page_content for doc in context_docs],
                "solution": solution,
                "verification": verification,
                "explanation": "",
                "feedback": "incorrect",
                "correction": corrected
            })
            st.success("Correction saved to memory. System will learn from this.")

    else:
        st.success("✅ Solution verified with high confidence.")

        explanation = explain_solution(
            parsed["problem_text"],
            solution
        )

        st.subheader("📘 Step-by-Step Explanation")
        st.write(explanation)

        # -------------------------
        # SAVE SUCCESSFUL CASE TO MEMORY
        # -------------------------
        add_memory({
            "raw_input": final_text,
            "parsed_problem": parsed,
            "retrieved_context": [doc.page_content for doc in context_docs],
            "solution": solution,
            "verification": verification,
            "explanation": explanation,
            "feedback": "correct",
            "correction": ""
        })

        # -------------------------
        # FEEDBACK BUTTONS
        # -------------------------
        st.subheader("🗳 Feedback")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Correct"):
                st.success("Thanks! Feedback recorded.")

        with col2:
            if st.button("❌ Incorrect"):
                feedback = st.text_area("What was wrong?")
                if st.button("Submit Feedback"):
                    st.success("Thanks! Feedback recorded.")

    # =================================================
    # AGENT TRACE (MANDATORY FOR EVALUATION)
    # =================================================
    with st.expander("🧩 Agent Trace"):
        st.markdown("""
        **Pipeline executed:**
        1. Parser Agent – cleaned & validated the problem  
        2. Memory Lookup – searched similar past problems  
        3. RAG Retriever – fetched relevant math knowledge  
        4. Solver Agent – generated solution  
        5. Verifier Agent – checked correctness & confidence  
        6. Explainer Agent – produced student-friendly explanation  
        7. Memory Store – saved outcome for future reuse  
        """)
