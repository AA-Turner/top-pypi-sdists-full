/*
 * SPDX-FileCopyrightText: 2022-2026 CERN.
 * SPDX-FileCopyrightText: 2024 Northwestern University.
 * SPDX-License-Identifier: MIT
 */

import { i18next } from "@translations/invenio_requests/i18next";
import React from "react";
import { Label } from "semantic-ui-react";

export const LabelTypeCommunitySubmission = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Draft review")}
  </Label>
);

export const LabelTypeCommunityInclusion = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Community inclusion")}
  </Label>
);

export const LabelTypeCommunityInvitation = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Member invitation")}
  </Label>
);

export const LabelTypeGuestAccess = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Guest access")}
  </Label>
);

export const LabelTypeUserAccess = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("User access")}
  </Label>
);

export const LabelTypeCommunityManageRecord = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Community manage record")}
  </Label>
);

export const LabelTypeCommunitySubcommunity = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Subcommunity")}
  </Label>
);

export const LabelTypeCommunitySubcommunityInvitation = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Subcommunity invitation")}
  </Label>
);

export const LabelTypeCommunityMembershipRequest = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Membership request")}
  </Label>
);

export const LabelTypeRecordDeletion = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Record deletion")}
  </Label>
);

export const LabelTypeFileModification = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("File modification")}
  </Label>
);

export const LabelTypeQuotaIncrease = (props) => (
  <Label horizontal className="primary theme-secondary" size="small">
    {i18next.t("Quota increase")}
  </Label>
);
