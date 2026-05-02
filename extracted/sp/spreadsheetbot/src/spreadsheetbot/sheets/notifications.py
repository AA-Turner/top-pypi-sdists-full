import pandas as pd
from spreadsheetbot.sheets.replysheet import ReplySheet

from spreadsheetbot.sheets.i18n import I18n
from spreadsheetbot.sheets.settings import Settings

from datetime import datetime

class NotificationsAdapterClass(ReplySheet):
    CALLBACK_SET_STATE_PREFIX   = 'notif_state_'
    CALLBACK_SET_STATE_TEMPLATE = 'notif_state_{state}'
    CALLBACK_SET_STATE_PATTERN  = 'notif_state_*'

    CALLBACK_ANSWER_PREFIX    = 'notif_answer_'
    CALLBACK_ANSWER_TEMPLATE  = 'notif_answer_{state}_{answer}'
    CALLBACK_ANSWER_PATTERN   = 'notif_answer_*'
    CALLBACK_ANSWER_SEPARATOR = '_'

    def __init__(self) -> None:
        super().__init__('notifications', 'notifications', initialize_as_df=True)

        self.selector_to_plan = lambda: self.as_df.is_active == I18n.yes
        self.selector_planned = lambda: (
            (self.as_df.is_active == I18n.planned) &
            (self.as_df.scheldue_date <= datetime.now())
        )
        self.wks_row_pad = 2
        self.selector = lambda idx: self.as_df.index == idx
    
    async def _pre_async_init(self):
        self.sheet_name = I18n.notifications
        self.update_sleep_time = Settings.notifications_update_time
        self.retry_sleep_time  = self.update_sleep_time // 2
    
    async def _get_df(self) -> pd.DataFrame:
        df = pd.DataFrame(await self.wks.get_all_records())
        df = df.drop(index = 0, axis = 0)
        df = self.reply_buttons_split(df)
        df = df.loc[
            (df.scheldue_date != "") &
            (df.is_active.isin(I18n.yes_no_planned_done)) &
            (df.text_markdown != "") &
            self.reply_state_get_df_condition(df)
        ]
        df.scheldue_date = df.scheldue_date.apply(lambda s: datetime.strptime(str(s), "%d.%m.%Y %H:%M"))
        return df
    
    def iterate_over_notifications_to_plan(self) -> list[tuple[int,pd.Series]]:
        return self.as_df.loc[self.selector_to_plan()].iterrows()
    
    def iterate_over_planned_notifications(self) -> list[tuple[int,pd.Series]]:
        return self.as_df.loc[self.selector_planned()].iterrows()
    
    async def set_planned(self, idx: int|str):
        await self._update_record(idx, 'is_active', I18n.planned)
    
    async def set_done(self, idx: int|str):
        await self._update_record(idx, 'is_active', I18n.done)

Notifications = NotificationsAdapterClass()
