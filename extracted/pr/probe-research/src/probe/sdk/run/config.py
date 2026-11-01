"""RunConfig (run.config: a dict whose writes merge through the run, W&B wandb_config.Config) and
ConfigMixin, Run's methods that read and update it."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ...foundation.safe_warn import safe_warn as _diagnostics
from ..values import values as _coerce
from .. import errors

if TYPE_CHECKING:  # Run only in annotations: importing it here would loop back into run.py
    from .run import Run


class RunConfig(dict):
    """``run.config`` (plan (c)): the run's config as a dict whose writes merge
    into the stored config through :meth:`Run.update_config`.

    Reads come from this handle's copy. Writes -- ``cfg["lr"] = ...``,
    ``cfg.update(...)``, ``cfg.setdefault(...)``, ``cfg.lr = ...`` -- are sent
    first and then reflected here. Removing a key raises ``TypeError``: the
    server merges, it never deletes, so a local delete would be a lie."""

    __slots__ = ("_run",)

    def __init__(self, run: "Run") -> None:
        super().__init__(run._data.get("config") or {})
        object.__setattr__(self, "_run", run)

    def _merge(self, values: dict) -> None:
        # stacklevel 4: _update_config <- _merge <- the dict method <- the caller.
        self._run._update_config(values, allow_val_change=None, strict=None, stacklevel=4)
        super().clear()
        super().update(self._run._data.get("config") or {})

    def __setitem__(self, key: Any, value: Any) -> None:
        self._merge({key: value})

    def update(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        # `run.config.update(args)` with an argparse Namespace is THE W&B
        # pattern (#2032 review): coerce anything config-shaped first; only a
        # plain iterable of pairs takes dict()'s path.
        values: dict = {}
        for arg in args:
            try:
                values.update(_coerce.to_config(arg))
            except errors.ValidationError:
                values.update(dict(arg))
        values.update(kwargs)
        self._merge(values)

    def __ior__(self, other: Any) -> "RunConfig":
        # `cfg |= {...}` would otherwise update only this local copy.
        self.update(other)
        return self

    def __reduce__(self) -> tuple:
        # copy.copy / deepcopy / pickle give a plain dict snapshot: a copy must
        # not send writes, and reconstructing this class would (#2032 review).
        return (dict, (dict(self),))

    def setdefault(self, key: Any, default: Any = None) -> Any:
        if key not in self:
            self._merge({key: default})
        return self.get(key, default)

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, value: Any) -> None:
        self._merge({name: value})

    def _no_removal(self, *_args: Any, **_kwargs: Any) -> Any:
        raise TypeError(
            "probe: a run's config only merges; keys cannot be removed "
            "(set the key to None instead)"
        )

    __delitem__ = pop = popitem = clear = __delattr__ = _no_removal  # type: ignore[assignment]


class ConfigMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- config (plan (c)) ---------------------------------------------------
    @property
    def config(self) -> "RunConfig":
        """This run's config as a dict: reads are local, writes are not.
        ``run.config["lr"] = 3e-4``, ``run.config.update({...})`` and
        ``run.config.lr = 3e-4`` all merge into the stored config through
        :meth:`update_config`. Keys can be added and changed, never removed:
        the server merges, it never deletes."""
        return RunConfig(self)

    def update_config(
        self,
        values: Any,
        *,
        allow_val_change: bool | None = None,
        strict: bool | None = None,
    ):
        """Merge ``values`` into this run's config after it started (plan (c)).

        Shallow and new-wins, like W&B's ``run.config.update``: each top-level
        key replaces the stored one whole, and keys not named are untouched.
        ``values`` is anything ``config=`` takes -- a dict, a Hydra
        ``DictConfig``, an ``argparse.Namespace``, a dataclass, a pydantic
        model -- coerced to plain JSON first (:mod:`probe.sdk.values.values`).

        A key whose value CHANGES warns once per key per run and the new value
        wins; ``allow_val_change=True`` changes it quietly, and
        ``allow_val_change=False`` refuses the whole update with
        ``ValidationError`` before anything is sent (W&B's default). Fail-open
        and journaled like every write; ``strict=True`` raises instead.

        Needs a server that serves ``run_config_merge``. An older one accepts
        the request and silently drops the field, so the SDK does not send it:
        it warns once per run and returns None (``strict=True``:
        ``CapabilityUnavailable``). When the server cannot be asked at all, the
        update is sent anyway -- an older server drops it harmlessly, a newer
        one stores it."""
        return self._update_config(
            values, allow_val_change=allow_val_change, strict=strict, stacklevel=3
        )

    def _update_config(
        self,
        values: Any,
        *,
        allow_val_change: bool | None,
        strict: bool | None,
        stacklevel: int,
    ):
        plain = _coerce.to_config(values)
        if not plain:
            return None
        # Compare and print only what goes over the wire (#2032 review): the
        # stored config is scrubbed, so a raw value under a credential key
        # always looked "changed", and the warning printed the raw secret into
        # stderr -- which the run log uploads.
        # scanning disabled: wire = default_scrub(plain)
        wire = plain
        if not isinstance(wire, dict):
            return None
        current = self._data.get("config") or {}
        changed = sorted(k for k, v in wire.items() if k in current and current[k] != v)
        if changed and allow_val_change is False:
            raise errors.ValidationError(
                f"config key(s) {changed} already have different values on this run; "
                "pass allow_val_change=True to change them"
            )
        if changed and allow_val_change is None:
            for key in changed:
                if key in self._config_warned:
                    continue
                self._config_warned.add(key)
                _diagnostics.warn(
                    f"probe: config {key!r} changed from {_diagnostics.describe(current[key])} "
                    f"to {_diagnostics.describe(wire[key])}; the new value wins. Pass "
                    "allow_val_change=True to change it without this warning.",
                    stacklevel=stacklevel,
                )
        try:
            supported = self._client.supports_feature("run_config_merge")
        except Exception:  # noqa: BLE001 -- cannot ask: send anyway (see update_config)
            supported = True
        if not supported:
            if strict:
                raise errors.CapabilityUnavailable(
                    "run_config_merge",
                    "this Probe server cannot merge a run's config after it started "
                    "(feature run_config_merge); pass config= when the run is created",
                )
            if not self._config_merge_refused:
                self._config_merge_refused = True
                _diagnostics.warn(
                    "probe: this Probe server cannot merge a run's config after it "
                    f"started (feature run_config_merge), so {sorted(plain)} were not "
                    "recorded. Pass config= when the run is created, or upgrade the server.",
                    stacklevel=stacklevel,
                )
            return None
        self._data["config"] = {**current, **wire}
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"config_merge": plain}, strict=strict
        )
        if isinstance(data, dict) and isinstance(data.get("config"), dict):
            self._data["config"] = data["config"]
        return data
