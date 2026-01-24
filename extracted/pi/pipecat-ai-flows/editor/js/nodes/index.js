/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import { LiteGraph } from "litegraph.js";

import { PipecatStartNode } from "./startNode.js";
import { PipecatFlowNode } from "./flowNode.js";
import { PipecatEndNode } from "./endNode.js";
import { PipecatFunctionNode } from "./functionNode.js";
import { PipecatMergeNode } from "./mergeNode.js";

/**
 * Registers all node types with LiteGraph
 */
export function registerNodes() {
  LiteGraph.registerNodeType("nodes/Start", PipecatStartNode);
  LiteGraph.registerNodeType("nodes/Flow", PipecatFlowNode);
  LiteGraph.registerNodeType("nodes/End", PipecatEndNode);
  LiteGraph.registerNodeType("nodes/Function", PipecatFunctionNode);
  LiteGraph.registerNodeType("flow/Merge", PipecatMergeNode);
}

export {
  PipecatStartNode,
  PipecatFlowNode,
  PipecatEndNode,
  PipecatFunctionNode,
  PipecatMergeNode,
};
