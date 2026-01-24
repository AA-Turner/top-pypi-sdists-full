import importlib
import io
import json
import logging
import os
import sys
import traceback
import uuid
from contextlib import suppress
from copy import deepcopy
from datetime import datetime
from importlib import import_module
from typing import Any, Callable, Dict, Optional

import magic
from celery import chain, shared_task
from croniter import croniter
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import post_delete, pre_delete
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask, cronexp
from import_export.resources import Resource
from picklefield.fields import PickledObjectField
from tablib import Dataset
from tqdm import tqdm

from wbcore.contrib.notifications.dispatch import send_notification
from wbcore.contrib.notifications.utils import create_notification_type
from wbcore.utils.models import ComplexToStringMixin

from ...workers import Queue
from .enums import ExportFormat, get_django_import_export_format
from .signals import post_import

logger = logging.getLogger("io")


class ParserHandler(models.Model):
    class MimeTypeChoices(models.TextChoices):
        CSV = "text/csv", "CSV"
        JSON = "application/json", "JSON"
        XLS = "application/vnd.ms-excel", "XLS"
        XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "XLSX"

    parser = models.CharField(max_length=255)
    handler = models.CharField(max_length=255)

    allow_file_type = models.CharField(max_length=68, blank=True, null=True, choices=MimeTypeChoices.choices)

    def __str__(self) -> str:
        return f"{self.parser}::{self.handler}"

    @cached_property
    def model(self):
        return apps.get_model(self.handler)

    def parse(self, import_source: "ImportSource") -> Dict[str, Any]:
        """
        call the parser on the provided data
        Args:
            import_source: The import source containing the data
        Returns:
            The parsed data
        """

        parser = importlib.import_module(self.parser)
        return parser.parse(import_source)

    def handle(self, import_source: "ImportSource", parsed_data: Dict[str, Any], **kwargs):
        """
        Call the Handler on the parsed data
        Args:
            import_source: The initial import source
            parsed_data: The parsed_data
        """
        if parsed_data:
            if handler_class := getattr(self.model, "import_export_handler_class", None):
                handler = handler_class(import_source)
                handler.process(parsed_data, **kwargs)

    class Meta:
        constraints = (models.UniqueConstraint(name="unique_parserhandler", fields=("parser", "handler")),)
        verbose_name = _("Parser-Handler")
        verbose_name_plural = _("Parsers-Handlers")

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{parser}}::{{handler}}"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcore:io:parserhandlerrepresentation-list"


class ImportedObjectProviderRelationship(ComplexToStringMixin):
    """
    A model that represent the relationship/link between the imported object and a provider.

    This model can be used to define different identifier in case the object is imported from difference providers
    """

    provider = models.ForeignKey(
        to="io.Provider", related_name="imported_object_relationships", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    provider_identifier = models.CharField(max_length=255)

    def compute_str(self) -> str:
        try:
            return f"{self.provider.title} -> {self.content_object}: {self.provider_identifier}"
        except AttributeError:
            return f"{self.provider.title} ({self.provider_identifier})"

    class Meta:
        verbose_name = _("Content object Provider Identifier relationship")
        verbose_name_plural = _("Content object Provider Identifier relationships")
        constraints = (
            models.UniqueConstraint(
                name="unique_contentobjectprovideridentifierrelationship",
                fields=("content_type", "object_id", "provider"),
            ),
            models.UniqueConstraint(
                name="unique_contentobjectprovideridentifier",
                fields=("content_type", "provider_identifier", "provider"),
            ),
        )
        indexes = [
            models.Index(fields=["content_type", "object_id", "provider"]),
            models.Index(fields=["content_type", "provider_identifier", "provider"]),
        ]


class Provider(models.Model):
    """
    Represent a data vendor/provider. Every source is linked to a provider and are represented by a unique identifier
    extracted from the data backend root folder

    Example:
        io/backend/refinitiv/instrument_prices.py => Provider.objects.get(key="refinitiv")
    """

    title = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.key})"

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")


