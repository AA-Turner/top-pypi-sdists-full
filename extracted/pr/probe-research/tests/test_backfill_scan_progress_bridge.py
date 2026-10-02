"""Saved jobs receive the same measured scan phases as the foreground board."""

from __future__ import annotations

import io
import json

from probe.cli import backfill as bf
from probe.cli import backfill_run as runner


def test_nonterminal_progress_reports_measured_steps_once_per_change(tmp_path):
    events = []
    log = io.StringIO()
    with runner.classification_context(
        'observed-files', lambda message, **fields: events.append((message, fields)),
        background=True,
    ):
        with runner._ReadProgress(tmp_path, 1154, 2, log) as progress:
            progress.begin('survey', 'Reading slice 1 of 2')
            for _ in range(20):
                progress.begin('survey', 'Reading slice 2 of 2')
            progress.finish('survey', 'Reading slice 2 of 2', success=True)
            progress.finish('survey', 'Reading slice 1 of 2', success=False)
            progress.finish('survey', 'Reading slice 2 of 2', success=True)  # already counted
            progress.finish('survey', 'Reading slice 1 of 2', success=True, cached=True)
            progress.begin('name', 'Naming projects')
            progress.finish('name', 'Naming projects', success=True)
            progress.begin('assign', 'Filing slice 1 of 2')
            progress.begin('assign', 'Filing slice 2 of 2')
            progress.finish('assign', 'Filing slice 2 of 2', success=True)
            progress.finish('assign', 'Filing slice 1 of 2', success=True)
        progress.begin('assign', 'A late event must not alter the next phase')
    fields = [fields for _, fields in events]
    assert [item['completed'] for item in fields] == [0, 1, 2, 2, 3, 3, 4, 5]
    assert all(item['phase'] == 'scanning' and item['total'] == 5 for item in fields)
    assert [(item['stage'], item['stage_completed'], item['stage_total']) for item in fields] == [
        ('survey', 0, 2), ('survey', 1, 2), ('survey', 2, 2),
        ('name', 0, 1), ('name', 1, 1),
        ('assign', 0, 2), ('assign', 1, 2), ('assign', 2, 2),
    ]
    assert fields[2]['cached'] is True
    assert 'Review and approve the plan next' in log.getvalue()


def test_opt_in_worker_log_does_not_promise_a_second_approval(tmp_path):
    log = io.StringIO()
    with runner.classification_context('observed-files', background=True, auto_approve=True):
        with runner._ReadProgress(tmp_path, 1154, 2, log):
            pass
    assert 'Automatic import is approved and starts after preparation.' in log.getvalue()
    assert 'Review and approve' not in log.getvalue()


def test_per_turn_notifications_cannot_overwrite_the_shared_scan_denominator(
    tmp_path, monkeypatch,
):
    events = []
    monkeypatch.setattr(bf, 'launch_agent', lambda *a, **kw: (
        True, json.dumps({'findings': [{'work': 'training'}]}),
    ))
    with runner.classification_context(
        'observed-files', lambda message, **fields: events.append((message, fields)),
    ):
        with runner._ReadProgress(tmp_path, 1154, 4, io.StringIO()):
            result, _ = runner._run_pass(
                tmp_path, 'prompt', agent=bf.Agent.CLAUDE, heading='Reading slice 1 of 4',
                work_dir=tmp_path, total=1154, key='findings',
            )
    assert result is not None
    assert [fields['completed'] for _, fields in events] == [0, 1]
    assert all(fields['phase'] == 'scanning' and fields['total'] == 9
               for _, fields in events)


def test_single_pass_start_is_not_persisted_twice_before_completion(tmp_path):
    events = []
    with runner.classification_context(
        'observed-files', lambda message, **fields: events.append((message, fields)),
    ):
        runner._classification_progress('Reading folder', 'classify')
        with runner._ReadProgress(tmp_path, 100, 0, io.StringIO()) as progress:
            progress.begin('classify', 'Reading folder')
            progress.finish('classify', 'Reading folder', success=True)
    assert [fields['completed'] for _, fields in events] == [0, 1]
    assert all(fields['stage'] == 'classify' and fields['total'] == 1
               for _, fields in events)
