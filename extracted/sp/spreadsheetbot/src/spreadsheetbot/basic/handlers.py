import traceback
import html
import json

from telegram import Bot, Update, Chat
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.log import LogSheet
from spreadsheetbot.sheets.groups import Groups
from spreadsheetbot.sheets.users import Users

from spreadsheetbot.basic.log import Log
from spreadsheetbot.basic.errors import BotShouldBeInactive

async def ErrorHandlerFun(update: Update|dict, context: ContextTypes.DEFAULT_TYPE) -> None:
    if type(context.error) == BotShouldBeInactive:
        Log.error(msg="Exception Bot should be inactive", exc_info=context.error)
        exit(1)
    
    if isinstance(update, Update):
        bot: Bot = context.bot
        await bot.send_message(update.effective_chat.id, Settings.error_reply, parse_mode=ParseMode.MARKDOWN)

    Log.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else update if isinstance(update, dict) else str(update)
    messages_parts = [
        f"An exception was raised while handling an update",
        f"update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}",
        f"context.chat_data = {html.escape(str(context.chat_data))}",
        f"context.user_data = {html.escape(str(context.user_data))}",
        f"{html.escape(tb_string)}",
    ]
    messages = []
    for idx,message_part in enumerate(messages_parts):
        curr_len = len(message_part)
        template = "<pre>{message_part}</pre>\n\n" if idx > 0 else "{message_part}\n"
        if len(messages) > 0 and (len(messages[-1]) + curr_len <= 4096):
            messages[-1] += template.format(message_part=message_part)
        elif curr_len <= 4096:
            messages.append(template.format(message_part=message_part))
        else:
            for idx in range(0,curr_len,4096):
                messages.append(template.format(message_part=message_part[idx:idx+4096]))

    for message in messages:
        await Groups.async_send_to_all_superadmin_groups(context.application, message,  ParseMode.HTML)

async def ChatMemberHandlerFun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    Log.debug(f"Chat member event \n{update.my_chat_member}\n")
    if update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP, Chat.CHANNEL]:
        Log.info((
            f"{update.my_chat_member.new_chat_member['status'].title()} event in "
            f"{update.effective_chat.type} with title {update.effective_chat.title} id {update.effective_chat.id}"
        ))
        
        await LogSheet.write(update.effective_chat.id,(
            f"{update.my_chat_member.new_chat_member['status'].title()} {update.effective_chat.type} "
            f"with title {update.effective_chat.title}"
        ))
        return
    
    elif update.effective_chat.type == Chat.PRIVATE:
        if update.my_chat_member.new_chat_member['status'] == update.my_chat_member.new_chat_member.BANNED:
            await Users.banned(update.effective_chat.id)
            Log.info(f"I was banned by private user {update.effective_chat.id}")
            await LogSheet.write(update.effective_chat.id, "Banned by private user")
            return
        
        elif update.my_chat_member.new_chat_member['status'] == update.my_chat_member.new_chat_member.MEMBER:
            await Users.unbanned(update.effective_chat.id)
            Log.info(f"I was unbanned by private user {update.effective_chat.id}")
            await LogSheet.write(update.effective_chat.id, "Unbanned by private user")
            return
    Log.info(f"Other chat member event in {update.effective_chat.type} {update.effective_chat.id}")
