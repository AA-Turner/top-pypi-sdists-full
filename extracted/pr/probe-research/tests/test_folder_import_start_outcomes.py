"""An unregistered folder attempt needs a decision before onboarding can advance."""

from contextlib import contextmanager, nullcontext
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import backfill as bf, backfill_import as imp, backfill_run as runner
from probe.cli import import_job_messages, import_jobs, import_jobs_ui, onboarding_complete, setup, tui
from probe.cli.backfill_coverage import CoverageError
from tests import test_backfill_auto_import as auto_tests
from tests import test_wizard_install_completion as install_tests

automatic = auto_tests.automatic
queued = auto_tests.queued
entry = install_tests.entry
installation = install_tests.installation
main = install_tests.main
run_selected_imports = main._run_selected_imports


@pytest.fixture
def attempt(tmp_path, monkeypatch):
    monkeypatch.setattr(bf, 'choose_folder_wandb', lambda *a, **k: (None, False))
    state = SimpleNamespace(folder=tmp_path, events=[], prompts=[], answer=tui.SKIP,
                            mode=bf.FolderImportMode.AUTOMATIC)
    monkeypatch.setattr(bf, 'choose_directory', lambda start: state.events.append('folder') or state.folder)
    monkeypatch.setattr(bf, 'resolve_agent', lambda *a, **k: state.events.append('agent') or (bf.Agent.CODEX, None))
    monkeypatch.setattr(bf, 'choose_import_mode', lambda *a: state.events.append('mode') or state.mode)
    monkeypatch.setattr(import_jobs, '_launch', import_jobs._read)
    monkeypatch.setattr(import_jobs_ui, 'show_started_import', lambda job: state.events.append('status') or job)

    def review(title, lines, choices):
        state.prompts.append((title, list(lines), choices))
        state.events.append('failure')
        return state.answer() if callable(state.answer) else state.answer

    monkeypatch.setattr(tui, 'review', review)
    return state


def _run(**kwargs):
    return bf.run(client_factory=object, interactive=True, background=True,
                  back_to_selection=True, **kwargs)


