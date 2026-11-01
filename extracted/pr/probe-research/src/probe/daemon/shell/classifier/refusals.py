"""agent/src/probe/daemon/shell/shell.py."""

from __future__ import annotations
_R_HEREDOC = (
    "Heredocs are allowed only as `cat > FILE <<'TAG'` into the notes folder, as the whole command."
)
_R_SCRAMBLE = (
    "{what} changes text (a key included) into characters the output scrubber can't recognise."
)


class _Refuse(Exception):
    """Raised inside the classifier; the message is the Verdict's reason."""


class _Fix(_Refuse):
    """A read one flag away from safe (`git log` without `--no-textconv
    --no-ext-diff`): not a question for the researcher -- the daemon adds the
    flag itself -- so it answers "not run" with what to add (bypass mode runs it)."""


class _Never(_Refuse):
    """A refusal no one can wave through: never held as a question, and not
    auto-approved in bypass mode either. For what would step around the daemon's
    own guarded paths -- Probe's key and state files, and `probe` run from the
    shell instead of the probe tool (its pre-check, lease and logbook)."""
