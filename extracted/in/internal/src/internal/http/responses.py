import json
import arrow

from datetime import datetime, date

import httpx

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from beanie import Document, Link
from ..const import ARR_HUMAN_READ_FMT, ARR_DATE_FMT


async def async_response(data=None, message=None, code=None, page_no=None, total_num=None, page_size=None,
                         time_zone="UTC", time_format=ARR_HUMAN_READ_FMT, date_format=ARR_DATE_FMT,
                         status_code=status.HTTP_200_OK):
    def _serialize(data):
        if issubclass(type(data), Document):
            link_field_list = []
            datetime_field_list = []
            date_field_list = []
            for field_name in data.__annotations__:
                field_type = getattr(data, field_name)
                if isinstance(field_type, Link):
                    link_field_list.append(field_name)

                if isinstance(field_type, datetime):
                    datetime_field_list.append(field_name)
                elif isinstance(field_type, date):
                    date_field_list.append(field_name)

            data = json.loads(data.model_dump_json(exclude={"password", "metadata", "otp_code_universal"}, by_alias=False))
            if link_field_list:
                for field_name in link_field_list:
                    if isinstance(data[field_name], dict) and "id" in data[field_name].keys():
                        data[field_name] = data[field_name]["id"]
            for field_name in datetime_field_list:
                if data[field_name]:
                    data[field_name] = arrow.get(data[field_name]).to(time_zone).format(time_format)
            for field_name in date_field_list:
                if data[field_name]:
                    data[field_name] = arrow.get(data[field_name]).to(time_zone).format(date_format)

            if "create_time" in data.keys() and data.get("create_time"):
                data["create_time"] = arrow.get(data["create_time"]).to(time_zone).format(ARR_HUMAN_READ_FMT)

            if "update_time" in data.keys() and data.get("update_time"):
                data["update_time"] = arrow.get(data["update_time"]).to(time_zone).format(ARR_HUMAN_READ_FMT)

        return data

    if isinstance(data, httpx.Response):
        return JSONResponse(status_code=data.status_code, content=data.json())

    ret = {}
    if isinstance(data, list):
        data = [_serialize(d) for d in data]
    else:
        data = _serialize(data)

    data = jsonable_encoder(data)

    ret['code'] = code or "ok"

    ret['message'] = message or "success"

    if page_no and page_size:
        ret['data'] = {
            'page_no': page_no,
            'page_size': page_size,
            'total_num': total_num,
            'page_data': data
        }
    else:
        ret['data'] = data

    return JSONResponse(status_code=status_code, content=ret)
