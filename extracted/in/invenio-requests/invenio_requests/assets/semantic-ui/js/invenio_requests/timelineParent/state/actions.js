// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { errorSerializer, payloadSerializer } from "../../api/serializers";
import {
  deleteDraftComment,
  deleteDraftFiles,
} from "../../timelineCommentEditor/draftStorage.js";
import { i18next } from "@translations/invenio_requests/i18next";

export const SET_INITIAL_LOADING = "timeline/SET_LOADING";
export const HAS_ERROR = "timeline/HAS_ERROR";
export const HAS_SUBMISSION_ERROR = "timeline/HAS_SUBMISSION_ERROR";
export const SET_REFRESHING = "timeline/SET_REFRESHING";
export const SET_SUBMITTING = "timeline/SET_SUBMITTING";
export const SET_TOTAL_HITS = "timeline/SET_TOTAL_HITS";
export const SET_FOCUSED_PAGE = "timeline/SET_FOCUSED_PAGE";
export const SET_LOADING_MORE = "timeline/SET_LOADING_MORE";
export const SET_WARNING = "timeline/SET_WARNING";
export const SET_PAGE = "timeline/SET_PAGE";
export const APPEND_TO_LAST_PAGE = "timeline/APPEND_TO_LAST_PAGE";
export const PARENT_UPDATED_COMMENT = "timeline/PARENT_UPDATED_COMMENT";
export const PARENT_DELETED_COMMENT = "timeline/PARENT_DELETED_COMMENT";
export const PARENT_SET_DRAFT_CONTENT = "timeline/PARENT_SET_DRAFT_CONTENT";
export const PARENT_RESTORE_DRAFT_CONTENT = "timeline/PARENT_RESTORE_DRAFT_CONTENT";
export const PARENT_SET_DRAFT_FILES = "timeline/PARENT_SET_DRAFT_FILES";
export const PARENT_RESTORE_DRAFT_FILES = "timeline/PARENT_RESTORE_DRAFT_FILES";

class intervalManager {
  static IntervalId = undefined;

  static setIntervalId(intervalId) {
    this.intervalId = intervalId;
  }

  static resetInterval() {
    clearInterval(this.intervalId);
    delete this.intervalId;
  }
}

export const fetchTimeline = (focusEvent = undefined) => {
  return async (dispatch, _, config) => {
    const { size } = config.defaultQueryParams;

    dispatch({ type: HAS_ERROR, payload: null });
    dispatch({ type: SET_WARNING, payload: { warning: null } });

    try {
      const firstPageResponse = await config.requestsApi.getTimeline({
        size,
        page: 1,
        sort: "oldest",
      });

      const totalHits = firstPageResponse.data.hits.total || 0;
      const lastPageNumber = Math.ceil(totalHits / size);

      let lastPageResponse = null;
      // Only fetch last page if not the same as the first page
      if (lastPageNumber > 1) {
        lastPageResponse = await config.requestsApi.getTimeline({
          size,
          page: lastPageNumber,
          sort: "oldest",
        });
      }

      let focusedPageNumber = null;
      let focusedPageResponse = null;

      if (focusEvent) {
        // Check if focused event is on first or last page
        const existsOnFirstPage = firstPageResponse.data.hits.hits.some(
          (h) => h.id === focusEvent.parentEventId
        );
        const existsOnLastPage = lastPageResponse?.data.hits.hits.some(
          (h) => h.id === focusEvent.parentEventId
        );

        if (existsOnFirstPage) {
          focusedPageNumber = 1;
        } else if (existsOnLastPage) {
          focusedPageNumber = lastPageNumber;
        } else {
          // Fetch focused event info to know which page it's on
          focusedPageResponse = await config.requestsApi.getTimelineFocused(
            focusEvent.parentEventId,
            {
              size,
              sort: "oldest",
            }
          );
          focusedPageNumber = focusedPageResponse?.data.page;

          if (
            !focusedPageResponse.data.hits.hits.some(
              (h) => h.id === focusEvent.parentEventId
            )
          ) {
            // Show a warning if the event ID in the hash was not found in the response list of events.
            // This happens if the server cannot find the requested event.
            dispatch({
              type: SET_WARNING,
              payload: {
                warning: i18next.t(
                  "We couldn't find the comment you were looking for."
                ),
              },
            });
          }
        }
      }

      dispatch({
        type: SET_PAGE,
        payload: {
          page: 1,
          hits: firstPageResponse.data.hits.hits,
        },
      });

      if (focusedPageResponse) {
        dispatch({
          type: SET_PAGE,
          payload: {
            page: focusedPageNumber,
            hits: focusedPageResponse.data.hits.hits,
          },
        });
      }

      if (lastPageResponse) {
        dispatch({
          type: SET_PAGE,
          payload: {
            page: lastPageNumber,
            hits: lastPageResponse.data.hits.hits,
          },
        });
      }

      dispatch({
        type: SET_TOTAL_HITS,
        payload: {
          totalHits,
        },
      });

      dispatch({
        type: SET_FOCUSED_PAGE,
        payload: {
          focusedPage: focusedPageNumber,
        },
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: errorSerializer(error),
      });
    }
  };
};

