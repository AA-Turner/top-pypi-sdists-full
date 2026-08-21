"""Unit tests for pipebio.jobs module."""

import pytest
from unittest.mock import patch, MagicMock

from pipebio.jobs import Jobs
from pipebio.models.job_filter import JobFilter
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.output_link import OutputLink


@pytest.fixture
def mock_session():
    """Create a mock session for Jobs."""
    session = MagicMock()
    session.post.return_value = MagicMock(status_code=200, json=lambda: {'id': 'job-123'})
    session.get.return_value = MagicMock(status_code=200, json=lambda: {'data': []})
    session.patch.return_value = MagicMock(status_code=204)
    session.delete.return_value = MagicMock(status_code=204)
    return session


@pytest.fixture
def mock_user():
    """Create a mock user with org."""
    return {'org': {'id': 'org-123'}}


@pytest.fixture
def jobs(mock_session, mock_user):
    """Create Jobs instance with mocked dependencies."""
    with patch('pipebio.jobs.Util.mount_standard_session', return_value=mock_session):
        with patch('pipebio.jobs.Util.get_organization_id', return_value='org-123'):
            return Jobs(mock_session, mock_user, 'job-123')


class TestJobFilter:
    """Tests for JobFilter model."""

    def test_to_json_basic(self):
        f = JobFilter(key='status', comparator='=', value='FAILED')
        assert f.to_json() == {'key': 'status', 'comparator': '=', 'value': 'FAILED', 'joiner': 'AND'}

    def test_to_json_with_joiner_or(self):
        f = JobFilter(key='type', comparator='=', value='ImportJob', joiner='OR')
        assert f.to_json() == {
            'key': 'type', 'comparator': '=', 'value': 'ImportJob', 'joiner': 'OR'
        }

    def test_to_json_with_joiner_and_included(self):
        f = JobFilter(key='status', comparator='=', value='RUNNING', joiner='AND')
        assert f.to_json()['joiner'] == 'AND'

    def test_allowed_comparators(self):
        for comp in ['=', '!=', '>', '<', 'LIKE', 'NOT LIKE', 'ILIKE', 'NOT ILIKE']:
            f = JobFilter(key='x', comparator=comp, value='test')
            assert f.comparator == comp

    def test_invalid_comparator_raises(self):
        with pytest.raises(ValueError, match='Invalid comparator'):
            JobFilter(key='x', comparator='INVALID', value='test')

    def test_invalid_joiner_raises(self):
        with pytest.raises(ValueError, match='Invalid joiner'):
            JobFilter(key='x', comparator='=', value='test', joiner='XOR')

    def test_value_types(self):
        f1 = JobFilter(key='progress', comparator='>', value=50)
        assert f1.to_json() == {'key': 'progress', 'comparator': '>', 'value': 50, 'joiner': 'AND'}

        f2 = JobFilter(key='active', comparator='=', value=True)
        assert f2.to_json()['value'] is True


class TestJobsList:
    """Tests for Jobs.list() method."""

    def test_list_backwards_compatible(self, jobs, mock_session):
        """Existing call pattern with only organization_id works."""
        jobs.list()
        mock_session.get.assert_called_once_with('jobs', params={'organizationId': 'org-123'})
        mock_session.post.assert_not_called()

    def test_list_with_organization_id(self, jobs, mock_session):
        jobs.list(organization_id='custom-org')
        mock_session.get.assert_called_once_with('jobs', params={'organizationId': 'custom-org'})

    def test_list_with_pagination(self, jobs, mock_session):
        jobs.list(page_offset=10, page_limit=50)
        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert call_args[1]['params']['pageOffset'] == 10
        assert call_args[1]['params']['pageLimit'] == 50

    def test_list_with_sort(self, jobs, mock_session):
        jobs.list(sort='-created_at,name')
        assert mock_session.get.call_args[1]['params']['sort'] == '-created_at,name'

    def test_list_with_include_cols(self, jobs, mock_session):
        jobs.list(include_cols=['id', 'status', 'name'])
        assert mock_session.get.call_args[1]['params']['includeCols'] == 'id,status,name'

    def test_list_with_include_total_count(self, jobs, mock_session):
        jobs.list(include_total_count=True)
        assert mock_session.get.call_args[1]['params']['includeTotalCount'] == 'true'

    def test_list_with_filters_uses_post_search(self, jobs, mock_session):
        filters = [
            JobFilter(key='status', comparator='=', value='FAILED'),
            JobFilter(key='type', comparator='=', value='ImportJob', joiner='OR'),
        ]
        jobs.list(filters=filters)
        mock_session.post.assert_called_once()
        call_args = mock_session.post.call_args
        assert call_args[0][0] == 'jobs/_search'
        assert call_args[1]['json']['filter'] == [
            {'key': 'status', 'comparator': '=', 'value': 'FAILED', 'joiner': 'AND'},
            {'key': 'type', 'comparator': '=', 'value': 'ImportJob', 'joiner': 'OR'},
        ]
        assert call_args[1]['params']['organizationId'] == 'org-123'
        mock_session.get.assert_not_called()

    def test_list_with_filters_and_pagination(self, jobs, mock_session):
        filters = [JobFilter(key='status', comparator='=', value='COMPLETE')]
        jobs.list(filters=filters, page_limit=25)
        call_args = mock_session.post.call_args
        assert call_args[1]['params']['pageLimit'] == 25
        assert call_args[1]['json']['filter'] == [
            {'key': 'status', 'comparator': '=', 'value': 'COMPLETE', 'joiner': 'AND'}
        ]

    def test_list_empty_filters_uses_get(self, jobs, mock_session):
        jobs.list(filters=[])
        mock_session.get.assert_called_once()
        mock_session.post.assert_not_called()


