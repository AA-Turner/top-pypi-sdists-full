import asyncio
import pandas as pd
from urllib.parse import urljoin
from xmlrpc.client import ServerProxy
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError


class Odoo(HTTPService, FlowComponent):
    """
    Odoo

        Overview

            This component interacts with an Odoo server to perform various operations like `search_read` and `create`.

        :widths: auto


        | credentials                  |   Yes    | A dictionary containing connection details to the Odoo server:      |
        |                              |          | "HOST", "PORT", "DB", "USERNAME", "PASSWORD".                       |
        | method                       |   Yes    | The Odoo method to be called (e.g., "search_read", "create").       |
        | model                        |   Yes    | The Odoo model to be used for the method call (e.g., "res.partner").|
        | domain                       |   No     | Domain filter for searching records, applicable for "search_read".  |
        | fields                       |   No     | Fields to be retrieved, applicable for "search_read".               |
        | values                       |   No     | Values to be used for creating records, applicable for "create".    |
        | use_field_from_previous_step |   No     | Field from previous step to filter records in "search_read".        |

        Returns

            This component returns a pandas DataFrame containing the results of the Odoo operation.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Odoo:
          credentials:
          HOST: ODOO_HOST
          PORT: ODOO_PORT
          DB: ODOO_DB
          USERNAME: ODOO_USERNAME
          PASSWORD: ODOO_PASSWORD
          model: stock.warehouse
          method: search_read
          domain:
          - - - company_id.name
          - '='
          - Pokemon
          fields:
          - id
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {
        "HOST": str,
        "PORT": int,
        "DB": str,
        "USERNAME": str,
        "PASSWORD": str,
    }

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

        self.processing_credentials()

        self.common = self.get_server_proxy("common")
        self.uid = self.common.authenticate(
            self.credentials["DB"],
            self.credentials["USERNAME"],
            self.credentials["PASSWORD"],
            {},
        )

        self.models = self.get_server_proxy("object")

        return True

    async def run(self):
        method_call = getattr(self, f"odoo_{self.method}")

        if not method_call:
            raise ComponentError("incorrect method or method not provided")

        method_call_task = asyncio.to_thread(method_call)

        method_call_result = await method_call_task

        df = pd.DataFrame(method_call_result)
        if df.empty:
            self._logger.warning("Empty DataFrame")

        self.add_metric("NUMROWS", len(df.index))
        self.add_metric("NUMCOLS", len(df.columns))

        self._result = df

        if self._debug is True:
            print("::: Printing Result Data === ")
            print("Data: ", self._result)
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])

        return self._result

    async def close(self):
        return True

    def get_server_proxy(self, endpoint):
        port = (
            f":{self.credentials['PORT']}" if self.credentials["PORT"] != 80 else ""
        )
        base_url = f"{self.credentials['HOST']}{port}/xmlrpc/2/"
        url = urljoin(base_url, endpoint)
        return ServerProxy(url)

    def model_call(self, method, *args, **kwargs):
        return self.models.execute_kw(
            self.credentials["DB"],
            self.uid,
            self.credentials["PASSWORD"],
            self.model,
            method,
            *args,
            **kwargs,
        )

    def get_values_from_previous_data(self, field=None):
        if isinstance(self.data, pd.DataFrame) and not self.data.empty:
            if not field:
                return [self.data.to_dict("records")]

            return [[(field, "in", self.data[field].to_list())]] or [[]]

    def odoo_search_read(self):
        prev_step_field = getattr(self, "use_field_from_previous_step", None)

        domain = getattr(
            self,
            "domain",
            self.get_values_from_previous_data(prev_step_field),
        )
        fields = getattr(self, "fields", {})

        self._logger.debug(f"Search Read with domain: {domain} and fields: {fields}")
        return self.model_call(
            "search_read", domain or [], fields and {"fields": fields}
        )

    def odoo_create(self):
        try:
            # values on step arguments have precedence
            values = getattr(self, "values", self.get_values_from_previous_data())
            assert values

            return self.model_call("create", values)

        except AssertionError:
            raise ComponentError(
                '"values" required for "create" method'
            )