export const fetchTimelinePage = (page) => {
  return async (dispatch, _, config) => {
    const { size } = config.defaultQueryParams;

    try {
      const response = await config.requestsApi.getTimeline({
        size,
        page,
        sort: "oldest",
      });

      dispatch({
        type: SET_PAGE,
        payload: {
          page,
          hits: response.data.hits.hits,
        },
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: errorSerializer(error),
      });
    }
  };
};

export const fetchTimelinePageWithLoading = (page) => {
  return async (dispatch) => {
    dispatch({ type: SET_LOADING_MORE, payload: { loadingMore: true } });
    await dispatch(fetchTimelinePage(page));
    dispatch({ type: SET_LOADING_MORE, payload: { loadingMore: false } });
  };
};

const timelineReload = async (dispatch, getState) => {
  const { timeline } = getState();
  const { initialLoading, lastPageRefreshing, error, submitting, pageNumbers } =
    timeline;

  if (error) {
    dispatch(clearTimelineInterval());
  }

  const concurrentRequests = initialLoading || lastPageRefreshing || submitting;
  if (concurrentRequests) return;

  const lastPage = pageNumbers[pageNumbers.length - 1];

  // Fetch only the last page
  dispatch({ type: SET_REFRESHING, payload: { refreshing: true } });
  await dispatch(fetchTimelinePage(lastPage));
  dispatch({ type: SET_REFRESHING, payload: { refreshing: false } });
};

export const getTimelineWithRefresh = (focusEventId) => {
  return async (dispatch) => {
    dispatch({
      type: SET_INITIAL_LOADING,
      payload: { loading: true },
    });
    // Fetch both first and last pages
    await dispatch(fetchTimeline(focusEventId));
    dispatch(setTimelineInterval());
    dispatch({
      type: SET_INITIAL_LOADING,
      payload: { loading: false },
    });
  };
};

export const setTimelineInterval = () => {
  return async (dispatch, getState, config) => {
    const intervalAlreadySet = intervalManager.intervalId;

    if (!intervalAlreadySet) {
      const intervalId = setInterval(
        () => timelineReload(dispatch, getState, config),
        config.refreshIntervalMs
      );
      intervalManager.setIntervalId(intervalId);
    }
  };
};

export const clearTimelineInterval = () => {
  return () => {
    intervalManager.resetInterval();
  };
};

export const submitComment = (content, format, files) => {
  return async (dispatch, getState, config) => {
    const { request } = getState();
    const { size } = config.defaultQueryParams;

    dispatch(clearTimelineInterval());

    dispatch({
      type: SET_SUBMITTING,
      payload: { submitting: true },
    });

    const payload = payloadSerializer(content, format || "html", files);

    try {
      /* Because of the delay in ES indexing we need to handle the updated state on the client-side until it is ready to be retrieved from the server.*/

      const response = await config.requestsApi.submitComment(payload);

      try {
        deleteDraftComment(request.data.id);
        deleteDraftFiles(request.data.id);
      } catch (e) {
        console.warn("Failed to delete saved comment:", e);
      }

      dispatch({
        type: APPEND_TO_LAST_PAGE,
        payload: {
          hit: response.data,
          pageSize: size,
        },
      });

      dispatch({
        type: SET_TOTAL_HITS,
        payload: {
          increaseCountBy: 1,
        },
      });

      dispatch({
        type: SET_SUBMITTING,
        payload: { submitting: false },
      });

      dispatch({
        type: PARENT_SET_DRAFT_CONTENT,
        payload: { content: "" },
      });

      dispatch({
        type: PARENT_SET_DRAFT_FILES,
        payload: { files: [] },
      });

      dispatch(setTimelineInterval());
    } catch (error) {
      dispatch({
        type: HAS_SUBMISSION_ERROR,
        payload: errorSerializer(error),
      });

      dispatch(setTimelineInterval());
    }
  };
};