class TestJobsCreate:
    """Tests for Jobs.create() method."""

    def test_create_backwards_compatible(self, jobs, mock_session):
        """Existing call pattern works unchanged."""
        job_id = jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
        )
        assert job_id == 'job-123'
        call_args = mock_session.post.call_args
        body = call_args[1]['json']
        assert body['shareableId'] == 'proj-1'
        assert body['inputEntities'] == ['ent-1']
        assert body['name'] == 'Export'
        assert body['type'] == 'ExportJob'
        assert 'messages' not in body
        assert 'status' not in body

    def test_create_with_messages(self, jobs, mock_session):
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ImportJob,
            name='Import',
            input_entity_ids=[],
            messages=['Starting import'],
        )
        assert mock_session.post.call_args[1]['json']['messages'] == ['Starting import']

    def test_create_with_status(self, jobs, mock_session):
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ImportJob,
            name='Import',
            input_entity_ids=[],
            status=JobStatus.QUEUED,
        )
        assert mock_session.post.call_args[1]['json']['status'] == 'QUEUED'

    def test_create_with_allow_deleted_entities(self, jobs, mock_session):
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ImportJob,
            name='Import',
            input_entity_ids=[],
            allow_deleted_entities=True,
        )
        assert mock_session.post.call_args[1]['params'] == {'allowDeletedEntities': 'true'}

    def test_create_injects_correlation_id_from_session_header(self, jobs, mock_session):
        """When X-Correlation-Id is set on the session, it is injected into job params."""
        mock_session.headers = {"X-Correlation-Id": "corr-abc-123"}
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
        )
        body = mock_session.post.call_args[1]['json']
        assert body['params']['correlationId'] == 'corr-abc-123'

    def test_create_does_not_override_explicit_correlation_id(self, jobs, mock_session):
        """Explicit correlationId in params takes precedence over the session header."""
        mock_session.headers = {"X-Correlation-Id": "from-header"}
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
            params={"correlationId": "explicit-value"},
        )
        body = mock_session.post.call_args[1]['json']
        assert body['params']['correlationId'] == 'explicit-value'

    def test_create_omits_correlation_id_when_not_set(self, jobs, mock_session):
        """When no X-Correlation-Id header is set, params should not contain correlationId."""
        mock_session.headers = {}
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
        )
        body = mock_session.post.call_args[1]['json']
        assert 'correlationId' not in body['params']

    def test_create_omits_correlation_id_when_empty_string(self, jobs, mock_session):
        """An empty-string header value is treated as unset and should not inject correlationId."""
        mock_session.headers = {"X-Correlation-Id": ""}
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
        )
        body = mock_session.post.call_args[1]['json']
        assert 'correlationId' not in body['params']

    def test_create_does_not_mutate_caller_params(self, jobs, mock_session):
        """The caller's original params dict must not be modified by create()."""
        mock_session.headers = {"X-Correlation-Id": "corr-xyz"}
        original_params = {"customKey": "value"}
        jobs.create(
            shareable_id='proj-1',
            job_type=JobType.ExportJob,
            name='Export',
            input_entity_ids=['ent-1'],
            params=original_params,
        )
        assert 'correlationId' not in original_params


class TestJobsUpdate:
    """Tests for Jobs.update() method."""

    def test_update_with_allow_deleted_entities(self, jobs, mock_session):
        jobs.update(JobStatus.COMPLETE, allow_deleted_entities=True)
        call_args = mock_session.patch.call_args
        assert call_args[1]['params'] == {'allowDeletedEntities': 'true'}
        assert call_args[1]['json']['status'] == 'COMPLETE'


