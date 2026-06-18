/*
 * SPDX-FileCopyrightText: 2025 CERN.
 * SPDX-License-Identifier: MIT
 */

import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Input } from "semantic-ui-react";
import React from "react";
import { RequestEventAvatarContainer } from "./RequestsFeed";

const FakeInput = ({ placeholder, userAvatar, onActivate, className, disabled }) => {
  return (
    <div className={`requests-comment-fake-reply ${className}`}>
      <div className="rel-mr-1 tablet computer only">
        <RequestEventAvatarContainer src={userAvatar} />
      </div>
      <div className="requests-comment-fake-reply-input">
        <Input
          placeholder={placeholder}
          fluid
          onClick={() => onActivate()}
          onChange={(e) => onActivate(e.target.value)}
          size="small"
          disabled={disabled}
        />
      </div>
    </div>
  );
};

FakeInput.propTypes = {
  placeholder: PropTypes.string.isRequired,
  userAvatar: PropTypes.string,
  onActivate: PropTypes.func.isRequired,
  className: PropTypes.string,
  disabled: PropTypes.bool,
};

FakeInput.defaultProps = {
  userAvatar: "",
  className: "",
  disabled: false,
};

export default Overridable.component("InvenioRequests.FakeInput", FakeInput);
