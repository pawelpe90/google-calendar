from calendar_handler import Calendar
from util.scrapper import league_scrapper
from datetime import datetime


def main():

    games = league_scrapper()
    c1 = Calendar()

    for game in games:
        info = game['info']
        date, sector = info.split(",")[0], info.split(",")[1][-1]
        day, time = date.split(" ")[0], date.split(" ")[-1]
        year, month, dom = int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])
        hour, mins = int(time.split(":")[0]), int(time.split(":")[1])

        start_time = datetime(year, month, dom, hour, mins, 0)

        c1.add_event(game['game'], "SP nr 205", f"Sektor: {sector}\nWynik: {game['sets']}\n{game['points']}", start_time)


main()
