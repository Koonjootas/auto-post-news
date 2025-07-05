from together import Together
import os

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def rewrite_news(title, summary):
    prompt = f"""Переработай следующую аннотацию научной статьи в виде короткого, информативного поста для Telegram, пиши как экспертный копирайтер своим языком, обязательно расскажи о практической ценности.

Вот заголовок оригинальной статьи:
{title}

Вот краткое описание:
{summary}

Сформируй:
1. Новый короткий и выразительный заголовок (без ссылки)
2. Затем — 3–4 абзаца пояснительного текста до 600 символов, с подходом как копирайтер

Формат ответа:
ЗАГОЛОВОК

ТЕКСТ
"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{ "role": "user", "content": prompt }]
    )

    result = response.choices[0].message.content.strip()
    if "\n\n" in result:
        headline, body = result.split("\n\n", 1)
    else:
        headline, body = result, ""

    return headline.strip(), body.strip()
