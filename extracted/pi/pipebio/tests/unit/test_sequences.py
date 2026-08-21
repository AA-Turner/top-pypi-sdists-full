"""Unit tests for the deprecated sequence extract service."""

import warnings
from unittest.mock import MagicMock, patch

import pytest

from pipebio.column import Column
from pipebio.models.sort import Sort
from pipebio.models.table_column_type import TableColumnType
from pipebio.sequences import Sequences


@pytest.fixture
def mock_session():
    """Create a mock session whose _extract POST returns no download links."""
    session = MagicMock()
    response = MagicMock()
    response.json.return_value = []
    session.post.return_value.__enter__.return_value = response
    return session


@pytest.fixture
def sequences(mock_session):
    with patch('pipebio.sequences.Util.mount_standard_session', return_value=mock_session):
        return Sequences(mock_session, is_aws=True)


def _extract_url(mock_session) -> str:
    """Return the URL passed to the _extract POST call."""
    return mock_session.post.call_args.args[0]


class TestDownload:
    def test_download_to_memory_warns(self, sequences):
        with patch.object(sequences, '_parallel_download'):
            with pytest.warns(
                FutureWarning,
                match='temporary disk.*does not guarantee row order',
            ):
                sequences.download_to_memory([])

    def test_download_to_memory_does_not_emit_nested_download_warning(
        self, sequences, mock_session, tmp_path
    ):
        signed_response = MagicMock()
        signed_response.read.return_value = b'parquet-bytes'
        mock_session.post.return_value.__enter__.return_value.json.return_value = [
            'https://signed.example/export.parquet'
        ]

        with patch.object(
            Sequences, '_get_filepath_for_entity_id', return_value=str(tmp_path / 'source')
        ), patch(
            'pipebio.sequences.urlopen', return_value=signed_response
        ), patch.object(
            sequences, 'convert_parquet_to_tsv'
        ), patch.object(
            sequences, '_read_tsv_to_map', return_value={}
        ):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always', FutureWarning)
                sequences.download_to_memory(['ent-1'])

        assert len(caught) == 1
        assert 'download_to_memory is deprecated' in str(caught[0].message)

    def test_download_warns_and_uses_extract_endpoint(self, sequences, mock_session):
        with pytest.warns(
            FutureWarning,
            match='allow_deleted_entities=True',
        ):
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv')

        assert _extract_url(mock_session).startswith('entities/ent-1/_extract?')

    def test_download_does_not_print_signed_download_links(
        self, sequences, mock_session, tmp_path, capsys
    ):
        signed_link = 'https://signed.example/export.parquet?token=secret'
        response = mock_session.post.return_value.__enter__.return_value
        response.json.return_value = [signed_link]
        signed_response = MagicMock()
        signed_response.read.return_value = b'parquet-bytes'

        with patch.object(
            Sequences, '_get_filepath_for_entity_id', return_value=str(tmp_path / 'source')
        ), patch(
            'pipebio.sequences.urlopen', return_value=signed_response
        ), patch.object(sequences, 'convert_parquet_to_tsv'):
            with pytest.warns(FutureWarning):
                sequences.download(
                    'ent-1',
                    destination=str(tmp_path / 'output.tsv'),
                )

        assert signed_link not in capsys.readouterr().out

    @pytest.mark.parametrize('kwargs,param_name', [
        ({'sort': [Sort('name', 'asc')]}, 'sort'),
        ({'query': 'name = "x"'}, 'query'),
        ({'include_cols': ['id']}, 'include_cols'),
        ({'exclude_cols': ['annotations']}, 'exclude_cols'),
        ({'limit': 10}, 'limit'),
    ])
    def test_legacy_parameter_warns_and_keeps_extract_request(
        self, sequences, mock_session, kwargs, param_name
    ):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', FutureWarning)
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv', **kwargs)

        assert any(param_name in str(warning.message) for warning in caught)
        assert any(
            'do not map directly to client.export_to_path' in str(warning.message)
            for warning in caught
        )
        assert _extract_url(mock_session).startswith('entities/ent-1/_extract?')

    def test_download_preserves_filter_and_sort_request_body(self, sequences, mock_session):
        sort = [Sort('name', 'desc')]

        with pytest.warns(FutureWarning):
            with pytest.raises(Exception, match='no download links'):
                sequences.download(
                    'ent-1',
                    destination='/tmp/ignored.tsv',
                    query='name = "example"',
                    sort=sort,
                )

        assert mock_session.post.call_args.kwargs['json'] == {
            'filter': 'name = "example"',
            'sort': [{'colId': 'name', 'sort': 'desc'}],
        }

    def test_allow_deleted_defaults_to_true(self, sequences, mock_session):
        with pytest.warns(FutureWarning):
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv')
        assert 'allowDeleted=true' in _extract_url(mock_session)

    def test_allow_deleted_false_is_serialized(self, sequences, mock_session):
        with pytest.warns(FutureWarning):
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv', allow_deleted=False)
        assert 'allowDeleted=false' in _extract_url(mock_session)

    def test_no_bare_boolean_token(self, sequences, mock_session):
        with pytest.warns(FutureWarning):
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv')
        url = _extract_url(mock_session)
        assert '&True' not in url
        assert '&False' not in url

    def test_limit_serialized_as_page_limit(self, sequences, mock_session):
        with pytest.warns(FutureWarning):
            with pytest.raises(Exception, match='no download links'):
                sequences.download('ent-1', destination='/tmp/ignored.tsv', limit=10000)
        assert 'pageLimit=10000' in _extract_url(mock_session)


class TestIterTsvEntries:
    """Cover the TSV parser still used by the legacy download_to_memory path."""

    def test_yields_compound_ids_and_records(self, tmp_path):
        tsv_path = tmp_path / 'exported.tsv'
        tsv_path.write_text(
            'id\tname\tsequence\tannotations\ttype\n'
            'seq-1\tExample\tATGC\t{}\tDNA\n'
            'seq-2\t\tGGCC\t\tDNA\n'
        )
        columns = [
            Column(name, TableColumnType.STRING)
            for name in ('id', 'name', 'sequence', 'annotations', 'type')
        ]

        entries = list(
            Sequences._iter_tsv_entries(str(tsv_path), 'entity-1', columns)
        )

        assert entries == [
            (
                'entity-1##@##seq-1',
                {
                    'id': 'seq-1',
                    'name': 'Example',
                    'sequence': 'ATGC',
                    'annotations': '{}',
                    'type': 'DNA',
                },
            ),
            (
                'entity-1##@##seq-2',
                {
                    'id': 'seq-2',
                    'name': '',
                    'sequence': 'GGCC',
                    'annotations': '',
                    'type': 'DNA',
                },
            ),
        ]
