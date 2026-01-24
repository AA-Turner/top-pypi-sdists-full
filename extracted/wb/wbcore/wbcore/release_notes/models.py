from django.db import models
from django.utils.translation import gettext_lazy as _

from wbcore.contrib.authentication.models.users import User
from wbcore.release_notes.utils import parse_release_note


class ReleaseNote(models.Model):
    """
    This model holds all relevant information about a new release. Instances of this model will never be created
    manually, but always through a management command that manages them from markdown files. Those markdown files
    sit in a dedicated folder called `release_notes`. There are two exceptions for this:
    - The release notes of wbcore: `wbcore/release_notes/release_notes`
    - The release notes of the frontend: `wbcore/release_notes/frontend_release_notes`

    The markdown files have to abide by a certain format, which includes metadata from which all fields are filled.
    The markdown content is parsed through python-markdown and is saved as html. With every deployment, the
    management command `handle_release_notes` is called.
    """

    version = models.CharField(max_length=18, help_text=_("The version/identifier of the release"))
    release_date = models.DateField(help_text=_("The date when this new version was released"))
    module = models.CharField(max_length=255, help_text=_("The workbench module of the release"))
    summary = models.CharField(max_length=512, help_text=_("A brief summary of the release"))
    notes = models.TextField(default="", help_text=_("What's new? What's improved? What's fixed?"))
    read_by = models.ManyToManyField(to=User, related_name="read_patch_notes", db_table="bridger_releasenote_read_by")

    @classmethod
    def handle_from_markdown(cls, markdown_content: str) -> "ReleaseNote":
        content, meta, version, module, summary, release_date = parse_release_note(markdown_content)

        try:
            release_note = cls.objects.get(version=version, module=module)
            release_note.summary = summary
            release_note.release_date = release_date
            release_note.notes = content
            release_note.save()
        except cls.DoesNotExist:
            release_note = cls.objects.create(
                version=version,
                module=module,
                release_date=release_date,
                summary=summary,
                notes=content,
            )

        return release_note

    def __str__(self) -> str:
        return f"{self.module}: {self.version}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:releasenote"

    class Meta:
        verbose_name = _("Release Note")
        verbose_name_plural = _("Release Notes")

        constraints = [
            models.UniqueConstraint(fields=["version", "module"], name="release_note_unique_version_module")
        ]

        db_table = "bridger_releasenote"
