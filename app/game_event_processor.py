import os
import time

from datetime import datetime, timedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event, Reminder
from dataclasses import dataclass
from dotenv import load_dotenv

from app.game import Game

load_dotenv()
HOME_TEAM_NAME = os.getenv("TEAM_NAME")


class GameEventProcessor:
    """Class for processing game events in Google Calendar"""

    def __init__(self, gc_client: GoogleCalendar) -> None:
        """Initialize the GameEventProcessor object.

        :param gc_client: The GoogleCalendar client object.
        """
        self.gc_client = gc_client

    def create_game_events(
        self,
        games: list[Game],
        attendees: list[str],
        apply_date_filter: bool = True,
        dry_run: bool = False,
    ) -> None:
        """Creating game events in Google Calendar.

        :param games: Games to create events for.
        :param attendees: Attendees to invite to the events.
        :param apply_date_filter: Flag to apply date filter for the games, defaults to True
        :param dry_run: Dry run flag, only prints if set to True, defaults to False
        """

        for game in games:
            game_event = game.to_gc_event(attendees)

            tz = game_event.start.tzinfo
            compare_date = (
                datetime.now(tz)
                if apply_date_filter
                else datetime(year=2000, month=1, day=1, tzinfo=tz)
            )

            if game_event.start > compare_date:
                print(f"Creating event: {game_event} in dry_run mode: {dry_run}")
                if not dry_run:
                    time.sleep(20)
                    try:
                        self.gc_client.add_event(game_event, send_updates="none")
                    except Exception as e:
                        print(f"Error creating event: {e}")

    def delete_game_events(self, dry_run: bool = False) -> None:
        """Delete game events from Google Calendar.

        :param dry_run: Dry run flag, only prints if set to True, defaults to False
        """

        for game_event in self.gc_client.get_events(query="Svábhegy FC"):
            if game_event.start > datetime.now(game_event.start.tzinfo):
                print(f"Deleting event: {game_event} in dry_run mode: {dry_run}")
                if not dry_run:
                    self.gc_client.delete_event(game_event)

    def get_game_events(self, apply_date_filter: bool = False) -> list[Event]:
        """Gets game events from Google Calendar.

        :param apply_date_filter: Flag to apply date filter for the games, defaults to False
        :return: List of games from Google Calendar
        """

        games = self.gc_client.get_events(query="Svábhegy FC")
        if apply_date_filter:
            return [
                game for game in games if game.start > datetime.now(game.start.tzinfo)
            ]
        else:
            return games

    def update_game_events(self, games: list[Game], dry_run: bool = False) -> None:
        """Updates game events in Google Calendar.

        :param games: Games to update events for.
        :param dry_run: _description_, defaults to False
        """

        raise NotImplementedError("Update mode is not implemented yet.")
        # gc.update_event(e, send_updates="all")
