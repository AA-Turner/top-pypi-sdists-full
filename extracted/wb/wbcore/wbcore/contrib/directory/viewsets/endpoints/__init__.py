from .contacts import (
    AddressContactEntryEndpointConfig,
    BankingContactEndpointConfig,
    BankingContactEntryEndpointConfig,
    EmailContactEntryEndpointConfig,
    SocialMediaContactEntryEndpointConfig,
    TelephoneContactEntryEndpointConfig,
    WebsiteContactEntryEndpointConfig,
)
from .entries import (
    CompanyModelEndpointConfig,
    EntryModelEndpointConfig,
    PersonModelEndpointConfig,
    UserIsManagerEndpointConfig,
    PersonRepresentationEndpointConfig,
    CompanyRepresentationEndpointConfig
)
from .relationships import (
    ClientManagerEndpoint,
    EmployeeEmployerEndpointConfig,
    EmployerEmployeeEndpointConfig,
    RelationshipEntryModelEndpoint,
    UserIsClientEndpointConfig,
)
