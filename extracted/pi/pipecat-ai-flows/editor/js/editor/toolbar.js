/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { generateFlowConfig } from "../utils/export.js";
import { createFlowFromConfig } from "../utils/import.js";
import { validateFlow } from "../utils/validation.js";
import { editorState } from "../editor/editorState.js";

/**
 * Manages the toolbar UI and actions
 */
export class Toolbar {
  /**
   * Creates a new Toolbar instance
   * @param {LGraph} graph - The LiteGraph instance
   */
  constructor(graph) {
    this.graph = graph;
    this.setupButtons();
  }

  /**
   * Sets up toolbar button event listeners
   */
  setupButtons() {
    // Get modal elements
    const newFlowModal = document.getElementById("new-flow-modal");
    const cancelNewFlow = document.getElementById("cancel-new-flow");
    const confirmNewFlow = document.getElementById("confirm-new-flow");

    // New Flow button now opens the modal
    document.getElementById("new-flow").onclick = () => {
      newFlowModal.showModal();
    };

    // Cancel button closes the modal
    cancelNewFlow.onclick = () => {
      newFlowModal.close();
    };

    // Confirm button clears the graph and closes the modal
    confirmNewFlow.onclick = () => {
      this.handleNew();
      newFlowModal.close();
    };

    document.getElementById("import-flow").onclick = () => this.handleImport();
    document.getElementById("export-flow").onclick = () => this.handleExport();
  }

  /**
   * Handles creating a new flow
   */
  handleNew() {
    // Clear the graph
    this.graph.clear();

    // Reset sidebar state
    editorState.updateSidePanel(null);
  }

  /**
   * Handles importing a flow configuration
   */
  handleImport() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.onchange = (e) => {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          // Clean the input string
          const cleanInput = event.target.result
            .replace(/[\u0000-\u001F\u007F-\u009F]/g, "")
            .replace(/\r\n/g, "\n")
            .replace(/\r/g, "\n");

          console.debug("Cleaned input:", cleanInput);

          const flowConfig = JSON.parse(cleanInput);
          console.debug("Parsed config:", flowConfig);

          // Validate imported flow
          const validation = validateFlow(flowConfig);
          if (!validation.valid) {
            console.error("Flow validation errors:", validation.errors);
            if (
              !confirm("Imported flow has validation errors. Import anyway?")
            ) {
              return;
            }
          }

          createFlowFromConfig(this.graph, flowConfig);
          console.log("Successfully imported flow configuration");
        } catch (error) {
          console.error("Error importing flow:", error);
          console.error("Error details:", {
            message: error.message,
            position: error.position,
            stack: error.stack,
          });
          alert("Error importing flow: " + error.message);
        }
      };
      reader.readAsText(file);
    };
    input.click();
  }

  /**
   * Handles exporting the current flow
   */
  handleExport() {
    try {
      const flowConfig = generateFlowConfig(this.graph);

      // Validate before export
      const validation = validateFlow(flowConfig);
      if (!validation.valid) {
        console.error("Flow validation errors:", validation.errors);
        if (!confirm("Flow has validation errors. Export anyway?")) {
          return;
        }
      }

      console.log("Generated Flow Configuration:");
      console.log(JSON.stringify(flowConfig, null, 2));

      // Generate timestamp
      const timestamp = new Date()
        .toISOString()
        .replace(/[:.]/g, "-")
        .replace("T", "_")
        .slice(0, -5);

      // Create a clean JSON string
      const jsonString = JSON.stringify(flowConfig, null, 2);

      const blob = new Blob([jsonString], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `flow_config_${timestamp}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error generating flow configuration:", error);
      alert("Error generating flow configuration: " + error.message);
    }
  }
}
