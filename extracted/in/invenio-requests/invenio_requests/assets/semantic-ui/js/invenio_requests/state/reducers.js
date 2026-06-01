// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { timelineReducer } from "../timelineParent/state/reducer";
import { combineReducers } from "redux";
import { requestReducer } from "../request/state/reducer";
import { timelineRepliesReducer } from "../timelineCommentReplies/state/reducer";

export default function createReducers() {
  return combineReducers({
    timeline: timelineReducer,
    timelineReplies: timelineRepliesReducer,
    request: requestReducer,
  });
}
