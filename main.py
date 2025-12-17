import os
from telegram.ext import (Application, CommandHandler, ConversationHandler,
                          MessageHandler, filters)
from src.bot import (TYPING_GOAL, add_goal_end, add_goal_start, cancel,
                     help_command, mark_done, motivation, show_goals,
                     show_stats, start)


def main():
    """Запуск бота."""
    with open('.env') as f:
        TOKEN = f.read().split('=')[1].strip()

    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Диалог для добавления цели
    add_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_goal_start)],
        states={
            TYPING_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_goal_end)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Регистрируем команды
    app.add_handler(add_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("goals", show_goals))
    app.add_handler(CommandHandler("done", mark_done))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("motivation", motivation))

    # Запускаем
    print("=" * 50)
    print("🤖 Бот для трекинга привычек запущен!")
    print("📋 Команды: /start /add /done /goals /stats /motivation")
    print("=" * 50)

    app.run_polling()


if __name__ == "__main__":
    main()