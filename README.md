# StudyAI

An AI-powered study assistant that helps you learn any topic through quizzes, summaries, and explanations — built with Python and the Gemini API.

## Features
- 📝 Quiz mode — generates 5 questions on any topic
- 📄 Summarize mode — paste your notes and get a clean summary
- 💡 Explain mode — get a beginner-friendly explanation of any concept
- 📂 PDF mode — upload any PDF and ask questions about it (RAG pipeline)

## How PDF mode works
Extracts text from a PDF using PyMuPDF, passes it as context to Gemini, and answers questions based on the document content. This is a basic implementation of Retrieval Augmented Generation (RAG).

## Setup
1. Clone this repo
2. Install dependencies: `pip install google-genai python-dotenv pymupdf`
3. Create a `.env` file and add your Gemini API key: `GEMINI_API_KEY=your-key-here`
4. Run: `python main.py`

## Tech used
- Python
- Google Gemini API
- PyMuPDF
- python-dotenv
