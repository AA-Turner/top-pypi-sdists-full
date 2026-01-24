/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { PipecatBaseNode } from "./baseNode.js";

/**
 * Represents the starting node of a flow
 * @extends PipecatBaseNode
 */
export class PipecatStartNode extends PipecatBaseNode {
  /**
   * Creates a new start node
   * @param {string} [title="Start"] - Optional custom title for the node
   */
  constructor(title = "Start") {
    super(title, "#2ecc71");
    this.addOutput("Out", "flow");

    // Initialize with both role and task messages for the start node
    this.properties = {
      role_messages: [
        {
          role: "system",
          content: "Enter bot's personality/role...",
        },
      ],
      task_messages: [
        {
          role: "system",
          content: "Enter initial task...",
        },
      ],
      pre_actions: [],
      post_actions: [],
    };
  }
}
