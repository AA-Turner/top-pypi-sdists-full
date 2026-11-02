from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..models.organization_list import OrganizationList
from ..enums.platform import Platform
from ..models.organization import Organization
from ..models.payment_authentication import PaymentAuthentication
from ..models.estimation import Estimation
from ..models.addon_list import AddonList
from ..models.addon import Addon
from ..enums.addon_key import AddonKey
from ..models.addon_price import AddonPrice
from ..models.aggregation_team_list import AggregationTeamList
from ..models.aggregation_team import AggregationTeam
from ..models.billing_address import BillingAddress
from ..models.credit_list import CreditList
from ..models.credit import Credit
from ..models.credit_available import CreditAvailable
from ..models.estimation_delete_organization import EstimationDeleteOrganization
from ..models.estimation_update_plan import EstimationUpdatePlan
from ..models.downgrade_feedback import DowngradeFeedback
from ..models.invoice_list import InvoiceList
from ..models.invoice import Invoice
from ..models.payment_method import PaymentMethod
from ..models.billing_plan import BillingPlan
from ..models.estimation_plan_change import EstimationPlanChange
from ..models.console_region_list import ConsoleRegionList
from ..models.roles import Roles
from ..models.usage_organization import UsageOrganization

T = TypeVar('T')


class Organizations(Service):

    def __init__(self, client) -> None:
        super(Organizations, self).__init__(client)

    def list(
        self,
        queries: Optional[List[str]] = None,
        search: Optional[str] = None,
        total: Optional[bool] = None,
        model_type: Type[T] = dict,
    ) -> OrganizationList[T]:
        """
        Get a list of all the teams in which the current user is a member. You can use the parameters to filter your results.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: name, total, billingPlan, paymentMethodId, backupPaymentMethodId, platform
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        model_type : Type[T], optional
            Pydantic model class for the user-defined data. Defaults to dict for backward compatibility.

        Returns
        -------
        OrganizationList[T]
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations'
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

        return OrganizationList.with_data(response, model_type)

    def create(
        self,
        organization_id: str,
        name: str,
        billing_plan: str,
        payment_method_id: Optional[str] = None,
        billing_address_id: Optional[str] = None,
        invites: Optional[List[str]] = None,
        coupon_id: Optional[str] = None,
        tax_id: Optional[str] = None,
        budget: Optional[float] = None,
        platform: Optional[Platform] = None,
        model_type: Type[T] = dict,
    ) -> Union[
        Organization,
        PaymentAuthentication,
    ]:
        """
        Create a new organization.

        Parameters
        ----------
        organization_id : str
            Organization ID. Choose a custom ID or generate a random ID with `ID.unique()`. Valid chars are a-z, A-Z, 0-9, period, hyphen, and underscore. Can't start with a special char. Max length is 36 chars.
        name : str
            Organization name. Max length: 128 chars.
        billing_plan : str
            Organization billing plan chosen
        payment_method_id : Optional[str]
            Payment method ID. Required for pro plans when trial is not available and user doesn't have default payment method set.
        billing_address_id : Optional[str]
            Unique ID of billing address
        invites : Optional[List[str]]
            Additional member invites
        coupon_id : Optional[str]
            Coupon id
        tax_id : Optional[str]
            Tax Id associated to billing.
        budget : Optional[float]
            Budget limit for additional usage set for the organization
        platform : Optional[Platform]
            Platform type
        model_type : Type[T], optional
            Pydantic model class for the user-defined data. Defaults to dict for backward compatibility.

        Returns
        -------
        Union[Organization, PaymentAuthentication]
            API response as one of the typed response models

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations'
        api_params = {}
        if organization_id is None:
            raise AppwriteException('Missing required parameter: "organization_id"')
        if name is None:
            raise AppwriteException('Missing required parameter: "name"')
        if billing_plan is None:
            raise AppwriteException('Missing required parameter: "billing_plan"')
        api_params['organizationId'] = self._normalize_value(organization_id)
        api_params['name'] = self._normalize_value(name)
        api_params['billingPlan'] = self._normalize_value(billing_plan)
        if payment_method_id is not None:
            api_params['paymentMethodId'] = self._normalize_value(payment_method_id)
        if billing_address_id is not None:
            api_params['billingAddressId'] = self._normalize_value(billing_address_id)
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)
        if coupon_id is not None:
            api_params['couponId'] = self._normalize_value(coupon_id)
        if tax_id is not None:
            api_params['taxId'] = self._normalize_value(tax_id)
        if budget is not None:
            api_params['budget'] = self._normalize_value(budget)
        if platform is not None:
            api_params['platform'] = self._normalize_value(platform)

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

        return self._parse_response(response, model=Organization)

    def estimation_create_organization(
        self,
        billing_plan: str,
        payment_method_id: Optional[str] = None,
        invites: Optional[List[str]] = None,
        coupon_id: Optional[str] = None,
        platform: Optional[Platform] = None,
    ) -> Estimation:
        """
        Get estimation for creating an organization.

        Parameters
        ----------
        billing_plan : str
            Organization billing plan chosen
        payment_method_id : Optional[str]
            Payment method ID. Required for pro plans when trial is not available and user doesn't have default payment method set.
        invites : Optional[List[str]]
            Additional member invites
        coupon_id : Optional[str]
            Coupon id
        platform : Optional[Platform]
            Platform type
        Returns
        -------
        Estimation
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/estimations/create-organization'
        api_params = {}
        if billing_plan is None:
            raise AppwriteException('Missing required parameter: "billing_plan"')
        api_params['billingPlan'] = self._normalize_value(billing_plan)
        if payment_method_id is not None:
            api_params['paymentMethodId'] = self._normalize_value(payment_method_id)
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)
        if coupon_id is not None:
            api_params['couponId'] = self._normalize_value(coupon_id)
        if platform is not None:
            api_params['platform'] = self._normalize_value(platform)

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

        return self._parse_response(response, model=Estimation)

    def delete(
        self,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Delete an organization.

        Parameters
        ----------
        organization_id : str
            Team ID.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def list_addons(
        self,
        organization_id: str,
    ) -> AddonList:
        """
        List all billing addons for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        Returns
        -------
        AddonList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AddonList)

    def create_baa_addon(
        self,
        organization_id: str,
    ) -> Addon:
        """
        Create the BAA billing addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/baa'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

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

        return self._parse_response(response, model=Addon)

    def create_premium_geo_db_addon(
        self,
        organization_id: str,
    ) -> Addon:
        """
        Create a Premium Geo DB addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/premium-geo-db'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

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

        return self._parse_response(response, model=Addon)

    def get_addon(
        self,
        organization_id: str,
        addon_id: str,
    ) -> Addon:
        """
        Get the details of a billing addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        addon_id : str
            Addon ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/{addonId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Addon)

    def delete_addon(
        self,
        organization_id: str,
        addon_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a billing addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        addon_id : str
            Addon ID
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/{addonId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def confirm_addon_payment(
        self,
        organization_id: str,
        addon_id: str,
    ) -> Addon:
        """
        Confirm payment for a billing addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        addon_id : str
            Addon ID
        Returns
        -------
        Addon
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/{addonId}/confirmations'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if addon_id is None or addon_id == '':
            raise AppwriteException('Missing required parameter: "addon_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{addonId}', self._encode_path(addon_id))

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

        return self._parse_response(response, model=Addon)

    def get_addon_price(
        self,
        organization_id: str,
        addon: AddonKey,
    ) -> AddonPrice:
        """
        Get the price details for a billing addon for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        addon : AddonKey
            Addon key identifier (e.g. baa).
        Returns
        -------
        AddonPrice
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/addons/{addon}/price'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if addon is None:
            raise AppwriteException('Missing required parameter: "addon"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{addon}', self._encode_path(addon))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AddonPrice)

    def list_aggregations(
        self,
        organization_id: str,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> AggregationTeamList:
        """
        Get a list of all aggregations for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: teamId, aggregationId, from, to
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        AggregationTeamList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/aggregations'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
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

        return self._parse_response(response, model=AggregationTeamList)

    def get_aggregation(
        self,
        organization_id: str,
        aggregation_id: str,
        limit: Optional[float] = None,
        offset: Optional[float] = None,
    ) -> AggregationTeam:
        """
        Get a specific aggregation using it's aggregation ID.

        Parameters
        ----------
        organization_id : str
            Organization ID
        aggregation_id : str
            Invoice unique ID
        limit : Optional[float]
            Maximum number of project aggregations to return in response. By default will return maximum 5 results. Maximum of 10 results allowed per request.
        offset : Optional[float]
            Offset value. The default value is 0. Use this param to manage pagination.
        Returns
        -------
        AggregationTeam
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/aggregations/{aggregationId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if aggregation_id is None or aggregation_id == '':
            raise AppwriteException('Missing required parameter: "aggregation_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{aggregationId}', self._encode_path(aggregation_id))
        if limit is not None:
            api_params['limit'] = self._normalize_value(limit)
        if offset is not None:
            api_params['offset'] = self._normalize_value(offset)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AggregationTeam)

    def set_billing_address(
        self,
        organization_id: str,
        billing_address_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Set a billing address for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        billing_address_id : str
            Unique ID of billing address
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

        api_path = '/organizations/{organizationId}/billing-address'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_address_id is None:
            raise AppwriteException('Missing required parameter: "billing_address_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['billingAddressId'] = self._normalize_value(billing_address_id)

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

        return Organization.with_data(response, model_type)

    def delete_billing_address(
        self,
        organization_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a team's billing address.

        Parameters
        ----------
        organization_id : str
            Organization ID
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/billing-address'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def get_billing_address(
        self,
        organization_id: str,
        billing_address_id: str,
    ) -> BillingAddress:
        """
        Get a billing address using it's ID.

        Parameters
        ----------
        organization_id : str
            Organization ID
        billing_address_id : str
            Unique ID of billing address
        Returns
        -------
        BillingAddress
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/billing-addresses/{billingAddressId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_address_id is None or billing_address_id == '':
            raise AppwriteException('Missing required parameter: "billing_address_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{billingAddressId}', self._encode_path(billing_address_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=BillingAddress)

    def set_billing_email(
        self,
        organization_id: str,
        billing_email: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Set the current billing email for the organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        billing_email : str
            Billing email for the organization.
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

        api_path = '/organizations/{organizationId}/billing-email'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_email is None:
            raise AppwriteException('Missing required parameter: "billing_email"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['billingEmail'] = self._normalize_value(billing_email)

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

        return Organization.with_data(response, model_type)

    def update_budget(
        self,
        organization_id: str,
        budget: Optional[float],
        alerts: Optional[List[float]] = None,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Update the budget limit for an organization.

        Parameters
        ----------
        organization_id : str
            Organization Unique ID
        budget : Optional[float]
            Budget limit for additional usage set for the organization
        alerts : Optional[List[float]]
            Budget alert limit percentage
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

        api_path = '/organizations/{organizationId}/budget'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['budget'] = self._normalize_value(budget)
        if alerts is not None:
            api_params['alerts'] = self._normalize_value(alerts)

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

        return Organization.with_data(response, model_type)

    def list_credits(
        self,
        organization_id: str,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> CreditList:
        """
        List all credits for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: teamId, couponId, credits, expiration, status
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        CreditList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/credits'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
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

        return self._parse_response(response, model=CreditList)

    def add_credit(
        self,
        organization_id: str,
        coupon_id: str,
    ) -> Credit:
        """
        Add credit to an organization using a coupon.

        Parameters
        ----------
        organization_id : str
            Organization ID
        coupon_id : str
            ID of the coupon
        Returns
        -------
        Credit
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/credits'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if coupon_id is None:
            raise AppwriteException('Missing required parameter: "coupon_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['couponId'] = self._normalize_value(coupon_id)

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

        return self._parse_response(response, model=Credit)

    def get_available_credits(
        self,
        organization_id: str,
    ) -> CreditAvailable:
        """
        Get total available valid credits for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        Returns
        -------
        CreditAvailable
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/credits/available'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=CreditAvailable)

    def get_credit(
        self,
        organization_id: str,
        credit_id: str,
    ) -> Credit:
        """
        Get credit details.

        Parameters
        ----------
        organization_id : str
            Organization ID
        credit_id : str
            Credit Unique ID
        Returns
        -------
        Credit
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/credits/{creditId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if credit_id is None or credit_id == '':
            raise AppwriteException('Missing required parameter: "credit_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{creditId}', self._encode_path(credit_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Credit)

    def estimation_delete_organization(
        self,
        organization_id: str,
    ) -> EstimationDeleteOrganization:
        """
        Get estimation for deleting an organization.

        Parameters
        ----------
        organization_id : str
            Team ID.
        Returns
        -------
        EstimationDeleteOrganization
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/estimations/delete-organization'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

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

        return self._parse_response(response, model=EstimationDeleteOrganization)

    def estimation_update_plan(
        self,
        organization_id: str,
        billing_plan: str,
        invites: Optional[List[str]] = None,
        coupon_id: Optional[str] = None,
    ) -> EstimationUpdatePlan:
        """
        Get estimation for updating the organization plan.

        Parameters
        ----------
        organization_id : str
            Organization ID
        billing_plan : str
            Organization billing plan chosen
        invites : Optional[List[str]]
            Additional member invites
        coupon_id : Optional[str]
            Coupon id
        Returns
        -------
        EstimationUpdatePlan
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/estimations/update-plan'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_plan is None:
            raise AppwriteException('Missing required parameter: "billing_plan"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['billingPlan'] = self._normalize_value(billing_plan)
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)
        if coupon_id is not None:
            api_params['couponId'] = self._normalize_value(coupon_id)

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

        return self._parse_response(response, model=EstimationUpdatePlan)

    def create_downgrade_feedback(
        self,
        organization_id: str,
        reason: str,
        message: str,
        from_plan_id: str,
        to_plan_id: str,
    ) -> DowngradeFeedback:
        """
        Submit feedback about downgrading from a paid plan to a lower tier. This helps the team understand user experience and improve the platform.

        Parameters
        ----------
        organization_id : str
            Organization Unique ID
        reason : str
            Feedback reason
        message : str
            Feedback message
        from_plan_id : str
            Plan downgrading from
        to_plan_id : str
            Plan downgrading to
        Returns
        -------
        DowngradeFeedback
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/feedbacks/downgrade'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if reason is None:
            raise AppwriteException('Missing required parameter: "reason"')
        if message is None:
            raise AppwriteException('Missing required parameter: "message"')
        if from_plan_id is None:
            raise AppwriteException('Missing required parameter: "from_plan_id"')
        if to_plan_id is None:
            raise AppwriteException('Missing required parameter: "to_plan_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['reason'] = self._normalize_value(reason)
        api_params['message'] = self._normalize_value(message)
        api_params['fromPlanId'] = self._normalize_value(from_plan_id)
        api_params['toPlanId'] = self._normalize_value(to_plan_id)

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

        return self._parse_response(response, model=DowngradeFeedback)

    def list_invoices(
        self,
        organization_id: str,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> InvoiceList:
        """
        List all invoices for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: teamId, aggregationId, type, amount, currency, from, to, dueAt, attempts, status, grossAmount
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        InvoiceList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
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

        return self._parse_response(response, model=InvoiceList)

    def get_invoice(
        self,
        organization_id: str,
        invoice_id: str,
    ) -> Invoice:
        """
        Get an invoice by its unique ID.

        Parameters
        ----------
        organization_id : str
            Organization ID
        invoice_id : str
            Invoice unique ID
        Returns
        -------
        Invoice
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices/{invoiceId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if invoice_id is None or invoice_id == '':
            raise AppwriteException('Missing required parameter: "invoice_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{invoiceId}', self._encode_path(invoice_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Invoice)

    def get_invoice_download(
        self,
        organization_id: str,
        invoice_id: str,
    ) -> bytes:
        """
        Download invoice in PDF

        Parameters
        ----------
        organization_id : str
            Organization ID
        invoice_id : str
            Invoice unique ID
        Returns
        -------
        bytes
            Response as bytes

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices/{invoiceId}/download'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if invoice_id is None or invoice_id == '':
            raise AppwriteException('Missing required parameter: "invoice_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{invoiceId}', self._encode_path(invoice_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': '*/*',
            },
            api_params,
        )

        return response

    def create_invoice_payment(
        self,
        organization_id: str,
        invoice_id: str,
        payment_method_id: str,
    ) -> Invoice:
        """
        Initiate payment for failed invoice to pay live from console

        Parameters
        ----------
        organization_id : str
            Organization ID
        invoice_id : str
            Invoice unique ID
        payment_method_id : str
            Payment method ID
        Returns
        -------
        Invoice
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices/{invoiceId}/payments'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if invoice_id is None or invoice_id == '':
            raise AppwriteException('Missing required parameter: "invoice_id"')
        if payment_method_id is None:
            raise AppwriteException('Missing required parameter: "payment_method_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{invoiceId}', self._encode_path(invoice_id))
        api_params['paymentMethodId'] = self._normalize_value(payment_method_id)

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

        return self._parse_response(response, model=Invoice)

    def validate_invoice(
        self,
        organization_id: str,
        invoice_id: str,
    ) -> Invoice:
        """
        Validates the payment linked with the invoice and updates the invoice status if the payment status is changed.

        Parameters
        ----------
        organization_id : str
            Organization ID
        invoice_id : str
            Invoice unique ID
        Returns
        -------
        Invoice
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices/{invoiceId}/status'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if invoice_id is None or invoice_id == '':
            raise AppwriteException('Missing required parameter: "invoice_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{invoiceId}', self._encode_path(invoice_id))

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

        return self._parse_response(response, model=Invoice)

    def get_invoice_view(
        self,
        organization_id: str,
        invoice_id: str,
    ) -> bytes:
        """
        View invoice in PDF

        Parameters
        ----------
        organization_id : str
            Organization ID
        invoice_id : str
            Invoice unique ID
        Returns
        -------
        bytes
            Response as bytes

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/invoices/{invoiceId}/view'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if invoice_id is None or invoice_id == '':
            raise AppwriteException('Missing required parameter: "invoice_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{invoiceId}', self._encode_path(invoice_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': '*/*',
            },
            api_params,
        )

        return response

    def set_default_payment_method(
        self,
        organization_id: str,
        payment_method_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Set a organization's default payment method.

        Parameters
        ----------
        organization_id : str
            Organization ID
        payment_method_id : str
            Unique ID of payment method
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

        api_path = '/organizations/{organizationId}/payment-method'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if payment_method_id is None:
            raise AppwriteException('Missing required parameter: "payment_method_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['paymentMethodId'] = self._normalize_value(payment_method_id)

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

        return Organization.with_data(response, model_type)

    def delete_default_payment_method(
        self,
        organization_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Delete the default payment method for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
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

        api_path = '/organizations/{organizationId}/payment-method'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return Organization.with_data(response, model_type)

    def set_backup_payment_method(
        self,
        organization_id: str,
        payment_method_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Set an organization's backup payment method.

        Parameters
        ----------
        organization_id : str
            Organization ID
        payment_method_id : str
            Unique ID of payment method
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

        api_path = '/organizations/{organizationId}/payment-method/backup'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if payment_method_id is None:
            raise AppwriteException('Missing required parameter: "payment_method_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['paymentMethodId'] = self._normalize_value(payment_method_id)

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

        return Organization.with_data(response, model_type)

    def delete_backup_payment_method(
        self,
        organization_id: str,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Delete a backup payment method for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
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

        api_path = '/organizations/{organizationId}/payment-method/backup'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return Organization.with_data(response, model_type)

    def get_payment_method(
        self,
        organization_id: str,
        payment_method_id: str,
    ) -> PaymentMethod:
        """
        Get an organization's payment method using it's payment method ID.

        Parameters
        ----------
        organization_id : str
            Organization ID
        payment_method_id : str
            Unique ID of payment method
        Returns
        -------
        PaymentMethod
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/payment-methods/{paymentMethodId}'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if payment_method_id is None or payment_method_id == '':
            raise AppwriteException('Missing required parameter: "payment_method_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_path = api_path.replace('{paymentMethodId}', self._encode_path(payment_method_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=PaymentMethod)

    def get_plan(
        self,
        organization_id: str,
    ) -> BillingPlan:
        """
        Get the details of the current billing plan for an organization.

        Parameters
        ----------
        organization_id : str
            Organization Unique ID
        Returns
        -------
        BillingPlan
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/plan'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

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

    def update_plan(
        self,
        organization_id: str,
        billing_plan: str,
        payment_method_id: Optional[str] = None,
        billing_address_id: Optional[str] = None,
        invites: Optional[List[str]] = None,
        coupon_id: Optional[str] = None,
        tax_id: Optional[str] = None,
        budget: Optional[float] = None,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Update the billing plan for an organization.

        Parameters
        ----------
        organization_id : str
            Organization Unique ID
        billing_plan : str
            Organization billing plan chosen
        payment_method_id : Optional[str]
            Payment method ID. Required for pro plans when trial is not available and user doesn't have default payment method set.
        billing_address_id : Optional[str]
            Unique ID of billing address
        invites : Optional[List[str]]
            Additional member invites
        coupon_id : Optional[str]
            Coupon id
        tax_id : Optional[str]
            Tax Id associated to billing.
        budget : Optional[float]
            Budget limit for additional usage set for the organization
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

        api_path = '/organizations/{organizationId}/plan'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_plan is None:
            raise AppwriteException('Missing required parameter: "billing_plan"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['billingPlan'] = self._normalize_value(billing_plan)
        if payment_method_id is not None:
            api_params['paymentMethodId'] = self._normalize_value(payment_method_id)
        if billing_address_id is not None:
            api_params['billingAddressId'] = self._normalize_value(billing_address_id)
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)
        if coupon_id is not None:
            api_params['couponId'] = self._normalize_value(coupon_id)
        if tax_id is not None:
            api_params['taxId'] = self._normalize_value(tax_id)
        if budget is not None:
            api_params['budget'] = self._normalize_value(budget)

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

        return Organization.with_data(response, model_type)

    def create_plan_estimation(
        self,
        organization_id: str,
        billing_plan: str,
        invites: Optional[List[str]] = None,
        coupon_id: Optional[str] = None,
    ) -> EstimationPlanChange:
        """
        Create a billing plan estimation for upgrading or downgrading an organization plan.

        Parameters
        ----------
        organization_id : str
            Organization ID
        billing_plan : str
            Target billing plan
        invites : Optional[List[str]]
            Additional member invites
        coupon_id : Optional[str]
            Coupon id
        Returns
        -------
        EstimationPlanChange
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/plan/estimations'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        if billing_plan is None:
            raise AppwriteException('Missing required parameter: "billing_plan"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['billingPlan'] = self._normalize_value(billing_plan)
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)
        if coupon_id is not None:
            api_params['couponId'] = self._normalize_value(coupon_id)

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

        return self._parse_response(response, model=EstimationPlanChange)

    def list_regions(
        self,
        organization_id: str,
    ) -> ConsoleRegionList:
        """
        Get all available regions for an organization.

        Parameters
        ----------
        organization_id : str
            Team ID.
        Returns
        -------
        ConsoleRegionList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/regions'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))

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

    def get_scopes(
        self,
        organization_id: str,
        project_id: Optional[str] = None,
    ) -> Roles:
        """
        Get Scopes

        Parameters
        ----------
        organization_id : str
            Organization id
        project_id : Optional[str]
            Project id
        Returns
        -------
        Roles
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/roles'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if project_id is not None:
            api_params['projectId'] = self._normalize_value(project_id)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Roles)

    def set_billing_tax_id(
        self,
        organization_id: str,
        tax_id: Optional[str],
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Set an organization's billing tax ID.

        Parameters
        ----------
        organization_id : str
            Organization ID
        tax_id : Optional[str]
            Tax Id associated to billing.
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

        api_path = '/organizations/{organizationId}/taxId'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        api_params['taxId'] = self._normalize_value(tax_id)

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

        return Organization.with_data(response, model_type)

    def get_usage(
        self,
        organization_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> UsageOrganization:
        """
        Get the usage data for an organization.

        Parameters
        ----------
        organization_id : str
            Organization ID
        start_date : Optional[str]
            Starting date for the usage
        end_date : Optional[str]
            End date for the usage
        Returns
        -------
        UsageOrganization
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/organizations/{organizationId}/usage'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if start_date is not None:
            api_params['startDate'] = self._normalize_value(start_date)
        if end_date is not None:
            api_params['endDate'] = self._normalize_value(end_date)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=UsageOrganization)

    def validate_payment(
        self,
        organization_id: str,
        invites: Optional[List[str]] = None,
        model_type: Type[T] = dict,
    ) -> Organization[T]:
        """
        Validate payment for team after creation or upgrade.

        Parameters
        ----------
        organization_id : str
            Organization ID
        invites : Optional[List[str]]
            Additional member invites
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

        api_path = '/organizations/{organizationId}/validate'
        api_params = {}
        if organization_id is None or organization_id == '':
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{organizationId}', self._encode_path(organization_id))
        if invites is not None:
            api_params['invites'] = self._normalize_value(invites)

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

        return Organization.with_data(response, model_type)
