import os
import requests

# GitHub Secrets se token uthayega, aur agar local ho toh direct use karega
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8782926177:AAH-7xoesBaXiDyJT_KAqePTxVJOGczLkes")
CHANNEL_USERNAME = "@dailyLootDeels"

deal_data = {
    "title": "Wireless Noise Cancelling Headphones",
    "original_price": "₹4,999",
    "deal_price": "₹1,999",
    "discount": "60% OFF",
    "affiliate_link": "https://earnkaro.com/"
}

def format_deal_message(deal):
    message = (
        f"🔥 **SUPER DEAL ALERT** 🔥\n\n"
        f"📌 **{deal['title']}**\n\n"
        f"❌ M.R.P.: ~{deal['original_price']}~\n"
        f"✅ Deal Price: **{deal['deal_price']}** ({deal['discount']})\n\n"
        f"🛒 **Buy Now:** {deal['affiliate_link']}\n\n"
        f"⚡ *Limited period offer! Fast grab!*"
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
        print("✅ Message successfully posted on Telegram channel!")
    else:
        print(f"❌ Failed to post: {response.text}")

if __name__ == "__main__":
    formatted_msg = format_deal_message(deal_data)
    post_to_telegram(formatted_msg)