"""Feature discovery: a short "Did you know?" list of what is new in the CLI, printed after a command, whatever its outcome.

Every six hours while the newest feature is less than a month old, and then once a week. The time of the last list is
`lastFeatureTipsShown` in `_config.json`. Setting `FIVETRAN_DISABLE_FEATURE_TIPS` to `1` or `true` turns it off. It is advisory: nothing here may fail a command."""
import os
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional, Sequence

from fivetran_connector_sdk_common.constants import (
    FEATURE_TIPS_FRESH_DAYS,
    FEATURE_TIPS_OLD_INTERVAL_IN_SEC,
    FIVETRAN_DISABLE_FEATURE_TIPS_ENV,
    LAST_FEATURE_TIPS_FIELD,
    SIX_HOUR_IN_SEC,
)
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli.connector_helper import load_config, update_config


@dataclass(frozen=True)
class FeatureTip:
    added: date
    message: str


# The commands after which the tips are shown; `version`, `help` and `reset` stay quiet.
FEATURE_TIPS_COMMANDS = ("init", "package", "deploy", "debug", "run", "configuration")

CHANGELOG_URL = "https://fivetran.com/docs/connector-sdk/changelog"

# Newest first. Add a feature here with the date of the release that first shows it.
FEATURE_TIPS = (
    FeatureTip(
        date(2026, 11, 17),
        "`fivetran run` writes what your connector emits to an Iceberg REST catalog (`--destination-file` or "
        "`destination.json`). See `fivetran run --help`."),
    FeatureTip(
        date(2026, 11, 17),
        "`op.truncate(table, deferred=True)` applies a truncate only after `update()` returns successfully, "
        "so a sync that fails deletes nothing."),
    FeatureTip(
        date(2026, 11, 17),
        "`fivetran deploy --proxy-id <id>` routes your connector's traffic through a Proxy Agent (beta). "
        "`--proxy-host-config-key` names the configuration key that holds the host."),
    FeatureTip(
        date(2026, 11, 17),
        "One connector can load several source schemas: name the `schema` of each table in `schema()` and "
        "pass `schema=` to operations such as `op.upsert`."),
    FeatureTip(
        date(2026, 11, 17),
        "Keep your deployment settings in an `options.toml` (`--options-file`, `./options.toml` or "
        "`~/.fivetran/connector_sdk/options.toml`) and pick one set with `--profile`."),
)


def _tips_disabled() -> bool:
    """True when FIVETRAN_DISABLE_FEATURE_TIPS is "1" or "true" (case-insensitive), like DO_NOT_TRACK."""
    value = os.getenv(FIVETRAN_DISABLE_FEATURE_TIPS_ENV, None)
    return value is not None and value.strip().lower() in ("1", "true")


def show_feature_tips(now: Optional[float] = None, tips: Sequence[FeatureTip] = FEATURE_TIPS) -> None:
    """Prints the list if it is time to: at most once per interval, and only in a terminal outside CI, and not when the user has disabled the tips."""
    try:
        if not tips or os.environ.get("CI") or _tips_disabled() or not sys.stdout.isatty():
            return
        config = load_config()
        if config is None:
            return
        now = time.time() if now is None else now
        today = datetime.fromtimestamp(now, timezone.utc).date()
        newest_is_fresh = (today - max(tip.added for tip in tips)).days < FEATURE_TIPS_FRESH_DAYS
        interval = SIX_HOUR_IN_SEC if newest_is_fresh else FEATURE_TIPS_OLD_INTERVAL_IN_SEC
        last_shown = config.get(LAST_FEATURE_TIPS_FIELD)
        if isinstance(last_shown, (int, float)) and 0 <= (now - last_shown) < interval:
            return

        lines = [f"  • {tip.message}" for tip in sorted(tips, key=lambda tip: tip.added, reverse=True)]
        lines.append(f"Full release notes: {CHANGELOG_URL}")
        print_library_log("Did you know? New in the Connector SDK:\n" + "\n".join(lines), log_icon=Logging.LogIcon.INFO)
        update_config(**{LAST_FEATURE_TIPS_FIELD: int(now)})
    except Exception:
        # feature tips are advisory; never abort commands due to unexpected error
        pass
