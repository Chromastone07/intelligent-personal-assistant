import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes for the APIs we want to access.
# If you modify these scopes, you must delete the token.json file.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

def get_google_api_service(api_name, api_version, client_secrets_file='credentials.json', token_file='token.json'):
    """
    A generic function to authenticate and create a Google API service object.

    Args:
        api_name (str): The name of the API (e.g., 'gmail' or 'calendar').
        api_version (str): The version of the API (e.g., 'v1' or 'v3').
        client_secrets_file (str): Path to the OAuth 2.0 client secrets file.
        token_file (str): Path to the stored token file.

    Returns:
        A Google API service object, or None if an error occurs.
    """
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                os.remove(token_file)
                return get_google_api_service(api_name, api_version, client_secrets_file, token_file)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(api_name, api_version, credentials=creds)
        print(f"Successfully connected to {api_name.capitalize()} API.")
        return service
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None