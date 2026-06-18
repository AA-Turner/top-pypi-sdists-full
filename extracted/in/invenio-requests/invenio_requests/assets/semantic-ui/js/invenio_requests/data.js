/*
 * SPDX-FileCopyrightText: 2022-2026 CERN.
 * SPDX-FileCopyrightText: 2024 Northwestern University.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import { createContext } from "react";

export const requestDetailsDiv = document.getElementById("request-detail");

export const getDataset = () => {
  if (!requestDetailsDiv) {
    throw new Error("Could not find div with ID `request-detail`");
  }

  return {
    request: JSON.parse(requestDetailsDiv.dataset.record),
    defaultQueryParams: JSON.parse(requestDetailsDiv.dataset.defaultQueryConfig),
    defaultReplyQueryParams: JSON.parse(
      requestDetailsDiv.dataset.defaultReplyQueryConfig
    ),
    userAvatar: JSON.parse(requestDetailsDiv.dataset.userAvatar),
    permissions: JSON.parse(requestDetailsDiv.dataset.permissions),
    config: JSON.parse(requestDetailsDiv.dataset.config),
  };
};

export const DatasetContext = createContext(null);
