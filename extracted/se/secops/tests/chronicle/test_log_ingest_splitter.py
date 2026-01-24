# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Tests for the log splitter functionality in log_ingest.py."""

import unittest
import json

from secops.chronicle import log_ingest


class TestLogSplitterRegistration(unittest.TestCase):
    """Test the log splitter registration and mapping functionality."""

    def test_splitter_registration(self):
        """Test that splitters are correctly registered for multi-line formats."""
        # Initialize the multi-line formats first
        log_ingest.initialize_multi_line_formats()

        # Directly check internal dictionary for registered multi-line format splitters
        self.assertIn("JSON", log_ingest._LOG_SPLITTERS)
        self.assertIn("WINDOWS", log_ingest._LOG_SPLITTERS)
        self.assertIn("XML", log_ingest._LOG_SPLITTERS)

    def test_alias_mapping(self):
        """Test that log type aliases are correctly mapped for multi-line formats."""
        # Initialize the multi-line formats first
        log_ingest.initialize_multi_line_formats()

        # Verify that alias mapping correctly maps to multi-line base formats
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["JSON"], "JSON")
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["WINDOWS"], "WINDOWS")
        self.assertEqual(
            log_ingest._LOG_TYPE_ALIASES["WINDOWS_SECURITY"], "WINDOWS"
        )
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["WINEVTLOG"], "WINDOWS")
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["XML"], "XML")
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["WINEVTLOG_XML"], "XML")

        # Check that SYSLOG and other non-multiline formats are not in the mapping
        self.assertNotIn("SYSLOG", log_ingest._LOG_TYPE_ALIASES)

    def test_lazy_initialization(self):
        """Test that the multi-line formats are lazily initialized."""
        # Clear existing aliases to simulate fresh module load
        log_ingest._LOG_TYPE_ALIASES.clear()
        self.assertEqual(len(log_ingest._LOG_TYPE_ALIASES), 0)

        # Initialize the multi-line formats
        log_ingest.initialize_multi_line_formats()

        # Verify that aliases are now populated
        self.assertGreater(len(log_ingest._LOG_TYPE_ALIASES), 0)
        self.assertIn("WINDOWS", log_ingest._LOG_TYPE_ALIASES)
        self.assertIn("XML", log_ingest._LOG_TYPE_ALIASES)
        self.assertIn("JSON", log_ingest._LOG_TYPE_ALIASES)


class TestLogSplitters(unittest.TestCase):
    """Test the individual log splitter functions for multi-line formats."""

    def test_json_splitter(self):
        """Test JSON log splitter with various JSON formats."""
        # Single JSON object
        single_json = '{"timestamp": "2023-01-23T12:34:56Z", "message": "test"}'
        result = log_ingest.split_json_logs(single_json)
        self.assertEqual(len(result), 1)
        self.assertEqual(json.loads(result[0])["message"], "test")

        # JSON array
        json_array = '[{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]'
        result = log_ingest.split_json_logs(json_array)
        self.assertEqual(len(result), 2)

        # JSON Lines (multiple objects, one per line)
        json_lines = '{"id": 1}\n{"id": 2}\n{"id": 3}'
        result = log_ingest.split_json_logs(json_lines)
        self.assertEqual(len(result), 3)

    def test_windows_splitter(self):
        """Test Windows log splitter."""
        # Test multi-event Windows logs with proper header separation
        windows_logs = """Log Name:      Security
Source:        Microsoft-Windows-Security-Auditing
Event ID:      4624

Log Name:      System
Source:        Microsoft-Windows-Kernel-Power
Event ID:      41
"""
        result = log_ingest.split_windows_logs(windows_logs)
        self.assertEqual(len(result), 2)
        self.assertIn("Security", result[0])
        self.assertIn("System", result[1])

    def test_windows_splitter_single_event(self):
        """Test Windows log splitter with a single event."""
        # Test single event Windows log format
        windows_logs = """Log Name:      Security
Source:        Microsoft-Windows-Security-Auditing
Event ID:      4624
Details:       User logon successful
"""
        result = log_ingest.split_windows_logs(windows_logs)
        self.assertEqual(len(result), 1)
        self.assertIn("Security", result[0])

    def test_xml_splitter(self):
        """Test XML log splitter."""
        # Create properly formatted XML content
        xml_logs = """<?xml version="1.0"?><event id="1"><data>test1</data></event><?xml version="1.0"?><event id="2"><data>test2</data></event>"""
        result = log_ingest.split_xml_logs(xml_logs)
        self.assertEqual(len(result), 2)
        self.assertIn('id="1"', result[0])
        self.assertIn('id="2"', result[1])

    def test_default_line_splitting(self):
        """Test that non-multi-line formats are split by newlines."""
        # Test with syslog format (should use default newline splitting)
        syslog_content = """
        Jan 23 14:25:26 server1 sshd[1234]: Failed password for invalid user
        Jan 23 14:26:01 server1 sshd[1235]: Accepted password for user1
        """
        result = log_ingest.split_logs("SYSLOG", syslog_content)
        self.assertEqual(len(result), 2)
        self.assertIn("Failed password", result[0])
        self.assertIn("Accepted password", result[1])

        # Test with CEF format (should use default newline splitting)
        cef_logs = """
        CEF:0|Vendor|Product|1.0|100|User Login|Low|src=192.168.1.1
        CEF:0|Vendor|Product|1.0|101|User Logout|Low|src=192.168.1.1
        """
        result = log_ingest.split_logs("CEF", cef_logs)
        self.assertEqual(len(result), 2)
        self.assertIn("User Login", result[0])
        self.assertIn("User Logout", result[1])


