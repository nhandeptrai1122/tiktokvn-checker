import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lấy token từ biến môi trường (cách bảo mật hơn)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Kiểm tra nếu chưa có token thì thông báo lỗi rõ ràng
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN chưa được đặt. Hãy thêm biến môi trường 'BOT_TOKEN' vào Render!")

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Chào mừng bạn đến với TiktokVN Checker Bot!")

# Tạo và chạy bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
