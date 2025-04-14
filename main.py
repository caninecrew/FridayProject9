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

    def ininUI(self): # Initializing the UI components
        # Set window properties
        self.setWindowTitle('OpenAI Interface')
        self.setGeometry(300, 300, 600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Add title label
        title_label = QLabel('OpenAI Interface')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold;')
        main_layout.addWidget(title_label)

        # Add input area
        prompt_label = QLabel('Enter your prompt:')
        main_layout.addWidget(prompt_label)

        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText('Write your prompt here...')
        self.prompt_text.setMinimumHeight(100)
        main_layout.addWidget(self.prompt_text)

        # Add button
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.get_response)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Add response area
        response_label = QLabel('Response:')
        main_layout.addWidget(response_label)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText('Response will appear here...')
        main_layout.addWidget(self.response_text)

        # Set central widget
        self.setCentralWidget(central_widget)

    def get_response(self):
        prompt = self.prompt_text.toPlainText()
        if not prompt:
            self.response_text.setText("Please enter a prompt.")
            return
            
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response = completion.choices[0].message.content
            self.response_text.setText(response)
            print(response)  # Also print to console for debugging
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.response_text.setText(error_message)
            print(error_message)
def main():
    app = QApplication(sys.argv) # Creating a QApplication instance
    gui = OpenAIGUI() # Creating an instance of OpenAIGUI
    gui.show() # Showing the GUI window
    sys.exit(app.exec_()) # Exiting the application when the window is closed

if __name__ == '__main__':
    main()