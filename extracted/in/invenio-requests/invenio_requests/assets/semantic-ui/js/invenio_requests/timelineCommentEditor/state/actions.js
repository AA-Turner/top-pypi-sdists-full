// This file is part of InvenioRequests
// Copyright (C) 2022-2025 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  getDraftComment,
  setDraftComment,
  getDraftFiles,
  setDraftFiles,
} from "../draftStorage";

export const setDraftContent = (content, parentRequestEventId, event) => {
  return async (dispatch, getState) => {
    dispatch({
      type: event,
      payload: {
        parentRequestEventId,
        content,
      },
    });
    const { request } = getState();

    try {
      setDraftComment(request.data.id, parentRequestEventId, content);
    } catch (e) {
      // This should not be a fatal error. The comment editor is still usable if
      // draft saving isn't working (e.g. on very old browsers or ultra-restricted
      // environments with 0 storage quota.)
      console.warn("Failed to save comment:", e);
    }
  };
};

export const restoreDraftContent = (parentRequestEventId, event) => {
  return (dispatch, getState) => {
    const { request } = getState();
    let savedDraft = null;
    try {
      savedDraft = getDraftComment(request.data.id, parentRequestEventId);
    } catch (e) {
      console.warn("Failed to get saved comment:", e);
    }

    if (savedDraft) {
      dispatch({
        type: event,
        payload: {
          parentRequestEventId,
          content: savedDraft,
        },
      });
    }
  };
};

export const setEventFiles = (files, parentRequestEventId, event) => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: event,
      payload: {
        parentRequestEventId,
        files,
      },
    });
    const { request } = getState();

    try {
      setDraftFiles(request.data.id, parentRequestEventId, files);
    } catch (e) {
      // This should not be a fatal error. The comment editor is still usable if
      // draft saving isn't working (e.g. on very old browsers or ultra-restricted
      // environments with 0 storage quota.)
      console.warn("Failed to save comment files:", e);
    }
  };
};

export const restoreEventFiles = (parentRequestEventId, event) => {
  return (dispatch, getState, config) => {
    const { request } = getState();
    let savedDraftFiles = null;
    try {
      savedDraftFiles = getDraftFiles(request.data.id, parentRequestEventId);
    } catch (e) {
      console.warn("Failed to get saved files:", e);
    }

    if (savedDraftFiles) {
      dispatch({
        type: event,
        payload: {
          parentRequestEventId,
          files: savedDraftFiles,
        },
      });
    }
  };
};
