import factory

from ..models import (
    AddressContact,
    BankingContact,
    EmailContact,
    SocialMediaContact,
    TelephoneContact,
    WebsiteContact,
)


class ContactBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    primary = factory.Faker("pybool")
    # location = factory.SubFactory('directory.factories.contacts.ContactLocationFactory')
    entry = factory.SubFactory("wbcore.contrib.directory.factories.entries.PersonFactory")


class BankingContactFactory(ContactBaseFactory):
    class Meta:
        model = BankingContact

    institute = factory.Faker("company")
    institute_additional = factory.Faker("sentence", nb_words=3)
    iban = factory.Faker("iban")
    swift_bic = factory.Faker("swift")
    currency = factory.SubFactory("wbcore.contrib.currency.factories.CurrencyFactory")
    additional_information = factory.Faker("paragraph")


class AddressContactFactory(ContactBaseFactory):
    class Meta:
        model = AddressContact

    street = factory.Faker("street_address")
    street_additional = factory.Faker("sentence", nb_words=3)
    zip = factory.Faker("zipcode")
    geography_city = factory.SubFactory("wbcore.contrib.geography.factories.CityFactory")


class TelephoneContactFactory(ContactBaseFactory):
    class Meta:
        model = TelephoneContact

    number = factory.Faker("phone_number")
    # telephone_type = factory.SubFactory('directory.factories.contacts.ContactTelephoneTypeFactory')


class EmailContactFactory(ContactBaseFactory):
    class Meta:
        model = EmailContact
        django_get_or_create = ["address"]

    address = factory.Faker("email")


class WebsiteContactFactory(ContactBaseFactory):
    class Meta:
        model = WebsiteContact

    url = factory.Faker("uri")


class SocialMediaContactFactory(ContactBaseFactory):
    class Meta:
        model = SocialMediaContact

    platform = factory.Iterator(SocialMediaContact.Platforms)
    url = factory.Faker("url")
