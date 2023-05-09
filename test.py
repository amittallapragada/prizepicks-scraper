from prizepicks_scraper.prizepicks import PrizePicksScraper
from prizepicks_scraper.db import session
from prizepicks_scraper.models.prizepicks import PrizePicksProjection
scraper = PrizePicksScraper()
scraper.save_projections_to_db()


session.query(PrizePicksProjection).first()
