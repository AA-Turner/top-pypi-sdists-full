# cython: language_level=3
from heapq import heappush, heappop

cpdef tuple c_bidirectional_dijkstra(G, source, target, weight='weight'):
    if source == target:
        return 0.0, [source]

    cdef dict adj = G._adj

    cdef list q_fwd = []
    cdef list q_bwd = []

    cdef dict dist_fwd = {source: 0.0}
    cdef dict dist_bwd = {target: 0.0}

    cdef dict pred_fwd = {}
    cdef dict pred_bwd = {}

    cdef double best = float("inf")
    cdef object meeting_node = None

    cdef object u, v, edge
    cdef double d, du, new_d, w

    cdef object push = heappush
    cdef object pop = heappop

    push(q_fwd, (0.0, source))
    push(q_bwd, (0.0, target))

    cdef bint use_callable = callable(weight)

    while q_fwd and q_bwd:

        # ---------------- FORWARD ----------------
        d, u = pop(q_fwd)

        if d > dist_fwd.get(u, float("inf")):
            continue

        du = d

        if u in dist_bwd:
            new_d = du + dist_bwd[u]
            if new_d < best:
                best = new_d
                meeting_node = u

        for v, edge in adj[u].items():

            if use_callable:
                w = weight(u, v, edge)
            else:
                w = edge.get(weight, 1.0)

            new_d = du + w

            if new_d < dist_fwd.get(v, float("inf")):
                dist_fwd[v] = new_d
                pred_fwd[v] = u
                push(q_fwd, (new_d, v))

        # ---------------- BACKWARD ----------------
        d, u = pop(q_bwd)

        if d > dist_bwd.get(u, float("inf")):
            continue

        du = d

        if u in dist_fwd:
            new_d = du + dist_fwd[u]
            if new_d < best:
                best = new_d
                meeting_node = u

        for v, edge in adj[u].items():

            if use_callable:
                w = weight(u, v, edge)
            else:
                w = edge.get(weight, 1.0)

            new_d = du + w

            if new_d < dist_bwd.get(v, float("inf")):
                dist_bwd[v] = new_d
                pred_bwd[v] = u
                push(q_bwd, (new_d, v))

        # early stop
        if best < float("inf"):
            if q_fwd and q_bwd:
                if q_fwd[0][0] + q_bwd[0][0] >= best:
                    break

    if meeting_node is None:
        return float("inf"), []

    # path reconstruction
    cdef list path_fwd = []
    cdef list path_bwd = []

    u = meeting_node
    while u in pred_fwd:
        path_fwd.append(u)
        u = pred_fwd[u]

    path_fwd.append(source)
    path_fwd.reverse()

    u = meeting_node
    while u in pred_bwd:
        u = pred_bwd[u]
        path_bwd.append(u)

    return best, path_fwd + path_bwd

def c_astar_path(G, source, target, heuristic=None, weight='weight', *, cutoff=None):
    raise Exception("Not (astar_path) implemented yet")

# -------------------------
# NodeView helper
# -------------------------
cdef class NodeView:
    cdef dict _adj
    cdef dict _node_attr

    def __init__(self, adj, node_attr):
        self._adj = adj
        self._node_attr = node_attr

    def __iter__(self):
        return iter(self._adj)

    def __len__(self):
        return len(self._adj)

    def __getitem__(self, node):
        return self._node_attr.get(node, {})

    def __contains__(self, node):
        return node in self._adj

    def __call__(self, data=False, default=None):
        if data is False:
            return iter(self._adj)
        if data is True:
            return ((n, self._node_attr.get(n, {})) for n in self._adj)
        # data is a specific attribute key
        return ((n, self._node_attr.get(n, {}).get(data, default)) for n in self._adj)

    def __repr__(self):
        return f"NodeView({list(self._adj.keys())})"

# -------------------------
# EdgeView helper
# -------------------------
cdef class EdgeView:
    cdef dict _adj
    cdef dict _edge_attr
    cdef bint _directed

    def __init__(self, adj, edge_attr, directed=False):
        self._adj = adj
        self._edge_attr = edge_attr
        self._directed = directed

    def __iter__(self):
        seen = set()
        for u, nbrs in self._adj.items():
            for v in nbrs:
                if self._directed or (v, u) not in seen:
                    yield (u, v)
                    seen.add((u, v))

    def __len__(self):
        cdef int count = 0
        seen = set()
        for u, nbrs in self._adj.items():
            for v in nbrs:
                if self._directed or (v, u) not in seen:
                    count += 1
                    seen.add((u, v))
        return count

    def __getitem__(self, edge):
        cdef object u, v
        u, v = edge
        return self._edge_attr.get((u, v), self._edge_attr.get((v, u), {}))

    def __contains__(self, edge):
        cdef object u, v
        u, v = edge
        if u in self._adj and v in self._adj[u]:
            return True
        if not self._directed and v in self._adj and u in self._adj[v]:
            return True
        return False

    def __call__(self, data=False, default=None, nbunch=None):
        nodes = set(nbunch) if nbunch is not None else None
        seen = set()

        for u, nbrs in self._adj.items():
            if nodes is not None and u not in nodes:
                continue
            for v in nbrs:
                if self._directed or (v, u) not in seen:
                    if nodes is None or u in nodes or v in nodes:
                        if data is False:
                            yield (u, v)
                        elif data is True:
                            key = (u, v) if (u, v) in self._edge_attr else (v, u)
                            yield (u, v, self._edge_attr.get(key, {}))
                        else:
                            key = (u, v) if (u, v) in self._edge_attr else (v, u)
                            yield (u, v, self._edge_attr.get(key, {}).get(data, default))
                    seen.add((u, v))

    def __repr__(self):
        return f"EdgeView({list(self.__iter__())})"

