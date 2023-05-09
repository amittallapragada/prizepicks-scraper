from prizepicks_scraper.utils import get_anonymous_driver, xpath_soup
from prizepicks_scraper.models.prizepicks import PrizePicksProjection
from prizepicks_scraper.db import session
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


class PrizePicksScraper():
    BASE_URL = "https://app.prizepicks.com/"
    DELAY = 2

    def __init__(self):
        self.driver = get_anonymous_driver()
        # get page
        self.get_base_website()

    def __remove_popups(driver):
        """
        closes the hero popup on first load.
        """
        try:
            popup_button = driver.find_element(
                By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button")
            if popup_button:
                popup_button.click()
                print("Popup Closed")
        except Exception as e:
            print("Unable to find popup")

    def __parse_projection(projection):
        player_div = projection.find("div", {"class": "player"})
        name_div = player_div.find("div", {"class": "name"})
        img_div = player_div.find("picture").find("img")
        score_div = projection.find("div", {"class": "projected-score"})
        line_div = score_div.find("div", {"class": "score"}).find(
            "span").find("div", "presale-score")
        type_div = score_div.find("div", {"class": "text"})
        return PrizePicksProjection(name=name_div.text.upper(), img=img_div["src"], line=line_div.text, bet_type=type_div.text.upper())

    def __get_current_page_projections(content):
        soup = BeautifulSoup(content, 'html.parser')
        projections = soup.find_all("div", {"class": "projection"})
        output = []
        for projection in projections:
            output.append(PrizePicksScraper.__parse_projection(projection))
        return output

    def __serialize_projections(projections):
        serialized_projections = [projection.as_dict()
                                  for projection in projections]
        return serialized_projections

    def get_base_website(self):
        self.driver.get(self.BASE_URL)
        print(f"Waiting {self.DELAY} seconds.")
        WebDriverWait(self.driver, self.DELAY)
        time.sleep(self.DELAY)
        PrizePicksScraper.__remove_popups(self.driver)

    def scrape_nba_projections(self, serialize_output=True):
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        stat_type_nav = soup.find_all("div", {"class": "stat"})
        output = PrizePicksScraper.__get_current_page_projections(content)
        for stat in stat_type_nav:
            try:
                print(f"Scraping {stat.text}")
                stat_obj = self.driver.find_element(By.XPATH, xpath_soup(stat))
                stat_obj.click()
                WebDriverWait(self.driver, 2)
                content = self.driver.page_source
                output.extend(
                    PrizePicksScraper.__get_current_page_projections(content))
            except Exception as e:
                print(f"Stat: {stat.text} errored: {e}")
        if serialize_output:
            return PrizePicksScraper.__serialize_projections(output)
        return output

    def save_projections_to_db(self):
        projections = self.scrape_nba_projections(serialize_output=False)
        for projection in projections:
            session.add(projection)
        session.commit()
