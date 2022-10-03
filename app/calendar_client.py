from __future__ import print_function

import datetime
import os.path
from zlib import DEF_BUF_SIZE

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarClient:

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self) -> None:
        """Initializes the calendar client service object"""
        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', CalendarClient.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', CalendarClient.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('calendar', 'v3', credentials=creds)
        
        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_event():
        pass

    def list_events(self, max_results=10):
        
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print(f'Getting the upcoming {max_results} events')
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=max_results, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

    def create_event(self, event, dry_run=False) -> None:
        """Creates Google Calendar Event"""

        try:
            if dry_run:
                event = {
                    'summary': 'Google I/O 2023',
                    'location': '800 Howard St., San Francisco, CA 94103',
                    'description': 'A chance to hear more about Google\'s developer products.',
                    'start': {
                        'dateTime': '2020-05-28T09:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': '2020-05-28T17:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=2'
                    ],
                    'attendees': [
                        {'email': 'cs23andris@gmail.com'}
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }

            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print('An error occurred: %s' % error)