import datetime

class Game:

    def __init__(self, home_team, away_team, venue, date, desc=None) -> None:
        self.home_team = home_team
        self.away_team = away_team
        self.venue = venue
        self.date = date
        self.desc = "Blsz II. 1.csoport"
        self.start_datetime = datetime.datetime.strptime(self.date, "%Y. %m. %d.  %H:%M")
        self.start_str = self.start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        self.end_datetime = self.start_datetime + datetime.timedelta(hours=2)
        self.end_str = self.end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        self.summary = f"{self.home_team} - {self.away_team}"

    def to_event(self):
        
        game_event = {
            'summary': self.summary,
            'description': self.desc,
            'location': self.venue,
            'start': {
                'dateTime': self.start_str,
                'timeZone': "Europe/Budapest"
            },
            'end': {
                'dateTime': self.end_str,
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