import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

def fetch_live_deal():
    try:
        # Desidime Public JSON Deals API
        url = "https://www.desidime.com/api/v1/deals.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Deals list extract karna
            deals = data.get("deals", [])
            if deals and len(deals) > 0:
                deal = deals[0] # Sabse latest deal
                title = deal.get("title", "Live Loot Offer")
                raw_link = deal.get("share_url", "https://desidime.com")
                
                # EarnKaro Affiliate Link mein convert karna
                affiliate_link = f"https://earnkaro.com/connect?url={raw_link}"
                
                return {
                    "title": title,
                    "link": affiliate_link
                }
    except Exception as e:
        print(f"Error fetching JSON feed: {e}")
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
    else:
        print(f"❌ Failed to post: {response.text}")

if __name__ == "__main__":
    deal = fetch_live_deal()
    if deal:
        msg = format_message(deal)
        post_to_telegram(msg)
    else:
        print("No deal fetched.")