cdef class CGraph:
    # internal data structures
    cdef dict adj
    cdef dict node_attr
    cdef NodeView _nodes_view     # cache the view
    cdef EdgeView _edges_view     # cache the view

    # graph-level attributes
    cdef public dict graph
    cdef public object kdtree


    def __init__(self):
        self.adj = {}
        self.node_attr = {}
        self._nodes_view = NodeView(self.adj, self.node_attr)
        self._edges_view = EdgeView(self.adj, self.node_attr)

        # kdtree
        self.graph = {}
        self.kdtree = None


    def __contains__(self, node):
        return node in self.adj

    def __iter__(self):
        return iter(self.adj)

    def __len__(self):
        return len(self.adj)


    # getter
    @property
    def _adj(self):
        return self.adj

    # setter
    @_adj.setter
    def _adj(self, edges_data):
        self.add_edges_from(edges_data)


    # getter
    @property
    def _node(self):
        return self.node_attr

    # setter
    @_node.setter
    def _node(self, nodes_data):
        self.add_nodes_from(nodes_data)


    @property
    def nodes(self):
        return self._nodes_view

    @property
    def edges(self):
        return self._edges_view

    # -------------------------
    # Node operations
    # -------------------------
    def add_node(self, node, **attr):
        cdef dict attrs

        if node not in self.adj:
            self.adj[node] = {}
            self.node_attr[node] = {}

        if attr:
            attrs = self.node_attr[node]
            attrs.update(attr)

    cpdef get_node_attr(self, node):
        return self.node_attr.get(node, {})

    # -------------------------
    # Edge operations
    # -------------------------
    def add_edge(self, u, v, **attr):
        cdef dict nbrs

        if u not in self.adj:
            self.adj[u] = {}
            self.node_attr[u] = {}

        if v not in self.adj:
            self.adj[v] = {}
            self.node_attr[v] = {}

        nbrs = self.adj[u]
        nbrs[v] = dict(attr)

    cpdef get_edge_attr(self, u, v):
        if u in self.adj and v in self.adj[u]:
            return self.adj[u][v]
        return None

    # -------------------------
    # Subgraph (node induced)
    # -------------------------
    cpdef subgraph(self, nodes):
        cdef CGraph g = CGraph()
        cdef dict nbrs
        cdef object u, v

        nodes_set = set(nodes)

        for u in nodes_set:
            if u in self.adj:
                g.add_node(u, **self.node_attr.get(u, {}))

        for u in nodes_set:
            if u in self.adj:
                nbrs = self.adj[u]
                for v in nbrs:
                    if v in nodes_set:
                        g.add_edge(u, v, **nbrs[v])

        return g


    cpdef get_edge_data(self, u, v):
        if u in self.adj and v in self.adj[u]:
            return self.adj[u][v]
        return None

    # -------------------------
    # Edge subgraph
    # -------------------------
    cpdef edge_subgraph(self, edges):
        cdef CGraph g = CGraph()
        cdef object u, v, eattr

        for (u, v) in edges:
            if u in self.adj and v in self.adj[u]:
                g.add_node(u, **self.node_attr.get(u, {}))
                g.add_node(v, **self.node_attr.get(v, {}))
                eattr = self.adj[u][v]
                g.add_edge(u, v, **eattr)

        return g

    # -------------------------
    # Helpers
    # -------------------------
    cpdef add_nodes_from(self, dict nodes):
        cdef object node
        cdef dict attr

        for node, attr in nodes.items():
            if attr is None:
                attr = {}
            self.add_node(node, **attr)

    cpdef add_edges_from(self, dict edges):
        cdef object u, v
        cdef object attr
        cdef dict v_s

        for u, v_s in edges.items():
            for v, attr in v_s.items():

                if attr is None:
                    self.add_edge(u, v)
                else:
                    self.add_edge(u, v, **attr)


    cpdef neighbors(self, node):
        if node in self.adj:
            return self.adj[node].keys()
        return []

    def __copy__(self):
        cdef CGraph result
        result = self.__class__.__new__(self.__class__)

        result.adj = self.adj.copy()   # valid
        result.node_attr = self.node_attr.copy()   # valid
        result.graph = self.graph.copy()   # valid
        result.kdtree = self.kdtree if self.kdtree is not None else None
        result._nodes_view = NodeView(result.adj, result.node_attr)  # create a new NodeView for the copied graph
        result._edges_view = EdgeView(result.adj, result.node_attr)  # create a new EdgeView for the copied graph
        return result



    def __repr__(self):
        cls_name = self.__class__.__name__

        if self.adj is None:
            return f"<{cls_name} uninitialized>"

        return f"<{cls_name} nodes={len(self.adj)}>"

