"""`python -m probe.integrations.miles <queue_dir>` drained the metric queue jobs wrote before W16. The queue is
retired: this entry stays so an old command says what to do instead of failing with a bare error."""

import sys

#: The command that still drains an old queue: a CLI that shipped the drain (0.466.0 through the release before the
#: retirement; 0.469.0 is the one this names).
DRAIN_COMMAND = "uv run --no-project --with 'probe-research==0.469.0' python -m probe.integrations.miles <queue_dir>"


def main() -> int:
    sys.stderr.write(
        "probe: the Miles metric queue was retired (RL plan W16; new runs send through each process's own outbox), "
        "and this CLI no longer drains one. To send a queue an older job left, run it with a CLI that still does:\n"
        f"  {DRAIN_COMMAND}\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
