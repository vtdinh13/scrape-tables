
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import argparse


def ingest_data(url:str) -> BeautifulSoup:

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    # Retrieve contents of webpage as a string
    html_source = driver.page_source

    # Pass the html_source to beautifulsoup
    soup = BeautifulSoup(html_source, 'html.parser')

    driver.quit()

    return soup


def parse_soup(soup:BeautifulSoup) -> pd.DataFrame:
    tables = soup.find_all('table')
    for i, table in enumerate(tables, start=0):
        rows=[]
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"]) 
            row = [cell.text.strip() for cell in cells]
            rows.append(row)
            df = pd.DataFrame(rows[1:], columns=rows[0])
            filename = f'table_{i}.csv'
            df.to_csv(filename, index=False)
 
        

def main(params):
    url = params.url
    soup = ingest_data(url)
    parse_soup(soup)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest and save table to csv')
    
    parser.add_argument('--url', help='url containing desired tables')    
    args = parser.parse_args()

    main(args)



