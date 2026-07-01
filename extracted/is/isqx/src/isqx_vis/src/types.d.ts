/** A unique, dot-separated string identifier for a quantity kind. */
export type CanonicalPath = string;

/** A numeric index corresponding to a node's position in the `nodes` array. */
export type NodeIndex = number;

//
// raw data structures from objects.json
//

export type StrFragment = string | { text: string; path: CanonicalPath };

/** A unit of measurement. */
export type Unit = StrFragment | StrFragment[]; // this will change in the future

/** A variable within the context of an equation. */
export interface WhereClause {
  symbol: string;
  description: StrFragment | StrFragment[];
  unit?: Unit;
}

export interface KaTeXWhere {
  katex: string;
  where?: WhereClause[];
}

export interface SymbolDetail extends KaTeXWhere {
  remarks?: string;
}

export interface EquationDetail extends KaTeXWhere {
  assumptions?: (StrFragment | StrFragment[])[];
}

export interface WikidataDetail {
  qcode: string;
}

export interface QtyKindDetail {
  parent?: CanonicalPath;
  unit_si_coherent?: Unit;
  tags?: string[];
  wikidata?: WikidataDetail[];
  symbols?: SymbolDetail[];
  equations?: EquationDetail[];
}

/** The root data structure loaded from the `objects.json` file. */
export type QtyKindData = Record<CanonicalPath, QtyKindDetail>;

export interface Quantity {
  value: string; // for now
  unit: Unit | null;
}

export type ConstantsData = Record<CanonicalPath, Quantity>;

export type UnitsData = Record<CanonicalPath, Unit>;

export interface IsqxData {
  qtyKinds: QtyKindData;
  constants: ConstantsData;
  units?: UnitsData; // empty for now until we figure out how to serialise things properly
}

//
// processed graph and state structures
//

/**
 * A node in the graph after being processed for visualization.
 * It contains layout information from D3 and a reference to its original data.
 */
export interface GraphNode {
  canonicalPath: CanonicalPath;
  details: QtyKindDetail;
  x: number;
  y: number;
  radius: number;
  isGroup: boolean;
  value: number;
}

/**
 * A link between two nodes, using numeric indices.
 * This is the final link structure used by the application state.
 */
export interface GraphLink {
  source: NodeIndex;
  target: NodeIndex;
}

/** The main reactive state of the application. */
export interface AppState {
  data: QtyKindData | null;
  nodes: GraphNode[];
  links: GraphLink[];
  linkMap: Map<number, GraphLink[]>;
  colorMap: string[];
  ui: {
    /** The indices of all nodes the user has explicitly clicked to select. */
    selectedNodeIndices: NodeIndex[];
    /** The index of the node currently under the pointer (hovered), or null. */
    highlightedNodeIndex: NodeIndex | null;
    /** The current zoom and pan state of the SVG canvas. */
    view: { k: number; x: number; y: number };
  };
}
