/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

/**
 * Singleton class to manage global editor state
 */
class EditorState {
  /** @type {EditorState|null} */
  static instance = null;

  /**
   * Creates or returns the EditorState singleton
   */
  constructor() {
    if (EditorState.instance) {
      return EditorState.instance;
    }
    /** @type {SidePanel|null} */
    this.sidePanel = null;
    EditorState.instance = this;
  }

  /**
   * Sets the side panel instance
   * @param {SidePanel} sidePanel
   */
  setSidePanel(sidePanel) {
    this.sidePanel = sidePanel;
  }

  /**
   * Updates the side panel with node data
   * @param {PipecatBaseNode|null} node
   */
  updateSidePanel(node) {
    if (this.sidePanel) {
      this.sidePanel.updatePanel(node);
    }
  }
}

export const editorState = new EditorState();
