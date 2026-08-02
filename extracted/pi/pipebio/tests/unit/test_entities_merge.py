"""Unit tests for Entities.merge (async MergeAssayDataJob path)."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from pipebio.column import Column
from pipebio.entities import Entities
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.table_column_type import TableColumnType


@pytest.fixture
def assay_file():
    """Write a small assay csv to a temp file and yield its path."""
    fd, path = tempfile.mkstemp(suffix='.csv', prefix='assay')
    with os.fdopen(fd, 'w') as f:
        f.write('clone_id,BindingScore\n')
        f.write('A,95.2\n')
        f.write('B,82.7\n')
    yield path
    os.remove(path)


@pytest.fixture
def session():
    """Mock session for the presigned upload and job create/poll calls."""
    session = MagicMock()
    # Real dict so Jobs.create's correlation-id lookup behaves predictably.
    session.headers = {}

    def post(url, **kwargs):
        if url == 'uploads/signed-url':
            return MagicMock(
                status_code=200,
                json=lambda: {'url': 'https://s3/upload', 'key': 'tenant/the-key', 'headers': {}},
            )
        if url == 'jobs':
            return MagicMock(status_code=201, json=lambda: {'id': 'merge-job-1'})
        raise AssertionError(f'Unexpected POST to {url}')

    session.post.side_effect = post
    return session


@pytest.fixture
def user():
    """Authenticated user whose default org owns created jobs."""
    return {'org': {'id': 'org-1'}}


@pytest.fixture
def entities(session, user):
    # Jobs mounts a retrying adapter on construction; keep the mock session as-is.
    with patch('pipebio.attachments.Attachments'), \
            patch('pipebio.jobs.Util.mount_standard_session', return_value=session):
        return Entities(session, user)


def test_merge_uploads_via_presigned_url_and_starts_merge_job(entities, session, assay_file):
    fields = [Column('existing', TableColumnType.STRING)]
    entities.get_fields = MagicMock(return_value=fields)

    # Entity GET first, then job poll returns COMPLETE.
    entity = {'id': 'entity-1', 'ownerId': 'project-1'}
    completed_job = {'id': 'merge-job-1', 'status': JobStatus.COMPLETE.value}
    session.get.side_effect = [
        MagicMock(status_code=200, json=lambda: entity),
        MagicMock(status_code=200, json=lambda: completed_job),
    ]

    with patch('pipebio.entities.requests.put') as mock_put, \
            patch('pipebio.jobs.time.sleep'):
        mock_put.return_value = MagicMock(status_code=200)
        result = entities.merge('entity-1', assay_file, 'clone_id', 'name')

    assert result == completed_job

    # Uploaded the assay bytes directly to the presigned URL.
    mock_put.assert_called_once()
    assert mock_put.call_args.args[0] == 'https://s3/upload'

    # Created a MergeAssayDataJob referencing the uploaded key, owned by the org.
    job_post = next(c for c in session.post.call_args_list if c.args[0] == 'jobs')
    body = job_post.kwargs['json']
    assert body['type'] == JobType.MergeAssayDataJob.value
    assert body['shareableId'] == 'project-1'
    assert body['ownerId'] == 'org-1'
    assert body['inputEntities'] == ['entity-1']
    params = body['params']
    assert params['entityId'] == 'entity-1'
    assert params['targetTableField'] == 'name'
    assert params['s3Key'] == 'tenant/the-key'
    assert params['appendUnmatchedRows'] is False
    # Schema carries the file-prefixed safe column names (non-alphanumerics stripped).
    names = {col['name'] for col in params['schema']}
    assert any(name.endswith('_cloneid') for name in names)
    assert any(name.endswith('_BindingScore') for name in names)
    # Assay join column resolves to the safe schema name (so the MergeAssayDataJob can match it).
    assert params['assayTableField'].endswith('_cloneid')
    assert params['assayTableField'] in names


def test_merge_raises_when_file_missing(entities):
    with pytest.raises(ValueError, match='does not exist'):
        entities.merge('entity-1', '/no/such/file.csv', 'clone_id', 'name')


def test_merge_raises_when_assay_column_missing(entities, session, assay_file):
    entities.get_fields = MagicMock(return_value=[])

    with patch('pipebio.entities.requests.put'), patch('pipebio.jobs.time.sleep'):
        with pytest.raises(ValueError, match='not found'):
            entities.merge('entity-1', assay_file, 'no_such_column', 'name')


def test_merge_raises_when_job_fails(entities, session, assay_file):
    entities.get_fields = MagicMock(return_value=[])

    entity = {'id': 'entity-1', 'ownerId': 'project-1'}
    failed_job = {'id': 'merge-job-1', 'status': JobStatus.FAILED.value, 'messages': ['boom']}
    session.get.side_effect = [
        MagicMock(status_code=200, json=lambda: entity),
        MagicMock(status_code=200, json=lambda: failed_job),
    ]

    with patch('pipebio.entities.requests.put') as mock_put, \
            patch('pipebio.jobs.time.sleep'):
        mock_put.return_value = MagicMock(status_code=200)
        with pytest.raises(Exception, match='failed: boom'):
            entities.merge('entity-1', assay_file, 'clone_id', 'name')
