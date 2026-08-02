import csv
import os
import tempfile
from inspect import getsourcefile
from os.path import dirname

from pipebio.column import Column
from pipebio.models.entity_types import EntityTypes
from pipebio.models.sequence_document_kind import SequenceDocumentKind
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_summary import UploadSummary
from pipebio.pipebio_client import PipebioClient
from pipebio.uploader import Uploader
from tests.test_helpers import get_parent_id, get_project_id


class TestMergeIntegration:

    def setup_method(self) -> None:
        self.api_url = os.environ.get("PIPE_API_URL")
        print('PIPE_API_URL', self.api_url)

    def test_merge_assay_data(self) -> None:
        """Upload a small document, then merge assay data into it via the async MergeAssayDataJob path."""
        client = PipebioClient(url=self.api_url)

        parent_folder_id = get_parent_id(client)
        project_id = get_project_id(client)

        # Create a small sequence document to merge into.
        entity = client.entities.create_file(
            project_id=project_id,
            name='merge_target.tsv',
            parent_id=parent_folder_id,
            entity_type=EntityTypes.SEQUENCE_DOCUMENT,
        )
        entity_id = entity['id']

        rows = [
            {'name': 'clone_a', 'sequence': 'ACGT'},
            {'name': 'clone_b', 'sequence': 'TGCA'},
        ]
        # NOTE: do not declare a 'name' column here. The Uploader always appends a
        # reserved 'name' column and fills it from each row's 'name' value, so
        # declaring our own would submit a duplicate column and the import fails
        # with a DuckDB "Column with name name already exists" error. The join key
        # rides on that reserved 'name' column (entity_column='name' below).
        columns = [
            Column(header='sequence', type=TableColumnType.STRING),
        ]
        uploader = Uploader(entity_id, columns, client.sequences)
        for row in rows:
            uploader.write_data(row)
        assert uploader.upload()
        client.entities.mark_file_visible(
            UploadSummary(entity_id, sequence_count=len(rows), sequence_document_kind=SequenceDocumentKind.DNA)
        )

        # Build an assay file keyed by the document's `name` column.
        assay_path = os.path.join(tempfile.gettempdir(), 'assay_scores.csv')
        with open(assay_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['clone_id', 'BindingScore'])
            writer.writerow(['clone_a', '95.2'])
            writer.writerow(['clone_b', '82.7'])

        # Merge assay data: uploads via presigned URL, runs a MergeAssayDataJob, blocks until complete.
        job = client.entities.merge(
            entity_id=entity_id,
            assay_absolute_file_path=assay_path,
            assay_column='clone_id',
            entity_column='name',
        )
        assert job['status'] == 'COMPLETE', f"Merge failed: {job.get('messages')}"

        # The merged assay column should now be present on the document.
        field_names = [c.name for c in client.entities.get_fields(entity_id)]
        assert any(name.endswith('_BindingScore') for name in field_names), field_names
