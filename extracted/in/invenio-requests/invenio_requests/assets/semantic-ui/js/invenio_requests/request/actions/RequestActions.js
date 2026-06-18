/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import { RequestLinksExtractor } from "../../api";
import React from "react";
import Overridable from "react-overridable";
import { RequestAction } from "./RequestAction";
import { Dropdown } from "semantic-ui-react";
import { AppMedia } from "@js/invenio_theme/Media";
import PropTypes from "prop-types";

export const RequestActions = ({ request, size }) => {
  const actions = Object.keys(new RequestLinksExtractor(request).actions);
  const { MediaContextProvider, Media } = AppMedia;

  return (
    <Overridable
      id="InvenioRequests.RequestActions.layout"
      request={request}
      actions={actions}
    >
      <MediaContextProvider>
        <Media greaterThanOrEqual="tablet" className="media-inline-block">
          {actions.map((action) => (
            <RequestAction
              action={action}
              key={action}
              requestType={request.type}
              size={size}
            />
          ))}
        </Media>
        <Media lessThan="tablet">
          <Dropdown
            text="Actions"
            icon="caret down"
            floating
            labeled
            button
            className="icon tiny"
          >
            <Dropdown.Menu>
              {actions.map((action) => {
                return (
                  <RequestAction
                    key={action}
                    action={action}
                    requestType={request.type}
                  />
                );
              })}
            </Dropdown.Menu>
          </Dropdown>
        </Media>
      </MediaContextProvider>
    </Overridable>
  );
};

RequestActions.propTypes = {
  request: PropTypes.shape({
    type: PropTypes.string.isRequired,
  }).isRequired,
  size: PropTypes.string.isRequired,
};

export default Overridable.component("InvenioRequests.RequestActions", RequestActions);
