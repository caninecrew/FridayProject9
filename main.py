import sys # Importing sys for system-specific parameters and functions
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTextEdit,
                            QProgressBar) # Importing necessary PyQt5 widgets
from PyQt5.QtCore import Qt, QTimer # Importing Qt for Qt-specific features
from openai import OpenAI # Importing OpenAI for API interaction
from dotenv import load_dotenv # Importing load_dotenv for loading environment variables
import os # Importing os for operating system dependent functionality
import tiktoken # Importing tiktoken for token counting

class OpenAIGUI(QMainWindow):
    def __init__(self):
        super().__init__() # Initializing the parent class
        self.setup_openai() # Setting up OpenAI API
        self.initUI() # Initializing the UI components
        
    def setup_openai(self):
        load_dotenv() # Loading environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY") # Loading the OpenAI API key from environment variables
        self.client = OpenAI(api_key=api_key) # Initializing OpenAI client with the API key
        # Initialize tokenizer for GPT-4
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def initUI(self): # Initializing the UI components
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
        self.prompt_text.textChanged.connect(self.update_counter)
        main_layout.addWidget(self.prompt_text)
        
        # Add counter label
        self.counter_label = QLabel('Characters: 0 | Tokens: 0')
        main_layout.addWidget(self.counter_label)

        # Add button
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.get_response)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Add loading indicator
        self.loading_indicator = QProgressBar()
        self.loading_indicator.setRange(0, 0)  # Makes it into an activity indicator
        self.loading_indicator.setVisible(False)  # Hide it initially
        self.loading_indicator.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 15px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 20px;
            }
        """)
        self.loading_text = QLabel("Waiting for response...")
        self.loading_text.setAlignment(Qt.AlignCenter)
        self.loading_text.setVisible(False)
        
        loading_layout = QVBoxLayout()
        loading_layout.addWidget(self.loading_text)
        loading_layout.addWidget(self.loading_indicator)
        main_layout.addLayout(loading_layout)

        # Add response area
        response_label = QLabel('Response:')
        main_layout.addWidget(response_label)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText('Response will appear here...')
        main_layout.addWidget(self.response_text)

        # Set central widget
        self.setCentralWidget(central_widget)
        
    def update_counter(self):
        """Update character and token count when text changes"""
        text = self.prompt_text.toPlainText()
        char_count = len(text)
        token_count = len(self.tokenizer.encode(text)) if text else 0
        self.counter_label.setText(f'Characters: {char_count} | Tokens: {token_count}')

    def show_loading(self, show=True):
        """Show or hide the loading indicator"""
        self.loading_indicator.setVisible(show)
        self.loading_text.setVisible(show)
        self.submit_button.setEnabled(not show)
        if show:
            self.response_text.setPlaceholderText("Generating response...")
        else:
            self.response_text.setPlaceholderText("Response will appear here...")
        QApplication.processEvents()  # Force UI update

    def get_response(self):
        prompt = self.prompt_text.toPlainText()
        if not prompt:
            self.response_text.setText("Please enter a prompt.")
            return
        
        # Show the loading indicator
        self.show_loading(True)
            
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
            # print(response)  # Also print to console for debugging
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.response_text.setText(error_message)
            print(error_message)
        finally:
            # Hide the loading indicator when done
            self.show_loading(False)

def main():
    app = QApplication(sys.argv) # Creating a QApplication instance
    gui = OpenAIGUI() # Creating an instance of OpenAIGUI
    gui.show() # Showing the GUI window
    sys.exit(app.exec_()) # Exiting the application when the window is closed

if __name__ == '__main__':
    main()