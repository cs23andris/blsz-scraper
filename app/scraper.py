from bs4 import BeautifulSoup
import requests
import re
import datetime
from game import Game
from gcsa.event import Event

class BlszScraper:

    def __init__(self, team_schedule_url, division, attendees) -> None:
        self.team_schedule_url = team_schedule_url
        self.division = division
        self.attendees = attendees

    def get_soup_from_url(self, url: str) -> object:  
        """Returns BeautifulSoup object from url or static html"""

        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')

        return soup

    def get_schedule_table(self) -> list:
        a_team_schedule_soup = self.get_soup_from_url(self.team_schedule_url)

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

        #game = Game(*data)

        return data

    def create_game_list(self, schedule_table, max_results=100):
            
        list_of_games = []
        for fixture in schedule_table[:max_results]:
            game = self.get_match_data(fixture)
            list_of_games.append(game)

        return list_of_games

    def prepare_game_event(self, game_dict) -> Event:

        summary = f"{game_dict.get('home_team')} - {game_dict.get('away_team')}"
        start_datetime = datetime.datetime.strptime(game_dict.get("date"), "%Y. %m. %d.  %H:%M")
        start_str = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        end_datetime = start_datetime + datetime.timedelta(hours=2)
        end_str = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        loc = game_dict.get("venue")
        
        arrival_datetime_str = (start_datetime + datetime.timedelta(minutes=-75)).strftime("%H:%M")
        steward_datetime_str = (start_datetime + datetime.timedelta(minutes=-45)).strftime("%H:%M")
        
        if game_dict.get('home_team') == "XII. KERÜLET SVÁBHEGY FC":
            description = f"""{self.division} bajnoki mérkőzés 
            \nÉrkezés játékosoknak: {arrival_datetime_str}\nÉrkezés rendezőknek: {steward_datetime_str}
            \nTALÁLKOZÓ A MEGBESZÉLT IDŐBEN A MEGBESZÉLT HELYEN!
            """
        else:
            description = f"""{self.division} bajnoki mérkőzés 
            \nÉrkezés játékosoknak: {arrival_datetime_str}
            \nTALÁLKOZÓ A MEGBESZÉLT IDŐBEN A MEGBESZÉLT HELYEN!"""

        event_data = {
            'summary': summary,
            'description': description,
            'location': loc,
            'start': start_datetime,
            'end': end_datetime,
            'attendees': self.attendees,
            'default_reminders': True
            # 'minutes_before_popup_reminder': 60*24,
            # 'minutes_before_email_reminder': 60*48
            # 'start': {
            #     'dateTime': start_str,
            #     'timeZone': "Europe/Budapest"
            # },
            # 'end': {
            #     'dateTime': end_str,
            #     'timeZone': "Europe/Budapest"
            # }
            # ,
            # 'extendedProperties': {
            #     'public': {
            #         'scraper_automatic_event': "yes"
            #     }
            # }
        }

        #print(event_data)
        gc_event = Event(**event_data)
        #print(gc_event)

        return gc_event
    
    def prepare_all(self, year_filter: int) -> list:
        
        schedule_table = self.get_schedule_table()
        game_list = self.create_game_list(schedule_table)
        prepared_events = []
        for game in game_list:
            game_event = self.prepare_game_event(game)
            #print(game_event)
            if game_event.start.year == year_filter:
                prepared_events.append(game_event)
            
        return prepared_events
        

if __name__ == "__main__":
    print("Getting schedule table...")
    team_schedule_url = "https://adatbank.mlsz.hu/club/59/5/25606/2/249120.html"
    blsz_scraper = BlszScraper(team_schedule_url, "Blsz II. 1.csoport")
    # schedule_table = blsz_scraper.get_schedule_table()
    # game_list = blsz_scraper.create_game_list(schedule_table)
    print(blsz_scraper.prepare_all())
    

