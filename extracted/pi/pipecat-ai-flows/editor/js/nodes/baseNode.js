/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { LGraphNode } from "litegraph.js";

import { editorState } from "../editor/editorState.js";
import { formatActions } from "../utils/helpers.js";

/**
 * @typedef {Object} Message
 * @property {string} role - Message role (e.g., 'system', 'user', 'assistant')
 * @property {string} content - Message content
 */

/**
 * @typedef {Object} Action
 * @property {string} type - Action type (e.g., 'tts_say', 'end_conversation')
 * @property {string} [text] - Text content for text-based actions
 */

/**
 * @typedef {Object} NodeProperties
 * @property {Array<Message>} [role_messages] - Messages defining bot's role/personality
 * @property {Array<Message>} [task_messages] - Messages defining the node's task
 * @property {Array<Action>} [pre_actions] - Actions to execute before node processing
 * @property {Array<Action>} [post_actions] - Actions to execute after node processing
 */

/**
 * Base class for all Pipecat nodes
 * @extends LGraphNode
 */
export class PipecatBaseNode extends LGraphNode {
  /**
   * Creates a new PipecatBaseNode
   * @param {string} title - The display title of the node
   * @param {string} color - The color of the node
   * @param {string} [defaultContent='Enter message...'] - Default message content
   */
  constructor(title, color, defaultContent) {
    super();
    this.title = title;
    this.color = color;
    this.size = [400, 200];

    /** @type {NodeProperties} */
    this.properties = {
      task_messages: [
        {
          role: "system",
          content: defaultContent || "Enter task message...",
        },
      ],
      pre_actions: [],
      post_actions: [],
    };

    // Force minimum width
    this.computeSize = function () {
      return [400, this.size[1]];
    };
  }

  /**
   * Forces a minimum width for the node
   * @returns {Array<number>} The minimum dimensions [width, height]
   */
  computeSize() {
    return [400, this.size[1]];
  }

  /**
   * Draws the node's content
   * @param {CanvasRenderingContext2D} ctx - The canvas rendering context
   */
  onDrawForeground(ctx) {
    const padding = 15;
    const textColor = "#ddd";
    const labelColor = "#aaa";
    let currentY = 40;

    /**
     * Draws wrapped text with a label
     * @param {string} text - The text to draw
     * @param {number} startY - Starting Y position
     * @param {string} label - Label for the text section
     * @returns {number} The Y position after drawing
     */
    const drawWrappedText = (text, startY, label) => {
      ctx.fillStyle = labelColor;
      ctx.font = "12px Arial";
      ctx.fillText(label, padding, startY + 5);

      ctx.fillStyle = textColor;
      ctx.font = "12px monospace";

      const words = text.split(" ");
      let line = "";
      let y = startY + 25;
      const maxWidth = this.size[0] - padding * 3;

      words.forEach((word) => {
        const testLine = line + word + " ";
        const metrics = ctx.measureText(testLine);
        if (metrics.width > maxWidth) {
          ctx.fillText(line, padding * 1.5, y);
          line = word + " ";
          y += 20;
        } else {
          line = testLine;
        }
      });
      ctx.fillText(line, padding * 1.5, y);

      return y + 25;
    };

    // Draw role messages if present
    if (this.properties.role_messages?.length > 0) {
      this.properties.role_messages.forEach((message) => {
        currentY = drawWrappedText(message.content, currentY, "Role Message");
        currentY += 10;
      });
    }

    // Draw task messages
    if (this.properties.task_messages) {
      this.properties.task_messages.forEach((message) => {
        currentY = drawWrappedText(message.content, currentY, "Task Message");
        currentY += 10;
      });
    }

    // Draw pre-actions
    if (this.properties.pre_actions?.length > 0) {
      currentY = drawWrappedText(
        formatActions(this.properties.pre_actions),
        currentY + 15,
        "Pre-actions",
      );
    }

    // Draw post-actions
    if (this.properties.post_actions?.length > 0) {
      currentY = drawWrappedText(
        formatActions(this.properties.post_actions),
        currentY + 15,
        "Post-actions",
      );
    }

    const desiredHeight = currentY + padding * 2;
    if (Math.abs(this.size[1] - desiredHeight) > 10) {
      this.size[1] = desiredHeight;
      this.setDirtyCanvas(true, true);
    }
  }

  /**
   * Handles node selection
   * Updates the side panel with this node's properties
   */
  onSelected() {
    editorState.updateSidePanel(this);
  }

  /**
   * Serializes the node for saving
   * @returns {Object} Serialized node data
   */
  serialize() {
    const data = super.serialize();
    data.properties = {
      role_messages: this.properties.role_messages,
      task_messages: this.properties.task_messages,
      pre_actions: this.properties.pre_actions,
      post_actions: this.properties.post_actions,
    };
    return data;
  }

  /**
   * Deserializes saved node data
   * @param {Object} data - The saved node data
   */
  configure(data) {
    super.configure(data);
    if (data.properties) {
      this.properties = {
        role_messages: data.properties.role_messages || [],
        task_messages: data.properties.task_messages || [
          { role: "system", content: "Enter task message..." },
        ],
        pre_actions: data.properties.pre_actions || [],
        post_actions: data.properties.post_actions || [],
      };
    }
  }
}
