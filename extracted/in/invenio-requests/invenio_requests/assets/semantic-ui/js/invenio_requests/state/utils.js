// This file is part of InvenioRequests
// Copyright (C) 2026 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

/**
 * Returns an object to include in an item of `commentStatuses`.
 * Either sets `totalHits` if specified, or increases if `increaseCountBy` is defined
 */
export const newOrIncreasedTotalHits = (state, payload) => {
  if (payload.totalHits) {
    return { totalHits: payload.totalHits };
  } else if (payload.increaseCountBy) {
    return { totalHits: state.totalHits + payload.increaseCountBy };
  }
  return {};
};

/**
 * Given a hits object (of shape { page_number: []hit }), returns the page number and array
 * index of the hit specified by `eventId`, or null if it is not found.
 */
export const findEventPageAndIndex = (hits, eventId) => {
  let pageNumber = null;
  let indexInPage = null;
  for (const thisPageNumber of Object.keys(hits)) {
    const index = hits[thisPageNumber].findIndex((c) => c.id === eventId);

    if (index !== -1) {
      pageNumber = thisPageNumber;
      indexInPage = index;
    }
  }

  if (pageNumber === null || indexInPage === null) return null;
  return { pageNumber, indexInPage };
};
