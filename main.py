import sys # Importing sys for system-specific parameters and functions
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTextEdit,
                            QProgressBar, QComboBox, QColorDialog, QMenu,
                            QAction, QToolBar, QDialog, QListWidget, QListWidgetItem,
                            QInputDialog, QMessageBox) # Importing necessary PyQt5 widgets
from PyQt5.QtCore import Qt, QTimer, QSettings, QSize # Importing Qt for Qt-specific features
from PyQt5.QtGui import QIcon, QFont, QColor # Importing Qt GUI components
from openai import OpenAI # Importing OpenAI for API interaction
from openai import APIConnectionError, APITimeoutError, RateLimitError # Import specific OpenAI exceptions
from dotenv import load_dotenv # Importing load_dotenv for loading environment variables
import os # Importing os for operating system dependent functionality
import tiktoken # Importing tiktoken for token counting
import requests.exceptions # Import requests exceptions for network error handling
import json # Importing json for storing and loading settings

class ThemeManager:
    """Manages theme settings and provides theme presets"""
    
    def __init__(self):
        # Define default themes
        self.themes = {
            "Light": {
                "background": "#FFFFFF",
                "text": "#000000",
                "accent": "#3498db",
                "button_primary": "#2ecc71",
                "button_secondary": "#e74c3c",
                "input_background": "#F5F5F5"
            },
            "Dark": {
                "background": "#2C3E50",
                "text": "#ECEFF1",
                "accent": "#3498db",
                "button_primary": "#2ecc71",
                "button_secondary": "#e74c3c",
                "input_background": "#34495E"
            },
            "Solarized": {
                "background": "#002B36",
                "text": "#839496",
                "accent": "#268BD2",
                "button_primary": "#859900",
                "button_secondary": "#DC322F",
                "input_background": "#073642"
            },
            "Pastel": {
                "background": "#F9F9F9",
                "text": "#5D4037",
                "accent": "#81C784",
                "button_primary": "#81D4FA",
                "button_secondary": "#FFCC80",
                "input_background": "#FAFAFA"
            }
        }
        
        # Custom user theme
        self.custom_theme = {
            "background": "#FFFFFF",
            "text": "#000000",
            "accent": "#3498db",
            "button_primary": "#2ecc71",
            "button_secondary": "#e74c3c",
            "input_background": "#F5F5F5"
        }
    
    def get_theme(self, theme_name):
        """Get a theme by name"""
        if theme_name == "Custom":
            return self.custom_theme
        return self.themes.get(theme_name, self.themes["Light"])
    
    def set_custom_theme(self, theme_dict):
        """Set the custom theme"""
        self.custom_theme = theme_dict
        
    def get_theme_names(self):
        """Get list of available theme names"""
        return list(self.themes.keys()) + ["Custom"]


class PromptsManager:
    """Manages saved prompts"""
    
    def __init__(self):
        self.saved_prompts = []
    
    def add_prompt(self, name, content):
        """Add a new prompt"""
        self.saved_prompts.append({
            "name": name,
            "content": content
        })
    
    def remove_prompt(self, index):
        """Remove a prompt by index"""
        if 0 <= index < len(self.saved_prompts):
            del self.saved_prompts[index]
    
    def get_prompts(self):
        """Get all saved prompts"""
        return self.saved_prompts
    
    def get_prompt_names(self):
        """Get names of all saved prompts"""
        return [prompt["name"] for prompt in self.saved_prompts]


class SettingsManager:
    """Manages application settings using QSettings"""
    
    def __init__(self, organization, application):
        self.settings = QSettings(organization, application)
    
    def save_window_geometry(self, window):
        """Save window size and position"""
        self.settings.setValue("geometry", window.saveGeometry())
    
    def load_window_geometry(self, window):
        """Load window size and position"""
        geometry = self.settings.value("geometry")
        if geometry:
            window.restoreGeometry(geometry)
    
    def save_theme(self, theme_name):
        """Save current theme name"""
        self.settings.setValue("theme", theme_name)
    
    def get_theme(self):
        """Get saved theme name"""
        return self.settings.value("theme", "Light")
    
    def save_custom_theme(self, theme_dict):
        """Save custom theme settings"""
        self.settings.setValue("custom_theme", json.dumps(theme_dict))
    
    def get_custom_theme(self):
        """Get saved custom theme settings"""
        theme_json = self.settings.value("custom_theme", None)
        if theme_json:
            try:
                return json.loads(theme_json)
            except json.JSONDecodeError:
                return None
        return None
    
    def save_prompts(self, prompts):
        """Save list of prompts"""
        self.settings.setValue("saved_prompts", json.dumps(prompts))
    
    def get_prompts(self):
        """Get saved prompts"""
        prompts_json = self.settings.value("saved_prompts", None)
        if prompts_json:
            try:
                return json.loads(prompts_json)
            except json.JSONDecodeError:
                return []
        return []


