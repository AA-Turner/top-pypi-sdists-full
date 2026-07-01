import * as d3 from "d3";
import type {
  QtyKindData,
  QtyKindDetail,
  GraphNode,
  GraphLink,
  CanonicalPath,
  NodeIndex
} from "./types";
import { findCanonicalPathInDescription } from "./utils";

export const VIEWBOX_WIDTH = 1024;
export const VIEWBOX_HEIGHT = 1024;

interface SimulationNode {
  canonicalPath: CanonicalPath;
  details: QtyKindDetail;
  x: number;
  y: number;
  r: number;
  numIncomingLinks: number;
  parent: SimulationNode | null;
  children: SimulationNode[] | null;
  value?: number;
  depth?: number;
  relX?: number;
  relY?: number;
}

/**
 * Creates the initial node and link structures from the raw data.
 */
function createSimulationGraph(qtyKindData: QtyKindData): {
  nodes: SimulationNode[];
  simulationLinks: { source: SimulationNode; target: SimulationNode }[];
} {
  const canonicalPaths = Object.keys(qtyKindData);
  const pathToIndex = new Map<CanonicalPath, NodeIndex>(
    canonicalPaths.map((p, i) => [p, i])
  );

  const nodes: SimulationNode[] = canonicalPaths.map(path => ({
    canonicalPath: path,
    details: qtyKindData[path],
    x: 0,
    y: 0,
    r: 0,
    parent: null,
    children: [],
    numIncomingLinks: 0
  }));

  const numIncomingLinks = new Array(nodes.length).fill(0);
  const simulationLinks: { source: SimulationNode; target: SimulationNode }[] =
    [];

  nodes.forEach((sourceNode, sourceIndex) => {
    sourceNode.details.equations?.forEach(eq => {
      eq.where?.forEach(clause => {
        const targetPath = findCanonicalPathInDescription(clause.description);
        if (!targetPath) return;

        const targetIndex = pathToIndex.get(targetPath);
        if (targetIndex === undefined || targetIndex === sourceIndex) return;

        simulationLinks.push({
          source: sourceNode,
          target: nodes[targetIndex]
        });
        numIncomingLinks[targetIndex]++;
      });
    });
  });

  nodes.forEach((node, i) => {
    node.numIncomingLinks = numIncomingLinks[i];
  });

  return { nodes, simulationLinks };
}

/**
 * Arranges nodes into a parent-child hierarchy and applies d3.pack and
 * d3.forceSimulation to calculate the final layout.
 */
function layoutGraph(
  nodes: SimulationNode[],
  simulationLinks: { source: SimulationNode; target: SimulationNode }[]
): SimulationNode[] {
  const rootNodes: SimulationNode[] = [];
  const pathToNode = new Map(nodes.map(n => [n.canonicalPath, n]));

  nodes.forEach(node => {
    const parentPath = node.details.parent;
    const parent = parentPath ? pathToNode.get(parentPath) : null;
    if (parent) {
      parent.children!.push(node);
      node.parent = parent;
    } else {
      rootNodes.push(node);
    }
  });

  const hierarchyRoot: SimulationNode = {
    canonicalPath: "root",
    details: {} as any,
    x: 0,
    y: 0,
    r: 0,
    parent: null,
    children: rootNodes,
    numIncomingLinks: 0
  };

  const hierarchy = d3
    .hierarchy(hierarchyRoot)
    .sum(d => (d.children?.length ? 0 : d.numIncomingLinks || 1) + 1)
    .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));

  const root = d3
    .pack<SimulationNode>()
    .size([VIEWBOX_WIDTH, VIEWBOX_HEIGHT])
    .padding(20)(hierarchy);

  const d3Nodes = root.descendants().slice(1);

  for (const hNode of d3Nodes) {
    const node = hNode.data;
    Object.assign(node, {
      x: hNode.x,
      y: hNode.y,
      r: hNode.r,
      value: hNode.value,
      depth: hNode.depth
    });
    if (hNode.parent && hNode.parent.data.canonicalPath !== "root") {
      Object.assign(node, {
        relX: hNode.x - hNode.parent.x,
        relY: hNode.y - hNode.parent.y
      });
    }
  }

  const topLevelNodes = root.children?.map(c => c.data) ?? [];
  const getTopLevel = (node: SimulationNode): SimulationNode => {
    let current = node;
    while (current.parent && current.parent.canonicalPath !== "root") {
      current = current.parent;
    }
    return current;
  };

  const forceLinks = simulationLinks
    .map(l => ({
      source: getTopLevel(l.source),
      target: getTopLevel(l.target)
    }))
    .filter(l => l.source !== l.target);

  const yPosScale = d3
    .scalePow()
    .exponent(0.5)
    .domain([0, d3.max(topLevelNodes, n => n.value) ?? 1])
    .range([VIEWBOX_HEIGHT * 0.8, VIEWBOX_HEIGHT * 0.2]);

  d3.forceSimulation(topLevelNodes)
    .force(
      "link",
      d3
        .forceLink(forceLinks)
        .strength(l => 4 / Math.min(l.source.value ?? 1, l.target.value ?? 1))
        .distance(d => d.source.r + d.target.r + 30)
    )
    .force("charge", d3.forceManyBody().strength(-120))
    .force(
      "collide",
      d3
        .forceCollide()
        .radius(d => d.r + 10)
        .strength(0.5)
    )
    .force("x", d3.forceX(VIEWBOX_WIDTH / 2).strength(0.02))
    .force("y", d3.forceY(d => yPosScale(d.value ?? 0)).strength(0.06))
    .tick(250);

  const finalSimNodes = d3Nodes.map(hNode => hNode.data);
  finalSimNodes.sort((a, b) => (a.depth ?? 0) - (b.depth ?? 0));

  for (const simNode of finalSimNodes) {
    if (simNode.parent && simNode.parent.canonicalPath !== "root") {
      simNode.x = simNode.parent.x + (simNode.relX ?? 0);
      simNode.y = simNode.parent.y + (simNode.relY ?? 0);
    }
  }
  return finalSimNodes;
}

export function processGraphData(qtyKindData: QtyKindData | null): {
  nodes: GraphNode[];
  links: GraphLink[];
  linkMap: Map<number, GraphLink[]>;
} {
  if (!qtyKindData) return { nodes: [], links: [], linkMap: new Map() };

  const { nodes: initialNodes, simulationLinks } =
    createSimulationGraph(qtyKindData);
  const finalSimNodes = layoutGraph(initialNodes, simulationLinks);

  const finalPathToIndex = new Map<CanonicalPath, NodeIndex>(
    finalSimNodes.map((n, i) => [n.canonicalPath, i])
  );

  const graphNodes: GraphNode[] = finalSimNodes.map(n => ({
    canonicalPath: n.canonicalPath,
    details: n.details,
    x: n.x,
    y: n.y,
    radius: n.r,
    isGroup: !!n.children?.length,
    value: n.value ?? 0
  }));

  const links: GraphLink[] = simulationLinks.map(link => ({
    source: finalPathToIndex.get(link.source.canonicalPath)!,
    target: finalPathToIndex.get(link.target.canonicalPath)!
  }));

  const linkMap = new Map<number, GraphLink[]>();
  for (const link of links) {
    if (!linkMap.has(link.source)) linkMap.set(link.source, []);
    linkMap.get(link.source)!.push(link);

    if (link.source !== link.target) {
      if (!linkMap.has(link.target)) linkMap.set(link.target, []);
      linkMap.get(link.target)!.push(link);
    }
  }

  return { nodes: graphNodes, links, linkMap };
}
