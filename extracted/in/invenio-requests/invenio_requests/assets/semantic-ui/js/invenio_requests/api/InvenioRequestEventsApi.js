// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { http } from "react-invenio-forms";
import { i18next } from "@translations/invenio_requests/i18next";

export class RequestEventsLinksExtractor {
  #links;

  constructor(links) {
    this.#links = links;
  }

  get eventUrl() {
    if (!this.#links.self) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Self",
        })
      );
    }
    return this.#links.self;
  }

  get eventHtmlUrl() {
    if (!this.#links.self_html) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Self HTML",
        })
      );
    }
    return this.#links.self_html;
  }

  get repliesUrl() {
    if (!this.#links.replies) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Replies",
        })
      );
    }
    return this.#links.replies;
  }

  get focusedRepliesUrl() {
    if (!this.#links.replies_focused) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Focused replies",
        })
      );
    }
    return this.#links.replies_focused;
  }

  get replyUrl() {
    if (!this.#links.reply) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Reply",
        })
      );
    }
    return this.#links.reply;
  }
}

export class InvenioRequestEventsApi {
  #links;

  constructor(links) {
    this.#links = links;
  }

  getComment = async () => {
    return await http.get(this.#links.eventUrl, { params: { expand: 1 } });
  };

  updateComment = async (payload) => {
    return http.put(this.#links.eventUrl, payload, { params: { expand: 1 } });
  };

  deleteComment = async () => {
    return await http.delete(this.#links.eventUrl);
  };

  getReplies = async (params) => {
    return await http.get(this.#links.repliesUrl, {
      params: {
        expand: 1,
        ...params,
      },
    });
  };

  getRepliesFocused = async (focusReplyEventId, params) => {
    return await http.get(this.#links.focusedRepliesUrl, {
      params: {
        expand: 1,
        focus_event_id: focusReplyEventId,
        ...params,
      },
    });
  };

  submitReply = async (payload) => {
    return await http.post(this.#links.replyUrl, payload, {
      params: { expand: 1 },
    });
  };
}
