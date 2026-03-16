import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from memory import save_session, load_session, list_sessions

load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

st.title("🎓 StudyAI")
st.caption("Your AI-powered study assistant")

if "history" not in st.session_state:
    st.session_state.history = []

backend = st.sidebar.radio("AI Backend", ["☁️ Gemini", "💻 Local (LM Studio)"])

mode = st.sidebar.selectbox("Choose a mode", [
    "💡 Explain a concept",
    "📝 Quiz me",
    "📄 Summarize notes",
    "📂 Ask about a PDF"
])

def ask(prompt):
    st.session_state.history.append({"role": "user", "parts": [{"text": prompt}]})

    if "Gemini" in backend:
        response = gemini_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=st.session_state.history
        )
        reply = response.text
    else:
        messages = [
            {"role": "user" if m["role"] == "user" else "assistant", "content": m["parts"][0]["text"]}
            for m in st.session_state.history
        ]
        response = local_client.chat.completions.create(
            model="local-model",
            messages=messages
        )
        reply = response.choices[0].message.content

    st.session_state.history.append({"role": "model", "parts": [{"text": reply}]})
    return reply

for msg in st.session_state.history:
    role = "You" if msg["role"] == "user" else "AI"
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(msg["parts"][0]["text"])

if "Explain" in mode:
    topic = st.text_input("Enter a concept:")
    if st.button("Explain") and topic:
        ask(f"Explain this like I'm a beginner: {topic}")
        st.rerun()

elif "Quiz" in mode:
    topic = st.text_input("Enter a topic:")
    if st.button("Quiz me") and topic:
        ask(f"Quiz me with 5 questions about: {topic}")
        st.rerun()

elif "Summarize" in mode:
    notes = st.text_area("Paste your notes:")
    if st.button("Summarize") and notes:
        ask(f"Summarize this in simple terms:\n{notes}")
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
        ask(f"Based on this document answer:\n{question}\n\nDocument:\n{pdf_text}")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Sessions")

sessions = list_sessions()
if sessions:
    selected = st.sidebar.selectbox("Load a session:", ["-- Select --"] + sessions)
    if selected != "-- Select --":
        if st.sidebar.button("Load"):
            st.session_state.history = load_session(f"sessions/{selected}")
            st.rerun()

if st.sidebar.button("💾 Save session"):
    if st.session_state.history:
        filename = save_session(st.session_state.history)
        st.sidebar.success(f"Saved!")
    else:
        st.sidebar.warning("Nothing to save yet.")


if st.sidebar.button("Clear conversation"):
    st.session_state.history = []
    st.rerun()