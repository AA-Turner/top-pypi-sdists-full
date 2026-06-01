/*
 * This file is part of Invenio.
 * Copyright (C) 2025 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { useState } from "react";
import PropTypes from "prop-types";
import { HeaderSubheader, Grid, List, Image, Segment } from "semantic-ui-react";
import { UsersApi } from "@js/invenio_communities/api/UsersApi";
import { GroupsApi } from "@js/invenio_communities/api/GroupsApi";
import {
  InvenioRequestsAPI,
  RequestLinksExtractor,
} from "@js/invenio_requests/api/InvenioRequestApi";
import { i18next } from "@translations/invenio_requests/i18next";
import RequestsFeed from "../../components/RequestsFeed";
import { EntityDetails, DeletedResource } from "../RequestMetadata";
import { CollapsedHeader } from "./components/CollapsedHeader";
import { ReviewerSearch } from "./components/ReviewerSearch";
import { SelectedReviewersList } from "./components/SelectedReviewersList";

const isResourceDeleted = (details) => details.is_ghost === true;

export const RequestReviewers = ({
  request,
  permissions,
  allowGroupReviewers,
  maxReviewers,
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchType, setSearchType] = useState("user");
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);

  const reviewers = request.expanded?.reviewers || [];

  const initialReviewers = reviewers.map((r, index) => {
    return "user" in request.reviewers[index]
      ? { ...r, user: request.reviewers[index].user }
      : { ...r, group: request.reviewers[index].group };
  });

  const [selectedReviewers, setSelectedReviewers] = useState(initialReviewers);
  const requestApi = new InvenioRequestsAPI(new RequestLinksExtractor(request));

  const handleSearchChange = async (e, { value }) => {
    setSearchQuery(value);
    if (value.length > 1) {
      try {
        let suggestions;
        if (searchType === "user") {
          const usersClient = new UsersApi();
          suggestions = await usersClient.suggestUsers(value);
        } else {
          const groupsClient = new GroupsApi();
          suggestions = await groupsClient.getGroups(value);
        }
        setResults(suggestions.data.hits.hits);
      } catch (error) {
        console.error(`Error fetching ${searchType} suggestions:`, error);
        setResults([]);
      }
    } else {
      setResults([]);
    }
  };

  const handleResultSelect = async (e, { result }) => {
    if (!selectedReviewers.find((r) => r.id === result.id)) {
      const newReviewers = [
        ...selectedReviewers,
        { ...result, [searchType]: result.id },
      ];
      setSelectedReviewers(newReviewers);
      const _ = await requestApi.addReviewer(newReviewers);
    }
    setSearchQuery("");
    setResults([]);
  };

  const removeReviewer = async (userId) => {
    const newReviewers = selectedReviewers.filter((r) => r.id !== userId);
    setSelectedReviewers(newReviewers);
    const _ = await requestApi.addReviewer(newReviewers);
    setSelectedReviewers(newReviewers);
  };

  // A helper to render a search result item.
  const renderResult = (item) => (
    <List.Item key={item.id}>
      <RequestsFeed.Avatar src={item.links?.avatar} as={Image} circular size="tiny" />
      <List.Content>{item.profile?.full_name || item.name}</List.Content>
    </List.Item>
  );

  return (
    <>
      <CollapsedHeader
        canUpdateReviewers={permissions.can_action_accept}
        onOpen={() => setIsMenuOpen(!isMenuOpen)}
        label={i18next.t("Reviewers")}
      />
      {!isMenuOpen ? (
        <Grid className="mt-0 mb-5">
          {selectedReviewers.length > 0 ? (
            selectedReviewers.map((reviewer) => (
              <Grid.Column width={14} className="pb-0" key={reviewer.id}>
                <React.Fragment>
                  {isResourceDeleted(reviewer) ? (
                    <DeletedResource details={reviewer} />
                  ) : (
                    <EntityDetails userData={reviewer} details={reviewer} />
                  )}
                </React.Fragment>
              </Grid.Column>
            ))
          ) : (
            <Grid.Column width={12} className="pb-0 pl-20">
              <HeaderSubheader>{i18next.t("No reviewers selected")}</HeaderSubheader>
            </Grid.Column>
          )}
        </Grid>
      ) : (
        <Segment>
          <ReviewerSearch
            searchType={searchType}
            onFilterChange={setSearchType}
            searchQuery={searchQuery}
            results={results}
            onSearchChange={handleSearchChange}
            onResultSelect={handleResultSelect}
            renderResult={renderResult}
            i18next={i18next}
            allowGroupReviewers={allowGroupReviewers}
          />

          <SelectedReviewersList
            selectedReviewers={selectedReviewers}
            removeReviewer={removeReviewer}
            i18next={i18next}
            maxReviewers={maxReviewers}
          />
        </Segment>
      )}
    </>
  );
};

RequestReviewers.propTypes = {
  request: PropTypes.object.isRequired,
  permissions: PropTypes.shape({
    can_action_accept: PropTypes.bool.isRequired,
  }).isRequired,
  allowGroupReviewers: PropTypes.bool.isRequired,
  maxReviewers: PropTypes.number.isRequired,
};
