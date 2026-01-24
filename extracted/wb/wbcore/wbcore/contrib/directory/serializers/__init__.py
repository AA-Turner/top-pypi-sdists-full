from ..configurations import configuration_registry

CompanyModelSerializer = configuration_registry.company_model_serializer
CompanyRepresentationSerializer = configuration_registry.company_representation_serializer
PersonModelSerializer = configuration_registry.person_model_serializer
PersonRepresentationSerializer = configuration_registry.person_representation_serializer

from .companies import (
    BankModelSerializer,
    CompanyModelListSerializer,
    CompanyModelSerializer,
)
from .contacts import (
    AddressContactRepresentationSerializer,
    AddressContactSerializer,
    BankingContactRepresentationSerializer,
    BankingContactSerializer,
    ReadOnlyBankingContactSerializer,
    CityRepresentationSerializer,
    EmailContactRepresentationSerializer,
    EmailContactSerializer,
    SocialMediaContactRepresentationSerializer,
    SocialMediaContactSerializer,
    TelephoneContactRepresentationSerializer,
    TelephoneContactSerializer,
    WebsiteContactRepresentationSerializer,
    WebsiteContactSerializer,
)
from .entries import (
    CompanyRepresentationSerializer,
    CompanyTypeModelSerializer,
    CompanyTypeRepresentationSerializer,
    CustomerStatusModelSerializer,
    CustomerStatusRepresentationSerializer,
    EntryModelSerializer,
    EntryRepresentationSerializer,
    InternalUserProfileRepresentationSerializer,
    PersonRepresentationSerializer,
    FullDetailPersonRepresentationSerializer,
    SpecializationModelSerializer,
    SpecializationRepresentationSerializer,
)
from .entry_representations import (
    EntryRepresentationSerializer,
    EntryUnlinkedRepresentationSerializer,
)
from .persons import (
    NewPersonModelSerializer,
    PersonModelListSerializer,
    PersonModelSerializer,
)
from .relationships import (
    ClientManagerModelSerializer,
    ClientManagerRelationshipRepresentationSerializer,
    EmployerEmployeeRelationshipSerializer,
    PositionModelSerializer,
    PositionRepresentationSerializer,
    RelationshipModelSerializer,
    RelationshipRepresentationSerializer,
    RelationshipTypeModelSerializer,
    RelationshipTypeRepresentationSerializer,
    UserIsClientModelSerializer,
)
