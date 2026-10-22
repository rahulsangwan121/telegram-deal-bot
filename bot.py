import os
import requests
import random

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

# Max-earning high demand loot products pool (Hum isme live scraper/API bhi aage hook karenge)
loot_deals = [
    {
        "title": "boAt Airdopes 141 True Wireless Earbuds",
        "mrp": "₹4,499",
        "price": "₹899",
        "discount": "80% OFF 🔥",
        "link": "https://earnkaro.com/" # Yahan aapka EarnKaro affiliate link aayega
    },
    {
        "title": "Fastrack Analog Dial Men's Watch",
        "mrp": "₹2,995",
        "price": "₹1,195",
        "discount": "60% OFF ⚡",
        "link": "https://earnkaro.com/"
    },
    {
        "title": "PUMA Men's Running Shoes",
        "mrp": "₹3,999",
        "price": "₹1,299",
        "discount": "67% OFF 🚀",
        "link": "https://earnkaro.com/"
    }
]

def format_loot_message(deal):
    message = (
        f"🚨 **MEGA LOOT DEAL ALERT** 🚨\n\n"
        f"🔥 **{deal['title']}**\n\n"
        f"❌ M.R.P.: ~{deal['mrp']}~\n"
        f"💥 **Deal Price: {deal['price']}**\n"
        f"🎯 Discount: **{deal['discount']}**\n\n"
        f"🛒 **Grab Fast Here:** {deal['link']}\n\n"
        f"⚡ *Limited Period Offer! Price can drop anytime!* 🏃‍♂️"
    )
    return message

def post_to_telegram(caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_USERNAME,
        "text": caption,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Loot deal successfully posted!")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    # Randomly select a high-converting loot deal from the pool
    selected_deal = random.choice(loot_deals)
    formatted_msg = format_loot_message(selected_deal)
    post_to_telegram(formatted_msg)
