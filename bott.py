import os
import openai
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Token và API Key từ biến môi trường
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
APP_URL = "https://tiktokvn-checker-001.onrender.com"  # ⚠️ Gắn cứng domain để Telegram webhook hoạt động

# Khởi tạo OpenAI client (DeepInfra proxy)
client = OpenAI(
    api_key=DEEPINFRA_API_KEY,
    base_url="https://api.deepinfra.com/v1/openai"
)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📹 Kiểm tra video", "👤 Theo dõi tài khoản"],
        ["💰 Spy doanh thu", "🤖 Chat với AI"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Chào mừng đến với TiktokVN Checker!\nChọn tác vụ:", reply_markup=reply_markup)

# Xử lý tin nhắn và gọi AI
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message == "📹 Kiểm tra video":
        await update.message.reply_text("📥 Vui lòng nhập link video TikTok để kiểm tra.")
        return
    elif user_message == "👤 Theo dõi tài khoản":
        await update.message.reply_text("👁️ Nhập link hoặc username tài khoản bạn muốn theo dõi.")
        return
    elif user_message == "💰 Spy doanh thu":
        await update.message.reply_text("💡 Gửi link sản phẩm/affiliate để phân tích doanh thu.")
        return
    elif user_message == "🤖 Chat với AI":
        await update.message.reply_text("🧠 Bạn có thể hỏi bất cứ điều gì! Ví dụ: 'Cách tăng follow TikTok'")
        return

    # Gọi AI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý hỗ trợ TikTok, nói tiếng Việt."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ AI bị lỗi:\n\n{e}")

# Khởi chạy bằng Webhook
def main():
    if not BOT_TOKEN or not DEEPINFRA_API_KEY:
        raise ValueError("❗ Thiếu BOT_TOKEN hoặc DEEPINFRA_API_KEY")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

    print("🚀 Bot đang chạy bằng Webhook tại:", APP_URL + "/webhook")
    app.run_web_app(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        path="/webhook"  # ✅ Quan trọng để Telegram nhận đúng endpoint
    )

if __name__ == "__main__":
    main()
