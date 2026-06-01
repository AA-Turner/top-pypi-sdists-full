// This file is part of InvenioRequests
// Copyright (C) 2025 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { RequestEventsLinksExtractor } from "../api/InvenioRequestEventsApi";

const COMMENT_PREFIX = "#commentevent-";

export const isEventSelected = (event) => {
  const eventUrl = new URL(new RequestEventsLinksExtractor(event.links).eventHtmlUrl);
  const currentUrl = new URL(window.location.href);
  return eventUrl.hash === currentUrl.hash;
};

export const getEventIdFromUrl = () => {
  const currentUrl = new URL(window.location.href);
  const hash = currentUrl.hash;
  let parentEventId = null;
  let replyEventId = null;

  if (hash.startsWith(COMMENT_PREFIX)) {
    let ids = hash.substring(COMMENT_PREFIX.length);
    ids = ids.split("_");
    parentEventId = ids[0];
    if (ids.length === 2) {
      replyEventId = ids[1];
    }
    return { parentEventId, replyEventId };
  }

  return null;
};
