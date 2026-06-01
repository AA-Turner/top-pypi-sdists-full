// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { clearTimelineInterval } from "../../timelineParent/state/actions";
import { payloadSerializer } from "../../api/serializers";

export const updateComment = ({
  content,
  format,
  files,
  parentRequestEventId,
  requestEventData,
  successEvent,
  loadingEvent,
}) => {
  return async (dispatch, _, config) => {
    dispatch(clearTimelineInterval());
    const commentsApi = config.requestEventsApi(requestEventData.links);

    const payload = payloadSerializer(content, format, files);

    dispatch({
      type: loadingEvent,
      payload: {
        parentRequestEventId,
      },
    });

    const response = await commentsApi.updateComment(payload);

    dispatch({
      type: successEvent,
      payload: {
        updatedComment: response.data,
        parentRequestEventId,
      },
    });

    return response.data;
  };
};

export const deleteComment = ({
  parentRequestEventId,
  requestEventData,
  loadingEvent,
  successEvent,
}) => {
  return async (dispatch, _, config) => {
    dispatch(clearTimelineInterval());
    const commentsApi = config.requestEventsApi(requestEventData.links);

    dispatch({
      type: loadingEvent,
      payload: {
        parentRequestEventId,
      },
    });

    const response = await commentsApi.deleteComment();

    dispatch({
      type: successEvent,
      payload: {
        deletedCommentId: requestEventData.id,
        parentRequestEventId,
      },
    });

    return response.data;
  };
};
