// This file is part of InvenioRequests
// Copyright (C) 2026 CERN.
//
// Invenio Requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import Overridable from "react-overridable";
import React, { useMemo } from "react";
import PropTypes from "prop-types";
import _cloneDeep from "lodash/cloneDeep";
import LoadMore from "./LoadMore";
import RequestsFeed from "../components/RequestsFeed";
import TimelineCommentEventControlled from "../timelineCommentEventControlled/TimelineCommentEventControlled.js";
import { Divider } from "semantic-ui-react";

const TimelineFeedElementRequestFeed = ({
  userAvatar,
  permissions,
  request,
  updateComment,
  deleteComment,
  parentRequestEvent,
  isBeforeLoadMore,
  isAfterLoadMore,
  openConfirmModal,
  hits,
  appendCommentContent,
}) => {
  return (
    <RequestsFeed
      className={`${isBeforeLoadMore ? "before-load-more" : ""}${
        isAfterLoadMore ? " after-load-more" : ""
      }`}
    >
      {hits.map((event, index) => (
        <TimelineCommentEventControlled
          key={event.id}
          event={event}
          openConfirmModal={openConfirmModal}
          userAvatar={userAvatar}
          allowQuote={false}
          allowReply={permissions.can_reply_comment}
          request={request}
          permissions={permissions}
          updateComment={updateComment}
          deleteComment={deleteComment}
          appendCommentContent={(content) => appendCommentContent(event.id, content)}
          isReply={!!parentRequestEvent}
          isBeforeLoadMore={isBeforeLoadMore && index === hits.length - 1}
        />
      ))}
    </RequestsFeed>
  );
};

TimelineFeedElementRequestFeed.propTypes = {
  userAvatar: PropTypes.string,
  permissions: PropTypes.object.isRequired,
  request: PropTypes.object.isRequired,
  updateComment: PropTypes.func.isRequired,
  deleteComment: PropTypes.func.isRequired,
  parentRequestEvent: PropTypes.object,
  isBeforeLoadMore: PropTypes.bool.isRequired,
  isAfterLoadMore: PropTypes.bool.isRequired,
  openConfirmModal: PropTypes.func.isRequired,
  hits: PropTypes.array.isRequired,
  appendCommentContent: PropTypes.func.isRequired,
};

TimelineFeedElementRequestFeed.defaultProps = {
  parentRequestEvent: null,
  userAvatar: null,
};

/**
 * Converts the Redux `hits` object into a series of "instructions" for rendering contiguous feed blocks
 * and load-more buttons. The instructions are then rendered into React elements. We don't directly generate
 * React elements here to allow easily appending contiguous children to the same RequestFeed and also to
 * somewhat preserve the declarativeness of React.
 */
