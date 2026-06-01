// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { RequestLinksExtractor, InvenioRequestsAPI } from "@js/invenio_requests/api";
import { errorSerializer } from "@js/invenio_requests/api/serializers";
import { RequestActions } from "@js/invenio_requests/request/actions/RequestActions";
import PropTypes from "prop-types";
import { RequestActionContext } from "./context";
import React, { Component } from "react";

export class RequestActionController extends Component {
  constructor(props) {
    super(props);
    const { request, requestApi } = props;
    this.linkExtractor = new RequestLinksExtractor(request);
    this.requestApi = requestApi || new InvenioRequestsAPI(this.linkExtractor);
    this.state = { modalOpen: {}, loading: false, error: undefined };
  }

  toggleActionModal = (actionId, val) => {
    const { modalOpen } = this.state;
    if (val) {
      modalOpen[actionId] = val;
    } else {
      modalOpen[actionId] = !modalOpen[actionId];
    }
    this.setState({ modalOpen: { ...modalOpen } });
  };

  performAction = async (action, commentContent) => {
    this.setState({ loading: true });
    const { actionSuccessCallback } = this.props;
    try {
      const response = await this.requestApi.performAction(action, commentContent);
      this.setState({ loading: false });
      this.toggleActionModal(action, false);
      actionSuccessCallback(response.data);
    } catch (error) {
      console.error(error);
      this.setState({ loading: false, error: errorSerializer(error) });
    }
  };

  cleanError = () => {
    this.setState({ error: undefined });
  };

  render() {
    const { modalOpen, error, loading } = this.state;
    const { request, children, size } = this.props;

    return (
      <RequestActionContext.Provider
        value={{
          modalOpen: modalOpen,
          toggleModal: this.toggleActionModal,
          linkExtractor: this.linkExtractor,
          requestApi: this.requestApi,
          performAction: this.performAction,
          cleanError: this.cleanError,
          error: error,
          loading: loading,
        }}
      >
        <RequestActions request={request} size={size} />
        {children}
      </RequestActionContext.Provider>
    );
  }
}

RequestActionController.propTypes = {
  request: PropTypes.object.isRequired,
  requestApi: PropTypes.instanceOf(InvenioRequestsAPI),
  actionSuccessCallback: PropTypes.func,
  size: PropTypes.string,
  children: PropTypes.node,
};

RequestActionController.defaultProps = {
  requestApi: null,
  actionSuccessCallback: () => {},
  size: "medium",
  children: null,
};
