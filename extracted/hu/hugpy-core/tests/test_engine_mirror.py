"""What core takes from a wrapper's engine database, and what it must not ask an older wrapper for."""
from pathlib import Path

from hugpy_core.intake import mirror


def test_only_the_log_tables_a_wrapper_serves_are_followed():
    assert mirror.log_tables({}) == ['call_log', 'resource_log', 'evictions', 'operator_actions']
    new = mirror.log_tables({'cursor_tables': ['call_log', 'resource_log', 'evictions', 'operator_actions',
                                               'load_runs', 'call_stages', 'added_later']})
    assert 'call_stages' in new and 'load_runs' in new and 'added_later' not in new


def test_a_number_in_a_text_column_does_not_rewrite_the_row_every_pass():
    written = mirror.convert(1, 'text')
    assert mirror._norm(written) == mirror._norm('1')
    assert mirror.convert(True, 'text') is True


def test_an_unreadable_store_is_not_a_console_source(monkeypatch):
    from hugpy_core.web import db_viewer
    real = Path.is_file

    def is_file(path):
        if path.name == 'locked.sqlite3':
            raise PermissionError(13, 'Permission denied', str(path))
        return real(path)

    monkeypatch.setattr(Path, 'is_file', is_file)
    monkeypatch.setenv('HUGPY_LOCKED_DB', '/nowhere/locked.sqlite3')
    from hugpy_core.registry import registrations
    monkeypatch.setattr(registrations, 'all', lambda: [])
    assert not any(s.get('path', '').endswith('locked.sqlite3') for s in db_viewer.sources().values())
