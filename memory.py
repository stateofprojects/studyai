import json
import os
from datetime import datetime

def save_session(history):
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sessions/session_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)
    return filename

def load_session(filename):
    with open(filename, "r") as f:
        return json.load(f)

def list_sessions():
    if not os.path.exists("sessions"):
        return []
    return sorted(os.listdir("sessions"), reverse=True)