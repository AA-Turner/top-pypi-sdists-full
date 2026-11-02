from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class ConsoleVariables(AppwriteModel):
    """
    Console Variables

    Attributes
    ----------
    app_domain_target_cname : str
        CNAME target for your Appwrite custom domains.
    app_domain_target_a : str
        A target for your Appwrite custom domains.
    app_compute_build_timeout : float
        Maximum build timeout in seconds.
    app_domain_target_aaaa : str
        AAAA target for your Appwrite custom domains.
    app_domain_target_caa : str
        CAA target for your Appwrite custom domains.
    app_storage_limit : float
        Maximum file size allowed for file upload in bytes.
    app_compute_size_limit : float
        Maximum file size allowed for deployment in bytes.
    app_usage_stats : str
        Defines if usage stats are enabled. This value is set to &#039;enabled&#039; by default, to disable the usage stats set the value to &#039;disabled&#039;.
    app_vcs_enabled : bool
        Defines if VCS (Version Control System) is enabled.
    app_vcs_providers : List[Any]
        List of configured VCS providers.
    app_vcs_providers_with_repository_creation : List[Any]
        List of configured VCS providers that support repository creation.
    app_vcs_providers_with_public_repositories : List[Any]
        List of configured VCS providers that can host public repositories.
    app_domain_enabled : bool
        Defines if main domain is configured. If so, custom domains can be created.
    app_domain_sites : str
        A comma separated list of domains to use for site URLs.
    app_domain_functions : str
        A domain to use for function URLs.
    app_options_force_https : str
        Defines if HTTPS is enforced for all requests.
    app_domains_nameservers : str
        Comma-separated list of nameservers.
    app_db_adapter : str
        Database adapter in use.
    supportforattributes : bool
        Whether the database adapter enforces defined attributes.
    supportforrelationships : bool
        Whether the database adapter supports relationships.
    supportforoperators : bool
        Whether the database adapter supports operators.
    supportforspatials : bool
        Whether the database adapter supports spatial attributes.
    supportforaggregations : bool
        Whether the database adapter supports aggregation queries.
    supportforjoins : bool
        Whether the database adapter supports join queries.
    supportforspatialindexnull : bool
        Whether the database adapter supports spatial indexes on nullable columns.
    supportforfulltextwildcard : bool
        Whether the database adapter supports fulltext wildcard search.
    supportformultiplefulltextindexes : bool
        Whether the database adapter supports multiple fulltext indexes per collection.
    supportfortrigramindex : bool
        Whether the database adapter supports trigram indexes.
    supportforattributeresizing : bool
        Whether the database adapter supports resizing attributes.
    supportforschemas : bool
        Whether the database adapter supports fixed schemas with row width limits.
    maxindexlength : float
        Maximum index length supported by the database adapter.
    supportforintegerids : bool
        Whether the database adapter uses integer sequence IDs.
    app_console_email_verification : str
        Whether email verification for console users is required. Can be &quot;true&quot; or &quot;false&quot;.
    app_domain_email : str
        Appwrite-owned zone for function testing email addresses, delivered to {functionId}@{projectId}.{zone}. Empty when inbound email is not configured.
    app_domain_target_smtp : str
        MX target a custom inbound email (SMTP) domain must point at. Empty when inbound email is not configured.
    """

    app_domain_target_cname: str = Field(..., alias='_APP_DOMAIN_TARGET_CNAME')
    app_domain_target_a: str = Field(..., alias='_APP_DOMAIN_TARGET_A')
    app_compute_build_timeout: float = Field(..., alias='_APP_COMPUTE_BUILD_TIMEOUT')
    app_domain_target_aaaa: str = Field(..., alias='_APP_DOMAIN_TARGET_AAAA')
    app_domain_target_caa: str = Field(..., alias='_APP_DOMAIN_TARGET_CAA')
    app_storage_limit: float = Field(..., alias='_APP_STORAGE_LIMIT')
    app_compute_size_limit: float = Field(..., alias='_APP_COMPUTE_SIZE_LIMIT')
    app_usage_stats: str = Field(..., alias='_APP_USAGE_STATS')
    app_vcs_enabled: bool = Field(..., alias='_APP_VCS_ENABLED')
    app_vcs_providers: List[Any] = Field(..., alias='_APP_VCS_PROVIDERS')
    app_vcs_providers_with_repository_creation: List[Any] = Field(
        ...,
        alias='_APP_VCS_PROVIDERS_WITH_REPOSITORY_CREATION',
    )
    app_vcs_providers_with_public_repositories: List[Any] = Field(
        ...,
        alias='_APP_VCS_PROVIDERS_WITH_PUBLIC_REPOSITORIES',
    )
    app_domain_enabled: bool = Field(..., alias='_APP_DOMAIN_ENABLED')
    app_domain_sites: str = Field(..., alias='_APP_DOMAIN_SITES')
    app_domain_functions: str = Field(..., alias='_APP_DOMAIN_FUNCTIONS')
    app_options_force_https: str = Field(..., alias='_APP_OPTIONS_FORCE_HTTPS')
    app_domains_nameservers: str = Field(..., alias='_APP_DOMAINS_NAMESERVERS')
    app_db_adapter: str = Field(..., alias='_APP_DB_ADAPTER')
    supportforattributes: bool = Field(..., alias='supportForAttributes')
    supportforrelationships: bool = Field(..., alias='supportForRelationships')
    supportforoperators: bool = Field(..., alias='supportForOperators')
    supportforspatials: bool = Field(..., alias='supportForSpatials')
    supportforaggregations: bool = Field(..., alias='supportForAggregations')
    supportforjoins: bool = Field(..., alias='supportForJoins')
    supportforspatialindexnull: bool = Field(..., alias='supportForSpatialIndexNull')
    supportforfulltextwildcard: bool = Field(..., alias='supportForFulltextWildcard')
    supportformultiplefulltextindexes: bool = Field(..., alias='supportForMultipleFulltextIndexes')
    supportfortrigramindex: bool = Field(..., alias='supportForTrigramIndex')
    supportforattributeresizing: bool = Field(..., alias='supportForAttributeResizing')
    supportforschemas: bool = Field(..., alias='supportForSchemas')
    maxindexlength: float = Field(..., alias='maxIndexLength')
    supportforintegerids: bool = Field(..., alias='supportForIntegerIds')
    app_console_email_verification: str = Field(..., alias='_APP_CONSOLE_EMAIL_VERIFICATION')
    app_domain_email: str = Field(..., alias='_APP_DOMAIN_EMAIL')
    app_domain_target_smtp: str = Field(..., alias='_APP_DOMAIN_TARGET_SMTP')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if '_APP_DOMAIN_TARGET_CNAME' not in data and 'app_domain_target_cname' not in data:
            data['_APP_DOMAIN_TARGET_CNAME'] = ''
        if '_APP_DOMAIN_TARGET_A' not in data and 'app_domain_target_a' not in data:
            data['_APP_DOMAIN_TARGET_A'] = ''
        if '_APP_DOMAIN_TARGET_AAAA' not in data and 'app_domain_target_aaaa' not in data:
            data['_APP_DOMAIN_TARGET_AAAA'] = ''
        if '_APP_DOMAIN_TARGET_CAA' not in data and 'app_domain_target_caa' not in data:
            data['_APP_DOMAIN_TARGET_CAA'] = ''
        if '_APP_USAGE_STATS' not in data and 'app_usage_stats' not in data:
            data['_APP_USAGE_STATS'] = ''
        if '_APP_VCS_ENABLED' not in data and 'app_vcs_enabled' not in data:
            data['_APP_VCS_ENABLED'] = False
        if '_APP_VCS_PROVIDERS' not in data and 'app_vcs_providers' not in data:
            data['_APP_VCS_PROVIDERS'] = []
        if '_APP_VCS_PROVIDERS_WITH_REPOSITORY_CREATION' not in data and 'app_vcs_providers_with_repository_creation' not in data:
            data['_APP_VCS_PROVIDERS_WITH_REPOSITORY_CREATION'] = []
        if '_APP_VCS_PROVIDERS_WITH_PUBLIC_REPOSITORIES' not in data and 'app_vcs_providers_with_public_repositories' not in data:
            data['_APP_VCS_PROVIDERS_WITH_PUBLIC_REPOSITORIES'] = []
        if '_APP_DOMAIN_ENABLED' not in data and 'app_domain_enabled' not in data:
            data['_APP_DOMAIN_ENABLED'] = False
        if '_APP_DOMAIN_SITES' not in data and 'app_domain_sites' not in data:
            data['_APP_DOMAIN_SITES'] = ''
        if '_APP_DOMAIN_FUNCTIONS' not in data and 'app_domain_functions' not in data:
            data['_APP_DOMAIN_FUNCTIONS'] = ''
        if '_APP_OPTIONS_FORCE_HTTPS' not in data and 'app_options_force_https' not in data:
            data['_APP_OPTIONS_FORCE_HTTPS'] = ''
        if '_APP_DOMAINS_NAMESERVERS' not in data and 'app_domains_nameservers' not in data:
            data['_APP_DOMAINS_NAMESERVERS'] = ''
        if '_APP_DB_ADAPTER' not in data and 'app_db_adapter' not in data:
            data['_APP_DB_ADAPTER'] = 'mariadb'
        if 'supportForAttributes' not in data and 'supportforattributes' not in data:
            data['supportForAttributes'] = True
        if 'supportForRelationships' not in data and 'supportforrelationships' not in data:
            data['supportForRelationships'] = True
        if 'supportForOperators' not in data and 'supportforoperators' not in data:
            data['supportForOperators'] = True
        if 'supportForSpatials' not in data and 'supportforspatials' not in data:
            data['supportForSpatials'] = True
        if 'supportForAggregations' not in data and 'supportforaggregations' not in data:
            data['supportForAggregations'] = True
        if 'supportForJoins' not in data and 'supportforjoins' not in data:
            data['supportForJoins'] = True
        if 'supportForSpatialIndexNull' not in data and 'supportforspatialindexnull' not in data:
            data['supportForSpatialIndexNull'] = False
        if 'supportForFulltextWildcard' not in data and 'supportforfulltextwildcard' not in data:
            data['supportForFulltextWildcard'] = True
        if 'supportForMultipleFulltextIndexes' not in data and 'supportformultiplefulltextindexes' not in data:
            data['supportForMultipleFulltextIndexes'] = True
        if 'supportForTrigramIndex' not in data and 'supportfortrigramindex' not in data:
            data['supportForTrigramIndex'] = False
        if 'supportForAttributeResizing' not in data and 'supportforattributeresizing' not in data:
            data['supportForAttributeResizing'] = True
        if 'supportForSchemas' not in data and 'supportforschemas' not in data:
            data['supportForSchemas'] = True
        if 'maxIndexLength' not in data and 'maxindexlength' not in data:
            data['maxIndexLength'] = 768
        if 'supportForIntegerIds' not in data and 'supportforintegerids' not in data:
            data['supportForIntegerIds'] = True
        if '_APP_CONSOLE_EMAIL_VERIFICATION' not in data and 'app_console_email_verification' not in data:
            data['_APP_CONSOLE_EMAIL_VERIFICATION'] = ''
        if '_APP_DOMAIN_EMAIL' not in data and 'app_domain_email' not in data:
            data['_APP_DOMAIN_EMAIL'] = ''
        if '_APP_DOMAIN_TARGET_SMTP' not in data and 'app_domain_target_smtp' not in data:
            data['_APP_DOMAIN_TARGET_SMTP'] = ''
        return data
