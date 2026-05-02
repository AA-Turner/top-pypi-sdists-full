from email.parser import Parser
from email.policy import default
import magic


class MailMessage:
    """docstring for MailMessage"""

    content_type = None

    def __init__(
        self, directory: str, raw: str, flags=None, validate_mime: bool = False
    ):
        msg = Parser(policy=default).parsestr(raw)
        self._mime = magic.Magic(mime=True)
        self._validate_mime = validate_mime
        self.content = None
        self.raw = raw
        self.subject = msg["subject"]
        self.email_from = msg["from"]
        self.email_to = msg["to"]
        self.body = msg.get_body()
        self.directory = directory
        self.flags = flags
        self.attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == "text" and "attachment" not in part.get(
                "Content-Disposition", ""
            ):
                self.content = (
                    part.get_payload(decode=True)
                    .decode(part.get_param("charset", "ascii"))
                    .strip()
                )
            if part.get_filename() is not None:
                mime_type = part.get_content_type()
                if mime_type == "application/octet-stream":
                    if self._validate_mime is True:
                        mime_type = self._mime.from_buffer(
                            part.get_payload(decode=True)
                        )
                self.attachments.append(
                    {
                        "filename": part.get_filename(),
                        "content_type": mime_type,
                        "type": part.get_content_maintype(),
                        "Content-Disposition": part.get("Content-Disposition"),
                        "attachment": part.get_payload(decode=True),
                        "size": len(part.as_bytes()),
                    }
                )

    def getSubject(self):
        return self.subject

    def __str__(self) -> str:
        return f"<MailMessage:>Subject: {self.subject}, From: {self.email_from}, To: {self.email_to}"

    def get_attachments(self):
        return self.attachments

    def get_attachments_names(self):
        return [at["filename"] for at in self.attachments]