@pytest.mark.parametrize('mode', list(bf.FolderImportMode))
def test_retry_keeps_folder_agent_and_mode_until_a_real_job_is_saved(attempt, monkeypatch, mode):
    attempt.mode = mode
    attempt.answer = 'retry'
    calls = []

    def execute(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            if mode == bf.FolderImportMode.AUTOMATIC:
                raise CoverageError('The selected destination is unavailable.')
            return ['The selected destination is unavailable.']
        job = import_jobs.enqueue('folder', {'folder': str(attempt.folder)}, 'Saved folder')
        return job if mode == bf.FolderImportMode.AUTOMATIC else bf.StartedFolderImport(job, ['Registered.'])

    monkeypatch.setattr(imp, 'enqueue_auto_import', execute)
    monkeypatch.setattr(runner, 'execute', execute)
    result = _run()
    assert isinstance(result, bf.StartedFolderImport)
    assert result.job['kind'] == import_jobs.Kind.FOLDER
    assert calls[0]['folder'] == calls[1]['folder'] == attempt.folder
    assert calls[0]['agent'] == calls[1]['agent'] == bf.Agent.CODEX
    assert attempt.events[:4] == ['folder', 'agent', 'mode', 'failure']
    assert attempt.events.count('folder') == attempt.events.count('agent') == attempt.events.count('mode') == 1
    assert len(import_jobs.list_jobs()) == 1
    assert 'selected destination is unavailable' in ' '.join(attempt.prompts[0][1])


@pytest.mark.parametrize('mode', list(bf.FolderImportMode))
@pytest.mark.parametrize('answer', [tui.SKIP, None], ids=['skip', 'quit'])
def test_unstarted_attempt_requires_skip_or_quit_and_never_creates_a_job(attempt, monkeypatch, mode, answer):
    attempt.mode, attempt.answer = mode, answer

    def fail(**kwargs):
        raise CoverageError('No matching workspace was found.')

    monkeypatch.setattr(imp, 'enqueue_auto_import', fail)
    monkeypatch.setattr(runner, 'execute', lambda **k: ['No matching workspace was found.'])
    if answer is None:
        with pytest.raises(KeyboardInterrupt):
            _run()
    else:
        assert _run() is None
    assert len(attempt.prompts) == 1
    title, lines, choices = attempt.prompts[0]
    assert title == 'Folder import did not start'
    assert 'No matching workspace was found.' in ' '.join(lines)
    assert [label for label, value in choices] == ['Retry', 'Skip folder', 'Back']
    assert import_jobs.list_jobs() == []


def test_back_after_failure_reopens_mode_without_repeating_the_failed_attempt(attempt, monkeypatch):
    attempt.answer = tui.BACK
    modes = iter([bf.FolderImportMode.AUTOMATIC, tui.SKIP])
    monkeypatch.setattr(bf, 'choose_import_mode', lambda *a: attempt.events.append('mode') or next(modes))
    calls = []

    def fail(**kwargs):
        calls.append(kwargs)
        raise CoverageError('The folder could not be approved.')

    monkeypatch.setattr(imp, 'enqueue_auto_import', fail)
    assert _run() is None
    assert attempt.events == ['folder', 'agent', 'mode', 'failure', 'mode']
    assert len(calls) == 1


@pytest.mark.parametrize('failure', ['missing_folder', 'missing_agent', 'empty_folder'])
def test_preflight_and_empty_results_are_visible_before_explicit_skip(attempt, monkeypatch, failure):
    if failure == 'missing_folder':
        attempt.folder = attempt.folder / 'no-longer-mounted'
        expected = 'is not a directory'
    elif failure == 'missing_agent':
        monkeypatch.setattr(bf, 'resolve_agent', lambda *a, **k: (None, 'Install a supported coding agent.'))
        expected = 'Install a supported coding agent.'
    else:
        attempt.mode = bf.FolderImportMode.REVIEW_FIRST
        monkeypatch.setattr(runner, 'execute', lambda **k: ['No files to import.'])
        expected = 'No files to import.'
    assert _run() is None
    assert expected in ' '.join(attempt.prompts[0][1])
    assert import_jobs.list_jobs() == []


def test_registered_reviewed_import_carries_its_job_through_optional_session_report(automatic, monkeypatch):
    h = automatic
    monkeypatch.setattr(runner, '_run_transcript_lane', lambda **k: ['Session import skipped.'])
    result = runner.execute(
        client_factory=lambda: nullcontext(h.client), folder=h.folder,
        agent=bf.Agent.CLAUDE, interactive=False, yes=True, concurrency=1,
        background=True, transcripts=True,
    )
    assert isinstance(result, bf.StartedFolderImport)
    assert result.job['kind'] == import_jobs.Kind.FOLDER
    assert result[-1] == 'Session import skipped.'
    assert import_jobs.get_job(result.job['id'])['kind'] == import_jobs.Kind.FOLDER


@pytest.mark.parametrize('failure', ['handoff', 'report', 'client_cleanup'])
def test_registered_reviewed_job_survives_later_status_or_cleanup_failure(automatic, queued, monkeypatch, failure):
    h = automatic
    monkeypatch.setattr(bf, 'choose_folder_wandb', lambda *a, **k: (None, False))
    monkeypatch.setattr(bf, 'choose_directory', lambda *a: h.folder)
    monkeypatch.setattr(bf, 'resolve_agent', lambda *a, **k: (bf.Agent.CLAUDE, None))
    monkeypatch.setattr(bf, 'choose_import_mode', lambda *a: bf.FolderImportMode.REVIEW_FIRST)
    monkeypatch.setattr(import_jobs_ui, 'show_started_import', lambda job: job)

    def review(title, lines, choices):
        assert title != 'Folder import did not start', 'Registered work was offered a new start'
        return choices[0][1]

    def fail(*args):
        raise RuntimeError('private transport detail')

    @contextmanager
    def client():
        yield h.client
        if failure == 'client_cleanup':
            fail()

    monkeypatch.setattr(tui, 'review', review)
    if failure == 'handoff':
        monkeypatch.setattr(import_jobs_ui, 'show_started_import', fail)
    elif failure == 'report':
        monkeypatch.setattr(import_job_messages, 'enqueue_report', fail)
    result = bf.run(client_factory=client, interactive=True, background=True,
                    back_to_selection=True, concurrency=1)
    assert isinstance(result, bf.StartedFolderImport)
    assert len(import_jobs.list_jobs()) == len(queued) == 1
    assert import_jobs.get_job(result.job['id'])['kind'] == import_jobs.Kind.FOLDER
    assert len(h.classified) == 1 and h.remote.calls == []
    assert 'status is unavailable (RuntimeError)' in ' '.join(result)
    assert 'Existing imports' in ' '.join(result)
    assert 'private transport detail' not in ' '.join(result)


def test_registered_automatic_job_survives_status_failure_without_retry(attempt, monkeypatch):
    def enqueue(**kwargs):
        return import_jobs.enqueue('folder', {'folder': str(attempt.folder)}, 'Saved folder')

    def fail(job):
        raise RuntimeError('private transport detail')

    monkeypatch.setattr(imp, 'enqueue_auto_import', enqueue)
    monkeypatch.setattr(import_jobs_ui, 'show_started_import', fail)
    result = _run()
    assert isinstance(result, bf.StartedFolderImport)
    assert len(import_jobs.list_jobs()) == 1
    assert attempt.prompts == []
    assert 'status is unavailable (RuntimeError)' in ' '.join(result)
    assert 'private transport detail' not in ' '.join(result)


def test_automatic_admission_client_closes_before_a_worker_is_registered(automatic):
    h = automatic

    @contextmanager
    def client():
        yield h.client
        raise RuntimeError('Admission client cleanup failed')

    with pytest.raises(RuntimeError, match='Admission client cleanup failed'):
        imp.enqueue_auto_import(
            client_factory=client, folder=h.folder, agent=bf.Agent.CLAUDE,
            concurrency=1, auto_approve=True,
        )
    assert import_jobs.list_jobs() == []
    assert h.classified == h.remote.calls == []


@pytest.mark.parametrize('answer', ['retry', tui.SKIP], ids=['retry', 'skip'])
def test_onboarding_waits_for_folder_failure_decision_before_final_page(installation, attempt, monkeypatch, answer):
    monkeypatch.setattr(main, '_run_selected_imports', run_selected_imports)
    monkeypatch.setattr(setup, 'run_backfill_offer', lambda *a, **k: {setup.BackfillChoice.PROJECT_FOLDER})
    calls = []

    def enqueue(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise CoverageError('The import destination could not be verified.')
        return import_jobs.enqueue('folder', {'folder': str(attempt.folder)}, 'Saved folder')

    def decide():
        assert installation.registrations[-1][1] is True
        assert len(calls) == 1 and import_jobs.list_jobs() == []
        assert 'dashboard' not in attempt.events
        return answer

    def finish(base):
        assert len(attempt.prompts) == 1
        assert 'import destination could not be verified' in ' '.join(attempt.prompts[0][1])
        assert len(import_jobs.list_jobs()) == (1 if answer == 'retry' else 0)
        attempt.events.append('dashboard')
        return True

    attempt.answer = decide
    monkeypatch.setattr(imp, 'enqueue_auto_import', enqueue)
    monkeypatch.setattr(onboarding_complete, 'show', finish)
    result = CliRunner().invoke(main.app, ['install', '--agent', 'claude'])
    assert result.exit_code == 0, result.output
    assert attempt.events[-1] == 'dashboard'
    assert len(calls) == (2 if answer == 'retry' else 1)
