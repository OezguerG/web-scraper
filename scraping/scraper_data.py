import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BoxOfficeScraper:
    def __init__(self, max_movies):
        self.max_movies = max_movies

    def scrape_budget_genre_from_webpaths(self, webpaths):
        budgets = []
        # Chat-GPT 16-17
        with open(webpaths, encoding='utf-8') as f:
            movies = json.load(f)

        # Chat-GPT 20 (opens browser controlled by selenium)
        driver = webdriver.Chrome()
        try:
            for movie in movies[:self.max_movies]:
                rank = movie["Rank"]
                title = movie["Title"]
                url = movie["Url"]
                # Chat-GPT 27 (navigates to url in the browser)
                driver.get(url)

                try:
                    # Chat-GPT 29 - 36 (waits for element to appear)
                    budget_span = WebDriverWait(driver, 1).until(
                        # (expects condition, waits for element given to appear in DOM, \
                        # using XPATH cause we cant access via ID)
                        EC.presence_of_element_located((By.XPATH, "//span[text()='Budget']/following-sibling::span"))
                    )
                    budget = budget_span.text
                except:
                    budget = "N/A"
                    
                try:
                    genre_span = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//span[text()='Genres']/following-sibling::span"))
                    )
                    genre = genre_span.text    
                except:
                    genre = "N/A"
                    

                print(f"Rank: {rank}, Titel: {title}, Budget: {budget}, Genre: {genre}")
                budgets.append({"Rank": rank, "Title": title, "Budget": budget, "Genre": genre})
              
        finally:
            driver.quit()
        
        return pd.DataFrame(budgets)
    
    
        
    def scrape_grossings_as_df(self):
        max = int(self.max_movies/3)
        url = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/"
        df1 = pd.read_html(url, header=0)[0][:max]
        url2 = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset=200" 
        df2 = pd.read_html(url2, header=0)[0][:max]
        url3 = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset=400" 
        df3 = pd.read_html(url3, header=0)[0][:max]
        combined_df = pd.concat([df1, df2, df3], ignore_index=True)
        return combined_df
            