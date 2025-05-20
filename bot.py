from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("7891909319:AAG0VDOdYCByfWSOrQwYowGaqPZEdNSK2hw")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎥 Kiểm tra video", callback_data='check_video')],
        [InlineKeyboardButton("➕ Theo dõi tài khoản", callback_data='add_user')],
        [InlineKeyboardButton("💰 Spy Affiliate", callback_data='spy_affiliate')],
        [InlineKeyboardButton("🧰 Tool Affiliate", callback_data='toolkit')]
    ]
    await update.message.reply_text(
        "🤖 Chào mừng đến với TiktokVN Checker!\n\n📌 Chọn tác vụ:\n- Kiểm tra video, kênh\n- Theo dõi tài khoản\n- Spy doanh thu Affiliate\n- Trọn bộ tool làm Affiliate",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'check_video':
        await query.edit_message_text("🔍 Đang kiểm tra video mới...")
    elif query.data == 'add_user':
        await query.edit_message_text("➕ Gửi username TikTok bạn muốn theo dõi.")
    elif query.data == 'spy_affiliate':
        await query.edit_message_text("💰 Đang kiểm tra doanh thu Affiliate...")
    elif query.data == 'toolkit':
        await query.edit_message_text("🧰 Gửi danh sách tool hỗ trợ làm Affiliate...")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("batdau", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.run_polling()
