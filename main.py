from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta


def get_credentials():
    # run it only once
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))


def new_calendar_event(summary, location, description, start_time, end_time):
    timezone = 'Poland'

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': timezone,
        },
        # 'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        # ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event


def main():
    # get_credentials()

    credentials = pickle.load(open('token.pkl', 'rb'))
    service = build('calendar', 'v3', credentials=credentials)

    # display all calendars connected to the account
    result_calendar = service.calendarList().list().execute()
    my_calendar = result_calendar['items'][0]['id']

    # display all events in a calendar
    # result_events = service.events().list(calendarId=my_calendar).execute()

    # insert new event
    start_time = datetime(2021, 5, 30, 6, 0, 0)
    end_time = start_time + timedelta(days=4)

    event = new_calendar_event('Summary here', 'Location here', 'Description here', start_time, end_time)
    service.events().insert(calendarId=my_calendar, body=event).execute()

    # for r in result_events['items']:
    #     print(r['summary'])


main()
