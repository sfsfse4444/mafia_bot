import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8739283943:AAF0QuCixWwviRhDiUE8_01AJfC166Ck6zc"

players = []
roles = {}
game_started = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎭 Бот Мафии готов!\n/join чтобы присоединиться")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, game_started

    if game_started:
        await update.message.reply_text("Игра уже началась ❌")
        return

    user = update.effective_user.first_name

    if user not in players:
        players.append(user)
        await update.message.reply_text(f"✅ {user} присоединился!")
    else:
        await update.message.reply_text("Ты уже в игре!")

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_started, roles

    if len(players) < 3:
        await update.message.reply_text("❗ Нужно минимум 3 игрока")
        return

    game_started = True

    mafia = random.sample(players, 1)

    for p in players:
        if p in mafia:
            roles[p] = "Мафия"
        else:
            roles[p] = "Мирный"

    await update.message.reply_text("🎮 Игра началась!")

    # отправка ролей в личку
    for p in players:
        role = roles[p]
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"{p}, твоя роль: {role}")
        except:
            pass

async def roles_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📜 Игроки и роли:\n"
    for p in players:
        text += f"{p} — {roles.get(p, 'Нет роли')}\n"
    await update.message.reply_text(text)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, roles, game_started
    players = []
    roles = {}
    game_started = False
    await update.message.reply_text("🔄 Игра сброшена")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("start_game", start_game))
app.add_handler(CommandHandler("roles", roles_list))
app.add_handler(CommandHandler("reset", reset))

print("Бот запущен...")
app.run_polling()
