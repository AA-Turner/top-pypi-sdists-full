"""A LIBERO checkpoint trained on one suite (the catalog's runs_on detail): the sim runs that
suite only."""

from __future__ import annotations

from dreamscale_transport import catalog


def sim_task(model, benchmark, suite):
    entry = catalog.entry(model)
    trained = {place.detail for place in entry.runs_on if place.detail}
    if trained and suite not in trained:
        raise ValueError(f"{entry.client.refusal_name}'s LIBERO checkpoint supports "
                         f"--task-suite {min(trained)}.")
