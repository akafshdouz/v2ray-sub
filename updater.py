import re
import requests
from bs4 import BeautifulSoup

# آدرس وب کانال تلگرام
CHANNEL_URL = "https://t.me/s/filembad"


def fetch_configs():
    try:
        response = requests.get(CHANNEL_URL, timeout=15)
        if response.status_code != 200:
            print(f"Error fetching channel: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # پیدا کردن متن تمام پیام‌ها
        messages = soup.find_all("div", class_="tgme_widget_message_text")

        configs = []

        # استخراج دقیق تمام پروتکل‌ها با Regex
        # این الگو کل لینک رو تا جایی که به پروتکل بعدی یا فاصله برسه جدا می‌کنه
        pattern = re.compile(
            r"(vless|vmess|ss|trojan)://[^(\s<>\"|vless|vmess|ss|trojan)]+"
        )

        # بررسی پیام‌ها از آخر به اول (جدیدترین‌ها)
        for msg in reversed(messages):
            text = msg.get_text()

            # پیدا کردن تمام کانفیگ‌های موجود در پیام جاری
            matches = [
                m.group(0) for m in pattern.finditer(text) if m.group(0)
            ]

            for config in matches:
                clean_config = config.strip()

                # حذف کاراکترهای مزاحم فارسی یا اموجی از انتهای کانفیگ
                clean_config = re.sub(
                    r"[^a-zA-Z0-9:@/?=&%#._~+-]+$", "", clean_config
                )

                # اطمینان از اینکه کانفیگ خالی نیست و تکراری هم نیست
                if clean_config and clean_config not in configs:
                    configs.append(clean_config)

                # اگر به ۵۰ تا رسیدیم، متوقف شو
                if len(configs) >= 50:
                    return configs[:50]

        return configs
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def main():
    print("Fetching new configs...")
    new_configs = fetch_configs()

    if not new_configs:
        print("No configs found or error occurred. Keeping the old file.")
        return

    # ذخیره کانفیگ‌ها؛ هر کانفیگ دقیقاً در یک ردیف مجزا
    with open("subscription.txt", "w", encoding="utf-8") as f:
        for config in new_configs:
            f.write(config + "\n")  # این \n باعث میشه بره خط بعدی

    print(f"Successfully saved {len(new_configs)} unique configs line by line.")


if __name__ == "__main__":
    main()
