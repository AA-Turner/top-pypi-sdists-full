/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import { connect } from "react-redux";
import RequestComponent from "./Request";
import { initRequest, updateRequestAfterAction } from "./state/actions";

const mapDispatchToProps = (dispatch) => ({
  initRequest: () => dispatch(initRequest()),
  updateRequestAfterAction: (request) => dispatch(updateRequestAfterAction(request)),
});

const mapStateToProps = (state) => ({
  request: state.request.data,
});

export const Request = connect(mapStateToProps, mapDispatchToProps)(RequestComponent);

export * from "./Status";
