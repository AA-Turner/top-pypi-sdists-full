/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

export const REQUEST_INIT = "request/INIT";

export const initRequest = () => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: REQUEST_INIT,
      payload: config.request,
    });
  };
};

export const updateRequest = (request) => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: REQUEST_INIT,
      payload: request,
    });
  };
};

export const updateRequestAfterAction = (request) => {
  return async (dispatch, getState, config) => {
    dispatch(updateRequest(request));
    window.location.reload();
  };
};

export const setRefreshInterval = () => {
  return (dispatch, getState, config) => {
    return config.refreshIntervalMs;
  };
};
