import factory
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_celery_beat.models import CrontabSchedule
from faker import Faker

from wbcore.contrib.io.imports import ImportExportHandler
from wbcore.contrib.io.mixins import ImportMixin

from .enums import ExportFormat
from .models import (
    DataBackend,
    ExportSource,
    ImportCredential,
    ImportSource,
    ParserHandler,
    Provider,
    Source,
)


class ImportExportModelHandler(ImportExportHandler):
    MODEL_APP_LABEL = "io.ImportModel"

    def _deserialize(self, data):
        data["relationship"] = ParserHandler.objects.get(id=data["relationship"])
        data["many_relationships"] = [ParserHandler.objects.get(id=d) for d in data["many_relationships"]]

    def _get_instance(self, data, history=None, **kwargs) -> models.Model | None:
        if id := data.get("id", None):
            if history:
                return history.filter(id=id).first()
            return self.model.objects.filter(id=id).first()

    def _create_instance(self, data, **kwargs) -> models.Model:
        data.pop("id", None)
        many_relationships = data.pop("many_relationships", [])
        obj = self.model.objects.create(import_source=self.import_source, **data)
        for rel in many_relationships:
            obj.many_relationships.add(rel)
        return obj

    def _get_history(self, history):
        # Return all object with the same relationship
        return self.model.objects.filter(relationship=history["relationship"])


# TODO remove this class
class ImportModel(ImportMixin):
    import_export_handler_class = ImportExportModelHandler
    relationship = models.ForeignKey(
        "io.ParserHandler", blank=True, null=True, on_delete=models.SET_NULL, related_name="imports"
    )
    import_source = models.ForeignKey(
        "io.ImportSource", blank=True, null=True, on_delete=models.SET_NULL, related_name="imports"
    )
    many_relationships = models.ManyToManyField("io.ParserHandler", blank=True, related_name="many_imports")
    number = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)


fake = Faker()


class CrontabScheduleFactory(factory.django.DjangoModelFactory):
    hour = factory.Iterator(range(0, 24))
    minute = factory.Iterator(range(0, 60))

    class Meta:
        model = CrontabSchedule


class ProviderFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("company")
    key = factory.LazyAttribute(lambda x: x.title.lower())

    class Meta:
        model = Provider


class DataBackendFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Data Backend {n}")
    save_data_in_import_source = False
    passive_only = False
    backend_class_path = "wbcore.contrib.io.backends.abstract"
    backend_class_name = "AbstractDataBackend"
    provider = factory.SubFactory("wbcore.contrib.io.factories.ProviderFactory")

    class Meta:
        model = DataBackend


class ExportSourceFactory(factory.django.DjangoModelFactory):
    """
    Default exportt source factory that are attached to the parser handler model and serializer
    """

    created = factory.Faker("date_time")
    last_updated = factory.Faker("date_time")
    log = factory.Faker("paragraph")
    origin = factory.Faker("company")
    status = ExportSource.Status.PENDING.value
    creator = factory.SubFactory("wbcore.contrib.authentication.factories.UserFactory")
    file = None
    format = factory.Iterator(ExportFormat.values)

    content_type = factory.LazyAttribute(lambda x: ContentType.objects.get_for_model(ParserHandler))
    resource_path = "wbcore.contrib.io.resources.ViewResource"
    resource_kwargs = {
        "columns_map": {"parser": "Parser", "handler": "Handler"},
        "serializer_class_path": "wbcore.contrib.io.serializers.ParserHandlerModelSerializer",
    }
    query_str = factory.LazyAttribute(lambda x: ParserHandler.objects.all().query.sql_with_params()[0])
    query_params = factory.LazyAttribute(lambda x: ParserHandler.objects.all().query.sql_with_params()[1])

    class Meta:
        model = ExportSource


class ImportSourceFactory(factory.django.DjangoModelFactory):
    created = factory.Faker("date_time")
    last_updated = factory.Faker("date_time")
    parser_handler = factory.SubFactory("wbcore.contrib.io.factories.ParserHandlerFactory")
    source = factory.SubFactory("wbcore.contrib.io.factories.SourceFactory")
    save_data = True
    log = factory.Faker("paragraph")
    origin = factory.Faker("company")
    file = None

    class Meta:
        model = ImportSource


class ImportCredentialFactory(factory.django.DjangoModelFactory):
    type = ImportCredential.Type.CREDENTIAL
    username = factory.Sequence(lambda n: f"username-{n}")
    password = factory.Sequence(lambda n: f"password-{n}")
    key = factory.Sequence(lambda n: f"credential-{n}")
    validity_start = None
    validity_end = None

    class Meta:
        model = ImportCredential


class SourceFactory(factory.django.DjangoModelFactory):
    crontab = factory.SubFactory("wbcore.contrib.io.factories.CrontabScheduleFactory")
    data_backend = factory.SubFactory("wbcore.contrib.io.factories.DataBackendFactory")
    import_parameters = factory.LazyAttribute(lambda o: {fake.name(): fake.name(), fake.name(): fake.name()})
    connection_parameters = factory.LazyAttribute(lambda o: {fake.name(): fake.name(), fake.name(): fake.name()})
    is_active = True
    title = factory.Sequence(lambda n: f"title {n}")

    class Meta:
        model = Source
        skip_postgeneration_save = True

    @factory.post_generation
    def parser_handler(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for parser_handler in extracted:
                self.parser_handler.add(parser_handler)

    @factory.post_generation
    def credentials(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for credential in extracted:
                self.credentials.add(credential)


class ParserHandlerFactory(factory.django.DjangoModelFactory):
    parser = factory.Sequence(lambda n: f"parser_{n}")
    handler = "io.ImportModel"
    allow_file_type = None

    class Meta:
        model = ParserHandler


class ImportModelFactory(factory.django.DjangoModelFactory):
    relationship = factory.SubFactory("wbcore.contrib.io.factories.ParserHandlerFactory")
    import_source = factory.SubFactory("wbcore.contrib.io.factories.ImportSourceFactory")
    number = factory.Faker("pyfloat")
    text = factory.Faker("paragraph")
    name = factory.Faker("name")

    class Meta:
        model = ImportModel
        skip_postgeneration_save = True

    @factory.post_generation
    def many_relationships(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for relationship in extracted:
                self.many_relationships.add(relationship)
