# ✅ callback_bot.py — логика обработки кнопок
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import os
import logging
import json
from telegram_sender import send_telegram_message_with_photo
from rewrite import rewrite_news_with_alt_prompt

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID_DRAFT = os.getenv("TG_CHAT_ID_DRAFT")
TG_CHAT_ID_MAIN = os.getenv("TG_CHAT_ID_MAIN")

CACHE_PATH = "cache.json"

assert TG_TOKEN is not None, "❌ BOT_TOKEN переменная не установлена!"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка кэша постов по ссылке
def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    cache = load_cache()
    if not query.data or "|" not in query.data:
        query.message.reply_text("❌ Неверный формат данных кнопки.")
        return

    action, link = query.data.split("|", 1)

    if link not in cache:
        query.message.reply_text("❌ Кэш не найден для этой статьи.")
        return

    post = cache[link]  # title, summary, body, image

    if action == "post":
        send_telegram_message_with_photo(
            title=post["title"],
            link=link,
            text=post["body"],
            image_url=post["image"],
            token=TG_TOKEN,
            chat_id=MAIN_ID
        )
        query.edit_message_reply_markup(reply_markup=None)
        query.message.reply_text("✅ Опубликовано в основной канал!")

    elif action == "rewrite":
        new_title, new_text = rewrite_news_with_alt_prompt(post["title"], post["summary"])
        post["title"] = new_title
        post["body"] = new_text
        cache[link] = post
        save_cache(cache)

        query.edit_message_caption(
            caption=f"*{new_title}*\n\n{new_text}\n[Читать статью]({link})",
            parse_mode="Markdown"
        )
        query.answer("✏️ Рерайт выполнен!")

def main():
    updater = Updater(TG_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("🚀 Callback-бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
