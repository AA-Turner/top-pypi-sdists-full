"""What model and reasoning effort an import's agents run at, and what they cost.

`import_agent_settings.resolve` decides it once per import process, field by
field: env (`PROBE_IMPORT_AGENT_SETTINGS`) over the server
(`GET /v1/import-jobs/agent-settings`) over BUILTIN. What is pinned here:

  * NO ANSWER IS TODAY'S ARGV. Every way the server read can fail lands on the
    builtin settings, and those produce, for every agent and lane, the argv
    the import sent before this module existed.
  * One bad field is dropped; the rest of the map is kept.
  * The meter never reports unknown usage as 0, and reaches both summary
    events: `backfill.summary` (the foreground import) and
    `import_job.finished` (each background worker attempt, failures included).

The server read is replaced by a fake transport (`real_import_agent_settings`
turns off the suite-wide stub); the real HTTP stack is not under test here.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_record
from probe.cli import import_agent_settings as settings_mod
from probe.cli.import_agent_settings import ENV_VAR, Lane, Meter, Source

pytestmark = pytest.mark.usefixtures("real_import_agent_settings")


class _Transport:
    def __init__(self, answer):
        self.answer, self.calls, self.deadlines = answer, 0, []

    def get(self, path):
        from probe.sdk import transport

        assert path == "/v1/import-jobs/agent-settings"
        self.calls += 1
        self.deadlines.append(transport._request_deadline.get())
        if isinstance(self.answer, BaseException):
            raise self.answer
        return self.answer


class _Client:
    def __init__(self, answer):
        self.transport = _Transport(answer)


def _server(settings, version="v1"):
    return _Client({"settings": settings, "version": version})


def _resolve(client, agent=bf.Agent.CODEX, env=None, meter=None):
    environ = {ENV_VAR: json.dumps(env)} if env is not None else {}
    return settings_mod.resolve(client, agent, meter=meter, environ=environ)


# -- precedence ---------------------------------------------------------------


def test_env_wins_over_server_wins_over_builtin_field_by_field():
    server = _server({"claude": {"*": {"effort": "low"}, "record": {"effort": "high"},
                                 "import": {"model": "opus"}}})
    env = {"claude": {"import": {"effort": "max"}}}
    agents = _resolve(server, bf.Agent.CLAUDE, env)
    assert agents.lane(Lane.CLASSIFY) == settings_mod.LaneSettings(
        Lane.CLASSIFY, None, "low", Source.SERVER)
    # Env's effort, the server's model: per field, not per lane.
    assert (agents.lane(Lane.IMPORT).model, agents.lane(Lane.IMPORT).effort) == ("opus", "max")
    assert agents.lane(Lane.IMPORT).source is Source.ENV
    # A named lane beats `*` within one source; the builtin model survives.
    record = agents.lane(Lane.RECORD)
    assert (record.model, record.effort, record.source) == ("sonnet", "high", Source.SERVER)
    assert record.builtin_model == "sonnet"
    assert agents.version == "v1"


def test_env_every_lane_beats_a_named_server_lane():
    """First hit wins by SOURCE, then by lane: a machine's own override is the
    escape hatch, so it is not undercut by a narrower server key."""
    agents = _resolve(_server({"codex": {"classify": {"effort": "low"}}}),
                      env={"codex": {"*": {"effort": "xhigh"}}})
    assert agents.lane(Lane.CLASSIFY).effort == "xhigh"


def test_an_agent_the_map_does_not_name_runs_as_built_in():
    agents = _resolve(_server({"codex": {"*": {"effort": "medium"}}}), bf.Agent.CLAUDE)
    assert all(agents.lane(lane).source is Source.BUILTIN for lane in Lane)
    assert agents.lane(Lane.CLASSIFY).effort is None
    assert agents.lane(Lane.RECORD).model == "sonnet"


# -- no answer is today's argv ------------------------------------------------


_MAIN_MODEL = {  # what each lane sent before settings existed (the claims draft's MODEL, now the record lane's)
    (bf.Agent.CLAUDE, Lane.RECORD): "sonnet",
}


@pytest.mark.parametrize("answer", [
    ConnectionError("unreachable"),
    TimeoutError("timed out"),
    RuntimeError("404 Not Found"),  # a self-hosted API without the route
    {"detail": "Not Found"},
    {"settings": "not a map"},
    ["a", "list"],
    None,
])
@pytest.mark.parametrize("agent", [bf.Agent.CLAUDE, bf.Agent.CODEX])
def test_every_failed_read_launches_exactly_as_before(monkeypatch, answer, agent):
    monkeypatch.setattr(bf, "codex_features", lambda binary: None)
    agents = _resolve(_Client(answer), agent)
    assert agents.version is None
    for lane in Lane:
        settings = agents.lane(lane)
        assert settings.source is Source.BUILTIN
        kwargs = dict(workdir=Path("/w"), session_id="s", tools=backfill_record.RECORD_TOOLS
                      if lane is Lane.RECORD and agent is bf.Agent.CLAUDE else None)
        today = bf.agent_argv(agent, f"/bin/{agent.value}", Path("/f"),
                              model=_MAIN_MODEL.get((agent, lane)), **kwargs)
        now = bf.agent_argv(agent, f"/bin/{agent.value}", Path("/f"),
                            model=settings.model, effort=settings.effort, **kwargs)
        assert now == today, (agent, lane)


def test_a_client_without_a_transport_is_no_answer():
    assert _resolve(object()).lane(Lane.IMPORT).source is Source.BUILTIN


def test_the_read_is_bounded_by_one_deadline():
    client = _server({})
    before = time.monotonic()
    _resolve(client)
    (deadline,) = client.transport.deadlines
    assert before + settings_mod.READ_TIMEOUT_S <= deadline <= time.monotonic() + settings_mod.READ_TIMEOUT_S


def test_settings_are_read_once_per_meter():
    """A background worker re-enters its job within one attempt (a connection
    retry); it asks the server once."""
    client, meter = _server({"codex": {"*": {"effort": "low"}}}), Meter()
    first = _resolve(client, meter=meter)
    assert _resolve(client, meter=meter) is first and client.transport.calls == 1


# -- per-field validation -------------------------------------------------------


def test_a_bad_field_is_dropped_and_the_rest_kept():
    server = _server({"codex": {
        "classify": {"effort": "bogus", "model": "gpt-6"},
        "import": {"effort": "low", "temperature": "0"},
        "summaries": {"effort": "low"},
        "record": {"model": "-c", "effort": "minimal"},
    }})
    agents = _resolve(server)
    assert (agents.lane(Lane.CLASSIFY).model, agents.lane(Lane.CLASSIFY).effort) == ("gpt-6", None)
    assert agents.lane(Lane.IMPORT).effort == "low"
    assert (agents.lane(Lane.RECORD).model, agents.lane(Lane.RECORD).effort) == (None, "minimal")
    assert agents.dropped == 4
    assert agents.notes == (), "a server field the CLI cannot take is not the researcher's doing"


def test_an_effort_is_checked_against_its_own_agents_list():
    agents = _resolve(_server({"claude": {"*": {"effort": "minimal"}}}), bf.Agent.CLAUDE)
    assert agents.lane(Lane.CLASSIFY).effort is None and agents.dropped == 1


def test_a_bad_env_value_is_said_in_the_report():
    agents = _resolve(_server({}), env={"codex": {"*": {"effort": "turbo"}}})
    assert agents.lane(Lane.IMPORT).effort is None
    assert any(ENV_VAR in note and "codex.*.effort" in note for note in agents.notes)
    unparseable = settings_mod.resolve(_server({}), bf.Agent.CODEX, environ={ENV_VAR: "{nope"})
    assert any("not a JSON object" in note for note in unparseable.notes)


# -- the meter ------------------------------------------------------------------


_USAGE = {"input_tokens": 30047, "cached_input_tokens": 12288, "cache_write_input_tokens": 0,
          "output_tokens": 5, "reasoning_output_tokens": 0}


def test_missing_usage_is_counted_and_never_summed_as_zero():
    agents = _resolve(_server({"codex": {"*": {"effort": "medium"}}}, version="abc"))
    agents.meter.launched(Lane.CLASSIFY, None)
    agents.meter.launched(Lane.IMPORT, _USAGE)
    agents.meter.launched(Lane.IMPORT, None)
    agents.meter.cached(Lane.CLASSIFY)
    agents.meter.rejected(Lane.IMPORT)
    props = agents.meter.properties()
    assert props["classify_usage_missing"] == 1 and props["classify_launches"] == 1
    assert "classify_input_tokens" not in props, "unknown, not free"
    assert props["classify_cached"] == 1
    assert props["import_launches"] == 2 and props["import_usage_missing"] == 1
    assert props["import_input_tokens"] == 30047 and props["import_cached_input_tokens"] == 12288
    assert props["import_rejected"] == 1
    assert props["import_effort"] == "medium" and props["import_source"] == "server"
    assert props["import_model"] is None
    assert props["record_launches"] == 0
    assert (props["backfill_agent"], props["settings_version"], props["settings_dropped"]) == (
        "codex", "abc", 0)


def test_the_properties_are_metadata_only():
    """Names, counts and sums: no path and no error text can get in."""
    agents = _resolve(_server({"codex": {"*": {"effort": "low"}}}))
    agents.meter.launched(Lane.IMPORT, _USAGE)
    for key, value in agents.meter.properties().items():
        assert value is None or isinstance(value, (int, str)), key
        assert not isinstance(value, str) or ("/" not in value and len(value) <= 80), key


def test_an_unused_meter_reports_nothing():
    assert Meter().properties() == {}


def test_the_meter_counts_every_launch_from_many_threads():
    meter = Meter()
    threads = [threading.Thread(target=lambda: [meter.launched(Lane.IMPORT, _USAGE) for _ in range(200)])
               for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    props = meter.properties()
    assert props["import_launches"] == 1600 and props["import_input_tokens"] == 1600 * 30047


def test_no_settings_means_no_launch_keywords():
    assert settings_mod.launch_kwargs(None, Lane.IMPORT) == {}


def test_the_degraded_note_names_a_settings_flag_only_when_this_import_sends_it(tmp_path, monkeypatch):
    help_text = "  --output-format <f>  x\n  --model <m>  x\n"
    binary = tmp_path / "claude"
    binary.write_text(f"#!/bin/sh\ncat <<'H'\n{help_text}\nH\n")
    binary.chmod(0o755)
    monkeypatch.setattr(bf, "which_agent", lambda agent: str(binary))
    monkeypatch.setattr(bf, "supported_flags", lambda b, agent=None: frozenset({"--model"}))
    monkeypatch.setattr(bf, "unsupported_flags", lambda agent, b: ([], []))
    monkeypatch.setattr(bf, "_agent_version_cached", lambda b: None)
    with_effort = _resolve(_server({"claude": {"import": {"effort": "low"}}}), bf.Agent.CLAUDE)
    assert "--effort" in bf.degraded_note(bf.Agent.CLAUDE, with_effort.flags())
    without = _resolve(_server({}), bf.Agent.CLAUDE)
    assert without.flags() == ("--model",), "Claude records send --model sonnet today"
    assert bf.degraded_note(bf.Agent.CLAUDE, without.flags()) is None


# -- every entry reads them and passes them down --------------------------------


@pytest.fixture
def harness(tmp_path, monkeypatch):
    from test_backfill_scoped_orchestration import make_harness

    h = make_harness(tmp_path, monkeypatch)
    launched = []
    real = bf.launch_agent  # the harness's scripted agent

    def spy(folder, prompt, **kwargs):
        launched.append(kwargs)
        return real(folder, prompt, **kwargs)

    monkeypatch.setattr(bf, "launch_agent", spy)
    monkeypatch.setattr(settings_mod, "_read_server",
                        lambda client: ({"claude": {"import": {"effort": "low"}}}, "v9"))
    h.launched = launched
    return h


def test_the_foreground_import_runs_its_units_at_the_servers_setting(harness):
    harness.run()
    (unit,) = harness.launched
    assert unit["settings"].lane is Lane.IMPORT and unit["settings"].effort == "low"
    summary = [data for event, data in harness.events if event == "backfill.summary"][-1]
    assert summary["import_effort"] == "low" and summary["import_source"] == "server"
    assert summary["settings_version"] == "v9" and summary["backfill_agent"] == "claude"


def test_a_background_job_reads_them_itself_and_meters_into_the_attempt(tmp_path, monkeypatch, harness):
    from contextlib import nullcontext

    from probe.cli import backfill_import as imp
    from probe.cli import import_jobs
    from probe.sdk import journal

    queued = []
    monkeypatch.setattr(import_jobs, "enqueue", lambda **kw: queued.append(
        json.loads(json.dumps(kw["payload"]))) or {"id": "job-1"})
    monkeypatch.setattr(imp, "_background_client", lambda payload: nullcontext(harness.client))
    monkeypatch.setattr(harness.client, "flush", lambda **kwargs: journal.drain(
        harness.client.journal, client_factory=lambda _: harness.remote, **kwargs))
    harness.run(background=True)
    assert harness.launched == [], "the foreground only classified (a faked classify)"
    meter = Meter()
    imp.run_background_job(queued[0], progress=lambda *a, **k: None, meter=meter)
    (unit,) = harness.launched
    assert unit["settings"].effort == "low" and unit["meter"] is meter
    assert meter.properties()["import_effort"] == "low"


def test_the_worker_hands_its_attempt_meter_to_the_folder_lane(monkeypatch):
    from probe.cli import backfill_import as imp
    from probe.cli import import_jobs

    seen = []
    monkeypatch.setattr(imp, "run_background_job",
                        lambda payload, *, progress, meter=None: seen.append(meter) or [])
    meter = Meter()
    monkeypatch.setattr(import_jobs, "_attempt_meter", meter)
    import_jobs._dispatch(import_jobs.Kind.FOLDER, {}, lambda *a, **k: None)
    assert seen == [meter]