class DataBackend(models.Model):
    """
    Represents the instantiated backend imported through the specified dotted path and the passed parameters
    """

    title = models.CharField(max_length=255)

    save_data_in_import_source = models.BooleanField(
        default=True, help_text="If true, save the data in the import_source json field"
    )
    passive_only = models.BooleanField(
        default=True, help_text="If True, this data backend is allowed to be called only from the import source."
    )

    backend_class_path = models.CharField(max_length=512)
    backend_class_name = models.CharField(max_length=128, default="DataBackend")

    provider = models.ForeignKey(
        "io.Provider",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Provider"),
    )

    def get_internal_object(self, object_content_type: ContentType, provider_external_id: str) -> models.Model | None:
        """
        Internal facing function that returns the internal id of the object with the given external provider identifier. If the relationship already exists, we simply returns the stored id. Otherwise we call the appropriate function to get
        Args:
            object_content_type: ContentType object representing the seeked object id
            provider_external_id: The object identifier as given by this backend provider

        Returns:
            The object as stored in the importer object-provider relationship. None if it doesn't exist yet
        """
        if rel := ImportedObjectProviderRelationship.objects.filter(
            provider=self.provider, provider_identifier=provider_external_id, content_type=object_content_type
        ).first():
            return rel.content_object

    class Meta:
        verbose_name = _("Data Backend")
        verbose_name_plural = _("Data Backends")

    @cached_property
    def backend_class(self) -> Any:
        """
        Return the imported backend class
        Returns:
            The backend class
        """
        return getattr(import_module(self.backend_class_path), self.backend_class_name)

    def __str__(self) -> str:
        return self.title

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{title}}"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcore:io:databackendrepresentation-list"


