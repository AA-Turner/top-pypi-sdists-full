/**
 * @fileoverview Manages the side panel UI for the flow editor, providing JSON editing capabilities
 * with validation and visual feedback.
 * @copyright 2024, Daily
 * @license BSD 2-Clause License
 */

/**
 * Handles JSON editing with validation and visual feedback.
 * Provides real-time validation, error messaging, and state management
 * for JSON content editing.
 */
class JsonEditor {
  /**
   * Creates a new JSON editor
   * @param {HTMLElement} element - The textarea element
   * @param {Function} onValid - Callback for valid JSON
   * @param {Function} onInvalid - Callback for invalid JSON
   * @param {Function} validator - Function to validate the parsed JSON
   */
  constructor(element, onValid, onInvalid, validator = (json) => true) {
    this.element = element;
    this.onValid = onValid;
    this.onInvalid = onInvalid;
    this.validator = validator;
    this.originalValue = element.value;

    // Create error message element
    this.errorElement = document.createElement("div");
    this.errorElement.className = "json-error-message";
    this.errorElement.style.display = "none";
    element.parentNode.insertBefore(this.errorElement, element.nextSibling);

    this.setupEditor();
  }

  /**
   * Sets up the editor event handlers
   */
  setupEditor() {
    // Just mark as unsaved while typing
    this.element.addEventListener("input", () => {
      this.element.classList.add("unsaved");
    });

    // Remove validation styles when focusing
    this.element.addEventListener("focus", () => {
      this.element.classList.remove("valid", "invalid");
      this.hideError();
    });

    // Validate when losing focus
    this.element.addEventListener("blur", () => {
      try {
        const parsed = JSON.parse(this.element.value);
        if (this.validator(parsed)) {
          this.element.classList.remove("invalid");
          this.hideError();
        } else {
          this.element.classList.add("invalid");
          this.showError("Invalid JSON format");
        }
      } catch (error) {
        this.element.classList.add("invalid");
        this.showError("Invalid JSON syntax");
      }
    });
  }

  /**
   * Shows an error message
   * @param {string} message - The error message to display
   */
  showError(message) {
    this.errorElement.textContent = message;
    this.errorElement.style.display = "block";
  }

  /**
   * Hides the error message
   */
  hideError() {
    this.errorElement.style.display = "none";
  }

  /**
   * Validates and saves the current content
   * @returns {boolean} Whether the save was successful
   */
  validateAndSave() {
    try {
      const value = this.element.value;
      const parsed = JSON.parse(value);

      if (this.validator(parsed)) {
        this.element.classList.remove("invalid", "unsaved");
        this.hideError();
        this.onValid(parsed);
        return true;
      } else {
        throw new Error("Validation failed");
      }
    } catch (error) {
      this.element.classList.add("invalid");
      this.onInvalid(error);

      const errorMsg =
        error instanceof SyntaxError
          ? `JSON Syntax Error: ${error.message}`
          : "Invalid JSON format";

      this.showError(errorMsg);
      alert(
        `Warning: ${errorMsg}\n\nPlease fix the JSON format to save your changes.`,
      );
      return false;
    }
  }

  /**
   * Sets the editor value
   * @param {any} value - The value to stringify and set
   */
  setValue(value) {
    this.element.value = JSON.stringify(value, null, 2);
    this.originalValue = this.element.value;
    this.element.classList.remove("valid", "invalid", "unsaved");
    this.hideError();
  }

  /**
   * Restores the fields to their original values
   */
  restoreOriginal() {
    this.element.value = this.originalValue;
    this.element.classList.remove("valid", "invalid", "unsaved");
    this.hideError();
  }

  /**
   * Checks if the editor has unsaved changes
   * @returns {boolean}
   */
  hasUnsavedChanges() {
    return this.element.classList.contains("unsaved");
  }
}

/**
 * @typedef {Object} SidePanelElements
 * @property {HTMLElement} panel - The main panel element
 * @property {HTMLElement} content - The content container
 * @property {HTMLElement} noSelection - The no-selection message element
 * @property {HTMLElement} title - The panel title element
 * @property {HTMLElement} messageEditor - The message editor container
 * @property {HTMLElement} functionEditor - The function editor container
 */

/**
 * Manages the side panel UI and interactions
 */
