import os
import requests
import xml.etree.ElementTree as ET

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

# Live Indian Deals Feed (Real Offers)
FEED_URL = "https://www.desidime.com/deals.xml"

def fetch_live_deal():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(FEED_URL, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Live latest item pick karna
            item = root.find(".//item")
            
            if item is not None:
                title = item.find("title").text if item.find("title") is not None else "Live Loot Offer"
                link = item.find("link").text if item.find("link") is not None else "https://amazon.in"
                
                # Link ko EarnKaro Affiliate Link mein convert karna
                affiliate_link = f"https://earnkaro.com/connect?url={link}"
                
                return {
                    "title": title,
                    "link": affiliate_link
                }
    except Exception as e:
        print(f"Error fetching live feed: {e}")
    return None

def format_message(deal):
    return (
        f"🚨 **LIVE LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n\n"
        f"🛒 **Grab Offer Here:** {deal['link']}\n\n"
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
        print("✅ Live deal successfully posted on Telegram!")
        
if __name__ == "__main__":
    deal = fetch_live_deal()
    if deal:
        msg = format_message(deal)
        post_to_telegram(msg)
