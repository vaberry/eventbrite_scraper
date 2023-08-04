from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
import funcs as funcs
load_dotenv()

driver = webdriver.Chrome()
for city, city_code in funcs.city_dict.items():
    for i in range(1, 2):
        try:
            driver.get(f"https://www.eventbrite.com/d/{city_code}/all-events/?page={i}")
            driver.implicitly_wait(10)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            events_list = soup.find_all('li', class_='search-main-content__events-list-item')
            for event in events_list:
                funcs.make_event_txt(driver, event)
        except Exception as e:
            print(e)
            break
driver.quit()