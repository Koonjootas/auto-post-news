import os
from together import Together

# Инициализация клиента
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def rewrite_news(title, summary, link):
    prompt = f"""Ты пишешь посты для Telegram-канала @FuturePulse — ежедневно один научный инсайт. Твоя задача — сделать короткий, понятный и цепляющий рерайт научной новости на русском языке. Пиши ясно, без сложного жаргона, но с уважением к научному факту.

Исходные данные:
**Заголовок:** {title}
**Описание:** {summary}
**Ссылка:** {link}



Формат вывода:
1. **Заголовок:** оформлен жирным (**звёздочки**), должен интриговать
2. Основной текст: 3–4 абзаца, объясни суть и значимость
3. Заверши практической пользой или интересным наблюдением
4. Не более 600 символов
5. Используй Markdown
6. Не добавляй фактов от себя. Не повторяй ссылку.

"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
