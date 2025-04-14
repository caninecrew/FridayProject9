# OpenAI GUI Interface

A PyQt5-based graphical user interface for interacting with OpenAI's API, developed for DS-3850-001 Friday Project 9.

## Project Overview

This application provides a simple and intuitive interface for sending prompts to OpenAI's language models and displaying the responses. It features a clean, user-friendly design that allows for easy interaction with sophisticated AI models.

## Features

- User-friendly graphical interface built with PyQt5
- Text input area for writing prompts
- Response display area for viewing AI-generated content
- Secure API key handling using environment variables
- Error handling for a smooth user experience

## Prerequisites

- Python 3.10 or higher
- PyQt5
- OpenAI Python library
- python-dotenv

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/caninecrew/FridayProject9.git
   cd FridayProject9
   ```

2. Install required dependencies:
   ```
   pip install PyQt5 openai python-dotenv
   ```

3. Create a `.env` file in the project root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```
python main.py
```

1. Enter your prompt in the text area
2. Click the "Submit" button to send the prompt to OpenAI
3. View the response in the output area

## Structure

- `main.py`: The main application file containing the GUI code and OpenAI API integration
- `.env`: Configuration file for storing the OpenAI API key
- `README.md`: Project documentation
- `project_instructions.md`: Original project requirements

## Troubleshooting

- **API Key Error**: If you receive an error about the API key, make sure your `.env` file is properly formatted and placed in the project root directory.
- **Module Not Found**: Ensure all required packages are installed using pip.
- **Connection Issues**: Check your internet connection and OpenAI API status.

## License

This project is part of the DS-3850-001 course assignment.

## Acknowledgments

- OpenAI for providing the API
- PyQt5 team for the GUI framework
