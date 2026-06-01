// This file is part of InvenioRequests
// Copyright (C) 2025 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { errorSerializer, payloadSerializer } from "../../api/serializers";
import {
  deleteDraftComment,
  deleteDraftFiles,
  setDraftComment,
} from "../../timelineCommentEditor/draftStorage";
import { i18next } from "@translations/invenio_requests/i18next";

export const SET_LOADING = "timelineReplies/SET_LOADING";
export const SET_TOTAL_HITS = "timelineReplies/SET_TOTAL_HITS";
export const SET_SUBMITTING = "timelineReplies/SET_SUBMITTING";
export const SET_REPLYING = "timelineReplies/SET_REPLYING";
export const SET_PAGE = "timelineReplies/SET_PAGE";
export const APPEND_TO_PAGE = "timelineReplies/APPEND_TO_PAGE";
export const HAS_ERROR = "timelineReplies/HAS_ERROR";
export const SET_WARNING = "timelineReplies/SET_WARNING";
export const HAS_SUBMISSION_ERROR = "timelineReplies/HAS_SUBMISSION_ERROR";
export const CLEAR_DRAFT = "timelineReplies/CLEAR_DRAFT";
export const REPLY_APPEND_DRAFT_CONTENT = "timelineReplies/APPEND_DRAFT_CONTENT";
export const REPLY_SET_DRAFT_CONTENT = "timelineReplies/SET_DRAFT_CONTENT";
export const REPLY_RESTORE_DRAFT_CONTENT = "timelineReplies/RESTORE_DRAFT_CONTENT";
export const REPLY_SET_DRAFT_FILES = "timelineReplies/SET_DRAFT_FILES";
export const REPLY_RESTORE_DRAFT_FILES = "timelineReplies/RESTORE_DRAFT_FILES";
export const REPLY_UPDATED_COMMENT = "timelineReplies/UPDATED_COMMENT";
export const REPLY_DELETED_COMMENT = "timelineReplies/DELETED_COMMENT";

export const appendEventContent = (parentRequestEventId, content) => {
  return (dispatch, getState) => {
    dispatch({
      type: REPLY_APPEND_DRAFT_CONTENT,
      payload: {
        content,
        parentRequestEventId,
      },
    });

    const { request } = getState();
    try {
      setDraftComment(request.data.id, parentRequestEventId, content);
    } catch (e) {
      console.warn("Failed to save comment:", e);
    }
  };
};

export const setIsReplying = (parentRequestEventId, replying) => {
  return (dispatch) => {
    dispatch({
      type: SET_REPLYING,
      payload: {
        parentRequestEventId,
        replying,
      },
    });
  };
};

export const setInitialReplies = (parentRequestEvent, focusEvent) => {
  return async (dispatch, _, config) => {
    // The server has the children newest-to-oldest, and we need oldest-to-newest so the newest is shown at the bottom.
    const children = (parentRequestEvent.children || []).toReversed();
    const childrenCount = parentRequestEvent.children_count || 0;
    const { size: pageSize } = config.defaultReplyQueryParams;

    dispatch({
      type: SET_WARNING,
      payload: { parentRequestEventId: parentRequestEvent.id, warning: null },
    });
    dispatch({
      type: SET_PAGE,
      payload: {
        parentRequestEventId: parentRequestEvent.id,
        hits: children,
        page: 1,
      },
    });
    dispatch({
      type: SET_TOTAL_HITS,
      payload: {
        parentRequestEventId: parentRequestEvent.id,
        totalHits: childrenCount,
      },
    });

    if (
      focusEvent &&
      focusEvent.parentEventId === parentRequestEvent.id &&
      focusEvent.replyEventId
    ) {
      // Check if focused event is on first or last page
      const existsInPreview = children.some((h) => h.id === focusEvent.replyEventId);

      if (!existsInPreview) {
        // Fetch focused event info to know which page it's on
        const focusedPageResponse = await config
          .requestEventsApi(parentRequestEvent.links)
          .getRepliesFocused(focusEvent.replyEventId, {
            size: pageSize,
            sort: "newest",
          });

        if (
          focusedPageResponse.data.hits.hits.some(
            (h) => h.id === focusEvent.replyEventId
          )
        ) {
          dispatch({
            type: SET_PAGE,
            payload: {
              parentRequestEventId: parentRequestEvent.id,
              hits: focusedPageResponse.data.hits.hits.toReversed(),
              page: focusedPageResponse.data.page,
            },
          });
        } else {
          // Show a warning if the event ID in the hash was not found in the response list of events.
          // This happens if the server cannot find the requested event.
          dispatch({
            type: SET_WARNING,
            payload: {
              parentRequestEventId: parentRequestEvent.id,
              warning: i18next.t("We couldn't find the reply you were looking for."),
            },
          });
        }
      }
    }
  };
};

export const fetchRepliesPage = (parentRequestEvent, page) => {
  return async (dispatch, _, config) => {
    const { size: pageSize } = config.defaultReplyQueryParams;

    dispatch({
      type: SET_LOADING,
      payload: { parentRequestEventId: parentRequestEvent.id, loading: true },
    });

    try {
      const api = config.requestEventsApi(parentRequestEvent.links);
      const response = await api.getReplies({
        size: pageSize,
        page,
        sort: "newest",
      });

      dispatch({
        type: SET_PAGE,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          // `hits` is ordered newest-to-oldest, which is correct for the pagination order.
          // But we need to insert the comments oldest-to-newest in the UI.
          hits: response.data.hits.hits.toReversed(),
          page,
        },
      });

      dispatch({
        type: SET_TOTAL_HITS,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          totalHits: response.data.hits.total,
        },
      });

      dispatch({
        type: SET_LOADING,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          loading: false,
        },
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          error: errorSerializer(error),
        },
      });
    }
  };
};

export const submitReply = (parentRequestEvent, content, format, files) => {
  return async (dispatch, getState, config) => {
    const { request } = getState();

    dispatch({
      type: SET_SUBMITTING,
      payload: {
        parentRequestEventId: parentRequestEvent.id,
        submitting: true,
      },
    });

    const payload = payloadSerializer(content, format || "html", files);

    try {
      const response = await config
        .requestEventsApi(parentRequestEvent.links)
        .submitReply(payload);

      try {
        deleteDraftComment(request.data.id, parentRequestEvent.id);
        deleteDraftFiles(request.data.id, parentRequestEvent.id);
      } catch (e) {
        console.warn("Failed to delete saved comment:", e);
      }

      dispatch({
        type: APPEND_TO_PAGE,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          hits: [response.data],
          page: 0,
        },
      });

      dispatch({
        type: SET_TOTAL_HITS,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          increaseCountBy: 1,
        },
      });

      dispatch({
        type: SET_SUBMITTING,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          submitting: false,
        },
      });

      dispatch({
        type: REPLY_SET_DRAFT_CONTENT,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          content: "",
        },
      });

      dispatch({
        type: REPLY_SET_DRAFT_FILES,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          files: [],
        },
      });
    } catch (error) {
      dispatch({
        type: HAS_SUBMISSION_ERROR,
        payload: {
          parentRequestEventId: parentRequestEvent.id,
          error: errorSerializer(error),
        },
      });

      throw error;
    }
  };
};

export const clearDraft = (parentRequestEventId) => {
  return (dispatch, getState) => {
    const { request } = getState();
    deleteDraftComment(request.data.id, parentRequestEventId);
    deleteDraftFiles(request.data.id, parentRequestEventId);
    dispatch({
      type: CLEAR_DRAFT,
      payload: {
        parentRequestEventId,
      },
    });
  };
};
