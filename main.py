import sys # Importing sys for system-specific parameters and functions
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTextEdit) # Importing necessary PyQt5 widgets
from PyQt5.QtCore import Qt # Importing Qt for Qt-specific features
from openai import OpenAI # Importing OpenAI for API interaction
from dotenv import load_dotenv # Importing load_dotenv for loading environment variables
import os # Importing os for operating system dependent functionality

class OpenAIGUI(QMainWindow):
    def __init__(self):
        super().__init__() # Initializing the parent class
        
    def setup_openai(self):
        load_dotenv() # Loading environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY") # Loading the OpenAI API key from environment variables
        self.client = OpenAI(api_key=api_key) # Initializing OpenAI client with the API key

    def ininUI(self):
        # Set window properties
        self.setWindowTitle('OpenAI Interface')
        self.setGeometry(300, 300, 600, 400)
        
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
