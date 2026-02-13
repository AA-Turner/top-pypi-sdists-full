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

                        file_name = normalize_filename(zip_info.filename)
                        file_name = get_unique_filename(file_name, used_filenames)
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

                        file_name = normalize_filename(tar_info.name)
                        file_name = get_unique_filename(file_name, used_filenames)
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

                    file_name = normalize_filename(a)
                    file_name = get_unique_filename(file_name, used_filenames)
                    status = post_attachment(client, session, file_content, file_name)
                    summary_rows.append([file_name, status])

    except Exception as e:
        client.print_exception_and_recover(e)

    display_summary_as_table(summary_rows)


def get_unique_filename(filepath: str, used_filenames: Set[str]) -> str:
    """
    Get a unique filename by extracting the basename and prepending parent folder if needed.
    Strategy:
    1. First occurrence: use basename (e.g., app.log)
    2. Duplicate: prepend parent folder (e.g., nested-app.log)
    3. Still duplicate: append .1, .2, etc. (e.g., nested-app.1.log)
    """
    filename = os.path.basename(filepath)

    # If basename is not used, return it
    if filename not in used_filenames:
        used_filenames.add(filename)
        return filename

    # Try prepending the parent directory name
    parent_dir = os.path.basename(os.path.dirname(filepath))
    if parent_dir:  # Has a parent directory
        name, ext = os.path.splitext(filename)
        filename = f"{parent_dir}-{name}{ext}"

        if filename not in used_filenames:
            used_filenames.add(filename)
            return filename

    # If still duplicate, append numbers
    name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        filename = f"{name}.{counter}{ext}"
        if filename not in used_filenames:
            used_filenames.add(filename)
            return filename
        counter += 1


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
