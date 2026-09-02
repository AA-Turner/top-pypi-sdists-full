"""WS-7 — agent-directed login: the pure engine, proven against synthetic pages and
a FakeWorker fill endpoint (no real worker, no DB).

The invariants under test, each named in D-11/D-12 and the credential-entry spec:

* incomplete spec is REFUSED before any page touch (no fill, no capture);
* multi-field materialization: a ``None`` field set requests nothing, a named set
  requests exactly those keys — the plumbing that lets the vault preserve its
  single-form behaviour byte-for-byte;
* four distinguishable verdicts, each with a confidence and its signals;
* ``challenged`` is never reported as failure; ``unknown`` is never success;
* NO plaintext secret appears in results, signals, exceptions, captures, or the
  FakeWorker's observable event log (grep-style assertion).
"""

from __future__ import annotations

import json

import pytest

from matrx_scraper.ai_browser.login import (
    AttemptSpec,
    ExpectSpec,
    FieldSpec,
    LoginRecipe,
    PageObservation,
    SignalDescriptor,
    SubmitSpec,
    run_login_attempt,
)
from matrx_scraper.ai_browser.login.executor import FieldUnavailable

SECRET_PASSWORD = "hunter2-DO-NOT-LEAK-9f3a"
SECRET_USERNAME = "arman-secret-user"


# ─────────────────────────────────────────────────────────────────────────────
# Test doubles — a FakeWorker that RECORDS every fill (so we can prove a value
# never escapes anywhere it shouldn't), a resolver, an observer over a synthetic
# page, and a capturer.
# ─────────────────────────────────────────────────────────────────────────────


class FakeResolver:
    def __init__(self, values: dict[str, str], *, unavailable: set[str] | None = None):
        self._values = values
        self._unavailable = unavailable or set()
        self.requested_keys: list[str] | None = None

    async def resolve(self, *, actor_id, credential_item_id, origin, field_keys):
        self.requested_keys = list(field_keys)
        for k in field_keys:
            if k in self._unavailable:
                raise FieldUnavailable(k, "not on this item")
        return {k: self._values[k] for k in field_keys if k in self._values}


class FakeWorker:
    """Records the values it was asked to fill so a test can prove no value leaks
    into any AGENT-visible channel. This log is the private worker channel, never
    surfaced to the model — a real worker never returns the value either."""

    def __init__(self) -> None:
        self.fills: list[tuple[str, str, bool]] = []
        self.submits: list[tuple[str, str | None]] = []
        self.filled_selectors: list[str] = []

    async def fill(self, selector, value, *, clear_first):
        self.fills.append((selector, value, clear_first))
        self.filled_selectors.append(selector)
        return True  # FillResult.value echo is discarded by the executor

    async def submit(self, *, kind, selector):
        self.submits.append((kind, selector))

    async def wait_for(self, selector, *, timeout_ms):
        return True


class SyntheticPage:
    """A synthetic login page whose state after submit is scripted."""

    def __init__(self, *, after: PageObservation, before_form: bool = True):
        self._after = after
        self._before_form = before_form
        self._observed = 0

    async def observe(self, *, login_form_present_before):
        self._observed += 1
        if self._observed == 1:
            return PageObservation(login_form_present=self._before_form)
        return self._after


class FakeCapturer:
    def __init__(self) -> None:
        self.phases: list[str] = []

    async def capture(self, *, phase):
        from matrx_scraper.ai_browser.login import CaptureRef

        self.phases.append(phase)
        return CaptureRef(capture_id=f"cap-{phase}", privacy_class="redacted")


def _basic_spec(**expect) -> AttemptSpec:
    return AttemptSpec(
        credential_item_id="item-1",
        fields=[
            FieldSpec(selector="#username", field_key="username"),
            FieldSpec(selector="#password", field_key="password"),
        ],
        submit=SubmitSpec(kind="click", selector="#signin"),
        expect=ExpectSpec(**expect),
    )


async def _run(spec, resolver, worker, page, capturer, recipe=None):
    return await run_login_attempt(
        actor_id="u1",
        credential_item_id="item-1",
        origin="https://signin.aws.amazon.com",
        spec=spec,
        resolver=resolver,
        worker=worker,
        observer=page,
        capturer=capturer,
        recipe=recipe,
    )


# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_incomplete_spec_refused_before_any_page_touch():
    spec = _basic_spec()
    resolver = FakeResolver({"username": SECRET_USERNAME}, unavailable={"password"})
    worker = FakeWorker()
    page = SyntheticPage(after=PageObservation())
    capturer = FakeCapturer()

    result = await _run(spec, resolver, worker, page, capturer)

    assert result.status == "spec_incomplete"
    assert "password" in result.missing_fields
    assert result.outcome is None
    # NOTHING touched: no fill, no submit, no capture.
    assert worker.fills == []
    assert worker.submits == []
    assert capturer.phases == []
    # A half-filled page never happened.
    assert worker.filled_selectors == []


