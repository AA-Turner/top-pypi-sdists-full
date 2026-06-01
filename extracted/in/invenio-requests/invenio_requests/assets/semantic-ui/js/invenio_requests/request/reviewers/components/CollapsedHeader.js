/*
 * This file is part of Invenio.
 * Copyright (C) 2025 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
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
