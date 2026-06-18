/*
 * SPDX-FileCopyrightText: 2025 CERN.
 * SPDX-License-Identifier: MIT
 */

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
