"""
Type annotations for pinpoint-sms-voice-v2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pinpoint_sms_voice_v2.client import PinpointSMSVoiceV2Client
    from types_aiobotocore_pinpoint_sms_voice_v2.paginator import (
        DescribeAccountAttributesPaginator,
        DescribeAccountLimitsPaginator,
        DescribeConfigurationSetsPaginator,
        DescribeKeywordsPaginator,
        DescribeOptOutListsPaginator,
        DescribeOptedOutNumbersPaginator,
        DescribePhoneNumbersPaginator,
        DescribePoolsPaginator,
        DescribeProtectConfigurationsPaginator,
        DescribeRegistrationAttachmentsPaginator,
        DescribeRegistrationFieldDefinitionsPaginator,
        DescribeRegistrationFieldValuesPaginator,
        DescribeRegistrationSectionDefinitionsPaginator,
        DescribeRegistrationTypeDefinitionsPaginator,
        DescribeRegistrationVersionsPaginator,
        DescribeRegistrationsPaginator,
        DescribeSenderIdsPaginator,
        DescribeSpendLimitsPaginator,
        DescribeVerifiedDestinationNumbersPaginator,
        ListPoolOriginationIdentitiesPaginator,
        ListProtectConfigurationRuleSetNumberOverridesPaginator,
        ListRegistrationAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("pinpoint-sms-voice-v2") as client:
        client: PinpointSMSVoiceV2Client

        describe_account_attributes_paginator: DescribeAccountAttributesPaginator = client.get_paginator("describe_account_attributes")
        describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
        describe_configuration_sets_paginator: DescribeConfigurationSetsPaginator = client.get_paginator("describe_configuration_sets")
        describe_keywords_paginator: DescribeKeywordsPaginator = client.get_paginator("describe_keywords")
        describe_opt_out_lists_paginator: DescribeOptOutListsPaginator = client.get_paginator("describe_opt_out_lists")
        describe_opted_out_numbers_paginator: DescribeOptedOutNumbersPaginator = client.get_paginator("describe_opted_out_numbers")
        describe_phone_numbers_paginator: DescribePhoneNumbersPaginator = client.get_paginator("describe_phone_numbers")
        describe_pools_paginator: DescribePoolsPaginator = client.get_paginator("describe_pools")
        describe_protect_configurations_paginator: DescribeProtectConfigurationsPaginator = client.get_paginator("describe_protect_configurations")
        describe_registration_attachments_paginator: DescribeRegistrationAttachmentsPaginator = client.get_paginator("describe_registration_attachments")
        describe_registration_field_definitions_paginator: DescribeRegistrationFieldDefinitionsPaginator = client.get_paginator("describe_registration_field_definitions")
        describe_registration_field_values_paginator: DescribeRegistrationFieldValuesPaginator = client.get_paginator("describe_registration_field_values")
        describe_registration_section_definitions_paginator: DescribeRegistrationSectionDefinitionsPaginator = client.get_paginator("describe_registration_section_definitions")
        describe_registration_type_definitions_paginator: DescribeRegistrationTypeDefinitionsPaginator = client.get_paginator("describe_registration_type_definitions")
        describe_registration_versions_paginator: DescribeRegistrationVersionsPaginator = client.get_paginator("describe_registration_versions")
        describe_registrations_paginator: DescribeRegistrationsPaginator = client.get_paginator("describe_registrations")
        describe_sender_ids_paginator: DescribeSenderIdsPaginator = client.get_paginator("describe_sender_ids")
        describe_spend_limits_paginator: DescribeSpendLimitsPaginator = client.get_paginator("describe_spend_limits")
        describe_verified_destination_numbers_paginator: DescribeVerifiedDestinationNumbersPaginator = client.get_paginator("describe_verified_destination_numbers")
        list_pool_origination_identities_paginator: ListPoolOriginationIdentitiesPaginator = client.get_paginator("list_pool_origination_identities")
        list_protect_configuration_rule_set_number_overrides_paginator: ListProtectConfigurationRuleSetNumberOverridesPaginator = client.get_paginator("list_protect_configuration_rule_set_number_overrides")
        list_registration_associations_paginator: ListRegistrationAssociationsPaginator = client.get_paginator("list_registration_associations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAccountAttributesRequestPaginateTypeDef,
    DescribeAccountAttributesResultTypeDef,
    DescribeAccountLimitsRequestPaginateTypeDef,
    DescribeAccountLimitsResultTypeDef,
    DescribeConfigurationSetsRequestPaginateTypeDef,
    DescribeConfigurationSetsResultTypeDef,
    DescribeKeywordsRequestPaginateTypeDef,
    DescribeKeywordsResultTypeDef,
    DescribeOptedOutNumbersRequestPaginateTypeDef,
    DescribeOptedOutNumbersResultTypeDef,
    DescribeOptOutListsRequestPaginateTypeDef,
    DescribeOptOutListsResultTypeDef,
    DescribePhoneNumbersRequestPaginateTypeDef,
    DescribePhoneNumbersResultTypeDef,
    DescribePoolsRequestPaginateTypeDef,
    DescribePoolsResultTypeDef,
    DescribeProtectConfigurationsRequestPaginateTypeDef,
    DescribeProtectConfigurationsResultTypeDef,
    DescribeRegistrationAttachmentsRequestPaginateTypeDef,
    DescribeRegistrationAttachmentsResultTypeDef,
    DescribeRegistrationFieldDefinitionsRequestPaginateTypeDef,
    DescribeRegistrationFieldDefinitionsResultTypeDef,
    DescribeRegistrationFieldValuesRequestPaginateTypeDef,
    DescribeRegistrationFieldValuesResultTypeDef,
    DescribeRegistrationSectionDefinitionsRequestPaginateTypeDef,
    DescribeRegistrationSectionDefinitionsResultTypeDef,
    DescribeRegistrationsRequestPaginateTypeDef,
    DescribeRegistrationsResultTypeDef,
    DescribeRegistrationTypeDefinitionsRequestPaginateTypeDef,
    DescribeRegistrationTypeDefinitionsResultTypeDef,
    DescribeRegistrationVersionsRequestPaginateTypeDef,
    DescribeRegistrationVersionsResultTypeDef,
    DescribeSenderIdsRequestPaginateTypeDef,
    DescribeSenderIdsResultTypeDef,
    DescribeSpendLimitsRequestPaginateTypeDef,
    DescribeSpendLimitsResultTypeDef,
    DescribeVerifiedDestinationNumbersRequestPaginateTypeDef,
    DescribeVerifiedDestinationNumbersResultTypeDef,
    ListPoolOriginationIdentitiesRequestPaginateTypeDef,
    ListPoolOriginationIdentitiesResultTypeDef,
    ListProtectConfigurationRuleSetNumberOverridesRequestPaginateTypeDef,
    ListProtectConfigurationRuleSetNumberOverridesResultTypeDef,
    ListRegistrationAssociationsRequestPaginateTypeDef,
    ListRegistrationAssociationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountAttributesPaginator",
    "DescribeAccountLimitsPaginator",
    "DescribeConfigurationSetsPaginator",
    "DescribeKeywordsPaginator",
    "DescribeOptOutListsPaginator",
    "DescribeOptedOutNumbersPaginator",
    "DescribePhoneNumbersPaginator",
    "DescribePoolsPaginator",
    "DescribeProtectConfigurationsPaginator",
    "DescribeRegistrationAttachmentsPaginator",
    "DescribeRegistrationFieldDefinitionsPaginator",
    "DescribeRegistrationFieldValuesPaginator",
    "DescribeRegistrationSectionDefinitionsPaginator",
    "DescribeRegistrationTypeDefinitionsPaginator",
    "DescribeRegistrationVersionsPaginator",
    "DescribeRegistrationsPaginator",
    "DescribeSenderIdsPaginator",
    "DescribeSpendLimitsPaginator",
    "DescribeVerifiedDestinationNumbersPaginator",
    "ListPoolOriginationIdentitiesPaginator",
    "ListProtectConfigurationRuleSetNumberOverridesPaginator",
    "ListRegistrationAssociationsPaginator",
)


if TYPE_CHECKING:
    _DescribeAccountAttributesPaginatorBase = AioPaginator[DescribeAccountAttributesResultTypeDef]
else:
    _DescribeAccountAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAccountAttributesPaginator(_DescribeAccountAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountAttributes.html#PinpointSMSVoiceV2.Paginator.DescribeAccountAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeaccountattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccountAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccountAttributesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountAttributes.html#PinpointSMSVoiceV2.Paginator.DescribeAccountAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeaccountattributespaginator)
        """


