from typing import Coroutine, Any
from telegram import Bot
from telegram.ext import Application
import asyncio
import gspread_asyncio
from gspread import utils
import pandas as pd

from telegram import (
    InlineKeyboardMarkup,
    Document
)
from telegram.ext.filters import MessageFilter

from google.oauth2.service_account import Credentials 

from spreadsheetbot.basic.drive import SaveToDrive
from spreadsheetbot.basic.log import Log

class AbstractSheetAdapter():
    def __init__(self, sheet_name: str, name: str, update_sleep_time: int = None, retry_sleep_time: int = None, initialize_as_df: bool = False) -> None:
        self.sheet_name = sheet_name
        self.name = name
        self.update_sleep_time = update_sleep_time if update_sleep_time is not None else 3600
        self.retry_sleep_time = retry_sleep_time if retry_sleep_time is not None else update_sleep_time
        self.initialize_as_df = initialize_as_df

        self.wks_row_pad = 1
        self.wks_col_pad = 1
        self.uid_col     = 'uid'
        
        self.wks_row  = lambda uid: self.as_df.loc[self.selector(uid)].index.values[0] + self.wks_row_pad
        self.wks_col  = lambda key: self.as_df.columns.get_loc(key) + self.wks_col_pad
        self.selector = lambda uid: (self.as_df[self.uid_col] == str(uid))
        self.exists   = lambda uid: not self.as_df.loc[self.selector(uid)].empty

        self.mutex = []
        self.whole_mutex = False
    
    def set_sleep_time(self, update_sleep_time: int = None, retry_sleep_time: int = None):
        self.update_sleep_time = update_sleep_time if update_sleep_time is not None else 3600
        self.retry_sleep_time = retry_sleep_time if retry_sleep_time is not None else update_sleep_time
    
    async def async_init(self, sheets_secret: str, sheets_link: str):
        self.sheets_secret = sheets_secret
        self.agcm = gspread_asyncio.AsyncioGspreadClientManager(self.get_creds)
        self.sheets_link = sheets_link

        await self._pre_async_init()
        await self._connect()
        if self.initialize_as_df:
            self.as_df = await self._get_df()
            Log.info(f"Initialized {self.name} as df")
            Log.debug(f"\n\n{self.as_df}\n\n")
        else:
            self.as_df = None
            Log.info(f"Initialized {self.name} as sheet")
        await self._post_async_init()
    
    def get_creds(self):
        creds = Credentials.from_service_account_info(self.sheets_secret)
        scoped = creds.with_scopes([
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])
        return scoped
    
    async def _connect(self):
        self.agc = await self.agcm.authorize()
        self.sh = await self.agc.open_by_url(self.sheets_link)
        self.wks = await self.sh.worksheet(self.sheet_name)
        Log.debug(f"(Re) Connected to {self.name} sheet")
    
    async def _pre_async_init(self):
        pass
    
    async def _post_async_init(self):
        await self._process_df_update()

    async def _get_df(self) -> pd.DataFrame:
        pass

    def _create_update_context(self, action, **kwargs) -> dict:
        return {
            'action': action,
            'name': self.name,
        } | kwargs
    
    def scheldue_update(self, app: Application) -> None:
        app.create_task(self._update(app), self._create_update_context('Whole df update'))
    
    async def _update_df(self) -> None:
        await self._connect()
        self.as_df = await self._get_df()
    
    async def _update(self, app: Application) -> None:
        await self._pre_update()
        await asyncio.sleep(self.update_sleep_time)
        
        Log.info(f"Prepared to update whole df {self.name}")
        while len(self.mutex) > 0:
            Log.info(f"Halted whole df update at {self.name} with mutex {self.mutex}")
            await asyncio.sleep(self.retry_sleep_time)
        self.scheldue_update(app)
        
        self.whole_mutex = True
        await self._update_df()
        self.whole_mutex = False

        Log.info(f"Updated whole df {self.name}")
        Log.debug(f"\n\n{self.as_df}\n\n")
        await self._post_update()
    
    async def _pre_update(self):
        pass

    async def _post_update(self):
        await self._process_df_update()
    
    async def _process_df_update(self):
        pass
    
    async def _next_available_row(self) -> int:
        str_list = list(filter(None, await self.wks.col_values(1)))
        return len(str_list)+1
    
    async def _find_col_by_data(self, data) -> int:
        cell = await self.wks.find(data)
        return cell.col
    
    def _prepare_batch_update(self, rowcols: list[tuple[str|int]]) -> list[str]:
        return [{
            'range': utils.rowcol_to_a1(x[0], x[1]),
            'values': [[x[2]]],
        } for x in rowcols ]
    
    async def _update_record(self, uid: str|int, key: str, value: str):
        selector = self.selector(uid)
        if self.as_df.loc[selector].empty:
            return
        self.as_df.loc[selector, key] = value
        wks_row = self.wks_row(uid)
        wks_col = self.wks_col(key)
        
        Log.info(f"Prepeared to update single record in {self.name} with {self.uid_col} {uid} write to {key} collumn")
        while self.whole_mutex:
            Log.info(f"Halted single update record in {self.name} with {self.uid_col} {uid} write to {key} collumn with whole mutex")
            await asyncio.sleep(self.retry_sleep_time)
        
        self.mutex.append(uid)
        await self.wks.update_cell(wks_row, wks_col, value)
        del self.mutex[self.mutex.index(uid)]
        
        Log.info(f"Done update single record in {self.name} with {self.uid_col} {uid} write to {key} collumn")
        Log.debug(f"Current mutext at {self.name} is {self.mutex}")
    
    async def _batch_update_or_create_record(self, uid: str|int, save_to = None, save_as = None, app: Application = None, raw: bool = True, **record_params):
        exists = self.exists(uid)
        record_action = 'update' if exists else 'create'
        collumns = record_params.keys()
        
        Log.info(f"Prepeared to batch update {record_action} record in {self.name} with {self.uid_col} {uid} and {collumns} collumns")
        while self.whole_mutex:
            Log.info(f"Halted to batch update {record_action} record in {self.name} with {self.uid_col} {uid} and {collumns} collumns with whole mutex")
            await asyncio.sleep(self.retry_sleep_time)
        self.mutex.append(uid)

        get_file = None
        for key,val in record_params.items():
            if type(val) in [list, tuple]:
                record_params[key] = val[-1].to_json()
                get_file = val[-1].get_file
            if type(val) == Document:
                record_params[key] = val.to_json()
                get_file = val.get_file
        
        if not exists:
            record_params[self.uid_col] = str(uid)
            tmp_df = pd.DataFrame(record_params, columns=self.as_df.columns, index=[0]).fillna('')
            if self.as_df.empty:
                self.as_df = tmp_df
            else:
                self.as_df = pd.concat([self.as_df, tmp_df], ignore_index=True)
        else:
            for key, value in record_params.items():
                self.as_df.loc[self.selector(uid), key] = value

        wks_row = self.wks_row(uid)
        wks_update = self._prepare_batch_update([
            (wks_row, self.wks_col(key), value)
            for key, value in record_params.items()
        ])
        
        await self.wks.batch_update(wks_update, raw)
        if get_file != None and save_to != None and save_as != None and app != None:
            app.create_task(
                SaveToDrive(self.agc.gc.auth.token, save_to, save_as, get_file),
                self._create_update_context('Save to drive', save_to=save_to, save_as=save_as)
            )
        
        del self.mutex[self.mutex.index(uid)]
        Log.info(f"Done batch update {record_action} record in {self.name} with {self.uid_col} {uid} and {collumns} collumns")
        Log.debug(f"Current mutext at {self.name} is {self.mutex}")
    
    def _get(self, selector, iloc = 0) -> pd.Series:
        row = self.as_df.loc[selector]
        if row.empty:
            return None
        return row.iloc[iloc]
    

    def _get_send_to_all_uids_coroutines(self, selector, app: Application, message: str, parse_mode: str, 
        send_photo: str = None, reply_markup: InlineKeyboardMarkup = None
    ) -> list[Coroutine[Any, Any, Any]]:
        bot: Bot = app.bot
        if send_photo not in [None, '']:
            return [
                bot.send_photo(chat_id=uid, photo=send_photo, caption=message, parse_mode=parse_mode, reply_markup=reply_markup)
                for uid in self.as_df.loc[selector][self.uid_col].to_list()
            ]
        return [
            bot.send_message(chat_id=uid, text=message, parse_mode=parse_mode, reply_markup=reply_markup)
            for uid in self.as_df.loc[selector][self.uid_col].to_list()
        ]

    def _send_to_all_uids(self, selector, app: Application, message: str, parse_mode: str, 
        send_photo: str = None, reply_markup: InlineKeyboardMarkup = None
    ):
        update = self._create_update_context(
            'Send to all uids',
            message=message,
            parse_mode=parse_mode,
            send_photo=send_photo,
            reply_markup=reply_markup.to_dict() if reply_markup else reply_markup
        )
        for send_message in self._get_send_to_all_uids_coroutines(selector, app, message, parse_mode, send_photo, reply_markup):
            app.create_task(send_message, update)
    
    class AbstractFilter(MessageFilter):
        def __init__(self, name: str = None, data_filter: bool = False, outer_obj = None):
            super().__init__(name, data_filter)
            self.outer_obj = outer_obj