import os
import json
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Google Calendar API scope and calendar ID
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = '7da101809682e84581d3a2b0f5a41af81173315147c5482f01be71bbf0045c2e@group.calendar.google.com'  # Replace with your actual calendar ID

# Decode the base64-encoded credentials from environment variable
b64_creds = os.getenv("GOOGLE_CREDENTIALS_B64")
if not b64_creds:
    raise ValueError("GOOGLE_CREDENTIALS_B64 environment variable not found.")

creds_json = base64.b64decode(b64_creds).decode("utf-8")
creds_dict = json.loads(creds_json)

# Create credentials object
credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(start, end):
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return len(events.get('items', [])) == 0

def suggest_slots():
    now = datetime.utcnow()
    slots = []
    for i in range(1, 6):  # next 5 days
        start = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=i)
        end = start + timedelta(hours=1)
        if check_availability(start, end):
            slots.append((start, end))
    return slots

def create_booking(summary, start, end):
    event = {
        'summary': summary,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return "Booking confirmed."
