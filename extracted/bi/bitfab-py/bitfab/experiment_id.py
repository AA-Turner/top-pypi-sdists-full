"""Accept the deprecated ``test_run_id`` spelling alongside ``experiment_id``."""

from bitfab.warn_once import warn_once


def resolve_experiment_id(
    experiment_id: str | None, test_run_id: str | None, *, where: str
) -> str | None:
    """Return the experiment ID passed under either name.

    ``test_run_id`` is the deprecated name and warns once per call site.

    Raises:
        ValueError: If both names are passed with different values.
    """
    if test_run_id is None:
        return experiment_id
    warn_once(
        f"deprecated-test-run-id:{where}",
        f"{where}(test_run_id=...) is deprecated; pass experiment_id=... instead.",
    )
    if experiment_id is not None and experiment_id != test_run_id:
        raise ValueError(
            f"{where} received experiment_id={experiment_id!r} and the deprecated "
            f"test_run_id={test_run_id!r}. Pass only experiment_id."
        )
    return test_run_id
