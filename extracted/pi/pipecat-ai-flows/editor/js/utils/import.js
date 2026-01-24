/**
 * Copyright (c) 2024, Daily
 *
 * SPDX-License-Identifier: BSD 2-Clause License
 */

import {
  PipecatStartNode,
  PipecatFlowNode,
  PipecatEndNode,
  PipecatFunctionNode,
  PipecatMergeNode,
} from "../nodes/index.js";
import dagre from "dagre";

/**
 * Creates a graph from a flow configuration
 * @param {LGraph} graph - The LiteGraph instance
 * @param {FlowConfig} flowConfig - The flow configuration
 */
export function createFlowFromConfig(graph, flowConfig) {
  // Clear existing graph
  graph.clear();

  const nodeSpacing = {
    horizontal: 400,
    vertical: 150,
  };
  /** @type {Object.<string, { node: LGraphNode, config: any }>} */
  const nodes = {};

  // Create dagre graph
  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: "LR", // Left to right layout
    nodesep: nodeSpacing.vertical,
    ranksep: nodeSpacing.horizontal,
    edgesep: 50,
    marginx: 100,
    marginy: 100,
  });
  g.setDefaultEdgeLabel(() => ({}));

  // Create nodes based on configuration
  Object.entries(flowConfig.nodes).forEach(([nodeId, nodeConfig]) => {
    let node;

    if (nodeId === flowConfig.initial_node) {
      // Create start node with the initial_node name
      node = new PipecatStartNode();
      node.title = nodeId;
    } else if (nodeId === "end") {
      node = new PipecatEndNode();
      node.title = nodeId;
    } else {
      node = new PipecatFlowNode();
      node.title = nodeId;
    }

    // Set node properties
    node.properties = {
      task_messages: nodeConfig.task_messages,
      pre_actions: nodeConfig.pre_actions || [],
      post_actions: nodeConfig.post_actions || [],
    };

    if (nodeConfig.role_messages?.length > 0) {
      node.properties.role_messages = nodeConfig.role_messages;
    }

    graph.add(node);
    nodes[nodeId] = { node, config: nodeConfig };

    // Add to dagre graph
    g.setNode(nodeId, {
      width: node.size[0],
      height: node.size[1],
      node: node,
    });
  });

  // Track function nodes and merge nodes for edge creation
  const functionNodes = new Map();
  const mergeNodes = new Map();

  // Create function nodes and analyze connections
  Object.entries(flowConfig.nodes).forEach(([sourceNodeId, nodeConfig]) => {
    if (nodeConfig.functions) {
      nodeConfig.functions.forEach((funcConfig) => {
        const functionNode = new PipecatFunctionNode();
        functionNode.properties.function = { ...funcConfig.function };

        graph.add(functionNode);

        // Add function node to dagre graph
        const funcNodeId = `func_${sourceNodeId}_${functionNode.properties.function.name}`;
        g.setNode(funcNodeId, {
          width: functionNode.size[0],
          height: functionNode.size[1],
          node: functionNode,
        });

        // Connect source to function node
        g.setEdge(sourceNodeId, funcNodeId);

        // If has transition_to, connect to target node
        if (funcConfig.function.transition_to) {
          g.setEdge(funcNodeId, funcConfig.function.transition_to);
        }

        functionNodes.set(functionNode, {
          source: nodes[sourceNodeId].node,
          target: nodes[funcConfig.function.transition_to]?.node,
          targetName: funcConfig.function.transition_to,
          funcNodeId: funcNodeId,
        });
      });
    }
  });

  // Group function nodes by target for merge nodes
  const targetToFunctions = new Map();
  functionNodes.forEach((data, functionNode) => {
    if (!targetToFunctions.has(data.targetName)) {
      targetToFunctions.set(data.targetName, []);
    }
    targetToFunctions.get(data.targetName).push({ functionNode, ...data });
  });

  // Create merge nodes where needed and connect in dagre
  targetToFunctions.forEach((functions, targetName) => {
    if (functions.length > 1 && nodes[targetName]) {
      // Create merge node
      const mergeNode = new PipecatMergeNode();
      while (mergeNode.inputs.length < functions.length) {
        mergeNode.addInput(`In ${mergeNode.inputs.length + 1}`, "flow");
        mergeNode.size[1] += 20;
      }
      graph.add(mergeNode);

      // Add merge node to dagre
      const mergeNodeId = `merge_${targetName}`;
      g.setNode(mergeNodeId, {
        width: mergeNode.size[0],
        height: mergeNode.size[1],
        node: mergeNode,
      });

      // Connect function nodes to merge node in dagre
      functions.forEach(({ funcNodeId }) => {
        g.setEdge(funcNodeId, mergeNodeId);
      });

      // Connect merge node to target in dagre
      g.setEdge(mergeNodeId, targetName);

      // Store for later LiteGraph connection
      mergeNodes.set(mergeNode, {
        sources: functions.map((f) => f.functionNode),
        target: nodes[targetName].node,
      });
    } else if (nodes[targetName]) {
      // Direct connection in dagre
      g.setEdge(functions[0].funcNodeId, targetName);
    }
  });

  // Apply dagre layout
  dagre.layout(g);

  // Apply positions from dagre to nodes
  g.nodes().forEach((nodeId) => {
    const dagreNode = g.node(nodeId);
    if (dagreNode.node) {
      dagreNode.node.pos = [dagreNode.x, dagreNode.y];
    }
  });

  // Create LiteGraph connections
  functionNodes.forEach((connections, functionNode) => {
    connections.source.connect(0, functionNode, 0);
  });

  mergeNodes.forEach((connections, mergeNode) => {
    connections.sources.forEach((source, index) => {
      source.connect(0, mergeNode, index);
    });
    mergeNode.connect(0, connections.target, 0);
  });

  // Connect function nodes to their targets when no merge node is involved
  functionNodes.forEach((connections, functionNode) => {
    if (
      connections.target &&
      !Array.from(mergeNodes.values()).some((mergeData) =>
        mergeData.sources.includes(functionNode),
      )
    ) {
      functionNode.connect(0, connections.target, 0);
    }
  });

  graph.setDirtyCanvas(true, true);
}
