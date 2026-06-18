/*
 * SPDX-FileCopyrightText: 2022-2025 CERN.
 * SPDX-License-Identifier: MIT
 */

import Overridable from "react-overridable";
import Loader from "../components/Loader";
import RequestActionsPortal from "./actions";
import RequestDetails from "./RequestDetails";
import React, { Component } from "react";
import PropTypes from "prop-types";
import isEmpty from "lodash/isEmpty";

export class Request extends Component {
  componentDidMount() {
    const { initRequest } = this.props;
    initRequest();
  }

  render() {
    const { request, updateRequestAfterAction, userAvatar, permissions, config } =
      this.props;

    return (
      <Overridable id="InvenioRequest.Request.layout">
        <Loader isLoading={isEmpty(request)}>
          <RequestActionsPortal
            request={request}
            actionSuccessCallback={updateRequestAfterAction}
          />
          <RequestDetails
            request={request}
            userAvatar={userAvatar}
            permissions={permissions}
            config={config}
          />
        </Loader>
      </Overridable>
    );
  }
}

Request.propTypes = {
  request: PropTypes.object.isRequired,
  initRequest: PropTypes.func.isRequired,
  updateRequestAfterAction: PropTypes.func.isRequired,
  userAvatar: PropTypes.string,
  permissions: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
};

Request.defaultProps = {
  userAvatar: "",
};

export default Overridable.component("InvenioRequests.Request", Request);
