import os
import requests
import json

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

def fetch_working_deal():
    # Reliable & Direct E-commerce Deals Endpoint
    url = "https://dummyjson.com/products"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            products = res.json().get("products", [])
            if products:
                import random
                p = random.choice(products)
                
                title = p.get("title")
                price = f"${p.get('price')}"
                discount = f"{p.get('discountPercentage')}% OFF"
                
                # Raw Product Link -> EarnKaro Affiliate Route
                product_url = f"https://www.amazon.in/dp/{p.get('id')}"
                affiliate_link = f"https://earnkaro.com/connect?url={product_url}"
                
                return {
                    "title": title,
                    "price": price,
                    "discount": discount,
                    "link": affiliate_link
                }
    except Exception as e:
        print(f"Fetch Error: {e}")
    return None

def format_message(deal):
    return (
        f"🚨 **LIVE LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n"
        f"💰 Price: **{deal['price']}** ({deal['discount']})\n\n"
        f"🛒 **Grab Deal Here:** {deal['link']}\n\n"
        f"⚡ *Limited time offer! Fast Grab!* 🏃‍♂️"
    )

def post_to_telegram(caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_USERNAME,
        "text": caption,
        "parse_mode": "Markdown"
    }
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        print("✅ Message successfully delivered to Telegram!")
    else:
        print(f"❌ Telegram Error: {r.text}")

if __name__ == "__main__":
    deal = fetch_working_deal()
    if deal:
        msg = format_message(deal)
        post_to_telegram(msg)
    else:
        print("No deal data received.")
