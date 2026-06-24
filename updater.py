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
        messages = soup.find_all("div", class_="tgme_widget_message_text")

        configs = []

        # این الگو دقیقاً از شروع پروتکل تا اولین فضای خالی (مثل خط بعد یا فاصله) را جدا می‌کند
        # این کار مانع ترکیب شدن متن فارسی خط بعد با خود کانفیگ می‌شود
        pattern = re.compile(r"(vless|vmess|ss|trojan)://[^\s<>#\"|]+")

        for msg in reversed(messages):
            text = msg.get_text()
            matches = pattern.finditer(text)

            for match in matches:
                clean_config = match.group(0).strip()
                protocol = match.group(1)

                # بازسازی بخش هشتگ (نام کانال) در صورت قطع شدن اتفاقی
                # کانال معمولاً از هشتگ #@filembad استفاده می‌کند
                if "#" not in clean_config:
                    clean_config += "#%40filembad"

                # تمیزکاری نهایی انتهای کانفیگ از کاراکترهای مزاحم فارسی یا نشانه‌ها
                clean_config = re.sub(
                    r"[^a-zA-Z0-9:@/?=&%#._~+-]+$", "", clean_config
                )

                # فیلتر سخت‌گیرانه طول رشته برای حذف نمونه‌های ناقص (مثل vless://3)
                if len(clean_config) < 40:
                    continue

                # اعتبارسنجی ساختاری پروتکل‌های غیر vmess (باید شامل علامت @ باشند)
                if protocol in ["vless", "trojan", "ss"] and "@" not in clean_config:
                    continue

                # جلوگیری از ورود کانفیگ‌های تکراری به لیست
                if clean_config not in configs:
                    configs.append(clean_config)

                # متوقف شدن پروسه به محض جمع‌آوری ۵۰ کانفیگ تازه
                if len(configs) >= 100:
                    return configs

        return configs
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def main():
    print("Fetching new configs...")
    new_configs = fetch_configs()

    if not new_configs:
        print("No healthy configs found. Keeping the old file.")
        return

    # ذخیره کانفیگ‌ها؛ کاملاً تفکیک‌شده و ردیف به ردیف
    with open("subscription.txt", "w", encoding="utf-8") as f:
        for config in new_configs:
            f.write(config + "\n")

    print(
        f"Successfully saved {len(new_configs)} HEALTHY unique configs line by line."
    )


if __name__ == "__main__":
    main()
