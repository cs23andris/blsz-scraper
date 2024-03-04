import pytest
from bs4 import BeautifulSoup, Tag, ResultSet
from unittest.mock import Mock

from app.scraper import BlszScraper
from app.game import Game


@pytest.fixture
def mock_soup():
    with open("tests/data/test_adatbank.html") as f:
        mock_html_content = f.read()

    mock_soup = BeautifulSoup(mock_html_content, "html.parser")
    return mock_soup


@pytest.fixture
def mock_table(monkeypatch, mock_soup):

    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_soup_from_url", lambda self, _: mock_soup
    )

    scraper = BlszScraper("dummy_url")
    return scraper.get_schedule_table()


@pytest.fixture
def mock_tag(mock_table):

    return mock_table[0]


def test_get_soup_from_url(monkeypatch):
    # Mock requests.get to return a response with the contents of your test_adatbank.html file
    with open("tests/data/test_adatbank.html") as f:
        mock_html_content = f.read()

    mock_response = Mock()
    mock_response.content = mock_html_content.encode()
    monkeypatch.setattr("requests.get", lambda _: mock_response)

    scraper = BlszScraper("dummy_url")
    soup = scraper.get_soup_from_url("dummy_url")

    assert isinstance(soup, BeautifulSoup)


def test_get_schedule_table(monkeypatch: pytest.MonkeyPatch, mock_soup):
    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_soup_from_url", lambda self, _: mock_soup
    )

    scraper = BlszScraper("dummy_url")
    schedule_table = scraper.get_schedule_table()

    assert isinstance(schedule_table, ResultSet)
    assert (
        str(schedule_table[0])
        == """<div class="schedule" rel="1848131">
<div class="home_team"><a href="https://adatbank.mlsz.hu/club/61/5/27291/1/268004.html" title="XII. KERÜLET SVÁBHEGY FC"><span>XII. KERÜLET SVÁBHEGY FC</span></a></div>
<div class="home_logo"><a href="https://adatbank.mlsz.hu/club/61/5/27291/1/268004.html" title="XII. KERÜLET SVÁBHEGY FC"><img src="https://adatbank.mlsz.hu/img/EgyesuletLogo/Logo/14/13698.png" width="20"/></a></div>
<div class="result-cont"><a href="https://adatbank.mlsz.hu/match/61/5/27291/1/1848131.html"><div class="result"><span class="schedule-points">1 - 3</span></div></a></div>
<div class="away_logo"><a href="https://adatbank.mlsz.hu/club/61/5/27291/1/267989.html" title="1908 SZAC BUDAPEST"><img src="https://adatbank.mlsz.hu/img/EgyesuletLogo/Logo/14/13690.png" width="20"/></a></div>
<div class="away_team"><a href="https://adatbank.mlsz.hu/club/61/5/27291/1/267989.html" title="1908 SZAC BUDAPEST"><span>1908 SZAC BUDAPEST</span></a></div>
<div class="team_sorsolas_date"><a href="https://adatbank.mlsz.hu/match/61/5/27291/1/1848131.html">2023. 08. 18. <span> 20:00</span></a></div>
<div class="team_sorsolas_arena"><a href="https://adatbank.mlsz.hu/match/61/5/27291/1/1848131.html">BVSC Utánpótlás Labdarúgó Centrum</a></div>
</div>"""
    )


def test_get_match_data(monkeypatch, mock_tag):

    scraper = BlszScraper("dummy_url")
    match_data = scraper.get_match_data(mock_tag)

    expected_data = Game(
        **{
            "home_team": "XII. KERÜLET SVÁBHEGY FC",
            "away_team": "1908 SZAC BUDAPEST",
            "date": "2023. 08. 18.  20:00",
            "venue": "BVSC Utánpótlás Labdarúgó Centrum",
            "division": "BLSZ I. osztály",
        }
    )

    assert match_data == expected_data


def test_create_game_list(monkeypatch, mock_soup):
    # Mock get_match_data to return a dummy game
    mock_game = {
        "home_team": "dummy_home_team",
        "away_team": "dummy_away_team",
        "date": "dummy_date",
        "venue": "dummy_venue",
        "division": "dummy_division",
    }
    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_match_data", lambda self, _: mock_game
    )

    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_soup_from_url", lambda self, _: mock_soup
    )

    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_division", lambda self: "dummy_division"
    )

    scraper = BlszScraper("dummy_url")

    # Create a dummy schedule_table with 5 fixtures
    schedule_table = ["fixture1", "fixture2", "fixture3", "fixture4", "fixture5"]

    list_of_games = scraper.get_game_list(schedule_table)

    # Check that the list of games has the correct length
    assert len(list_of_games) == 5

    # Check that each game in the list is the same as the mock game
    for game in list_of_games:
        assert game == mock_game


def test_get_division(monkeypatch, mock_soup):
    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_soup_from_url", lambda self, _: mock_soup
    )

    scraper = BlszScraper("dummy_url")
    division = scraper.get_division()

    assert division == "BLSZ I. osztály"


def test_fetch_games(monkeypatch, mock_soup):
    monkeypatch.setattr(
        "app.scraper.BlszScraper.get_soup_from_url", lambda self, _: mock_soup
    )

    scraper = BlszScraper("dummy_url")
    games = scraper.fetch_games()

    assert len(games) == 30
    assert games[0] == Game(
        **{
            "home_team": "XII. KERÜLET SVÁBHEGY FC",
            "away_team": "1908 SZAC BUDAPEST",
            "date": "2023. 08. 18.  20:00",
            "venue": "BVSC Utánpótlás Labdarúgó Centrum",
            "division": "BLSZ I. osztály",
        }
    )

    games_filtered = scraper.fetch_games(year_filter=2024)

    assert len(games_filtered) == 15
    assert games_filtered[1] == Game(
        **{
            "home_team": "TFSE-11TEAMSPORTS",
            "away_team": "XII. KERÜLET SVÁBHEGY FC",
            "date": "2024. 02. 23.  19:30",
            "venue": "Dr. Koltai Jenő Sportközpont",
            "division": "BLSZ I. osztály",
        }
    )
