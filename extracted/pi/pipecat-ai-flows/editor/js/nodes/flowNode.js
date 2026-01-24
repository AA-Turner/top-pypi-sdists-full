/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { PipecatBaseNode } from "./baseNode.js";

/**
 * Represents an intermediate flow node
 * @extends PipecatBaseNode
 */
export class PipecatFlowNode extends PipecatBaseNode {
  /**
   * Creates a new flow node
   */
  constructor() {
    super("Flow Node", "#3498db");
    this.addInput("In", "flow");
    this.addOutput("Out", "flow");

    // Initialize with only task messages since role is inherited
    this.properties = {
      task_messages: [
        {
          role: "system",
          content: "Enter task message...",
        },
      ],
      pre_actions: [],
      post_actions: [],
    };
  }
}
