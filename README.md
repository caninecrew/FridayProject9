# OpenAI GUI Interface

A PyQt5-based graphical user interface for interacting with OpenAI's API, developed for DS-3850-001 Friday Project 9.

## Project Overview

This application provides a simple and intuitive interface for sending prompts to OpenAI's language models and displaying the responses. It features a clean, user-friendly design that allows for easy interaction with sophisticated AI models.

## Features

- User-friendly graphical interface built with PyQt5
- Text input area for writing prompts
- Response display area for viewing AI-generated content
- Character and token counting for input management
- Clear button to reset input and output fields
- Loading indicator while waiting for API responses
- Comprehensive network error handling with user-friendly messages
- Secure API key handling using environment variables
- Color-coded action buttons for intuitive interaction

## Prerequisites

- Python 3.10 or higher
- PyQt5
- OpenAI Python library
- python-dotenv
- tiktoken (for token counting)
- requests (for network operations)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/caninecrew/FridayProject9.git
   cd FridayProject9
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   (You can use the provided `.env.example` file as a template)

## Usage

Run the application:
```
python main.py
```

1. Enter your prompt in the text area (note the character and token count)
2. Click the "Submit" button (green) to send the prompt to OpenAI
3. Watch the loading indicator while waiting for the response
4. View the response in the output area
5. Use the "Clear" button (red) to reset both input and output fields

## Structure

- `main.py`: The main application file containing the GUI code and OpenAI API integration
- `.env`: Configuration file for storing the OpenAI API key
- `.env.example`: Template for creating your own `.env` file
- `requirements.txt`: List of project dependencies
- `README.md`: Project documentation
- `project_instructions.md`: Original project requirements

## Troubleshooting

- **API Key Error**: If you receive an error about the API key, make sure your `.env` file is properly formatted and placed in the project root directory.
- **Module Not Found**: Ensure all required packages are installed using pip.
- **Network Errors**: The application provides specific error messages for network issues. Follow the suggestions in the error message to resolve connectivity problems.
- **Token Limit Exceeded**: If your prompt is too long, check the token counter to ensure you're within the model's limits.

## License

This project is part of the DS-3850-001 course assignment.

## Acknowledgments

- OpenAI for providing the API
- PyQt5 team for the GUI framework
- tiktoken library for accurate token counting
