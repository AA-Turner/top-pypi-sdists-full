# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Runtime checks for the dedicated EU regression runner.

`is_running_on_eu_runner` asks the GCE metadata server for the zone and the
service account, and allows EU retrieval only in a `europe-west9` zone under
the `connector-regression-eu-job` service account.

This is a guard against mistakes, not a security boundary. It stops a US runner,
a laptop or Cloud Run from reading EU secrets, and the EU runner from reading a
US connection, by accident. A process with root off GCE could answer the
metadata requests itself, and IAM does not separate the regions yet: a workspace
secret's name does not carry its region, so a grant cannot tell EU and US
secrets apart.
"""

from __future__ import annotations

import requests

EU_RUNNER_REGION = "europe-west9"
EU_RUNNER_SERVICE_ACCOUNT = (
    "connector-regression-eu-job@internal-airbyte-ai-infra.iam.gserviceaccount.com"
)
EU_RUNNER_REQUIRED_MESSAGE = (
    "Retrieval for EU connections is only permitted on the EU regression runner "
    f"({EU_RUNNER_REGION}, service account {EU_RUNNER_SERVICE_ACCOUNT})"
)
EU_RUNNER_EU_ONLY_MESSAGE = (
    "The EU regression runner only retrieves EU connections; a non-EU "
    "connection runs on the US runner"
)

_METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance"
_METADATA_HEADERS = {"Metadata-Flavor": "Google"}


def is_running_on_eu_runner() -> bool:
    """Return whether the process runs in the expected EU GCE zone and identity."""
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

            service_account_response = session.get(
                f"{_METADATA_URL}/service-accounts/default/email",
                headers=_METADATA_HEADERS,
                timeout=2,
                allow_redirects=False,
            )
            if (
                service_account_response.status_code != 200
                or service_account_response.headers.get("Metadata-Flavor") != "Google"
            ):
                return False
    except requests.RequestException:
        return False

    zone = zone_response.text.strip().rsplit("/", 1)[-1]
    service_account = service_account_response.text.strip()
    return zone.startswith(f"{EU_RUNNER_REGION}-") and (
        service_account == EU_RUNNER_SERVICE_ACCOUNT
    )
