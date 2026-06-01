// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

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
