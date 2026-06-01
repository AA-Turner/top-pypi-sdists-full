// This file is part of Invenio Requests
// Copyright (C) 2024-2026 CERN.
//
// Invenio is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  LabelStatusAccept,
  LabelStatusCancel,
  LabelStatusDecline,
  LabelStatusDelete,
  LabelStatusExpire,
  LabelStatusSubmit,
  LabelTypeCommunityInclusion,
  LabelTypeCommunityInvitation,
  LabelTypeCommunitySubmission,
  LabelTypeGuestAccess,
  LabelTypeUserAccess,
  LabelTypeCommunityManageRecord,
  LabelTypeCommunitySubcommunity,
  LabelTypeCommunitySubcommunityInvitation,
  LabelTypeCommunityMembershipRequest,
  LabelTypeRecordDeletion,
  LabelTypeFileModification,
  LabelTypeQuotaIncrease,
} from "@js/invenio_requests/contrib";
import {
  RequestAcceptButton,
  RequestCancelButton,
  RequestDeclineButton,
  RequestSubmitButton,
} from "@js/invenio_requests/components/Buttons";
import {
  RequestAcceptModalTrigger,
  RequestDeclineModalTrigger,
  RequestCancelModalTrigger,
  RequestSubmitModalTrigger,
} from "@js/invenio_requests/components/ModalTriggers";
import {
  AccessRequestIcon,
  CommunityInclusionIcon,
  CommunityInvitationIcon,
} from "./Icons";

export const defaultContribComponents = {
  [`RequestTypeLabel.layout.community-submission`]: LabelTypeCommunitySubmission,
  [`RequestTypeLabel.layout.community-inclusion`]: LabelTypeCommunityInclusion,
  [`RequestTypeLabel.layout.community-invitation`]: LabelTypeCommunityInvitation,
  [`RequestTypeLabel.layout.guest-access-request`]: LabelTypeGuestAccess,
  [`RequestTypeLabel.layout.user-access-request`]: LabelTypeUserAccess,
  [`RequestTypeLabel.layout.community-manage-record`]: LabelTypeCommunityManageRecord,
  [`RequestTypeLabel.layout.subcommunity`]: LabelTypeCommunitySubcommunity,
  [`RequestTypeLabel.layout.subcommunity-invitation`]:
    LabelTypeCommunitySubcommunityInvitation,
  [`RequestTypeLabel.layout.community-membership-request`]:
    LabelTypeCommunityMembershipRequest,
  [`RequestTypeLabel.layout.record-deletion`]: LabelTypeRecordDeletion,
  [`RequestTypeLabel.layout.file-modification`]: LabelTypeFileModification,
  [`RequestTypeLabel.layout.quota-increase`]: LabelTypeQuotaIncrease,
  [`RequestStatusLabel.layout.submitted`]: LabelStatusSubmit,
  [`RequestStatusLabel.layout.deleted`]: LabelStatusDelete,
  [`RequestStatusLabel.layout.accepted`]: LabelStatusAccept,
  [`RequestStatusLabel.layout.declined`]: LabelStatusDecline,
  [`RequestStatusLabel.layout.cancelled`]: LabelStatusCancel,
  [`RequestStatusLabel.layout.expired`]: LabelStatusExpire,
  [`RequestActionButton.cancel`]: RequestCancelButton,
  [`RequestActionButton.decline`]: RequestDeclineButton,
  [`RequestActionButton.submit`]: RequestSubmitButton,
  [`RequestActionButton.accept`]: RequestAcceptButton,
  [`RequestActionModalTrigger.accept`]: RequestAcceptModalTrigger,
  [`RequestActionModalTrigger.decline`]: RequestDeclineModalTrigger,
  [`RequestActionModalTrigger.cancel`]: RequestCancelModalTrigger,
  [`RequestActionModalTrigger.submit`]: RequestSubmitModalTrigger,
  [`InvenioRequests.RequestTypeIcon.layout.guest-access-request`]: AccessRequestIcon,
  [`InvenioRequests.RequestTypeIcon.layout.user-access-request`]: AccessRequestIcon,
  [`InvenioRequests.RequestTypeIcon.layout.community-inclusion`]:
    CommunityInclusionIcon,
  [`InvenioRequests.RequestTypeIcon.layout.community-submission`]:
    CommunityInclusionIcon,
  [`InvenioRequests.RequestTypeIcon.layout.community-invitation`]:
    CommunityInvitationIcon,
};

export * from "./labels";
export * from "./Icons";
