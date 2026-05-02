from telegram import Bot
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ChatMemberHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Defaults,
    BaseHandler
)

from spreadsheetbot.sheets.i18n import I18n
from spreadsheetbot.sheets.switch import Switch
from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.registration import Registration
from spreadsheetbot.sheets.log import LogSheet
from spreadsheetbot.sheets.groups import Groups
from spreadsheetbot.sheets.users import Users
from spreadsheetbot.sheets.report import Report
from spreadsheetbot.sheets.keyboard import Keyboard
from spreadsheetbot.sheets.notifications import Notifications

from spreadsheetbot.basic.log import Log
from logging import INFO, DEBUG
Log.setLevel(INFO)

from spreadsheetbot.basic.scheldue import PerformAndScheldueNotifications
from spreadsheetbot.basic.handlers import ErrorHandlerFun, ChatMemberHandlerFun

UPDATE_GROUP_USER_REQUEST  = 0
UPDATE_GROUP_GROUP_REQUEST = 2
UPDATE_GROUP_CHAT_MEMBER   = 3

START_COMMAND  = 'start'
HELP_COMMAND   = 'help'
REPORT_COMMAND = 'report'

class SpreadSheetBot():
    def __init__(self, bot_token: str, sheets_secret: str, sheets_link: str, switch_update_time: int, setting_update_time: int):
        self.bot_token           = bot_token
        self.sheets_secret       = sheets_secret
        self.sheets_link         = sheets_link
        self.switch_update_time  = switch_update_time
        self.setting_update_time = setting_update_time

    async def post_init(self, app: Application) -> None:
        Switch.set_sleep_time(self.switch_update_time)
        Settings.set_sleep_time(self.setting_update_time)

        await I18n.async_init(self.sheets_secret, self.sheets_link)
        await LogSheet.async_init(self.sheets_secret, self.sheets_link)
        await Switch.async_init(self.sheets_secret, self.sheets_link)
        await Settings.async_init(self.sheets_secret, self.sheets_link)
        await Groups.async_init(self.sheets_secret, self.sheets_link)
        await Users.async_init(self.sheets_secret, self.sheets_link)
        await Registration.async_init(self.sheets_secret, self.sheets_link)
        await Report.async_init(self.sheets_secret, self.sheets_link)
        await Keyboard.async_init(self.sheets_secret, self.sheets_link)
        await Notifications.async_init(self.sheets_secret, self.sheets_link)

        bot: Bot = app.bot
        await bot.set_my_commands([(HELP_COMMAND, Settings.help_command_description)])
        
        my_name = await bot.get_my_name()
        if my_name.name != Settings.my_name:
            await bot.set_my_name(Settings.my_name)
        
        my_short_description = await bot.get_my_short_description()
        if my_short_description.short_description  != Settings.my_short_description:
            await bot.set_my_short_description(Settings.my_short_description)
        
        my_description = await bot.get_my_description()
        if my_description.description  != Settings.my_description:
            await bot.set_my_description(Settings.my_description)

        await LogSheet.write(None, "Started an application")

        Switch.scheldue_update(app)
        Settings.scheldue_update(app)
        Groups.scheldue_update(app)
        Users.scheldue_update(app)
        Registration.scheldue_update(app)
        Report.scheldue_update(app)
        Keyboard.scheldue_update(app)
        PerformAndScheldueNotifications(app)

    async def post_shutdown(self, app: Application) -> None:
        await LogSheet.write(None, "Stopped an application")

    def run_polling(self, defaults: Defaults = None, extra_user_handlers: list[BaseHandler] = None):
        Log.info("Starting...")
        app = ApplicationBuilder() \
            .token(self.bot_token) \
            .concurrent_updates(True) \
            .post_init(self.post_init) \
            .post_shutdown(self.post_shutdown) \
            .defaults(defaults) \
            .build()

        app.add_error_handler(ErrorHandlerFun)

        ##
        # Chat member handlers
        ##
        app.add_handler(
            ChatMemberHandler(ChatMemberHandlerFun, chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER, block=False),
            group=UPDATE_GROUP_CHAT_MEMBER
        )

        ##
        # Group handlers
        ##
        app.add_handler(
            CommandHandler(HELP_COMMAND, Groups.help_handler, filters=Groups.IsRegisteredFilter, block=False),
            group=UPDATE_GROUP_GROUP_REQUEST
        )

        app.add_handler(
            CommandHandler(REPORT_COMMAND, Groups.report_handler, filters=Groups.IsAdminFilter, block=False),
            group=UPDATE_GROUP_GROUP_REQUEST
        )

        ##
        # User handlers
        ##
        app.add_handler(
            MessageHandler(Users.IsRegistrationOverFilter, Users.registration_is_over_handler, block=False),
            group=UPDATE_GROUP_USER_REQUEST
        )

        app.add_handler(
            MessageHandler(Users.EditedMessageFilter, Users.edited_message_handler, block=False),
            group=UPDATE_GROUP_USER_REQUEST
        )

        app.add_handler(
            CommandHandler(START_COMMAND, Users.start_registration_handler, filters=Users.StartRegistrationFilter, block=False),
            group=UPDATE_GROUP_USER_REQUEST
        )

        app.add_handlers([
            CommandHandler(START_COMMAND, Users.restart_help_registration_handler, filters=Users.HasActiveRegistrationStateFilter, block=False),
            CommandHandler(HELP_COMMAND,  Users.restart_help_registration_handler, filters=Users.HasActiveRegistrationStateFilter, block=False),
            MessageHandler(Users.HasActiveRegistrationStateFilter, Users.proceed_registration_handler, block=False),
        ], group=UPDATE_GROUP_USER_REQUEST)
        
        app.add_handlers([
            CommandHandler(START_COMMAND, Users.restart_help_on_registration_complete_handler, filters=Users.HasNoRegistrationStateFilter, block=False),
            CommandHandler(HELP_COMMAND,  Users.restart_help_on_registration_complete_handler, filters=Users.HasNoRegistrationStateFilter, block=False),
        ], group=UPDATE_GROUP_USER_REQUEST)

        app.add_handler(MessageHandler(Users.KeyboardKeyInputFilter, Users.keyboard_key_handler, block=False), group=UPDATE_GROUP_USER_REQUEST)

        app.add_handlers([
            CallbackQueryHandler(Users.set_active_state_callback_handler,          pattern=Users.CALLBACK_USER_ACTIVE_STATE_PATTERN, block=False),
            CallbackQueryHandler(Users.change_state_callback_handler,              pattern=Users.CALLBACK_USER_CHANGE_STATE_PATTERN, block=False),
            CommandHandler(START_COMMAND, Users.restart_help_change_state_handler, filters=Users.HasChangeRegistrationStateFilter,   block=False),
            CommandHandler(HELP_COMMAND,  Users.restart_help_change_state_handler, filters=Users.HasChangeRegistrationStateFilter,   block=False),
            MessageHandler(Users.HasChangeRegistrationStateFilter, Users.change_state_reply_handler, block=False),
        ], group=UPDATE_GROUP_USER_REQUEST)

        app.add_handlers([
            CallbackQueryHandler(Users.notification_set_state_callback_handler,    pattern=Notifications.CALLBACK_SET_STATE_PATTERN,     block=False),
            CallbackQueryHandler(Users.notification_answer_callback_handler,       pattern=Notifications.CALLBACK_ANSWER_PATTERN,        block=False),
            CommandHandler(START_COMMAND, Users.restart_help_notification_handler, filters=Users.HasNotificationRegistrationStateFilter, block=False),
            CommandHandler(HELP_COMMAND,  Users.restart_help_notification_handler, filters=Users.HasNotificationRegistrationStateFilter, block=False),
            MessageHandler(Users.HasNotificationRegistrationStateFilter,           Users.notification_reply_handler,                     block=False),
        ], group=UPDATE_GROUP_USER_REQUEST)

        app.add_handlers([
            CallbackQueryHandler(Users.keyboard_set_state_callback_handler,    pattern=Keyboard.CALLBACK_SET_STATE_PATTERN,      block=False),
            CallbackQueryHandler(Users.keyboard_answer_callback_handler,       pattern=Keyboard.CALLBACK_ANSWER_PATTERN,         block=False),
            CommandHandler(START_COMMAND, Users.restart_help_keyboard_handler, filters=Users.HasKeyboardRegistrationStateFilter, block=False),
            CommandHandler(HELP_COMMAND,  Users.restart_help_keyboard_handler, filters=Users.HasKeyboardRegistrationStateFilter, block=False),
            MessageHandler(Users.HasKeyboardRegistrationStateFilter,           Users.keyboard_reply_handler,                     block=False),
        ], group=UPDATE_GROUP_USER_REQUEST)

        if extra_user_handlers:
            app.add_handlers(extra_user_handlers, group=UPDATE_GROUP_USER_REQUEST)
        
        app.add_handler(MessageHandler(Users.StrangeErrorFilter, Users.strange_error_handler, block=False), group=UPDATE_GROUP_USER_REQUEST)

        app.run_polling()
        Log.info("Done. Goodby!")