from bs4 import BeautifulSoup
import requests
import re
import datetime
from game import Game

class BlszScraper:

    def __init__(self, a_team_schedule_url, b_team_schedule_url=None) -> None:
        self.a_team_schedule_url = a_team_schedule_url
        if b_team_schedule_url:
            self.b_team_schedule_url = b_team_schedule_url

    def get_soup_from_url(self, url: str) -> object:  
        """Returns BeautifulSoup object from url or static html"""

        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')

        return soup

    def get_schedule_table(self) -> list:
        a_team_schedule_soup = self.get_soup_from_url(self.a_team_schedule_url)

        schedule_table = a_team_schedule_soup.findAll("div", attrs={"class":"schedule"})
        
        return schedule_table

    def get_match_data(self, fixture_div):
        data = {}

        home_team = fixture_div.find("div", attrs={"class":"home_team"}).get_text()
        away_team = fixture_div.find("div", attrs={"class":"away_team"}).get_text()
        date = fixture_div.find("div", attrs={"class":"team_sorsolas_date"}).get_text()
        venue = fixture_div.find("div", attrs={"class":"team_sorsolas_arena"}).get_text()

        data["home_team"] = home_team
        data["away_team"] = away_team
        data["date"] = date
        data["venue"] = venue

        game = Game(*data)

        return game

    def create_game_list(self, schedule_table, max_results=100):
            
        list_of_games = []
        for fixture in schedule_table[:max_results]:
            game = self.get_match_data(fixture)
            list_of_games.append(game)

        return list_of_games

    def prepare_game_event(self, game_dict):

        summary = f"{game_dict.get('home_team')} - {game_dict.get('away_team')}"
        start_datetime = datetime.datetime.strptime(game_dict.get("date"), "%Y. %m. %d.  %H:%M")
        start_str = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        end_datetime = start_datetime + datetime.timedelta(hours=2)
        end_str = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        loc = game_dict.get("venue")

        game_event = {
            'summary': summary,
            'description': 'Blsz II. 1.csoport',
            'location': loc,
            'start': {
                'dateTime': start_str,
                'timeZone': "Europe/Budapest"
            },
            'end': {
                'dateTime': end_str,
                'timeZone': "Europe/Budapest"
            },
            'extendedProperties': {
                'public': {
                    'scraper_automatic_event': "yes"
                }
            }
        }

        print(game_event)

        return game_event

if __name__ == "__main__":
    print("Getting schedule table...")
    a_team_schedule_url = "https://adatbank.mlsz.hu/club/59/5/25606/2/249120.html"
    blsz_scraper = BlszScraper(a_team_schedule_url)
    game_list = blsz_scraper.get_schedule_table()
    for game in game_list:
        game_event = blsz_scraper.prepare_game_event(game)

