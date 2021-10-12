from googleapiclient.discovery import build
from util.methods import new_calendar_event, get_credentials
from datetime import timedelta
import os
import pickle


class Calendar:
    def __init__(self):
        if not os.path.exists('token.pkl'):
            get_credentials()
        self.credentials = pickle.load(open('token.pkl', 'rb'))
        self.service = build('calendar', 'v3', credentials=self.credentials)

    @staticmethod
    def printer(iterate):
        for i in iterate['items']:
            print(i['summary'], i['id'])

    def display_all_calendars(self):
        result_calendar = self.service.calendarList().list().execute()
        self.printer(result_calendar)
        return result_calendar

    def add_event(self, summary, location, description, start_time):

        my_calendar = '57k1mpn9cft8sll6nlibspre7k@group.calendar.google.com'
        end_time = start_time + timedelta(minutes=90)

        event = new_calendar_event(summary, location, description, start_time, end_time)
        self.service.events().insert(calendarId=my_calendar, body=event).execute()