class Source(models.Model):
    title = models.CharField(max_length=128)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    parser_handler = models.ManyToManyField(
        "io.ParserHandler",
        verbose_name="Parser/Handler",
        related_name="sources",
    )

    is_active = models.BooleanField(default=True)

    connection_parameters = models.JSONField(default=dict, null=True, blank=True)
    import_parameters = models.JSONField(default=dict, null=True, blank=True)

    credentials = models.ManyToManyField("io.ImportCredential", blank=True, related_name="sources")

    data_backend = models.ForeignKey("io.DataBackend", on_delete=models.CASCADE, verbose_name=_("Data Backend"))

    crontab = models.ForeignKey(
        CrontabSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Crontab Schedule"),
        help_text=_("Crontab Schedule to run the task on.  Set only one schedule type, leave the others null."),
    )

    periodic_task = models.ForeignKey(
        PeriodicTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Periodic Task",
        related_name="sources",
    )

    import_timedelta_interval = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instantiated_backend: Any = None

    def init_backend(self, execution_datetime: datetime):
        """
        Singleton that instantiate the backend attribute

        Args:
            execution_datetime: Datetime at which the backend is supposed to be initialize

        """
        if not self.instantiated_backend:
            self.instantiated_backend = self.data_backend.backend_class(
                import_credential=self.get_valid_credential(execution_datetime),
                data_backend=self.data_backend,
                **self.connection_parameters,
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_periodic_task()

    def __str__(self) -> str:
        return self.title if self.title else f"{self.uuid}"

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    @property
    def current_valid_credential(self) -> "ImportCredential":
        """
        Property that returns the current valid credential

        Returns:
            The valid ImportCredential (as of now)
        """
        return self.get_valid_credential(timezone.now())

    @property
    def crontab_repr(self) -> str:
        """
        Returns the crontab string representation.
        :return: crontab string representation
        """
        if not self.crontab:
            return ""

        return "{0} {1} {2} {3} {4}".format(
            cronexp(self.crontab.minute),
            cronexp(self.crontab.hour),
            cronexp(self.crontab.day_of_month),
            cronexp(self.crontab.month_of_year),
            cronexp(self.crontab.day_of_week),
        )

    def update_periodic_task(self):
        """
        Utility function to find and update the link periodic task given the current source state
        """
        if self.crontab:
            if task := self.periodic_task:
                task.crontab = self.crontab
                task.enabled = self.is_active
                task.save()
            else:
                task = PeriodicTask.objects.update_or_create(
                    name=f"Import-Export: {self}",
                    defaults={
                        "crontab": self.crontab,
                        "args": json.dumps([self.pk]),
                        "task": "wbcore.contrib.io.models.trigger_workflow_as_task",
                    },
                )[0]
            Source.objects.filter(pk=self.pk).update(periodic_task=task)
            self.refresh_from_db()

    def get_valid_credential(self, val_datetime: datetime) -> "ImportCredential":
        """
        Get the valid credential
        Args:
            val_datetime: The date at which the credentials need to be valid
        Returns:
            A valid credential
        """
        return (
            self.credentials.filter(
                (Q(validity_start__lte=val_datetime) | Q(validity_start__isnull=True))
                & (Q(validity_end__gte=val_datetime) | Q(validity_end__isnull=True))
            )
            .order_by("-validity_end")
            .first()
        )

    def get_or_create_provider_id(self, obj: models.Model) -> str | None:
        """
        Workflow method that try to get or fetch the provider identifier for the passed object.

        If the relationship already exists, we directly returns the stored external id. Otherwise we call the appropriate function on the already instantiated backend to get it from the provider itself. If the value is returned, we store the relationship

        Args:
            obj: The object to get the external provider identifier from

        Returns:
            If it exists, the external identifier (from this source provider). None otherwise.
        """

        if (provider := self.data_backend.provider) and self.instantiated_backend is not None:
            if self.instantiated_backend.is_object_valid(obj):
                if rel := ImportedObjectProviderRelationship.objects.filter(
                    provider=provider, content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk
                ).first():
                    return rel.provider_identifier
                else:
                    if provider_identifier := self.instantiated_backend.get_provider_id(obj):
                        with transaction.atomic():
                            ImportedObjectProviderRelationship.objects.create(
                                provider=provider,
                                content_type=ContentType.objects.get_for_model(obj),
                                object_id=obj.pk,
                                provider_identifier=provider_identifier,
                            )
                            return provider_identifier
            obj.save()
        else:
            raise ValueError(
                f"You can't create a provider relationship with {obj} with for backend {self.data_backend} without a provider assigned"
            )

    def is_valid_date(self, sync_datetime: datetime) -> bool:
        """
        check wether a date is valid given the stored crontab schedule
        Args:
            sync_datetime: The datetime at which validity needs to be checked
        Returns:
            True if the given date is valid given the source crontab
        """
        if not self.crontab:
            return False
        return croniter.match(self.crontab_repr, sync_datetime)

    def trigger_workflow(
        self,
        execution_time: Optional[datetime] = None,
        callback_signature: Callable | None = None,
        callback_args: list | None = None,
        callback_kwargs: Dict | None = None,
        synchronous: bool = False,
        **kwargs,
    ):
        """
        The entry point function of the whole import source workflow.
        Loop over all files return by the attached backend and save the result into a serie of import sources.

        Args:
            execution_time: The time at which the worfklow was triggerd
            callback_signature: The celery canvas signature to be called upon completion (if any)
            callback_args: the potential positional arguments to be passed to the callback function (if any)
            callback_kwargs: Potential keyword arguments to be passed to the callback function (if any)
            synchronous: If true, will execute the workflow synchronously. Default to False
            **kwargs: keyword arguments to be passed down along the workflow

        Returns:
            A generator of import sources
        """
        if not execution_time:
            execution_time = timezone.now()
        # If a queryset is provided, we need to convert it into a list of valid external id that we will get from the relationship through model or from the backend directly if not existing

        chained_tasks = [
            generate_import_sources_as_task.s(self.pk, execution_time, **kwargs),
            process_import_sources_as_task.s(),
        ]
        if not callback_args:
            callback_args = []
        if not callback_kwargs:
            callback_kwargs = {}
        if callback_signature:
            chained_tasks.append(callback_signature.si(*callback_args, **callback_kwargs))
        if synchronous:
            import_source_ids = chained_tasks[0].apply().get()
            chained_tasks[1].apply((import_source_ids,))
            if len(chained_tasks) > 2:
                chained_tasks[2].apply(tuple(callback_args), callback_kwargs)
        else:
            chain(*chained_tasks).apply_async(eta=execution_time)

    def generate_import_sources(
        self,
        execution_time: datetime,
        only_handler: str | None = None,
        **kwargs,
    ) -> list["ImportSource"]:
        """
                Process the source based on its attached backend (returns an error if such backend does not exist)
        The backend is first initialize through constructor and then, The generator `get_files` is called, passing the
        execution time, the expected data time, and some keyword arguments.

        For each file returns by the generator, we create a ImportSource objects and trigger its import task
        Args:
            execution_time: The time at which this task was triggered
            **kwargs: keyword arguments to be passed down along the workflow
        Returns:
            Return a generator of import sources
        """
        if not self.data_backend:
            raise ValueError("Data Backend not specied for this source")

        # Import the data backend module and extract its class_name
        res = []
        # Get the expected date at which this source should return its data (e.g. T-1)

        # Loop over the backend returned generator
        self.init_backend(execution_time)
        errors = []
        queryset = kwargs.pop("queryset", self.instantiated_backend.get_default_queryset())
        if self.data_backend.provider and queryset is not None:
            obj_external_ids = []
            for obj in tqdm(queryset, total=queryset.count()):
                try:
                    if external_id := self.get_or_create_provider_id(obj):
                        obj_external_ids.append(external_id)
                except IntegrityError:
                    errors.append(str(obj))
            kwargs["obj_external_ids"] = obj_external_ids
        else:
            kwargs["queryset"] = queryset
        streams = self.instantiated_backend.get_files(
            execution_time,
            **{
                **self.import_parameters,
                **kwargs,
            },
        )
        if streams:
            for file_name, _file in streams:
                content_file = ContentFile(_file.getvalue())
                content_file.name = file_name
                parser_handlers = self.parser_handler.all()
                if only_handler:
                    parser_handlers = parser_handlers.filter(handler__iexact=only_handler)
                for parser_handler in parser_handlers:
                    with transaction.atomic():
                        import_source = ImportSource.objects.create(
                            file=content_file,
                            parser_handler=parser_handler,
                            save_data=self.import_parameters.get(
                                "save_data_in_import_source", self.data_backend.save_data_in_import_source
                            ),
                            source=self,
                        )
                        res.append(import_source)
        return res

    @classmethod
    def load_sources_from_settings(cls, settings: list[tuple[list[tuple[str, str]], str, dict[str, Any]]]):
        """
        Utility classmethod to parser sources from the settings.

        We assume data structure as follow

        [
            (
                [("module1.HandlerModel1", "module1.io.parsers.provider1.handler1")],
                "module1.io.backends.provider1.handler1.DataBackend",
                {
                    "credentials": [credential_dict],
                    "crontab": "10 9,17,1 * * *",
                },
            ),
            (
                [("module2.HandlerModel2", "module2.io.parsers.provider2.handler2")],
                "module2.io.backends.provider2.handler2.DataBackend",
            )
        ]
        Args:
            settings: The source settings to parse

        """
        for parser_handlers, data_backend_module, config in settings:
            with suppress(Exception):
                # This method is loaded when server boots. If this fail, it can prevent the server from starting.
                backend_class_path, _, backend_class_name = data_backend_module.rpartition(".")

                data_backend = DataBackend.objects.get(
                    backend_class_path=backend_class_path, backend_class_name=backend_class_name
                )
                crontab = None
                credentials = config.pop("credentials", [])
                if crontab_data := config.pop("crontab", None):
                    minute, hour, day_of_month, month_of_year, day_of_week = crontab_data.split(" ")
                    crontab_kwargs = {
                        "minute": minute,
                        "hour": hour,
                        "day_of_week": day_of_week,
                        "day_of_month": day_of_month,
                        "month_of_year": month_of_year,
                    }
                    crontabs = CrontabSchedule.objects.filter(**crontab_kwargs)
                    if crontabs.exists():
                        crontab = crontabs.first()
                    else:
                        crontab = CrontabSchedule.objects.create(**crontab_kwargs)

                source, source_created = Source.objects.get_or_create(
                    data_backend=data_backend,
                    defaults={"crontab": crontab, **config},
                )
                for handler, parser in parser_handlers:
                    parser_handler = ParserHandler.objects.get_or_create(parser=parser, handler=handler)[0]
                    if parser_handler not in source.parser_handler.all():
                        source.parser_handler.add(parser_handler)
                for credential_data in credentials:
                    credential, created = ImportCredential.objects.get_or_create(
                        key=credential_data["key"], defaults=credential_data
                    )
                    if credential not in source.credentials.all():
                        source.credentials.add(credential)
                source.save()

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{title}} ({{id}})"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcore:io:sourcerepresentation-list"


