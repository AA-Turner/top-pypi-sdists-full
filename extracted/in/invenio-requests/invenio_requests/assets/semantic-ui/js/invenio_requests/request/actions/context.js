/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */

import React from "react";

export const RequestActionContext = React.createContext({
  modalOpen: false,
  toggleModal: () => {},
  linkExtractor: undefined,
  requestApi: undefined,
  performAction: () => {},
  cleanError: () => {},
  error: undefined,
  loading: false,
});
