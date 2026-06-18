/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */
export const payloadSerializer = (content, format, files) => ({
  payload: {
    content,
    format,
    files: files.map((file) => ({
      file_id: file.file_id,
    })),
  },
});

export const errorSerializer = (error) =>
  error?.response?.data?.message || error?.message;
