from together import Together
import os

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

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
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": prompt}]
        )
        topic = response.choices[0].message.content.strip().lower()
        if " " in topic or not topic.isascii():
            return None
        return topic
    except Exception as e:
        print(f"❌ Ошибка в extract_image_topic: {e}")
        return None
