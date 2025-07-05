
import requests
import os

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

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

    response = requests.post(
        "https://api.together.xyz/inference",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/Llama-3-70B-Instruct",
            "prompt": prompt,
            "max_tokens": 800,
            "temperature": 0.7
        }
    )
    response.raise_for_status()
    return response.json()["output"].strip()
