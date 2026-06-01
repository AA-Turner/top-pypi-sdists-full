// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React, { Component, createRef } from "react";
import { Image } from "react-invenio-forms";
import Overridable from "react-overridable";
import { Divider, Container, Dropdown, Feed, Icon } from "semantic-ui-react";
import { CancelButton, SaveButton } from "../components/Buttons";
import Error from "../components/Error";
import { RichEditor } from "react-invenio-forms";
import RequestsFeed from "../components/RequestsFeed";
import TimelineEventBody from "../components/TimelineEventBody";
import { toRelativeTime } from "react-invenio-forms";
import { isEventSelected } from "./utils";
import { RequestEventsLinksExtractor } from "../api/InvenioRequestEventsApi.js";
import { InvenioRequestFilesApi } from "../api/InvenioRequestFilesApi.js";
import TimelineFeedReplies from "../timelineCommentReplies/index.js";

class TimelineCommentEvent extends Component {
  constructor(props) {
    super(props);

    const { event } = props;

    this.state = {
      commentContent: event?.payload?.content,
      files: event?.expanded?.files || [],
      isSelected: false,
    };
    this.ref = createRef(null);
  }

  componentDidMount() {
    window.addEventListener("hashchange", this.updateSelected);
    this.updateSelected();
  }

  componentWillUnmount() {
    window.removeEventListener("hashchange", this.updateSelected);
  }

  updateSelected = () => {
    const { event } = this.props;
    const isSelected = isEventSelected(event);
    this.setState({ isSelected });
    if (isSelected && this.ref.current) {
      // We need to manually focus the element since it will have been loaded after the initial page load.
      this.ref.current.scrollIntoView({ behaviour: "smooth" });
      this.ref.current.focus();
    }
  };

  eventToType = ({ type, payload }) => {
    switch (type) {
      case "L":
        if (payload?.event === "comment_deleted") {
          return "comment";
        }
        return payload?.event || "unknown";
      case "C":
        return "comment";
      case "R":
        return payload?.event || "unknown";
      default:
        return "unknown";
    }
  };

  copyLink() {
    const {
      event: { links },
    } = this.props;
    navigator.clipboard.writeText(new RequestEventsLinksExtractor(links).eventHtmlUrl);
  }

  /**
   * Append a quote of the comment's content to the new comment in the editor.
   *
   * @param {string} [text] - The text to quote
   */
  quoteReply = (text) => {
    const { appendCommentContent } = this.props;
    appendCommentContent(`<blockquote>${text}</blockquote><br />`);
  };

  onFileUpload = async (filename, payload, options) => {
    const client = new InvenioRequestFilesApi();
    const { request } = this.props;
    return await client.uploadFile(request.id, filename, payload, options);
  };

