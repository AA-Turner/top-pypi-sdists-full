// This file is part of InvenioRequests
// Copyright (C) 2022-2026 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
// Copyright (C) 2025 Graz University of Technology.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import PropTypes from "prop-types";
import React, { Component } from "react";
import Overridable from "react-overridable";
import { Container, Message, Icon, Button } from "semantic-ui-react";
import Error from "../components/Error";
import Loader from "../components/Loader";
import { DeleteConfirmationModal } from "../components/modals/DeleteConfirmationModal";
import TimelineCommentEditor from "../timelineCommentEditor/TimelineCommentEditor.js";
import { i18next } from "@translations/invenio_requests/i18next";
import FakeInput from "../components/FakeInput.js";
import TimelineFeedElements from "./TimelineFeedElements.js";

const TimelineContainerElement = ({ children, isReplyTimeline }) => {
  if (isReplyTimeline) {
    return <div className="requests-reply-container">{children}</div>;
  } else {
    return (
      <Container id="requests-timeline" className="ml-0-mobile mr-0-mobile">
        {children}
      </Container>
    );
  }
};

TimelineContainerElement.propTypes = {
  children: PropTypes.node.isRequired,
  isReplyTimeline: PropTypes.bool.isRequired,
};

class TimelineFeed extends Component {
  constructor(props) {
    super(props);

    this.state = {
      modalOpen: false,
      modalAction: null,
      expanded: true,
    };
  }

  loadPage = (page) => {
    const { fetchPage } = this.props;
    return fetchPage(page);
  };

  onOpenModal = (action) => {
    this.setState({ modalOpen: true, modalAction: action });
  };

  onRepliesClick = () => {
    this.setState((state) => ({ expanded: !state.expanded }));
  };

  onCancelClick = () => {
    const { setIsReplying, clearDraft } = this.props;
    setIsReplying(false);
    clearDraft();
  };

  onFakeInputActivate = () => {
    const { setIsReplying } = this.props;
    setIsReplying(true);
  };

  appendCommentContent = (eventId, content) => {
    const { appendCommentContent, parentRequestEvent } = this.props;
    if (parentRequestEvent) {
      appendCommentContent(parentRequestEvent.id, content);
    } else {
      appendCommentContent(eventId, content);
    }
  };