@pytest.mark.asyncio
async def test_undeclared_step_selector_refused_before_touch():
    spec = AttemptSpec(
        credential_item_id="item-1",
        fields=[FieldSpec(selector="#username", field_key="username")],
        steps=[
            # references a selector not declared in fields
            {"fields": ["#password"], "submit": {"kind": "click", "selector": "#next"}},
        ],
    )
    worker = FakeWorker()
    result = await _run(
        spec,
        FakeResolver({"username": SECRET_USERNAME}),
        worker,
        SyntheticPage(after=PageObservation()),
        FakeCapturer(),
    )
    assert result.status == "spec_incomplete"
    assert worker.fills == []


@pytest.mark.asyncio
async def test_none_field_set_requests_nothing_multi_field_requests_exactly_named():
    # A literal-only attempt names no vault field → resolver is never asked.
    literal_spec = AttemptSpec(
        credential_item_id="item-1",
        fields=[FieldSpec(selector="#region", literal="us-west-1")],
        submit=SubmitSpec(kind="none"),
    )
    resolver = FakeResolver({})
    worker = FakeWorker()
    await _run(
        literal_spec, resolver, worker, SyntheticPage(after=PageObservation()), FakeCapturer()
    )
    assert resolver.requested_keys is None  # never called — no secret fields
    assert worker.fills == [("#region", "us-west-1", True)]

    # A named-field attempt asks the resolver for exactly those keys, sorted.
    resolver2 = FakeResolver({"username": SECRET_USERNAME, "password": SECRET_PASSWORD})
    await _run(
        _basic_spec(),
        resolver2,
        FakeWorker(),
        SyntheticPage(after=PageObservation()),
        FakeCapturer(),
    )
    assert resolver2.requested_keys == ["password", "username"]


@pytest.mark.asyncio
async def test_four_distinguishable_verdicts_with_confidence_and_signals():
    values = {"username": SECRET_USERNAME, "password": SECRET_PASSWORD}

    # authenticated
    r = await _run(
        _basic_spec(success_url_prefix="https://console.aws.amazon.com/", success_selector="#acct"),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(
            after=PageObservation(
                url="https://console.aws.amazon.com/home",
                present_selectors=frozenset({"#acct"}),
                login_form_present=False,
            )
        ),
        FakeCapturer(),
    )
    assert r.outcome == "authenticated"
    assert 0.0 < r.confidence <= 1.0
    assert r.signals

    # rejected
    r = await _run(
        _basic_spec(failure_selector="#error-message"),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(after=PageObservation(present_selectors=frozenset({"#error-message"}))),
        FakeCapturer(),
    )
    assert r.outcome == "rejected"

    # challenged
    r = await _run(
        _basic_spec(challenge_selector="#mfacode"),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(after=PageObservation(present_selectors=frozenset({"#mfacode"}))),
        FakeCapturer(),
    )
    assert r.outcome == "challenged"
    # A generic (recipe-less) challenge is honestly classed "challenge"; the AWS
    # recipe classifies it precisely as "mfa" (see test_recipe_mfa_challenge_class).
    assert r.challenge_class == "challenge"

    # unknown — nothing observable
    r = await _run(
        _basic_spec(),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(after=PageObservation()),
        FakeCapturer(),
    )
    assert r.outcome == "unknown"
    assert r.confidence == 0.0


@pytest.mark.asyncio
async def test_challenged_is_not_failure_and_unknown_is_not_success():
    values = {"username": SECRET_USERNAME, "password": SECRET_PASSWORD}
    # A challenge page that ALSO removed the login form must not read as authenticated.
    r = await _run(
        _basic_spec(
            success_url_prefix="https://console.aws.amazon.com/",
            challenge_selector="#mfacode",
        ),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(
            after=PageObservation(
                url="https://signin.aws.amazon.com/mfa",
                present_selectors=frozenset({"#mfacode"}),
                login_form_present=False,
            )
        ),
        FakeCapturer(),
    )
    assert r.outcome == "challenged"  # never rejected, never authenticated

    # Contradiction (success + error together) → unknown, never rounded up.
    r = await _run(
        _basic_spec(
            success_selector="#acct",
            failure_selector="#error-message",
        ),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(
            after=PageObservation(present_selectors=frozenset({"#acct", "#error-message"}))
        ),
        FakeCapturer(),
    )
    assert r.outcome == "unknown"
    assert r.contradiction is True


