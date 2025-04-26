""" Databricks Secret Type """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcli.models import Secret


@dataclass
class MCLIDatabricksSecret(Secret):
    """Secret class for DATABRICKS_HOST and DATABRICKS_TOKEN that will be added as environment variables
    """
    host: Optional[str] = None
    token: Optional[str] = None

    @property
    def mapi_data(self) -> Dict[str, Any]:
        return {
            'databricksSecret': {
                'name': self.name,
                'value': {
                    'host': self.host,
                    'token': self.token,
                }
            },
        }
