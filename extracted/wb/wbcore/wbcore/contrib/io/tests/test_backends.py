from unittest.mock import patch

import pytest
from anymail.inbound import AnymailInboundMessage
from anymail.signals import AnymailInboundEvent, EventType, inbound
from django.utils import timezone
from faker import Faker

from ..models import Source
from .test_models import get_byte_stream

fake = Faker()


def conn(sftpsrv):
    """return a dictionary holding argument info for the sftp client"""
    return {
        "host": sftpsrv.host,
        "port": sftpsrv.port,
        "username": "user",
        "password": "pw",
        "default_path": "/home/test",
    }


# filesystem served by pytest-sftpserver plugin
VFS = {
    "home": {
        "test": {
            "pub": {
                "make.txt": "content of make.txt",
                "foo1.csv": "CSV Content",
                "image01.jpg": "data for image01.jpg",
            },
            "read.me": "contents of read.me",
        }
    }
}


@pytest.mark.django_db
class TestBackend:
    def test_mail_backend(self):
        from wbcore.contrib.io.import_export.backends.mail import DataBackend as MailDataBackend

        b1 = get_byte_stream()
        b2 = get_byte_stream()
        filename1 = "file_valid_12385.json"
        filename2 = "file.json"
        att1 = AnymailInboundMessage.construct_attachment(
            "application/json", b1.getvalue(), charset="utf-8", filename=filename1
        )

        att2 = AnymailInboundMessage.construct_attachment(
            "application/json", b2.getvalue(), charset="utf-8", filename=filename2
        )

        msg = AnymailInboundMessage.construct(
            from_email="from@example.com",
            to="to@example.com",
            cc="cc@example.com",
            subject="test subject",
            attachments=[att1, att2],
        )
        backend = MailDataBackend()
        res = list(backend.get_files(timezone.now(), file_name_regex="file_valid_([A-Z0-9]*).json", message=msg))
        assert len(res) == 1
        assert res[0][0] == filename1
        assert (res[0][1]).getvalue() == b1.getvalue()

    @pytest.mark.parametrize(
        "source__import_parameters,from_email",
        [
            ({"whitelisted_emails": ["test@test.ch"]}, "test@test.ch"),
            ({"whitelisted_emails": ["test@test.ch"]}, "spam@    test.ch"),
        ],
    )
    @patch.object(Source, "trigger_workflow")
    def test_inbound_mail(self, mock_process_source, source, from_email):
        from wbcore.contrib.io.models import DataBackend

        data_backend = DataBackend.objects.get(title="Default Mail")

        assert data_backend.backend_class_path == "wbcore.contrib.io.import_export.backends.mail"

        source.data_backend = data_backend
        source.save()
        message = AnymailInboundMessage.construct(
            from_email=from_email,
            to="to@example.com",
            subject=fake.paragraph(),
            text=fake.paragraph(),
            html=f"<p>{fake.paragraph()}</p>",
        )
        event = AnymailInboundEvent(
            event_type=EventType.INBOUND,
            timestamp=None,
            event_id=fake.uuid4(),
            esp_event={"from_email": from_email},
            message=message,
        )
        inbound.send(sender="TEST", event=event, esp_name="test")
        if source.import_parameters.get("whitelisted_emails", [None])[0] == from_email:
            assert mock_process_source.call_count == 1
        else:
            assert mock_process_source.call_count == 0

    def test_sftp_backend_without_credential(self):
        from wbcore.contrib.io.import_export.backends.sftp import DataBackend as SFTPDataBackend

        with pytest.raises(ValueError):
            SFTPDataBackend()

    def test_sftp_backend(self, sftpserver, import_credential_factory):
        from wbcore.contrib.io.import_export.backends.sftp import DataBackend as SFTPDataBackend

        with sftpserver.serve_content(VFS):
            import_credential = import_credential_factory.create(
                username="user",
                password="password",  # noqa
                additional_resources={
                    "host": sftpserver.host,
                    "port": sftpserver.port,
                },
            )
            copied_file_content = VFS["home"]["test"]["pub"]["foo1.csv"]
            backend = SFTPDataBackend(import_credential=import_credential)
            res = list(
                backend.get_files(timezone.now(), "/home/test/pub", file_name_regex=r".+\.csv$", cleanup_files=True)
            )

            assert len(res) == 1
            assert res[0][0] == "foo1.csv"
            assert (res[0][1]).getvalue().decode("utf-8") == copied_file_content
