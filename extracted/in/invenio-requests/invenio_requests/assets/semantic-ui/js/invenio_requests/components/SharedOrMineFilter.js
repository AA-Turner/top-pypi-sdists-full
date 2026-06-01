// This file is part of Invenio
// Copyright (C) 2023 CERN.
//
// Invenio is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { withState } from "react-searchkit";
import { Button } from "semantic-ui-react";

class SharedOrMineFilterComponent extends Component {
  constructor(props) {
    super(props);

    // Extract `sharedWithMe` from `currentQueryState.filters`
    const { currentQueryState } = props;
    const userSelectionFilters = currentQueryState.filters || [];
    const sharedWithMe = userSelectionFilters.find((obj) =>
      obj.includes("shared_with_me")
    );

    // Initialize state without needing to use `setState` later
    this.state = {
      sharedWithMe: sharedWithMe ? sharedWithMe.includes("true") : false,
    };
  }

  /**
   * Updates queryFilters based on selection and removing previous filters
   * @param {string} sharedWithMeStatus is evaluated to true or false based on `shared_with_me` URL parameter
   */
  retrieveSharedOrMine = (sharedWithMeStatus) => {
    const { currentQueryState, updateQueryState, keepFiltersOnUpdate } = this.props;

    this.setState({
      sharedWithMe: sharedWithMeStatus,
    });
    currentQueryState.filters = keepFiltersOnUpdate
      ? currentQueryState.filters.filter((element) => element[0] !== "shared_with_me")
      : [];
    currentQueryState.filters.push(["shared_with_me", sharedWithMeStatus]);
    updateQueryState(currentQueryState);
  };

  render() {
    const { sharedWithMe } = this.state;
    const { sharedWithMeLabel, mineLabel } = this.props;

    return (
      <Button.Group basic fluid>
        <Button
          active={sharedWithMe === false}
          onClick={() => {
            this.retrieveSharedOrMine(false);
          }}
        >
          {mineLabel}
        </Button>
        <Button
          active={sharedWithMe === true}
          onClick={() => {
            this.retrieveSharedOrMine(true);
          }}
        >
          {sharedWithMeLabel}
        </Button>
      </Button.Group>
    );
  }
}

SharedOrMineFilterComponent.propTypes = {
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  keepFiltersOnUpdate: PropTypes.bool,
  sharedWithMeLabel: PropTypes.string,
  mineLabel: PropTypes.string,
};

SharedOrMineFilterComponent.defaultProps = {
  keepFiltersOnUpdate: true,
  sharedWithMeLabel: i18next.t("Shared with me"),
  mineLabel: i18next.t("My requests"),
};

export const SharedOrMineFilter = withState(SharedOrMineFilterComponent);