@receiver(post_delete, sender="io.Source")
def post_delete_source(sender, instance, **kwargs):
    # Delete the attached period task
    if instance.periodic_task:
        instance.periodic_task.delete()


@receiver(pre_delete, sender="io.Source")
def pre_delete_source(sender, instance, **kwargs):
    # Unassign import source from the deleting source
    ImportSource.objects.filter(source=instance).update(source=None)


@shared_task(queue=Queue.BACKGROUND.value)
def trigger_workflow_as_task(source_id: int, execution_time: datetime | None = None, **kwargs):
    """
    Call the `import_source` as a celery task
    """
    source = Source.objects.get(id=source_id)
    source.trigger_workflow(execution_time=execution_time, **kwargs)


@shared_task(queue=Queue.BACKGROUND.value)
def generate_import_sources_as_task(source_id: int, execution_time: datetime, **kwargs) -> list[int]:
    """
    Call the `import_source` as a celery task
    """
    source = Source.objects.get(id=source_id)
    import_source_ids = [
        import_source.pk for import_source in source.generate_import_sources(execution_time, **kwargs)
    ]  # convert to list to be json serializable
    return import_source_ids


@shared_task(queue=Queue.BACKGROUND.value)
def process_import_sources_as_task(import_source_ids: list[int]):
    """
    Call the `import_source` as a celery task
    """
    for import_source_id in import_source_ids:
        import_source = ImportSource.objects.get(id=import_source_id)
        import_source.import_data(force_reimport=True)


