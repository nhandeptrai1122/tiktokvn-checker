import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Lấy token Telegram bot từ biến môi trường
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Lấy API Key của DeepInfra từ biến môi trường
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

# Cấu hình DeepInfra API
openai.api_key = DEEPINFRA_API_KEY
openai.api_base = "https://api.deepinfra.com/v1/openai"

# Hàm khởi động bot và hiện menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📹 Kiểm tra video", "👤 Theo dõi tài khoản"],
        ["💰 Spy doanh thu", "🤖 Chat với AI"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Chào mừng đến với TiktokVN Checker!\nChọn tác vụ:", reply_markup=reply_markup)

# Xử lý menu lệnh và AI chat
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Xử lý các lệnh có sẵn
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

    # Xử lý AI chat qua DeepInfra
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # bạn có thể thử các model khác: mistralai/Mistral-7B-Instruct
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý hỗ trợ TikTok, nói tiếng Việt, trả lời gọn gàng."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ AI bị lỗi: {e}")

# Hàm khởi chạy bot
def main():
    if not BOT_TOKEN or not DEEPINFRA_API_KEY:
        raise ValueError("❗ BOT_TOKEN hoặc DEEPINFRA_API_KEY chưa được cấu hình.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
