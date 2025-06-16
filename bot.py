import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# ✅ Your Discord webhook
WEBHOOK_URL = 'https://discord.com/api/webhooks/1384231438987038782/qmljoAKv6ZpJWr4_KdxxPwz2bAssq0APa0lC00U0Ch8EzPqbHqhD8NOLU9Ba7JEkpaw2'

def fetch_boosted_info():
    try:
        response = requests.get('https://tibiaroute.com')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        boosted_section = soup.find('section', {'id': 'boosted'})
        if not boosted_section:
            return None, None

        boss_div = boosted_section.find('div', class_='boss')
        creature_div = boosted_section.find('div', class_='creature')

        boosted_boss = boss_div.get_text(strip=True) if boss_div else "Unknown"
        boosted_creature = creature_div.get_text(strip=True) if creature_div else "Unknown"

        return boosted_boss, boosted_creature

    except Exception as e:
        print(f"[ERROR] Boosted info fetch failed: {e}")
        return None, None

def fetch_events():
    try:
        response = requests.get('https://tibiaroute.com')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        events_section = soup.find('section', {'id': 'events'})

        if not events_section:
            return []

        events = events_section.find_all('div', class_='event')
        event_texts = [event.get_text(strip=True) for event in events]
        return event_texts

    except Exception as e:
        print(f"[ERROR] Events fetch failed: {e}")
        return []

def send_to_discord(boss, creature, events):
    events_text = "\n".join([f"- {e}" for e in events]) if events else "No events listed."
    message = {
        "content": f"🚨 **Tibia Daily Info** 🚨\n\n"
                   f"🧟 **Boosted Creature:** {creature}\n"
                   f"👹 **Boosted Boss:** {boss}\n\n"
                   f"🎉 **Events Today:**\n{events_text}"
    }

    try:
        response = requests.post(WEBHOOK_URL, json=message)
        response.raise_for_status()
        print("[INFO] Message sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send message to Discord: {e}")

def job():
    print(f"[INFO] Running job at {datetime.utcnow().isoformat()} UTC")
    boss, creature = fetch_boosted_info()
    events = fetch_events()
    if boss and creature:
        send_to_discord(boss, creature, events)
    else:
        print("[WARN] Boosted info incomplete. Skipping message.")

# ⏰ Schedule the job daily at 9:05 AM UTC
schedule.every().day.at("09:05").do(job)

if __name__ == "__main__":
    print("[INFO] Bot started. Waiting for schedule...")
    while True:
        schedule.run_pending()
        time.sleep(60)