class TestSplitLogs(unittest.TestCase):
    """Test the split_logs function that routes logs to appropriate splitters."""

    def setUp(self):
        # Save original state
        self.original_splitters = log_ingest._LOG_SPLITTERS.copy()
        self.original_aliases = log_ingest._LOG_TYPE_ALIASES.copy()
        # Initialize multi-line formats for testing
        log_ingest.initialize_multi_line_formats()

    def tearDown(self):
        # Restore original state
        log_ingest._LOG_SPLITTERS = self.original_splitters.copy()
        log_ingest._LOG_TYPE_ALIASES = self.original_aliases.copy()

    def test_split_logs_with_direct_match(self):
        """Test split_logs with a direct match to a registered multi-line splitter."""
        # Use an actual multi-line format that should have a registered splitter
        windows_logs = "Log Name: Security\nEvent ID: 1234\nDetails: Test event"
        result = log_ingest.split_logs("WINDOWS", windows_logs)
        # The Windows splitter should keep this as a single event
        self.assertEqual(len(result), 1)
        self.assertIn("Security", result[0])

    def test_split_logs_with_alias(self):
        """Test split_logs with an alias that maps to a registered multi-line splitter."""
        # Use an actual alias for a multi-line format
        windows_logs = "Log Name: Security\nEvent ID: 1234\nDetails: Test event"
        result = log_ingest.split_logs("WINDOWS_SECURITY", windows_logs)
        # The Windows splitter should keep this as a single event
        self.assertEqual(len(result), 1)
        self.assertIn("Security", result[0])

    def test_split_logs_default_splitting(self):
        """Test split_logs default line splitting for non-multi-line formats."""
        # Use a format that's not registered as multi-line
        syslog_content = (
            "Jan 23 14:25:26 server1: msg1\nJan 23 14:25:27 server1: msg2"
        )
        result = log_ingest.split_logs("SYSLOG", syslog_content)
        self.assertEqual(len(result), 2)
        self.assertIn("msg1", result[0])
        self.assertIn("msg2", result[1])

    def test_split_logs_with_unknown_type(self):
        """Test split_logs with completely unknown type uses default line splitting."""
        log_content = "line1\nline2\nline3"
        result = log_ingest.split_logs("UNKNOWN_TYPE", log_content)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ["line1", "line2", "line3"])


class TestMultiLineFormatHandling(unittest.TestCase):
    """Test the handling of multi-line log formats."""

    def setUp(self):
        # Initialize multi-line formats for testing
        log_ingest._LOG_TYPE_ALIASES.clear()  # Clear any existing aliases
        log_ingest.initialize_multi_line_formats()

    def test_multi_line_formats_initialized(self):
        """Test that multi-line formats are properly identified."""
        # Check that multi-line formats are registered in the constant
        self.assertIn("WINDOWS", log_ingest.MULTI_LINE_LOG_FORMATS)
        self.assertIn("JSON", log_ingest.MULTI_LINE_LOG_FORMATS)
        self.assertIn("XML", log_ingest.MULTI_LINE_LOG_FORMATS)

    def test_multi_line_format_aliases(self):
        """Test that aliases for multi-line formats are properly mapped."""
        # Check some key aliases
        self.assertEqual(
            log_ingest._LOG_TYPE_ALIASES["WINDOWS_SECURITY"], "WINDOWS"
        )
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["WINEVTLOG_XML"], "XML")
        self.assertEqual(log_ingest._LOG_TYPE_ALIASES["OKTA"], "JSON")

    def test_non_multi_line_formats_not_registered(self):
        """Test that non-multi-line formats are not registered as aliases."""
        self.assertNotIn("SYSLOG", log_ingest._LOG_TYPE_ALIASES)
        self.assertNotIn("CEF", log_ingest._LOG_TYPE_ALIASES)
        self.assertNotIn("CSV", log_ingest._LOG_TYPE_ALIASES)


if __name__ == "__main__":
    unittest.main()
