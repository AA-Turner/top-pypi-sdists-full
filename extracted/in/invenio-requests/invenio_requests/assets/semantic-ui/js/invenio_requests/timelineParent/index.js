// This file is part of InvenioRequests
// Copyright (C) 2026 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { connect } from "react-redux";
import {
  getTimelineWithRefresh,
  clearTimelineInterval,
  PARENT_SET_DRAFT_CONTENT,
  PARENT_RESTORE_DRAFT_CONTENT,
  PARENT_SET_DRAFT_FILES,
  PARENT_RESTORE_DRAFT_FILES,
  submitComment,
  PARENT_UPDATED_COMMENT,
  SET_REFRESHING,
  PARENT_DELETED_COMMENT,
  fetchTimelinePageWithLoading,
} from "./state/actions";
import TimelineFeedParent from "./TimelineFeedParent";
import {
  restoreDraftContent,
  setDraftContent,
  setEventFiles,
  restoreEventFiles,
} from "../timelineCommentEditor/state/actions";
import {
  deleteComment,
  updateComment,
} from "../timelineCommentEventControlled/state/actions";
import { appendEventContent } from "../timelineCommentReplies/state/actions";

const mapDispatchToProps = (dispatch) => ({
  getTimelineWithRefresh: (includeEventId) =>
    dispatch(getTimelineWithRefresh(includeEventId)),
  timelineStopRefresh: () => dispatch(clearTimelineInterval()),
  fetchPage: (page) => dispatch(fetchTimelinePageWithLoading(page)),
  setCommentContent: (content) =>
    dispatch(setDraftContent(content, null, PARENT_SET_DRAFT_CONTENT)),
  restoreCommentContent: () =>
    dispatch(restoreDraftContent(null, PARENT_RESTORE_DRAFT_CONTENT)),
  setCommentFiles: (files) =>
    dispatch(setEventFiles(files, null, PARENT_SET_DRAFT_FILES)),
  restoreCommentFiles: () =>
    dispatch(restoreEventFiles(null, PARENT_RESTORE_DRAFT_FILES)),
  submitComment: (content, format, files) =>
    dispatch(submitComment(content, format, files)),
  updateComment: async (payload) =>
    dispatch(
      updateComment({
        ...payload,
        successEvent: PARENT_UPDATED_COMMENT,
        loadingEvent: SET_REFRESHING,
      })
    ),
  deleteComment: async (payload) =>
    dispatch(
      deleteComment({
        ...payload,
        successEvent: PARENT_DELETED_COMMENT,
        loadingEvent: SET_REFRESHING,
      })
    ),
  appendCommentContent: (eventId, content) =>
    dispatch(appendEventContent(eventId, content)),
});

const mapStateToProps = (state) => {
  return {
    hits: state.timeline.hits,
    totalHits: state.timeline.totalHits,
    pageNumbers: state.timeline.pageNumbers,
    initialLoading: state.timeline.initialLoading,
    error: state.timeline.error,
    isSubmitting: state.timeline.submitting,
    warning: state.timeline.warning,
    commentContent: state.timeline.commentContent,
    storedCommentContent: state.timeline.storedCommentContent,
    draftFiles: state.timeline.files,
    submissionError: state.timeline.submissionError,
  };
};

export const Timeline = connect(
  mapStateToProps,
  mapDispatchToProps
)(TimelineFeedParent);
