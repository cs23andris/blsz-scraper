from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import Jan, Apr


calendar = GoogleCalendar('cs23andris@gmail.com', credentials_path = "/Users/andrascsillag/Documents/Repos/blsz-scraper/.credentials/credentials.json")

blsz_events = calendar.get_events(query='Blsz II. 1.csoport')

for event in blsz_events:
    print(type(event))
    print(event)


