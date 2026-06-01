/*
 * This file is part of Invenio.
 * Copyright (C) 2025 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React from "react";
import { Button, Search } from "semantic-ui-react";

// Renders the filter buttons and search input.
export const ReviewerSearch = ({
  searchType,
  onFilterChange,
  searchQuery,
  results,
  onSearchChange,
  onResultSelect,
  renderResult,
  i18next,
  allowGroupReviewers,
}) => (
  <>
    {allowGroupReviewers && (
      <div className="mb-10">
        <Button.Group fluid basic size="mini">
          <Button active={searchType === "user"} onClick={() => onFilterChange("user")}>
            {i18next.t("People")}
          </Button>
          <Button
            active={searchType === "group"}
            onClick={() => onFilterChange("group")}
          >
            {i18next.t("Groups")}
          </Button>
        </Button.Group>
      </div>
    )}
    <div>
      <Search
        placeholder={
          searchType === "user"
            ? i18next.t("Search for user")
            : i18next.t("Search for groups")
        }
        onSearchChange={onSearchChange}
        results={results}
        resultRenderer={renderResult}
        value={searchQuery}
        onResultSelect={onResultSelect}
        showNoResults={false}
        input={{ fluid: true }}
      />
    </div>
  </>
);

ReviewerSearch.propTypes = {
  searchType: PropTypes.oneOf(["user", "group"]).isRequired,
  onFilterChange: PropTypes.func.isRequired,
  searchQuery: PropTypes.string.isRequired,
  results: PropTypes.array.isRequired,
  onSearchChange: PropTypes.func.isRequired,
  onResultSelect: PropTypes.func.isRequired,
  renderResult: PropTypes.func.isRequired,
  i18next: PropTypes.object.isRequired,
  allowGroupReviewers: PropTypes.bool.isRequired,
};
