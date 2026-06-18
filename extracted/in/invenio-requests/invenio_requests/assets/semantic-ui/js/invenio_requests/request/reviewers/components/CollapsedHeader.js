/*
 * SPDX-FileCopyrightText: 2025 CERN.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import React from "react";
import { Grid, Header, Icon } from "semantic-ui-react";

// Renders the header when the menu is collapsed.
export const CollapsedHeader = ({ canUpdateReviewers, onOpen, label }) => {
  if (!canUpdateReviewers) {
    return (
      <Header as="h3" size="tiny" className="mb-0">
        {label}
      </Header>
    );
  }
  return (
    <Grid onClick={onOpen} className="pb-0 mr-0">
      <Grid.Column width={12} floated="left">
        <Header as="h3" size="tiny" className="m-0">
          {label}
        </Header>
      </Grid.Column>
      <Grid.Column floated="right" className="mt-2 pr-20">
        <Icon name="setting" className="m-0 link" />
      </Grid.Column>
    </Grid>
  );
};

CollapsedHeader.propTypes = {
  canUpdateReviewers: PropTypes.bool.isRequired,
  onOpen: PropTypes.func.isRequired,
  label: PropTypes.string.isRequired,
};
