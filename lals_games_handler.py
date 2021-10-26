from calendar_handler import CalendarHandler
from util.lals_scrapper import league_scrapper
from datetime import datetime


class CalendarRunner:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id

    def populate_calendar_events(self, team_name):
        games = league_scrapper(team_name)
        c = CalendarHandler(self.calendar_id)

        for game in games:
            info = game['info'].replace(".", ":")
            if len(info) == 32:
                date, sector = info.split(",")[0], info.split(",")[1][-1]
                day, time = date.split(" ")[0], date.split(" ")[-1]
                year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
                hour, mins = int(time.split(":")[0]), int(time.split(":")[1])
                start_time = datetime(year, month, dom, hour, mins, 0)
                update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                c.add_event(game['game'], "SP nr 205", f"Sektor: {sector}\nWynik: {game['sets']}\n{game['points']}\n\n"
                                                       f"Ostatnia aktualizacja: {update_date}", start_time)
            else:
                sector = "-"
                start_time = datetime(2022, 3, 12, 00, 00, 0)
                update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

                c.add_event(game['game'], "SP nr 205", f"Sektor: {sector}\nWynik: {game['sets']}\n{game['points']}\n\n"
                                                       f"Ostatnia aktualizacja: {update_date}", start_time)

    def update_calendar_events(self, team_name):
        games = league_scrapper(team_name)
        c1 = CalendarHandler(self.calendar_id)

        events = c1.list_events()

        for event in events['items']:
            for game in games:
                if event['summary'] == game['game']:
                    info = game['info'].replace(".", ":")
                    points = game['points']
                    if len(info) == 32 and len(points) > 0:
                        status = "ROZEGRANY"
                        date, sector = info.split(",")[0], info.split(",")[1][-1]
                        day, time = date.split(" ")[0], date.split(" ")[-1]
                        year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
                        hour, mins = int(time.split(":")[0]), int(time.split(":")[1])

                        start_time = datetime(year, month, dom, hour, mins, 0)
                        update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

                        c1.update_event_description(event['id'], f"Status: {status}\n\n"
                                                                 f"Sektor: {sector}\n"
                                                                 f"Wynik: {game['sets']}\n{game['points']}\n\n"
                                                                 f"Ostatnia aktualizacja: {update_date}")

                        c1.update_event_start_time(event['id'], start_time)

                    elif len(info) == 32 and len(points) == 0:
                        status = "NADCHODZĄCY"
                        date, sector = info.split(",")[0], info.split(",")[1][-1]
                        day, time = date.split(" ")[0], date.split(" ")[-1]
                        year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
                        hour, mins = int(time.split(":")[0]), int(time.split(":")[1])

                        start_time = datetime(year, month, dom, hour, mins, 0)
                        update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

                        c1.update_event_description(event['id'], f"Status: {status}\n\n"
                                                                 f"Sektor: {sector}\n"
                                                                 f"Wynik: {game['sets']}\n{game['points']}\n\n"
                                                                 f"Ostatnia aktualizacja: {update_date}")

                        c1.update_event_start_time(event['id'], start_time)

                    else:
                        status = "PRZEŁOŻONY"
                        sector = "-"
                        start_time = datetime(2022, 3, 12, 00, 00, 0)
                        update_date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

                        c1.update_event_description(event['id'],
                                                    f"Status: {status}\n\n"
                                                    f"Sektor: {sector}\n"
                                                    f"Wynik: {game['sets']}\n{game['points']}\n\n"
                                                    f"Ostatnia aktualizacja: {update_date}")

                        c1.update_event_start_time(event['id'], start_time)

    def list_calendar_events(self):
        c = CalendarHandler(self.calendar_id)
        c.list_events()

    def print_calendar_events(self):
        c = CalendarHandler(self.calendar_id)
        c.print_events()
