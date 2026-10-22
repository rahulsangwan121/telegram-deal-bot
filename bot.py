import os
import requests
import xml.etree.ElementTree as ET
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

def fetch_live_deal():
    try:
        url = "https://www.desidime.com/deals.xml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # verify=False SSL verification check bypass karta hai
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            # Clean invalid characters to avoid XML parsing errors
            clean_xml = response.text.encode('utf-8', 'ignore').decode('utf-8')
            root = ET.fromstring(clean_xml)
            
            # Find all items
            items = root.findall(".//item")
            if items:
                # Get the first deal item
                item = items[0]
                title = item.find("title").text if item.find("title") is not None else "Live Loot Offer"
                raw_link = item.find("link").text if item.find("link") is not None else "https://www.desidime.com"
                
                # Convert to EarnKaro affiliate routing link
                affiliate_link = f"https://earnkaro.com/connect?url={raw_link}"
                
                return {
                    "title": title.strip(),
                    "link": affiliate_link
                }
    except Exception as e:
        print(f"Error fetching feed: {e}")
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
    response = requests.post(url, json=payload, verify=False, timeout=10)
    if response.status_code == 200:
        print("✅ Live deal successfully posted on Telegram!")
        return True
    else:
        print(f"❌ Failed to post to Telegram: {response.text}")
        return False

if __name__ == "__main__":
    deal = fetch_live_deal()
    if deal:
        msg = format_message(deal)
        post_to_telegram(msg)
    else:
        print("No deal fetched.")
