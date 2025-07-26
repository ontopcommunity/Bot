from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from collections import defaultdict
from PIL import Image, ImageDraw
import requests
import io
import datetime
Bot = "7550142487:AAHIm7uxWug1vlJId18ospVz1fZpoYLaRgA"

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = None

    # Trường hợp 1: Trả lời tin nhắn ai đó
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    # Trường hợp 2: Nhập ID hoặc @username
    elif context.args:
        arg = context.args[0]
        try:
            if arg.startswith("@"):
                target_user = await context.bot.get_chat(arg)
            else:
                target_user = await context.bot.get_chat(int(arg))
        except Exception:
            await update.message.reply_text("🚫 Không tìm thấy người dùng.")
            return

    # Trường hợp 3: Mặc định là người gửi lệnh
    else:
        target_user = update.effective_user

    chat = await context.bot.get_chat(target_user.id)
    photos = await context.bot.get_user_profile_photos(target_user.id, limit=100)

    user_id = target_user.id
    username = f"@{target_user.username}" if target_user.username else "Không có"
    bio = f"{chat.bio}" if chat.bio else "“Không có”"
    photo_count = photos.total_count
    join_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Tạo ảnh nền
    background = Image.open("template.jpg").convert("RGBA")

    # Tải avatar và xử lý
    if photo_count > 0:
        photo_file = await context.bot.get_file(photos.photos[0][-1].file_id)
        avatar_bytes = await photo_file.download_as_bytearray()
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((280, 280))

        # Bo tròn avatar
        mask = Image.new("L", (280, 280), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 280, 280), fill=255)
        avatar.putalpha(mask)

        # Căn giữa vào ảnh nền
        pos = ((background.width - 280) // 2, (background.height - 280) // 2)
        background.paste(avatar, pos, avatar)

    # Xuất ảnh kết quả
    output = io.BytesIO()
    background.save(output, format="PNG")
    output.seek(0)

    # Caption gửi kèm ảnh
    caption = (
        f"📍 <b>Thông tin thành viên</b>\n\n"
        f"🔸 Tên: {target_user.full_name}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"✴️ Tên người dùng: {username}\n"
        f"💠 TT Dữ liệu: {photo_count} ảnh\n"
        f"👨🏿‍💻 Bio: <blockquote>{bio}</blockquote>\n"
        f"⏰ Vào lúc: {join_time}"
    )

    # Gửi ảnh kèm caption
    await update.message.reply_photo(
        photo=InputFile(output),
        caption=caption,
        parse_mode="HTML"
    )
import os
import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"

# Media & nút
MEDIA = {
    "cutie": "https://graph.org/file/24375c6e54609c0e4621c.mp4",
    "hot": "https://graph.org/file/745ba3ff07c1270958588.mp4",
    "horny": "https://graph.org/file/eaa834a1cbfad29bd1fe4.mp4",
    "sexy": "https://graph.org/file/58da22eb737af2f8963e6.mp4",
    "gay": "https://graph.org/file/850290f1f974c5421ce54.mp4",
    "lesbian": "https://graph.org/file/ff258085cf31f5385db8a.mp4",
    "boob": "https://i.gifer.com/8ZUg.gif",
    "cock": "https://telegra.ph/file/423414459345bf18310f5.gif"
}

# Lệnh media vui
COMMAND_USAGE = defaultdict(int)

async def handle_fun(update: Update, context: ContextTypes.DEFAULT_TYPE, command, caption_template):
    user = update.effective_user
    chat_id = update.effective_chat.id

    reply_user = update.message.reply_to_message.from_user if update.message.reply_to_message else user
    reply_id = update.message.reply_to_message.message_id if update.message.reply_to_message else update.message.message_id

    uid = user.id
    date_key = f"{uid}:{command}:{datetime.date.today()}"

    if COMMAND_USAGE[date_key] >= 30:
        await update.message.reply_text(f"🚫 Bạn đã dùng /{command} 30 lần hôm nay. Hãy thử lại ngày mai!")
        return
    COMMAND_USAGE[date_key] += 1  # Tăng số lần sử dụng

    mention = f"[{reply_user.first_name}](tg://user?id={reply_user.id})"
    value = random.randint(1, 100)
    caption = caption_template.format(mention=mention, value=value)

    await context.bot.send_document(
        chat_id=chat_id,
        document=MEDIA[command],
        caption=caption,
        parse_mode="Markdown",
        reply_to_message_id=reply_id
    )
# Từng lệnh
async def cutie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "cutie", "🍑 {mention} dễ thương {value}% nhé! 🥀")

async def hot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "hot", "🔥 {mention} nóng bỏng {value}%! 🔥")

async def horny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "horny", "🔥 {mention} tò mò {value}% nha! 😏")

async def sexy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "sexy", "🔥 {mention} quyến rũ {value}%! 😘")

async def gay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "gay", "🍷 {mention} gay {value}% nè! 🏳️‍🌈")

async def lesbian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "lesbian", "💜 {mention} lesbian {value}% đó! 🏳️‍🌈")

async def boob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "boob", "🍒 Kích thước ngực của {mention} là {value}! 😜")

async def cock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_fun(update, context, "cock", "🍆 Kích thước của {mention} là {value}cm! 😎")



# Cài bot
app = ApplicationBuilder().token(Bot).build()
app.add_handler(CommandHandler("thongtin", info))
app.add_handler(CommandHandler("cutie", cutie))
app.add_handler(CommandHandler("hot", hot))
app.add_handler(CommandHandler("horny", horny))
app.add_handler(CommandHandler("sexy", sexy))
app.add_handler(CommandHandler("gay", gay))
app.add_handler(CommandHandler("lesbian", lesbian))
app.add_handler(CommandHandler("boob", boob))
app.add_handler(CommandHandler("cock", cock))

app.run_polling()
