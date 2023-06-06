# NBA PrizePicks Odds Scraper
## Run the PrizePicks Scraper

1. upgrade chrome to version (113.0.5672.63) to use the existing selenium chrome driver or download another chromedriver that matches your chrome browser's versions.
2. create a venv `python3 -m venv venv` and activate it `source venv/bin/activate`
3. run `pip3 install -r requirements.txt`
4. create a file called `env_variables.py` and get its contents from an author to connect to prod db.
5. test by running the test_prizepicks.py file. `python3 test_prizepicks.py`. this will autopopulate a sqlite db on your machine with todays prizepicks bets.
