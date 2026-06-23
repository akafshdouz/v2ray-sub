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
        # الگوهای شناسایی کانفیگ‌ها
        pattern = re.compile(r"(vless|vmess|ss|trojan)://[^\s<>\"]+")

        # بررسی پیام‌ها از آخر به اول (جدیدترین‌ها)
        for msg in reversed(messages):
            text = msg.get_text()
            found = pattern.findall(text)

            # الگوی findall فقط پروتکل رو برمی‌گردونه، پس کل لینک رو با جزییات استخراج می‌کنیم
            matches = [
                m.group(0) for m in pattern.finditer(text) if m.group(0)
            ]

            # اضافه کردن به لیست به ترتیب معکوس تا جدیدترین‌ها اول باشند
            for config in matches:
                if config not in configs:
                    configs.append(config)

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

    # ذخیره ۵۰ کانفیگ نهایی در فایل
    with open("subscription.txt", "w", encoding="utf-8") as f:
        for config in new_configs:
            f.write(config + "\n")

    print(f"Successfully saved {len(new_configs)} unique configs.")


if __name__ == "__main__":
    main()
