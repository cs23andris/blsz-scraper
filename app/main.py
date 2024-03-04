import os
import argparse

from bs4 import BeautifulSoup
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime
from dotenv import load_dotenv

from app.utils import config_parser, get_config_by_team, get_credentials_path
from app.game_event_processor import GameEventProcessor
from app.scraper import BlszScraper

load_dotenv()
HOME_TEAM_NAME = os.getenv("TEAM_NAME")
SENDER_MAIL = os.getenv("SENDER_MAIL")


def main():
    parser = argparse.ArgumentParser(description="Blsz Adatbank Scraper CLI.")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["C", "R", "U", "D"],
        help="Mode of operation: C for create, R for read, U for update, D for delete events.",
    )

    parser.add_argument(
        "--limit", type=int, help="Limit the number of events to create"
    )
    parser.add_argument("--dry_run", action="store_true", help="Set the dry_run flag")

    args = parser.parse_args()
    run_mode = args.mode
    dry_run = args.dry_run
    limit = args.limit or 100
    print(f"Run mode: {run_mode}, Dry run: {dry_run}, Limit: {limit}")

    config = config_parser()
    a_team_config = get_config_by_team(config, HOME_TEAM_NAME)
    credentials_path = get_credentials_path()

    gc = GoogleCalendar(SENDER_MAIL, credentials_path=credentials_path)
    gep = GameEventProcessor(gc)
    blsz_scraper = BlszScraper(a_team_config["url"])

    if run_mode == "C":
        print("Creating events...")
        games = blsz_scraper.fetch_games(year_filter=2024)
        gep.create_game_events(
            games[:limit], attendees=a_team_config["attendees_test"], dry_run=dry_run
        )
    elif run_mode == "R":
        print("Reading events from the calendar...")
        created_game_events = gep.get_game_events(apply_date_filter=True)
        print(
            f"Found {len(created_game_events)} events in the calendar: {created_game_events}"
        )
    elif run_mode == "U":
        raise NotImplementedError("Update mode is not implemented yet.")
    elif run_mode == "D":
        raise NotImplementedError("Delete mode is not fully implemented yet.")
    else:
        raise ValueError("Invalid mode of operation.")


if __name__ == "__main__":

    main()
