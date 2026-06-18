/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import { applyMiddleware, createStore } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";
import { default as createReducers } from "./state/reducers";
import thunk from "redux-thunk";

const composeEnhancers = composeWithDevTools({
  name: "InvenioRequests",
});

export function configureStore(config) {
  return createStore(
    createReducers(),
    // config object will be available in the actions,
    {},
    composeEnhancers(applyMiddleware(thunk.withExtraArgument(config)))
  );
}
