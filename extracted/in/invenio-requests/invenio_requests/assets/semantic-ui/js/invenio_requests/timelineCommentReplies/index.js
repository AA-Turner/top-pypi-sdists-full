// This file is part of InvenioRequests
// Copyright (C) 2026 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { connect } from "react-redux";
import { selectCommentReplies, selectCommentRepliesStatus } from "./state/reducer.js";
import {
  appendEventContent,
  clearDraft,
  fetchRepliesPage,
  REPLY_DELETED_COMMENT,
  REPLY_RESTORE_DRAFT_CONTENT,
  REPLY_SET_DRAFT_CONTENT,
  REPLY_SET_DRAFT_FILES,
  REPLY_RESTORE_DRAFT_FILES,
  REPLY_UPDATED_COMMENT,
  SET_SUBMITTING,
  setInitialReplies,
  setIsReplying,
  submitReply,
} from "./state/actions.js";
import {
  restoreDraftContent,
  setDraftContent,
  restoreEventFiles,
  setEventFiles,
} from "../timelineCommentEditor/state/actions.js";
import {
  deleteComment,
  updateComment,
} from "../timelineCommentEventControlled/state/actions.js";
import TimelineFeedRepliesComponent from "./TimelineFeedReplies.js";

const mapDispatchToProps = (dispatch, { parentRequestEvent }) => ({
  fetchPage: (page) => dispatch(fetchRepliesPage(parentRequestEvent, page)),
  setCommentContent: (content) =>
    dispatch(setDraftContent(content, parentRequestEvent.id, REPLY_SET_DRAFT_CONTENT)),
  restoreCommentContent: () =>
    dispatch(restoreDraftContent(parentRequestEvent.id, REPLY_RESTORE_DRAFT_CONTENT)),
  submitComment: (content, format, files) =>
    dispatch(submitReply(parentRequestEvent, content, format, files)),
  setCommentFiles: (files) =>
    dispatch(setEventFiles(files, parentRequestEvent.id, REPLY_SET_DRAFT_FILES)),
  restoreCommentFiles: () =>
    dispatch(restoreEventFiles(parentRequestEvent.id, REPLY_RESTORE_DRAFT_FILES)),
  updateComment: (payload) =>
    dispatch(
      updateComment({
        ...payload,
        parentRequestEventId: parentRequestEvent.id,
        successEvent: REPLY_UPDATED_COMMENT,
        loadingEvent: SET_SUBMITTING,
      })
    ),
  deleteComment: async (payload) =>
    dispatch(
      deleteComment({
        ...payload,
        parentRequestEventId: parentRequestEvent.id,
        successEvent: REPLY_DELETED_COMMENT,
        loadingEvent: SET_SUBMITTING,
      })
    ),
  appendCommentContent: (eventId, content) =>
    dispatch(appendEventContent(eventId, content)),
  setInitialReplies: (focusEvent) =>
    dispatch(setInitialReplies(parentRequestEvent, focusEvent)),
  setIsReplying: (replying) => dispatch(setIsReplying(parentRequestEvent.id, replying)),
  clearDraft: () => dispatch(clearDraft(parentRequestEvent.id)),
});

const mapStateToProps = (state, { parentRequestEvent }) => {
  const {
    pageNumbers,
    error,
    submitting: isSubmitting,
    draftContent: commentContent,
    storedDraftContent: storedCommentContent,
    draftFiles,
    appendedDraftContent: appendedCommentContent,
    submissionError,
    totalHits,
    replying,
    warning,
  } = selectCommentRepliesStatus(state.timelineReplies, parentRequestEvent.id);

  return {
    hits: selectCommentReplies(state.timelineReplies, parentRequestEvent.id),
    totalHits,
    pageNumbers,
    error,
    isSubmitting,
    permissions: parentRequestEvent.permissions,
    initialLoading: false,
    commentContent,
    draftFiles,
    storedCommentContent,
    appendedCommentContent,
    submissionError,
    replying,
    warning,
  };
};

const TimelineFeedReplies = connect(
  mapStateToProps,
  mapDispatchToProps
)(TimelineFeedRepliesComponent);

export default TimelineFeedReplies;
