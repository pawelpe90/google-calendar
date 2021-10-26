from googleapiclient.discovery import build
from util.methods import get_credentials
import os
import pickle


class CalendarCreator:
    def __init__(self):
        if not os.path.exists('token.pkl'):
            get_credentials()
        self.credentials = pickle.load(open('token.pkl', 'rb'))
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def add_new_calendar(self, summary, time_zone='Poland'):
        calendar = {
            'summary': summary,
            'timeZone': time_zone
        }

        self.service.calendars().insert(body=calendar).execute()
