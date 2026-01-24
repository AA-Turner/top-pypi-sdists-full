/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { LGraphNode, LiteGraph } from "litegraph.js";

import { editorState } from "../editor/editorState.js";

/**
 * @typedef {Object} FunctionParameter
 * @property {string} type - Parameter type (e.g., 'string', 'integer')
 * @property {string} [description] - Parameter description
 * @property {Array<string>} [enum] - Possible values for enum types
 * @property {number} [minimum] - Minimum value for numeric types
 * @property {number} [maximum] - Maximum value for numeric types
 */

/**
 * @typedef {Object} FunctionDefinition
 * @property {string} name - Function name
 * @property {string} description - Function description
 * @property {Object} parameters - Function parameters
 * @property {Object.<string, FunctionParameter>} parameters.properties - Parameter definitions
 * @property {Array<string>} [parameters.required] - Required parameter names
 */

/**
 * @typedef {Object} FunctionNodeProperties
 * @property {string} type - Always 'function'
 * @property {FunctionDefinition} function - The function definition
 * @property {boolean} isNodeFunction - Whether this is a node function
 */

/**
 * Represents a function node in the flow
 * @extends LGraphNode
 */
export class PipecatFunctionNode extends LGraphNode {
  /**
   * Creates a new function node
   */
  constructor() {
    super();
    this.title = "Function";
    this.addInput("From", "flow");
    this.addOutput("To", "flow", {
      linkType: LiteGraph.MULTIPLE_LINK,
    });

    /** @type {FunctionNodeProperties} */
    this.properties = {
      type: "function",
      function: {
        name: "function_name",
        description: "Function description",
        parameters: {
          type: "object",
          properties: {},
        },
      },
      isNodeFunction: false,
    };

    this.color = "#9b59b6";
    this.size = [400, 150];
  }

  /**
   * Forces a minimum width for the node
   * @returns {Array<number>} The minimum dimensions [width, height]
   */
  computeSize() {
    return [400, this.size[1]];
  }

  /**
   * Updates the node status of the function based on its connections
   */
  updateNodeFunctionStatus() {
    const hasOutputConnection =
      this.outputs[0].links && this.outputs[0].links.length > 0;
    const newStatus = !hasOutputConnection;

    if (this.properties.isNodeFunction !== newStatus) {
      this.properties.isNodeFunction = newStatus;
      this.setDirtyCanvas(true, true);
    }
  }

  /**
   * Handles node connection
   * @param {number} slot - Output slot index
   * @param {LGraphNode} targetNode - Node to connect to
   * @param {number} targetSlot - Target node's input slot index
   * @returns {boolean} Whether the connection was successful
   */
  connect(slot, targetNode, targetSlot) {
    if (slot === 1 && this.outputs[slot].links == null) {
      this.outputs[slot].links = [];
    }
    const result = super.connect(slot, targetNode, targetSlot);
    this.updateNodeFunctionStatus();
    return result;
  }

  /**
   * Handles output disconnection
   * @param {number} slot - Output slot index
   */
  disconnectOutput(slot) {
    if (this.outputs[slot].links == null) {
      this.outputs[slot].links = [];
    }
    super.disconnectOutput(slot);
    this.updateNodeFunctionStatus();
  }

  /**
   * Handles input disconnection
   * @param {number} slot - Input slot index
   */
  disconnectInput(slot) {
    super.disconnectInput(slot);
    this.updateNodeFunctionStatus();
  }

  /**
   * Handles connection changes
   * @param {string} type - Type of connection change
   * @param {number} slot - Slot index
   * @param {boolean} connected - Whether connection was made or removed
   * @param {Object} link_info - Information about the connection
   */
  onConnectionsChange(type, slot, connected, link_info) {
    if (type === LiteGraph.OUTPUT && this.outputs[slot].links == null) {
      this.outputs[slot].links = [];
    }
    super.onConnectionsChange &&
      super.onConnectionsChange(type, slot, connected, link_info);
    this.updateNodeFunctionStatus();
  }

  /**
   * Draws the node's content
   * @param {CanvasRenderingContext2D} ctx - The canvas rendering context
   */
  onDrawForeground(ctx) {
    this.updateNodeFunctionStatus();

    const padding = 15;
    const textColor = "#ddd";
    const labelColor = "#aaa";

    this.color = this.properties.isNodeFunction ? "#e67e22" : "#9b59b6";

    // Draw node/edge indicator
    ctx.fillStyle = labelColor;
    ctx.font = "11px Arial";
    const typeText = this.properties.isNodeFunction
      ? "[Node Function]"
      : "[Edge Function]";
    ctx.fillText(typeText, padding, 35);

    // Draw function name
    ctx.fillStyle = textColor;
    ctx.font = "14px monospace";
    ctx.fillText(this.properties.function.name, padding, 60);

    // Draw description
    ctx.fillStyle = labelColor;
    ctx.font = "12px Arial";
    const description = this.properties.function.description;

    // Word wrap description
    const words = description.split(" ");
    let line = "";
    let y = 80;
    const maxWidth = this.size[0] - padding * 3;

    words.forEach((word) => {
      const testLine = line + word + " ";
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth) {
        ctx.fillText(line, padding, y);
        line = word + " ";
        y += 20;
      } else {
        line = testLine;
      }
    });
    ctx.fillText(line, padding, y);

    // Draw parameters indicator
    const hasParameters =
      Object.keys(this.properties.function.parameters.properties).length > 0;
    if (hasParameters) {
      ctx.fillStyle = "#666";
      ctx.font = "11px Arial";
      ctx.fillText("Has Parameters ⚙️", padding, y + 25);
    }

    // Optional: Draw transition indicator
    if (this.properties.function.transition_to) {
      ctx.fillStyle = "#666";
      ctx.font = "11px Arial";
      ctx.fillText(
        `→ ${this.properties.function.transition_to}`,
        padding,
        y + (hasParameters ? 45 : 25),
      );
      y += 20; // Increase y for the new line
    }

    // Adjust node height
    const desiredHeight = y + (hasParameters ? 45 : 25);
    if (Math.abs(this.size[1] - desiredHeight) > 10) {
      this.size[1] = desiredHeight;
      this.setDirtyCanvas(true, true);
    }
  }

  /**
   * Handles node selection
   */
  onSelected() {
    editorState.updateSidePanel(this);
  }

  /**
   * Handles graph changes
   */
  onAfterGraphChange() {
    this.updateNodeFunctionStatus();
  }
}
