import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = []

def ask(prompt):
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation_history
    )
    
    reply = response.text
    conversation_history.append({"role": "model", "parts": [{"text": reply}]})
    
    print("\nAI: " + reply)

def read_pdf(file_path):
    import fitz
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

while True:
    print("\n=== Study Assistant ===")
    print("1. Quiz me on a topic")
    print("2. Summarize my notes")
    print("3. Explain a concept")
    print("4. Ask questions about a PDF")
    print("5. Follow up / continue conversation")
    print("6. Exit")

    mode = input("\nChoose a mode (1-6): ")

    if mode == "1":
        topic = input("Enter a topic: ")
        ask(f"Quiz me with 5 questions about: {topic}")
    elif mode == "2":
        notes = input("Paste your notes: ")
        ask(f"Summarize this in simple terms:\n{notes}")
    elif mode == "3":
        topic = input("Enter a concept: ")
        ask(f"Explain this like I'm a beginner:\n{topic}")
    elif mode == "4":
        file_path = input("Enter the path to your PDF file: ")
        pdf_text = read_pdf(file_path)
        question = input("What do you want to know about this PDF? ")
        ask(f"Based on this document, answer the following:\n{question}\n\nDocument content:\n{pdf_text}")
    elif mode == "5":
        follow_up = input("Your follow up: ")
        ask(follow_up)
    elif mode == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please pick 1-6")