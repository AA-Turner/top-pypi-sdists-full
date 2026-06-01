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

class RequestStatusFilterComponent extends Component {
  constructor(props) {
    super(props);

    const { currentQueryState } = props;
    const userSelectionFilters = currentQueryState.filters;
    const openFilter = userSelectionFilters.find((obj) => obj.includes("is_open"));

    this.state = {
      open: openFilter ? openFilter.includes("true") : false,
    };
  }

  /**
   * Updates queryFilters based on selection and removing previous filters
   * @param {string} OpenStatus true if open requests and false if closed requests
   */
  retrieveRequests = (OpenStatus) => {
    const { currentQueryState, updateQueryState, keepFiltersOnUpdate } = this.props;
    const { open } = this.state;

    if (open === OpenStatus) {
      return;
    }
    this.setState({
      open: OpenStatus,
    });
    currentQueryState.filters = keepFiltersOnUpdate
      ? currentQueryState.filters.filter((element) => element[0] !== "is_open")
      : [];
    currentQueryState.filters.push(["is_open", OpenStatus]);
    updateQueryState(currentQueryState);
  };

  retrieveOpenRequests = () => {
    this.retrieveRequests(true);
  };

  retrieveClosedRequests = () => {
    this.retrieveRequests(false);
  };

  render() {
    const { open } = this.state;
    return (
      <Button.Group basic>
        <Button
          className="request-search-filter"
          onClick={this.retrieveOpenRequests}
          active={open === true}
        >
          {i18next.t("Open")}
        </Button>
        <Button
          className="request-search-filter"
          onClick={this.retrieveClosedRequests}
          active={open === false}
        >
          {i18next.t("Closed")}
        </Button>
      </Button.Group>
    );
  }
}

RequestStatusFilterComponent.propTypes = {
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  keepFiltersOnUpdate: PropTypes.bool,
};

RequestStatusFilterComponent.defaultProps = {
  keepFiltersOnUpdate: false,
};

export const RequestStatusFilter = withState(RequestStatusFilterComponent);
