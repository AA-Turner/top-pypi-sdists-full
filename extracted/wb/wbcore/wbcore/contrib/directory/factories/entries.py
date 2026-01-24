import random

import factory
from django.core.files.base import ContentFile
from django.db.models import signals

from ..models import Company, CompanyType, CustomerStatus, Entry, Person, Specialization


class CustomerStatusFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=32)

    class Meta:
        model = CustomerStatus


class CompanyTypeFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=32)

    class Meta:
        model = CompanyType
        django_get_or_create = ["title"]


class BankCompanyTypeFactory(CompanyTypeFactory):
    title = "Bank"


class SpecializationFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=32)

    class Meta:
        model = Specialization


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class EntryBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = False


class EntryContactBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = False

    profile_image = factory.django.ImageField(filename="image_profile.jpeg")

    banking = factory.RelatedFactory("wbcore.contrib.directory.factories.contacts.BankingContactFactory", "entry")
    addresses = factory.RelatedFactory("wbcore.contrib.directory.factories.contacts.WebsiteContactFactory", "entry")


class EntryFactory(EntryBaseFactory):
    class Meta:
        model = Entry
        skip_postgeneration_save = True

    # entry_type
    signature = factory.django.ImageField(filename="signature.jpeg")
    activity_heat = random.uniform(0.0, 1.0)
    salutation = factory.Faker("text", max_nb_chars=64)

    @factory.post_generation
    def relationship_managers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for in_charg in extracted:
                self.relationship_managers.add(in_charg)


class CompanyFactory(EntryFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    customer_status = factory.SubFactory(CustomerStatusFactory)
    type = factory.SubFactory(CompanyTypeFactory)
    tier = factory.Iterator(Company.Tiering.choices, getter=lambda tier: tier[0])


class EntryContactFactory(EntryFactory):
    @factory.post_generation
    def telephones(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for telephone in extracted:
                self.telephones.add(telephone)

    @factory.post_generation
    def emails(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for email in extracted:
                self.emails.add(email)


class EmployersCompanyFactory(CompanyFactory):
    @factory.post_generation
    def employees(self, create, extracted, **kwargs):
        if extracted:
            for _ in range(extracted):
                PersonFactory(employers=(self,))


class BankFactory(CompanyFactory):
    type = factory.SubFactory(BankCompanyTypeFactory)


class PersonFactory(EntryFactory):
    class Meta:
        model = Person

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthday = factory.Faker("date_object")
    description = factory.Faker("text")
    personality_profile_red = random.randint(1, 5)
    personality_profile_green = random.randint(1, 5)
    personality_profile_blue = random.randint(1, 5)
    prefix = factory.Iterator(Person.Prefix.choices, getter=lambda prefix: prefix[0])

    @factory.post_generation
    def employers(self, create, extracted, **kwargs):
        if extracted:
            for employer in extracted:
                self.employers.add(employer)


class PersonWithEmployerFactory(PersonFactory):
    employers = factory.RelatedFactory(
        "wbcore.contrib.directory.factories.relationships.EmployerEmployeeRelationshipFactory",
        factory_related_name="employee",
    )


class PersonSignatureFactory(PersonFactory):
    signature = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 768}),
            "example.jpg",
        )
    )


class CompanyWithEmployerEmployeeRelationshipFactory(CompanyFactory):
    employees = factory.RelatedFactory(
        "wbcore.contrib.directory.factories.relationships.EmployerEmployeeRelationshipFactory",
        factory_related_name="employer",
    )


class ClientFactory(PersonFactory):
    @factory.post_generation
    def clients(self, create, extracted, **kwargs):
        if extracted:
            for person in extracted:
                self.clients.add(person)


class RandomClientFactory(ClientFactory):
    @factory.post_generation
    def clients(self, create, extracted, **kwargs):
        self.clients.add(PersonFactory())


class UnemployedPersonFactory(PersonFactory):
    @factory.post_generation
    def employers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.employers.set()
