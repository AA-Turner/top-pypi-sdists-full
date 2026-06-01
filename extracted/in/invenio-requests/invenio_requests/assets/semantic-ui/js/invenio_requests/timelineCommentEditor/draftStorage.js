// This file is part of InvenioRequests
// Copyright (C) 2026 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

const draftCommentKey = (requestId, parentRequestEventId) =>
  `draft-comment-${requestId}${parentRequestEventId ? "-" + parentRequestEventId : ""}`;
export const setDraftComment = (requestId, parentRequestEventId, content) => {
  localStorage.setItem(draftCommentKey(requestId, parentRequestEventId), content);
};
export const getDraftComment = (requestId, parentRequestEventId) => {
  return localStorage.getItem(draftCommentKey(requestId, parentRequestEventId));
};
export const deleteDraftComment = (requestId, parentRequestEventId) => {
  localStorage.removeItem(draftCommentKey(requestId, parentRequestEventId));
};

const draftFilesKey = (requestId, parentRequestEventId) =>
  `draft-files-${requestId}${parentRequestEventId ? "-" + parentRequestEventId : ""}`;
export const setDraftFiles = (requestId, parentRequestEventId, files) => {
  localStorage.setItem(
    draftFilesKey(requestId, parentRequestEventId),
    JSON.stringify(files)
  );
};
export const getDraftFiles = (requestId, parentRequestEventId) => {
  return JSON.parse(
    localStorage.getItem(draftFilesKey(requestId, parentRequestEventId))
  );
};
export const deleteDraftFiles = (requestId, parentRequestEventId) => {
  localStorage.removeItem(draftFilesKey(requestId, parentRequestEventId));
};
