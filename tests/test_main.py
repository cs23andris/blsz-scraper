import pytest

from unittest.mock import Mock
from gcsa.google_calendar import GoogleCalendar

from app.main import main
from app.game_event_processor import GameEventProcessor
from app.scraper import BlszScraper
from app.game import Game


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


@pytest.fixture
def make_event(make_game):
    return make_game.to_gc_event(["email1"])


def test_main_create_mode(monkeypatch, make_game):
    # Mock the command line arguments
    mock_args = Mock()
    mock_args.mode = "C"
    mock_args.dry_run = False
    mock_args.limit = 10
    monkeypatch.setattr("argparse.ArgumentParser.parse_args", lambda *args: mock_args)

    # Mock the config_parser function
    monkeypatch.setattr("app.main.config_parser", lambda: {})

    # Mock the get_config_by_team function
    monkeypatch.setattr(
        "app.main.get_config_by_team",
        lambda *args: {"url": "http://example.com", "attendees_test": ["email1"]},
    )

    # Mock the GoogleCalendar class
    mock_gc = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.main.GoogleCalendar", lambda *args, **kwargs: mock_gc)

    # Mock the GameEventProcessor class
    mock_gep = Mock(spec=GameEventProcessor)
    monkeypatch.setattr("app.main.GameEventProcessor", lambda *args: mock_gep)

    # Mock the BlszScraper class
    mock_blsz_scraper = Mock(spec=BlszScraper)
    monkeypatch.setattr("app.main.BlszScraper", lambda *args: mock_blsz_scraper)
    mock_blsz_scraper.fetch_games.return_value = [make_game]

    # Call the main function
    main()

    mock_blsz_scraper.fetch_games.assert_called_once_with(year_filter=2024)
    mock_gep.create_game_events.assert_called_once_with(
        [make_game], attendees=["email1"], dry_run=False
    )


def test_main_read_mode(monkeypatch, make_event):
    # Mock the command line arguments
    mock_args = Mock()
    mock_args.mode = "R"
    mock_args.dry_run = False
    mock_args.limit = 10
    monkeypatch.setattr("argparse.ArgumentParser.parse_args", lambda *args: mock_args)

    # Mock the config_parser function
    monkeypatch.setattr("app.main.config_parser", lambda: {})

    # Mock the get_config_by_team function
    monkeypatch.setattr(
        "app.main.get_config_by_team",
        lambda *args: {"url": "http://example.com", "attendees_test": ["email1"]},
    )

    # Mock the GoogleCalendar class
    mock_gc = Mock(spec=GoogleCalendar)
    monkeypatch.setattr("app.main.GoogleCalendar", lambda *args, **kwargs: mock_gc)

    # Mock the GameEventProcessor class
    mock_gep = Mock(spec=GameEventProcessor)
    monkeypatch.setattr("app.main.GameEventProcessor", lambda *args: mock_gep)
    mock_gep.get_game_events.return_value = [make_event]

    # Mock the BlszScraper class
    mock_blsz_scraper = Mock(spec=BlszScraper)
    monkeypatch.setattr("app.main.BlszScraper", lambda *args: mock_blsz_scraper)

    # Call the main function
    main()

    mock_blsz_scraper.fetch_games.assert_not_called()
    mock_gep.create_game_events.assert_not_called()
    mock_gep.get_game_events.assert_called_once_with(apply_date_filter=True)
