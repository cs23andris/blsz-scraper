# blsz-scraper
Scraping adatbank.mlsz.hu fixture schedule and creating google calendar events from game times


# Common errors
If you see google calendar authentication related errors when running the application, a common solution is to delete the token pickle file from the .credentials folder and re-run the application which will force you to allow permissions to the application again and generates a new pickle file.
Apply year filter on main.py line 49 to avoid scraping all the years.

# How to run

`python app/main.py --mode C --limit 3 --dry_run`

Arguments:
- `--mode` : C for create, D for delete
- `--limit` : limit the number of events to be created or deleted
- `--dry_run` : if set, no changes will be made to the calendar, only the events will be printed to the console