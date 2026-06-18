/*
 * SPDX-FileCopyrightText: 2022-2023 CERN.
 * SPDX-License-Identifier: MIT
 */

import { RequestActionController } from "@js/invenio_requests/request/actions/RequestActionController";
import PropTypes from "prop-types";
import ReactDOM from "react-dom";
import React from "react";
import Overridable from "react-overridable";

const element = document.getElementById("request-actions");

const RequestActionsPortalCmp = ({ request, actionSuccessCallback }) => {
  return ReactDOM.createPortal(
    <RequestActionController
      request={request}
      actionSuccessCallback={actionSuccessCallback}
      size="medium"
    />,
    element
  );
};

RequestActionsPortalCmp.propTypes = {
  request: PropTypes.object.isRequired,
  actionSuccessCallback: PropTypes.func.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestActionsPortal",
  RequestActionsPortalCmp
);
