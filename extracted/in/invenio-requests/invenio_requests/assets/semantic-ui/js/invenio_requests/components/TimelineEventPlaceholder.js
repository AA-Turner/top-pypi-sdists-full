import React from "react";
import RequestsFeed from "./RequestsFeed";
import { Placeholder, Feed } from "semantic-ui-react";
import Overridable from "react-overridable";
import PropTypes from "prop-types";

const TimelineEventPlaceholder = ({ isTiny }) => {
  return (
    <>
      {/* Comment placeholder */}
      <RequestsFeed.Item isReply={isTiny}>
        <RequestsFeed.Content>
          <Placeholder className="requests-avatar-container requests-placeholder-avatar">
            <Placeholder.Image />
          </Placeholder>
          <RequestsFeed.Event isReply={isTiny}>
            <Placeholder fluid>
              <Placeholder.Paragraph>
                <Placeholder.Line />
                <Placeholder.Line />
                <Placeholder.Line />
              </Placeholder.Paragraph>
            </Placeholder>
          </RequestsFeed.Event>
        </RequestsFeed.Content>
      </RequestsFeed.Item>

      {/* Log/Action line placeholder */}
      {!isTiny ? (
        <RequestsFeed.Item>
          <RequestsFeed.Content isEvent>
            <Placeholder className="requests-placeholder-event-icon">
              <Placeholder.Image />
            </Placeholder>
            <RequestsFeed.Event isActionEvent>
              <Feed.Content>
                <Feed.Summary className="flex">
                  <Placeholder className="requests-placeholder-avatar-icon">
                    <Placeholder.Image />
                  </Placeholder>
                  <Feed.Date>
                    <Placeholder>
                      <Placeholder.Line className="requests-placeholder-summary-line" />
                    </Placeholder>
                  </Feed.Date>
                </Feed.Summary>
              </Feed.Content>
            </RequestsFeed.Event>
          </RequestsFeed.Content>
        </RequestsFeed.Item>
      ) : null}
    </>
  );
};

TimelineEventPlaceholder.propTypes = {
  isTiny: PropTypes.bool.isRequired,
};

export default Overridable.component(
  "InvenioRequests.TimelineEventPlaceholder",
  TimelineEventPlaceholder
);
