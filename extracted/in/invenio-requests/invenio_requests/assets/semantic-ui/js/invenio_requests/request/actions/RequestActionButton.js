// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Button } from "semantic-ui-react";

export const RequestActionButton = ({
  action,
  handleActionClick,
  loading,
  className,
  size,
  requestType,
}) => {
  return (
    <Overridable
      id={`RequestActionButton.${action}`}
      onClick={handleActionClick}
      loading={loading}
      className={className}
      size={size}
    >
      <Button
        onClick={handleActionClick}
        loading={loading}
        className={className}
        size={size}
        requestType={requestType}
      >
        {action}
      </Button>
    </Overridable>
  );
};

RequestActionButton.propTypes = {
  action: PropTypes.string.isRequired,
  handleActionClick: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
  className: PropTypes.string,
  size: PropTypes.string,
  requestType: PropTypes.string.isRequired,
};

RequestActionButton.defaultProps = {
  className: "",
  size: "medium",
};

export default Overridable.component(
  "InvenioRequests.RequestActionButton",
  RequestActionButton
);
