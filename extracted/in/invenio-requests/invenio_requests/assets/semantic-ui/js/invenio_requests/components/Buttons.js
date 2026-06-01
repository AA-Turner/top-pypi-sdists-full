// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { i18next } from "@translations/invenio_requests/i18next";
import React, { useEffect } from "react";
import { Button } from "semantic-ui-react";
import PropTypes from "prop-types";

// components for most common actions, used in other modules, not explicitly in invenio-requests

export const SaveButton = (props) => (
  <Button
    icon="save"
    labelPosition="left"
    positive
    size="mini"
    content={i18next.t("Save")}
    {...props}
  />
);

export const RequestDeclineButton = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  return (
    <Button
      icon="cancel"
      labelPosition="left"
      content={i18next.t("Decline")}
      onClick={onClick}
      loading={loading}
      disabled={loading}
      negative
      size={size}
      className={className}
      {...ariaAttributes}
    />
  );
};

RequestDeclineButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestDeclineButton.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "",
};

export const RequestAcceptButton = ({
  onClick,
  requestType,
  loading,
  ariaAttributes,
  size,
  className,
}) => {
  let buttonText;
  switch (requestType) {
    case "community-submission":
      buttonText = i18next.t("Accept and publish");
      break;
    case "record-deletion":
      buttonText = i18next.t("Accept and delete");
      break;
    default:
      buttonText = i18next.t("Accept");
  }
  return (
    <Button
      icon="checkmark"
      labelPosition="left"
      content={buttonText}
      onClick={onClick}
      positive
      loading={loading}
      disabled={loading}
      size={size}
      className={className}
      {...ariaAttributes}
    />
  );
};

RequestAcceptButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  requestType: PropTypes.string.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
};

RequestAcceptButton.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  className: "",
};

export const CancelButton = React.forwardRef((props, ref) => {
  useEffect(() => {
    ref?.current?.focus();
  }, [ref]);

  return (
    <Button
      ref={ref}
      icon="cancel"
      labelPosition="left"
      content={i18next.t("Cancel")}
      size="mini"
      {...props}
    />
  );
});

CancelButton.displayName = "CancelButton";

export const RequestCancelButton = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  content = i18next.t("Cancel request"),
  className,
  negative = true,
}) => {
  return (
    <Button
      icon="cancel"
      labelPosition="left"
      content={content}
      onClick={onClick}
      loading={loading}
      disabled={loading}
      size={size}
      negative={negative}
      className={className}
      {...ariaAttributes}
    />
  );
};

RequestCancelButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  content: PropTypes.string,
  className: PropTypes.string,
  negative: PropTypes.bool,
};

RequestCancelButton.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  content: i18next.t("Cancel request"),
  className: "",
  negative: true,
};

export const RequestSubmitButton = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  content,
  className,
}) => {
  return (
    <Button
      icon="unlock alternate"
      labelPosition="left"
      content={i18next.t("Request access")}
      onClick={onClick}
      positive
      loading={loading}
      disabled={loading}
      size={size}
      className={className}
      {...ariaAttributes}
    />
  );
};

RequestSubmitButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  content: PropTypes.string,
  className: PropTypes.string,
};

RequestSubmitButton.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "mini",
  content: i18next.t("Request access"),
  className: "",
};

export const RequestLockButton = ({
  onClick,
  loading,
  ariaAttributes,
  size,
  className,
  content,
  icon,
}) => {
  return (
    <Button
      icon={icon}
      onClick={onClick}
      content={content}
      loading={loading}
      disabled={loading}
      size={size}
      fluid
      className={className}
      {...ariaAttributes}
    />
  );
};

RequestLockButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  ariaAttributes: PropTypes.object,
  size: PropTypes.string,
  className: PropTypes.string,
  icon: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
};

RequestLockButton.defaultProps = {
  loading: false,
  ariaAttributes: {},
  size: "small",
  className: "request-lock-button",
};