if TYPE_CHECKING:
    _DescribeAccountLimitsPaginatorBase = AioPaginator[DescribeAccountLimitsResultTypeDef]
else:
    _DescribeAccountLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAccountLimitsPaginator(_DescribeAccountLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountLimits.html#PinpointSMSVoiceV2.Paginator.DescribeAccountLimits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeaccountlimitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccountLimitsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccountLimitsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeAccountLimits.html#PinpointSMSVoiceV2.Paginator.DescribeAccountLimits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeaccountlimitspaginator)
        """


if TYPE_CHECKING:
    _DescribeConfigurationSetsPaginatorBase = AioPaginator[DescribeConfigurationSetsResultTypeDef]
else:
    _DescribeConfigurationSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeConfigurationSetsPaginator(_DescribeConfigurationSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeConfigurationSets.html#PinpointSMSVoiceV2.Paginator.DescribeConfigurationSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeconfigurationsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConfigurationSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeConfigurationSetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeConfigurationSets.html#PinpointSMSVoiceV2.Paginator.DescribeConfigurationSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeconfigurationsetspaginator)
        """


if TYPE_CHECKING:
    _DescribeKeywordsPaginatorBase = AioPaginator[DescribeKeywordsResultTypeDef]
else:
    _DescribeKeywordsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeKeywordsPaginator(_DescribeKeywordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeKeywords.html#PinpointSMSVoiceV2.Paginator.DescribeKeywords)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describekeywordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeKeywordsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeKeywordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeKeywords.html#PinpointSMSVoiceV2.Paginator.DescribeKeywords.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describekeywordspaginator)
        """


if TYPE_CHECKING:
    _DescribeOptOutListsPaginatorBase = AioPaginator[DescribeOptOutListsResultTypeDef]
else:
    _DescribeOptOutListsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOptOutListsPaginator(_DescribeOptOutListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptOutLists.html#PinpointSMSVoiceV2.Paginator.DescribeOptOutLists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeoptoutlistspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOptOutListsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeOptOutListsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptOutLists.html#PinpointSMSVoiceV2.Paginator.DescribeOptOutLists.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeoptoutlistspaginator)
        """


if TYPE_CHECKING:
    _DescribeOptedOutNumbersPaginatorBase = AioPaginator[DescribeOptedOutNumbersResultTypeDef]
else:
    _DescribeOptedOutNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOptedOutNumbersPaginator(_DescribeOptedOutNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptedOutNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeOptedOutNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeoptedoutnumberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOptedOutNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeOptedOutNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeOptedOutNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeOptedOutNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeoptedoutnumberspaginator)
        """


if TYPE_CHECKING:
    _DescribePhoneNumbersPaginatorBase = AioPaginator[DescribePhoneNumbersResultTypeDef]
else:
    _DescribePhoneNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePhoneNumbersPaginator(_DescribePhoneNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePhoneNumbers.html#PinpointSMSVoiceV2.Paginator.DescribePhoneNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describephonenumberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePhoneNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribePhoneNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePhoneNumbers.html#PinpointSMSVoiceV2.Paginator.DescribePhoneNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describephonenumberspaginator)
        """


if TYPE_CHECKING:
    _DescribePoolsPaginatorBase = AioPaginator[DescribePoolsResultTypeDef]
else:
    _DescribePoolsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePoolsPaginator(_DescribePoolsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePools.html#PinpointSMSVoiceV2.Paginator.DescribePools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describepoolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePoolsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribePools.html#PinpointSMSVoiceV2.Paginator.DescribePools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describepoolspaginator)
        """


if TYPE_CHECKING:
    _DescribeProtectConfigurationsPaginatorBase = AioPaginator[
        DescribeProtectConfigurationsResultTypeDef
    ]
else:
    _DescribeProtectConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeProtectConfigurationsPaginator(_DescribeProtectConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeProtectConfigurations.html#PinpointSMSVoiceV2.Paginator.DescribeProtectConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeprotectconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProtectConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeProtectConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeProtectConfigurations.html#PinpointSMSVoiceV2.Paginator.DescribeProtectConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeprotectconfigurationspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationAttachmentsPaginatorBase = AioPaginator[
        DescribeRegistrationAttachmentsResultTypeDef
    ]
else:
    _DescribeRegistrationAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationAttachmentsPaginator(_DescribeRegistrationAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationAttachments.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationAttachments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationAttachments.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationAttachments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationattachmentspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationFieldDefinitionsPaginatorBase = AioPaginator[
        DescribeRegistrationFieldDefinitionsResultTypeDef
    ]
else:
    _DescribeRegistrationFieldDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationFieldDefinitionsPaginator(
    _DescribeRegistrationFieldDefinitionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationfielddefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationFieldDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationFieldDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationfielddefinitionspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationFieldValuesPaginatorBase = AioPaginator[
        DescribeRegistrationFieldValuesResultTypeDef
    ]
else:
    _DescribeRegistrationFieldValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationFieldValuesPaginator(_DescribeRegistrationFieldValuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldValues.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldValues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationfieldvaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationFieldValuesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationFieldValuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationFieldValues.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationFieldValues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationfieldvaluespaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationSectionDefinitionsPaginatorBase = AioPaginator[
        DescribeRegistrationSectionDefinitionsResultTypeDef
    ]
else:
    _DescribeRegistrationSectionDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationSectionDefinitionsPaginator(
    _DescribeRegistrationSectionDefinitionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationSectionDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationSectionDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationsectiondefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationSectionDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationSectionDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationSectionDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationSectionDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationsectiondefinitionspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationTypeDefinitionsPaginatorBase = AioPaginator[
        DescribeRegistrationTypeDefinitionsResultTypeDef
    ]
else:
    _DescribeRegistrationTypeDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationTypeDefinitionsPaginator(
    _DescribeRegistrationTypeDefinitionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationTypeDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationTypeDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationtypedefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationTypeDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationTypeDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationTypeDefinitions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationTypeDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationtypedefinitionspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationVersionsPaginatorBase = AioPaginator[
        DescribeRegistrationVersionsResultTypeDef
    ]
else:
    _DescribeRegistrationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationVersionsPaginator(_DescribeRegistrationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationVersions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrationVersions.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrationVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeRegistrationsPaginatorBase = AioPaginator[DescribeRegistrationsResultTypeDef]
else:
    _DescribeRegistrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRegistrationsPaginator(_DescribeRegistrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrations.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistrationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeRegistrations.html#PinpointSMSVoiceV2.Paginator.DescribeRegistrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeregistrationspaginator)
        """


if TYPE_CHECKING:
    _DescribeSenderIdsPaginatorBase = AioPaginator[DescribeSenderIdsResultTypeDef]
else:
    _DescribeSenderIdsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSenderIdsPaginator(_DescribeSenderIdsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSenderIds.html#PinpointSMSVoiceV2.Paginator.DescribeSenderIds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describesenderidspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSenderIdsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSenderIdsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSenderIds.html#PinpointSMSVoiceV2.Paginator.DescribeSenderIds.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describesenderidspaginator)
        """


if TYPE_CHECKING:
    _DescribeSpendLimitsPaginatorBase = AioPaginator[DescribeSpendLimitsResultTypeDef]
else:
    _DescribeSpendLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSpendLimitsPaginator(_DescribeSpendLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSpendLimits.html#PinpointSMSVoiceV2.Paginator.DescribeSpendLimits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describespendlimitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSpendLimitsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSpendLimitsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeSpendLimits.html#PinpointSMSVoiceV2.Paginator.DescribeSpendLimits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describespendlimitspaginator)
        """


if TYPE_CHECKING:
    _DescribeVerifiedDestinationNumbersPaginatorBase = AioPaginator[
        DescribeVerifiedDestinationNumbersResultTypeDef
    ]
else:
    _DescribeVerifiedDestinationNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeVerifiedDestinationNumbersPaginator(_DescribeVerifiedDestinationNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeVerifiedDestinationNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeVerifiedDestinationNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeverifieddestinationnumberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVerifiedDestinationNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeVerifiedDestinationNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/DescribeVerifiedDestinationNumbers.html#PinpointSMSVoiceV2.Paginator.DescribeVerifiedDestinationNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#describeverifieddestinationnumberspaginator)
        """


if TYPE_CHECKING:
    _ListPoolOriginationIdentitiesPaginatorBase = AioPaginator[
        ListPoolOriginationIdentitiesResultTypeDef
    ]
else:
    _ListPoolOriginationIdentitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPoolOriginationIdentitiesPaginator(_ListPoolOriginationIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListPoolOriginationIdentities.html#PinpointSMSVoiceV2.Paginator.ListPoolOriginationIdentities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listpooloriginationidentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoolOriginationIdentitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoolOriginationIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListPoolOriginationIdentities.html#PinpointSMSVoiceV2.Paginator.ListPoolOriginationIdentities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listpooloriginationidentitiespaginator)
        """


if TYPE_CHECKING:
    _ListProtectConfigurationRuleSetNumberOverridesPaginatorBase = AioPaginator[
        ListProtectConfigurationRuleSetNumberOverridesResultTypeDef
    ]
else:
    _ListProtectConfigurationRuleSetNumberOverridesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProtectConfigurationRuleSetNumberOverridesPaginator(
    _ListProtectConfigurationRuleSetNumberOverridesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListProtectConfigurationRuleSetNumberOverrides.html#PinpointSMSVoiceV2.Paginator.ListProtectConfigurationRuleSetNumberOverrides)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listprotectconfigurationrulesetnumberoverridespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectConfigurationRuleSetNumberOverridesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProtectConfigurationRuleSetNumberOverridesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListProtectConfigurationRuleSetNumberOverrides.html#PinpointSMSVoiceV2.Paginator.ListProtectConfigurationRuleSetNumberOverrides.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listprotectconfigurationrulesetnumberoverridespaginator)
        """


if TYPE_CHECKING:
    _ListRegistrationAssociationsPaginatorBase = AioPaginator[
        ListRegistrationAssociationsResultTypeDef
    ]
else:
    _ListRegistrationAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegistrationAssociationsPaginator(_ListRegistrationAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListRegistrationAssociations.html#PinpointSMSVoiceV2.Paginator.ListRegistrationAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listregistrationassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistrationAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegistrationAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-sms-voice-v2/paginator/ListRegistrationAssociations.html#PinpointSMSVoiceV2.Paginator.ListRegistrationAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_sms_voice_v2/paginators/#listregistrationassociationspaginator)
        """
