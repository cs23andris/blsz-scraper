import pytest
from app import utils


def test_config_parser_with_path():
    expected_result = {
        "sender_mail": "andras.csillag.tech@gmail.com",
        "schedules": [
            {
                "team_name": "Svábhegy FC",
                "division": "Blsz II. 1.csoport",
                "url": "https://adatbank.mlsz.hu/club/61/5/27291/5/268004.html",
                "attendees_test": ["cs23andris@gmail.com", "anna.e.pomazi@gmail.com"],
                "attendees_prod": [
                    "cs23andris@gmail.com",
                    "anna.e.pomazi@gmail.com",
                    "andras.csillag@datapao.com",
                ],
            }
        ],
    }
    result = utils.config_parser("./tests/data/test_config.yaml")
    assert result == expected_result


def test_config_parser_without_path(monkeypatch):
    monkeypatch.setattr("os.path.join", lambda *args: "./tests/data/test_config.yaml")

    result = utils.config_parser()

    expected_result = {
        "sender_mail": "andras.csillag.tech@gmail.com",
        "schedules": [
            {
                "team_name": "Svábhegy FC",
                "division": "Blsz II. 1.csoport",
                "url": "https://adatbank.mlsz.hu/club/61/5/27291/5/268004.html",
                "attendees_test": ["cs23andris@gmail.com", "anna.e.pomazi@gmail.com"],
                "attendees_prod": [
                    "cs23andris@gmail.com",
                    "anna.e.pomazi@gmail.com",
                    "andras.csillag@datapao.com",
                ],
            }
        ],
    }

    assert result == expected_result


def test_get_config_by_team():
    parsed_config = {"schedules": [{"team_name": "team1"}, {"team_name": "team2"}]}
    result = utils.get_config_by_team(parsed_config, "team1")
    assert result == {"team_name": "team1"}


def test_get_credentials_path(monkeypatch):
    monkeypatch.setattr("os.path.abspath", lambda _: "/path/to/file/app")
    monkeypatch.setattr("os.path.dirname", lambda _: "/path/to/file")
    result = utils.get_credentials_path()
    assert result == "/path/to/file/.credentials/credentials.json"