# ✅ main.py — с кэшированием и отправкой постов с кнопками в черновик
import json
import os
from rss_reader import read_rss_sources, fetch_news
from rewrite import rewrite_news
from telegram_sender import send_post_with_buttons

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID_DRAFT = os.getenv("TG_CHAT_ID_DRAFT")
TG_CHAT_ID_MAIN = os.getenv("TG_CHAT_ID_MAIN")
# Всегда отправляем в черновик
SENT_LOG = "sent_log.json"
CACHE_PATH = "cache.json"
FALLBACK_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"

# Загрузка лога отправленных ссылок
if os.path.exists(SENT_LOG):
    with open(SENT_LOG, "r") as f:
        sent_links = set(json.load(f))
else:
    sent_links = set()

# Загрузка кэша для callback-бота
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r") as f:
        cache = json.load(f)
else:
    cache = {}

def save_log():
    with open(SENT_LOG, "w") as f:
        json.dump(list(sent_links), f)

def save_cache():
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

def main():
    for url in read_rss_sources():
        for item in fetch_news(url):
            if item["link"] in sent_links:
                print(f"🛑 Пропущено (дубль): {item['link']}")
                continue

            try:
                headline, body = rewrite_news(item["title"], item["summary"])
                image = item.get("image") or FALLBACK_IMAGE

                # Отправка с кнопками в черновик
                send_post_with_buttons(
                    title=headline,
                    link=item["link"],
                    text=body,
                    image_url=image,
                    token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID
                )

                # Обновление логов и кэша
                sent_links.add(item["link"])
                cache[item["link"]] = {
                    "title": item["title"],
                    "summary": item["summary"],
                    "body": body,
                    "image": image
                }

                print(f"✅ Отправлено: {item['link']}")

            except Exception as e:
                print(f"❌ Ошибка: {e}")

    save_log()
    save_cache()

if __name__ == "__main__":
    main()
