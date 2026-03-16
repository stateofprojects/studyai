import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from memory import save_session, load_session, list_sessions

load_dotenv()

st.title("🎓 StudyAI")
st.caption("Your AI-powered study assistant")

# Sidebar — API key
api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password", placeholder="Paste your key here")
gemini_client = genai.Client(api_key=api_key) if api_key else None
local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

SYSTEM_PROMPT = """You are StudyAI, an intelligent study assistant. 
Based on what the user sends you, respond appropriately:
- If they ask you to explain something, explain it clearly like a beginner
- If they ask to be quizzed, generate 5 questions on the topic
- If they paste notes or text and ask for a summary, summarize it simply
- If they ask questions about a PDF they uploaded, answer based on the content
- If they follow up on something, use the conversation history for context
Always be helpful, clear and encouraging."""

if "history" not in st.session_state:
    st.session_state.history = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# Sidebar — AI backend
backend = st.sidebar.radio("AI Backend", ["☁️ Gemini", "💻 Local (LM Studio)"])

# Sidebar — PDF upload
st.sidebar.markdown("---")
st.sidebar.subheader("📂 PDF")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", label_visibility="collapsed")
if uploaded_file:
    import fitz
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.session_state.pdf_text = ""
    for page in doc:
        st.session_state.pdf_text += page.get_text()
    st.sidebar.success("✅ PDF loaded!")
if st.session_state.pdf_text:
    if st.sidebar.button("❌ Remove PDF"):
        st.session_state.pdf_text = ""
        st.rerun()

# Sidebar — Sessions
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Sessions")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("💾 Save"):
        if st.session_state.history:
            save_session(st.session_state.history)
            st.sidebar.success("Saved!")
        else:
            st.sidebar.warning("Nothing to save.")
with col2:
    if st.sidebar.button("🗑️ Clear"):
        st.session_state.history = []
        st.session_state.pdf_text = ""
        st.rerun()

sessions = list_sessions()
if sessions:
    selected = st.sidebar.selectbox("Load a session:", ["-- Select --"] + sessions)
    if selected != "-- Select --":
        if st.sidebar.button("📂 Load"):
            st.session_state.history = load_session(f"sessions/{selected}")
            st.rerun()

def ask(prompt):
    if "Gemini" in backend and not api_key:
        st.error("Please enter your Gemini API key in the sidebar to use cloud AI.")
        return ""

    if st.session_state.pdf_text:
        full_prompt = f"{prompt}\n\nPDF context:\n{st.session_state.pdf_text}"
    else:
        full_prompt = prompt

    st.session_state.history.append({"role": "user", "parts": [{"text": full_prompt}]})

    if "Gemini" in backend:
        response = gemini_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}] + st.session_state.history
        )
        reply = response.text
    else:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in st.session_state.history:
            messages.append({
                "role": "user" if m["role"] == "user" else "assistant",
                "content": m["parts"][0]["text"]
            })
        response = local_client.chat.completions.create(
            model="local-model",
            messages=messages
        )
        reply = response.choices[0].message.content

    st.session_state.history.append({"role": "model", "parts": [{"text": reply}]})
    return reply

# Chat history
for msg in st.session_state.history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["parts"][0]["text"])

# Chat input
if prompt := st.chat_input("Ask anything — explain, quiz, summarize..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask(prompt)
        if reply:
            st.markdown(reply)
    st.rerun()