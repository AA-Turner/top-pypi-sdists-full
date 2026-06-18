/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

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