const TimelineFeedElements = ({
  hits,
  pageNumbers,
  size,
  totalHits,
  loadPage,
  userAvatar,
  permissions,
  request,
  parentRequestEvent,
  updateComment,
  deleteComment,
  appendCommentContent,
  openConfirmModal,
}) => {
  const isReplyTimeline = !!parentRequestEvent;

  const feedElements = useMemo(() => {
    // Clone the hits object to avoid accidentally modifying the Redux store
    const clonedHits = _cloneDeep(hits);

    const reversePages = isReplyTimeline;
    let iterPageNumbers = pageNumbers;
    if (reversePages) {
      iterPageNumbers = iterPageNumbers.toReversed();
    }

    // Exclude hits on the virtual "page zero", which are new comments added by the user since page load.
    // We do not need to count these for the purpose of the load more buttons.
    const pageZeroHits = iterPageNumbers.includes(0) ? clonedHits[0].length : 0;
    const iterTotalHits = totalHits - pageZeroHits;

    const elements = [];
    iterPageNumbers.forEach((pageNumber, i) => {
      // If we are on the top-most page
      if (i === 0) {
        if (!reversePages) {
          // If rendering in normal order, this means we have some non-loaded pages at the top of the page.
          if (pageNumber > 1) {
            elements.push({
              type: "LoadMore",
              page: pageNumber - 1,
              count: (pageNumber - 1) * size,
              key: "LoadMore-" + pageNumber,
              isLoadingAbove: false,
            });
          }

          elements.push({
            type: "RequestFeed",
            children: clonedHits[pageNumber],
            key: "RequestFeed-" + pageNumber,
          });
        } else {
          // We are not starting from page 1, so we need to figure out how many pages have not yet been loaded
          // at the top of the page. If it's not zero, we need a button.
          const lastPage = Math.ceil(iterTotalHits / size);
          const lastLoadedPage = iterPageNumbers[0];
          const difference = lastPage - lastLoadedPage;
          if (difference > 0) {
            elements.push({
              type: "LoadMore",
              page: lastLoadedPage + 1,
              count: iterTotalHits - lastLoadedPage * size,
              key: "LoadMore-" + (lastLoadedPage + 1),
              isLoadingAbove: false,
            });
          }
          elements.push({
            type: "RequestFeed",
            children: clonedHits[pageNumber],
            key: "RequestFeed-" + pageNumber,
          });
        }

        return;
      }

      // Check if there is a gap in the page numbers, and add a button if there is.
      const previousPageNumber = iterPageNumbers[i - 1];
      const difference = reversePages
        ? previousPageNumber - pageNumber
        : pageNumber - previousPageNumber;
      if (difference > 1) {
        const pageToLoad = reversePages ? pageNumber + 1 : pageNumber - 1;
        elements.push({
          type: "LoadMore",
          page: pageToLoad,
          count: (difference - 1) * size,

          key: "LoadMore-" + pageNumber,
          isLoadingAbove: false,
        });
        elements.push({
          type: "RequestFeed",
          children: clonedHits[pageNumber],
          key: "RequestFeed-" + pageNumber,
        });
        return;
      }

      // Append the children of this page to the previous RequestFeed.
      // To preserve the correct margins, padding, etc, we want to add the items to an
      // existing RequestFeed instead of creating a new one.
      elements[elements.length - 1].children.push(...clonedHits[pageNumber]);
    });

    return elements;
  }, [hits, totalHits, pageNumbers, size, isReplyTimeline]);

  return (
    // For CSS, we need this to be inside a div
    <div>
      {feedElements.map((el, index) =>
        el.type === "LoadMore" ? (
          <LoadMore
            key={el.key}
            count={el.count}
            onClick={() => loadPage(el.page)}
            isTiny={isReplyTimeline}
            isLoadingAbove={el.isLoadingAbove}
          />
        ) : (
          <TimelineFeedElementRequestFeed
            key={el.key}
            userAvatar={userAvatar}
            permissions={permissions}
            request={request}
            parentRequestEvent={parentRequestEvent}
            updateComment={updateComment}
            deleteComment={deleteComment}
            appendCommentContent={appendCommentContent}
            isBeforeLoadMore={
              index < feedElements.length - 1 &&
              feedElements[index + 1].type === "LoadMore"
            }
            isAfterLoadMore={index > 0 && feedElements[index - 1].type === "LoadMore"}
            openConfirmModal={openConfirmModal}
            hits={el.children}
          />
        )
      )}
      {isReplyTimeline ? <Divider /> : null}
    </div>
  );
};

TimelineFeedElements.propTypes = {
  hits: PropTypes.object.isRequired,
  pageNumbers: PropTypes.array.isRequired,
  size: PropTypes.number.isRequired,
  totalHits: PropTypes.number.isRequired,
  loadPage: PropTypes.func.isRequired,
  userAvatar: PropTypes.string,
  permissions: PropTypes.object.isRequired,
  request: PropTypes.object.isRequired,
  parentRequestEvent: PropTypes.object,
  updateComment: PropTypes.func.isRequired,
  deleteComment: PropTypes.func.isRequired,
  appendCommentContent: PropTypes.func.isRequired,
  openConfirmModal: PropTypes.func.isRequired,
};
TimelineFeedElements.defaultProps = {
  userAvatar: null,
  parentRequestEvent: null,
};

export default Overridable.component(
  "InvenioRequests.TimelineFeed.Elements",
  TimelineFeedElements
);
