import os
import time

from datetime import datetime, timedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event, Reminder
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
HOME_TEAM_NAME = os.getenv("TEAM_NAME")


@dataclass
class Game:
    """Class for representing a game"""

    home_team: str
    away_team: str
    venue: str
    date: str
    division: str

    @property
    def summary(self):
        """
        Get the summary of the game.

        Returns:
            str: The summary of the game in the format "{home_team} - {away_team}".
        """
        return f"{self.home_team} - {self.away_team}"

    @property
    def start_datetime(self):
        """
        Get the start datetime of the game.

        Returns:
            datetime: The start datetime of the game.
        """
        return datetime.strptime(self.date, "%Y. %m. %d.  %H:%M")

    @property
    def end_datetime(self):
        """
        Get the end datetime of the game.

        Returns:
            datetime: The end datetime of the game, which is 2 hours after the start datetime.
        """
        return self.start_datetime + timedelta(hours=2)

    @property
    def arrival_datetime_str(self):
        """
        Get the arrival datetime for players as a string.

        Returns:
            str: The arrival datetime for players in the format "%H:%M".
        """
        return (self.start_datetime + timedelta(minutes=-75)).strftime("%H:%M")

    @property
    def steward_datetime_str(self):
        """
        Get the arrival datetime for stewards as a string.

        Returns:
            str: The arrival datetime for stewards in the format "%H:%M".
        """
        return (self.start_datetime + timedelta(minutes=-45)).strftime("%H:%M")

    @property
    def is_home_game(self):
        """
        Check if the game is a home game.

        Returns:
            bool: True if the game is a home game, False otherwise.
        """
        return self.home_team == HOME_TEAM_NAME

    @property
    def description(self):
        """
        Get the description of the game.

        Returns:
            str: The description of the game.
        """
        if self.is_home_game:
            return f"""{self.division} bajnoki mérkőzés 
                \nÉrkezés játékosoknak: {self.arrival_datetime_str}\nÉrkezés rendezőknek: {self.steward_datetime_str}
                \nTALÁLKOZÓ A MEGBESZÉLT IDŐBEN A MEGBESZÉLT HELYEN!
                """
        else:
            return f"""{self.division} bajnoki mérkőzés 
            \nÉrkezés játékosoknak: {self.arrival_datetime_str}
            \nTALÁLKOZÓ A MEGBESZÉLT IDŐBEN A MEGBESZÉLT HELYEN!"""

    def to_gc_event(self, attendees: list[str]) -> Event:
        """
        Convert the Game object to a Google Calendar event.

        Args:
            attendees (list[str]): A list of attendees for the event.

        Returns:
            Event: The Google Calendar event representing the game.
        """
        game_event_data = {
            "summary": self.summary,
            "description": self.description,
            "location": self.venue,
            "start": self.start_datetime,
            "end": self.end_datetime,
            "attendees": attendees,
            # for some reason reminders are not working for invitees
            "default_reminders": False,
            "reminders": Reminder("email", 60 * 48),
            "minutes_before_popup_reminder": 60 * 24,
            "extendedProperties": {"public": {"scraper_automatic_event": "yes"}},
        }

        gc_event = Event(**game_event_data)
        print(gc_event)

        return gc_event

    # def from_event(google_calendar_event: Event):
    #     summary = google_calendar_event.summary
    #     event_id = google_calendar_event.id
    #     location = google_calendar_event.location
    #     start = google_calendar_event.start
    #     end = google_calendar_event.end
