from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import pandas as pd
from spreadsheetbot.sheets.abstract import AbstractSheetAdapter

from spreadsheetbot.basic.log import Log

class ReplySheet(AbstractSheetAdapter):
    def __init__(self, sheet_name: str, name: str, update_sleep_time: int = None, retry_sleep_time: int = None, initialize_as_df: bool = False) -> None:
        super().__init__(sheet_name, name, update_sleep_time, retry_sleep_time, initialize_as_df)

        self.reply_state_get_df_condition = lambda df: (
            (
                (df.state == "")
            ) | (
                (df.state != "") &
                (df.button_text.apply(lambda x: len(x))   == 1) &
                (df.button_answer.apply(lambda x: len(x)) == 2)
            ) | (
                (df.state != "") &
                (df.button_text.apply(lambda x: len(x)) == df.button_answer.apply(lambda x: len(x)))
            )
        )
    
    def reply_buttons_split(self, df) -> pd.DataFrame:
        df.button_text   = df.button_text.apply(lambda x: x.split('\n'))
        df.button_answer = df.button_answer.apply(lambda x: x.split('\n'))
        return df
    
    async def _process_df_update(self):
        self.states = self.as_df[self.as_df.state.str.len() > 0].state.values
    
    def get_by_state(self, state: str) -> pd.Series:
        return self._get(self.as_df.state == state)
    
    def get_text_markdown_by_state(self, state: str) -> str:
        return self.get_by_state(state).text_markdown
    
    def get_button_answer_by_state(self, state: str, answer_idx: int = None) -> str|tuple[str,str]:
        row = self.get_by_state(state)
        if len(row.button_text) == 1:
            return row.button_answer[0]
        if len(row.button_text) > 1 and answer_idx in range(len(row.button_text)):
            return row.button_answer[answer_idx], row.button_text[answer_idx]
        return None

    def get_inline_keyboard_by_state(self, state: str) -> InlineKeyboardMarkup|None:
        if state in [None, '']:
            Log.info('There is no state so there is no buttons')
            return None
        button_text = self.get_by_state(state).button_text
        if len(button_text) == 1:
            return InlineKeyboardMarkup([
                [InlineKeyboardButton(button_text[0],
                    callback_data=self.CALLBACK_SET_STATE_TEMPLATE.format(state=state)
                )]
            ])
        if len(button_text) > 1:
            return InlineKeyboardMarkup([
                [InlineKeyboardButton(button_text[idx],
                    callback_data=self.CALLBACK_ANSWER_TEMPLATE.format(state=state, answer=idx)
                )]
                for idx in range(len(button_text))
            ])
        return None