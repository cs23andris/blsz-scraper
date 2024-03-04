import requests
import datetime

from bs4 import BeautifulSoup, ResultSet, Tag
from gcsa.event import Event

from app.game import Game


class BlszScraper:
    """Class for scraping the fixture schedule of a team from the MLSZ Adatbank website"""

    def __init__(self, team_schedule_url: str) -> None:
        """Initializes the BlszScraper object

        :param team_schedule_url: The URL from where the fixture schedule can be scraped
        """
        self.team_schedule_url = team_schedule_url
        self.soup = self.get_soup_from_url(self.team_schedule_url)
        self.division = self.get_division()

    def get_soup_from_url(self, url: str) -> BeautifulSoup:
        """Returns BeautifulSoup object from url or static html"""

        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def get_schedule_table(self) -> ResultSet[Tag]:
        """Returns the schedule table from the team schedule page as a ResultSet of Tag objects"""

        schedule_table = self.soup.findAll("div", attrs={"class": "schedule"})
        return schedule_table

    def get_division(self) -> str:
        """Gets division from the team schedule page"""

        return self.soup.select_one(".team_tabella .container_title").get_text().strip()

    def get_match_data(self, fixture_div: Tag) -> Game:
        """From a fixture div, returns a dictionary with the match data"""

        home_team = fixture_div.find("div", attrs={"class": "home_team"}).get_text()
        away_team = fixture_div.find("div", attrs={"class": "away_team"}).get_text()
        date = fixture_div.find("div", attrs={"class": "team_sorsolas_date"}).get_text()
        venue = fixture_div.find(
            "div", attrs={"class": "team_sorsolas_arena"}
        ).get_text()

        return Game(home_team, away_team, venue, date, self.division)

    def get_game_list(
        self, schedule_table: ResultSet[Tag], max_results: int = 100
    ) -> list[Game]:
        """Creates a list of Game objects from the schedule table

        :param schedule_table: The schedule table tag from the team schedule page
        :param max_results: Max results count, defaults to 100
        :return: A list of Game objects
        """

        list_of_games = []
        for fixture in schedule_table[:max_results]:
            game = self.get_match_data(fixture)
            list_of_games.append(game)

        return list_of_games

    def fetch_games(
        self, year_filter: int = None, max_results: int = 100
    ) -> list[Game]:
        """Fetches the game list from the team schedule page

        :param max_results: Max results count, defaults to 100
        :return: A list of Game objects
        """

        schedule_table = self.get_schedule_table()
        game_list = self.get_game_list(schedule_table, max_results)
        result = []
        for game in game_list:
            if (
                year_filter is not None and game.start_datetime.year == year_filter
            ) or year_filter is None:
                result.append(game)

        return result


if __name__ == "__main__":
    pass
    print("Getting schedule table...")
    team_schedule_url = "https://adatbank.mlsz.hu/club/59/5/25606/2/249120.html"
    blsz_scraper = BlszScraper(team_schedule_url, "Blsz II. 1.csoport")
    # schedule_table = blsz_scraper.get_schedule_table()
    # game_list = blsz_scraper.create_game_list(schedule_table)
    print(blsz_scraper.prepare_all())
