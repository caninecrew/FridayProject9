import sys # Importing sys for system-specific parameters and functions
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTextEdit) # Importing necessary PyQt5 widgets
from PyQt5.QtCore import Qt # Importing Qt for Qt-specific features
from openai import OpenAI # Importing OpenAI for API interaction
from dotenv import load_dotenv # Importing load_dotenv for loading environment variables
import os # Importing os for operating system dependent functionality

class OpenAIGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
    def setup_openai(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn."
        }
    ]
)

print(completion.choices[0].message.content)