export class SidePanel {
  /**
   * Creates a new SidePanel instance
   * @param {LGraph} graph - The LiteGraph instance
   */
  constructor(graph) {
    this.graph = graph;
    this.selectedNode = null;

    /** @type {SidePanelElements} */
    this.elements = {
      panel: document.querySelector("#side-panel"),
      content: document.querySelector(".editor-content"),
      noSelection: document.querySelector(".no-selection-message"),
      title: document.getElementById("editor-title"),
      messageEditor: document.querySelector(".message-editor"),
      functionEditor: document.querySelector(".function-editor"),
    };

    // Create save button container
    const saveContainer = document.createElement("div");
    saveContainer.className =
      "save-button-container flex justify-end gap-2 mt-4";

    // Add cancel button
    this.cancelButton = document.createElement("button");
    this.cancelButton.className =
      "btn btn-sm btn-secondary cancel-button hidden";
    this.cancelButton.textContent = "Cancel";
    saveContainer.appendChild(this.cancelButton);

    // Add save button
    this.saveButton = document.createElement("button");
    this.saveButton.className = "btn btn-sm btn-primary save-button hidden";
    this.saveButton.textContent = "Save changes";
    saveContainer.appendChild(this.saveButton);

    // Add save button after each editor
    this.elements.messageEditor.appendChild(saveContainer.cloneNode(true));
    this.elements.functionEditor.appendChild(saveContainer);

    this.setupEventListeners();
  }

