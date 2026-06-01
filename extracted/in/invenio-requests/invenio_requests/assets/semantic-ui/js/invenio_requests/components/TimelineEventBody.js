// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Button, Popup, ButtonGroup } from "semantic-ui-react";
import { FilesList } from "react-invenio-forms";
import { i18next } from "@translations/invenio_requests/i18next";

const TimelineEventBody = ({ payload, quoteReply, collapsible, expandedByDefault }) => {
  return (
    <Overridable
      id="InvenioRequests.TimelineEventBody.layout"
      collapsible={collapsible}
      expandedByDefault={expandedByDefault}
    >
      <TimelineEventBodyContainer
        payload={payload}
        quoteReply={quoteReply}
        collapsible={collapsible}
        expandedByDefault={expandedByDefault}
      />
    </Overridable>
  );
};

TimelineEventBody.propTypes = {
  payload: PropTypes.object,
  quoteReply: PropTypes.func,
  collapsible: PropTypes.bool,
  expandedByDefault: PropTypes.bool,
};

TimelineEventBody.defaultProps = {
  payload: {},
  quoteReply: null,
  collapsible: true,
  expandedByDefault: false,
};

const TimelineEventBodyRender = React.forwardRef(
  (
    {
      refInner,
      isOverflowing,
      expanded,
      collapsible,
      toggleCollapsed,
      content,
      format,
      files,
    },
    ref
  ) => {
    const getCollapsibleClass = () => {
      if (!isOverflowing) return "";
      return expanded || !collapsible ? "expanded" : "overflowing";
    };

    return (
      <>
        <span
          ref={ref}
          className={`${
            collapsible ? "collapsible-comment" : ""
          } ${getCollapsibleClass()}`}
        >
          <span
            ref={refInner}
            className={collapsible ? "collapsible-comment-inner" : ""}
          >
            {format === "html" ? (
              <span dangerouslySetInnerHTML={{ __html: content }} />
            ) : (
              content
            )}
            {isOverflowing && collapsible && (
              <button
                type="button"
                className="ui tiny button text-only show-more"
                onClick={toggleCollapsed}
              >
                {expanded ? i18next.t("Show less") : i18next.t("Show more")}
              </button>
            )}
          </span>
        </span>
        {files !== undefined && <FilesList files={files} />}
      </>
    );
  }
);
TimelineEventBodyRender.displayName = "TimelineEventBodyRender";

TimelineEventBodyRender.propTypes = {
  refInner: PropTypes.object.isRequired,
  isOverflowing: PropTypes.bool.isRequired,
  expanded: PropTypes.bool.isRequired,
  collapsible: PropTypes.bool.isRequired,
  toggleCollapsed: PropTypes.func.isRequired,
  content: PropTypes.string.isRequired,
  format: PropTypes.string,
  files: PropTypes.array,
};

TimelineEventBodyRender.defaultProps = {
  format: null,
  files: [],
};

