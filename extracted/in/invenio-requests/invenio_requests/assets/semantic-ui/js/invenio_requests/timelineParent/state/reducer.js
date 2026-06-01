// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  HAS_ERROR,
  SET_WARNING,
  PARENT_DELETED_COMMENT,
  PARENT_UPDATED_COMMENT,
  SET_PAGE,
  SET_TOTAL_HITS,
  SET_FOCUSED_PAGE,
  SET_LOADING_MORE,
  APPEND_TO_LAST_PAGE,
  PARENT_SET_DRAFT_CONTENT,
  PARENT_RESTORE_DRAFT_CONTENT,
  PARENT_SET_DRAFT_FILES,
  PARENT_RESTORE_DRAFT_FILES,
  HAS_SUBMISSION_ERROR,
  SET_SUBMITTING,
  SET_REFRESHING,
  SET_INITIAL_LOADING,
} from "./actions";
import _cloneDeep from "lodash/cloneDeep";
import { findEventPageAndIndex, newOrIncreasedTotalHits } from "../../state/utils";

export const initialState = {
  initialLoading: false,
  lastPageRefreshing: false,
  loadingMore: false,
  // Dictionary of form { page_number: []hit }
  hits: {},
  pageNumbers: [],
  totalHits: 0,
  error: null,
  submissionError: null,
  // The page number that the focused event belongs to.
  focusedPage: null,
  warning: null,
  commentContent: "",
  files: [],
  storedCommentContent: null,
  submitting: false,
};

const newStateWithUpdate = (timelineState, updatedComment) => {
  const newTimelineState = _cloneDeep(timelineState);
  const position = findEventPageAndIndex(newTimelineState["hits"], updatedComment.id);
  if (position === null) return newTimelineState;
  newTimelineState.hits[position.pageNumber][position.indexInPage] = {
    ...newTimelineState.hits[position.pageNumber][position.indexInPage],
    ...updatedComment,
  };
  return newTimelineState;
};

const newStateWithDelete = (timelineState, deletedCommentId) => {
  return newStateWithUpdate(timelineState, {
    id: deletedCommentId,
    type: "L",
    payload: {
      content: "comment was deleted",
      format: "html",
      event: "comment_deleted",
    },
  });
};

const appendToLastOrNewPage = (timelineState, hit, pageSize) => {
  const lastPage = Math.max(...timelineState.pageNumbers);
  const lastPageSize = timelineState.hits[lastPage].length;

  if (lastPageSize >= pageSize) {
    return {
      ...timelineState,
      hits: {
        ...timelineState.hits,
        [lastPage + 1]: [hit],
      },
      pageNumbers: [...timelineState.pageNumbers, lastPage + 1].toSorted(),
    };
  } else {
    return {
      ...timelineState,
      hits: {
        ...timelineState.hits,
        [lastPage]: [...timelineState.hits[lastPage], hit],
      },
    };
  }
};

export const timelineReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_INITIAL_LOADING:
      return { ...state, initialLoading: action.payload.loading };
    case SET_REFRESHING:
      return { ...state, lastPageRefreshing: action.payload.refreshing };
    case SET_PAGE:
      return {
        ...state,
        hits: {
          ...state.hits,
          [action.payload.page]: action.payload.hits,
        },
        pageNumbers: [...new Set(state.pageNumbers).add(action.payload.page)].toSorted(
          (a, b) => a - b
        ),
      };
    case APPEND_TO_LAST_PAGE:
      return appendToLastOrNewPage(state, action.payload.hit, action.payload.pageSize);
    case SET_TOTAL_HITS:
      return {
        ...state,
        ...newOrIncreasedTotalHits(state, action.payload),
      };
    case SET_FOCUSED_PAGE:
      return {
        ...state,
        focusedPage: action.payload.focusedPage,
      };
    case SET_LOADING_MORE:
      return {
        ...state,
        loadingMore: action.payload.loadingMore,
      };
    case SET_SUBMITTING:
      return {
        ...state,
        submitting: action.payload.submitting,
        submissionError: null,
      };
    case HAS_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    case HAS_SUBMISSION_ERROR:
      return {
        ...state,
        submitting: false,
        submissionError: action.payload,
      };
    case SET_WARNING:
      return {
        ...state,
        warning: action.payload.warning,
      };
    case PARENT_UPDATED_COMMENT:
      return newStateWithUpdate(state, action.payload.updatedComment);
    case PARENT_DELETED_COMMENT:
      return newStateWithDelete(state, action.payload.deletedCommentId);
    case PARENT_SET_DRAFT_CONTENT:
      return { ...state, commentContent: action.payload.content };
    case PARENT_RESTORE_DRAFT_CONTENT:
      return {
        ...state,
        commentContent: action.payload.content,
        // We'll never change this later, so it can be used as an `initialValue`
        storedCommentContent: action.payload.content,
      };
    case PARENT_SET_DRAFT_FILES:
      return { ...state, files: action.payload.files };
    case PARENT_RESTORE_DRAFT_FILES:
      return {
        ...state,
        files: action.payload.files,
      };

    default:
      return state;
  }
};