  render() {
    const {
      initialLoading,
      error,
      userAvatar,
      request,
      permissions,
      warning,
      parentRequestEvent,
      isSubmitting,
      commentContent,
      storedCommentContent,
      appendedCommentContent,
      setCommentContent,
      restoreCommentContent,
      setCommentFiles,
      restoreCommentFiles,
      submissionError,
      submitComment,
      totalHits,
      replying,
      hits,
      pageNumbers,
      size,
      updateComment,
      deleteComment,
      draftFiles,
    } = this.props;
    const { modalOpen, modalAction, expanded } = this.state;

    const isReplyTimeline = parentRequestEvent !== null;
    const hasHits = totalHits !== 0;

    return (
      <Loader isLoading={initialLoading}>
        <Error error={error}>
          <Overridable id="TimelineFeed.layout" {...this.props}>
            <TimelineContainerElement isReplyTimeline={isReplyTimeline}>
              {warning && (
                <Message visible warning>
                  <p>
                    <Icon name="warning sign" />
                    {warning}
                  </p>
                </Message>
              )}

              {!isReplyTimeline ? (
                <Overridable
                  id="TimelineFeed.header"
                  request={request}
                  permissions={permissions}
                />
              ) : null}

              {isReplyTimeline && hasHits ? (
                <Button
                  size="tiny"
                  onClick={this.onRepliesClick}
                  className="text-only requests-reply-expand"
                >
                  <Icon
                    name={`caret ${expanded ? "down" : "right"}`}
                    className="requests-reply-caret"
                  />
                  {i18next.t("Replies")}
                  <span className="requests-reply-count ml-5">{totalHits}</span>
                </Button>
              ) : null}

              {expanded && hasHits ? (
                <TimelineFeedElements
                  hits={hits}
                  pageNumbers={pageNumbers}
                  size={size}
                  totalHits={totalHits}
                  loadPage={this.loadPage}
                  userAvatar={userAvatar}
                  permissions={permissions}
                  request={request}
                  parentRequestEvent={parentRequestEvent}
                  updateComment={updateComment}
                  deleteComment={deleteComment}
                  appendCommentContent={this.appendCommentContent}
                  openConfirmModal={this.onOpenModal}
                />
              ) : null}

              {!replying && isReplyTimeline ? (
                <FakeInput
                  placeholder={i18next.t("Write a reply")}
                  userAvatar={userAvatar}
                  onActivate={this.onFakeInputActivate}
                  className={!hasHits || !expanded ? "mt-10" : undefined}
                  disabled={!permissions.can_reply_comment}
                />
              ) : (
                <TimelineCommentEditor
                  isLoading={isSubmitting}
                  commentContent={commentContent}
                  storedCommentContent={storedCommentContent}
                  appendedCommentContent={appendedCommentContent}
                  setCommentContent={setCommentContent}
                  restoreCommentContent={restoreCommentContent}
                  files={draftFiles}
                  restoreCommentFiles={restoreCommentFiles}
                  setCommentFiles={setCommentFiles}
                  error={submissionError}
                  submitComment={submitComment}
                  userAvatar={userAvatar}
                  canCreateComment={
                    isReplyTimeline
                      ? permissions.can_reply_comment
                      : permissions.can_create_comment
                  }
                  // This is a custom autoFocus prop, not the browser one
                  // eslint-disable-next-line jsx-a11y/no-autofocus
                  autoFocus={isReplyTimeline}
                  saveButtonLabel={
                    isReplyTimeline ? i18next.t("Reply") : i18next.t("Comment")
                  }
                  saveButtonIcon={isReplyTimeline ? "reply" : "send"}
                  onCancel={isReplyTimeline ? this.onCancelClick : undefined}
                  requestId={request.id}
                />
              )}

              <DeleteConfirmationModal
                open={modalOpen}
                action={modalAction}
                onOpen={() => this.setState({ modalOpen: true })}
                onClose={() => this.setState({ modalOpen: false })}
              />
            </TimelineContainerElement>
          </Overridable>
        </Error>
      </Loader>
    );
  }
}

TimelineFeed.propTypes = {
  hits: PropTypes.object.isRequired,
  pageNumbers: PropTypes.array.isRequired,
  totalHits: PropTypes.number.isRequired,
  fetchPage: PropTypes.func.isRequired,
  error: PropTypes.string,
  isSubmitting: PropTypes.bool,
  size: PropTypes.number.isRequired,
  userAvatar: PropTypes.string,
  request: PropTypes.object.isRequired,
  permissions: PropTypes.object.isRequired,
  initialLoading: PropTypes.bool.isRequired,
  warning: PropTypes.string,
  parentRequestEvent: PropTypes.object,
  commentContent: PropTypes.string.isRequired,
  storedCommentContent: PropTypes.string,
  appendedCommentContent: PropTypes.string,
  setCommentContent: PropTypes.func.isRequired,
  restoreCommentContent: PropTypes.func.isRequired,
  draftFiles: PropTypes.array.isRequired,
  restoreCommentFiles: PropTypes.func.isRequired,
  setCommentFiles: PropTypes.func.isRequired,
  submissionError: PropTypes.string,
  submitComment: PropTypes.func.isRequired,
  updateComment: PropTypes.func.isRequired,
  deleteComment: PropTypes.func.isRequired,
  appendCommentContent: PropTypes.func.isRequired,
  replying: PropTypes.bool,
  setIsReplying: PropTypes.func,
  clearDraft: PropTypes.func,
};

TimelineFeed.defaultProps = {
  error: null,
  isSubmitting: false,
  userAvatar: "",
  warning: null,
  parentRequestEvent: null,
  storedCommentContent: null,
  submissionError: null,
  replying: false,
  setIsReplying: null,
  appendedCommentContent: null,
  clearDraft: null,
};

export default Overridable.component("TimelineFeed", TimelineFeed);