class CustomThemeDialog(QDialog):
    """Dialog for customizing theme colors"""
    
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme.copy() if theme else {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Customize Theme")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Create color pickers for each theme element
        self.color_buttons = {}
        
        for name, color in self.theme.items():
            row_layout = QHBoxLayout()
            
            label = QLabel(name.replace("_", " ").title())
            color_button = QPushButton()
            color_button.setStyleSheet(f"background-color: {color}; min-width: 80px; min-height: 30px;")
            color_button.clicked.connect(lambda checked, n=name: self.choose_color(n))
            
            row_layout.addWidget(label)
            row_layout.addWidget(color_button)
            
            self.color_buttons[name] = color_button
            layout.addLayout(row_layout)
        
        # Add save button
        save_button = QPushButton("Save Theme")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
    
    def choose_color(self, name):
        """Open color dialog to choose a new color"""
        current_color = QColor(self.theme[name])
        color = QColorDialog.getColor(current_color, self)
        
        if color.isValid():
            hex_color = color.name()
            self.theme[name] = hex_color
            self.color_buttons[name].setStyleSheet(f"background-color: {hex_color}; min-width: 80px; min-height: 30px;")
    
    def get_theme(self):
        """Return the customized theme"""
        return self.theme


class SavedPromptsDialog(QDialog):
    """Dialog for managing saved prompts"""
    
    def __init__(self, parent=None, prompts_manager=None):
        super().__init__(parent)
        self.prompts_manager = prompts_manager
        self.selected_prompt = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Saved Prompts")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # List of saved prompts
        self.prompt_list = QListWidget()
        self.update_prompt_list()
        self.prompt_list.itemDoubleClicked.connect(self.use_prompt)
        layout.addWidget(self.prompt_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        use_button = QPushButton("Use Selected")
        use_button.clicked.connect(self.use_selected_prompt)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_prompt)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        
        button_layout.addWidget(use_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def update_prompt_list(self):
        """Update the list of saved prompts"""
        self.prompt_list.clear()
        for prompt in self.prompts_manager.get_prompts():
            item = QListWidgetItem(prompt["name"])
            item.setToolTip(prompt["content"])
            self.prompt_list.addItem(item)
    
    def use_prompt(self, item):
        """Use the selected prompt"""
        index = self.prompt_list.row(item)
        self.selected_prompt = self.prompts_manager.get_prompts()[index]["content"]
        self.accept()
    
    def use_selected_prompt(self):
        """Use the selected prompt from button click"""
        current_item = self.prompt_list.currentItem()
        if current_item:
            self.use_prompt(current_item)
    
    def delete_prompt(self):
        """Delete the selected prompt"""
        current_item = self.prompt_list.currentItem()
        if current_item:
            index = self.prompt_list.row(current_item)
            self.prompts_manager.remove_prompt(index)
            self.update_prompt_list()


class OpenAIGUI(QMainWindow):
    def __init__(self):
        super().__init__() # Initializing the parent class
        
        # Initialize managers
        self.theme_manager = ThemeManager()
        self.prompts_manager = PromptsManager()
        self.settings_manager = SettingsManager("FridayProject9", "OpenAIGUI")
        
        # Load saved settings
        self.load_settings()
        
        # Setup OpenAI and UI
        self.setup_openai() # Setting up OpenAI API
        self.initUI() # Initializing the UI components
        
        # Apply theme
        self.apply_theme(self.current_theme)
        
        # Restore window geometry
        self.settings_manager.load_window_geometry(self)
        
    def setup_openai(self):
        load_dotenv() # Loading environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY") # Loading the OpenAI API key from environment variables
        self.client = OpenAI(api_key=api_key) # Initializing OpenAI client with the API key
        # Initialize tokenizer for GPT-4
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        
    def load_settings(self):
        """Load user settings"""
        # Load theme settings
        self.current_theme = self.settings_manager.get_theme()
        custom_theme = self.settings_manager.get_custom_theme()
        if custom_theme:
            self.theme_manager.set_custom_theme(custom_theme)
        
        # Load saved prompts
        saved_prompts = self.settings_manager.get_prompts()
        if saved_prompts:
            self.prompts_manager.saved_prompts = saved_prompts
    
    def save_settings(self):
        """Save user settings"""
        # Save window geometry
        self.settings_manager.save_window_geometry(self)
        
        # Save theme settings
        self.settings_manager.save_theme(self.current_theme)
        if self.current_theme == "Custom":
            self.settings_manager.save_custom_theme(self.theme_manager.custom_theme)
        
        # Save prompts
        self.settings_manager.save_prompts(self.prompts_manager.get_prompts())

    def initUI(self): # Initializing the UI components
        # Set window properties
        self.setWindowTitle('OpenAI Interface')
        self.setGeometry(300, 300, 600, 400)

        # Create toolbar for settings
        self.create_toolbar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)

        # Add title label
        self.title_label = QLabel('OpenAI Interface')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 18px; font-weight: bold;')
        self.main_layout.addWidget(self.title_label)

        # Add input area
        self.prompt_label = QLabel('Enter your prompt:')
        self.main_layout.addWidget(self.prompt_label)

        # Add saved prompts selector
        prompt_selector_layout = QHBoxLayout()
        self.prompt_selector = QComboBox()
        self.update_prompt_selector()
        self.prompt_selector.currentIndexChanged.connect(self.load_saved_prompt)
        
        prompt_selector_layout.addWidget(QLabel("Saved Prompts:"))
        prompt_selector_layout.addWidget(self.prompt_selector, 1)
        
        # Add manage prompts button
        manage_prompts_button = QPushButton("Manage")
        manage_prompts_button.clicked.connect(self.open_saved_prompts)
        prompt_selector_layout.addWidget(manage_prompts_button)
        
        self.main_layout.addLayout(prompt_selector_layout)

        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText('Write your prompt here...')
        self.prompt_text.setMinimumHeight(100)
        self.prompt_text.textChanged.connect(self.update_counter)
        self.main_layout.addWidget(self.prompt_text)
        
        # Add counter label
        self.counter_label = QLabel('Characters: 0 | Tokens: 0')
        self.main_layout.addWidget(self.counter_label)

        # Add buttons
        button_layout = QHBoxLayout()
        
        # Save prompt button
        self.save_prompt_button = QPushButton('Save')
        self.save_prompt_button.clicked.connect(self.save_prompt)
        
        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.get_response)
        
        # Clear button
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_fields)
        
        button_layout.addWidget(self.save_prompt_button)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()
        self.main_layout.addLayout(button_layout)

        # Add loading indicator
        self.loading_indicator = QProgressBar()
        self.loading_indicator.setRange(0, 0)  # Makes it into an activity indicator
        self.loading_indicator.setVisible(False)  # Hide it initially
        
        self.loading_text = QLabel("Waiting for response...")
        self.loading_text.setAlignment(Qt.AlignCenter)
        self.loading_text.setVisible(False)
        
        loading_layout = QVBoxLayout()
        loading_layout.addWidget(self.loading_text)
        loading_layout.addWidget(self.loading_indicator)
        self.main_layout.addLayout(loading_layout)

        # Add response area
        self.response_label = QLabel('Response:')
        self.main_layout.addWidget(self.response_label)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText('Response will appear here...')
        self.main_layout.addWidget(self.response_text)

        # Set central widget
        self.setCentralWidget(central_widget)
    
    def create_toolbar(self):
        """Create toolbar with settings options"""
        self.toolbar = QToolBar("Settings")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        
        # Theme selector
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(self.theme_manager.get_theme_names())
        self.theme_selector.setCurrentText(self.current_theme)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        
        self.toolbar.addWidget(QLabel("Theme: "))
        self.toolbar.addWidget(self.theme_selector)
        self.toolbar.addSeparator()
        
        # Customize theme action
        customize_action = QAction("Customize Theme", self)
        customize_action.triggered.connect(self.customize_theme)
        self.toolbar.addAction(customize_action)
    
    def change_theme(self, theme_name):
        """Change the current theme"""
        self.current_theme = theme_name
        self.apply_theme(theme_name)
    
    def customize_theme(self):
        """Open dialog to customize theme"""
        current_theme = self.theme_manager.get_theme(self.current_theme)
        dialog = CustomThemeDialog(self, current_theme)
        
        if dialog.exec_():
            custom_theme = dialog.get_theme()
            self.theme_manager.set_custom_theme(custom_theme)
            
            # Switch to custom theme
            self.theme_selector.setCurrentText("Custom")
            self.current_theme = "Custom"
            self.apply_theme("Custom")
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the UI"""
        theme = self.theme_manager.get_theme(theme_name)
        
        # Apply to window and central widget
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
            }}
            QLabel {{
                color: {theme['text']};
            }}
            QTextEdit {{
                background-color: {theme['input_background']};
                color: {theme['text']};
                border: 1px solid {theme['accent']};
                border-radius: 4px;
            }}
            QProgressBar {{
                border: 1px solid {theme['accent']};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {theme['accent']};
            }}
            QComboBox {{
                background-color: {theme['input_background']};
                color: {theme['text']};
                border: 1px solid {theme['accent']};
                border-radius: 4px;
                padding: 2px;
            }}
            QComboBox:hover {{
                border: 1px solid {theme['button_primary']};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left: 1px solid {theme['accent']};
            }}
        """)
        
        # Apply to buttons individually
        self.submit_button.setStyleSheet(f"background-color: {theme['button_primary']}; color: white; font-weight: bold;")
        self.clear_button.setStyleSheet(f"background-color: {theme['button_secondary']}; color: white;")
        self.save_prompt_button.setStyleSheet(f"background-color: {theme['accent']}; color: white;")
    
    def update_prompt_selector(self):
        """Update the saved prompts dropdown"""
        self.prompt_selector.clear()
        self.prompt_selector.addItem("-- Select a saved prompt --")
        self.prompt_selector.addItems([prompt["name"] for prompt in self.prompts_manager.get_prompts()])
    
    def load_saved_prompt(self, index):
        """Load a saved prompt into the prompt text field"""
        if index <= 0:  # Skip the "Select a prompt" item
            return
            
        # Adjust index to account for the placeholder item
        prompt_index = index - 1
        prompts = self.prompts_manager.get_prompts()
        
        if 0 <= prompt_index < len(prompts):
            self.prompt_text.setText(prompts[prompt_index]["content"])
    
    def save_prompt(self):
        """Save the current prompt"""
        prompt_text = self.prompt_text.toPlainText()
        if not prompt_text:
            QMessageBox.warning(self, "Empty Prompt", "Cannot save an empty prompt.")
            return
            
        name, ok = QInputDialog.getText(self, "Save Prompt", "Enter a name for this prompt:")
        
        if ok and name:
            self.prompts_manager.add_prompt(name, prompt_text)
            self.update_prompt_selector()
            self.prompt_selector.setCurrentText(name)
            QMessageBox.information(self, "Prompt Saved", f"Prompt '{name}' has been saved.")
    
    def open_saved_prompts(self):
        """Open dialog to manage saved prompts"""
        dialog = SavedPromptsDialog(self, self.prompts_manager)
        
        if dialog.exec_():
            if dialog.selected_prompt:
                self.prompt_text.setText(dialog.selected_prompt)
            
            # Update the selector
            self.update_prompt_selector()
    
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
                ],
                timeout=30  # Set a reasonable timeout (30 seconds)
            )
            
            response = completion.choices[0].message.content
            self.response_text.setText(response)
            # print(response)  # Also print to console for debugging
            
        # Network-specific error handling
        except APIConnectionError as e:
            error_message = "Network Error: Could not connect to the OpenAI API. Please check your internet connection."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Connection error: {str(e)}")
            
        except APITimeoutError as e:
            error_message = "Timeout Error: The request to OpenAI API timed out. The server might be experiencing high traffic or your connection might be slow."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Timeout error: {str(e)}")
            
        except RateLimitError as e:
            error_message = "Rate Limit Error: You've exceeded the allowed number of API requests. Please try again later."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Rate limit error: {str(e)}")
            
        except requests.exceptions.ConnectionError as e:
            error_message = "Network Connection Error: Failed to establish a connection. Please check your internet connection."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Requests connection error: {str(e)}")
            
        except requests.exceptions.Timeout as e:
            error_message = "Network Timeout: The request timed out. Please check your internet connection speed or try again later."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Requests timeout error: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            error_message = "Network Request Error: There was an issue with the network request."
            self.response_text.setText(f"{error_message}\n\nDetails: {str(e)}")
            print(f"Requests error: {str(e)}")
            
        # Fallback general exception handler
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.response_text.setText(error_message)
            print(f"General error: {str(e)}")
            
        finally:
            # Hide the loading indicator when done
            self.show_loading(False)

    def clear_fields(self):
        """Clear both input and output fields"""
        # Reset the prompt text field
        self.prompt_text.clear()
        
        # Reset the response text field
        self.response_text.clear()
        self.response_text.setPlaceholderText('Response will appear here...')
        
        # Reset the counter
        self.counter_label.setText('Characters: 0 | Tokens: 0')
        
        # Set focus back to the input field for convenience
        self.prompt_text.setFocus()
        
    def closeEvent(self, event):
        """Save settings when closing the application"""
        self.save_settings()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv) # Creating a QApplication instance
    gui = OpenAIGUI() # Creating an instance of OpenAIGUI
    gui.show() # Showing the GUI window
    sys.exit(app.exec_()) # Exiting the application when the window is closed

if __name__ == '__main__':
    main()