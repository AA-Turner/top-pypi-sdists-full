import io
import unittest
import re
import os
import datetime
import sys
from unittest.mock import patch, mock_open, MagicMock

import pytest

import eumdac
from eumdac.cli import cli
from eumdac.collection import Collection
from eumdac.errors import EumdacError
from eumdac.product import Product


def get_mock_collection(product_ids):
    mock_stream = io.BytesIO(b"ProductBytes")
    mock_stream.name = "MockProduct.zip"

    mock_collection = MagicMock(spec=Collection)
    mock_collection._id = "MockCollection"

    mock_collection_search_products = []
    for product_id in product_ids:
        mock_product = MagicMock(spec=Product)
        mock_product.open.return_value.__enter__.return_value = mock_stream
        mock_product._id = product_id
        mock_product.collection = mock_collection
        mock_collection_search_products.append(mock_product)

    mock_collection.search.return_value = mock_collection_search_products

    return mock_collection


class CliExit(Exception):
    pass


class CliError(Exception):
    pass


class TestCommandLineInterface(unittest.TestCase):
    credentials = ("abc", "xyz")

    def setUp(self):
        super().setUp()
        self.patch_argv()
        self.cli = cli
        self.get_mock("argparse.ArgumentParser.exit", new=MagicMock(side_effect=CliExit))
        self.mock_error = self.get_mock(
            "argparse.ArgumentParser.error", new=MagicMock(side_effect=CliError)
        )
        self.mock_stdin = self.get_mock("eumdac.cli.sys.stdin", new_callable=mock_open())
        self.mock_stdin.isatty.return_value = False

    @pytest.fixture(autouse=True)
    def propagate_pytest_fixtures(self, monkeypatch, tmp_path):
        self.monkeypatch = monkeypatch
        self.tmp_path = tmp_path

    def patch_argv(self):
        patcher = patch.object(sys, "argv", ["eumdac"])
        patcher.start()
        self.addCleanup(patcher.stop)

    def get_mock(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        mock = patcher.start()
        self.addCleanup(patcher.stop)
        return mock

    @patch("eumdac.AccessToken")
    @patch("pathlib.Path.open", new_callable=mock_open)
    def test_set_credentials(self, mock_path_open, mock_AccessToken):
        consumer_key, consumer_secret = self.credentials
        command_line = ["--set-credentials", consumer_key, consumer_secret]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(CliExit):
                self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), r"Credentials are correct.")
        mock_path_open.return_value.__enter__().write.assert_called_once_with(
            f"{consumer_key},{consumer_secret}"
        )

    @patch("eumdac.cli_helpers.load_credentials")
    @patch("eumdac.cli_helpers.DataStore")
    def test_describe_list_collections(self, mock_DataStore, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        collection = MagicMock(spec=Collection)
        collection.__str__.return_value = "MockCollection"
        collection.title = "MockTitle"
        mock_DataStore.return_value.collections = [collection]
        command_line = ["describe"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), "MockCollection - MockTitle")

    def test_print_help(self):
        regex = re.compile(f"usage: (.*(\r)?\n)+EUMETSAT Data Access Client", re.MULTILINE)
        command_line = ["--help"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(CliExit):
                self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), regex)

        # print help if no argument is given
        command_line = []
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), regex)

    def test_print_version(self):
        command_line = ["--version"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(CliExit):
                self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), re.escape(eumdac.__version__))

    def test_pipe_in(self):
        self.mock_stdin.read.return_value = "--version"
        with patch("eumdac.cli.sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(CliExit):
                self.cli()
            self.assertRegex(mock_stdout.getvalue(), re.escape(eumdac.__version__))

    @patch("eumdac.cli_helpers.load_credentials")
    @patch("eumdac.cli_helpers.DataStore")
    def test_describe_collection(self, mock_DataStore, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        collection = MagicMock(spec=Collection)
        collection.__str__.return_value = "MockCollection"
        collection.title = "MockTitle"
        collection.abstract = "MockAbstract"
        collection.metadata = {"properties": {"date": "2020/"}}
        mock_DataStore.return_value.get_collection.return_value = collection
        command_line = ["describe", "-c", "MockCollection"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            regex = re.compile(
                f"MockCollection.*MockTitle(.*(\r)?\n)+Date:(.*(\r)?\n)+MockAbstract",
                re.MULTILINE,
            )
            out = mock_stdout.getvalue()
            self.assertRegex(out, regex)

    @patch("eumdac.cli_helpers.load_credentials")
    def test_describe_product_without_collection(self, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        command_line = ["describe", "-p", "MockProduct", "--debug"]
        with self.assertRaises(ValueError):
            self.cli(command_line)

    @patch("eumdac.cli_helpers.load_credentials")
    @patch("eumdac.cli_helpers.DataStore")
    def test_describe_product(self, mock_DataStore, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        product = MagicMock(spec=Product)
        product.__str__.return_value = "MockProduct"
        product.collection = "MockCollection"
        product.satellite = "MockSatellite"
        product.instrument = "MockInstrument"
        product.acronym = "MockAcronym"
        product.sensing_start = datetime.datetime(2020, 1, 1)
        product.sensing_end = datetime.datetime(2020, 1, 2)
        product.size = 123456
        product.ingested = datetime.datetime(2020, 1, 2)
        product.md5 = "123456789"
        product.entries = [
            "product_file_1.nc",
            "product_file_2.nc",
            "product_file_3.nc",
            "product_group/entry1.nc",
            "product_group/entry2.nc",
            "product_group/entry3/file.nc",
            "metadata.xml",
        ]
        mock_DataStore.return_value.get_product.return_value = product
        expected_lines = [
            "MockCollection - MockProduct",
            "Platform: MockSatellite",
            "Instrument: MockInstrument",
            "Acronym: MockAcronym",
            "Orbit: LEO",
            "Sensing Start: 2020-01-01T00:00:00.000Z",
            "Sensing End: 2020-01-02T00:00:00.000Z",
            "Size: 123456 KB",
            "Published: 2020-01-02T00:00:00.000Z",
            "MD5: 123456789",
            "SIP Entries:",
            "product_file_1.nc",
            "product_file_2.nc",
            "product_file_3.nc",
            "product_group/",
            "- entry1.nc",
            "- entry2.nc",
            "- entry3/file.nc",
            "metadata.xml",
            "",
        ]
        command_line = ["describe", "-c", "MockCollection", "-p", "MockProduct"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            for line in expected_lines:
                self.assertIn(line, mock_stdout.getvalue())

    @patch("eumdac.cli_helpers.load_credentials")
    @patch("eumdac.cli_helpers.DataStore")
    def test_describe_product_flat(self, mock_DataStore, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        product = MagicMock(spec=Product)
        product.__str__.return_value = "MockProduct"
        product.collection = "MockCollection"
        product.satellite = "MockSatellite"
        product.instrument = "MockInstrument"
        product.acronym = "MockAcronym"
        product.sensing_start = datetime.datetime(2020, 1, 1)
        product.sensing_end = datetime.datetime(2020, 1, 2)
        product.size = 123456
        product.ingested = datetime.datetime(2020, 1, 2)
        product.md5 = "123456789"
        product.entries = [
            "product_file_1.nc",
            "product_file_2.nc",
            "product_file_3.nc",
            "product_group/entry1.nc",
            "product_group/entry2.nc",
            "product_group/entry3/file.nc",
            "metadata.xml",
        ]
        mock_DataStore.return_value.get_product.return_value = product
        expected_lines = [
            "MockCollection - MockProduct",
            "Platform: MockSatellite",
            "Instrument: MockInstrument",
            "Acronym: MockAcronym",
            "Orbit: LEO",
            "Sensing Start: 2020-01-01T00:00:00.000Z",
            "Sensing End: 2020-01-02T00:00:00.000Z",
            "Size: 123456 KB",
            "Published: 2020-01-02T00:00:00.000Z",
            "MD5: 123456789",
            "SIP Entries:",
            "product_file_1.nc",
            "product_file_2.nc",
            "product_file_3.nc",
            "product_group/entry1.nc",
            "product_group/entry2.nc",
            "product_group/entry3/file.nc",
            "metadata.xml",
            "",
        ]
        command_line = ["describe", "-c", "MockCollection", "-p", "MockProduct", "--flat"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            for line in expected_lines:
                self.assertIn(line, mock_stdout.getvalue())

    @patch("eumdac.cli_helpers.AccessToken")
    @patch("eumdac.cli_helpers.DataStore")
    @patch("eumdac.cli_helpers.load_credentials")
    def test_load_credentials(self, mock_load_credentials, mock_DataStore, mock_AccessToken):
        mock_load_credentials.return_value = ("CONSUMER_KEY", "CONSUMER_SECRET")
        mock_DataStore.return_value.collections = []
        command_line = ["describe"]
        self.cli(command_line)
        mock_AccessToken.assert_called_once_with(("CONSUMER_KEY", "CONSUMER_SECRET"))

    @patch("pathlib.Path.read_text")
    @patch("eumdac.cli_helpers.DataStore")
    def test_load_credentials_file_not_found(self, mock_DataStore, mock_read_text):
        mock_read_text.side_effect = FileNotFoundError
        command_line = (
            "download -c EO:EUM:DAT:MSG:MSG15-RSS "
            "--time-range 2021-09-20 2022-09-30 --limit 1 --debug"
        ).split()
        with self.assertRaises(EumdacError):
            self.cli(command_line)

    @patch("eumdac.cli_helpers.get_credentials_path")
    @patch("eumdac.cli.AccessToken")
    @patch("eumdac.cli_helpers.DataStore")
    def test_load_credentials_corrupted_file(
        self, mock_DataStore, mock_AccessToken, mock_get_credentials_path
    ):
        mock_get_credentials_path.return_value.read_text.return_value = "corrupted!"
        mock_DataStore.return_value.collections = []
        command_line = ["describe", "--debug"]
        with self.assertRaises(EumdacError):
            self.cli(command_line)

    @patch("eumdac.cli_helpers.get_datastore")
    @patch("eumdac.cli_helpers.load_credentials")
    def test_search(self, _, mock_get_datastore):
        mock_collection = MagicMock(spec=Collection)
        mock_collection.search.return_value = [
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301121500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301120000.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301114500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301113000.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301111500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301110000.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301104500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301103000.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301101500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301100000.000000000Z-NA",
        ]
        mock_DataStore = MagicMock(spec=eumdac.DataStore)
        mock_DataStore.get_collection.return_value = mock_collection
        mock_get_datastore.return_value = mock_DataStore
        command_line = [
            "search",
            "-s",
            "2020-03-01",
            "-e",
            "2020-03-01T12:15",
            "-c",
            "EO:EUM:DAT:MSG:CLM",
            "--limit",
            "3",
        ]
        expected_lines = [
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301121500.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301120000.000000000Z-NA",
            "MSG4-SEVI-MSGCLMK-0100-0100-20200301114500.000000000Z-NA",
            "",
        ]
        expected_output = "\n".join(expected_lines)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("eumdac.cli_helpers.get_datastore")
    @patch("eumdac.cli_helpers.load_credentials")
    def test_search_bbox(self, _, mock_get_datastore):
        mock_collection = MagicMock(spec=Collection)
        mock_collection.search.return_value = [
            "MockProduct-a",
            "MockProduct-b",
            "MockProduct-c",
            "MockProduct-d",
        ]
        mock_DataStore = MagicMock(spec=eumdac.DataStore)
        mock_DataStore.get_collection.return_value = mock_collection
        mock_get_datastore.return_value = mock_DataStore

        command_line = [
            "search",
            "-c",
            "MockCollection",
            "--bbox",
            "2.0",
            "10.0",
            "10.0",
            "52.0",
            "--limit",
            "3",
        ]
        self.cli(command_line)
        print(mock_collection.call_count)
        mock_collection.search.assert_called_with(bbox="2.0,10.0,10.0,52.0", set="brief")

    @patch("eumdac.cli_helpers.load_credentials")
    def test_local_tailor_set(self, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        tailor_url = "http://NON_EXISTANT:40000"
        tailor_id = "local"

        def mock_get_url_path():
            return self.tmp_path

        self.monkeypatch.setattr("eumdac.local_tailor.get_url_path", mock_get_url_path)
        command_line = ["local-tailor", "set", tailor_id, tailor_url]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)

        command_line = ["local-tailor", "remove", tailor_id]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)

    @patch("eumdac.cli_helpers.load_credentials")
    def test_local_tailor_instances(self, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        tailor_url = "http://NON_EXISTANT:40000"
        tailor_id = "local"

        def mock_get_url_path():
            return self.tmp_path

        self.monkeypatch.setattr("eumdac.local_tailor.get_url_path", mock_get_url_path)

        command_line = ["local-tailor", "set", tailor_id, tailor_url]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)

        command_line = ["local-tailor", "instances"]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), f".*{tailor_url}.*")
            self.assertRegex(mock_stdout.getvalue(), f".*{tailor_id}.*")
            self.assertRegex(mock_stdout.getvalue(), f".*OFFLINE.*")

        command_line = ["local-tailor", "remove", tailor_id]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)

    @patch("eumdac.cli_helpers.load_credentials")
    def test_local_tailor_show(self, mock_load_credentials):
        mock_load_credentials.return_value = self.credentials
        tailor_url = "http://NON_EXISTANT:40000"
        tailor_id = "local"

        def mock_get_url_path():
            return self.tmp_path

        self.monkeypatch.setattr("eumdac.local_tailor.get_url_path", mock_get_url_path)

        command_line = ["local-tailor", "set", tailor_id, tailor_url]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)

        command_line = ["local-tailor", "show", tailor_id]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
            self.assertRegex(mock_stdout.getvalue(), f".*{tailor_url}.*")
            self.assertRegex(mock_stdout.getvalue(), f".*{tailor_id}.*")
            self.assertRegex(mock_stdout.getvalue(), f".*OFFLINE.*")

        command_line = ["local-tailor", "remove", tailor_id]
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.cli(command_line)
