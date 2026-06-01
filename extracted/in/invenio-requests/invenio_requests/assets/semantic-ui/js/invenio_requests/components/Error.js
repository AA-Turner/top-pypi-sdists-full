// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import React, { Component } from "react";
import Overridable from "react-overridable";
import { Message } from "semantic-ui-react";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_requests/i18next";

class Error extends Component {
  render() {
    const { children, error, errorInfo } = this.props;
    if (error) {
      return (
        <Overridable id="Error.layout" {...this.props}>
          <Message negative>
            <Message.Header>{i18next.t("Something went wrong.")}</Message.Header>
            <p>
              {error && error.toString()}
              <br />
              {errorInfo}
            </p>
          </Message>
        </Overridable>
      );
    }
    return children;
  }
}

Error.propTypes = {
  error: PropTypes.object,
  errorInfo: PropTypes.string,
  children: PropTypes.node,
};

Error.defaultProps = {
  error: null,
  errorInfo: null,
  children: null,
};

export default Overridable.component("Error", Error);
