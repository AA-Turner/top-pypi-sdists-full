from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase

class OpenWeather(QSBase):
    """
    OpenWeather.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          OpenWeather:
          # attributes here
        ```
    """
    _version = "1.0.0"
    type = "weather"
    _driver = "openweather"
    _mapping: dict = {
        "dt": "timestamp",
        "main": "temperature",
        "coord": "coordinates",
        "name": "city",
        "id": "city_id"
    }
    _from_conditions: list = [
        "country",
        "store_id",
        "store_name"
    ]

    async def weather(self):
        try:
            rst = []
            resultset = await self._qs.weather()
            print('CONDITIONS > ', self._qs._conditions)
            data = resultset.copy()
            for key, value in data.items():
                if key in self._mapping:
                    resultset[self._mapping[key]] = value
                    del resultset[key]
            if self._from_conditions:
                for key in self._from_conditions:
                    if key in self._qs._conditions:
                        resultset[key] = self._qs._conditions[key]
            rst.append(resultset)
            return rst
        except QSNotFound as err:
            raise DataNotFound(f"Coordinates Not Found: {err}") from err
        except Exception as err:
            self._logger.exception(err)
            raise ComponentError(f"OpenWeather ERROR: {err!s}") from err