  /**
   * Sets up event listeners for the editors
   */
  setupEventListeners() {
    // Prevent node deselection when clicking in the side panel
    this.elements.panel.addEventListener("mousedown", (e) => {
      e.stopPropagation();
    });

    // Save button handlers
    document.querySelectorAll(".save-button").forEach((button) => {
      button.addEventListener("click", () => {
        this.saveAllEditors();
      });
    });

    document.querySelectorAll(".cancel-button").forEach((button) => {
      button.addEventListener("click", () => {
        Object.values(this.editors).forEach((editor) => {
          if (editor.hasUnsavedChanges()) {
            editor.restoreOriginal();
          }
        });
        document
          .querySelectorAll(".save-button, .cancel-button")
          .forEach((btn) => {
            btn.style.display = "none";
          });
      });
    });

    // Keyboard shortcut for saving
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.key === "s") {
        e.preventDefault();
        this.saveAllEditors();
      }
    });

    // Role messages editor
    const roleMessagesEditor = new JsonEditor(
      document.getElementById("role-messages-editor"),
      (validJson) => {
        if (this.selectedNode) {
          this.selectedNode.properties.role_messages = validJson;
          this.selectedNode.setDirtyCanvas(true);
          this.graph.change();
        }
      },
      (error) => {
        console.error("Invalid role messages JSON:", error);
      },
      (json) => Array.isArray(json), // Validator for messages
    );

    // Task messages editor
    const taskMessagesEditor = new JsonEditor(
      document.getElementById("task-messages-editor"),
      (validJson) => {
        if (this.selectedNode) {
          this.selectedNode.properties.task_messages = validJson;
          this.selectedNode.setDirtyCanvas(true);
          this.graph.change();
        }
      },
      (error) => {
        console.error("Invalid task messages JSON:", error);
      },
      (json) => Array.isArray(json), // Validator for messages
    );

    // Pre-actions editor
    const preActionsEditor = new JsonEditor(
      document.getElementById("pre-actions-editor"),
      (validJson) => {
        if (this.selectedNode) {
          this.selectedNode.properties.pre_actions = validJson;
          this.selectedNode.setDirtyCanvas(true);
          this.graph.change();
        }
      },
      (error) => {
        console.error("Invalid pre-actions JSON:", error);
      },
      (json) => Array.isArray(json), // Validator for actions
    );

    // Post-actions editor
    const postActionsEditor = new JsonEditor(
      document.getElementById("post-actions-editor"),
      (validJson) => {
        if (this.selectedNode) {
          this.selectedNode.properties.post_actions = validJson;
          this.selectedNode.setDirtyCanvas(true);
          this.graph.change();
        }
      },
      (error) => {
        console.error("Invalid post-actions JSON:", error);
      },
      (json) => Array.isArray(json), // Validator for actions
    );

    // Function editor
    const functionEditor = new JsonEditor(
      document.getElementById("function-editor"),
      (validJson) => {
        if (this.selectedNode) {
          this.selectedNode.properties.function = validJson.function;
          this.selectedNode.setDirtyCanvas(true);
          this.graph.change();
        }
      },
      (error) => {
        console.error("Invalid function JSON:", error);
      },
      // Updated validator to allow transition_to
      (json) => {
        // Basic structure check
        if (json.type !== "function" || !json.function) {
          return false;
        }

        const func = json.function;

        // Must have name and parameters
        if (!func.name || !func.parameters) {
          return false;
        }

        // transition_to is optional but must be a string if present
        if (
          func.transition_to !== undefined &&
          typeof func.transition_to !== "string"
        ) {
          return false;
        }

        return true;
      },
    );

    // Store editor instances for use in updatePanel
    this.editors = {
      roleMessages: roleMessagesEditor,
      taskMessages: taskMessagesEditor,
      preActions: preActionsEditor,
      postActions: postActionsEditor,
      function: functionEditor,
    };

    // Monitor changes to show/hide save button
    const checkUnsavedChanges = () => {
      const hasUnsavedChanges = Object.values(this.editors).some((editor) =>
        editor.hasUnsavedChanges(),
      );
      document
        .querySelectorAll(".save-button, .cancel-button")
        .forEach((button) => {
          button.style.display = hasUnsavedChanges ? "inline-block" : "none";
        });
    };

    // Add change monitoring to each editor
    Object.values(this.editors).forEach((editor) => {
      editor.element.addEventListener("input", checkUnsavedChanges);
    });
  }

  /**
   * Saves all editors
   */
  saveAllEditors() {
    let allValid = true;
    Object.values(this.editors).forEach((editor) => {
      if (editor.hasUnsavedChanges()) {
        allValid = editor.validateAndSave() && allValid;
      }
    });
    if (allValid) {
      document.querySelectorAll(".save-button").forEach((button) => {
        button.style.display = "none";
      });
    }
  }

  /**
   * Checks if any editors have unsaved changes
   * @returns {boolean}
   */
  hasUnsavedChanges() {
    return Object.values(this.editors).some((editor) =>
      editor.hasUnsavedChanges(),
    );
  }

  /**
   * Updates the side panel with node data
   * @param {PipecatBaseNode|null} node
   */
  updatePanel(node) {
    if (this.hasUnsavedChanges()) {
      if (!confirm("You have unsaved changes. Discard them?")) {
        return;
      }

      // Hide both buttons when discarding changes
      document
        .querySelectorAll(".save-button, .cancel-button")
        .forEach((button) => {
          button.style.display = "none";
        });
    }

    console.log("updatePanel called with node:", node);

    // Update the selected node reference
    this.selectedNode = node;

    if (!node) {
      console.log("No node provided, hiding panel");
      this.elements.content.style.display = "none";
      this.elements.noSelection.style.display = "block";
      this.elements.title.textContent = "Node Editor";
      document.querySelectorAll(".save-button").forEach((button) => {
        button.style.display = "none";
      });
      return;
    }

    console.log("Node type:", node.constructor.name);
    console.log("Node properties:", node.properties);

    this.elements.content.style.display = "block";
    this.elements.noSelection.style.display = "none";
    this.elements.title.textContent = `Edit ${node.title}`;

    // Handle different node types
    if (node.constructor.name === "PipecatFunctionNode") {
      this.elements.messageEditor.style.display = "none";
      this.elements.functionEditor.style.display = "block";

      const functionData = {
        type: "function",
        function: node.properties.function,
      };
      this.editors.function.setValue(functionData);
    } else {
      this.elements.messageEditor.style.display = "block";
      this.elements.functionEditor.style.display = "none";

      // Show/hide role messages editor based on node type
      const roleMessagesContainer = document.getElementById(
        "role-messages-container",
      );
      if (node.constructor.name === "PipecatStartNode") {
        roleMessagesContainer.style.display = "block";
        this.editors.roleMessages.setValue(node.properties.role_messages || []);
      } else {
        roleMessagesContainer.style.display = "none";
      }

      this.editors.taskMessages.setValue(node.properties.task_messages || []);
      this.editors.preActions.setValue(node.properties.pre_actions || []);
      this.editors.postActions.setValue(node.properties.post_actions || []);
    }

    // Hide save button initially
    document.querySelectorAll(".save-button").forEach((button) => {
      button.style.display = "none";
    });
  }
}
