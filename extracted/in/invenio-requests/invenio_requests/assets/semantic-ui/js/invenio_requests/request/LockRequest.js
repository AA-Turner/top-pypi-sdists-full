// This file is part of InvenioRequests
// Copyright (C) 2025 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import { Divider, Popup, Icon, Grid } from "semantic-ui-react";
import { RequestLockButton } from "@js/invenio_requests/components/Buttons";
import {
  RequestLinksExtractor,
  InvenioRequestsAPI,
} from "@js/invenio_requests/api/InvenioRequestApi";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_requests/i18next";
import Overridable from "react-overridable";
import Error from "../components/Error";
import { errorSerializer } from "../api/serializers";

export class LockRequestComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      error: null,
    };
  }

  render() {
    const { request, popupComponent, lockHelpText, unlockHelpText } = this.props;
    const { loading, error } = this.state;

    const requestLinksExtractor = new RequestLinksExtractor(request);
    const requestsApi = new InvenioRequestsAPI(requestLinksExtractor);
    const { is_locked: isLocked } = request;

    return (
      <>
        <Divider />
        <Grid columns={2}>
          <Grid.Column floated="left" width={13}>
            <RequestLockButton
              onClick={async () => {
                let response;
                this.setState({ loading: true });
                try {
                  if (isLocked) {
                    response = await requestsApi.unlockRequest();
                  } else {
                    response = await requestsApi.lockRequest();
                  }
                  window.location.reload();
                } catch (error) {
                  this.setState({ error: error, loading: false });
                }
              }}
              className="request-lock-button"
              loading={loading}
              disabled={error !== null}
              content={i18next.t(
                isLocked ? "Unlock conversation" : "Lock conversation"
              )}
              icon={isLocked ? "unlock" : "lock"}
            />
          </Grid.Column>
          <Grid.Column
            floated="right"
            width={3}
            verticalAlign="middle"
            textAlign="center"
          >
            {popupComponent({ content: isLocked ? unlockHelpText : lockHelpText })}
          </Grid.Column>
        </Grid>
        {error && <Error error={errorSerializer(error)} />}
      </>
    );
  }
}

LockRequestComponent.propTypes = {
  request: PropTypes.object.isRequired,
  popupComponent: PropTypes.func,
  lockHelpText: PropTypes.string,
  unlockHelpText: PropTypes.string,
};

LockRequestComponent.defaultProps = {
  popupComponent: (props) => (
    <Popup
      trigger={
        <span role="button" tabIndex="0">
          <Icon name="question circle outline" />
        </span>
      }
      {...props}
    />
  ),
  lockHelpText: i18next.t(
    "Locking the conversation will disallow users with access to add/update comments."
  ),
  unlockHelpText: i18next.t(
    "Unlocking the conversation will allow users with access to add/update comments."
  ),
};

export const LockRequest = Overridable.component(
  "InvenioRequests.LockRequest",
  LockRequestComponent
);
