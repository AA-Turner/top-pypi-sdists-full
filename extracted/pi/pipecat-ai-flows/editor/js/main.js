/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { LGraph, LiteGraph } from "litegraph.js";
import 'litegraph.js/css/litegraph.css';

import { registerNodes } from "./nodes/index.js";
import { SidePanel } from "./editor/sidePanel.js";
import { Toolbar } from "./editor/toolbar.js";
import { setupCanvas } from "./editor/canvas.js";
import { editorState } from "./editor/editorState.js";

// Clear all default node types
LiteGraph.clearRegisteredTypes();

/**
 * Initializes the flow editor
 */
document.addEventListener("DOMContentLoaded", function () {
  // Initialize graph
  const graph = new LGraph();

  // Register node types
  registerNodes();

  // Setup UI components
  const canvas = setupCanvas(graph);
  const sidePanel = new SidePanel(graph);
  const toolbar = new Toolbar(graph);

  // Register side panel with editor state
  editorState.setSidePanel(sidePanel);

  // Add graph change listener
  graph.onAfterChange = () => {
    graph._nodes.forEach((node) => {
      if (node.onAfterGraphChange) {
        node.onAfterGraphChange();
      }
    });
  };

  // Handle node selection
  graph.onNodeSelected = (node) => {
    editorState.updateSidePanel(node);
  };

  graph.onNodeDeselected = () => {
    editorState.updateSidePanel(null);
  };

  // Start the graph
  graph.start();
});
