import csv
import os
from inspect import getsourcefile
from os.path import dirname
from unittest.mock import patch

import pytest

from pipebio.column import Column
from pipebio.models.entity_types import EntityTypes
from pipebio.models.sequence_document_kind import SequenceDocumentKind
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_summary import UploadSummary
from pipebio.multipart_upload import upload_multipart_aws
from pipebio.pipebio_client import PipebioClient
from pipebio.uploader import Uploader
from tests.test_helpers import get_project_id, get_parent_id


class TestPipeBioClientIntegration:

    def setup_method(self):
        self.api_url = os.environ.get("PIPE_API_URL")
        print('PIPE_API_URL', self.api_url)

    def test_upload_fasta_file(self):
        """Test file upload and export functionality."""

        client = PipebioClient(url=self.api_url)

        file_name = '137_adimab_VH.fsa'
        current_dir = dirname(getsourcefile(lambda: 0))
        test_file = os.path.join(current_dir, '../sample_data/adimab', file_name)

        parent_folder_id = get_parent_id(client)
        project_id = get_project_id(client)

        # Test file upload
        result = client.upload_file(
            file_name=file_name,
            absolute_file_location=test_file,
            parent_id=parent_folder_id,
            project_id=project_id,
        )
        ten_mins = 10 * 60
        job = client.jobs.poll_job(result['id'], ten_mins)

        assert job["status"] == "COMPLETE", "Upload failed"

    def test_upload_tsv_file(self):
        sequence_document_kind = SequenceDocumentKind.DNA

        client = PipebioClient(url=self.api_url)

        parent_folder_id = get_parent_id(client)
        project_id = get_project_id(client)

        # Get file to upload.
        file_name = 'upload.tsv'
        current_dir = dirname(getsourcefile(lambda: 0))
        file_path = os.path.join(current_dir, f'../sample_data/{file_name}')

        # First create the entity
        new_entity = client.entities.create_file(
            project_id=project_id,
            name='upload2.tsv',
            parent_id=parent_folder_id,
            entity_type=EntityTypes.SEQUENCE_DOCUMENT,
        )
        new_entity_id = new_entity['id']
        print(f"Created new_entity {new_entity_id} {file_name}")

        # Specify the column schema
        input_columns = [
            # id, name, description, labels added automatically
            Column(header='sequence', type=TableColumnType.STRING),
        ]

        uploader = Uploader(new_entity_id, input_columns, client.sequences)

        # Write the rows from the TSV file
        write_count = 0
        with open(file_path, 'r') as file:
            for row in csv.DictReader(file, delimiter='\t'):
                uploader.write_data(row)
                write_count = write_count + 1

        # Upload the file contents
        ok = uploader.upload()
        assert ok

        summary = UploadSummary(
            new_entity_id,
            sequence_count=write_count,
            sequence_document_kind=sequence_document_kind
        )

        # Finally, mark the file as visible
        client.entities.mark_file_visible(summary)

        assert write_count == 137, f"Expected write_count to be 137, but got {write_count}"

        written_entity = client.entities.get(new_entity_id)
        assert written_entity['sequenceCount'] == 137, f"Expected sequenceCount to be 137, but got {written_entity['sequenceCount']}"

    def test_upload_file_via_multipart(self):
        """Test the multipart upload path by lowering the threshold so a small file triggers it."""
        client = PipebioClient(url=self.api_url)

        if not client.is_aws:
            pytest.skip("Multipart upload is only supported on AWS")

        file_name = '137_adimab_VH.fsa'
        current_dir = dirname(getsourcefile(lambda: 0))
        test_file = os.path.join(current_dir, '../sample_data/adimab', file_name)

        project_id = get_project_id(client)

        with patch("pipebio.pipebio_client.MULTIPART_THRESHOLD", 1024), \
             patch("pipebio.pipebio_client.upload_multipart_aws", wraps=upload_multipart_aws) as mock_multipart:
            result = client.upload_file(
                file_name=file_name,
                absolute_file_location=test_file,
                parent_id=None,
                project_id=project_id,
            )
            assert mock_multipart.call_count == 1, "Expected multipart upload path to be used"

        ten_mins = 10 * 60
        job = client.jobs.poll_job(result['id'], ten_mins)
        assert job["status"] == "COMPLETE", f"Multipart upload failed: {job.get('messages')}"
