import pytest

from unittest.mock import Mock, patch
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from app.game import Game
from app.game_event_processor import GameEventProcessor
import datetime


@pytest.fixture
def make_game():
    # Make a Game object
    return Game(
        home_team="Team1",
        away_team="Team2",
        venue="Venue",
        date="2022. 01. 01.  12:00",
        division="Division",
    )


def test_create_game_events(monkeypatch):
    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)

    # Mock the Game objects
    mock_game = Mock(spec=Game)
    mock_game.to_gc_event.return_value.start = datetime.datetime.now()

    # Call the method
    gep.create_game_events([mock_game], ["attendee1@example.com"], dry_run=True)

    # Assert that add_event was not called because it's a dry run
    mock_gc_client.add_event.assert_not_called()


def test_create_game_events_with_date_filter_false(monkeypatch, make_game):

    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)
    game = make_game

    # Call the method
    attendees = ["attendee1@example.com", "attendee2@example.com"]
    game_event = game.to_gc_event(attendees)

    # Call the method
    gep.create_game_events([game], attendees, apply_date_filter=False, dry_run=False)

    # Assert that add_event called because apply_date_filter is False
    mock_gc_client.add_event.assert_called_once_with(game_event, send_updates="none")


def test_create_game_events_with_date_filter_true(monkeypatch, make_game):

    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)
    game = make_game

    # Call the method
    attendees = ["attendee1@example.com", "attendee2@example.com"]
    game_event = game.to_gc_event(attendees)
    # Call the method
    gep.create_game_events([game], attendees, apply_date_filter=True, dry_run=False)

    # Assert that add_event called because apply_date_filter is True
    mock_gc_client.add_event.assert_not_called()


def test_delete_game_events_dry_run(monkeypatch):
    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)

    # Mock the Event objects
    mock_event = Mock(spec=Event)
    mock_event.start = datetime.datetime.now()

    # Mock the get_events method
    mock_gc_client.get_events.return_value = [mock_event]

    # Call the method
    gep.delete_game_events(dry_run=True)

    # Assert that delete_event was not called because it's a dry run
    mock_gc_client.delete_event.assert_not_called()


@pytest.mark.skip(reason="Need freezegun to mock datetime.now")
def test_delete_game_events(monkeypatch):
    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    def mock_now():
        return datetime(2020, 1, 1)

    # # Replace datetime.now with the mock function
    # # monkeypatch.setattr(datetime, 'datetime.now', mock_now)
    monkeypatch.setattr("datetime.datetime.now", mock_now)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)

    # Mock the Event objects
    mock_event = Mock(spec=Event)
    mock_event.start = datetime.datetime.now()

    # Mock the get_events method
    mock_gc_client.get_events.return_value = [mock_event]

    # Call the method
    gep.delete_game_events(dry_run=False)

    # Assert that delete_event was not called because it's a dry run
    mock_gc_client.delete_event.assert_called_once_with(mock_event)


def test_get_game_events(monkeypatch):
    # Mock the GoogleCalendar client
    mock_gc_client = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.game_event_processor.GoogleCalendar", mock_gc_client)

    # Create a GameEventProcessor object
    gep = GameEventProcessor(mock_gc_client)

    # Mock the Event objects
    mock_event = Mock(spec=Event)
    mock_event.start = datetime.datetime.now()

    # Mock the get_events method
    mock_gc_client.get_events.return_value = [mock_event]

    # Call the method
    events = gep.get_game_events(apply_date_filter=False)

    # Assert that get_events was called and the returned events are correct
    mock_gc_client.get_events.assert_called_once_with(query="Svábhegy FC")
    assert events == [mock_event]
