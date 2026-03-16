import os
from dotenv import load_dotenv
from google import genai
import fitz

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are StudyAI, an intelligent study assistant.
Based on what the user sends you, respond appropriately:
- If they ask you to explain something, explain it clearly like a beginner
- If they ask to be quizzed, generate 5 questions on the topic
- If they paste notes or text and ask for a summary, summarize it simply
- If they ask questions about a PDF, answer based on the content provided
- If they follow up on something, use the conversation history for context
Always be helpful, clear and encouraging."""

conversation_history = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]
pdf_context = ""

def ask(prompt):
    full_prompt = prompt
    if pdf_context:
        full_prompt = f"{prompt}\n\nPDF context:\n{pdf_context}"
    
    conversation_history.append({"role": "user", "parts": [{"text": full_prompt}]})
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation_history
    )
    reply = response.text
    conversation_history.append({"role": "model", "parts": [{"text": reply}]})
    print("\nAI: " + reply)

def load_pdf(file_path):
    global pdf_context
    doc = fitz.open(file_path)
    pdf_context = ""
    for page in doc:
        pdf_context += page.get_text()
    print("✅ PDF loaded successfully!")

print("=== StudyAI Terminal ===")
print("Commands: 'load pdf' to load a PDF, 'exit' to quit")
print("Otherwise just type naturally!\n")

while True:
    user_input = input("You: ").strip()
    
    if not user_input:
        continue
    elif user_input.lower() == "exit":
        print("Goodbye!")
        break
    elif user_input.lower() == "load pdf":
        path = input("Enter PDF path: ")
        load_pdf(path)
    else:
        ask(user_input)
