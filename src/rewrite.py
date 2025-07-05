from together import Together
import os

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def rewrite_news(summary):
    prompt = f"""Переработай следующую аннотацию научной статьи в виде короткого, информативного поста для Telegram, пиши как экспертный копирайтер своим языком, обязательно расскажи о практической ценности. Без заголовка и ссылки, только текст (3–4 абзаца, до 600 символов):

{summary}
"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{ "role": "user", "content": prompt }]
    )

    return response.choices[0].message.content.strip()
