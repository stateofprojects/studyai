# StudyAI

An AI-powered study assistant that helps you learn any topic through quizzes, summaries, and explanations. Supports both cloud AI (Gemini) and fully offline local AI (LM Studio).

## Features
- 💬 Smart chat — detects intent automatically, no mode switching needed
- 💡 Explain — get beginner-friendly explanations of any concept
- 📝 Quiz — generates 5 questions on any topic
- 📄 Summarize — paste notes and get a clean summary
- 📂 PDF support — upload any PDF and ask questions about it (RAG pipeline)
- 🧠 Conversation memory — follows up on previous answers within a session
- 💾 Save & load sessions — export study sessions to JSON and reload them later
- ☁️ Cloud AI — powered by Google Gemini API
- 💻 Local AI — runs fully offline via LM Studio, no API needed

## How PDF mode works
Extracts text from a PDF using PyMuPDF and passes it as context to the AI model. This is a basic implementation of Retrieval Augmented Generation (RAG).

## How session saving works
Conversations are saved as timestamped JSON files locally. Load any previous session to restore full context — the AI picks up exactly where you left off.

## Setup
1. Clone this repo
2. Install dependencies:
```
pip install google-genai python-dotenv pymupdf streamlit openai
```
3. Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your-key-here
```
4. Optional: Download LM Studio from lmstudio.ai and load any local model for fully offline use

## Running the app
- Web UI: `streamlit run app.py`
- Terminal version: `python main.py`

## Tech used
- Python
- Google Gemini API
- LM Studio (local AI)
- PyMuPDF
- Streamlit
- python-dotenv
- OpenAI SDK