  render() {
    const {
      isLoading,
      isEditing,
      error,
      event,
      updateComment,
      deleteComment,
      toggleEditMode,
      userAvatar: currentUserAvatar,
      isReply,
      allowQuoteReply,
      allowCopyLink,
      request,
      isBeforeLoadMore,
    } = this.props;
    const { commentContent, files, isSelected } = this.state;

    const commentHasBeenDeleted = event?.payload?.event === "comment_deleted";

    // A deleted comment is already visually distinct so doesn't need an additional "edited" label
    const commentHasBeenEdited =
      event?.revision_id > 1 && event?.payload && !commentHasBeenDeleted;

    const canDelete = event?.permissions?.can_delete_comment;
    const canUpdate = event?.permissions?.can_update_comment;
    const canReply = event?.permissions?.can_reply_comment;

    const createdBy = event.created_by;
    const isUser = "user" in createdBy;
    const isEmail = "email" in createdBy;
    const expandedCreatedBy = event.expanded?.created_by;
    let userAvatar,
      userName = null;
    if (isUser) {
      userAvatar = (
        <RequestsFeed.Avatar
          src={expandedCreatedBy.links.avatar}
          as={Image}
          circular
          hasLine={isReply}
          lineFade={isBeforeLoadMore}
        />
      );
      userName = expandedCreatedBy.profile?.full_name || expandedCreatedBy.username;
    } else if (isEmail) {
      userAvatar = <Icon size="large" name="user circle outline" />;
      userName = createdBy.email;
    }

    const eventSelfURL = new URL(
      new RequestEventsLinksExtractor(event.links).eventHtmlUrl
    );
    // Remove the # character from the start of the hash
    const eventItemId = eventSelfURL.hash.substring(1);

    return (
      <Overridable id={`TimelineEvent.layout.${this.eventToType(event)}`} event={event}>
        <RequestsFeed.Item
          id={eventItemId}
          ref={this.ref}
          selected={isSelected}
          isReply={isReply}
        >
          <RequestsFeed.Content>
            {userAvatar}
            <RequestsFeed.Event isReply={isReply}>
              <Feed.Content>
                {(!commentHasBeenDeleted || allowCopyLink) && (
                  <Dropdown
                    icon="ellipsis horizontal"
                    className="right-floated"
                    direction="left"
                    aria-label={i18next.t("Actions")}
                  >
                    <Dropdown.Menu>
                      {allowQuoteReply && !commentHasBeenDeleted && (
                        <Dropdown.Item
                          onClick={() => this.quoteReply(event.payload.content, true)}
                        >
                          {i18next.t("Quote reply")}
                        </Dropdown.Item>
                      )}
                      {/* We still allow copying a link to a deleted comment in case it has replies for example */}
                      {allowCopyLink && (
                        <Dropdown.Item onClick={() => this.copyLink()}>
                          {i18next.t("Copy link")}
                        </Dropdown.Item>
                      )}
                      {canUpdate && !commentHasBeenDeleted && (
                        <Dropdown.Item onClick={() => toggleEditMode()}>
                          {i18next.t("Edit")}
                        </Dropdown.Item>
                      )}
                      {canDelete && !commentHasBeenDeleted && (
                        <Dropdown.Item onClick={() => deleteComment()}>
                          {i18next.t("Delete")}
                        </Dropdown.Item>
                      )}
                    </Dropdown.Menu>
                  </Dropdown>
                )}
                <Feed.Summary>
                  <b>{userName}</b>
                  <Feed.Date>
                    {i18next.t("commented {{commentTime}}", {
                      commentTime: toRelativeTime(event.created, i18next.language),
                    })}
                  </Feed.Date>
                </Feed.Summary>

                <Feed.Extra text={!isEditing}>
                  {error && <Error error={error} />}

                  {isEditing ? (
                    <RichEditor
                      initialValue={event?.payload?.content}
                      inputValue={commentContent}
                      onEditorChange={(event, editor) => {
                        this.setState({ commentContent: editor.getContent() });
                      }}
                      files={files}
                      onFilesChange={(files) => {
                        this.setState({ files: files });
                      }}
                      // This is an existing comment, so we do not delete the file via the API.
                      onFileUpload={this.onFileUpload}
                      minHeight={150}
                    />
                  ) : (
                    <TimelineEventBody
                      payload={{ ...event?.payload, files: event?.expanded?.files }}
                      quoteReply={this.quoteReply}
                    />
                  )}

                  {isEditing && (
                    <Container fluid className="mt-15" textAlign="right">
                      <CancelButton onClick={() => toggleEditMode()} />
                      <SaveButton
                        onClick={() => updateComment(commentContent, "html", files)}
                        loading={isLoading}
                      />
                    </Container>
                  )}
                </Feed.Extra>
                {commentHasBeenEdited && <Feed.Meta>{i18next.t("Edited")}</Feed.Meta>}
              </Feed.Content>

              {!isReply ? (
                <>
                  <Divider className="requests-reply-top-divider" />
                  <TimelineFeedReplies
                    parentRequestEvent={event}
                    userAvatar={currentUserAvatar}
                    allowReply={canReply}
                    request={request}
                  />
                </>
              ) : null}
            </RequestsFeed.Event>
          </RequestsFeed.Content>
        </RequestsFeed.Item>
      </Overridable>
    );
  }
}

TimelineCommentEvent.propTypes = {
  event: PropTypes.object.isRequired,
  request: PropTypes.object.isRequired,
  deleteComment: PropTypes.func.isRequired,
  updateComment: PropTypes.func.isRequired,
  appendCommentContent: PropTypes.func.isRequired,
  toggleEditMode: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
  isEditing: PropTypes.bool,
  error: PropTypes.string,
  userAvatar: PropTypes.string,
  isReply: PropTypes.bool,
  isBeforeLoadMore: PropTypes.bool.isRequired,
  allowQuoteReply: PropTypes.bool,
  allowCopyLink: PropTypes.bool,
};

TimelineCommentEvent.defaultProps = {
  isLoading: false,
  isEditing: false,
  error: undefined,
  userAvatar: "",
  isReply: false,
  allowQuoteReply: true,
  allowCopyLink: true,
};

export default Overridable.component("TimelineEvent", TimelineCommentEvent);
