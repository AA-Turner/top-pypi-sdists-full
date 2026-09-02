import unittest
import sys

from unittest.mock import patch, mock_open, MagicMock

import eumdac
from eumdac.cli import cli
from eumdac.collection import Collection
from eumdac.order import Order

from .base import INTEGRATION_TESTING


class CliExit(Exception):
    pass


class CliError(Exception):
    pass


class TestCommandLineInterface(unittest.TestCase):
    credentials = ("abc", "xyz")

    def setUp(self):
        super().setUp()
        self.patch_argv()
        self.get_mock("argparse.ArgumentParser.exit", new=MagicMock(side_effect=CliExit))
        self.mock_error = self.get_mock(
            "argparse.ArgumentParser.error", new=MagicMock(side_effect=CliError)
        )
        self.mock_stdin = self.get_mock("eumdac.cli.sys.stdin", new_callable=mock_open())
        self.mock_stdin.isatty.return_value = False

    def patch_argv(self):
        patcher = patch.object(sys, "argv", ["eumdac"])
        patcher.start()
        self.addCleanup(patcher.stop)

    def get_mock(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        mock = patcher.start()
        self.addCleanup(patcher.stop)
        return mock

    @unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
    @patch("eumdac.cli_helpers.get_datastore")
    @patch("eumdac.cli_helpers.load_credentials")
    def test_download_coverage(self, _load_credentials, mock_get_datastore):
        mock_DataStore = MagicMock(spec=eumdac.DataStore)
        mock_get_datastore.return_value = mock_DataStore
        _load_credentials.return_value = self.credentials
        mock_collection = MagicMock(spec=Collection)
        mock_collection.search.return_value = []
        mock_DataStore.get_collection.return_value = mock_collection

        command_line = [
            "download",
            "-c",
            "EO:EUM:DAT:0665",
            "--limit",
            "1",
            "--download-coverage",
            "FD",
        ]

        cli(command_line)

    def test_is_collection_valid_for_coverage(self):
        from eumdac.cli_mtg_helpers import is_collection_valid_for_coverage

        # Valid collections for coverage downloading
        for i in [
            "0662",
            "0665",
            "0672",
        ]:
            self.assertTrue(is_collection_valid_for_coverage(f"EO:EUM:DAT:{i}"))
            self.assertTrue(is_collection_valid_for_coverage(f"EO:EUMIVV:DAT:{i}"))
            self.assertTrue(is_collection_valid_for_coverage(f"EO:EUMVAL:DAT:{i}"))
            self.assertTrue(is_collection_valid_for_coverage(f"EO:EUM:DAT:{i}:COM"))

        # MTG collections invalid for coverage download
        for i in [
            "0659",
            "0660",
            "0661",
            "0664",
            "0667",
            "0668",
            "0669",
            "0670",
            "0671",
            "0674",
            "0675",
            "0676",
            "0677",
            "0678",
            "0679",
            "0680",
            "0681",
            "0682",
            "0683",
            "0684",
            "0685",
            "0686",
            "0687",
            "0688",
            "0689",
            "0690",
            "0691",
            "0692",
            "0693",
            "0694",
            "0749",
            "0750",
            "0751",
            "0752",
            "0753",
            "0773",
            "0774",
            "0775",
            "0782",
            "0788",
            "0789",
            "0790",
            "0791",
            "0792",
            "0793",
            "0794",
            "0795",
            "0796",
            "0799",
            "0800",
            "0801",
            "0845",
        ]:
            self.assertFalse(is_collection_valid_for_coverage(f"EO:EUM:DAT:{i}"))
            self.assertFalse(is_collection_valid_for_coverage(f"EO:EUMIVV:DAT:{i}"))
            self.assertFalse(is_collection_valid_for_coverage(f"EO:EUMVAL:DAT:{i}"))
            self.assertFalse(is_collection_valid_for_coverage(f"EO:EUM:DAT:{i}:COM"))

        # Invalid collections for coverage downloading
        for c in ["EO:EUM:DAT:MSG:HRSEVIRI", ""]:
            self.assertFalse(is_collection_valid_for_coverage(c))
