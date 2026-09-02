from typing import Optional
import asyncio
import pandas
from asyncdb import AsyncDB
from navconfig.logging import logging
from querysource.conf import asyncpg_url, default_dsn
from ..credentials import CredentialsInterface
from ...utils.functions import is_empty, as_boolean
from ...exceptions import DataNotFound


class DBSupport(CredentialsInterface):
    """DBSupport.

        Interface for adding AsyncbDB-based Database Support to Components.
    """
    _service_name: str = 'Flowtask'
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str,
    }

    def __init__(
        self,
        *args,
        **kwargs
    ):
        self.as_dataframe: bool = as_boolean(kwargs.get("as_dataframe", False))
        # using "string" instead objects in pandas
        self.as_string: bool = as_boolean(kwargs.get("as_string", False))
        # Infer types:
        self.infer_types: bool = as_boolean(kwargs.get("infer_types", False))
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(
                'Flowtask.DBSupport'
            )
        super().__init__(*args, **kwargs)

    def event_loop(
        self, evt: Optional[asyncio.AbstractEventLoop] = None
    ) -> asyncio.AbstractEventLoop:
        if evt is not None:
            asyncio.set_event_loop(evt)
            return evt
        else:
            try:
                return asyncio.get_event_loop()
            except RuntimeError as exc:
                try:
                    evt = asyncio.new_event_loop()
                    asyncio.set_event_loop(evt)
                    return evt
                except RuntimeError as exc:
                    raise RuntimeError(
                        f"There is no Event Loop: {exc}"
                    ) from exc

    def get_connection(
        self,
        driver: str = "pg",
        dsn: Optional[str] = None,
        params: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs,
    ):
        # TODO: datasources and credentials
        if not kwargs and driver == "pg":
            kwargs = {
                "server_settings": {
                    "application_name": f"{self._service_name}.DB",
                    "client_min_messages": "notice",
                    "max_parallel_workers": "512",
                    "jit": "on",
                }
            }
        if not event_loop:
            event_loop = self.event_loop()
        args = {
            "loop": event_loop,
            **kwargs
        }
        if dsn is not None:
            args["dsn"] = dsn
        if params:
            args["params"] = params
        return AsyncDB(
            driver, **args
        )

    def db_connection(
        self,
        driver: str = "pg",
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        if not credentials:
            credentials = {"dsn": default_dsn}
        else:
            credentials = {"params": credentials}
        kwargs = {}
        if driver == "pg":
            kwargs = {
                "server_settings": {
                    "application_name": f"{self._service_name}.DB",
                    "client_min_messages": "notice",
                    "max_parallel_workers": "512",
                    "jit": "on",
                }
            }
        if not event_loop:
            event_loop = self.event_loop()
        return AsyncDB(
            driver,
            loop=event_loop,
            **credentials,
            **kwargs
        )

    def pg_connection(
        self,
        dsn: Optional[str] = None,
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        if not credentials:
            if dsn is not None:
                credentials = {"dsn": dsn}
            else:
                credentials = {"dsn": asyncpg_url}
        else:
            credentials = {"params": credentials}
        kwargs: dict = {
            "min_size": 2,
            "server_settings": {
                "application_name": f"{self._service_name}.DB",
                "client_min_messages": "notice",
                "max_parallel_workers": "512",
                "jit": "on",
            },
        }
        if not event_loop:
            event_loop = self.event_loop()
        return AsyncDB(
            "pg",
            loop=event_loop, **credentials, **kwargs
        )

    def get_default_driver(self, driver: str):
        """get_default_driver.

        Getting a default connection based on driver's name.
        """
        driver_path = f"querysource.datasources.drivers.{driver}"
        drv = f"{driver}_default"
        try:
            driver_module = __import__(driver_path, fromlist=[driver])
            drv_obj = getattr(driver_module, drv)
            return drv_obj
        except ImportError as err:
            raise ImportError(
                f"Error importing driver: {err!s}"
            ) from err
        except AttributeError as err:
            raise AttributeError(
                f"Error getting driver: {err!s}"
            ) from err
        except Exception as err:
            raise Exception(
                f"Error getting default connection: {err!s}"
            ) from err

    def default_connection(self, driver: str):
        """default_connection.

        Default Connection to Database.
        """
        credentials = {}
        try:
            driver = self.get_default_driver(driver)
            credentials = driver.params()
            if driver.driver == 'pg' and credentials.get('username', None) is not None:
                credentials['user'] = credentials.pop('username')
        except ImportError as err:
            raise ImportError(
                f"Error importing Default driver: {err!s}"
            ) from err
        try:
            return self.get_connection(
                driver=driver.driver,
                params=credentials
            )
        except Exception as err:
            raise Exception(
                f"Error getting Default Connection: {err!s}"
            ) from err

    async def get_dataframe(self, result):
        try:
            df = pandas.DataFrame(result)
        except Exception as err:  # pylint: disable=W0703
            logging.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        if is_empty(df):
            raise DataNotFound("DbClient: Data not Found")
        df.infer_objects()
        if self.infer_types is True:
            df = df.convert_dtypes(convert_string=self.as_string)
        if self._debug is True:
            print(df.dtypes)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if (
            hasattr(self, "clean_strings") and getattr(self, "clean_strings", False) is True
        ):
            u = df.select_dtypes(include=["object", "string"])
            df[u.columns] = u.fillna("")
        return df
