import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

# Live Deal Scraper Function
def fetch_live_deals():
    try:
        # Example: Real-time public deals feed URL
        url = "https://www.desidime.com/deals"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Scraping live deal elements
        deal_card = soup.find("div", class_="deal-detail")
        if deal_card:
            title = deal_card.find("a").text.strip()
            raw_link = "https://www.desidime.com" + deal_card.find("a")["href"]
            
            # Link ko EarnKaro ke affiliate link format me route karna
            affiliate_link = f"https://earnkaro.com/connect?url={raw_link}"
            
            return {
                "title": title,
                "link": affiliate_link
            }
    except Exception as e:
        print(f"Error fetching live deals: {e}")
    
    return None

def format_live_message(deal):
    return (
        f"🚨 **LIVE LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n\n"
        f"🛒 **Grab Live Offer Here:** {deal['link']}\n\n"
        f"⚡ *Limited time deal! Hurry up!* 🏃‍♂️"
    )

def post_to_telegram(caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_USERNAME,
        "text": caption,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Live deal posted successfully!")
    else:
        print(f"❌ Failed to post: {response.text}")

if __name__ == "__main__":
    live_deal = fetch_live_deals()
    if live_deal:
        msg = format_live_message(live_deal)
        post_to_telegram(msg)
    else:
        print("No new live deal found at this moment.")
