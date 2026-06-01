// This file is part of InvenioRequests
// Copyright (C) 2025 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { http } from "react-invenio-forms";

export class InvenioRequestFilesApi {
  baseUrl = "/api/requests";

  /**
   * Upload a file linked to a request.
   *
   * @param {string} requestId - Request ID
   * @param {string} filename - Original filename
   * @param {object} payload - File
   * @param {object} options - Custom options
   */
  async uploadFile(requestId, filename, payload, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
    };
    return http.put(`${this.baseUrl}/${requestId}/files/upload/${filename}`, payload, {
      headers: headers,
      ...options,
    });
  }

  /**
   * Delete a file linked to a request.
   *
   * @param {string} requestId - Request ID
   * @param {string} fileKey - Unique filename (key)
   * @param {object} options - Custom options
   */
  async deleteFile(requestId, fileKey, options) {
    options = options || {};
    const headers = {
      "Content-Type": "application/octet-stream",
    };
    return http.delete(`${this.baseUrl}/${requestId}/files/${fileKey}`, {
      headers: headers,
      ...options,
    });
  }
}
