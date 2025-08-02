# arpakit

from __future__ import annotations

import asyncio
import datetime as dt
import logging
from typing import Any
from urllib.parse import urljoin

import cachetools
from aiohttp import ClientResponse
from pydantic import ConfigDict, BaseModel

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_http_request_util import async_make_http_request

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class Weekdays(Enumeration):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class Months(Enumeration):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)


class CurrentSemesterAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    value: str


class CurrentWeekAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    value: int


class GroupAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    uust_api_id: int
    title: str
    faculty: str | None
    course: int | None
    difference_level: int | None = None
    uust_api_data: dict[str, Any]


class TeacherAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    uust_api_id: int
    name: str | None
    surname: str | None
    patronymic: str | None
    fullname: str | None
    shortname: str | None
    posts: list[str]
    post: str | None
    units: list[str]
    unit: str | None
    difference_level: int | None
    uust_api_data: dict[str, Any]


class GroupLessonAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: dt.time | None
    time_end: dt.time | None
    numbers: list[int]
    location: str | None
    teacher_uust_api_id: int | None
    group_uust_api_id: int | None
    group: GroupAPIModel
    teacher: TeacherAPIModel | None
    uust_api_data: dict[str, Any]

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class TeacherLessonAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: dt.datetime
    entity_type: str
    actualization_dt: dt.datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: dt.time | None
    time_end: dt.time | None
    numbers: list[int]
    location: str | None
    group_uust_api_ids: list[int]
    teacher_uust_api_id: int
    teacher: TeacherAPIModel
    groups: list[GroupAPIModel]
    uust_api_data: dict[str, Any]

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class WeatherInUfaAPIModel(BaseAPIModel):
    temperature: float
    temperature_feels_like: float
    description: str
    wind_speed: float
    sunrise_dt: dt.datetime
    sunset_dt: dt.datetime
    has_rain: bool
    has_snow: bool
    data: dict


class DatetimeAPIModel(BaseAPIModel):
    date: dt.date
    datetime: dt.datetime | None = None
    year: int
    month: int
    day: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None
    microsecond: int | None = None


class ARPAKITScheduleUUSTAPIClient:
    def __init__(
            self,
            *,
            base_url: str = "https://api.schedule-uust.arpakit.com/api/v1",
            api_key: str | None = "viewer",
            use_cache: bool = False,
            cache_ttl: dt.timedelta | None = dt.timedelta(minutes=10)
    ):
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        base_url = base_url.strip()
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key is not None:
            self.headers.update({"apikey": self.api_key})
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        if cache_ttl is not None:
            self.ttl_cache = cachetools.TTLCache(maxsize=100, ttl=cache_ttl.total_seconds())
        else:
            self.ttl_cache = None

    async def _async_make_http_request(
            self,
            *,
            method: str = "GET",
            url: str,
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> ClientResponse:
        response = await async_make_http_request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            max_tries_=5,
            raise_for_status_=True,
            **kwargs
        )
        return response

    def clear_cache(self):
        if self.ttl_cache is not None:
            self.ttl_cache.clear()

    async def check_auth(self) -> dict[str, Any]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "check_auth")
        )
        json_data = await response.json()
        return json_data

    async def get_current_week(self) -> CurrentWeekAPIModel | None:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_current_week")
        )
        json_data = await response.json()
        if json_data is None:
            return None
        return CurrentWeekAPIModel.model_validate(json_data)

    async def get_current_semester(self) -> CurrentSemesterAPIModel | None:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_current_semester")
        )
        json_data = await response.json()
        if json_data is None:
            return None
        return CurrentSemesterAPIModel.model_validate(json_data)

    async def get_weather_in_ufa(self) -> WeatherInUfaAPIModel:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_weather_in_ufa")
        )
        json_data = await response.json()
        return WeatherInUfaAPIModel.model_validate(json_data)

    async def get_now_datetime_in_ufa(self) -> DatetimeAPIModel:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_now_datetime_in_ufa")
        )
        json_data = await response.json()
        return DatetimeAPIModel.model_validate(json_data)

    async def get_log_file_content(self) -> str | None:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_log_file")
        )
        text_data = await response.text()
        return text_data

    async def get_groups(self) -> list[GroupAPIModel]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_groups")
        )
        json_data = await response.json()
        return [GroupAPIModel.model_validate(d) for d in json_data]

    async def get_group(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> GroupAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_group"), params=params)
        json_data = await response.json()
        if json_data is None:
            return None
        return GroupAPIModel.model_validate(json_data)

    async def find_groups(
            self, *, q: str
    ) -> list[GroupAPIModel]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "find_groups"), params={"q": q.strip()}
        )
        json_data = await response.json()
        return [GroupAPIModel.model_validate(d) for d in json_data]

    async def get_teachers(self) -> list[TeacherAPIModel]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_teachers")
        )
        json_data = await response.json()
        return [TeacherAPIModel.model_validate(d) for d in json_data]

    async def get_teacher(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> TeacherAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_teacher"), params=params
        )
        json_data = await response.json()
        if json_data is None:
            return None
        return TeacherAPIModel.model_validate(json_data)

    async def find_teachers(
            self, *, q: str
    ) -> list[TeacherAPIModel]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "find_teachers"), params={"q": q.strip()}
        )
        json_data = await response.json()
        return [TeacherAPIModel.model_validate(d) for d in json_data]

    async def find_any(
            self, *, q: str
    ) -> list[TeacherAPIModel | GroupLessonAPIModel]:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "find_any"), params={"q": q.strip()}
        )
        json_data = await response.json()

        results = []
        for d in json_data:
            if d["entity_type"] == "group":
                results.append(GroupAPIModel.model_validate(d))
            elif d["entity_type"] == "teacher":
                results.append(TeacherAPIModel.model_validate(d))
            else:
                pass
        return results

    async def get_group_lessons(
            self,
            *,
            filter_group_id: int | None = None,
            filter_group_uust_api_id: int | None = None
    ) -> list[GroupLessonAPIModel]:
        params = {}
        if filter_group_id is not None:
            params["filter_group_id"] = filter_group_id
        if filter_group_uust_api_id is not None:
            params["filter_group_uust_api_id"] = filter_group_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_group_lessons"), params=params
        )
        json_data = await response.json()
        return [GroupLessonAPIModel.model_validate(d) for d in json_data]

    async def get_teacher_lessons(
            self,
            *,
            filter_teacher_id: int | None = None,
            filter_teacher_uust_api_id: int | None = None
    ) -> list[TeacherLessonAPIModel]:
        params = {}
        if filter_teacher_id is not None:
            params["filter_teacher_id"] = filter_teacher_id
        if filter_teacher_uust_api_id is not None:
            params["filter_teacher_uust_api_id"] = filter_teacher_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_teacher_lessons"), params=params
        )
        json_data = await response.json()
        return [TeacherLessonAPIModel.model_validate(d) for d in json_data]


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
