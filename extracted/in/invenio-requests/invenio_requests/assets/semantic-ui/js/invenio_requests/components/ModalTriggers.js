// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { AppMedia } from "@js/invenio_theme/Media";
import { i18next } from "@translations/invenio_requests/i18next";
import React from "react";
import PropTypes from "prop-types";
import { Dropdown } from "semantic-ui-react";
import {
  RequestAcceptButton,
  RequestSubmitButton,
  RequestCancelButton,
  RequestDeclineButton,
} from "./Buttons";

const { MediaContextProvider, Media } = AppMedia;

// components for most common actions, used in other modules, not explicitly in invenio-requests

export const RequestDeclineModalTrigger = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  return (
    <MediaContextProvider>
      <Media greaterThanOrEqual="tablet">
        <RequestDeclineButton
          onClick={onClick}
          loading={loading}
          disabled={loading}
          size={size}
          className={className}
          {...ariaAttributes}
        />
      </Media>
      <Media at="mobile">
        <Dropdown.Item
          icon={{
            name: "cancel",
            color: "negative",
            className: "mr-5",
          }}
          onClick={onClick}
          content={i18next.t("Decline")}
        />
      </Media>
    </MediaContextProvider>
  );
};

RequestDeclineModalTrigger.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestDeclineModalTrigger.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "ml-5",
};

export const RequestAcceptModalTrigger = ({
  onClick,
  requestType,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  let text; // logic duplicated from Buttons.js for Dropdown text
  switch (requestType) {
    case "community-submission":
      text = i18next.t("Accept and publish");
      break;
    case "record-deletion":
      text = i18next.t("Accept and delete");
      break;
    default:
      text = i18next.t("Accept");
  }
  return (
    <MediaContextProvider>
      <Media greaterThanOrEqual="tablet">
        <RequestAcceptButton
          onClick={onClick}
          loading={loading}
          disabled={loading}
          requestType={requestType}
          size={size}
          className={className}
          {...ariaAttributes}
        />
      </Media>
      <Media at="mobile">
        <Dropdown.Item
          icon={{
            name: "checkmark",
            color: "positive",
            className: "mr-5",
          }}
          onClick={onClick}
          content={text}
        />
      </Media>
    </MediaContextProvider>
  );
};

RequestAcceptModalTrigger.propTypes = {
  onClick: PropTypes.func.isRequired,
  requestType: PropTypes.string.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestAcceptModalTrigger.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "ml-5",
};

export const RequestCancelModalTrigger = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  return (
    <MediaContextProvider>
      <Media greaterThanOrEqual="tablet">
        <RequestCancelButton
          content={i18next.t("Cancel")}
          onClick={onClick}
          loading={loading}
          disabled={loading}
          size={size}
          className={className}
          negative={false}
          {...ariaAttributes}
        />
      </Media>
      <Media at="mobile">
        <Dropdown.Item
          icon={{
            name: "cancel",
            className: "neutral mr-5",
          }}
          onClick={onClick}
          content={i18next.t("Cancel")}
        />
      </Media>
    </MediaContextProvider>
  );
};

RequestCancelModalTrigger.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestCancelModalTrigger.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "ml-5",
};

export const RequestSubmitModalTrigger = ({
  onClick,
  requestType,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  const text = i18next.t("Request access");
  return (
    <MediaContextProvider>
      <Media greaterThanOrEqual="tablet">
        <RequestSubmitButton
          onClick={onClick}
          loading={loading}
          disabled={loading}
          requestType={requestType}
          size={size}
          className={className}
          {...ariaAttributes}
        />
      </Media>
      <Media at="mobile">
        <Dropdown.Item
          icon={{
            name: "unlock alternate",
            color: "positive",
            className: "mr-5",
          }}
          onClick={onClick}
          content={text}
        />
      </Media>
    </MediaContextProvider>
  );
};

RequestSubmitModalTrigger.propTypes = {
  onClick: PropTypes.func.isRequired,
  requestType: PropTypes.string.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestSubmitModalTrigger.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "ml-5",
};
