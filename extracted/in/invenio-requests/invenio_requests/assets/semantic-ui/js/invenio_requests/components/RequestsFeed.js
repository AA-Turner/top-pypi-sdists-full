// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import PropTypes from "prop-types";
import React, { forwardRef } from "react";
import { Image } from "react-invenio-forms";
import { Container, Feed, Icon } from "semantic-ui-react";

// Wrapper component for the custom styles being used inside the request events timeline
// Enables centralizing the styles and abstracts it away from the template
export const RequestsFeed = ({ children, className }) => (
  <Container className="requests-feed-container rich-input-content ml-0-mobile mr-0-mobile">
    <Feed className={className}>{children}</Feed>
  </Container>
);

RequestsFeed.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
};

RequestsFeed.defaultProps = {
  children: null,
  className: null,
};

export const RequestEventItem = forwardRef(function RequestEventItem(
  { id, children, selected, isReply },
  ref
) {
  return (
    <div
      className={`requests-event-item${selected ? " selected" : ""}`}
      id={id}
      ref={ref}
    >
      <div className={`requests-event-container${isReply ? " reply" : ""}`}>
        {children}
      </div>
    </div>
  );
});

RequestEventItem.propTypes = {
  id: PropTypes.string,
  children: PropTypes.node,
  selected: PropTypes.bool,
  isReply: PropTypes.bool,
};

RequestEventItem.defaultProps = {
  id: null,
  children: null,
  selected: false,
  isReply: false,
};

export const RequestEventInnerContainer = ({ children, isEvent }) => (
  <div className={`requests-event-inner-container${isEvent ? " thread" : ""}`}>
    {children}
  </div>
);

RequestEventInnerContainer.propTypes = {
  children: PropTypes.node,
  isEvent: PropTypes.bool,
};

RequestEventInnerContainer.defaultProps = {
  children: null,
  isEvent: false,
};

export const RequestEventAvatarContainer = ({ src, hasLine, lineFade, ...uiProps }) => (
  <div
    className={`requests-avatar-container${hasLine ? " has-line" : ""}${
      lineFade ? " line-fade" : ""
    }`}
  >
    {src && <Image src={src} rounded avatar {...uiProps} />}
    {!src && <Icon size="large" name="user circle outline" />}
  </div>
);

RequestEventAvatarContainer.propTypes = {
  src: PropTypes.string,
  hasLine: PropTypes.bool,
  lineFade: PropTypes.bool,
};

RequestEventAvatarContainer.defaultProps = {
  src: null,
  hasLine: false,
  lineFade: false,
};

export const RequestEventItemIconContainer = ({ name, size, color }) => (
  <div className="requests-action-event-icon">
    <Icon name={name} size={size} className={color} />
  </div>
);

RequestEventItemIconContainer.propTypes = {
  name: PropTypes.string.isRequired,
  size: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
};

export const RequestEventItemBody = ({ isActionEvent, isReply, ...props }) => (
  <Feed.Event
    {...props}
    className={
      isActionEvent ? "requests-action-event" : isReply ? "requests-reply-event" : ""
    }
  />
);

RequestEventItemBody.propTypes = {
  isActionEvent: PropTypes.bool,
  isReply: PropTypes.bool,
};
RequestEventItemBody.defaultProps = {
  isActionEvent: false,
  isReply: false,
};

RequestsFeed.Content = RequestEventInnerContainer;
RequestsFeed.Avatar = RequestEventAvatarContainer;
RequestsFeed.Icon = RequestEventItemIconContainer;
RequestsFeed.Item = RequestEventItem;
RequestsFeed.Event = RequestEventItemBody;

export default RequestsFeed;
