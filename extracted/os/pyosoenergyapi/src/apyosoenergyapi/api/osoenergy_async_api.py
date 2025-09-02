"""OSO Energy API Module."""

import operator
from typing import Optional
from numpy import number

import urllib3
from aiohttp import ClientResponse, ClientSession
from aiohttp.web_exceptions import HTTPError

from ..helper.const import HTTP_UNAUTHORIZED, HTTP_FORBIDDEN
from ..helper.osoenergy_exceptions import NoSubscriptionKey

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OSOEnergyApiAsync:
    """OSO Energy API Code."""

    def __init__(
            self,
            osoenergy_session=None,
            websession: Optional[ClientSession] = None):
        """Init the api."""
        self.base_url = "https://api.osoenergy.no/water-heater-api"
        self.urls = {
            "devices": self.base_url + "/1/Device/All",
            "turn_on": self.base_url + "/1/Device/{0}/TurnOn?fullUtilizationParam={1}",
            "turn_off": self.base_url + "/1/Device/{0}/TurnOff?fullUtilizationParam={1}",
            "profile": self.base_url + "/1/Device/{0}/Profile",
            "optimization_mode": self.base_url + "/1/Device/{0}/OptimizationMode",
            "set_v40_min": self.base_url + "/1/Device/{0}/V40Min/{1}",
            "enable_holiday_mode": self.base_url + "/1/Device/{0}/HolidayMode/{1}/{2}",
            "disable_holiday_mode": self.base_url + "/1/Device/{0}/HolidayMode",
            "user": self.base_url + "/1/User/Details"
        }
        self.headers = {
            "content-type": "application/json",
            "Accept": "*/*"
        }
        self.timeout = 10
        self.json_return = {
            "original": "No response to OSO Energy API request",
            "parsed": "No response to OSO Energy API request",
        }
        self.session = osoenergy_session
        self.websession = ClientSession() if websession is None else websession

    async def request(self, method: str, url: str, **kwargs) -> ClientResponse:
        """Make a request."""
        data = kwargs.get("data", None)

        if not self.session.subscription_key:
            raise NoSubscriptionKey

        self.headers.update(
            {"Ocp-Apim-Subscription-Key": self.session.subscription_key}
        )

        async with self.websession.request(
            method, url, headers=self.headers, data=data
        ) as resp:
            await resp.json(content_type=None)

            self.json_return.update({"original": resp.status})
            self.json_return.update({"parsed": await resp.json(content_type=None)})

        if operator.contains(str(resp.status), "20"):
            return True

        if resp.status == HTTP_UNAUTHORIZED:
            self.session.logger.error(
                f"Subscription key not authorized when calling {url} - "
                f"HTTP status is - {resp.status}"
            )
        elif resp.status == HTTP_FORBIDDEN:
            self.session.logger.error(
                f"Subscription key not authorized when calling {url} - "
                f"HTTP status is - {resp.status}"
            )
        elif url is not None and resp.status is not None:
            self.session.logger.error(
                f"Something has gone wrong calling {url} - "
                f"HTTP status is - {resp.status}"
            )

        return False

    async def get_user_details(self):
        """Get user details."""
        url = self.urls["user"]
        try:
            await self.request("get", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def get_devices(self):
        """Call the get devices endpoint."""
        url = self.urls["devices"]
        try:
            await self.request("get", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def turn_on(self, device_id: str, full_utilization: bool):
        """Call the get V40 Min endpoint."""
        url = self.urls["turn_on"].format(device_id, full_utilization)
        try:
            await self.request("post", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def turn_off(self, device_id: str, full_utilization: bool):
        """Call the get V40 Min endpoint."""
        url = self.urls["turn_off"].format(device_id, full_utilization)
        try:
            await self.request("post", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def set_profile(self, device_id: str, **kwargs):
        """Call the get V40 Min endpoint."""
        jsc = (
            "{"
            + ",".join(
                ('"' + str(i) + '": ' + str(t) for i, t in kwargs.items())
            )
            + "}"
        )

        url = self.urls["profile"].format(device_id)
        try:
            await self.request("put", url, data=jsc)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def set_optimization_mode(self, device_id: str, **kwargs):
        """Call the get V40 Min endpoint."""
        jsc = (
            "{"
            + ",".join(
                ('"' + str(i) + '": ' + str(t) + ' ' for i, t in kwargs.items())
            )
            + "}"
        )
        url = self.urls["optimization_mode"].format(device_id)
        try:
            await self.request("put", url, data=jsc)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def set_v40_min(self, device_id: str, v40_min: number):
        """Call the get V40 Min endpoint."""
        url = self.urls["set_v40_min"].format(device_id, v40_min)
        try:
            await self.request("put", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return

    async def enable_holiday_mode(self, device_id: str, start_date: str, end_date: str):
        """Enable holiday mode."""
        url = self.urls["enable_holiday_mode"].format(device_id, start_date, end_date)
        try:
            await self.request("post", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return
    
    async def disable_holiday_mode(self, device_id: str):
        """Disable holiday mode."""
        url = self.urls["disable_holiday_mode"].format(device_id)
        try:
            await self.request("delete", url)
        except (OSError, RuntimeError, ZeroDivisionError) as exception:
            raise HTTPError from exception

        return self.json_return