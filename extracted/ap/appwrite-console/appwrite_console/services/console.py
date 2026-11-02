from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..models.campaign import Campaign
from ..models.coupon import Coupon
from ..models.database_list import DatabaseList
from ..models.console_o_auth2_provider_list import ConsoleOAuth2ProviderList
from ..enums.platform import Platform
from ..models.billing_plan_list import BillingPlanList
from ..models.billing_plan import BillingPlan
from ..models.postgres_extension_list import PostgresExtensionList
from ..models.program import Program
from ..models.organization import Organization
from ..models.console_region_list import ConsoleRegionList
from ..enums.console_resource_type import ConsoleResourceType
from ..models.console_key_scope_list import ConsoleKeyScopeList
from ..models.column_list import ColumnList
from ..models.column_index_list import ColumnIndexList
from ..enums.query_suggestion_resource import QuerySuggestionResource
from ..enums.project_email_template_id import ProjectEmailTemplateId
from ..enums.project_email_template_locale import ProjectEmailTemplateLocale
from ..models.email_template import EmailTemplate
from ..models.console_variables import ConsoleVariables

T = TypeVar('T')


class Console(Service):

    def __init__(self, client) -> None:
        super(Console, self).__init__(client)

    def get_campaign(
        self,
        campaign_id: str,
    ) -> Campaign:
        """
        Receive the details of a campaign using its ID.

        Parameters
        ----------
        campaign_id : str
            ID of the campaign
        Returns
        -------
        Campaign
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/campaigns/{campaignId}'
        api_params = {}
        if campaign_id is None or campaign_id == '':
            raise AppwriteException('Missing required parameter: "campaign_id"')
        api_path = api_path.replace('{campaignId}', self._encode_path(campaign_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Campaign)

    def get_coupon(
        self,
        coupon_id: str,
    ) -> Coupon:
        """
        Get the details of a coupon using it's coupon ID.

        Parameters
        ----------
        coupon_id : str
            ID of the coupon
        Returns
        -------
        Coupon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/coupons/{couponId}'
        api_params = {}
        if coupon_id is None or coupon_id == '':
            raise AppwriteException('Missing required parameter: "coupon_id"')
        api_path = api_path.replace('{couponId}', self._encode_path(coupon_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Coupon)

    def list_databases(
        self,
        queries: Optional[List[str]] = None,
        search: Optional[str] = None,
        total: Optional[bool] = None,
    ) -> DatabaseList:
        """
        Get a list of all the project's databases. You can use the query params to filter your results. This returns every database across all types and product APIs in a single call.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: name
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        DatabaseList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/databases'
        api_params = {}
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if search is not None:
            api_params['search'] = self._normalize_value(search)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=DatabaseList)

    def list_o_auth2_providers(
        self,
        total: Optional[bool] = None,
    ) -> ConsoleOAuth2ProviderList:
        """
        List all OAuth2 providers supported by the Appwrite server, along with the parameters required to configure each provider. The response excludes mock providers but includes sandbox providers.

        Parameters
        ----------
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        ConsoleOAuth2ProviderList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/oauth2-providers'
        api_params = {}
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ConsoleOAuth2ProviderList)

    def get_plans(
        self,
        platform: Optional[Platform] = None,
    ) -> BillingPlanList:
        """
        Return a list of all available plans.

        Parameters
        ----------
        platform : Optional[Platform]
            Platform type
        Returns
        -------
        BillingPlanList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/plans'
        api_params = {}
        if platform is not None:
            api_params['platform'] = self._normalize_value(platform)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=BillingPlanList)

    def get_plan(
        self,
        plan_id: str,
    ) -> BillingPlan:
        """
        Get the details of a plan using its plan ID.

        Parameters
        ----------
        plan_id : str
            Plan id
        Returns
        -------
        BillingPlan
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/plans/{planId}'
        api_params = {}
        if plan_id is None or plan_id == '':
            raise AppwriteException('Missing required parameter: "plan_id"')
        api_path = api_path.replace('{planId}', self._encode_path(plan_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=BillingPlan)

    def list_postgres_extensions(
        self,
    ) -> PostgresExtensionList:
        """
        Get the catalog of Postgres extensions that can be installed on a dedicated Postgres database.
        Returns
        -------
        PostgresExtensionList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/postgres-extensions'
        api_params = {}

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=PostgresExtensionList)

    def get_program(
        self,
        program_id: str,
    ) -> Program:
        """
        Receive the details of a program using its ID.

        Parameters
        ----------
        program_id : str
            ID of the program
        Returns
        -------
        Program
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/programs/{programId}'
        api_params = {}
        if program_id is None or program_id == '':
            raise AppwriteException('Missing required parameter: "program_id"')
        api_path = api_path.replace('{programId}', self._encode_path(program_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Program)

    def create_program_membership(
        self,
        program_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Create a new membership for an account to a program.

        Parameters
        ----------
        program_id : str
            ID of the program
        model_type : Type[T], optional
            Pydantic model class for the user-defined data. Defaults to dict for backward compatibility.

        Returns
        -------
        Organization[T]
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/programs/{programId}/memberships'
        api_params = {}
        if program_id is None or program_id == '':
            raise AppwriteException('Missing required parameter: "program_id"')
        api_path = api_path.replace('{programId}', self._encode_path(program_id))

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return Organization.with_data(response, model_type)

    def list_regions(
        self,
    ) -> ConsoleRegionList:
        """
        Get all available regions for the console.
        Returns
        -------
        ConsoleRegionList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/regions'
        api_params = {}

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ConsoleRegionList)

    def get_resource(
        self,
        value: str,
        type: ConsoleResourceType,
    ) -> Dict[str, Any]:
        """
        Check if a resource ID is available.

        Parameters
        ----------
        value : str
            Resource value.
        type : ConsoleResourceType
            Resource type.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/resources'
        api_params = {}
        if value is None:
            raise AppwriteException('Missing required parameter: "value"')
        if type is None:
            raise AppwriteException('Missing required parameter: "type"')
        api_params['value'] = self._normalize_value(value)
        api_params['type'] = self._normalize_value(type)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def list_organization_scopes(
        self,
        total: Optional[bool] = None,
    ) -> ConsoleKeyScopeList:
        """
        List all scopes available for organization API keys, along with a description for each scope.

        Parameters
        ----------
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        ConsoleKeyScopeList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/scopes/organization'
        api_params = {}
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ConsoleKeyScopeList)

    def list_project_scopes(
        self,
        total: Optional[bool] = None,
    ) -> ConsoleKeyScopeList:
        """
        List all scopes available for project API keys, along with a description for each scope.

        Parameters
        ----------
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        ConsoleKeyScopeList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/scopes/project'
        api_params = {}
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ConsoleKeyScopeList)

    def create_source(
        self,
        ref: Optional[str] = None,
        referrer: Optional[str] = None,
        utm_source: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        utm_medium: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new source.

        Parameters
        ----------
        ref : Optional[str]
            Ref param
        referrer : Optional[str]
            Referrer
        utm_source : Optional[str]
            Utm source
        utm_campaign : Optional[str]
            Utm campaign
        utm_medium : Optional[str]
            Utm medium
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/sources'
        api_params = {}
        if ref is not None:
            api_params['ref'] = self._normalize_value(ref)
        if referrer is not None:
            api_params['referrer'] = self._normalize_value(referrer)
        if utm_source is not None:
            api_params['utmSource'] = self._normalize_value(utm_source)
        if utm_campaign is not None:
            api_params['utmCampaign'] = self._normalize_value(utm_campaign)
        if utm_medium is not None:
            api_params['utmMedium'] = self._normalize_value(utm_medium)

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def update_sources(
        self,
        claims: List[str],
    ) -> Dict[str, Any]:
        """
        Link sources captured before sign-up to the current console user. Pass the `claim` values returned when each source was created; invalid claims, sources older than 30 days and sources already linked to a user are ignored.

        Parameters
        ----------
        claims : List[str]
            Source claims, as returned by create source, to link to the current user.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/sources'
        api_params = {}
        if claims is None:
            raise AppwriteException('Missing required parameter: "claims"')
        api_params['claims'] = self._normalize_value(claims)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def suggest_columns(
        self,
        database_id: str,
        table_id: str,
        context: Optional[str] = None,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> ColumnList:
        """
        Suggests column names and their size limits based on the provided table name. The API will also analyze other tables in the same database to provide context-aware suggestions, ensuring consistency across schema design. Users may optionally provide custom context to further refine the suggestions.

        Parameters
        ----------
        database_id : str
            Database ID.
        table_id : str
            Table ID.
        context : Optional[str]
            Optional user provided context to refine suggestions.
        min : Optional[float]
            Minimum number of suggestions to generate.
        max : Optional[float]
            Maximum number of suggestions to generate.
        Returns
        -------
        ColumnList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/suggestions/columns'
        api_params = {}
        if database_id is None:
            raise AppwriteException('Missing required parameter: "database_id"')
        if table_id is None:
            raise AppwriteException('Missing required parameter: "table_id"')
        api_params['databaseId'] = self._normalize_value(database_id)
        api_params['tableId'] = self._normalize_value(table_id)
        if context is not None:
            api_params['context'] = self._normalize_value(context)
        if min is not None:
            api_params['min'] = self._normalize_value(min)
        if max is not None:
            api_params['max'] = self._normalize_value(max)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ColumnList)

    def suggest_indexes(
        self,
        database_id: str,
        table_id: str,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> ColumnIndexList:
        """
        Suggests database indexes for table columns based on the provided table structure and existing columns. The API will also analyze the table's column types, names, and patterns to recommend optimal indexes that improve query performance for common database operations like filtering, sorting, and searching.

        Parameters
        ----------
        database_id : str
            Database ID.
        table_id : str
            Table ID.
        min : Optional[float]
            Minimum number of suggestions to generate.
        max : Optional[float]
            Maximum number of suggestions to generate.
        Returns
        -------
        ColumnIndexList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/suggestions/indexes'
        api_params = {}
        if database_id is None:
            raise AppwriteException('Missing required parameter: "database_id"')
        if table_id is None:
            raise AppwriteException('Missing required parameter: "table_id"')
        api_params['databaseId'] = self._normalize_value(database_id)
        api_params['tableId'] = self._normalize_value(table_id)
        if min is not None:
            api_params['min'] = self._normalize_value(min)
        if max is not None:
            api_params['max'] = self._normalize_value(max)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ColumnIndexList)

    def suggest_queries(
        self,
        resource: QuerySuggestionResource,
        input: str,
        database_id: Optional[str] = None,
        table_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Suggest valid Appwrite query JSON objects for a supported list resource from free-text user intent. The endpoint picks a validator based on `resource` — for system resources it uses the static validator and its allowed attributes, and for user-owned table rows it loads the table schema and validates against those attributes at request time. The returned queries are guaranteed to parse and pass the relevant queries validator.

        Parameters
        ----------
        resource : QuerySuggestionResource
            Resource to generate queries for.
        input : str
            Natural language query intent used to generate filters/sorting/pagination.
        database_id : Optional[str]
            Database ID. Required when resource is `tables` or `rows`.
        table_id : Optional[str]
            Table ID. Required when resource is `rows`.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/suggestions/queries'
        api_params = {}
        if resource is None:
            raise AppwriteException('Missing required parameter: "resource"')
        if input is None:
            raise AppwriteException('Missing required parameter: "input"')
        api_params['resource'] = self._normalize_value(resource)
        api_params['input'] = self._normalize_value(input)
        if database_id is not None:
            api_params['databaseId'] = self._normalize_value(database_id)
        if table_id is not None:
            api_params['tableId'] = self._normalize_value(table_id)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def get_email_template(
        self,
        template_id: ProjectEmailTemplateId,
        locale: Optional[ProjectEmailTemplateLocale] = None,
    ) -> EmailTemplate:
        """
        Get the Appwrite built-in default email template for the specified type and locale. Always returns the unmodified default, ignoring any custom project overrides.

        Parameters
        ----------
        template_id : ProjectEmailTemplateId
            Email template type. Can be one of: verification, magicSession, recovery, invitation, mfaChallenge, sessionAlert, otpSession, otpVerification, otpRecovery
        locale : Optional[ProjectEmailTemplateLocale]
            Template locale. If left empty, the fallback locale (en) will be used.
        Returns
        -------
        EmailTemplate
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/templates/email/{templateId}'
        api_params = {}
        if template_id is None:
            raise AppwriteException('Missing required parameter: "template_id"')
        api_path = api_path.replace('{templateId}', self._encode_path(template_id))
        if locale is not None:
            api_params['locale'] = self._normalize_value(locale)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=EmailTemplate)

    def variables(
        self,
    ) -> ConsoleVariables:
        """
        Get all Environment Variables that are relevant for the console.
        Returns
        -------
        ConsoleVariables
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/console/variables'
        api_params = {}

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ConsoleVariables)
