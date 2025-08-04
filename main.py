import os
import telebot
import openai
import requests
import uuid

# Подгружаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    try:
        file_info = bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем как .ogg
        unique_id = str(uuid.uuid4())
        input_filename = f"{unique_id}.ogg"
        with open(input_filename, 'wb') as f:
            f.write(downloaded_file)

        # Отправляем в OpenAI Whisper
        with open(input_filename, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        bot.reply_to(message, transcript["text"])
        os.remove(input_filename)

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.polling()
