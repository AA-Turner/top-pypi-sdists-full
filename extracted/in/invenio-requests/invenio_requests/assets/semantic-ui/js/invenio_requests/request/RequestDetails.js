/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import RequestMetadata from "./RequestMetadata";
import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Grid } from "semantic-ui-react";
import { Timeline } from "../timelineParent";

class RequestDetails extends Component {
  render() {
    const { request, userAvatar, permissions, config } = this.props;
    return (
      <Overridable id="InvenioRequests.RequestDetails.layout" {...this.props}>
        <Grid stackable reversed="mobile">
          <Grid.Column mobile={16} tablet={12} computer={13}>
            <Timeline
              userAvatar={userAvatar}
              request={request}
              permissions={permissions}
            />
          </Grid.Column>
          <Grid.Column mobile={16} tablet={4} computer={3}>
            <RequestMetadata
              request={request}
              permissions={permissions}
              config={config}
            />
          </Grid.Column>
        </Grid>
      </Overridable>
    );
  }
}

RequestDetails.propTypes = {
  request: PropTypes.object.isRequired,
  userAvatar: PropTypes.string,
  permissions: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
};

RequestDetails.defaultProps = {
  userAvatar: "",
};

export default Overridable.component("InvenioRequests.RequestDetails", RequestDetails);
