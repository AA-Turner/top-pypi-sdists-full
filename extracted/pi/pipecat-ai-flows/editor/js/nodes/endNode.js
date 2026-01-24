/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { PipecatBaseNode } from "./baseNode.js";
import { LiteGraph } from "litegraph.js";

/**
 * Represents the end node of a flow
 * @extends PipecatBaseNode
 */
export class PipecatEndNode extends PipecatBaseNode {
  /**
   * Creates a new end node
   */
  constructor() {
    super("End Node", "#e74c3c");
    this.addInput("In", "flow", {
      multipleConnections: true,
      linkType: LiteGraph.MULTIPLE_LINK,
    });

    // Initialize with only task messages for the end node
    this.properties = {
      task_messages: [
        {
          role: "system",
          content: "Enter final task message...",
        },
      ],
      pre_actions: [],
      post_actions: [],
    };
  }

  /**
   * Handles input connection
   * @param {number} targetSlot - Input slot index
   * @param {string} type - Type of connection
   * @param {Object} output - Output connection information
   * @param {LGraphNode} input_node - Node being connected
   * @param {number} input_slot - Slot being connected to
   * @returns {boolean} Whether the connection is allowed
   */
  onConnectInput(targetSlot, type, output, input_node, input_slot) {
    if (this.inputs[0].link == null) {
      this.inputs[0].link = [];
    }
    return true;
  }

  /**
   * Handles node connection
   * @param {number} slot - Input slot index
   * @param {LGraphNode} targetNode - Node to connect to
   * @param {number} targetSlot - Target node's slot index
   * @returns {boolean} Whether the connection was successful
   */
  connect(slot, targetNode, targetSlot) {
    if (this.inputs[slot].link == null) {
      this.inputs[slot].link = [];
    }
    return super.connect(slot, targetNode, targetSlot);
  }

  /**
   * Handles connection changes
   * @param {string} type - Type of connection change
   * @param {number} slot - Slot index
   * @param {boolean} connected - Whether connection was made or removed
   * @param {Object} link_info - Information about the connection
   */
  onConnectionsChange(type, slot, connected, link_info) {
    if (type === LiteGraph.INPUT && this.inputs[slot].link == null) {
      this.inputs[slot].link = [];
    }
    super.onConnectionsChange &&
      super.onConnectionsChange(type, slot, connected, link_info);
  }
}
