import os
from together import Together

# Инициализация клиента
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def rewrite_news(title, summary, link):
    prompt = f"""Ты пишешь посты для Telegram-канала @FuturePulse — ежедневно один научный инсайт.

**Заголовок:** {title}
**Описание:** {summary}
**Ссылка:** {link}

Сформируй пост:
- **Цепляющий заголовок** (жирный)
- 2–4 абзаца с кратким подробным объяснением
- До 600 символов
- Заверши практической ценностью
- Используй Markdown"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
