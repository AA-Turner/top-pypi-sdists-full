from typing import Any

from project.api.schema.common import BaseSO


class RawDataCommonSO(BaseSO):
    raw_data: dict[str, Any] = {}
