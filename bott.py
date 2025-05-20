import os
import openai
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Lấy token Telegram và DeepInfra
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render tự gán URL này
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

# Khởi tạo client OpenAI (DeepInfra)
client = OpenAI(
    api_key=DEEPINFRA_API_KEY,
    base_url="https://api.deepinfra.com/v1/openai"
)

# Hàm xử lý lệnh /start và menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📹 Kiểm tra video", "👤 Theo dõi tài khoản"],
        ["💰 Spy doanh thu", "🤖 Chat với AI"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Chào mừng đến với TiktokVN Checker!\nChọn tác vụ:", reply_markup=reply_markup)

# Hàm xử lý AI chat
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Xử lý các menu cố định
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

    # Gọi AI trả lời
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

# Khởi tạo và chạy bot bằng webhook
def main():
    if not BOT_TOKEN or not APP_URL or not DEEPINFRA_API_KEY:
        raise ValueError("❗ Thiếu BOT_TOKEN hoặc RENDER_EXTERNAL_URL hoặc DEEPINFRA_API_KEY")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

    print("🚀 Bot đang chạy bằng Webhook tại:", APP_URL + "webhook")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=APP_URL + "webhook"
    )

if __name__ == "__main__":
    main()