class ImportExportSource(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSED = "PROCESSED", "Processed"
        WARNING = "WARNING", "Warning"
        ERROR = "ERROR", "Error"
        IGNORED = "IGNORED", "Ignore"

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING.value,
    )

    log = models.TextField(null=True, blank=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    creator = models.ForeignKey(
        "authentication.User", null=True, blank=True, verbose_name="Creator", on_delete=models.SET_NULL
    )
    data = models.JSONField(default=dict, null=True, blank=True)
    resource_kwargs = models.JSONField(default=dict, blank=True, null=False)

    class Meta:
        abstract = True


class ExportSource(ImportExportSource):
    file = models.FileField(max_length=256, upload_to="io/export_source/files", null=True, blank=True)
    format = models.IntegerField(
        choices=ExportFormat.choices,
        default=ExportFormat.CSV.value,
        verbose_name=_("Format of file to be exported"),
    )

    content_type = models.ForeignKey(ContentType, verbose_name=_("Export job Content Type"), on_delete=models.CASCADE)

    resource_path = models.CharField(
        verbose_name=_("Resource path to use when exporting"), max_length=255, default="", blank=True, null=True
    )

    query_str = models.TextField(verbose_name=_("SQL query to be executed"), blank=True, null=False)
    query_params = PickledObjectField(  # we have to use picklefield because the sql parameters are given as python object. However, no django model should be stored in this field, which should be the case as these objects are given through their IDs
        blank=True, verbose_name=_("SQL query parameters to be used with the sql query"), default=list
    )

    class Meta:
        verbose_name = _("Export Source")
        verbose_name_plural = _("Export Sources")
        notification_types = [
            create_notification_type(
                code="io.export_done",
                title="File Export has finished",
                help_text="Notifies user when their submitted export files is done and available",
                web=True,
                mobile=True,
                email=True,
                resource_button_label="Download File",
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(query_str__isnull=False, resource_path__isnull=False) | ~Q(data__exact=dict()),
                name="check_either_data_or_resource_isnotnull",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)

    @property
    def file_format(self):
        return get_django_import_export_format(self.format)()

    @property
    def resource(self) -> Resource:
        """
        Load into an attribute the instantiated resource loaded from the resource path
        """
        resource_class = import_string(self.resource_path)
        return resource_class(**self.resource_kwargs)

    @property
    def queryset(self) -> models.QuerySet:
        """
        Recreate the base queryset from the content type model class base manager and the saved query string and parameters
        """

        return self.content_type.model_class().objects.raw(self.query_str, self.query_params)

    def get_export_filename(self):
        date_str = timezone.now().strftime("%Y-%m-%d")
        ts = datetime.timestamp(timezone.now())
        filename = "%s-%s_%s.%s" % (
            self.content_type.model_class().__name__,
            date_str,
            ts,
            self.file_format.get_extension(),
        )
        return filename

    def notify(self):
        """
        Notify the user if the export job is done and accessible
        """
        if self.file and self.status == self.Status.PROCESSED:
            send_notification(
                code="io.export_done",
                title=_("Your export file is available"),
                body=_("<p>The export job you requested is finished and available for one hour.</p>").format(
                    url=self.file.url
                ),
                endpoint=self.file.url,
                user=self.creator,
            )

    def export_data(self, debug: bool = False, **kwargs):
        self.log = ""
        self.status = self.Status.PENDING.name
        self.save()
        try:
            file_format = get_django_import_export_format(self.format)()
            if self.data:
                # Data was saved as a dictionary from a tablib.dataset, we need to recreate it
                data = Dataset()
                data.headers = self.data["headers"]
                data.extend(self.data["data"])
            else:
                data = self.resource.export(queryset=self.queryset)

            export_data = file_format.export_data(data)
            if not file_format.is_binary():
                export_data = export_data.encode("utf-8")
            self.file.save(self.get_export_filename(), ContentFile(export_data))
            self.status = self.Status.PROCESSED.name
            self.save()
            self.notify()

        except Exception as e:
            if debug:
                raise e
            else:
                ex_type, ex_value, _ = sys.exc_info()
                self.status = self.Status.ERROR.name
                self.log = f"{ex_type}: {ex_value}\n"
                self.log += traceback.format_exc()
                self.save()
                logger.error(
                    "Data source export failed: Processing error during file generation.",
                    extra={"export_source": self, "parser_handler": self.parser_handler, "detail": e},
                )


class ImportSource(ImportExportSource):
    file = models.FileField(max_length=256, upload_to="io/import_source/files", null=True, blank=True)

    save_data = models.BooleanField(default=True, help_text="If True, will save the raw data in a field")
    progress_index = models.PositiveIntegerField(default=0)

    parser_handler = models.ForeignKey("io.ParserHandler", on_delete=models.CASCADE)
    source = models.ForeignKey("io.Source", null=True, blank=True, verbose_name="Source", on_delete=models.SET_NULL)
    errors_log = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Import Source")
        verbose_name_plural = _("Import Sources")
        notification_types = [
            create_notification_type(
                code="io.import_done",
                title="File Import has finished",
                help_text="Notifies user when their submitted import files has finished",
            )
        ]

    def __str__(self) -> str:
        return f"{self.pk}"

    def _validate_file_type(self):
        """
        Valid the file type based on the allowed types specified by the parser
        Returns:
            True if the filetype is valid
        """
        if (upload := self.file) and (allow_file_type := self.parser_handler.allow_file_type):
            file_type = magic.from_buffer(upload.file.read(1024), mime=True)
            if file_type != allow_file_type:
                raise ValidationError("File type not supported.")

    def save(self, *args, **kwargs):
        # Check here company name, modify ...
        self._validate_file_type()
        super().save(*args, **kwargs)

    def _parse_data(self) -> dict[str, Any]:
        """
        Given the ParserHandler linked object, we import its related module and call its defined `parse` function
        Returns:
            Dict The parsed data as a python dictionary
        """
        if not self.file:
            raise ValueError("This import source does not include a valid file")
        parsed_data = self.parser_handler.parse(self)
        if self.save_data:
            self.data = parsed_data
        self.save()
        return parsed_data

    def _process_data(self, parsed_data: dict[str, Any], **kwargs):
        """
        Given the parsed data (as a python dictionary), import the corresponding handler and calls its defined `process
        Args:
            data: The deserialized data to be passed down to the parser
        """
        self.status = self.Status.PROCESSED.name
        if parsed_data:
            parsed_data_copy = deepcopy(parsed_data)
            if data := parsed_data_copy.pop("data", None):
                self.parser_handler.handle(self, {"data": data[self.progress_index :], **parsed_data_copy}, **kwargs)
                if self.errors_log:
                    self.status = self.Status.WARNING.name
        # clean log if we don't want to use space to save it
        if not self.save_data:
            self.log = ""
        self.save()

    def import_data(self, force_reimport: Optional[bool] = False, **kwargs):
        """
        General workflow method:
        * Parse the data given the linked import file
        * Handle the parsed data
        * Change the import_source status based on sucess
        Args:
            silent: False if this method is not suppose to silently catch the exceptions
        """
        if force_reimport:
            self.progress_index = 0
        self.log = ""
        self.errors_log = ""
        # self.data = {}
        self.status = self.Status.PENDING.name
        self.save()
        debug = kwargs.pop("debug", settings.DEBUG)
        try:
            data = self._parse_data()
            self._process_data(data, debug=debug, **kwargs)
            post_import.send(sender=self.parser_handler.model, import_source=self)

        except Exception as e:
            ex_type, ex_value, _ = sys.exc_info()
            self.status = self.Status.ERROR.name
            self.log = f"{ex_type}: {ex_value}\n"
            self.log += traceback.format_exc()
            self.save()
            if debug:
                raise e
            elif not self.creator:  # if a creator is set in this import source, they will receive a proper notification with feedback. No need then to pollute the logger
                logger.error(
                    "Data import failed: Processing error during file parsing and handling.",
                    extra={"import_source": self, "parser_handler": self.parser_handler, "detail": e},
                )

        self.notify()

    def notify(self):
        if self.creator:
            body = f"""<p><strong>File Name Processed:</strong> {self.file.name}</p>
        <p><strong>Number of Rows:</strong> {self.progress_index}</p>
        <p><strong>Status:</strong> {self.Status[self.status].label}</p>"""
            if self.status == self.Status.ERROR:
                body += "<p>While processing the import, we encountered an unrecoverable error. Please contact a system administrator.</p>"
            elif self.status == self.Status.WARNING and self.errors_log:
                body += f"""<p><strong>Warning:</strong> Some rows were ignored during import.</p>
        <p><strong>Ignored Rows:</strong></p>
        <ul>{"".join(["<li>" + line + "</li>" for line in io.StringIO(self.errors_log)])}</ul>"""
            send_notification(
                code="io.import_done",
                title=f"Your import finished with status {self.Status[self.status].label}",
                body=body,
                user=self.creator,
            )

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{file}}"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcore:io:importsourcerepresentation-list"


@shared_task(queue=Queue.BACKGROUND.value)
def import_data_as_task(import_source_id: int, **kwargs):
    """
    Call `import_data` as a celery task
    :param Int The import_source id
    """
    import_source = ImportSource.objects.get(id=import_source_id)
    import_source.import_data(**kwargs)


@shared_task(queue=Queue.DEFAULT.value)
def export_data_as_task(export_source_id: int, **kwargs):
    """
    Call `import_data` as a celery task
    :param Int The import_source id
    """
    export_source = ExportSource.objects.get(id=export_source_id)
    export_source.export_data(**kwargs)


@receiver(models.signals.post_save, sender=ExportSource)
def post_save_export_source(sender, instance: ExportSource, created: bool, raw: bool, **kwargs):
    """Triggers the export task on creation"""

    if not raw and created and instance.status == ExportSource.Status.PENDING:
        transaction.on_commit(lambda: export_data_as_task.delay(instance.id))


def validate_key_file(value: models.FileField):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != ".key":
        raise ValidationError("The file extension needs to be a .key")


def validate_pem_file(value: models.FileField):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != ".pem":
        raise ValidationError("The file extension needs to be a .pem")


class ImportCredential(models.Model):
    class Type(models.TextChoices):
        CREDENTIAL = "CREDENTIAL", "Credential"
        AUTHENTICATION_TOKEN = "AUTHENTICATION_TOKEN", "Authentication Token"
        CERTIFICATE = "CERTIFICATE", "Certificate"

    key = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, default=Type.CREDENTIAL, max_length=64)

    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    authentication_token = models.CharField(max_length=2048, null=True, blank=True)

    certificate_pem = models.FileField(
        max_length=256,
        null=True,
        blank=True,
        upload_to="io/import_credential/certificates",
        help_text="We are expecting a .cert file",
        validators=[validate_pem_file],
    )
    certificate_key = models.FileField(
        max_length=256,
        null=True,
        blank=True,
        upload_to="io/import_credential/certificates",
        help_text="We are expecting a .key file",
        validators=[validate_key_file],
    )

    additional_resources = models.JSONField(default=dict, null=True, blank=True)

    validity_start = models.DateTimeField(null=True, blank=True)
    validity_end = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.type == self.Type.CREDENTIAL and (not self.username or not self.password):
            raise ValidationError("The type is credential, you need to specify a username and a password")
        elif self.type == self.Type.AUTHENTICATION_TOKEN and not self.authentication_token:
            raise ValidationError("The type is authentication header, you need to specify a valid header")
        elif self.type == self.Type.CERTIFICATE and (not self.certificate_key or not self.certificate_pem):
            raise ValidationError("The type is certificate, you need to specify valid public and private key files")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Import Credential")
        verbose_name_plural = _("Import Credentials")

    def __str__(self) -> str:
        dates_repr = ""
        if self.validity_start:
            dates_repr += f"{self.validity_start:%Y-%m-%d %H:%M:%S}"
        if self.validity_end:
            dates_repr += f"- {self.validity_end:%Y-%m-%d %H:%M:%S}"
        if dates_repr:
            return f"{self.key} ({dates_repr})"
        return self.key
