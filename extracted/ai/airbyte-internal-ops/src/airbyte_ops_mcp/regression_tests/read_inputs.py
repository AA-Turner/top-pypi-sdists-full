# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""The READ budget and record cap a regression run takes from the workflow's inputs.

Run as a script by both jobs' `Resolve READ inputs` steps, the US job's before
SPEC and the EU job's before it submits its Batch job, so the two cannot drift
and a bad value fails the run before the build or the VM's setup. Workflow
expressions have no arithmetic, and shell arithmetic evaluates its operand as
an expression, so a value is judged here, as text, before any number is made
from it. The script imports nothing outside the standard library, so the steps
run it with the runner's `python3` straight from the checkout.
"""

from __future__ import annotations

import re
import sys

READ_TIMEOUT_MINUTES_DEFAULT = 170

READ_TIMEOUT_MINUTES_MAX = 300
"""The largest READ budget the workflow accepts, in minutes.

The READ step's timeout is the budget plus ten, so 300 makes a 310-minute step
and leaves fifty minutes of a GitHub-hosted job's six hours for setup, the
build, SPEC, CHECK, DISCOVER and the uploads. The MCP tool refuses anything
larger before dispatch, and the workflow refuses it again here.
"""

READ_STEP_MARGIN_MINUTES = 10
"""The READ step's timeout ends this long after the budget, so the CLI
compares and reports a long read before GitHub kills the step."""


def main(argv: list[str]) -> int:
    """Judge the two inputs and append the step outputs.

    `argv` is `read_timeout_minutes` and `max_records`, each empty when not
    given, then the `$GITHUB_OUTPUT` file. Writes `read_timeout_seconds` and
    `step_timeout_minutes`, then `max_records` when a cap was given. A value
    that is not a whole number in range prints a workflow error and returns 1
    before its own output is written.
    """
    read_timeout_minutes, max_records, output_path = argv
    minutes = read_timeout_minutes or str(READ_TIMEOUT_MINUTES_DEFAULT)
    if (
        not re.fullmatch(r"[1-9][0-9]{0,2}", minutes)
        or int(minutes) > READ_TIMEOUT_MINUTES_MAX
    ):
        print(
            "::error::read_timeout_minutes must be a whole number of minutes "
            f"from 1 to {READ_TIMEOUT_MINUTES_MAX}, got '{read_timeout_minutes}'"
        )
        return 1
    budget = int(minutes)
    print(f"READ budget: {budget} minutes")
    with open(output_path, "a", encoding="utf-8") as output:
        output.write(f"read_timeout_seconds={budget * 60}\n")
        output.write(f"step_timeout_minutes={budget + READ_STEP_MARGIN_MINUTES}\n")

    # Digits only, so the CLI gets one argument and a value such as
    # '5 --no-http-replay' cannot smuggle in a flag.
    if max_records:
        if not re.fullmatch(r"[1-9][0-9]*", max_records):
            print(
                "::error::max_records must be a whole number of records, at "
                f"least 1, got '{max_records}'"
            )
            return 1
        print(f"Capping each side of the READ at {max_records} records")
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"max_records={max_records}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
