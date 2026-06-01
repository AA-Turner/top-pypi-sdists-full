// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  InvenioRequestsAPI,
  RequestLinksExtractor,
  InvenioRequestEventsApi,
  RequestEventsLinksExtractor,
} from "./api";
import { Request } from "./request";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { configureStore } from "./store";
import { OverridableContext } from "react-overridable";
import { Provider } from "react-redux";
import { DatasetContext } from "./data";

export class InvenioRequestsApp extends Component {
  constructor(props) {
    super(props);
    const {
      requestsApi,
      requestEventsApi,
      dataset: { request, defaultQueryParams, defaultReplyQueryParams },
    } = this.props;

    const defaultRequestsApi = new InvenioRequestsAPI(
      new RequestLinksExtractor(request)
    );
    const defaultRequestEventsApi = (commentLinks) =>
      new InvenioRequestEventsApi(new RequestEventsLinksExtractor(commentLinks));
    const appConfig = {
      requestsApi: requestsApi || defaultRequestsApi,
      request,
      requestEventsApi: requestEventsApi || defaultRequestEventsApi,
      refreshIntervalMs: 5000,
      defaultQueryParams,
      defaultReplyQueryParams,
    };

    this.store = configureStore(appConfig);
  }

  render() {
    const { overriddenCmps, dataset } = this.props;
    const { userAvatar, permissions, config } = dataset;

    return (
      <OverridableContext.Provider value={overriddenCmps}>
        <Provider store={this.store}>
          <DatasetContext.Provider value={dataset}>
            <Request
              userAvatar={userAvatar}
              permissions={permissions}
              config={config}
            />
          </DatasetContext.Provider>
        </Provider>
      </OverridableContext.Provider>
    );
  }
}

InvenioRequestsApp.propTypes = {
  dataset: PropTypes.object.isRequired,
  requestsApi: PropTypes.object,
  requestEventsApi: PropTypes.object,
  overriddenCmps: PropTypes.object,
};

InvenioRequestsApp.defaultProps = {
  overriddenCmps: {},
  requestsApi: null,
  requestEventsApi: null,
};
