import os
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

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print("\n" + response.text)

print("=== Study Assistant ===")
print("1. Quiz me on a topic")
print("2. Summarize my notes")
print("3. Explain a concept")

mode = input("\nChoose a mode (1/2/3): ")

if mode == "2":
    notes = input("Paste your notes: ")
    ask(mode, "", notes)
else:
    topic = input("Enter a topic: ")
    ask(mode, topic)
