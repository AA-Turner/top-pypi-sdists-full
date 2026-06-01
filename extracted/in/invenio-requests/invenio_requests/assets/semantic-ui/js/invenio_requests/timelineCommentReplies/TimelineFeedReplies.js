import React, { Component } from "react";
import TimelineFeedComponent from "../timeline/TimelineFeed";
import PropTypes from "prop-types";
import { getEventIdFromUrl } from "../timelineEvents/utils";
import { DatasetContext } from "../data";

class TimelineFeedReplies extends Component {
  componentDidMount() {
    const { setInitialReplies } = this.props;
    setInitialReplies(getEventIdFromUrl());
  }

  static contextType = DatasetContext;

  render() {
    const { ...props } = this.props;
    const {
      defaultReplyQueryParams: { size },
    } = this.context;
    return <TimelineFeedComponent size={size} {...props} />;
  }
}

TimelineFeedReplies.propTypes = {
  setInitialReplies: PropTypes.func.isRequired,
};

export default TimelineFeedReplies;
