/*
 * SPDX-FileCopyrightText: 2023 CERN.
 * SPDX-License-Identifier: MIT
 */

import { InvenioSearchPagination } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React from "react";
import { Count, ResultsList, Sort } from "react-searchkit";
import { Grid, Segment } from "semantic-ui-react";

export const RequestsResults = ({
  sortOptions,
  paginationOptions,
  currentResultsState,
}) => {
  const { total } = currentResultsState.data;

  const handleResultsRendered = () => {
    window.invenio?.onSearchResultsRendered();
  };
  return (
    total && (
      <Grid>
        <Grid.Row>
          <Grid.Column width={16}>
            <Segment>
              <Grid>
                <Grid.Row
                  verticalAlign="middle"
                  className="small pt-5 pb-5 highlight-background"
                >
                  <Grid.Column width={4}>
                    <Count
                      label={() => (
                        <>
                          {i18next.t("{{count}} results found", {
                            count: total,
                          })}
                        </>
                      )}
                    />
                  </Grid.Column>
                  <Grid.Column width={12} textAlign="right">
                    {sortOptions && (
                      <Sort
                        values={sortOptions}
                        label={(cmp) => (
                          <>
                            <label className="mr-10">{i18next.t("Sort by")}</label>
                            {cmp}
                          </>
                        )}
                      />
                    )}
                  </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                  <Grid.Column>
                    <ResultsList onResultsRendered={handleResultsRendered} />
                  </Grid.Column>
                </Grid.Row>
              </Grid>
            </Segment>
          </Grid.Column>
        </Grid.Row>
        <InvenioSearchPagination paginationOptions={paginationOptions} />
      </Grid>
    )
  );
};

RequestsResults.propTypes = {
  sortOptions: PropTypes.object.isRequired,
  paginationOptions: PropTypes.object.isRequired,
  currentResultsState: PropTypes.object.isRequired,
};