const TimelineEventBodyContainer = ({
  payload,
  quoteReply,
  collapsible,
  expandedByDefault,
}) => {
  const ref = useRef(null);
  const refInner = useRef(null);
  const [selectionRange, setSelectionRange] = useState(null);
  const [expanded, setExpanded] = useState(collapsible ? expandedByDefault : true);
  const [isOverflowing, setIsOverflowing] = useState(false);

  useEffect(() => {
    if (ref.current === null) return;

    const onSelectionChange = () => {
      const selection = window.getSelection();

      // anchorNode is where the user started dragging the mouse,
      // focusNode is where they finished. We make sure both nodes
      // are contained by the ref so we are sure that 100% of the selection
      // is within this comment event.
      const selectionIsContainedByRef =
        ref.current.contains(selection.anchorNode) &&
        ref.current.contains(selection.focusNode);

      if (
        !selectionIsContainedByRef ||
        selection.rangeCount === 0 ||
        // A "Caret" type e.g. should not trigger a tooltip
        selection.type !== "Range"
      ) {
        setSelectionRange(null);
        return;
      }

      setSelectionRange(selection.getRangeAt(0));
    };

    document.addEventListener("selectionchange", onSelectionChange);
    return () => document.removeEventListener("selectionchange", onSelectionChange);
  }, []);

  useEffect(() => {
    const el = refInner.current;
    if (!collapsible || !el) return;

    if (expanded) {
      // The collapsed comment height is 200px. If the comment is too short to need expanding but `expanded` is true
      // nonetheless, `el.scrollHeight` will still be less than 200, so the comment will not be overflowing.
      // This ensures the "Show less" button is hidden for comments where `expandedByDefault` is true but the comment
      // is too short to need expanding/collapsing.
      setIsOverflowing(el.scrollHeight > 200);
      // To prevent race conditions, we disable the resize observer once the comment is expanded.
      return;
    }

    const resizeObserver = new ResizeObserver((entries) => {
      if (entries.length !== 1) return;
      const el = entries[0].target;
      setIsOverflowing(el.scrollHeight > el.clientHeight);
    });

    resizeObserver.observe(el);
    return () => {
      resizeObserver.unobserve(el);
    };
  }, [collapsible, expanded]);

  const toggleCollapsed = () => {
    if (!collapsible) return;
    setExpanded((prev) => !prev);
  };

  const tooltipOffset = useMemo(() => {
    if (!selectionRange) return null;

    const selectionRect = selectionRange.getBoundingClientRect();
    const refRect = ref.current.getBoundingClientRect();

    // Offset set as [x, y] from the reference position.
    // E.g. `top left` is relative to [0,0] but `top center` is relative to [{center}, 0]
    return [selectionRect.x - refRect.x, -(selectionRect.y - refRect.y)];
  }, [selectionRange]);

  const onQuoteClick = useCallback(() => {
    if (!selectionRange || !quoteReply) return;
    const selectionString = selectionRange.toString();
    quoteReply(selectionString);
    window.getSelection().removeAllRanges();
  }, [selectionRange, quoteReply]);

  useEffect(() => {
    if (refInner.current !== null) {
      // Run MathJax typesetting only on the inner element that contains the content of the comment
      window.invenio?.onSearchResultsRendered([refInner.current]);
    }
  }, []);

  const { format, content, files, event } = payload;

  if (!quoteReply) {
    return (
      <TimelineEventBodyRender
        ref={ref}
        refInner={refInner}
        isOverflowing={isOverflowing}
        expanded={expanded}
        collapsible={collapsible}
        toggleCollapsed={toggleCollapsed}
        content={content}
        files={files}
      />
    );
  }

  if (event === "comment_deleted") {
    return (
      <span ref={ref}>
        <p className="requests-event-body-deleted">
          {i18next.t("Comment was deleted.")}
        </p>
      </span>
    );
  }

  return (
    <Popup
      eventsEnabled={false}
      open={!!tooltipOffset}
      offset={tooltipOffset}
      position="top left"
      className="requests-event-body-popup"
      trigger={
        <TimelineEventBodyRender
          ref={ref}
          refInner={refInner}
          isOverflowing={isOverflowing}
          expanded={expanded}
          collapsible={collapsible}
          toggleCollapsed={toggleCollapsed}
          content={content}
          format={format}
          files={files}
        />
      }
      basic
    >
      <ButtonGroup basic size="small">
        <Button
          onClick={onQuoteClick}
          icon="reply"
          content={i18next.t("Quote reply")}
        />
      </ButtonGroup>
    </Popup>
  );
};

TimelineEventBodyContainer.propTypes = {
  payload: PropTypes.object,
  quoteReply: PropTypes.func,
  collapsible: PropTypes.bool,
  expandedByDefault: PropTypes.bool,
};

TimelineEventBodyContainer.defaultProps = {
  payload: {},
  quoteReply: null,
  collapsible: true,
  expandedByDefault: false,
};

export default Overridable.component(
  "InvenioRequests.TimelineEventBody",
  TimelineEventBody
);
