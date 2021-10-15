from calendar_handler import Calendar
from util.scrapper import league_scrapper
from datetime import datetime


def populate_calendar():

    games = league_scrapper()
    c1 = Calendar('57k1mpn9cft8sll6nlibspre7k@group.calendar.google.com')

    for game in games:
        info = game['info']
        date, sector = info.split(",")[0], info.split(",")[1][-1]
        day, time = date.split(" ")[0], date.split(" ")[-1]
        year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
        hour, mins = int(time.split(":")[0]), int(time.split(":")[1])

        start_time = datetime(year, month, dom, hour, mins, 0)
        update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

        c1.add_event(game['game'], "SP nr 205", f"Sektor: {sector}\nWynik: {game['sets']}\n{game['points']}\n\n"
                                                f"Ostatnia aktualizacja: {update_date}", start_time)


def update_calendar_events():

    games = league_scrapper()
    c1 = Calendar('57k1mpn9cft8sll6nlibspre7k@group.calendar.google.com')

    events = c1.list_events()

    for event in events['items']:
        for game in games:
            if event['summary'] == game['game']:
                info = game['info']
                date, sector = info.split(",")[0], info.split(",")[1][-1]
                day, time = date.split(" ")[0], date.split(" ")[-1]
                year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
                hour, mins = int(time.split(":")[0]), int(time.split(":")[1])

                start_time = datetime(year, month, dom, hour, mins, 0)
                update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

                c1.update_event_description(event['id'], f"Sektor: {sector}\nWynik: {game['sets']}\n{game['points']}\n"
                                                         f"\nOstatnia aktualizacja: {update_date}")

                c1.update_event_start_time(event['id'], start_time)


def list_events():
    c = Calendar('57k1mpn9cft8sll6nlibspre7k@group.calendar.google.com')
    c.list_events()


# list_events()
update_calendar_events()
