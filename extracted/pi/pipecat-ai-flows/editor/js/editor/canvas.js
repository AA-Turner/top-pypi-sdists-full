/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { LGraphCanvas } from "litegraph.js";

/**
 * Sets up the canvas and its event handlers
 * @param {LGraph} graph - The LiteGraph instance
 * @returns {LGraphCanvas} The configured canvas instance
 */
export function setupCanvas(graph) {
  const canvas = new LGraphCanvas("#graph-canvas", graph);

  document.getElementById("zoom-in").onclick = () => {
    if (canvas.ds.scale < 2) {
      // Limit max zoom
      canvas.ds.scale *= 1.2;
      canvas.setDirty(true, true);
    }
  };

  document.getElementById("zoom-out").onclick = () => {
    if (canvas.ds.scale > 0.2) {
      // Limit min zoom
      canvas.ds.scale *= 0.8;
      canvas.setDirty(true, true);
    }
  };

  /**
   * Resizes the canvas to fit its container
   */
  function resizeCanvas() {
    const canvasElement = document.getElementById("graph-canvas");
    const container = document.getElementById("graph-container");
    canvasElement.width = container.offsetWidth;
    canvasElement.height = container.offsetHeight;
  }

  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  return canvas;
}
