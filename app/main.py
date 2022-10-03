from bs4 import BeautifulSoup
from scraper import BlszScraper
from calendar_client import CalendarClient

if __name__ == "__main__":
    cc = CalendarClient()
    #cc.list_events()

    a_team_schedule_url = "https://adatbank.mlsz.hu/club/59/5/25606/2/249120.html"
    blsz_scraper = BlszScraper(a_team_schedule_url)

    game_list = blsz_scraper.get_schedule_table()

    for game in game_list:
        game_event = blsz_scraper.prepare_game_event(game)
        cc.create_event(game_event)
