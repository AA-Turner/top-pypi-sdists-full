import pandas as pd
from spreadsheetbot.sheets.abstract import AbstractSheetAdapter

from telegram import Message, Update, Chat
from telegram.ext import Application, ContextTypes

from spreadsheetbot.sheets.i18n import I18n
from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.report import Report

class GroupsAdapterClass(AbstractSheetAdapter):
    def __init__(self) -> None:
        super().__init__('groups', 'groups', initialize_as_df=True)
        self.GroupChatFilter    = self.GroupChatClass(outer_obj=self)
        self.IsRegisteredFilter = self.GroupChatFilter & self.IsRegisteredClass(outer_obj=self)
        self.IsAdminFilter      = self.GroupChatFilter & self.IsAdminClass(outer_obj=self)

        self.uid_col = 'chat_id'
    
    async def _pre_async_init(self):
        self.sheet_name = I18n.groups
        self.update_sleep_time = Settings.groups_update_time
        self.retry_sleep_time  = self.update_sleep_time // 2
    
    async def _get_df(self) -> pd.DataFrame:
        df = pd.DataFrame(await self.wks.get_all_records())
        df = df.drop(index = 0, axis = 0)
        df = df.loc[
            (df.chat_id != "") &
            (df.is_admin.isin(I18n.yes_no_super)) &
            (df.is_active == I18n.yes)
        ]
        df.chat_id = df.chat_id.apply(str)
        return df
    
    def send_to_all_normal_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None):
        self._send_to_all_uids(
            self.as_df.is_admin == I18n.no,
            app, message, parse_mode, send_photo
        )
    
    def send_to_all_admin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None):
        self._send_to_all_uids(
            self.as_df.is_admin.isin(I18n.yes_super),
            app, message, parse_mode, send_photo
        )
    
    def send_to_all_superadmin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None):
        self._send_to_all_uids(
            self.as_df.is_admin == I18n.super,
            app, message, parse_mode, send_photo
        )
    
    async def async_send_to_all_superadmin_groups(self, app: Application, message: str, parse_mode: str, send_photo: str = None):
        for send_message_continue in self._get_send_to_all_uids_coroutines(
            self.as_df.is_admin == I18n.super,
            app, message, parse_mode, send_photo
        ):
            await send_message_continue
    
    class GroupChatClass(AbstractSheetAdapter.AbstractFilter):
        def filter(self, message: Message) -> bool:
            return message.chat.type in [Chat.GROUP, Chat.SUPERGROUP, Chat.CHANNEL]
    
    class IsRegisteredClass(AbstractSheetAdapter.AbstractFilter):
        def filter(self, message: Message) -> bool:
            return self.outer_obj.exists(message.chat_id)
    
    class IsAdminClass(AbstractSheetAdapter.AbstractFilter):
        def filter(self, message: Message) -> bool:
            df = self.outer_obj.as_df
            return not df.loc[
                self.outer_obj.selector(message.chat_id) &
                (df.is_admin.isin(I18n.yes_super))
            ].empty
    
    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        group = self.as_df.loc[self.selector(update.effective_chat.id)].iloc[0]
        reply = Settings.help_admin_group if group.is_admin else Settings.help_normal_group
        await update.message.reply_markdown(reply)
    
    async def report_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_markdown(Report.markdown)

Groups = GroupsAdapterClass()
