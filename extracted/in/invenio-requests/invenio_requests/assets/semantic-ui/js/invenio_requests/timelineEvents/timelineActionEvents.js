// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_requests/i18next";
import React from "react";
import TimelineActionEvent from "../components/TimelineActionEvent";
import PropTypes from "prop-types";

export const TimelineAcceptEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="check circle"
    iconColor="positive"
    event={event}
    eventContent={i18next.t("accepted this request")}
  />
);

TimelineAcceptEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineDeclineEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    event={event}
    eventContent={i18next.t("declined this request")}
    iconColor="negative"
  />
);

TimelineDeclineEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineExpireEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="calendar times"
    event={event}
    eventContent={i18next.t("this request expired")}
    iconColor="negative"
  />
);

TimelineExpireEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineCancelEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    event={event}
    eventContent={i18next.t("cancelled this request")}
    iconColor="negative"
  />
);

TimelineCancelEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineUnknownEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    iconColor="negative"
    event={event}
    eventContent={i18next.t("unknown event")}
  />
);

TimelineUnknownEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineReviewersUpdatedEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="user circle"
    iconColor="grey"
    event={event}
    eventContent={i18next.t(event.payload.content) || i18next.t("updated reviewers")}
  />
);

TimelineReviewersUpdatedEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineCommentDeletionEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="erase"
    iconColor="grey"
    event={event}
    eventContent={i18next.t("deleted a comment")}
  />
);

TimelineCommentDeletionEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineLockRequestEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="lock"
    iconColor="grey"
    event={event}
    eventContent={i18next.t("locked this conversation")}
  />
);

TimelineLockRequestEvent.propTypes = {
  event: PropTypes.object.isRequired,
};

export const TimelineUnlockRequestEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="unlock"
    iconColor="grey"
    event={event}
    eventContent={i18next.t("unlocked this conversation")}
  />
);

TimelineUnlockRequestEvent.propTypes = {
  event: PropTypes.object.isRequired,
};
