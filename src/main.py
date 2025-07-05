import json
import os
from rss_reader import read_rss_sources, fetch_news
from rewrite import rewrite_news
from telegram_sender import send_telegram_message_with_photo

TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")
SENT_LOG = "sent_log.json"
FALLBACK_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"

# Загрузка лога
if os.path.exists(SENT_LOG):
    with open(SENT_LOG, "r") as f:
        sent_links = set(json.load(f))
else:
    sent_links = set()

# Сохранение лога
def save_log():
    with open(SENT_LOG, "w") as f:
        json.dump(list(sent_links), f)

def main():
    for url in read_rss_sources():
        for item in fetch_news(url):
            if item["link"] in sent_links:
                print(f"🛑 Пропущено (дубль): {item['link']}")
                continue

            try:
                # Генерация текста
                rewritten = rewrite_news(item["summary"])

                # Отправка поста с изображением
                send_telegram_message_with_photo(
                    title=item["title"],
                    link=item["link"],
                    text=rewritten,
                    image_url=item.get("image") or FALLBACK_IMAGE,
                    token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID
                )

                print(f"✅ Отправлено: {item['link']}")
                sent_links.add(item["link"])

            except Exception as e:
                print(f"❌ Ошибка: {e}")

    save_log()

if __name__ == "__main__":
    main()
