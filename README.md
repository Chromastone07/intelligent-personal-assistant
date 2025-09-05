# Intelligent Productivity Assistant

This project is designed to enhance productivity by integrating various Google services such as Gmail and Google Calendar. It provides a user-friendly interface built with Streamlit, allowing users to manage their tasks and emails efficiently.

## Project Structure

```
intelligent-productivity-assistant
├── .env                  # For storing secret API keys and configurations
├── .gitignore            # To exclude sensitive files and caches from Git
├── README.md             # Project description, setup, and run instructions
├── app.py                # The main entry point for our Streamlit application
├── requirements.txt      # List of all Python packages needed for the project
├── credentials.json      # Downloaded from Google Cloud for OAuth
├── token.json            # Generated after user authorization (DO NOT COMMIT)
└── src/
    ├── __init__.py
    ├── data_ingestion/
    │   ├── __init__.py
    │   ├── google_api.py
    │   ├── gmail_reader.py
    │   ├── calendar_reader.py
    │   └── document_parser.py
    ├── processing/
    │   ├── __init__.py
    │   ├── nlp_tasks.py
    │   └── priority_engine.py
    └── utils/
        ├── __init__.py
        └── helpers.py
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/intelligent-productivity-assistant.git
   cd intelligent-productivity-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud credentials:
   - Download `credentials.json` from your Google Cloud project and place it in the root directory.

5. Create a `.env` file to store your API keys and configurations.

## Run Instructions

To start the Streamlit application, run the following command:
```
streamlit run app.py
```

Follow the on-screen instructions to authenticate with your Google account and start using the application.