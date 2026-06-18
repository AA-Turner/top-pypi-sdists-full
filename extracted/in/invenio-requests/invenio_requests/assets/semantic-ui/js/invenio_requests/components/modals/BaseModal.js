/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */
import React from "react";
import { Modal, Button, Message } from "semantic-ui-react";
import PropTypes from "prop-types";

export const BaseModal = ({
  contentText,
  action,
  isLoading,
  error,
  headerText,
  cancelButtonText,
  actionButtonText,
  open,
  onOpen,
  onClose,
}) => {
  return (
    <Modal onClose={onOpen} onOpen={onClose} open={open}>
      <Modal.Header>{headerText}</Modal.Header>
      <Modal.Content>{contentText}</Modal.Content>
      <Modal.Actions>
        {error && (
          <Message negative compact>
            {error}
          </Message>
        )}

        <Button content={cancelButtonText} onClick={() => onClose()} />
        <Button
          content={actionButtonText}
          negative
          onClick={() => action()}
          loading={isLoading}
        />
      </Modal.Actions>
    </Modal>
  );
};

BaseModal.propTypes = {
  contentText: PropTypes.string.isRequired,
  action: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
  error: PropTypes.string,
  headerText: PropTypes.string.isRequired,
  cancelButtonText: PropTypes.string.isRequired,
  actionButtonText: PropTypes.string.isRequired,
  open: PropTypes.bool.isRequired,
  onOpen: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
};

BaseModal.defaultProps = {
  error: "",
};

export default BaseModal;
