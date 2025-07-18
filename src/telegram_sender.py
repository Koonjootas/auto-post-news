from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import requests

def send_telegram_message_with_photo(title, link, text, image_url, token, chat_id):
    caption = f"[**{title}**]({link})\n\n{text}"
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

def send_telegram_message_without_photo(title, link, text, token, chat_id):
    message = f"[**{title}**]({link})\n\n{text}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

def send_post_with_buttons(title, link, text, image_url, token, chat_id):
    bot = Bot(token=token)
    caption = f"*{title}*\n\n{text}\n[Читать статью]({link})"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Опубликовать", callback_data=f"post|{link}")],
        [InlineKeyboardButton("✏️ Рерайт", callback_data=f"rewrite|{link}")]
    ])

    bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
