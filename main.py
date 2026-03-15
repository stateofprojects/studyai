import os
import pymupdf
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask(mode, topic, notes=""):
    if mode == "1":
        prompt = f"Quiz me with 5 questions about: {topic}"
    elif mode == "2":
        prompt = f"Summarize this in simple terms:\n{notes}"
    elif mode == "3":
        prompt = f"Explain this like I'm a beginner:\n{topic}"
    elif mode == "4":
        prompt = f"Based on this document, answer the following:\n{notes}\n\nDocument content:\n{topic}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print("\n" + response.text)

print("=== Study Assistant ===")
print("1. Quiz me on a topic")
print("2. Summarize my notes")
print("3. Explain a concept")
print("4. Ask questions about a PDF")


mode = input("\nChoose a mode (1/2/3/4): ")

if mode == "2":
    notes = input("Paste your notes: ")
    ask(mode, "", notes)
elif mode == "4":
    file_path = input("Enter the path to your PDF file: ")
    from pdf_reader import read_pdf
    pdf_text = read_pdf(file_path)
    question = input("What do you want to know about this PDF? ")
    ask(mode, pdf_text, question)
else:
    topic = input("Enter a topic: ")
    ask(mode, topic)
