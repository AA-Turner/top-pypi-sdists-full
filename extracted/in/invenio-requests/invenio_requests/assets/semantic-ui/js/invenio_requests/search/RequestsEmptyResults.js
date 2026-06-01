// This file is part of Invenio
// Copyright (C) 2023 CERN.
//
// Invenio is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React from "react";
import { Button, Header, Icon, Segment } from "semantic-ui-react";

import { withState } from "react-searchkit";

export const RequestsEmptyResults = ({
  queryString,
  userSelectionFilters,
  updateQueryState,
}) => {
  const isOpen = userSelectionFilters.some(
    (obj) => obj.includes("is_open") && obj.includes("true")
  );
  const filtersToNotReset = userSelectionFilters.find((obj) => obj.includes("is_open"));
  const elementsToReset = {
    queryString: "",
    page: 1,
    filters: [filtersToNotReset],
  };

  const AllDone = () => {
    return (
      <Header as="h1" icon>
        {i18next.t("All done!")}
        <Header.Subheader>
          {i18next.t("You've caught up with all open requests.")}
        </Header.Subheader>
      </Header>
    );
  };

  const NoResults = () => {
    return (
      <>
        <Header icon>
          <Icon name="search" />
          {i18next.t("No requests found!")}
        </Header>
        {queryString && (
          <Button primary onClick={() => updateQueryState(elementsToReset)}>
            {i18next.t("Reset search")}
          </Button>
        )}
      </>
    );
  };

  const allRequestsDone = isOpen && !queryString;
  return (
    <Segment placeholder textAlign="center">
      {allRequestsDone ? <AllDone /> : <NoResults />}
    </Segment>
  );
};

RequestsEmptyResults.propTypes = {
  queryString: PropTypes.string.isRequired,
  userSelectionFilters: PropTypes.array.isRequired,
  updateQueryState: PropTypes.func.isRequired,
};

export const RequestsEmptyResultsWithState = withState(RequestsEmptyResults);
