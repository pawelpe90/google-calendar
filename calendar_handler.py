from googleapiclient.discovery import build
from util.methods import new_calendar_event, get_credentials
from datetime import timedelta
import os
import pickle


class Calendar:
    def __init__(self, my_calendar_id):
        if not os.path.exists('token.pkl'):
            get_credentials()
        self.credentials = pickle.load(open('token.pkl', 'rb'))
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.my_calendar_id = my_calendar_id

    @staticmethod
    def printer(iterate):
        max_length = 0

        for i in iterate['items']:
            length = len(i['summary'])
            if length > max_length:
                max_length = length

        for i in iterate['items']:
            length = len(i['summary'])
            length_delta = max_length - length
            space = " " * length_delta

            print(f"Summary: {i['summary']} {space}| id: {i['id']} | start_time: {i['start']['dateTime']}")

    def display_all_calendars(self):
        result_calendar = self.service.calendarList().list().execute()
        self.printer(result_calendar)
        return result_calendar

    def add_event(self, summary, location, description, start_time):
        end_time = start_time + timedelta(minutes=90)
        event = new_calendar_event(summary, location, description, start_time, end_time)
        self.service.events().insert(calendarId=self.my_calendar_id, body=event).execute()

    def list_events(self):
        events = self.service.events().list(calendarId=self.my_calendar_id).execute()
        self.printer(events)
        return events

    def update_event_summary(self, event_id, update):
        event = self.service.events().get(calendarId=self.my_calendar_id, eventId=event_id).execute()
        event['summary'] = update
        self.service.events().update(calendarId=self.my_calendar_id, eventId=event['id'], body=event).execute()

    def update_event_description(self, event_id, update):
        event = self.service.events().get(calendarId=self.my_calendar_id, eventId=event_id).execute()
        event['description'] = update
        self.service.events().update(calendarId=self.my_calendar_id, eventId=event['id'], body=event).execute()

    def update_event_location(self, event_id, update):
        event = self.service.events().get(calendarId=self.my_calendar_id, eventId=event_id).execute()
        event['location'] = update
        self.service.events().update(calendarId=self.my_calendar_id, eventId=event['id'], body=event).execute()

    def update_event_start_time(self, event_id, update):
        event = self.service.events().get(calendarId=self.my_calendar_id, eventId=event_id).execute()
        event['start']['dateTime'] = update.strftime('%Y-%m-%dT%H:%M:%S')
        self.service.events().update(calendarId=self.my_calendar_id, eventId=event['id'], body=event).execute()
