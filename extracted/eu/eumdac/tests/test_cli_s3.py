import io
import unittest
import re
import os
import datetime
import sys

from datetime import datetime, timedelta
from typing import Dict

from unittest.mock import patch, mock_open, MagicMock

import eumdac
from eumdac.cli import cli
from eumdac.collection import Collection

from .base import INTEGRATION_TESTING, CONSUMER_KEY, CONSUMER_SECRET


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

    # @unittest.skipIf(not INTEGRATION_TESTING, "To be tested only on integration testing phase")
    @unittest.skip("Skipping for integration testing temporarily")
    def test_search_timeliness(self):
        aweekago = datetime.now() - timedelta(days=7)
        start = aweekago.strftime("%Y-%m-%d")
        end = aweekago.strftime("%Y-%m-%dT03")
        command_line = [
            "search",
            "-c",
            "EO:EUM:DAT:0409",
            "-s",
            start,
            "-e",
            end,
            "--limit",
            "3",
        ]
        with patch.object(eumdac.cli, "load_credentials") as mock_load_credentials:
            mock_load_credentials.return_value = (CONSUMER_KEY, CONSUMER_SECRET)
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                cli(command_line + ["--timeliness", "NR"])
                self.assertRegex(
                    mock_stdout.getvalue(),
                    "(.*?_NR_.*?(\r)?\n){3}",
                    "Expected NR products were not received",
                )
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                cli(command_line + ["--timeliness", "NT"])
                self.assertRegex(
                    mock_stdout.getvalue(),
                    "(.*?_NT_.*?(\r)?\n){3}",
                    "Expected NT products were not received",
                )

    # @unittest.skipIf(not INTEGRATION_TESTING, "To be tested only on integration testing phase")
    @unittest.skip("Skipping for integration testing temporarily")
    def test_search_orbit_number(self):
        command_line = [
            "search",
            "-c",
            "EO:EUM:DAT:0409",
            "-s",
            "2022-07-01",
            "-e",
            "2022-07-01T03",
            "--limit",
            "100",
        ]
        num_full_query_output_lines: int = 0
        with patch.object(eumdac.cli, "load_credentials") as mock_load_credentials:
            mock_load_credentials.return_value = (CONSUMER_KEY, CONSUMER_SECRET)
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                cli(command_line)
                output = mock_stdout.getvalue()
                self.assertRegex(output, "(.*?.SEN3(\r)?\n)+", "Products not received")
                num_full_query_output_lines = len(output.split("\n"))

            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                cli(command_line + ["--orbit", "33172"])
                output = mock_stdout.getvalue()
                self.assertRegex(output, "(.*?.SEN3(\r)?\n)+", "Products not received")
                self.assertGreater(num_full_query_output_lines, len(output.split("\n")))

    @unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
    @patch("eumdac.cli_helpers.get_datastore")
    @patch("eumdac.cli_helpers.load_credentials")
    def test_sen3_search_params(self, _, mock_get_datastore):
        mock_DataStore = MagicMock(spec=eumdac.DataStore)
        mock_get_datastore.return_value = mock_DataStore

        mock_collection = MagicMock(spec=Collection)
        mock_collection.search.return_value = []
        mock_DataStore.get_collection.return_value = mock_collection
        command_line = [
            "search",
            "-s",
            "2020-03-01",
            "-e",
            "2020-03-01T12:15",
            "-c",
            "EO:EUM:DAT:0409",
            "--limit",
            "3",
            "--timeliness",
            "NR",
            "--orbit",
            "20",
            "--relorbit",
            "2120",
            "--cycle",
            "13",
            "--filename",
            "*file*expr*.SEN3",
        ]

        cli(command_line)

        search_kwargs = mock_collection.search.call_args[1]
        self.assertTrue(search_kwargs.get("orbit") == 20, "Unexpected orbit value")
        self.assertTrue(search_kwargs.get("relorbit") == 2120, "Unexpected relorbit value")
        self.assertTrue(search_kwargs.get("timeliness") == "NR", "Unexpected timeliness value")
        self.assertTrue(search_kwargs.get("cycle") == 13, "Unexpected cycle value")
        self.assertTrue(
            search_kwargs.get("title") == "*file*expr*.SEN3", "Unexpected filename value"
        )
