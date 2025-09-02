"""An API library for Efergy energy meters."""

# pylint: disable=too-many-arguments, too-many-public-methods
from __future__ import annotations

from asyncio.exceptions import TimeoutError as timeouterr
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import logging
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectorError, ServerDisconnectedError
import iso4217

from . import exceptions

CACHETTL = "cachettl"
COST = "cost"
CURRENCY = "currency"
DATA = "data"
DEFAULT_PERIOD = "month"
DEFAULT_TYPE = "kwh"
DESC = "description"
ERROR = "error"
HID = "hid"
ID = "id"
INSTANT = "instant_readings"
LISTOFMACS = "listOfMacs"
MAC = "mac"
MORE = "more"
SID = "sid"
STATUS = "status"
SUM = "sum"
TYPE = "type"
UTC_OFFSET = "utc_offset"
VERSION = "version"

_ALTERNATE_RES = "https://www.energyhive.com/mobile_proxy"
_RES = "https://engage.efergy.com/mobile_proxy"

_LOGGER = logging.getLogger(__name__)

TIMEOUT = 10


class Efergy:  # pylint:disable=too-many-instance-attributes
    """Implementation of Efergy object."""

    _close_session = False
    _from_aenter = False

    def __init__(
        self,
        api_key: str,
        session: ClientSession | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize.

        utc_offset may be a string of 4 digits to represent the offset from UTC
        (ex. 0400) HH:MM or a TZ database name:
        https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

        Set alt to true to use the alternate API endpoint.
        """
        if session is None:
            session = ClientSession()
            self._close_session = True
        self._session = session
        self.info: dict[str, str] = {}
        self.sids: list[int] = []
        self._utc_offset = 0
        self._cachettl = 60
        self.update_params(api_key=api_key, **kwargs)

    async def __aenter__(self) -> Efergy:
        """Async enter."""
        self._from_aenter = True
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        if self._session and self._close_session:
            await self._session.close()

    def api_url(self, command: str) -> str:
        """Return the generated base URL based on host configuration."""
        return f"{self._url}/{command}?token={self._api_key}&offset={self._utc_offset}"

    def update_params(
        self,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Update API key and UTC offset.

        kwargs can include:
        cachettl: int, alt: bool, utc_offset, and currency: ISO 4217 code.
        """
        if api_key:
            self._api_key = api_key
        self._url = _ALTERNATE_RES if "alt" in kwargs else _RES
        self._cachettl = kwargs.get(CACHETTL, self._cachettl)
        if CURRENCY in kwargs:
            for cty in list(iso4217.raw_table.values()):
                if kwargs[CURRENCY] == cty["Ccy"]:
                    self.info[CURRENCY] = kwargs[CURRENCY]
                    break
            if CURRENCY not in self.info:
                raise exceptions.InvalidCurrency("Provided currency is invalid")
        if (offset := kwargs.get(UTC_OFFSET, "")) and offset.isnumeric():
            self._utc_offset = offset
            return
        try:
            z_info = ZoneInfo(offset)
        except ZoneInfoNotFoundError as ex:
            raise exceptions.InvalidOffset("Provided offset is invalid") from ex
        utc_offset = cast(timedelta, z_info.utcoffset(datetime.now())).total_seconds()
        self._utc_offset = -int(utc_offset // 60)

    async def _async_req(
        self, command: str, params: dict[str, str | int | float] | None = None
    ) -> Any:
        """Send get request."""
        _data = None
        try:
            _response = await self._session.request(
                method="GET",
                url=self.api_url(command),
                params=params,
                timeout=ClientTimeout(TIMEOUT),
            )
            _data = await _response.json(content_type="text/html")
        except (timeouterr, ClientConnectorError, ServerDisconnectedError) as ex:
            raise exceptions.ConnectError() from ex
        if _response.status == 200 and _data is None:
            return {}
        if DESC in _data and _data[DESC] == "bad token":
            raise exceptions.InvalidAuth("Provided API token is invalid.")
        if "desc" in _data and _data["desc"] == "Method call failed":
            raise exceptions.ServiceError(
                "Error communicating with sensor/hub. Check connections"
            )
        if ERROR in _data and _data[ERROR][ID] == 400:
            if "period" in _data[ERROR][MORE]:
                raise exceptions.InvalidPeriod(
                    "Provided period is invalid. Options are: day, week, month, year"
                )
            raise exceptions.DataError(_data)
        if ERROR in _data and _data[ERROR][ID] == 404:
            raise exceptions.APICallLimit(
                "API key has reached calls per day allowed limit"
            )
        if ERROR in _data and _data[ERROR][ID] == 500:
            raise exceptions.ServiceError(
                "Error communicating with sensor/hub. Check connections"
            )
        return _data

    async def async_get_sids(self) -> None:
        """Get current values sids."""
        sids = []
        for sid in await self._async_req("getCurrentValuesSummary"):
            sids.append(int(sid[SID]))
        self.sids = sids

    async def async_get_reading(
        self,
        reading_type: str,
        period: str | None = DEFAULT_PERIOD,
        sid: int | None = None,
    ) -> str | int | float | dict[str, int]:
        """Get reading for instant, budget, or summary.

        'reading_type' can be any of the following:
        instant: Current Watt usage.
        energy: kWh of energy used during specified period.
        cost: Cost of energy used during specified period.
        budget: Currently set budget and status of that budget.
        current_values: Values for each sensor attached to the account.

        The API treats monthly data as 28 days as months vary in the number of days.
        'reading type' for energy and cost may include
        extra characters for easier keying by period.
        """
        type_str = None
        params: dict = {}
        if reading_type == INSTANT:
            command = "getInstant"
            type_str = "reading"
        elif "energy" in reading_type:
            command = "getEnergy"
            params["period"] = period
            type_str = SUM
        elif COST in reading_type:
            command = "getCost"
            params["period"] = period
            type_str = SUM
        elif reading_type == "budget":
            command = "getBudget"
            type_str = STATUS
        elif reading_type == "current_values":
            command = "getCurrentValuesSummary"
        _data = await self._async_req(command, params=params)
        if (
            CURRENCY in self.info
            and COST in reading_type
            and self.info[CURRENCY] != _data["units"]
        ):
            _LOGGER.debug(
                "Currency provided does not match device settings. "
                "This can affect energy cost statistics"
            )
        if type_str:
            return _data[type_str]
        _readings = {}
        for sensor in _data:
            if sid == int(sensor[SID]):
                return list(sensor[DATA][0].values())[0]
            _readings[sensor[SID]] = list(sensor[DATA][0].values())[0]
        return _readings

    async def async_hid_simple_tarrif(self, cost: str | int) -> dict:
        """Create and Apply tariff. Only requires a pence per kWh value."""
        return await self._async_req(
            "createHidSimpleTariff", params={"cost_per_kwh": cost}
        )

    async def async_carbon(
        self,
        period: str = DEFAULT_PERIOD,
        fromtime: int = 0,
        totime: int = 0,
    ) -> dict[str, str | int]:
        """Get amount of carbon generated by the energy production to meet the usage.

        of the household over a given period.
        By default the usage so far "this month" is returned.
        """
        params: dict = {
            "period": period,
            "fromTime": fromtime,
            "toTime": totime,
        }
        return await self._async_req("getCarbon", params=params)

    async def async_channel_aggregated(
        self,
        fromtime: str | int | None = None,
        totime: str | int | None = None,
        aggperiod: str = DEFAULT_PERIOD,
        type_str: str | None = None,
        aggfunc: str = SUM,
        cachekey: str | None = None,
    ) -> dict[str, str | list[dict[str, str | list[dict[str, Any]]]]]:
        """Return timeseries of aggregated devices on a given channel for an hid."""
        params: dict = {
            "fromTime": fromtime,
            "toTime": totime,
            "aggPeriod": aggperiod,
            "cacheTTL": self._cachettl,
            "type": type_str,
            "aggFunc": aggfunc,
            "cacheKey": cachekey,
        }
        return await self._async_req("getChannelAggregated", params=params)

    async def async_comp_combined(self) -> dict[str, dict[str, dict[str, float]]]:
        """Retrieve comparison data between a given household and all other households.

        for day, week and month. The comparisons are also available elsewhere separately
        (getCompDay etc.)
        """
        return await self._async_req("getCompCombined")

    async def async_comp_day(self) -> dict[str, dict[str, dict[str, float]]]:
        """Retrieve comparison data between a given household.

        and all other households over the period of a day.
        """
        return await self._async_req("getCompDay")

    async def async_comp_week(self) -> dict[str, dict[str, dict[str, float]]]:
        """Retrieve comparison data between a given household.

        and all other households over the period of a week.
        """
        return await self._async_req("getCompWeek")

    async def async_comp_month(self) -> dict[str, dict[str, dict[str, float]]]:
        """Retrieve comparison data between a given household.

        and all other households over the period of a month.
        """
        return await self._async_req("getCompMonth")

    async def async_comp_year(self) -> dict[str, dict[str, dict[str, float]]]:
        """Retrieve comparison data between a given household.

        and all other households over the period of a year.
        """
        return await self._async_req("getCompYear")

    async def async_consumption_co2_graph(
        self,
        fromtime: str | int,
        totime: str | int,
        aggperiod: str = DEFAULT_PERIOD,
        cachekey: str | None = None,
    ) -> dict:
        """Return timeseries of consumed/cost and CO2."""
        params: dict = {
            "aggPeriod": aggperiod,
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
            "fromTime": fromtime,
            "toTime": totime,
        }
        return await self._async_req("getConsumptionCostCO2Graph", params=params)

    async def async_generated_consumption_import(
        self,
        fromtime: str | int,
        totime: str | int,
        cachekey: str | None = None,
    ) -> dict[str, float]:
        """Deliver proportion of consumed power that is generated in the home.

        vs that imported. Only useful if PWER and PWER_GAC channels are present.
        """
        params: dict = {
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
            "fromTime": fromtime,
            "toTime": totime,
        }
        _data = await self._async_req("getConsumptionGeneratedAndImport", params=params)
        return _data[DATA]

    async def async_generated_consumption_export(
        self,
        fromtime: str | int,
        totime: str | int,
        cachekey: str | None = None,
    ) -> dict[str, float]:
        """Deliver proportion of generated power.

        that is used in the home vs that exported.
        Only useful if PWER and PWER_GAC channels are present.
        """
        params: dict = {
            "fromTime": fromtime,
            "toTime": totime,
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
        }
        _data = await self._async_req("getGeneratedConsumptionAndExport", params=params)
        return _data[DATA]

    async def async_country_list(self) -> dict[str, str]:
        """Retrieve list of countries with their associated voltage."""
        return await self._async_req("getCountryList")

    async def async_day(
        self, getpreviousperiod: int = 0, cache: bool = True
    ) -> dict[str, list[float]]:
        """Retrieve historical timeseries of consumption data.

        for household for previous 24 hours.
        Data will be returned at a minute level of resolution.
        """
        params: dict = {
            "getPreviousPeriod": getpreviousperiod,
            "cache": str(cache),
        }
        _data = await self._async_req("getDay", params=params)
        return _data[DATA]

    async def async_week(
        self,
        getpreviousperiod: int = 0,
        cache: bool = True,
        datatype: str = DEFAULT_TYPE,
    ) -> dict[str, list[float]]:
        """Retrieve the historical timeseries of consumption data.

        for a household for the previous week.
        Data will be returned at a hour level of resolution.
        """
        params: dict = {
            "getPreviousPeriod": getpreviousperiod,
            "cache": str(cache),
            "dataType": datatype,
        }
        _data = await self._async_req("getWeek", params=params)
        return _data[DATA]

    async def async_month(
        self,
        getpreviousperiod: int = 0,
        cache: bool = True,
        datatype: str = DEFAULT_TYPE,
    ) -> dict[str, list[float]]:
        """Retrieve the historical timeseries of consumption data.

        or a household for the previous month.
        Data will be returned at a day level of resolution.
        """
        params: dict = {
            "getPreviousPeriod": getpreviousperiod,
            "cache": str(cache),
            "dataType": datatype,
        }
        _data = await self._async_req("getMonth", params=params)
        return _data[DATA]

    async def async_year(
        self,
        cache: bool = True,
        datatype: str = DEFAULT_TYPE,
    ) -> dict[str, list[float]]:
        """Retrieve the historical timeseries of consumption data.

        for a household for the previous year.
        Data will be returned at a month level of resolution.
        """
        params: dict = {
            "cache": str(cache),
            "dataType": datatype,
        }
        _data = await self._async_req("getYear", params=params)
        return _data[DATA]

    async def async_estimated_combined(self) -> dict[str, float | dict[str, float]]:
        """Retrieve estimated usage data for a given household for the current.

        day and current month.
        The comparisons are also available elsewhere separately (see getForecast)
        """
        return await self._async_req("getEstCombined")

    async def async_first_data(self) -> dict[str, str]:
        """Return first data point time. (UTC)."""
        return await self._async_req("getFirstData")

    async def async_forecast(self, period: str) -> dict[str, dict[str, float]]:
        """Get forecast for energy consumption, greenhouse gas generation.

        or cost (if tariff set).
        """
        return await self._async_req("getForecast", params={"period": period})

    async def async_generated_energy_revenue_carbon(
        self,
        fromtime: str | int,
        totime: str | int,
        aggperiod: str = DEFAULT_PERIOD,
        cachekey: str | None = None,
    ) -> dict[str, str | list[dict[str, Any]]]:
        """Return a timeseries of consumed, revenue and c02 saved."""
        params: dict = {
            "fromTime": fromtime,
            "toTime": totime,
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
            "aggPeriod": aggperiod,
        }
        return await self._async_req("getGeneratedEnergyRevenueCarbon", params=params)

    async def async_generated_consumption_graph(
        self,
        fromtime: str | int,
        totime: str | int,
        cachekey: str | None = None,
        aggperiod: str = DEFAULT_PERIOD,
    ) -> dict[str, str | list[dict[str, Any]]]:
        """Deliver timeseries array of consumed/generated/genconsumed/exported/imported.

        Only useful if PWER and PWER_GAC channels are present.
        """
        params: dict = {
            "fromTime": fromtime,
            "toTime": totime,
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
            "aggPeriod": aggperiod,
        }
        return await self._async_req("getGenerationConsumptionGraph", params=params)

    async def async_generated_consumption_graph_costrev(
        self,
        fromtime: str | int,
        totime: str | int,
        cachekey: str | None = None,
        aggperiod: str = DEFAULT_PERIOD,
    ) -> dict[str, str | list[dict[str, Any]]]:
        """Deliver timeseries array of consumed/generated/genconsumed/exported/imported.

        costs/revenue.
        Only useful if PWER and PWER_GAC channels are present.
        """
        params: dict = {
            "aggPeriod": aggperiod,
            "fromTime": fromtime,
            "toTime": totime,
            "cacheTTL": self._cachettl,
            "cacheKey": cachekey,
        }
        return await self._async_req(
            "getGenerationConsumptionGraphCostRevenue", params=params
        )

    async def async_historical_values(
        self, period: str = DEFAULT_PERIOD, type_str: str = "PWER"
    ) -> dict[str, str | list[dict[str, str | list[dict[str, str]]]]]:
        """Return array of historical values."""
        return await self._async_req(
            "getHV", params={"period": period, "type": type_str}
        )

    async def async_household(self) -> dict[str, str]:
        """Get household attributes as set in setHousehold.php."""
        return await self._async_req("getHousehold")

    async def async_household_data_reference(
        self,
    ) -> dict[str, dict[str, dict[str, str | list]]]:
        """Return a set of allowed values for setting the household attributes."""
        return await self._async_req("getHouseholdDataReference")

    async def async_mac(self) -> dict[str, list[dict[str, str | int | list]]]:
        """Set the list of MACs as a listOfMACs for a valid householder ID (HID)."""
        return await self._async_req("getMAC")

    async def async_mac_status(
        self, mac: str
    ) -> dict[str, list[dict[str, str | int | list]]]:
        """Retrieve the device status for a given MAC."""
        return await self._async_req("getMACStatus", params={"mac_address": mac})

    async def async_pulse(self, sid: str | int) -> dict[str, str | int]:
        """Get the pulse rate for a given IR clamp."""
        return await self._async_req("getPulse", params={"sid": sid})

    async def async_status(self, get_sids: bool = False) -> dict[str, str | list[dict]]:
        """Retrieve the device status as a list of statuses."""
        _data = await self._async_req("getStatus")
        self.info[HID] = _data[HID]
        self.info[MAC] = _data[LISTOFMACS][0][MAC]
        self.info[STATUS] = _data[LISTOFMACS][0][STATUS]
        self.info[TYPE] = ""
        if TYPE in _data[LISTOFMACS][0]:
            self.info[TYPE] = _data[LISTOFMACS][0][TYPE]
        self.info[VERSION] = _data[LISTOFMACS][0][VERSION]
        if get_sids:
            await self.async_get_sids()
        return _data

    async def async_tariff(self) -> list[dict[str, str | int | dict]]:
        """Return the tariff structure(s) for the HID supplied.

        (limited by optional sid).
        """
        return await self._async_req("getTariff")

    async def async_time_series(
        self,
        fromtime: str | int,
        totime: str | int,
        aggperiod: str = DEFAULT_PERIOD,
        aggfunc: str = SUM,
        cache: bool = True,
        datatype: str = DEFAULT_TYPE,
    ) -> dict[str, str | dict[str, list[str]]]:
        """Retrieve the historical timeseries of consumption data.

        for a household over the specified period.
        `fromtime` and `totime` are expressed in epoch timestamp
        data_type: cost or kwh
        """
        params: dict = {
            "fromTime": fromtime,
            "toTime": totime,
            "aggPeriod": aggperiod,
            "aggFunc": aggfunc,
            "cache": str(cache),
            "dataType": datatype,
        }
        return await self._async_req("getTimeSeries", params=params)

    async def async_weather(
        self, city: str, country: str, timestamp: str | None = None
    ) -> list[Any] | dict[str, str]:
        """Get the current weather for the location of the HID."""
        params: dict = {
            "city": city,
            "country": country,
            "timestamp": timestamp,
        }
        return await self._async_req("getWeather", params=params)

    async def async_set_budget(self, budget: float) -> dict[str, str | float]:
        """Set a value for the monthly budget for a HID."""
        return await self._async_req("setBudget", params={"budget": budget})
