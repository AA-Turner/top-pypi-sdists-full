"""
Example CLI: connect with env-based credentials, list objects, read sample rows.

Environment variables: ``DC_SITE_URL``, ``DC_CLIENT_ID``, ``DC_API_KEY``
(see ``dealcloud_sdk.constants.env_var_names``).
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[assignment]

from dealcloud_sdk import DealCloud
from dealcloud_sdk.factories.from_env import dc_from_environment_variables
from dealcloud_sdk.models.factory_models import DealCloudConfig

# Keep in sync with package __init__ (re-exported there).
TEST_OBJECT_API_NAME = "Contacts"


def _load_dotenv() -> None:
    if load_dotenv is None:
        return
    here = Path(__file__).resolve().parent
    # example_project/.env when running from editable install
    for candidate in (
        here.parent.parent.parent / ".env",
        here.parent.parent / ".env",
        Path.cwd() / ".env",
    ):
        if candidate.is_file():
            load_dotenv(candidate)
            return


def build_client() -> DealCloud:
    """Build a :class:`DealCloud` client from environment variables."""
    raw = dc_from_environment_variables()
    if isinstance(raw, DealCloudConfig):
        return DealCloud.from_config_object(raw)
    return DealCloud(
        site_url=raw.site_url,
        client_id=raw.client_id,
        client_secret=raw.client_secret,
        scope=raw.scope,
    )


def main() -> None:
    _load_dotenv()
    try:
        dc = build_client()
    except KeyError as e:
        print(
            "Missing configuration. Set DC_SITE_URL, DC_CLIENT_ID, and DC_API_KEY "
            "(see .env.example).",
            file=sys.stderr,
        )
        print(f"Detail: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 — surface auth/HTTP errors to the user
        print(f"Failed to connect: {e}", file=sys.stderr)
        sys.exit(1)

    objects = dc.get_objects()
    print(f"Schema: {len(objects)} object(s).")
    for obj in objects[:10]:
        print(f"  - {obj.apiName}: {obj.pluralName}")
    if len(objects) > 10:
        print("  ...")

    names = {o.apiName for o in objects}
    if TEST_OBJECT_API_NAME not in names:
        print(
            f"\nNote: '{TEST_OBJECT_API_NAME}' was not found. "
            "Adjust TEST_OBJECT_API_NAME in dealcloud_sdk_example for your site.",
            file=sys.stderr,
        )
        return

    # Do not use OData-style ``query="$top=5"``: the rows POST API expects a JSON/Mongo-style
    # filter string for ``query=``, not ``$top``. Limit rows by taking the first streaming page.
    rows: list = []
    for batch in dc.read_data_streaming(TEST_OBJECT_API_NAME, page_size=5):
        rows = batch
        break

    print(f"\nRead up to 5 rows from {TEST_OBJECT_API_NAME!r} ({len(rows)} row(s) returned).")
    if rows:
        print("First row keys:", ", ".join(sorted(rows[0].keys())))


if __name__ == "__main__":
    main()
