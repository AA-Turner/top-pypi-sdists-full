// This file is part of InvenioRequests
// Copyright (C) 2025 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  APPEND_TO_PAGE,
  CLEAR_DRAFT,
  HAS_ERROR,
  HAS_SUBMISSION_ERROR,
  REPLY_APPEND_DRAFT_CONTENT,
  REPLY_DELETED_COMMENT,
  REPLY_RESTORE_DRAFT_CONTENT,
  REPLY_SET_DRAFT_CONTENT,
  REPLY_SET_DRAFT_FILES,
  REPLY_RESTORE_DRAFT_FILES,
  REPLY_UPDATED_COMMENT,
  SET_LOADING,
  SET_PAGE,
  SET_REPLYING,
  SET_SUBMITTING,
  SET_TOTAL_HITS,
  SET_WARNING,
} from "./actions";
import _cloneDeep from "lodash/cloneDeep";
import { findEventPageAndIndex, newOrIncreasedTotalHits } from "../../state/utils.js";

// Store lists of child comments and status objects, both grouped by parent request event ID.
// This follows Redux recommendations for a neater and more maintainable state shape: https://redux.js.org/usage/structuring-reducers/normalizing-state-shape#designing-a-normalized-state
export const initialState = {
  // { parent_event_id: { page_number: comment[] } }
  commentRepliesData: {},
  // { parent_event_id: status_obj (see below) }
  commentStatuses: {},
};

/**
 * @returns object { page_number: comment[] }
 */
export const selectCommentReplies = (state, parentRequestEventId) => {
  const { commentRepliesData } = state;
  if (Object.prototype.hasOwnProperty.call(commentRepliesData, parentRequestEventId)) {
    return commentRepliesData[parentRequestEventId];
  } else {
    return {};
  }
};

export const newOrAppendedPage = (state, parentRequestEventId, page, hits) => {
  const commentReplies = selectCommentReplies(state, parentRequestEventId);
  if (Object.prototype.hasOwnProperty.call(commentReplies, page)) {
    return [...commentReplies[page], ...hits];
  } else {
    return hits;
  }
};

// Initial value for a single item in `commentStatuses`
const initialCommentStatus = {
  pageNumbers: [],
  totalHits: 0,
  loading: false,
  submitting: false,
  error: null,
  warning: null,
  submissionError: null,
  draftContent: "",
  storedDraftContent: "",
  appendedDraftContent: "",
  draftFiles: [],
  replying: false,
};

export const selectCommentRepliesStatus = (state, parentRequestEventId) => {
  const { commentStatuses } = state;
  // Using `parentRequestEventId in status` is not advised, as the key could be in the prototype: https://stackoverflow.com/a/455366
  // Using status.hasOwnProperty is not allowed by eslint: https://eslint.org/docs/latest/rules/no-prototype-builtins
  if (Object.prototype.hasOwnProperty.call(commentStatuses, parentRequestEventId)) {
    return { ...initialCommentStatus, ...commentStatuses[parentRequestEventId] };
  } else {
    return initialCommentStatus;
  }
};

const newCommentRepliesWithUpdate = (childComments, updatedComment) => {
  const newChildComments = _cloneDeep(childComments);
  const position = findEventPageAndIndex(newChildComments, updatedComment.id);
  if (position === null) return newChildComments;

  newChildComments[position.pageNumber][position.indexInPage] = {
    ...newChildComments[position.pageNumber][position.indexInPage],
    ...updatedComment,
  };
  return newChildComments;
};

const newCommentRepliesWithDelete = (childComments, deletedCommentId) => {
  return newCommentRepliesWithUpdate(childComments, {
    id: deletedCommentId,
    type: "L",
    payload: {
      content: "comment was deleted",
      format: "html",
      event: "comment_deleted",
    },
  });
};

// Partially update the status for a given parent event, leaving everything else unchanged.
const newStateWithUpdatedStatus = (state, parentRequestEventId, newStatus) => {
  return {
    ...state,
    commentStatuses: {
      ...state.commentStatuses,
      [parentRequestEventId]: {
        ...selectCommentRepliesStatus(state, parentRequestEventId),
        ...newStatus,
      },
    },
  };
};

