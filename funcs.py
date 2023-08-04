from bs4 import BeautifulSoup
import requests
import re
import os

city_dict = {
    'chicago': 'il--chicago',
    # 'philadelphia': 'pa--philadelphia',
}

def clean_string(input_string):
    cleaned_string = re.sub(r'[ /]', '_', input_string).lower()
    return cleaned_string

def make_api_call(event_id):
    base_url = f"https://www.eventbriteapi.com/v3/events/{event_id}"
    headers = {"Authorization": f"Bearer {os.getenv('EVENTBRITE_API_KEY')}"}
    response = requests.get(base_url, headers=headers)
    data = response.json()
    return data

def make_event_txt(driver, event):
    event_name = event.find('h2', class_='Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd').text
    cleaned_event_name = clean_string(event_name)
    event_link = event.find('a', class_='event-card-link')['href']
    event_id = event.find('a', class_='event-card-link')['data-event-id']
    driver.get(event_link)
    driver.implicitly_wait(10)
    event_soup = BeautifulSoup(driver.page_source, 'html.parser')
    event_description = str(event_soup.find('div', class_='eds-text--left').text)
    with open(f'./events/{str(event_id)}.html', 'w') as f:
        f.write(f'Event Name: {event_name}\n')
        f.write(f'Event Link: {event_link}\n')
        f.write(f'Event ID: {event_id}\n')
        f.write(f'Event Description: {event_description}')