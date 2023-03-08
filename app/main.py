import os
from bs4 import BeautifulSoup
from scraper import BlszScraper
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from utils import config_parser, get_config_by_team

if __name__ == "__main__":
    
    config = config_parser()
    a_team_config = get_config_by_team(config, "Svábhegy FC")
    #print(a_team_config)
    base_path = os.path.dirname(os.path.abspath(__file__)).removesuffix("/app")
    credentials_path = os.path.join(base_path, ".credentials", "credentials.json")
    
    gc = GoogleCalendar('andras.csillag.tech@gmail.com', credentials_path=credentials_path)

    blsz_scraper = BlszScraper(team_schedule_url=a_team_config["url"], division=a_team_config["division"], attendees=a_team_config["attendees_prod"])
    prepared_events = blsz_scraper.prepare_all(year_filter=2023)
    # print(prepared_events)
    for i, game_event in enumerate(prepared_events):
        # print(game_event)
        gc.add_event(game_event, send_updates="all")
        
    # [gc.delete_event(e) for e in gc.get_events(query="Svábhegy FC")]
    
    print([e for e in gc.get_events(query="Svábhegy FC")])
    
    # for e in gc.get_events(query="Svábhegy FC"):
        
        # e.attendees.append(e._ensure_attendee_from_email("andras.csillag@datapao.com"))
        # gc.update_event(e, send_updates="all")
        # break