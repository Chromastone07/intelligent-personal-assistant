from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    creds = None
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def fetch_events(calendar_id='primary', time_min=None, time_max=None):
    service = get_calendar_service()
    
    if time_min is None:
        time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    if time_max is None:
        time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'  # Next 7 days

    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def parse_event(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    summary = event.get('summary', 'No Title')
    
    return {
        'summary': summary,
        'start': start,
        'end': end
    }

def get_upcoming_events():
    events = fetch_events()
    return [parse_event(event) for event in events]