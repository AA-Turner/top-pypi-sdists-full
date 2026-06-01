/*
 * This file is part of Invenio.
 * Copyright (C) 2025 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React from "react";
import { Grid, Header, HeaderSubheader, Icon } from "semantic-ui-react";
import { DeletedResource, EntityDetails } from "../../RequestMetadata";

const isResourceDeleted = (details) => details.is_ghost === true;

// Renders the list of selected reviewers.
export const SelectedReviewersList = ({
  selectedReviewers,
  removeReviewer,
  i18next,
  maxReviewers,
}) => {
  return (
    <>
      <Header fluid as="h4" className="mb-5" size="tiny">
        {i18next.t(`Add up to ${maxReviewers} reviewers`)}
      </Header>
      {selectedReviewers.length === 0 ? (
        <HeaderSubheader className="pl-2 pt-2">
          {i18next.t("No reviewers selected")}
        </HeaderSubheader>
      ) : (
        <Grid className="pt-10 mb-5">
          {selectedReviewers.map((reviewer) => (
            <React.Fragment key={reviewer.id}>
              <Grid.Column width={13} className="pb-0">
                <React.Fragment key={reviewer.id}>
                  {isResourceDeleted(reviewer) ? (
                    <DeletedResource details={reviewer} />
                  ) : (
                    <EntityDetails userData={reviewer} details={reviewer} />
                  )}
                </React.Fragment>
              </Grid.Column>
              <Grid.Column width={2}>
                <Icon
                  name="close"
                  className="right-floated link"
                  onClick={() => removeReviewer(reviewer.id)}
                />
              </Grid.Column>
            </React.Fragment>
          ))}
        </Grid>
      )}
    </>
  );
};

SelectedReviewersList.propTypes = {
  selectedReviewers: PropTypes.array.isRequired,
  removeReviewer: PropTypes.func.isRequired,
  maxReviewers: PropTypes.number.isRequired,
  i18next: PropTypes.object.isRequired,
};
