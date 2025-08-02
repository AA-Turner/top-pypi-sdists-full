from datetime import datetime, timedelta
from typing import Literal, Optional

import click
from gable.cli.helpers.data_asset_s3.path_pattern_manager import PathPatternManager
from gable.cli.helpers.emoji import EMOJI


def validate_input(
    action: Literal["register", "check"],
    bucket: Optional[str],
    lookback_days: int,
    include_prefix_list: Optional[tuple[str, ...]],
    exclude_prefix_list: Optional[tuple[str, ...]],
    history: Optional[bool],
) -> None:
    if not bucket:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Missing required option --bucket for S3 file registration and checking. You can use the --debug or --trace flags for more details."
        )

    if history:
        if action == "check":
            raise click.ClickException(
                f"{EMOJI.RED_X.value} --history is only valid for the register command."
            )
        if include_prefix_list is None or len(include_prefix_list) != 2:
            raise click.ClickException(
                "Two include prefixes are required for historical data asset detection when using --history."
            )

    if lookback_days <= 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} --lookback-days must be at least 1."
        )

    if not history:
        if include_prefix_list is not None:
            for include_prefix in include_prefix_list:
                _, dt = PathPatternManager().substitute_date_placeholders(
                    include_prefix
                )
                if dt and dt < datetime.now() - timedelta(days=lookback_days):
                    raise click.ClickException(
                        f"{EMOJI.RED_X.value} Include prefix '{include_prefix}' must be within lookback window (between --lookback-days ago and now())."
                    )
        if exclude_prefix_list is not None:
            for exclude_prefix in exclude_prefix_list:
                _, dt = PathPatternManager().substitute_date_placeholders(
                    exclude_prefix
                )
                if dt and dt < datetime.now() - timedelta(days=lookback_days):
                    raise click.ClickException(
                        f"{EMOJI.RED_X.value} Exclude prefix '{exclude_prefix}' must be within lookback window (between --lookback-days ago and now())."
                    )
                if include_prefix_list is not None and len(include_prefix_list) > 0:
                    if not any(
                        (
                            include_prefix != exclude_prefix
                            and include_prefix in exclude_prefix
                        )
                        for include_prefix in include_prefix_list
                    ):
                        raise click.ClickException(
                            f"{EMOJI.RED_X.value} Exclude prefix '{exclude_prefix}' must be more specific than at least one include prefix."
                        )
