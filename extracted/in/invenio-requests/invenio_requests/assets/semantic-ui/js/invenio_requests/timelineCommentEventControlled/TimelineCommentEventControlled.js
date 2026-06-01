// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { TimelineEvent } from "../timelineEvents";
import { errorSerializer } from "../api/serializers";
import Overridable from "react-overridable";

class TimelineCommentEventControlled extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      isEditing: false,
      error: null,
    };
  }

  toggleEditMode = () => {
    const { isEditing } = this.state;
    this.setState({ isEditing: !isEditing, error: null });
  };

  updateComment = async (content, format, files) => {
    const { updateComment, event } = this.props;

    if (!content) return;

    this.setState({
      isLoading: true,
    });

    try {
      await updateComment({ content, format, files, requestEventData: event });

      this.setState({
        isLoading: false,
        isEditing: false,
        error: null,
      });
    } catch (error) {
      this.setState({
        isLoading: false,
        isEditing: true,
        error: errorSerializer(error),
      });
    }
  };

  deleteComment = async () => {
    const { deleteComment, event, openConfirmModal } = this.props;

    openConfirmModal(() => deleteComment({ requestEventData: event }));
  };

  render() {
    const {
      event,
      userAvatar,
      isReply,
      appendCommentContent,
      allowQuoteReply,
      allowCopyLink,
      allowReply,
      request,
      isBeforeLoadMore,
    } = this.props;
    const { isLoading, isEditing, error } = this.state;

    return (
      <Overridable id="TimelineCommentEventControlled.layout">
        <TimelineEvent
          updateComment={this.updateComment}
          deleteComment={this.deleteComment}
          appendCommentContent={appendCommentContent}
          toggleEditMode={this.toggleEditMode}
          quote={this.quote}
          isLoading={isLoading}
          isEditing={isEditing}
          error={error}
          event={event}
          userAvatar={userAvatar}
          isReply={isReply}
          allowQuoteReply={allowQuoteReply}
          allowCopyLink={allowCopyLink}
          allowReply={allowReply}
          request={request}
          isBeforeLoadMore={isBeforeLoadMore}
        />
      </Overridable>
    );
  }
}

TimelineCommentEventControlled.propTypes = {
  event: PropTypes.object.isRequired,
  updateComment: PropTypes.func.isRequired,
  deleteComment: PropTypes.func.isRequired,
  appendCommentContent: PropTypes.func.isRequired,
  openConfirmModal: PropTypes.func.isRequired,
  userAvatar: PropTypes.string,
  isReply: PropTypes.bool,
  allowQuoteReply: PropTypes.bool,
  allowCopyLink: PropTypes.bool,
  allowReply: PropTypes.bool,
  request: PropTypes.object.isRequired,
  isBeforeLoadMore: PropTypes.bool.isRequired,
};

TimelineCommentEventControlled.defaultProps = {
  userAvatar: "",
  isReply: false,
  allowQuoteReply: true,
  allowCopyLink: true,
  allowReply: true,
};

export default Overridable.component(
  "TimelineCommentEventControlled",
  TimelineCommentEventControlled
);
