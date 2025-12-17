import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для диалога добавления цели
TYPING_GOAL = 1

# Базы данных (простые словари)
user_goals = {}  # {user_id: ["цель1", "цель2"]}
user_completed = {}  # {user_id: ["выполненная_цель1", "выполненная_цель2"]}

# Мотивационные цитаты
motivation_quotes = [
    "🌟 Маленькие шаги приводят к большим целям.",
    "🚀 Сегодняшние усилия - завтрашние результаты.",
    "💪 Постоянство - ключ к успеху.",
    "📈 Лучше сделать немного, чем ничего.",
    "🔥 Каждый день - новый шанс стать лучше.",
]


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы с ботом."""
    user = update.effective_user
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🤖 Я бот для трекинга привычек!\n\n"
        "🌟 Создавай полезные привычки\n"
        "📈 Отмечай прогресс\n"
        "✅ Выполняй цели\n"
        "📊 Следи за статистикой\n\n"
        "💡 *Простой принцип работы:*\n"
        "1. Добавь цели (/add)\n"
        "2. Отмечай выполнение (/done)\n"
        "3. Следи за прогрессом (/stats)\n"
        "4. Получай мотивацию!\n\n"
        "📋 *Доступные команды:*\n"
        "/add - Добавить новую цель\n"
        "/done - Отметить цель выполненной\n"
        "/stats - Посмотреть статистику\n"
        "/goals - Активные привычки\n"
        "/motivation - Мотивация\n"
        "/help - Справка\n"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Справка по командам."""
    help_text = (
        "🤖 *Бот для трекинга привычек*\n\n"
        "🎯 *Основные команды:*\n"
        "/start - Начать работу\n"
        "/add - Добавить новую цель\n"
        "/done - Отметить выполнение\n"
        "/goals - Активные привычки\n"
        "/stats - Статистика\n"
        "/motivation - Мотивация\n"
        "/cancel - Отменить действие\n\n"
        "🚀 *Совет для старта:*\n"
        "Начни с одной простой привычки и делай её регулярно!\n"
        "Лучше небольшие, но постоянные шаги, чем редкие подвиги."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


# Команда /add (начало)
async def add_goal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинаем добавление цели."""
    await update.message.reply_text(
        "*🎯 Новая цель*\n\n"
        "Какую привычку ты хочешь выработать?\n\n"
        "*📝 Примеры:*\n"
        "• Читать 30 минут каждый день\n"
        "• Пить 2 литра воды\n"
        "• Ложиться спать до 23:00\n"
        "• Делать зарядку\n\n"
        "*❌ Отменить:* /cancel",
        parse_mode="Markdown"
    )
    return TYPING_GOAL


# Команда /add (окончание)
async def add_goal_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Заканчиваем добавление цели."""
    user_id = update.effective_user.id
    new_goal = update.message.text

    # Создаем список целей, если его нет
    if user_id not in user_goals:
        user_goals[user_id] = []

    # Добавляем цель
    user_goals[user_id].append(new_goal)

    await update.message.reply_text(
        f"✅ Цель добавлена: *{new_goal}*\n"
        f"📊 Всего целей: {len(user_goals[user_id])}\n\n"
        f"📝 *Что дальше?*\n"
        f"• /goals - Посмотреть все цели\n"
        f"• /add - Добавить ещё цель\n"
        f"• /done - Отметить выполнение",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


# Команда /goals
async def show_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает активные цели."""
    user_id = update.effective_user.id

    if user_id not in user_goals or not user_goals[user_id]:
        await update.message.reply_text(
            "🌟 *Активные привычки*\n\nСписок пуст. Добавь первую цель: /add",
            parse_mode="Markdown"
        )
    else:
        goals_list = "\n".join([f"✅ {goal}" for goal in user_goals[user_id]])
        message = f"🌟 *Активные привычки*\n\n{goals_list}\n\n📊 Всего активных: {len(user_goals[user_id])}"
        await update.message.reply_text(message, parse_mode="Markdown")


# Команда /done
async def mark_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отметить выполнение цели."""
    user_id = update.effective_user.id

    if user_id not in user_goals or not user_goals[user_id]:
        await update.message.reply_text("У тебя пока нет целей для отметки. Добавь через /add!")
        return

    # Простой способ - отмечаем первую цель
    completed_goal = user_goals[user_id].pop(0)  # Убираем первую цель

    # Сохраняем выполненную цель
    if user_id not in user_completed:
        user_completed[user_id] = []
    user_completed[user_id].append(completed_goal)

    await update.message.reply_text(
        f"🎉 *Отлично!*\n"
        f"Цель выполнена: *{completed_goal}*\n\n"
        f"📊 Осталось целей: {len(user_goals.get(user_id, []))}",
        parse_mode="Markdown"
    )


# Команда /stats
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статистику."""
    user_id = update.effective_user.id

    active = len(user_goals.get(user_id, []))
    completed = len(user_completed.get(user_id, []))
    total = active + completed

    # Мотивация
    if total == 0:
        motivation = "🚀 Начни с малого — добавь первую цель!"
        progress = 0
    elif completed == 0:
        motivation = "👍 У тебя есть цели! Начни действовать!"
        progress = 0
    else:
        progress = int((completed / total) * 100)
        if progress < 30:
            motivation = "📈 Хорошее начало! Продолжай!"
        elif progress < 70:
            motivation = "💪 Отличный прогресс!"
        else:
            motivation = "🏆 Потрясающие результаты!"

    # Прогресс-бар
    filled = "▓" * (progress // 20)  # 5 уровней
    empty = "░" * (5 - progress // 20)
    progress_bar = f"[{filled}{empty}]"

    stats_text = (
        f"📊 *Твоя статистика*\n\n"
        f"• Активных целей: {active}\n"
        f"• Выполнено целей: {completed}\n"
        f"• Всего целей: {total}\n"
        f"• Прогресс: {progress}% {progress_bar}\n\n"
        f"💡 {motivation}"
    )

    # Последние выполненные
    if user_id in user_completed and user_completed[user_id]:
        last_three = user_completed[user_id][-3:]  # 3 последние
        if last_three:
            stats_text += f"\n\n🎯 *Последние выполненные:*\n"
            for goal in last_three:
                stats_text += f"• {goal}\n"

    await update.message.reply_text(stats_text, parse_mode="Markdown")


# Команда /motivation
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет мотивационную цитату."""
    quote = random.choice(motivation_quotes)
    await update.message.reply_text(f"💫 *Мотивация на сегодня:*\n\n{quote}", parse_mode="Markdown")


# Команда /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменяет действие."""
    await update.message.reply_text("❌ Действие отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

__all__ = [
    'start', 'help_command', 'add_goal_start', 'add_goal_end',
    'show_goals', 'mark_done', 'show_stats', 'motivation', 'cancel',
    'TYPING_GOAL'
]


