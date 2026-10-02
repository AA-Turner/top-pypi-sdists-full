"""Preparation counts completed analysis, then hands the plan to approval."""

from __future__ import annotations

import io
import json
import threading
from pathlib import Path

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_evidence as evidence
from probe.cli import backfill_run as runner
from probe.cli import tui


class _Terminal(io.StringIO):
    def isatty(self):
        return True


class _Board:
    instances = []

    def __init__(self, title, labels, out=None):
        self.title = title
        self.rows = [''] * len(labels)
        self.snapshots = []
        self.opened = False
        self.closed = False
        self.instances.append(self)

    def open(self):
        self.opened = True

    def update(self, index, text):
        assert not self.closed
        self.rows[index] = text
        self.snapshots.append(tuple(self.rows))

    def close(self, **kwargs):
        self.closed = True


@pytest.fixture
def board(monkeypatch):
    _Board.instances = []
    monkeypatch.setattr(tui, 'Board', _Board)
    return _Board


def _answer(payload):
    return json.dumps({'type': 'result', 'result': json.dumps(payload)})


def _inputs(tmp_path):
    return evidence.Evidence(
        root=str(tmp_path),
        files=[evidence.FileEvidence(
            path=str(tmp_path / 'a.py'), size=10, mtime=0,
            tier=evidence.Tier.EVIDENCE, sample='train()',
        )],
        clusters=[], sampled_files=1, sampled_bytes=7,
    )


def test_only_successful_slices_advance_the_phase_and_activity_is_not_a_file_count(board):
    with runner._ReadProgress(Path('Odyssey'), 1154, 4, _Terminal()) as progress:
        display, = board.instances
        assert '1,154 files found' in display.rows[0]
        assert '0/4 slices' in display.rows[2]
        progress.begin('survey', 'Reading slice 2 of 4')
        paint = progress.activity('survey', 'Reading slice 2 of 4')
        paint('0:12 · thinking')
        assert '0:12 · thinking' in display.rows[6]
        assert '0/4 slices' in display.rows[2]
        progress.finish('survey', 'Reading slice 2 of 4', success=True)
        assert '1/4 slices' in display.rows[2]
        progress.finish('survey', 'Reading slice 1 of 4', success=False)
        assert '1/4 slices' in display.rows[2]
        progress.finish('survey', 'Reading slice 2 of 4', success=True, cached=True)
        assert '1/4 slices' in display.rows[2]  # a reused result is not two slices
        assert '0/1 step' in display.rows[3]
        assert '0/4 slices' in display.rows[4]
        assert 'approve' in display.rows[7] and 'before anything uploads' in display.rows[7]
        assert 'Nothing has been uploaded' in display.rows[8]
        assert 'background' not in display.rows[8]
        assert all('0/1154' not in line and '%' not in line for line in display.rows)
    assert display.closed
    paint('a late worker must not repaint over the next page')


