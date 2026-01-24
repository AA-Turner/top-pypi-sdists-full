import datetime
import json
import os
from contextlib import suppress
from datetime import timedelta
from typing import Dict, Generator, List, Optional

import magic
import reversion
from celery import shared_task
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.template.loader import get_template
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from wbcore.contrib.authentication.models import User
from wbcore.contrib.guardian.models.mixins import PermissionObjectModelMixin
from wbcore.models import WBModel
from wbcore.utils.html import convert_html2text
from wbcore.workers import Queue

from .document_model_relationships import DocumentModelRelationship
from .shareable_links import ShareableLink


def upload_to(instance: "Document", filename: str) -> str:
    """
    Return the document path based on the document type mptt tree
    Args:
        instance: A document instance
        filename: The given filename

    Returns:
        The relative document path
    """

    if instance.document_type:
        type_ancestors = instance.document_type.get_ancestors(ascending=False, include_self=True).values_list(
            "name", flat=True
        )
        base_path = "/".join(["dms/document", *[slugify(ancestor_name) for ancestor_name in type_ancestors]])
    else:
        base_path = "dms/document"
    return f"{base_path}/{filename}"


@reversion.register()
class Document(PermissionObjectModelMixin, WBModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True, verbose_name=_("Description"))
    file = models.FileField(max_length=256, upload_to=upload_to, verbose_name=_("File"))
    document_type = models.ForeignKey(
        to="documents.DocumentType",
        related_name="documents",
        on_delete=models.PROTECT,
        verbose_name=_("Document Type"),
    )
    system_created = models.BooleanField(default=False, verbose_name=_("System Created"))
    system_key = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("System Key"), unique=True)

    valid_from = models.DateField(null=True, blank=True, verbose_name=_("Valid From"))
    valid_until = models.DateField(null=True, blank=True, verbose_name=_("Valid Until"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_("Updated"))

    def __str__(self) -> str:
        return f"{self.name} ({self.document_type})"

    @cached_property
    def content_type(self) -> str:
        """
        Guess the file content type using magic library

        Returns:
            The file content type

        Raises:
            MagicException: If content type cannot be guessed
        """
        try:
            return magic.from_buffer(self.file.read(), mime=True)
        except magic.MagicException:
            return None

    @cached_property
    def filename(self) -> str:
        """
        Return the extracted filename from the relative path

        Returns:
            The filename
        """
        return os.path.basename(self.file.name)

    @property
    def linked_objects(self) -> Generator[models.Model, None, None]:
        """
        All objects that share a relationship with this document instance

        Returns:
            An generator of Object (any type)

        """
        for relation in self.relationships.all():
            with suppress(
                AttributeError
            ):  # maybe the content type doesn't exist anymore and getting content_object will then trigger an attribute error that we want to silently catch
                yield relation.content_object

    def get_permissions_for_user(self, user: "User", created: Optional[datetime.datetime] = None) -> Dict[str, bool]:
        """
        Return a generator of allowed (view|change|delete) permission and its editable state

        Args:
            user: The user to which we get permission for the given object
            created: The permission creation date. Defaults to None.

        Returns:
            A dictionary of string permission identifier, editable state key value pairs.
        """
        # We do not call super here, as we do not want that by default everyone has access to all documents
        base_permission = {}
        if not self.system_created:
            base_permission = super().get_permissions_for_user(user, created=created)

        for linked_object in self.linked_objects:
            if _callable := getattr(linked_object, "get_permissions_for_user_and_document", None):
                extra_permissions = _callable(user, self, created=created)
                for perm, editable in extra_permissions:
                    base_permission[perm] = editable
        return base_permission

    def generate_shareable_link(
        self, sharing_seconds_duration: Optional[int] = 3600, one_time_link: Optional[bool] = False
    ) -> "ShareableLink":
        """
        Generate a shareable link instance.

        Args:
            sharing_seconds_duration: The validity in second. Convert this value into a valid datetime. Defaults to 1 hour.
            one_time_link: Set to True if this link can be accessed only once. Defaults to False.

        Returns:
            The newly created shareable link instance
        """
        return ShareableLink.objects.create(
            document=self,
            valid_until=(
                timezone.now() + timedelta(seconds=sharing_seconds_duration) if sharing_seconds_duration else None
            ),
            one_time_link=one_time_link,
        )

    def link(self, obj: models.Model) -> bool:
        """
        Link a document to the passed object

        Args:
            obj: The object that is related to the document

        Returns:
            True if the relationship was created. False otherwise.
        """

        return DocumentModelRelationship.objects.update_or_create(
            document=self,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            defaults={"primary": True},
        )[0]

    def send_email(
        self,
        to_emails: List | str,
        as_link: Optional[bool] = True,
        subject: Optional[str] = None,
        from_email: Optional[str] = None,
        body: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
    ):
        """
        Send a document through the configured mailing backend

        Args:
            to_emails: A list of emails or an email address
            as_link: True if the document needs to be sent with a shareable link (Otherwise attached as file). Defaults to True.
            subject: The email subject. Defaults to None.
            from_email: The sender email address. Defaults to None.
            body: Mail Content: Defaults to None.
            cc_emails: CC addresses. Defaults to None.
            bcc_emails: BCC addresses. Defaults to None.
        """
        send_email_as_task.delay(self.id, to_emails, as_link, subject, from_email, body, cc_emails, bcc_emails)

    @classmethod
    def get_for_object(cls, obj) -> "models.QuerySet[Document]":
        """
        Returns a Queryset of document linked to the passed object

        Args:
            obj: The related object

        Returns:
            A queryset of documents
        """
        document_ids = DocumentModelRelationship.objects.filter(
            content_type=ContentType.objects.get_for_model(obj), object_id=obj.id
        ).values("document")
        return cls.objects.filter(id__in=document_ids)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:documents:document"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:documents:documentrepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{name}}"

    class Meta(PermissionObjectModelMixin.Meta):
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def send_email_as_task(
    document_id,
    to_emails: List | str,
    as_link: Optional[bool] = True,
    subject: Optional[str] = None,
    from_email: Optional[str] = None,
    body: Optional[str] = None,
    cc_emails: Optional[List[str]] = None,
    bcc_emails: Optional[List[str]] = None,
):
    """
    Send a document through the configured mailing backend

    Args:
        document_id: The ID of the document.
        to_emails: A list of emails or an email address
        as_link: True if the document needs to be sent with a shareable link (Otherwise attached as file). Defaults to True.
        subject: The email subject. Defaults to the document name.
        from_email: The sender email address. Defaults to the global preferences
        body: The mail content. Defaults to the default template.
        cc_emails:  CC addresses. Defaults to None.
        bcc_emails: BCC addresses. Defaults to None.
    """
    document = Document.objects.get(id=document_id)
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not subject:
        subject = document.name
    context = {"title": gettext("A file was shared with you")}
    if as_link:
        link = document.generate_shareable_link(sharing_seconds_duration=0).link
        context["endpoint"] = link
        context["message"] = gettext(
            """
        <p>Please find your {document_type} \"{filename}\" under this <a href={link}>link</a></p>
        """
        ).format(document_type=document.document_type, filename=document.filename, link=link)
    else:
        context["message"] = gettext(
            """
        <p>Please find the {document_type} \"{filename}\" attached to this mail.</p>
        """
        ).format(document_type=document.document_type, filename=document.filename)
    if body:
        html_content = Template(body).render(Context(context))
    else:
        template = get_template(settings.WBCORE_NOTIFICATION_TEMPLATE)
        html_content = template.render(context)

    if not isinstance(to_emails, list):
        to_emails = [to_emails]

    msg = EmailMultiAlternatives(
        strip_tags(subject),
        body=convert_html2text(html_content),
        to=to_emails,
        from_email=from_email,
        cc=cc_emails,
        bcc=bcc_emails,
    )
    msg.attach_alternative(html_content, "text/html")

    if not as_link:
        alternative_dict = {"id": document.id, "filename": document.filename}
        msg.attach_alternative(
            json.dumps(alternative_dict).encode("ascii"), "wbdms/document"
        )  # leave this mimetype. Used by wbmailing
        msg.attach(document.filename, document.file.read())
    msg.send()
