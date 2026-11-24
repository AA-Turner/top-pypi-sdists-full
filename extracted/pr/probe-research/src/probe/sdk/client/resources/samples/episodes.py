"""EpisodesMixin, Client's methods: a run's episodes one step at a time, one episode whole, and the episode an old
rollout link opens, each a dict as the route answers it (twin: app/runs/samples/episodes)."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote


def _quote(value: Any) -> str:
    return quote(str(value), safe="")


class EpisodesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_episodes(self, run_id: str, *, step: int | None = None, split: str | None = None,
                      group_by: str | None = None, cursor: str | None = None, limit: int | None = None) -> dict:  # fmt: skip
        """`GET /v1/runs/{id}/episodes`: one step's episodes (the latest when no ``step``) and the run's steps
        (`EpisodeList`). ``group_by``: episode, environment or recent_rollouts; pass back `next_cursor`."""
        values = (("step", step), ("split", split), ("group_by", group_by), ("cursor", cursor), ("limit", limit))
        query = {name: value for name, value in values if value is not None}
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/episodes", params=query or None)

    def get_episode(self, run_id: str, episode_key: str) -> dict:
        """`GET /v1/runs/{id}/episodes/{key}`: one episode whole, its rollouts, branches and turns (`EpisodeDetail`)."""
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/episodes/{_quote(episode_key)}")

    def find_episode(self, run_id: str, *, sample_id: str | None = None, key: str | None = None,
                     span_id: str | None = None) -> dict:  # fmt: skip
        """`GET /v1/runs/{id}/episodes/find`: the episode a sample id, a producer/attempt key or an old trial link's
        rollout span belongs to (`EpisodeLink`)."""
        values = (("sample", sample_id), ("key", key), ("span", span_id))
        query = {name: value for name, value in values if value is not None}
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/episodes/find", params=query)
