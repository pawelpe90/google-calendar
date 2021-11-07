import logging
import os
from datetime import datetime
from argparse import ArgumentParser

from lals_games_handler import CalendarRunner

# ---- Parse arguments ---- #

parser = ArgumentParser()
parser.add_argument("--calendar-id", "-cid")
parser.add_argument("--team-name", "-tn")
args = parser.parse_args()

# ---- Arguments into variables ---- #

calendar_id = args.calendar_id
team_name = args.team_name

# ---- Set up logging handlers ---- #

log_file_location = r"C:\logs\google_calendar"
t = str(datetime.now()).replace("-", "_").replace(":", "_").replace(" ", "_")[:19]

mylogs = logging.getLogger('run')
mylogs.setLevel(logging.DEBUG)
data_format = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S %Z")

file = logging.FileHandler(os.path.join(log_file_location, f"{calendar_id}_{t}.log"), "a")
file.setLevel(logging.INFO)
file.setFormatter(data_format)

stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(data_format)

mylogs.addHandler(file)
mylogs.addHandler(stream)

# ---- Main runner ---- #


def main():
    mylogs.info("Google calendar populator is running...")
    mylogs.info("-----------------------------------------")
    mylogs.info("# Running with parameters:")
    mylogs.info(f"# Calendar id: {calendar_id}")
    if team_name is not "":
        mylogs.info(f"# Team name: {team_name}")
    mylogs.info("-----------------------------------------")

    calendar = CalendarRunner(calendar_id)
    calendar.update_calendar_events(team_name)

    mylogs.info("Calendar population is FINISHED.")


if __name__ == '__main__':
    main()