class TestJobsStartImportJob:
    """Tests for Jobs.start_import_job() method."""

    def test_start_import_job_default(self, jobs, mock_session):
        jobs.start_import_job()
        mock_session.patch.assert_called_once_with(
            'jobs/job-123/import',
            json=None,
        )

    def test_start_import_job_with_file_size(self, jobs, mock_session):
        jobs.start_import_job(file_size=1024)
        mock_session.patch.assert_called_once_with(
            'jobs/job-123/import',
            json={'fileSize': 1024},
        )


class TestJobsCancel:
    """Tests for Jobs.cancel() method."""

    def test_cancel_uses_instance_job_id(self, jobs, mock_session):
        jobs.cancel()
        mock_session.delete.assert_called_once_with('jobs/job-123')

    def test_cancel_with_job_id(self, jobs, mock_session):
        jobs.cancel(job_id='other-job-id')
        mock_session.delete.assert_called_once_with('jobs/other-job-id')


class TestJobsReschedule:
    """Tests for Jobs.reschedule() method."""

    def test_reschedule_default(self, jobs, mock_session):
        mock_session.post.return_value = MagicMock(status_code=200, json=lambda: {'id': 'job-123', 'status': 'QUEUED'})
        result = jobs.reschedule()
        mock_session.post.assert_called_once_with('jobs/job-123/reschedule', json=None)
        assert result['id'] == 'job-123'

    def test_reschedule_with_automated(self, jobs, mock_session):
        mock_session.post.return_value = MagicMock(status_code=200, json=lambda: {'id': 'job-123'})
        jobs.reschedule(job_id='job-456', automated=True)
        mock_session.post.assert_called_once_with(
            'jobs/job-456/reschedule',
            json={'automated': True},
        )


class TestJobsBulkUpdate:
    """Tests for Jobs.bulk_update() method."""

    def test_bulk_update_success(self, jobs, mock_session):
        updates = [
            {'id': 'job-1', 'status': 'COMPLETE'},
            {'id': 'job-2', 'status': 'FAILED', 'messages': ['Error']},
        ]
        jobs.bulk_update(updates)
        mock_session.patch.assert_called_once_with(
            'jobs',
            json={'updates': updates},
        )

    def test_bulk_update_empty_raises(self, jobs):
        with pytest.raises(ValueError, match='At least one update'):
            jobs.bulk_update([])

    def test_bulk_update_too_many_raises(self, jobs):
        updates = [{'id': f'job-{i}', 'status': 'CANCELLED'} for i in range(101)]
        with pytest.raises(ValueError, match='Maximum 100'):
            jobs.bulk_update(updates)


class TestJobsGet:
    """Tests for Jobs.get() - ensure backwards compat."""

    def test_get_uses_instance_job_id(self, jobs, mock_session):
        jobs.get()
        mock_session.get.assert_called_with('jobs/job-123')

    def test_get_with_explicit_job_id(self, jobs, mock_session):
        jobs.get(job_id='explicit-id')
        mock_session.get.assert_called_with('jobs/explicit-id')


class TestJobsPollJob:
    """Tests for Jobs.poll_job() timeout behavior."""

    def test_poll_job_waits_indefinitely_by_default(self, jobs):
        """Polling without a timeout waits past the old 600s default."""
        responses = [{'status': 'RUNNING'}] * 200 + [
            {'status': 'COMPLETE', 'id': 'job-456'}
        ]

        with patch('pipebio.jobs.time.sleep'), \
                patch('pipebio.jobs.time.time', side_effect=range(0, 10000, 5)), \
                patch.object(jobs, 'get', side_effect=lambda _: responses.pop(0)), \
                patch('builtins.print'):
            job = jobs.poll_job('job-456')

        assert job['status'] == 'COMPLETE'

    def test_poll_job_waits_indefinitely_when_timeout_is_none(self, jobs):
        """Explicit None matches the omitted-timeout default."""
        responses = [{'status': 'RUNNING'}] * 200 + [
            {'status': 'COMPLETE', 'id': 'job-456'}
        ]

        with patch('pipebio.jobs.time.sleep'), \
                patch('pipebio.jobs.time.time', side_effect=range(0, 10000, 5)), \
                patch.object(jobs, 'get', side_effect=lambda _: responses.pop(0)), \
                patch('builtins.print'):
            job = jobs.poll_job('job-456', timeout_seconds=None)

        assert job['status'] == 'COMPLETE'

    def test_poll_job_honors_explicit_timeout(self, jobs):
        """An explicit timeout still raises when elapsed."""
        times = iter([0, 6, 12])

        with patch('pipebio.jobs.time.sleep'), \
                patch('pipebio.jobs.time.time', side_effect=lambda: next(times)), \
                patch.object(jobs, 'get', return_value={'status': 'RUNNING'}), \
                patch('builtins.print'):
            with pytest.raises(Exception, match='Timeout waiting for job job-456'):
                jobs.poll_job('job-456', timeout_seconds=10)
