import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🎓 StudyAI")
st.caption("Your AI-powered study assistant")

if "history" not in st.session_state:
    st.session_state.history = []

mode = st.sidebar.selectbox("Choose a mode", [
    "💡 Explain a concept",
    "📝 Quiz me",
    "📄 Summarize notes",
    "📂 Ask about a PDF"
])

def ask(prompt):
    st.session_state.history.append({"role": "user", "parts": [{"text": prompt}]})
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=st.session_state.history
    )
    reply = response.text
    st.session_state.history.append({"role": "model", "parts": [{"text": reply}]})
    return reply

for msg in st.session_state.history:
    role = "You" if msg["role"] == "user" else "AI"
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(msg["parts"][0]["text"])

if "Explain" in mode:
    topic = st.text_input("Enter a concept:")
    if st.button("Explain") and topic:
        reply = ask(f"Explain this like I'm a beginner: {topic}")
        st.rerun()

elif "Quiz" in mode:
    topic = st.text_input("Enter a topic:")
    if st.button("Quiz me") and topic:
        reply = ask(f"Quiz me with 5 questions about: {topic}")
        st.rerun()

elif "Summarize" in mode:
    notes = st.text_area("Paste your notes:")
    if st.button("Summarize") and notes:
        reply = ask(f"Summarize this in simple terms:\n{notes}")
        st.rerun()

elif "PDF" in mode:
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    question = st.text_input("What do you want to know?")
    if st.button("Ask") and uploaded_file and question:
        import fitz
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()
        reply = ask(f"Based on this document answer:\n{question}\n\nDocument:\n{pdf_text}")
        st.rerun()

if st.sidebar.button("Clear conversation"):
    st.session_state.history = []
    st.rerun()
