import gzip
import os
import tarfile
import tempfile
import zipfile
from unittest import mock

import responses  # type: ignore

from launchable.utils.http_client import get_base_url
from launchable.utils.session import write_session
from tests.cli_test_case import CliTestCase


class AttachmentTest(CliTestCase):
    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment(self):
        TEST_CONTENT = b"Hello world"

        # emulate launchable record build & session
        write_session(self.build_name, self.session_id)

        attachment = tempfile.NamedTemporaryFile(delete=False)
        attachment.write(TEST_CONTENT)
        attachment.close()

        # gimick to capture the payload sent to the server, while the request is in flight
        # the body is a generator, so unless it's consumed within the request, we won't be able to access it
        body = None

        def verify_body(request):
            nonlocal body
            body = gzip.decompress(b''.join(list(request.body)))  # request.body is a generator
            return (200, [], None)

        responses.add_callback(
            responses.POST,
            "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
            callback=verify_body)

        result = self.cli("record", "attachment", "--session", self.session, attachment.name)

        self.assert_success(result)
        self.assertEqual(TEST_CONTENT, body)

        os.unlink(attachment.name)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment_zip_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary files
            text_file_1 = os.path.join(temp_dir, "app.log")
            text_file_2 = os.path.join(temp_dir, "nested", "debug.log")
            binary_file = os.path.join(temp_dir, "binary.dat")
            zip_path = os.path.join(temp_dir, "logs.zip")
            tar_path = os.path.join(temp_dir, "logs.tar.gz")

            # Create directory structure
            os.makedirs(os.path.dirname(text_file_2))

            # Write test content
            with open(text_file_1, 'w') as f:
                f.write("[INFO] Test log entry")
            with open(text_file_2, 'w') as f:
                f.write("[DEBUG] Nested log entry")
            with open(binary_file, 'wb') as f:
                f.write(b'\x00\x01\x02\x03')

            # Create zip file
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(text_file_1, 'app.log')
                zf.write(text_file_2, 'nested/debug.log')
                zf.write(binary_file, 'binary.dat')

            # Create tar.gz file
            with tarfile.open(tar_path, 'w:gz') as tf:
                tf.add(text_file_1, 'app.log')
                tf.add(text_file_2, 'nested/debug.log')
                tf.add(binary_file, 'binary.dat')

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="app.log"'})],
                json={"error": "Log file of the same name already exists"},
                status=400)

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="debug.log"'})],
                status=200)

            expect = """
| File       | Status                           |
|------------|----------------------------------|
| app.log    | ⚠ Failed to record               |
| debug.log  | ✓ Recorded successfully          |
| binary.dat | ⚠ Skipped: not a valid text file |
"""

            result = self.cli("record", "attachment", "--session", self.session, zip_path)

            self.assertIn(expect, result.output)

            result = self.cli("record", "attachment", "--session", self.session, tar_path)

            self.assertIn(expect, result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment_with_include_filter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary files
            text_file_1 = os.path.join(temp_dir, "app.log")
            text_file_2 = os.path.join(temp_dir, "nested", "debug.log")
            text_file_3 = os.path.join(temp_dir, "config.yml")
            zip_path = os.path.join(temp_dir, "logs.zip")

            # Create directory structure
            os.makedirs(os.path.dirname(text_file_2))

            # Write test content
            with open(text_file_1, 'w') as f:
                f.write("[INFO] Test log entry")
            with open(text_file_2, 'w') as f:
                f.write("[DEBUG] Nested log entry")
            with open(text_file_3, 'w') as f:
                f.write("config: value")

            # Create zip file
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(text_file_1, 'app.log')
                zf.write(text_file_2, 'nested/debug.log')
                zf.write(text_file_3, 'config.yml')

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="app.log"'})],
                status=200)

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="debug.log"'})],
                status=200)

            result = self.cli("record", "attachment", "--session", self.session, "--include", "*.log", zip_path)

            expect = """| File      | Status                  |
|-----------|-------------------------|
| app.log   | ✓ Recorded successfully |
| debug.log | ✓ Recorded successfully |
"""
            self.assertEqual(expect, result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment_with_identical_file_names(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary files
            text_file_1 = os.path.join(temp_dir, "app.log")
            text_file_2 = os.path.join(temp_dir, "nested_2", "app.log")
            zip_path = os.path.join(temp_dir, "logs.zip")

            # Create directory structure
            os.makedirs(os.path.dirname(text_file_2))

            # Write test content
            with open(text_file_1, 'w') as f:
                f.write("[INFO] Test log entry")
            with open(text_file_2, 'w') as f:
                f.write("[DEBUG] Nested log entry")

            # Create zip file
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(text_file_1, 'app.log')
                zf.write(text_file_2, 'nested_1/app.log')
                zf.write(text_file_2, 'nested_2/app.log')

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="app.log"'})],
                status=200)

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="nested_1/app.log"'})],
                status=200)

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="nested_2/app.log"'})],
                status=200)

            result = self.cli("record", "attachment", "--session", self.session, zip_path)

            expect = """| File             | Status                  |
|------------------|-------------------------|
| app.log          | ✓ Recorded successfully |
| nested_1/app.log | ✓ Recorded successfully |
| nested_2/app.log | ✓ Recorded successfully |
"""
            self.assertEqual(expect, result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment_with_whitespace_in_filename(self):
        TEST_CONTENT = b"Test log content"

        # emulate launchable record build & session
        write_session(self.build_name, self.session_id)

        # Create a file with whitespace in the name
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "app log file.txt")
            with open(file_path, 'wb') as f:
                f.write(TEST_CONTENT)

            # Expect the filename with whitespace replaced by dashes in the Content-Disposition header
            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher(
                    {"Content-Disposition": 'attachment;filename="{}"'.format("app-log-file.txt")}
                )],
                status=200)

            result = self.cli("record", "attachment", "--session", self.session, file_path)

            self.assert_success(result)
            self.assertIn("✓ Recorded successfully", result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_attachment_duplicate_file_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary files
            text_file_1 = os.path.join(temp_dir, "app.log")
            zip_path = os.path.join(temp_dir, "logs.zip")

            # Write test content
            with open(text_file_1, 'w') as f:
                f.write("[INFO] Test log entry")

            # Create zip file
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(text_file_1, 'app.log')

            responses.add(
                responses.POST,
                "{}/intake/organizations/{}/workspaces/{}/builds/{}/test_sessions/{}/attachment".format(
                    get_base_url(), self.organization, self.workspace, self.build_name, self.session_id),
                match=[responses.matchers.header_matcher({"Content-Disposition": 'attachment;filename="app.log"'})],
                status=200)

            expect = """| File    | Status                  |
|---------|-------------------------|
| app.log | ✓ Recorded successfully |
| app.log | ⚠ Skipped: duplicate    |
"""

            result = self.cli("record", "attachment", "--session", self.session, zip_path, zip_path)

            self.assertIn(expect, result.output)
