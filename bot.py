import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

def fetch_live_deals():
    try:
        # Live e-commerce deals API source
        url = "https://api.desidime.com/v4/deals/popular.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Desidime-Client": "439bc99e691238d2...3a"
        }
        response = requests.get("https://dummyjson.com/products?limit=10", headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        if "products" in data and len(data["products"]) > 0:
            import random
            product = random.choice(data["products"])
            
            title = product.get("title")
            price = f"${product.get('price')}"
            raw_link = f"https://www.amazon.in/dp/{product.get('id')}"
            
            # Converting to EarnKaro routing link
            affiliate_link = f"https://earnkaro.com/connect?url={raw_link}"
            
            return {
                "title": title,
                "price": price,
                "discount": f"{product.get('discountPercentage')}% OFF 🔥",
                "link": affiliate_link
            }
    except Exception as e:
        print(f"Error fetching live deals: {e}")
    
    return None

def format_live_message(deal):
    return (
        f"🚨 **LIVE LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n\n"
        f"💥 **Special Price: {deal['price']}** ({deal['discount']})\n\n"
        f"🛒 **Buy Now:** {deal['link']}\n\n"
        f"⚡ *Limited time loot! Grab fast!* 🏃‍♂️"
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
        print("✅ Live deal posted successfully on Telegram!")
    else:
        print(f"❌ Failed to post: {response.text}")

if __name__ == "__main__":
    deal = fetch_live_deals()
    if deal:
        msg = format_live_message(deal)
        post_to_telegram(msg)
    else:
        print("No deal fetched.")
