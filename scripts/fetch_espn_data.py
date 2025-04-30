# fetch_espn_data.py
# Scrape rendered ESPN F1 results using Selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, '..', 'data', 'raw')
os.makedirs(data_path, exist_ok=True)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

url = 'https://www.espn.com/f1/results'
driver.get(url)
time.sleep(5)

blocks = driver.find_elements(By.CLASS_NAME, 'ResponsiveTable')
race_tables = []

for block in blocks:
    try:
        title_el = block.find_element(By.XPATH, './preceding-sibling::h2[1]')
        race_title = title_el.text.strip()
        rows = block.find_elements(By.TAG_NAME, 'tr')
        headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, 'th')]
        all_rows = []
        for row in rows[1:]:
            cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, 'td')]
            if len(cols) == len(headers):
                all_rows.append(cols)

        df = pd.DataFrame(all_rows, columns=headers)
        df.insert(0, 'Race', race_title)
        race_tables.append(df)
    except Exception as e:
        continue

driver.quit()

if race_tables:
    full = pd.concat(race_tables, ignore_index=True)
    out_path = os.path.join(data_path, 'espn_2024_results.csv')
    full.to_csv(out_path, index=False)
    print(f"Saved scraped results to {out_path}")
else:
    print("No race data found on ESPN page.")
