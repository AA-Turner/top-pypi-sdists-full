/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import { REQUEST_INIT } from "./actions";

export const initialState = {
  loading: false,
  data: {},
  error: null,
};

export const requestReducer = (state = initialState, action) => {
  switch (action.type) {
    case REQUEST_INIT:
      return {
        ...state,
        loading: false,
        data: action.payload,
        error: null,
      };
    default:
      return state;
  }
};