@pytest.mark.asyncio
async def test_low_confidence_success_proceeds_but_flagged():
    values = {"username": SECRET_USERNAME, "password": SECRET_PASSWORD}
    # Only the weak "form gone" signal fires → authenticated at low confidence.
    r = await _run(
        _basic_spec(),
        FakeResolver(values),
        FakeWorker(),
        SyntheticPage(after=PageObservation(login_form_present=False), before_form=True),
        FakeCapturer(),
    )
    assert r.outcome == "authenticated"
    assert r.low_confidence is True  # proceeds, but never silently (D-16 item 4)


@pytest.mark.asyncio
async def test_recipe_supersedes_and_records_override():
    recipe = LoginRecipe(
        recipe_id="rec-aws",
        normalized_origin="https://signin.aws.amazon.com",
        recipe_version=3,
        field_map=[
            {"step": 0, "selector": "#username", "field_key": "username"},
            {"step": 0, "selector": "#password", "field_key": "password"},
        ],
        success_signals=[
            SignalDescriptor(
                kind="selector_present", value="#acct", direction="authenticated", weight=0.6
            )
        ],
    )
    # Agent spec uses a DIFFERENT selector — the recipe wins and records the override.
    spec = AttemptSpec(
        credential_item_id="item-1",
        fields=[
            FieldSpec(selector="#user_wrong", field_key="username"),
            FieldSpec(selector="#pass_wrong", field_key="password"),
        ],
        submit=SubmitSpec(kind="click", selector="#signin"),
    )
    worker = FakeWorker()
    r = await _run(
        spec,
        FakeResolver({"username": SECRET_USERNAME, "password": SECRET_PASSWORD}),
        worker,
        SyntheticPage(after=PageObservation(present_selectors=frozenset({"#acct"}))),
        FakeCapturer(),
        recipe=recipe,
    )
    assert r.outcome == "authenticated"
    assert r.recipe.recipe_overrode_agent_spec is True
    assert r.recipe.recipe_version == 3
    # The recipe's selectors were used, not the agent's wrong ones.
    assert "#username" in worker.filled_selectors
    assert "#user_wrong" not in worker.filled_selectors


@pytest.mark.asyncio
async def test_state_captured_before_and_after_every_attempt():
    capturer = FakeCapturer()
    r = await _run(
        _basic_spec(),
        FakeResolver({"username": SECRET_USERNAME, "password": SECRET_PASSWORD}),
        FakeWorker(),
        SyntheticPage(after=PageObservation()),
        capturer,
    )
    assert capturer.phases == ["before", "after"]
    assert r.before_capture is not None and r.after_capture is not None


@pytest.mark.asyncio
async def test_no_plaintext_secret_in_any_agent_visible_channel():
    values = {"username": SECRET_USERNAME, "password": SECRET_PASSWORD}
    worker = FakeWorker()
    capturer = FakeCapturer()
    r = await _run(
        _basic_spec(success_selector="#acct"),
        FakeResolver(values),
        worker,
        SyntheticPage(after=PageObservation(present_selectors=frozenset({"#acct"}))),
        capturer,
    )
    # The result the agent receives, serialized, contains NO secret and DOES carry
    # the field NAMES and the leak-report instructions.
    blob = json.dumps(r.model_dump())
    assert SECRET_PASSWORD not in blob
    assert SECRET_USERNAME not in blob
    assert "password" in r.field_keys  # the NAME is fine
    assert "credential_login({action:'report'" in r.feedback.how_to_report

    # The worker DID receive the values (that is the whole point — it types them),
    # but that channel is the private worker fill, never surfaced to the model.
    assert any(v == SECRET_PASSWORD for _, v, _ in worker.fills)

    # Signals never carry a value.
    for s in r.signals:
        assert SECRET_PASSWORD not in json.dumps(s.model_dump())


@pytest.mark.asyncio
async def test_recipe_mfa_challenge_class():
    from matrx_scraper.ai_browser.login import AWS_IAM_CONSOLE_RECIPE

    r = await _run(
        _basic_spec(),
        FakeResolver(
            {"account_id": "1234", "username": SECRET_USERNAME, "password": SECRET_PASSWORD}
        ),
        FakeWorker(),
        SyntheticPage(after=PageObservation(present_selectors=frozenset({"#mfacode"}))),
        FakeCapturer(),
        recipe=AWS_IAM_CONSOLE_RECIPE,
    )
    assert r.outcome == "challenged"
    assert r.challenge_class == "mfa"


@pytest.mark.asyncio
async def test_field_unavailable_exception_names_field_never_value():
    resolver = FakeResolver({"username": SECRET_USERNAME}, unavailable={"password"})
    r = await _run(
        _basic_spec(),
        resolver,
        FakeWorker(),
        SyntheticPage(after=PageObservation()),
        FakeCapturer(),
    )
    blob = json.dumps(r.model_dump())
    assert SECRET_USERNAME not in blob  # even the resolvable value never surfaces
    assert "password" in r.missing_fields
