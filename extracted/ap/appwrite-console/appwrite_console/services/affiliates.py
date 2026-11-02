from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..models.affiliate_link_list import AffiliateLinkList
from ..models.affiliate_link import AffiliateLink
from ..models.affiliate_referral_list import AffiliateReferralList
from ..models.affiliate_reward_list import AffiliateRewardList
from ..models.affiliate_reward import AffiliateReward


class Affiliates(Service):

    def __init__(self, client) -> None:
        super(Affiliates, self).__init__(client)

    def list_links(
        self,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> AffiliateLinkList:
        """
        List affiliate links for the current account.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: name, status
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        AffiliateLinkList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/links'
        api_params = {}
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

        return self._parse_response(response, model=AffiliateLinkList)

    def create_link(
        self,
        link_id: str,
        name: Optional[str] = None,
    ) -> AffiliateLink:
        """
        Create a shareable affiliate link for the current account. Every console user is automatically in the affiliates program.

        Parameters
        ----------
        link_id : str
            Link ID. Choose a custom ID or generate a random ID with `ID.unique()`. Valid chars are a-z, A-Z, 0-9, period, hyphen, and underscore. Can't start with a special char. Max length is 36 chars. This ID is the shareable referral code.
        name : Optional[str]
            Link name. Max length: 128 chars.
        Returns
        -------
        AffiliateLink
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/links'
        api_params = {}
        if link_id is None:
            raise AppwriteException('Missing required parameter: "link_id"')
        api_params['linkId'] = self._normalize_value(link_id)
        if name is not None:
            api_params['name'] = self._normalize_value(name)

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

        return self._parse_response(response, model=AffiliateLink)

    def get_link(
        self,
        link_id: str,
    ) -> AffiliateLink:
        """
        Get a single affiliate link owned by the current account.

        Parameters
        ----------
        link_id : str
            Link ID.
        Returns
        -------
        AffiliateLink
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/links/{linkId}'
        api_params = {}
        if link_id is None or link_id == '':
            raise AppwriteException('Missing required parameter: "link_id"')
        api_path = api_path.replace('{linkId}', self._encode_path(link_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=AffiliateLink)

    def delete_link(
        self,
        link_id: str,
    ) -> Dict[str, Any]:
        """
        Delete an affiliate link owned by the current account. Existing referrals and rewards keep their stored link IDs for history.

        Parameters
        ----------
        link_id : str
            Link ID.
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/links/{linkId}'
        api_params = {}
        if link_id is None or link_id == '':
            raise AppwriteException('Missing required parameter: "link_id"')
        api_path = api_path.replace('{linkId}', self._encode_path(link_id))

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

    def list_referrals(
        self,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> AffiliateReferralList:
        """
        List referrals attributed to the current account's affiliate links. Responses include privacy-safe metadata only (truncated user ID and signup country), never email or name. Referrals are created automatically on signup when the invite cookie is present.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: linkId, referredUserMaskedId, referredUserCountry, status, attributedAt, expiresAt, convertedAt
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        AffiliateReferralList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/referrals'
        api_params = {}
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

        return self._parse_response(response, model=AffiliateReferralList)

    def list_rewards(
        self,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> AffiliateRewardList:
        """
        List rewards earned by the current account from affiliate link conversions.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/databases#querying-documents). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: linkId, referralId, amount, status, teamId, creditId
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        AffiliateRewardList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/rewards'
        api_params = {}
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

        return self._parse_response(response, model=AffiliateRewardList)

    def update_reward(
        self,
        reward_id: str,
        status: str,
        organization_id: str,
    ) -> AffiliateReward:
        """
        Claim a pending affiliate reward by setting its status to `claimed`. Creates organization credits for the target organization. The current user must be an owner of that organization.

        Parameters
        ----------
        reward_id : str
            Reward ID
        status : str
            New reward status. Use `claimed` to claim the reward as organization credits.
        organization_id : str
            Organization ID to apply credits to when claiming.
        Returns
        -------
        AffiliateReward
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/affiliates/rewards/{rewardId}'
        api_params = {}
        if reward_id is None or reward_id == '':
            raise AppwriteException('Missing required parameter: "reward_id"')
        if status is None:
            raise AppwriteException('Missing required parameter: "status"')
        if organization_id is None:
            raise AppwriteException('Missing required parameter: "organization_id"')
        api_path = api_path.replace('{rewardId}', self._encode_path(reward_id))
        api_params['status'] = self._normalize_value(status)
        api_params['organizationId'] = self._normalize_value(organization_id)

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

        return self._parse_response(response, model=AffiliateReward)
