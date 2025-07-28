from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_image_topic(title, summary):
    prompt = f"""
Ты — нейросеть, которая помогает выбрать один ключевой английский тег (по одному слову), который наилучшим образом описывает тему научной статьи для поиска подходящего изображения на Unsplash.

Формат ответа: только 1 английское слово, без точек, кавычек и пояснений.

Заголовок:
{title}

Описание:
{summary}
"""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.5-pro",
            messages=[{
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }],
            extra_headers={
                "HTTP-Referer": "https://t.me/FuturePulse",
                "X-Title": "FuturePulse Topic"
            },
            extra_body={}
        )
        topic = response.choices[0].message.content.strip().lower()
        if " " in topic or not topic.isascii():
            return None
        return topic
    except Exception as e:
        print(f"❌ Ошибка в extract_image_topic: {e}")
        return None
