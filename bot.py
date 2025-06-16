import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# Replace with your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/YOUR_WEBHOOK_URL'

def fetch_boosted_info():
    try:
        # Send a GET request to the TibiaRoute website
        response = requests.get('https://tibiaroute.com')
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section containing the boosted information
        boosted_section = soup.find('section', {'id': 'boosted'})

        if boosted_section:
            # Extract the boosted boss and creature names
            boosted_boss = boosted_section.find('div', {'class': 'boss'}).get_text(strip=True)
            boosted_creature = boosted_section.find('div', {'class': 'creature'}).get_text(strip=True)

            return boosted_boss, boosted_creature
        else:
            print("Boosted information not found on the page.")
            return None, None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

def fetch_events():
    try:
        # Send a GET request to the TibiaRoute website
        response = requests.get('https://tibiaroute.com')
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section containing the events information
        events_section = soup.find('section', {'id': 'events'})

        if events_section:
            # Extract the events
            events = events_section.find_all('div', {'class': 'event'})
            event_list = [event.get_text(strip=True) for event in events]
            return event_list
        else:
            print("Events information not found on the page.")
            return []

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def send_to_discord(boss, creature, events):
    message = {
        'content': f"🚨 **Tibia Boosted Today** 🚨\n\n🧟 Boosted Creature: **{creature}**\n👹 Boosted Boss: **{boss}**\n\n🎉 **Today's Events:**\n" + "\n".join(events)
    }
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        response.raise_for_status()
        print("Notification sent to Discord.")
    except requests.RequestException as e:
        print(f"Error sending notification: {e}")

def job():
    print(f"Running job at {datetime.now()}")
    boosted_boss, boosted_creature = fetch_boosted_info()
    events = fetch_events()
    if boosted_boss and boosted_creature:
        send_to_discord(boosted_boss, boosted_creature, events)

# Schedule the job to run daily at 9:05 AM UTC
schedule.every().day.at("09:05").do(job)

if __name__ == "__main__":
    print("Bot is running...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for one minute
