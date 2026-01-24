import json
from datetime import datetime
from io import BytesIO
from typing import Generator, Optional

import pandas as pd
import requests
from django.db.models import QuerySet
from dynamic_preferences.registries import global_preferences_registry
from pandas.tseries.offsets import BDay

from wbcore.contrib.currency.models import Currency
from wbcore.contrib.io.backends import AbstractDataBackend, register
from wbcore.contrib.io.models import ImportCredential

from ..utils import get_timedelta_import_currency_fx_rates


@register("Currency FX Rates", provider_key="fixerio", save_data_in_import_source=False, passive_only=False)
class DataBackend(AbstractDataBackend):
    ENDPOINT = "https://data.fixer.io/api/"
    HEADERS = {"user-agent": "stainly", "Content-Type": "application/json", "Accept": "application/json"}

    def get_provider_id(self, obj: Currency) -> str:
        return obj.key

    def get_default_queryset(self) -> QuerySet[Currency]:
        return Currency.objects.all()

    def __init__(
        self,
        import_credential: Optional[ImportCredential] = None,
        base_currency: Optional[str] = None,
        **kwargs,
    ):
        if not import_credential or not import_credential.authentication_token:
            raise ValueError("Fixer IO backend needs a valid import credential object")
        if not base_currency:
            base_currency = global_preferences_registry.manager()["currency__default_currency"]
        self.authentication_token = import_credential.authentication_token
        self.base_currency = base_currency

    def get_files(
        self,
        execution_time: datetime,
        obj_external_ids: Optional[list[str]] = None,
        **kwargs,
    ) -> Generator[tuple[str, BytesIO], None, None]:
        execution_date = execution_time.date()
        start = kwargs.get("start", execution_date - BDay(get_timedelta_import_currency_fx_rates() + 1))
        params = {"access_key": self.authentication_token, "base": self.base_currency}
        if (
            obj_external_ids and len(obj_external_ids) < Currency.objects.count()
        ):  # We add symbols only if the requests objects count is lower than the maximum expected currency
            params["symbols"] = ",".join(obj_external_ids)
        res = []
        for _date in pd.date_range(start, execution_date, freq="B"):
            r = requests.get(
                f'{self.ENDPOINT}/{_date.strftime("%Y-%m-%d")}?', params=params, headers=self.HEADERS, timeout=10
            )
            if r.status_code == requests.codes.ok:
                res_json = r.json()
                if res_json and res_json["success"]:
                    res.append(res_json)
        if res:
            content_file = BytesIO()
            content_file.write(json.dumps(res).encode())
            file_name = f"fixerio_currency_fx_rates_{start:%Y-%m-%d}_{execution_date:%Y-%m-%d}_{datetime.timestamp(execution_time)}.json"
            yield file_name, content_file
