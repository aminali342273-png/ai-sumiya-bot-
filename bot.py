from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN =load_dotenv()9151106485:AAHbCtroD89AdrhmnO5RNg8qmDAkrpQ6hnA
GEMINI_API_KEY =AQ.Ab8RN6JNQq9FweYLcxUbPewgXKOD-s3PCl89ucB2sCIGvGUa8Q

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
তুমি Ai Sumiya, MicroJob ওয়েবসাইটের বাংলা AI সহকারী।
তোমার কাজ:
1. ওয়েবসাইটের সমস্যা বিশ্লেষণ করা।
2. Supabase Database সমস্যার সমাধান প্রস্তাব করা।
3. ওয়েবসাইটের ডিজাইন ও কোড উন্নত করা।
4. GitHub, Vercel ও Supabase-এর কাজে সাহায্য করা।
সবসময় বাংলায় উত্তর দেবে।
কোনো পরিবর্তনের আগে মালিকের অনুমতি নেবে।
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম! আমি Ai Sumiya। "
        "MicroJob ওয়েবসাইটের সমস্যা আমাকে বলুন।"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\n\nUser: " + message
        )
        await update.message.reply_text(response.text or "উত্তর পাওয়া যায়নি।")
    except Exception as error:
        logging.exception("AI error")
        await update.message.reply_text(
            "দুঃখিত, AI-তে সমস্যা হয়েছে। পরে চেষ্টা করুন।"
        )

def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        raise RuntimeError("Bot token বা Gemini API key পাওয়া যায়নি।")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
