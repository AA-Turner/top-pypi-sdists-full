import tarfile
import zipfile
from io import BytesIO
from typing import Optional

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
@click.argument('attachments', nargs=-1)  # type=click.Path(exists=True)
@click.pass_context
def attachment(
        context: click.core.Context,
        attachments,
        session: Optional[str] = None
):
    client = LaunchableClient(app=context.obj)
    summary_rows = []
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

                        file_content = zip_file.read(zip_info.filename)

                        if not valid_utf8_file(file_content):
                            summary_rows.append(
                                [zip_info.filename, AttachmentStatus.SKIPPED_NON_TEXT])
                            continue

                        status = post_attachment(
                            client, session, file_content, zip_info.filename)
                        summary_rows.append([zip_info.filename, status])

            # If tar file (tar, tar.gz, tar.bz2, tgz, etc.)
            elif tarfile.is_tarfile(a):
                with tarfile.open(a, 'r:*') as tar_file:
                    for tar_info in tar_file:
                        if tar_info.isdir():
                            continue

                        file_obj = tar_file.extractfile(tar_info)
                        if file_obj is None:
                            continue

                        file_content = file_obj.read()

                        if not valid_utf8_file(file_content):
                            summary_rows.append(
                                [tar_info.name, AttachmentStatus.SKIPPED_NON_TEXT])
                            continue

                        status = post_attachment(
                            client, session, file_content, tar_info.name)
                        summary_rows.append([tar_info.name, status])

            else:
                with open(a, mode='rb') as f:
                    file_content = f.read()

                    if not valid_utf8_file(file_content):
                        summary_rows.append(
                            [a, AttachmentStatus.SKIPPED_NON_TEXT])
                        continue

                    status = post_attachment(client, session, file_content, a)
                    summary_rows.append([a, status])

    except Exception as e:
        client.print_exception_and_recover(e)

    display_summary_as_table(summary_rows)


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
