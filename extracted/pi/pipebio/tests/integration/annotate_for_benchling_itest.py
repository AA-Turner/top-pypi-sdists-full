import uuid
import os
import re
import csv
from pipebio.pipebio_client import PipebioClient
from pipebio.models.job_type import JobType
from pipebio.annotate.AnnotateForBenchlingParams import (
    AnnotateForBenchlingParams,
    VariableDomain,
    LinkerDomain,
    ConstantDomain,
    ShortScaffold,
    DomainNames
)
from pipebio.shared_python.selection_range import SelectionRange
from tests.test_helpers import get_project_id
from pipebio.column import Column
from pipebio.models.entity_types import EntityTypes
from pipebio.models.sequence_document_kind import SequenceDocumentKind
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_summary import UploadSummary
from pipebio.uploader import Uploader

class TestAnnotateForBenchlingIntegration:

    def setup_method(self):
        self.api_url = os.environ.get("PIPE_API_URL")
        print('PIPE_API_URL', self.api_url)

    def test_full_sdk_run(self):

        print('Starting')

        client = PipebioClient(url=self.api_url)

        project_id = get_project_id(client)
        organization_id = client.user['org']['id']

        germlines = client.organization_lists.get_germlines()

        # Filter for human IMGT germlines
        human_imgt_germlines = [
            g for g in germlines
            if 'human' in g['name'].lower() and 'imgt' in g['name'].lower() and 'tcr' not in g['name'].lower()
        ]

        # Extract version numbers if present
        def get_version(name):
            match = re.search(r'v?(\d+(?:\.\d+)*)', name)
            return float(match.group(1)) if match else -1

        # Sort by version (highest first)
        human_imgt_germlines.sort(key=lambda g: get_version(g['name']), reverse=True)

        human_germline = human_imgt_germlines[0] if human_imgt_germlines else None
        if not human_germline:
            raise Exception('No human IMGT germline found')

        germline_id = human_germline['id']
        print(f"Using germline: {human_germline['name']} (ID: {germline_id})")

        job_run = f'test-{uuid.uuid4()}'

        folder = client.entities.create_folder(
            project_id=project_id,
            name=job_run,
            parent_id=None,
            visible=True
        )

        folder_id = folder['id']

        print('Uploading query/reference sequences as TSV.')
        test_data_dir = os.path.join(os.path.dirname(__file__), "../sample_data")

        def upload_tsv_file(file_name, entity_name):
            file_path = os.path.join(test_data_dir, file_name)

            new_entity = client.entities.create_file(
                project_id=project_id,
                name=entity_name,
                parent_id=folder_id,
                entity_type=EntityTypes.SEQUENCE_DOCUMENT,
            )
            new_entity_id = new_entity['id']
            print(f"Created entity {new_entity_id} for {file_name}")

            input_columns = [
                Column(header='sequence', type=TableColumnType.STRING),
            ]

            uploader = Uploader(new_entity_id, input_columns, client.sequences)

            write_count = 0
            with open(file_path, 'r') as file:
                for row in csv.DictReader(file, delimiter='\t'):
                    uploader.write_data(row)
                    write_count += 1

            ok = uploader.upload()
            assert ok, f"Failed to upload {file_name}"

            summary = UploadSummary(
                new_entity_id,
                sequence_count=write_count,
                sequence_document_kind=SequenceDocumentKind.AA
            )

            client.entities.mark_file_visible(summary)
            print(f"Uploaded {write_count} sequences from {file_name}")

            return new_entity_id

        reference_db_doc_id = upload_tsv_file('aa_database.tsv', 'aa_database.tsv')
        query_db_doc_id = upload_tsv_file('test_sequences_aa.tsv', 'test_sequences_aa.tsv')

        params = AnnotateForBenchlingParams(
            target_folder_id=folder_id,
            scaffolds=[
                ShortScaffold(
                    selection=SelectionRange(start_id=1, end_id=2),
                    domains=[VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id])
                             ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=3, end_id=4),
                    domains=[VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id])
                             ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=5, end_id=6),
                    domains=[VariableDomain(name=DomainNames.VL.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             ConstantDomain(name=DomainNames.CH1.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.H.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.CH2.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.CH3.value, reference_sequences=[reference_db_doc_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id])
                             ]
                ),
                ShortScaffold(
                    selection=SelectionRange(start_id=7, end_id=8),
                    domains=[VariableDomain(name=DomainNames.VL.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             ConstantDomain(name=DomainNames.CH1.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.H.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.CH2.value, reference_sequences=[reference_db_doc_id]),
                             ConstantDomain(name=DomainNames.CH3.value, reference_sequences=[reference_db_doc_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VH.value, germline_ids=[germline_id]),
                             LinkerDomain(name=DomainNames.L.value),
                             VariableDomain(name=DomainNames.VL.value, germline_ids=[germline_id])
                             ]
                ),
            ]
        )

        annotation_job_id = client.jobs.create(
            shareable_id=project_id,
            job_type=JobType.AnnotateForBenchlingJob,
            name=job_run,
            input_entity_ids=[reference_db_doc_id, query_db_doc_id],
            params=params.to_json(),
            owner_id=organization_id,
        )
        # Set a timeout to allow sufficient time for the job to finish.
        client.jobs.poll_job(job_id=annotation_job_id, timeout_seconds=60*10)
        annotation_job = client.jobs.get(annotation_job_id)

        if not annotation_job.get('outputEntities'):
            raise Exception(f"Job failed or produced no output. Status: {annotation_job.get('status')}")

        result_id = annotation_job['outputEntities'][0]['id']

        # Download the results (e.g. for post-processing in Benchling).
        absolute_location = os.path.join(os.getcwd(), f'Benchling annotation - {job_run}.tsv')
        client.sequences.download(result_id, destination=absolute_location)
        print(f'Downloaded results to: {absolute_location}')


