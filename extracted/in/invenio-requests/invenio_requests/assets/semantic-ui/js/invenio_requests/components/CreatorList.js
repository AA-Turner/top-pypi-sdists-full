/*
 * SPDX-FileCopyrightText: 2022 CERN.
 * SPDX-License-Identifier: MIT
 */
import React from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { List } from "semantic-ui-react";

const CreatorList = ({ creators }) => {
  return (
    <Overridable id="CreatorList.layout">
      <List horizontal>
        {creators.map((creator) => {
          return (
            <List.Item key={creator.person_or_org.name}>
              <List.Content>
                <List.Icon name="user" />
                {creator.person_or_org.name}
              </List.Content>
            </List.Item>
          );
        })}
      </List>
    </Overridable>
  );
};

CreatorList.propTypes = {
  creators: PropTypes.array.isRequired,
};

export default Overridable.component("CreatorList", CreatorList);
