"""ServerFeaturesMixin, Client's methods: ask whether the server supports a feature (route present,
team flag) before relying on it."""

from __future__ import annotations

from .. import errors


def _route_absent(exc: errors.RosError) -> bool:
    """FastAPI's own 404 for a path no route matches: an older server."""
    return isinstance(exc, errors.NotFoundError) and exc.detail == "Not Found"


class ServerFeaturesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- server capabilities (0185) -----------------------------------------
    def _require_dry_run_delete(self) -> None:
        """A dry-run delete only on a server with the trash (0261): an older one
        ignores `?dry_run=true` and the same DELETE removes for good."""
        if not self.supports_feature("trash"):
            raise errors.RosError("this Probe server has no trash, so a delete has no dry run")

    def supports_feature(self, name: str) -> bool:
        """Whether the connected server declares ``name`` in
        ``GET /v1/server/features``.

        Cached for the client's lifetime: the answer is a property of the
        deployed build, and one process talks to one deployment. A 404 on the
        route itself IS the answer — a server too old to have the route is too
        old to have any feature the route would declare."""
        feats = getattr(self, "_server_features_cache", None)
        if feats is None:
            try:
                data = self.transport.get("/v1/server/features")
                feats = frozenset((data or {}).get("features") or ())
            except errors.NotFoundError:
                feats = frozenset()
            self._server_features_cache = feats
        return name in feats

    def _forget_server_features(self) -> None:
        """Ask again on the next look, for a client kept longer than one deployment may live:
        the outbox worker's (I13), reused across its passes."""
        self._server_features_cache = None
        self._team_features_cache = None

    def supports_team_feature(self, name: str) -> bool:
        """Whether ``GET /v1/teams/features`` lists ``name`` for this client's team.

        A per-team switch (a canary list on the server), unlike
        :meth:`supports_feature`'s per-build list. An answer is cached for the
        client's lifetime, and so is an older server's 404 (no such route). Any
        other failure -- no credential, a 5xx, the network -- is "not enabled"
        THIS time and asked again next time, so one blip does not switch a
        long-lived process off for good."""
        try:
            return name in self._fetch_team_features()
        except Exception:  # noqa: BLE001 -- unknown is not enabled, and not remembered
            return False

    def _fetch_team_features(self) -> frozenset[str]:
        """``GET /v1/teams/features``'s listing, cached as :meth:`supports_team_feature` says.
        Raises what the read raised on any other failure, remembering nothing: for a caller
        that must tell "not on" from "could not ask"."""
        feats = getattr(self, "_team_features_cache", None)
        if feats is None:
            try:
                data = self.transport.get("/v1/teams/features")
                feats = frozenset((data or {}).get("features") or ())
            except errors.NotFoundError:
                feats = frozenset()
            self._team_features_cache = feats
        return feats

    def _require_feature(self, name: str, message: str) -> None:
        """Preflight gate: refuse BEFORE any state changes, with the fix named.

        Exists for requests whose worst failure is a server silently ignoring
        an unknown field — for those, discovering skew after the write is
        discovering it too late."""
        if not self.supports_feature(name):
            raise errors.NotFoundError(message)
