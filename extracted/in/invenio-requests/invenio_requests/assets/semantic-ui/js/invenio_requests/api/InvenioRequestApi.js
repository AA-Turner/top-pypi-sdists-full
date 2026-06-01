// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import _isEmpty from "lodash/isEmpty";
import { http } from "react-invenio-forms";
import { i18next } from "@translations/invenio_requests/i18next";

export class RequestLinksExtractor {
  #urls;

  constructor(request) {
    if (!request?.links) {
      throw TypeError(
        i18next.t("{{link_name}} links are undefined. Please refresh the page.", {
          link_name: "Request resource",
        })
      );
    }
    this.#urls = request.links;
  }

  get self() {
    return this.#urls.self;
  }

  get timeline() {
    if (!this.#urls.timeline) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Timeline",
        })
      );
    }
    return this.#urls.timeline;
  }

  get timelineFocused() {
    if (!this.#urls.timeline_focused) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Focused timeline",
        })
      );
    }
    return this.#urls.timeline_focused;
  }

  get comments() {
    if (!this.#urls.comments) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Comments",
        })
      );
    }
    return this.#urls.comments;
  }

  get actions() {
    if (!this.#urls.actions) {
      throw TypeError(
        i18next.t("{{link_name}} link missing from resource.", {
          link_name: "Actions",
        })
      );
    }
    return this.#urls.actions;
  }

  get lock() {
    if (!this.#urls.lock) {
      throw TypeError("Lock link missing from resource.");
    }
    return this.#urls.lock;
  }

  get unlock() {
    if (!this.#urls.unlock) {
      throw TypeError("Unlock link missing from resource.");
    }
    return this.#urls.unlock;
  }
}

export class InvenioRequestsAPI {
  #urls;

  constructor(requestLinksExtractor) {
    this.#urls = requestLinksExtractor;
  }

  get availableRequestStatuses() {
    return ["accepted", "declined", "expired", "cancelled"];
  }

  getTimeline = async (params) => {
    return await http.get(this.#urls.timeline, {
      params: {
        expand: 1,
        ...params,
      },
    });
  };

  getTimelineFocused = async (focusEventId, params) => {
    return await http.get(this.#urls.timelineFocused, {
      params: {
        expand: 1,
        focus_event_id: focusEventId,
        ...params,
      },
    });
  };

  getRequest = async () => {
    return await http.get(this.#urls.self, { params: { expand: 1 } });
  };

  submitComment = async (payload) => {
    return await http.post(this.#urls.comments, payload, {
      params: { expand: 1 },
    });
  };

  addReviewer = async (reviewers) => {
    return await http.put(this.#urls.self, {
      reviewers: reviewers.map((r) => {
        return "user" in r ? { user: r.id } : { group: r.id };
      }),
    });
  };

  performAction = async (action, commentContent = null, files = []) => {
    let payload = {};
    if (!_isEmpty(commentContent)) {
      payload = {
        payload: {
          content: commentContent,
          format: "html",
          files: files,
        },
      };
    }
    return await http.post(this.#urls.actions[action], payload, {
      params: { expand: 1 },
    });
  };

  lockRequest = async () => {
    return await http.get(this.#urls.lock);
  };

  unlockRequest = async () => {
    return await http.get(this.#urls.unlock);
  };
}
