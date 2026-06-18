/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import React from "react";
import { Icon } from "semantic-ui-react";
import { i18next } from "@translations/invenio_requests/i18next";

export const SubmitStatus = () => (
  <div>
    <Icon name="clock outline" />
    <span>{i18next.t("Submitted")}</span>
  </div>
);

export const DeleteStatus = () => (
  <div>
    <Icon name="trash" />
    <span>{i18next.t("Deleted")}</span>
  </div>
);

export const AcceptStatus = () => (
  <div>
    <Icon name="check circle" />
    <span>{i18next.t("Accepted")}</span>
  </div>
);

export const DeclineStatus = () => (
  <div>
    <Icon name="times" />
    <span>{i18next.t("Declined")}</span>
  </div>
);

export const CancelStatus = () => (
  <div>
    <Icon name="stop" />
    <span>{i18next.t("Cancelled")}</span>
  </div>
);

export const ExpireStatus = () => (
  <div>
    <Icon name="calendar times outline" />
    <span>{i18next.t("Expired")}</span>
  </div>
);