def test_parallel_surveys_are_bounded_and_naming_waits_for_every_ordered_result(
    tmp_path, monkeypatch, board,
):
    rows = [json.dumps({'path': f'{i}.py', 'sample': str(i)}) for i in range(1, 5)]
    monkeypatch.setattr(evidence, 'chunk_lines', lambda _: [[row] for row in rows])
    monkeypatch.setattr(runner, '_git_note', lambda *_: '')
    barrier = threading.Barrier(2)
    lock = threading.Lock()
    active = peak = 0
    surveyed = set()
    named = False
    calls = []
    actual_name = runner.prompts.name_projects

    def name_prompt(**kwargs):
        assert [row['slice'] for row in json.loads(kwargs['findings_json'])] == [1, 2, 3, 4]
        return actual_name(**kwargs)

    monkeypatch.setattr(runner.prompts, 'name_projects', name_prompt)

    def launch(folder, prompt, **kwargs):
        nonlocal active, peak, named
        assert kwargs['total'] == 0
        assert callable(kwargs['paint_to'])
        heading = kwargs['heading']
        calls.append(heading)
        if heading.startswith('Reading'):
            index = int(heading.split('slice ')[1].split()[0])
            with lock:
                active += 1
                peak = max(peak, active)
            barrier.wait(timeout=5)
            kwargs['paint_to'](f'0:04 · thinking about slice {index}')
            with lock:
                surveyed.add(index)
                active -= 1
            return True, _answer({'findings': [{'work': f'slice {index}'}]})
        if heading.startswith('Naming'):
            assert surveyed == {1, 2, 3, 4}
            assert '4/4 slices' in board.instances[0].rows[2]
            named = True
            return True, _answer({'projects': [{'slug': 'alpha', 'name': 'Alpha'}]})
        assert named
        index = int(heading.split('slice ')[1].split()[0])
        return True, _answer({'assignments': [{'path': f'{index}.py', 'project': 'alpha'}]})

    monkeypatch.setattr(bf, 'launch_agent', launch)
    plan, _ = runner.classify_chunked(
        tmp_path, _inputs(tmp_path), agent=bf.Agent.CLAUDE,
        existing=[], work_dir=tmp_path / 'work', stream=_Terminal(),
    )
    assert plan is not None and len(plan.assignments) == 4
    assert peak == 2
    assert len(calls) == 9  # overlap changes latency, never the evidence or model work
    display, = board.instances
    assert display.opened and display.closed
    assert '4/4 slices' in display.rows[2]
    assert '1/1 step' in display.rows[3]
    assert '4/4 slices' in display.rows[4]


@pytest.mark.parametrize('success', [True, False])
def test_single_classification_progress_does_not_claim_prompt_evidence_is_tool_reads(
    tmp_path, monkeypatch, board, success,
):
    monkeypatch.setattr(runner, '_git_note', lambda *_: '')

    def launch(folder, prompt, **kwargs):
        assert kwargs['total'] == 0
        kwargs['paint_to']('0:05 · identifying projects')
        return success, _answer({
            'projects': [{'slug': 'alpha'}],
            'assignments': [{'path': 'a.py', 'project': 'alpha'}],
        })

    monkeypatch.setattr(bf, 'launch_agent', launch)
    plan, _, _ = runner.classify(
        tmp_path, _inputs(tmp_path), agent=bf.Agent.CLAUDE,
        existing=[], work_dir=tmp_path / 'work', stream=_Terminal(),
    )
    assert (plan is not None) == success
    display, = board.instances
    assert ('1/1 step' if success else '0/1 step') in display.rows[2]
    assert display.closed


def test_ctrl_c_stops_classification_children_without_waiting_for_them(monkeypatch):
    futures = []
    shutdowns = []
    stopped = []

    class Future:
        cancelled = False

        def result(self):
            raise KeyboardInterrupt

        def cancel(self):
            self.cancelled = True

    class Pool:
        def __init__(self, **kwargs):
            pass

        def submit(self, *args):
            future = Future()
            futures.append(future)
            return future

        def shutdown(self, **kwargs):
            shutdowns.append(kwargs)

    monkeypatch.setattr(runner, 'ThreadPoolExecutor', Pool)
    monkeypatch.setattr(bf, 'stop_all', lambda: stopped.append(True))
    with pytest.raises(KeyboardInterrupt):
        runner._classification_results(lambda _: None, [(1, []), (2, [])], workers=2)
    assert stopped == [True]
    assert all(future.cancelled for future in futures)
    assert shutdowns == [{'wait': False, 'cancel_futures': True}]


def test_unmeasured_activity_shows_liveness_without_zero_over_zero():
    state = bf.Activity(total=0)
    bf.fold_event(json.dumps({'type': 'turn.started'}), state)
    assert 'thinking' in state.line(15)
    assert '0:15' in state.line(15)
    assert '/' not in state.line(15)
    assert state.eta(15) == ''
    assert '/' not in bf.Activity(total=0, queued=True).line(0)


