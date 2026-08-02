"""Unit tests for pipebio.sequences module."""

import warnings

import pytest
from unittest.mock import patch, MagicMock

from pipebio.models.sort import Sort
from pipebio.sequences import Sequences


@pytest.fixture
def mock_session():
    """Create a mock session whose _extract POST returns no download links."""
    session = MagicMock()
    # download() uses `with self._session.post(...) as response:`, so the
    # response is the context manager's __enter__ value. Return empty links so
    # download() raises before attempting any real shard downloads.
    response = MagicMock()
    response.json.return_value = []
    session.post.return_value.__enter__.return_value = response
    return session


@pytest.fixture
def sequences(mock_session):
    """Create a Sequences instance with a mocked session."""
    with patch('pipebio.sequences.Util.mount_standard_session', return_value=mock_session):
        return Sequences(mock_session, is_aws=True)


def _extract_url(mock_session) -> str:
    """Return the URL passed to the _extract POST call."""
    return mock_session.post.call_args[0][0]


class TestDeprecatedParams:
    """Deprecation warnings for sort/query/include_cols/exclude_cols/limit."""

    @pytest.mark.parametrize('kwargs,param_name', [
        ({'sort': [Sort('name', 'asc')]}, 'sort'),
        ({'query': 'name = "x"'}, 'query'),
        ({'include_cols': ['id']}, 'include_cols'),
        ({'exclude_cols': ['annotations']}, 'exclude_cols'),
        ({'limit': 10}, 'limit'),
    ])
    def test_deprecated_param_warns(self, sequences, mock_session, kwargs, param_name):
        with pytest.warns(DeprecationWarning, match=param_name):
            with pytest.raises(Exception):
                sequences.download('ent-1', destination='/tmp/ignored.tsv', **kwargs)

    def test_no_warning_without_deprecated_params(self, sequences, mock_session):
        with warnings.catch_warnings():
            warnings.simplefilter('error', DeprecationWarning)
            with pytest.raises(Exception):
                sequences.download('ent-1', destination='/tmp/ignored.tsv')


class TestDownloadUrl:
    """Tests for the query string built by Sequences.download()."""

    def test_allow_deleted_defaults_to_true(self, sequences, mock_session):
        # download() raises because no links are returned; we only care about the URL.
        with pytest.raises(Exception):
            sequences.download('ent-1', destination='/tmp/ignored.tsv')
        assert 'allowDeleted=true' in _extract_url(mock_session)

    def test_allow_deleted_false_is_serialized(self, sequences, mock_session):
        with pytest.raises(Exception):
            sequences.download('ent-1', destination='/tmp/ignored.tsv', allow_deleted=False)
        assert 'allowDeleted=false' in _extract_url(mock_session)

    def test_no_bare_boolean_token(self, sequences, mock_session):
        # Regression guard against the previous bug that appended a bare "&True"/"&False".
        with pytest.raises(Exception):
            sequences.download('ent-1', destination='/tmp/ignored.tsv')
        url = _extract_url(mock_session)
        assert '&True' not in url
        assert '&False' not in url

    def test_limit_serialized_as_page_limit(self, sequences, mock_session):
        with pytest.warns(DeprecationWarning):
            with pytest.raises(Exception):
                sequences.download('ent-1', destination='/tmp/ignored.tsv', limit=10000)
        assert 'pageLimit=10000' in _extract_url(mock_session)
