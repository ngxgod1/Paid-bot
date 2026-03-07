import requests
import time
import re
import telegram
import phonenumbers
from phonenumbers import geocoder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "BOT TOKEN"
CHAT_ID = GROUP ID

API_URL = "API URL"
TOKEN = "API TOKEN"

bot = telegram.Bot(token=BOT_TOKEN)

sent = set()

print("✅ OTP Forwarder Started...")


# Country flag function
def get_flag(country_code):
    try:
        OFFSET = 127397
        return ''.join(chr(ord(c) + OFFSET) for c in country_code.upper())
    except:
        return "🌍"


# Hide number
def hide_number(num):
    if len(num) > 8:
        return num[:4] + "xxxx" + num[-4:]
    return num


while True:

    try:

        r = requests.get(API_URL, params={"token": TOKEN}, timeout=20)

        if r.status_code != 200:
            time.sleep(5)
            continue

        try:
            data = r.json()
        except:
            print("⚠ API empty response")
            time.sleep(5)
            continue

        if "data" not in data:
            time.sleep(5)
            continue

        entries = data["data"]

        for sms in entries:

            number = sms.get("num")
            message = str(sms.get("message"))
            dt = sms.get("dt")

            service = str(sms.get("cli", "UNKNOWN")).upper()

            unique = str(number) + str(dt)

            if unique in sent:
                continue

            sent.add(unique)

            # OTP detect
            otp_match = re.search(r"\d{3}-\d{3}|\d{6}", message)

            if otp_match:
                otp = otp_match.group()
            else:
                otp = "N/A"

            # Country detect
            try:
                numobj = phonenumbers.parse("+" + number)
                country = geocoder.description_for_number(numobj, "en")
                country_code = phonenumbers.region_code_for_number(numobj)
                flag = get_flag(country_code)
            except:
                country = "Unknown"
                flag = "🌍"

            hidden_number = hide_number(number)

            text = f"""
✅ {flag} {country} {service} OTP!

━━━━━━━━━━━━━━━━━━

📱 Number: {hidden_number}
🔒 OTP Code: {otp}
⚙ Service: {service}
⏳ Time: {dt}

━━━━━━━━━━━━━━━━━━

💬 Message:
{message}

━━━━━━━━━━━━━━━━━━

👤 By: @ngxgod1
"""

            keyboard = [
                [InlineKeyboardButton("📱 Numbers Channel", url="https://t.me/NumOTPV1BOT")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            try:

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )

                print("✅ OTP Forwarded:", otp)

            except Exception as tg_error:

                print("❌ Telegram Error:", tg_error)

    except Exception as api_error:

        print("❌ API Error:", api_error)

    time.sleep(5)