def test_installer_guidance_names_background_import_only_when_requested(board):
    with runner.classification_context('observed-files', background=True):
        with runner._ReadProgress(Path('Odyssey'), 1154, 4, _Terminal()):
            display, = board.instances
            assert 'approve' in display.rows[7]
            assert 'After approval' in display.rows[8] and 'background' in display.rows[8]


@pytest.mark.parametrize('agent', [bf.Agent.CLAUDE, bf.Agent.CODEX, bf.Agent.PI])
def test_a_cancelled_launch_never_resolves_or_starts_an_agent(tmp_path, monkeypatch, agent):
    cancelled = threading.Event()
    cancelled.set()
    monkeypatch.setattr(bf, 'which_agent', lambda *_: pytest.fail('cancelled before launch'))
    ok, detail = bf.launch_agent(tmp_path, 'prompt', agent=agent, cancel_event=cancelled)
    assert not ok and 'cancelled' in detail


@pytest.mark.parametrize('agent', [bf.Agent.CLAUDE, bf.Agent.CODEX, bf.Agent.PI])
def test_cancellation_during_spawn_stops_the_child_missed_by_stop_all(
    tmp_path, monkeypatch, agent,
):
    """Force the race without timing guesses: spawn -> cancel -> register.

    The real child only sleeps. stop_all cannot see it until spawn_child returns,
    so the launch's registration check must reap it before entering its read.
    """
    import sys

    from probe.cli import import_jobs

    cancelled = threading.Event()
    children = []
    monkeypatch.setattr(bf, '_LIVE', set())
    monkeypatch.setattr(bf, 'which_agent', lambda *_: sys.executable)
    monkeypatch.setattr(bf, 'agent_argv', lambda *a, **kw: [
        sys.executable, '-c', 'import time; time.sleep(30)',
    ])
    original_spawn = import_jobs.spawn_child

    def spawn(*args, **kwargs):
        proc = original_spawn(*args, **kwargs)
        children.append(proc)
        cancelled.set()
        bf.stop_all()
        assert proc not in bf._LIVE
        assert proc.poll() is None  # the snapshot really missed this live child
        return proc

    monkeypatch.setattr(import_jobs, 'spawn_child', spawn)
    try:
        ok, detail = bf.launch_agent(
            tmp_path, 'prompt', agent=agent, stream=io.StringIO(), cancel_event=cancelled,
        )
        assert not ok and 'cancelled' in detail
        child, = children
        assert child.poll() is not None
        assert child not in bf._LIVE
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)


def test_pool_cancellation_is_carried_to_the_actual_agent_launch(tmp_path, monkeypatch, board):
    with runner._ReadProgress(tmp_path, 1, 1, _Terminal()) as progress:
        def launch(*args, **kwargs):
            assert kwargs['cancel_event'] is progress.cancelled
            progress.cancelled.set()
            return False, 'cancelled while launching'

        monkeypatch.setattr(bf, 'launch_agent', launch)
        result, detail = runner._run_pass(
            tmp_path, 'prompt', agent=bf.Agent.CLAUDE, heading='Reading slice 1 of 1',
            work_dir=tmp_path, total=1, key='findings',
        )
        assert result is None and detail == 'scan cancelled'


@pytest.mark.parametrize('agent', [bf.Agent.CLAUDE, bf.Agent.CODEX, bf.Agent.PI])
def test_cancellation_during_cli_preflight_prevents_spawn(tmp_path, monkeypatch, agent):
    from probe.cli import import_jobs

    cancelled = threading.Event()
    monkeypatch.setattr(bf, 'which_agent', lambda *_: '/bin/unused')

    def argv(*args, **kwargs):
        cancelled.set()
        return ['/bin/unused']

    monkeypatch.setattr(bf, 'agent_argv', argv)
    monkeypatch.setattr(import_jobs, 'spawn_child', lambda *a, **kw: pytest.fail('late spawn'))
    ok, detail = bf.launch_agent(
        tmp_path, 'prompt', agent=agent, stream=io.StringIO(), cancel_event=cancelled,
    )
    assert not ok and 'cancelled' in detail
