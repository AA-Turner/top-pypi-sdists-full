import fnmatch
import os
import tarfile
import zipfile
from io import BytesIO
from typing import Optional, Set, Tuple

import click
from tabulate import tabulate

from ...utils.launchable_client import LaunchableClient
from ..helper import require_session


class AttachmentStatus:
    SUCCESS = "✓ Recorded successfully"
    FAILED = "⚠ Failed to record"
    SKIPPED_NON_TEXT = "⚠ Skipped: not a valid text file"
    SKIPPED_DUPLICATE = "⚠ Skipped: duplicate"


@click.command()
@click.option(
    '--session',
    'session',
    help='In the format builds/<build-name>/test_sessions/<test-session-id>',
    type=str,
)
@click.option(
    '--include',
    'include_patterns',
    help='Include only files matching pattern (e.g., "*.log"). Can be specified multiple times.',
    type=str,
    multiple=True,
)
@click.argument('attachments', nargs=-1)  # type=click.Path(exists=True)
@click.pass_context
def attachment(
        context: click.core.Context,
        attachments,
        session: Optional[str] = None,
        include_patterns: Tuple[str, ...] = ()
):
    client = LaunchableClient(app=context.obj)
    summary_rows = []
    used_filenames: Set[str] = set()

    try:
        session = require_session(session)
        assert session is not None

        for a in attachments:
            # If zip file
            if zipfile.is_zipfile(a):
                with zipfile.ZipFile(a, 'r') as zip_file:
                    for zip_info in zip_file.infolist():
                        if zip_info.is_dir():
                            continue

                        if not matches_include_patterns(zip_info.filename, include_patterns):
                            continue

                        file_content = zip_file.read(zip_info.filename)

                        if not valid_utf8_file(file_content):
                            summary_rows.append(
                                [zip_info.filename, AttachmentStatus.SKIPPED_NON_TEXT])
                            continue

                        file_name = get_unique_filename(zip_info.filename, used_filenames)
                        if not file_name:
                            summary_rows.append(
                                [zip_info.filename, AttachmentStatus.SKIPPED_DUPLICATE])
                            continue

                        status = post_attachment(
                            client, session, file_content, file_name)
                        summary_rows.append([file_name, status])

            # If tar file (tar, tar.gz, tar.bz2, tgz, etc.)
            elif tarfile.is_tarfile(a):
                with tarfile.open(a, 'r:*') as tar_file:
                    for tar_info in tar_file:
                        if tar_info.isdir():
                            continue

                        if not matches_include_patterns(tar_info.name, include_patterns):
                            continue

                        file_obj = tar_file.extractfile(tar_info)
                        if file_obj is None:
                            continue

                        file_content = file_obj.read()

                        if not valid_utf8_file(file_content):
                            summary_rows.append(
                                [tar_info.name, AttachmentStatus.SKIPPED_NON_TEXT])
                            continue

                        file_name = get_unique_filename(tar_info.name, used_filenames)
                        if not file_name:
                            summary_rows.append(
                                [tar_info.name, AttachmentStatus.SKIPPED_DUPLICATE])
                            continue

                        status = post_attachment(
                            client, session, file_content, file_name)
                        summary_rows.append([file_name, status])

            else:
                with open(a, mode='rb') as f:
                    file_content = f.read()

                    if not valid_utf8_file(file_content):
                        summary_rows.append(
                            [a, AttachmentStatus.SKIPPED_NON_TEXT])
                        continue

                    file_name = get_unique_filename(a, used_filenames)
                    if not file_name:
                        summary_rows.append(
                            [a, AttachmentStatus.SKIPPED_DUPLICATE])
                        continue

                    status = post_attachment(client, session, file_content, file_name)
                    summary_rows.append([file_name, status])

    except Exception as e:
        client.print_exception_and_recover(e)

    display_summary_as_table(summary_rows)


def get_unique_filename(filepath: str, used_filenames: Set[str]) -> Optional[str]:
    """
    Get a unique filename by extracting the basename and prepending parent folders if needed.
    Strategy:
    1. First occurrence: use basename (e.g., app.log)
    2. Duplicate: prepend parent directories until unique
    """
    # Normalize path separators to forward slash (archives always use forward slash in both linux, and windows)
    normalized_path = filepath.replace(os.sep, '/')
    normalized_path = normalize_filename(normalized_path)

    basename = normalized_path.split('/')[-1]

    # If basename is not used, return it
    if basename not in used_filenames:
        used_filenames.add(basename)
        return basename

    # Try prepending parents from nearest to farthest
    path_parts = normalized_path.split('/')
    parent_parts = [p for p in path_parts[:-1] if p]

    prefixed_name = basename
    for parent in reversed(parent_parts):
        prefixed_name = f"{parent}/{prefixed_name}"

        if prefixed_name not in used_filenames:
            used_filenames.add(prefixed_name)
            return prefixed_name

    return None


def matches_include_patterns(filename: str, include_patterns: Tuple[str, ...]) -> bool:
    """
    Check if a file should be included based on the include patterns.
    If no patterns are specified, all files are included.
    """
    if not include_patterns:
        return True

    for pattern in include_patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True

    return False


def normalize_filename(filename: str) -> str:
    """
    Normalize filename by replacing whitespace with dashes.
    """
    return filename.replace(' ', '-')


def valid_utf8_file(file_content: bytes) -> bool:
    # Check for null bytes (binary files)
    if b'\x00' in file_content:
        return False

    try:
        file_content.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def post_attachment(client: LaunchableClient, session: str, file_content: bytes, filename: str) -> str:
    try:
        res = client.request(
            "post", "{}/attachment".format(session), compress=True, payload=BytesIO(file_content),
            additional_headers={"Content-Disposition": "attachment;filename=\"{}\"".format(filename)})
        res.raise_for_status()
        return AttachmentStatus.SUCCESS
    except Exception as e:
        click.echo("Failed to upload {}: {}".format(
            filename, str(e)), err=True)
        return AttachmentStatus.FAILED


def display_summary_as_table(rows):
    headers = ["File", "Status"]
    click.echo(tabulate(rows, headers, tablefmt="github"))