const newPageNumbersWithPage = (state, parentRequestEventId, page) => {
  return [
    // Pass through a set to ensure de-duplication
    ...new Set(selectCommentRepliesStatus(state, parentRequestEventId).pageNumbers).add(
      page
    ),
  ].toSorted((a, b) => a - b);
};

export const timelineRepliesReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_LOADING:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        loading: action.payload.loading,
        error: null,
      });
    case SET_SUBMITTING:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        submitting: action.payload.submitting,
        submissionError: null,
      });
    case SET_TOTAL_HITS:
      return newStateWithUpdatedStatus(
        state,
        action.payload.parentRequestEventId,
        newOrIncreasedTotalHits(
          selectCommentRepliesStatus(state, action.payload.parentRequestEventId),
          action.payload
        )
      );
    case SET_REPLYING:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        replying: action.payload.replying,
      });
    case SET_PAGE:
      return {
        ...newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
          pageNumbers: newPageNumbersWithPage(
            state,
            action.payload.parentRequestEventId,
            action.payload.page
          ),
        }),
        commentRepliesData: {
          ...state.commentRepliesData,
          [action.payload.parentRequestEventId]: {
            ...selectCommentReplies(state, action.payload.parentRequestEventId),
            [action.payload.page]: action.payload.hits,
          },
        },
      };
    case SET_WARNING:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        warning: action.payload.warning,
      });
    case APPEND_TO_PAGE:
      return {
        ...newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
          pageNumbers: newPageNumbersWithPage(
            state,
            action.payload.parentRequestEventId,
            action.payload.page
          ),
        }),
        commentRepliesData: {
          ...state.commentRepliesData,
          [action.payload.parentRequestEventId]: {
            ...selectCommentReplies(state, action.payload.parentRequestEventId),
            [action.payload.page]: newOrAppendedPage(
              state,
              action.payload.parentRequestEventId,
              action.payload.page,
              action.payload.hits
            ),
          },
        },
      };
    case HAS_ERROR:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        error: action.payload.error,
        loading: false,
      });
    case HAS_SUBMISSION_ERROR:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        submissionError: action.payload.error,
        submitting: false,
      });
    case REPLY_SET_DRAFT_CONTENT:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftContent: action.payload.content,
      });

    case REPLY_RESTORE_DRAFT_CONTENT:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftContent: action.payload.content,
        storedDraftContent: action.payload.content,
      });

    case REPLY_APPEND_DRAFT_CONTENT:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftContent:
          selectCommentRepliesStatus(state, action.payload.parentRequestEventId)
            .draftContent + action.payload.content,
        appendedDraftContent:
          selectCommentRepliesStatus(state, action.payload.parentRequestEventId)
            .draftContent + action.payload.content,
        replying: true,
      });
    case REPLY_SET_DRAFT_FILES:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftFiles: action.payload.files,
      });
    case REPLY_RESTORE_DRAFT_FILES:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftFiles: action.payload.files,
      });
    case CLEAR_DRAFT:
      return newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
        draftContent: "",
        storedDraftContent: "",
        draftFiles: [],
      });
    case REPLY_UPDATED_COMMENT:
      return {
        ...newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
          submitting: false,
        }),
        commentRepliesData: {
          ...state.commentRepliesData,
          [action.payload.parentRequestEventId]: newCommentRepliesWithUpdate(
            selectCommentReplies(state, action.payload.parentRequestEventId),
            action.payload.updatedComment
          ),
        },
      };
    case REPLY_DELETED_COMMENT:
      return {
        ...newStateWithUpdatedStatus(state, action.payload.parentRequestEventId, {
          submitting: false,
        }),
        commentRepliesData: {
          ...state.commentRepliesData,
          [action.payload.parentRequestEventId]: newCommentRepliesWithDelete(
            selectCommentReplies(state, action.payload.parentRequestEventId),
            action.payload.deletedCommentId
          ),
        },
      };
    default:
      return state;
  }
};
