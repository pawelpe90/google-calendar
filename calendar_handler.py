from googleapiclient.discovery import build
from util.methods import new_calendar_event, get_credentials
from datetime import timedelta
import os
import pickle
import logging


class CalendarHandler:
    def __init__(self, my_calendar_id):
        if not os.path.exists('token.pkl'):
            get_credentials()
        self.credentials = pickle.load(open('token.pkl', 'rb'))
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.my_calendar_id = my_calendar_id
        self.logger = logging.getLogger('run.calendar_handler')
        self.logger.info("Calendar initiated.")

    @staticmethod
    def printer(iterate):
        max_length = max([len(i['summary']) for i in iterate['items']])

        for i in iterate['items']:
            length = len(i['summary'])
            length_delta = max_length - length
            space = " " * length_delta

            print(f"Summary: {i['summary']} {space}| id: {i['id']} | start_time: {i['start']['dateTime']}")

    def display_all_calendars(self):
        result_calendars = self.service.calendarList().list().execute()
        for calendar in result_calendars['items']:
            print(calendar)
        return result_calendars

    def add_event(self, summary, location, description, start_time):
        self.logger.info(f"Adding event: {summary}")

        end_time = start_time + timedelta(minutes=90)
        event = new_calendar_event(summary, location, description, start_time, end_time)
        self.service.events().insert(calendarId=self.my_calendar_id, body=event).execute()

    def list_events(self):
        events = self.service.events().list(calendarId=self.my_calendar_id).execute()
        return events

    def print_events(self):
        events = self.service.events().list(calendarId=self.my_calendar_id).execute()
        self.printer(events)

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
        end_time = update + timedelta(minutes=90)
        event['start']['dateTime'] = update.strftime('%Y-%m-%dT%H:%M:%S')
        event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.service.events().update(calendarId=self.my_calendar_id, eventId=event['id'], body=event).execute()
