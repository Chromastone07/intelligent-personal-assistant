from src.data_ingestion.google_api import get_google_api_service

def main():
    print("Attempting to connect to Google APIs...")
    
    # Test Gmail connection
    gmail_service = get_google_api_service('gmail', 'v1')
    if gmail_service:
        print("Gmail connection successful!")
    else:
        print("Gmail connection failed.")

    print("-" * 20)

    # Test Calendar connection
    calendar_service = get_google_api_service('calendar', 'v3')
    if calendar_service:
        print("Calendar connection successful!")
    else:
        print("Calendar connection failed.")

if __name__ == '__main__':
    main()