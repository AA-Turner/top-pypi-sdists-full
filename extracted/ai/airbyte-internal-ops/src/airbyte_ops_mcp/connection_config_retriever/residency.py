# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Runtime residency checks for EU regression runners and debug workstations.

`is_running_in_eu_region` asks the GCE metadata server for the zone and allows
EU retrieval only in a `europe-west9` zone. IAM authorizes secret access,
independently of the service account attached to the VM.

This is a guard against mistakes, not a security boundary. It stops a US runner
or workstation, a laptop or Cloud Run from reading EU secrets, and an EU runtime
from reading a US connection, by accident. A process with root off GCE could
answer the metadata requests itself, and IAM does not separate the regions yet:
a workspace secret's name does not carry its region, so a grant cannot tell EU
and US secrets apart.
"""

from __future__ import annotations

import requests

EU_REGION = "europe-west9"
EU_REGION_REQUIRED_MESSAGE = (
    "Retrieval for EU connections is only permitted in the EU region "
    f"({EU_REGION}). Use an EU regression runner or debug workstation"
)
EU_REGION_EU_ONLY_MESSAGE = (
    "Retrieval in the EU region is only permitted for EU connections; "
    "use a US runner or debug workstation for a non-EU connection"
)

_METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance"
_METADATA_HEADERS = {"Metadata-Flavor": "Google"}


def is_running_in_eu_region() -> bool:
    """Return whether the process runs in the permitted EU GCE region."""
    try:
        with requests.Session() as session:
            session.trust_env = False
            zone_response = session.get(
                f"{_METADATA_URL}/zone",
                headers=_METADATA_HEADERS,
                timeout=2,
                allow_redirects=False,
            )
            if (
                zone_response.status_code != 200
                or zone_response.headers.get("Metadata-Flavor") != "Google"
            ):
                return False
    except requests.RequestException:
        return False

    zone = zone_response.text.strip().rsplit("/", 1)[-1]
    return zone.startswith(f"{EU_REGION}-")
