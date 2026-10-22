import os
import requests
import random

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

def fetch_deal():
    url = "https://dummyjson.com/products"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            products = res.json().get("products", [])
            if products:
                p = random.choice(products)
                title = p.get("title")
                price = f"${p.get('price')}"
                discount = f"{p.get('discountPercentage')}% OFF"
                image_url = p.get("thumbnail") # Product ki live image
                
                # Raw Product Link -> EarnKaro Affiliate Route
                product_url = f"https://www.amazon.in/dp/{p.get('id')}"
                affiliate_link = f"https://earnkaro.com/connect?url={product_url}"
                
                return {
                    "title": title,
                    "price": price,
                    "discount": discount,
                    "image": image_url,
                    "link": affiliate_link
                }
    except Exception as e:
        print(f"Error fetching deal: {e}")
    return None

def post_to_telegram(deal):
    # sendPhoto API ka use karenge image aur button ke liye
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    caption = (
        f"🚨 **LIVE LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n"
        f"💰 Price: **{deal['price']}** ({deal['discount']})\n\n"
        f"⚡ *Limited time offer! Grab fast!* 🏃‍♂️"
    )
    
    # Inline Clickable Button Markup
    reply_markup = {
        "inline_keyboard": [
            [{"text": "🛒 Buy Now @ Best Price", "url": deal['link']}]
        ]
    }
    
    payload = {
        "chat_id": CHANNEL_USERNAME,
        "photo": deal['image'],
        "caption": caption,
        "parse_mode": "Markdown",
        "reply_markup": reply_markup
    }
    
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        print("✅ Photo deal with inline button successfully posted!")
    else:
        print(f"❌ Telegram Error: {r.text}")

if __name__ == "__main__":
    deal = fetch_deal()
    if deal:
        post_to_telegram(deal)
    else:
        print("No deal found.")
