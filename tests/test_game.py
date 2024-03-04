import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from app.game import Game

HOME_TEAM_NAME = "Team1"


def test_summary():
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.summary == "Team1 - Team2"


def test_start_datetime():
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.start_datetime == datetime(2022, 1, 1, 12, 0)


def test_end_datetime():
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.end_datetime == datetime(2022, 1, 1, 14, 0)


def test_arrival_datetime_str():
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.arrival_datetime_str == "10:45"


def test_steward_datetime_str():
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.steward_datetime_str == "11:15"


def test_is_home_game(monkeypatch):

    monkeypatch.setattr("app.game.HOME_TEAM_NAME", "Mock Home Team")
    game = Game(
        home_team="Mock Home Team",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    assert game.is_home_game == True


def test_description(monkeypatch):

    monkeypatch.setattr("app.game.HOME_TEAM_NAME", "Team1")
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )
    print(game.description)

    expected_description = """Division bajnoki mérkőzés 
                
Érkezés játékosoknak: 10:45
Érkezés rendezőknek: 11:15
                
TALÁLKOZÓ A MEGBESZÉLT IDŐBEN A MEGBESZÉLT HELYEN!"""
    assert game.description.rstrip() == expected_description


def test_to_gc_event(monkeypatch):
    # Mock the Event class
    mock_event = Mock()
    mock_reminder = Mock()
    monkeypatch.setattr("app.game.Event", mock_event)
    monkeypatch.setattr("app.game.Reminder", mock_reminder)

    # Create a Game object
    game = Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )

    # Call the method
    attendees = ["attendee1@example.com", "attendee2@example.com"]
    result = game.to_gc_event(attendees)

    # Assert that the Event class was called with the correct arguments
    expected_event_data = {
        "summary": game.summary,
        "description": game.description,
        "location": game.venue,
        "start": game.start_datetime,
        "end": game.end_datetime,
        "attendees": attendees,
        "default_reminders": False,
        "reminders": mock_reminder("email", 60 * 48),
        "minutes_before_popup_reminder": 60 * 24,
        "extendedProperties": {"public": {"scraper_automatic_event": "yes"}},
    }
    mock_event.assert_called_once_with(**expected_event_data)

    # Assert that the method returned the correct result
    assert result == mock_event.return_value
