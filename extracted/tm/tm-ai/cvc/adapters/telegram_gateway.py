import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

logger = logging.getLogger("cvc.telegram_gateway")

_bot: Bot | None = None
_dp: Dispatcher | None = None
_polling_task: asyncio.Task | None = None

async def start_telegram_gateway(settings, workspace_mgr):
    global _bot, _dp, _polling_task
    
    if not settings.telegram.bot_token:
        logger.error("Telegram bot_token is missing.")
        return

    _bot = Bot(token=settings.telegram.bot_token)
    _dp = Dispatcher()

    # Import handler to bind routes
    from cvc.adapters.telegram_handler import register_handlers
    register_handlers(_dp, _bot, settings, workspace_mgr)

    logger.info("Setting bot commands...")
    commands = [
        BotCommand(command="help", description="Show help information"),
        BotCommand(command="status", description="Show current agent status"),
        BotCommand(command="log", description="Show agent logs"),
        BotCommand(command="commit", description="Commit current changes"),
        BotCommand(command="branch", description="Switch or manage branches"),
        BotCommand(command="checkout", description="Checkout a branch"),
        BotCommand(command="branches", description="List all branches"),
        BotCommand(command="search", description="Search in workspace"),
        BotCommand(command="compact", description="Compact session history"),
        BotCommand(command="health", description="Check agent health"),
        BotCommand(command="model", description="Switch LLM model"),
        BotCommand(command="provider", description="Switch LLM provider"),
        BotCommand(command="undo", description="Undo last commit/action"),
        BotCommand(command="retry", description="Retry last command"),
        BotCommand(command="cost", description="Show session cost"),
        BotCommand(command="analytics", description="Show agent analytics"),
        BotCommand(command="web", description="Web search/fetch"),
        BotCommand(command="git", description="Git operations"),
        BotCommand(command="image", description="Image operations"),
        BotCommand(command="memory", description="Memory operations"),
        BotCommand(command="clear", description="Clear conversation context"),
    ]
    try:
        await _bot.set_my_commands(commands)
        print("DEBUG: set_my_commands success")
    except Exception as e:
        print(f"DEBUG: set_my_commands failed: {e}")
        logger.error(f"Failed to set bot commands: {e}")

    logger.info("Telegram gateway starting polling...")
    print("DEBUG: starting polling...")
    try:
        await _bot.delete_webhook(drop_pending_updates=True)
        _polling_task = asyncio.create_task(_dp.start_polling(_bot))
        def _on_polling_done(task):
            try:
                task.result()
                print("DEBUG: polling task finished cleanly")
            except Exception as e:
                print(f"DEBUG: polling task crashed: {e}")
                logger.error(f"Polling task crashed: {e}", exc_info=True)
        _polling_task.add_done_callback(_on_polling_done)
        print("DEBUG: polling task created")
    except Exception as e:
        print(f"DEBUG: polling task creation failed: {e}")

async def stop_telegram_gateway():
    global _bot, _dp, _polling_task
    if _polling_task:
        _polling_task.cancel()
    if _dp:
        await _dp.stop_polling()
    if _bot:
        await _bot.session.close()
