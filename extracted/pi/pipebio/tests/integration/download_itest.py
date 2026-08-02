import os
import re
import tempfile
from pipebio.models.export_format import ExportFormat
from pipebio.pipebio_client import PipebioClient
from tests.test_helpers import get_adimab_vh_id


class TestPipeBioClientIntegration:

    def setup_method(self):
        self.api_url = os.environ.get("PIPE_API_URL")
        print('PIPE_API_URL', self.api_url)

    def test_download_file_as_tsv(self):
        # Set the download name and folder.

        client = PipebioClient(url=self.api_url)
        document_id = get_adimab_vh_id(client)

        destination_filename = f"{document_id}.tsv"
        absolute_location = os.path.join(tempfile.gettempdir(), destination_filename)

        client.sequences.download(
            entity_id=document_id,
            destination=absolute_location,
        )

        # Verify file was downloaded successfully
        assert os.path.exists(absolute_location), f"Downloaded file not found at {absolute_location}"
        assert os.path.getsize(absolute_location) > 0, f"Downloaded file is empty at {absolute_location}"

        with open(absolute_location, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 138

        # Clean up
        os.remove(absolute_location)

    def test_download_file_to_memory(self):
        client = PipebioClient(url=self.api_url)

        document_id = get_adimab_vh_id(client)
        result = client.sequences.download_to_memory([document_id])

        assert len(result) == 137

        row_id = f'{document_id}##@##1'
        assert result[row_id]['name'] == 'P00125_A01 abituzumab'
        assert result[row_id][
                   'sequence'] == 'CAGGTGCAGCTGCAGCAGAGCGGCGGCGAGCTGGCCAAGCCCGGCGCCAGCGTGAAGGTGAGCTGCAAGGCCAGCGGCTACACCTTCAGCAGCTTCTGGATGCACTGGGTGAGGCAGGCCCCCGGCCAGGGCCTGGAGTGGATCGGCTACATCAACCCCAGGAGCGGCTACACCGAGTACAACGAGATCTTCAGGGACAAGGCCACCATGACCACCGACACCAGCACCAGCACCGCCTACATGGAGCTGAGCAGCCTGAGGAGCGAGGACACCGCCGTGTACTACTGCGCCAGCTTCCTGGGCAGGGGCGCCATGGACTACTGGGGCCAGGGCACCACCGTGACCGTGAGCAGC'

    def test_download_to_biological_format(self):
        # Set the download name and folder.
        absolute_location = tempfile.gettempdir()

        client = PipebioClient(url=self.api_url)

        document_id = get_adimab_vh_id(client)

        client.export(
            entity_id=document_id,
            format=ExportFormat.GENBANK,
            destination_folder=absolute_location,
            destination_filename='myFile.gb'
        )

        # Verify file was downloaded successfully
        download_file = os.path.join(absolute_location, 'myFile.gb')
        assert os.path.exists(download_file), f"Downloaded file not found at {download_file}"
        assert os.path.getsize(download_file) > 0, f"Downloaded file is empty at {download_file}"

        # Open the file and check the first line
        with open(download_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 2375
            # Check all parts except the date which changes
            first_line = lines[0]
            assert first_line.startswith('LOCUS       P00125_A01abituz         354 bp    DNA              UNK ')
            # Ensure it has the date format but don't check the exact date
            assert re.match(r'LOCUS\s+P00125_A01abituz\s+354 bp\s+DNA\s+UNK\s+\d{2}-[A-Z]{3}-\d{4}\n$', first_line)

        # Clean up.
        os.remove(download_file)
