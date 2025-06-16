import arrow
from datetime import datetime
from typing import Optional, Dict

import dictdiffer
from pydantic import BaseModel


class Operate(BaseModel):
    add: Optional[dict] = None
    remove: Optional[dict] = None
    change: Optional[dict] = None

    @classmethod
    async def generate_operate(cls, original: dict = None, compare: dict = None):
        if original:
            original = await cls.remove_ignore_field(original)
            await cls.convert_datetime_timezone_utc_field(original)
        else:
            original = {}

        if compare:
            compare = await cls.remove_ignore_field(compare)
            await cls.convert_datetime_timezone_utc_field(compare)
        else:
            compare = {}

        diff_result = {'add': {}, 'remove': {}, 'change': {}}
        for diff in list(dictdiffer.diff(original, compare)):
            diff = (list(diff))
            if diff[0] == 'add' or diff[0] == 'remove':
                diff[2] = list(diff[2])
                for j in range(0, len(diff[2])):
                    diff[2][j] = list(diff[2][j])
            if diff[1] == 'change':
                diff[2] = list(diff[2])

            if diff[0] == 'change':
                temp_key = diff[1]
                if type(diff[1]) == list:
                    temp_key = "_".join([str(temp_x) for temp_x in list(diff[1])])
                diff_result['change'][temp_key] = {'orig': diff[2][0], 'new': diff[2][1]}

            if diff[0] == 'add' or diff[0] == 'remove':
                for j in range(0, len(diff[2])):
                    if str(diff[2][j][0]).isdigit():
                        diff_result[diff[0]][f"{diff[1]}_{diff[2][j][0]}"] = diff[2][j][1]
                    else:
                        diff_result[diff[0]][diff[2][j][0]] = diff[2][j][1]

        final_diff_result = cls.split_keys(diff_result)
        return Operate(**final_diff_result)

    @classmethod
    async def remove_ignore_field(cls, model_dict: dict):
        return {k: v for k, v in model_dict.items() if k not in ['create_time', 'update_time']}

    @classmethod
    async def convert_datetime_timezone_utc_field(cls, model_dict: dict):
        # 統一使用arrow.get取代datetime，使其包含tzinfo，避免diff因時區有無判斷錯誤
        for k, v in model_dict.items():
            if isinstance(v, datetime):
                model_dict[k] = arrow.get(v).datetime

    @classmethod
    def split_keys(cls, diff_result: Dict):
        result = {}
        for key, value in diff_result.items():
            key = str(key)
            if '.' in key:
                parts = key.split('.')
                current_level = result
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:
                        current_level[part] = cls.split_keys(value) if isinstance(value, dict) else value
                    else:
                        if part not in current_level:
                            current_level[part] = {}
                        current_level = current_level[part]
            else:
                result[key] = cls.split_keys(value) if isinstance(value, dict) else value
        return result
