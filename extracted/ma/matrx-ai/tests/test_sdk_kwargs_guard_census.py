"""CENSUS GUARD — every provider adapter that forwards a dict blind into an SDK
method (``sdk.method(**kwargs)``) must do so through ``route_undeclared_params``.

Fix-the-class for the 2026-09-09 anthropic 1.4.0 outage: the SDKs in this repo
float as "latest", so any of them can drop a keyword on any bump. A bare
``**kwargs`` forward is the whole defect class; this test makes a new one fail
CI the moment it is written.

Proven failing-then-passing: with the guard call removed from any site below,
this test names the file:line.
"""

from __future__ import annotations

import re
from pathlib import Path

PROVIDERS = Path(__file__).resolve().parents[1] / "matrx_ai" / "providers"

# ``<something>.<sdk_method>(**<dict>`` — a blind forward. ``asyncio.to_thread(fn, **d)``
# is the same thing one hop removed.
_BLIND_FORWARD = re.compile(
    r"(?:\.\w+\(\s*\*\*|to_thread\(\s*[\w.]+\s*,\s*\*\*)(?P<arg>[\w.]+)\s*[,)]"
)
_GUARDED = "route_undeclared_params("

# Dict-forwarding calls that are NOT provider SDK entry points.
_ALLOWED_TARGETS = {
    "dict(",  # dict(**x) copies
    "replace(",  # dataclasses.replace(obj, **changes)
    "model_copy(",
    "model_validate(",
    "Adjustment(",
    "WarningPayload(",
    "InfoPayload(",
}


_SDK_CLIENT = r"(self\.client|_client\(\)|get_\w+_client\(\))"
# ``_stream = self.client.aio.models.generate_content_stream`` — a local alias of an
# SDK method. A later ``_stream(**cfg)`` is the same blind forward one name removed.
_SDK_ALIAS = re.compile(r"^\s*(?P<alias>\w+)\s*=\s*" + _SDK_CLIENT + r"[\w.]*\s*$", re.M)
# ``alias(**cfg`` / ``await alias(**cfg``
_ALIAS_FORWARD = re.compile(r"(?<![\w.])(?P<alias>\w+)\(\s*\*\*(?P<arg>[\w.]+)\s*[,)]")


def _blind_forwards() -> list[str]:
    offenders: list[str] = []
    for path in sorted(PROVIDERS.rglob("*.py")):
        if "/tests/" in str(path) or path.name == "sdk_drift.py":
            continue
        text = path.read_text(encoding="utf-8")
        aliases = {m.group("alias") for m in _SDK_ALIAS.finditer(text)}
        matches = [(m, m.group("arg"), False) for m in _BLIND_FORWARD.finditer(text)]
        matches += [
            (m, m.group("arg"), True)
            for m in _ALIAS_FORWARD.finditer(text)
            if m.group("alias") in aliases
        ]
        for match, arg, via_alias in sorted(matches, key=lambda item: item[0].start()):
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_no = text.count("\n", 0, match.start()) + 1
            # the statement: from the line start to the closing paren of this call
            stmt = text[line_start : match.end() + 400]
            head = text[line_start : match.start() + 1]
            if any(t in head for t in _ALLOWED_TARGETS):
                continue
            if not via_alias and not re.search(_SDK_CLIENT, head + match.group(0)):
                continue  # not an SDK client call (helpers, pydantic, our own functions)
            if _GUARDED in arg or _GUARDED in stmt.split("\n\n", 1)[0]:
                continue
            offenders.append(
                f"{path.relative_to(PROVIDERS.parent.parent)}:{line_no}: {stmt.splitlines()[0].strip()}"
            )
    return offenders


def test_every_blind_sdk_forward_goes_through_the_drift_guard() -> None:
    offenders = _blind_forwards()
    assert not offenders, (
        "provider adapters forwarding a dict blind into an SDK method without "
        "route_undeclared_params(...) — an SDK bump turns any of these into a "
        "client-side TypeError:\n  " + "\n  ".join(offenders)
    )


def test_the_census_guard_still_bites(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "providers" / "fake"
    fake.mkdir(parents=True)
    (fake / "fake_api.py").write_text(
        "class X:\n    async def go(self, config_data):\n"
        "        return await self.client.chat.completions.create(**config_data)\n"
        "\n    async def aliased(self, config_data):\n"
        "        _stream = self.client.aio.models.generate_content_stream\n"
        "        async for chunk in await _stream(**config_data):\n"
        "            yield chunk\n"
        "\n    def fine(self, config_data):\n"
        "        return dict(**config_data)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("test_sdk_kwargs_guard_census.PROVIDERS", tmp_path / "providers")
    offenders = _blind_forwards()
    assert len(offenders) == 2, offenders
    assert "fake_api.py:3" in offenders[0]
    assert "fake_api.py:7" in offenders[1] and "_stream(**config_data)" in offenders[1]
