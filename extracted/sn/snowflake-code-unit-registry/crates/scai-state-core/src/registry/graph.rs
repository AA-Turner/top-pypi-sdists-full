//! Dependency-graph refresh engine.
//!
//! Provides reusable traversal utilities over CodeUnit dependency edges
//! (`predecessors`, `successors`, `build_successors_map`, `topo_sort`,
//! `expand_scope`) and a [`RefreshState`] computation struct that accumulates
//! derived fields during traversals and applies them in a single pass.
//!
//! Edge direction: if A depends on B (A -> B):
//!   - B is A's **predecessor** — B must be deployed before A
//!   - A is B's **successor**   — A is deployed after B
//!
//! `predecessors(A)` yields B — follows `dependsOn` (what must come before A)
//! `successors(B)`   yields A — follows `requiredBy` (what comes after B)
//! `dependsOn` self-references (`A -> A`, from the unit root or any part) are
//! ignored for deployment ordering (topological rank and cycle detection) but
//! remain in stored `dependsOn`.

use std::collections::{HashMap, HashSet, VecDeque};

use crate::dependency_view;
use crate::error::*;
use crate::generated::types::CodeUnit;

// ── Public interface ────────────────────────────────────────────────────

/// Mutable graph view over loaded units for dependency refresh.
pub(super) struct RegistryGraph<'a> {
    units: &'a mut [CodeUnit],
    id_to_index: &'a HashMap<String, usize>,
}

impl<'a> RegistryGraph<'a> {
    pub(super) fn new(units: &'a mut [CodeUnit], id_to_index: &'a HashMap<String, usize>) -> Self {
        Self { units, id_to_index }
    }

    /// Full refresh: recompute derived fields for all units.
    /// Returns the indices of units whose fields actually changed.
    pub(super) fn refresh(&mut self, strict: bool) -> Result<Vec<usize>> {
        let scope: HashSet<usize> = (0..self.units.len()).collect();
        self.refresh_scope(&scope, strict)
    }

    /// Scoped refresh: recompute derived fields for nodes reachable from seeds.
    /// Returns the indices of units whose fields actually changed.
    pub(super) fn refresh_scoped(&mut self, seeds: &[usize], strict: bool) -> Result<Vec<usize>> {
        let scope = expand_scope(seeds, self.units, self.id_to_index);
        self.refresh_scope(&scope, strict)
    }

    fn refresh_scope(&mut self, scope: &HashSet<usize>, strict: bool) -> Result<Vec<usize>> {
        if scope.is_empty() {
            return Ok(vec![]);
        }

        // Build successors map (for each node, who depends on it) and topologically sort the scope.
        let successors_map = build_successors_map(self.units, self.id_to_index);
        let (topo_order, cycle_affected) = topo_sort(&successors_map, scope);

        if strict && !cycle_affected.is_empty() {
            let mut ids: Vec<&str> = cycle_affected
                .iter()
                .filter_map(|&i| self.units[i].id.as_deref())
                .collect();
            ids.sort_unstable();
            return CycleDetectedSnafu {
                message: ids.join(" -> "),
            }
            .fail();
        }

        let mut state = RefreshState::new(self.units.len());

        // Pass 1: order-independent fields (predecessor_is_missing, required_by, predecessor cache).
        for &i in scope {
            state.resolve_unit_edges(i, self.units, self.id_to_index, &successors_map[i]);
        }

        // Cycle-affected nodes get rank -1 and transitive_missing = true.
        for &idx in &cycle_affected {
            state.mark_cycle(idx);
        }

        // Pass 2: topo-order-dependent fields (rank, transitive_missing propagation).
        for &idx in &topo_order {
            state.propagate_from_predecessors(idx);
        }

        // Pass 3: collect dirty indices. `scope` is a `HashSet`, so each is
        // unique — `refresh_and_sync` relies on this for parallel write-back.
        let mut dirty = Vec::new();
        for &i in scope {
            if state.apply(i, &mut self.units[i]) {
                dirty.push(i);
            }
        }

        Ok(dirty)
    }
}

// ── Traversal utilities ─────────────────────────────────────────────────

/// True when a `dependsOn` edge points at the unit itself (self-FK or dbt `{{ this }}`).
/// Self-loops are not deployment cycles and are dropped from ranking/cycle detection.
fn is_self_dep(unit_id: Option<&str>, dep_id: Option<&str>) -> bool {
    unit_id.is_some() && dep_id == unit_id
}

/// Indices of this unit's predecessors (units it depends on).
/// A depends on B means B is A's predecessor.
fn predecessors<'a>(
    unit: &'a CodeUnit,
    id_to_index: &'a HashMap<String, usize>,
) -> impl Iterator<Item = usize> + 'a {
    dependency_view::depends_on_with_origin(unit).filter_map(move |(_origin, dep)| {
        let id = dep.id.as_deref()?;
        if is_self_dep(unit.id.as_deref(), Some(id)) {
            return None;
        }
        id_to_index.get(id).copied()
    })
}

/// Indices of this unit's successors (units that depend on it),
/// from stored `requiredBy`.
fn successors<'a>(
    unit: &'a CodeUnit,
    id_to_index: &'a HashMap<String, usize>,
) -> impl Iterator<Item = usize> + 'a {
    dependency_view::required_by(unit).filter_map(|id| id_to_index.get(id).copied())
}

/// For each node, lists its successors (nodes that depend on it).
/// Built from `dependsOn` edges: if A depends on B, A is added to `successors_map[B]`.
fn build_successors_map(
    units: &[CodeUnit],
    id_to_index: &HashMap<String, usize>,
) -> Vec<Vec<usize>> {
    let mut successors_map = vec![vec![]; units.len()];
    for (i, unit) in units.iter().enumerate() {
        for pred_idx in predecessors(unit, id_to_index) {
            successors_map[pred_idx].push(i);
        }
    }
    successors_map
}

/// Kahn's topological sort over nodes in scope (dependency order).
///
/// Returns `(topo_order, cycle_affected)`. Only edges between nodes in
/// `scope` participate; nodes outside scope are ignored.
/// In-degrees are derived from `successors_map` so no additional dependency
/// traversal is needed.
fn topo_sort(
    successors_map: &[Vec<usize>],
    scope: &HashSet<usize>,
) -> (Vec<usize>, HashSet<usize>) {
    let n = successors_map.len();
    let mut in_degree = vec![0usize; n];
    for &i in scope {
        for &succ in &successors_map[i] {
            if scope.contains(&succ) {
                in_degree[succ] += 1;
            }
        }
    }

    let mut queue: VecDeque<usize> = scope
        .iter()
        .copied()
        .filter(|&i| in_degree[i] == 0)
        .collect();

    let mut topo_order = Vec::with_capacity(scope.len());
    while let Some(idx) = queue.pop_front() {
        topo_order.push(idx);
        for &succ in &successors_map[idx] {
            if !scope.contains(&succ) {
                continue;
            }
            in_degree[succ] -= 1;
            if in_degree[succ] == 0 {
                queue.push_back(succ);
            }
        }
    }

    let ordered: HashSet<usize> = topo_order.iter().copied().collect();
    let cycle_affected: HashSet<usize> = scope.difference(&ordered).copied().collect();

    (topo_order, cycle_affected)
}

/// BFS from seeds following predecessors and successors until no new nodes are found.
fn expand_scope(
    seeds: &[usize],
    units: &[CodeUnit],
    id_to_index: &HashMap<String, usize>,
) -> HashSet<usize> {
    let mut scope = HashSet::new();
    let mut queue: VecDeque<usize> = seeds.iter().copied().collect();

    while let Some(idx) = queue.pop_front() {
        if !scope.insert(idx) {
            continue;
        }
        for pred in predecessors(&units[idx], id_to_index) {
            if !scope.contains(&pred) {
                queue.push_back(pred);
            }
        }
        for succ in successors(&units[idx], id_to_index) {
            if !scope.contains(&succ) {
                queue.push_back(succ);
            }
        }
    }

    scope
}

// ── Refresh computation ─────────────────────────────────────────────────

/// Accumulated state for derived-field computation during refresh.
///
/// Adding a new derived field:
/// 1. Add a storage array here
/// 2. Add computation in [`resolve_unit_edges`](Self::resolve_unit_edges) (order-independent)
///    or [`propagate_from_predecessors`](Self::propagate_from_predecessors) (needs topo order)
/// 3. Add a `set_*` helper below
/// 4. Add one `set_*` call in [`apply`](Self::apply)
struct RefreshState {
    /// Topological rank per unit: 0 for leaves (no predecessors), max(predecessor ranks) + 1
    /// otherwise, or -1 for units involved in a cycle.
    ranks: Vec<i64>,

    /// IDs of successor units (units that depend on this one), written to `dependencies.requiredBy`.
    required_by: Vec<Vec<String>>,

    /// Per-dependency `isMissing` flag: true when the dependency's target is absent from the registry.
    predecessor_is_missing: Vec<Vec<bool>>,

    /// True when the unit itself has a missing dependency **or** any of its predecessors do
    /// (i.e., the missing-dep signal propagates transitively up the dependency chain).
    /// Also set to true for units involved in a cycle.
    transitive_missing: Vec<bool>,

    /// Resolved predecessor indices (dependsOn), cached during `resolve_unit_edges` for `propagate_from_predecessors`.
    predecessor_indices: Vec<Vec<usize>>,
}

impl RefreshState {
    fn new(n: usize) -> Self {
        Self {
            ranks: vec![0; n],
            required_by: vec![vec![]; n],
            predecessor_is_missing: vec![vec![]; n],
            transitive_missing: vec![false; n],
            predecessor_indices: vec![vec![]; n],
        }
    }

    /// Compute order-independent fields for a single unit.
    /// Also caches resolved predecessor indices (dependsOn) for use by `propagate_from_predecessors`.
    fn resolve_unit_edges(
        &mut self,
        idx: usize,
        units: &[CodeUnit],
        id_to_index: &HashMap<String, usize>,
        successors: &[usize],
    ) {
        let unit = &units[idx];

        let mut predecessor_is_missing = Vec::new();
        let mut resolved_predecessors = Vec::new();
        let mut saw_any = false;

        for (_origin, dep) in dependency_view::depends_on_with_origin(unit) {
            saw_any = true;
            let missing = match dep.id.as_deref() {
                None => true,
                Some(id) => match id_to_index.get(id) {
                    None => true,
                    Some(&dep_idx) => {
                        if !is_self_dep(unit.id.as_deref(), dep.id.as_deref()) {
                            resolved_predecessors.push(dep_idx);
                        }
                        units[dep_idx].is_missing
                    }
                },
            };
            predecessor_is_missing.push(missing);
        }

        if saw_any {
            self.predecessor_is_missing[idx] = predecessor_is_missing;
            self.predecessor_indices[idx] = resolved_predecessors;
        }

        self.required_by[idx] = successors
            .iter()
            .filter_map(|&j| units[j].id.clone())
            .collect();
        self.required_by[idx].sort_unstable();
    }

    fn mark_cycle(&mut self, idx: usize) {
        self.ranks[idx] = -1;
        self.transitive_missing[idx] = true;
    }

    /// Compute topo-order-dependent fields for a single unit.
    /// Assumes predecessors have already been visited, so their ranks and transitive-missing flags are populated.
    /// Uses predecessor indices cached by `resolve_unit_edges` instead of re-traversing edges.
    fn propagate_from_predecessors(&mut self, idx: usize) {
        let mut max_rank: Option<i64> = None;

        for &pred in &self.predecessor_indices[idx] {
            max_rank = Some(max_rank.map_or(self.ranks[pred], |r| r.max(self.ranks[pred])));
            if self.transitive_missing[pred] {
                self.transitive_missing[idx] = true;
            }
        }

        if self.predecessor_is_missing[idx].iter().any(|&m| m) {
            self.transitive_missing[idx] = true;
        }

        self.ranks[idx] = max_rank.map_or(0, |r| r + 1);
    }

    /// Apply all computed fields to a unit. Returns true if anything changed.
    fn apply(&self, idx: usize, unit: &mut CodeUnit) -> bool {
        let mut changed = false;
        changed |= set_rank(unit, self.ranks[idx]);
        changed |= set_predecessor_missing(unit, &self.predecessor_is_missing[idx]);
        changed |= set_required_by(unit, &self.required_by[idx]);
        changed |= set_transitive_missing(unit, self.transitive_missing[idx]);
        changed
    }
}

// ── Field setters ───────────────────────────────────────────────────────

fn set_rank(unit: &mut CodeUnit, rank: i64) -> bool {
    let current = unit.planning.as_ref().and_then(|p| p.topological_rank);
    if current == Some(rank) {
        return false;
    }
    unit.planning
        .get_or_insert_with(Default::default)
        .topological_rank = Some(rank);
    true
}

fn set_predecessor_missing(unit: &mut CodeUnit, expected: &[bool]) -> bool {
    let mut changed = false;
    for (dep, &missing) in dependency_view::depends_on_mut(unit).zip(expected.iter()) {
        if dep.is_missing != Some(missing) {
            dep.is_missing = Some(missing);
            changed = true;
        }
    }
    changed
}

fn set_required_by(unit: &mut CodeUnit, expected: &[String]) -> bool {
    let mut current: Vec<String> = unit
        .dependencies
        .as_ref()
        .map_or_else(Vec::new, |d| d.required_by.clone());
    current.sort_unstable();
    if current == expected {
        return false;
    }
    unit.dependencies
        .get_or_insert_with(Default::default)
        .required_by = expected.to_vec();
    true
}

fn set_transitive_missing(unit: &mut CodeUnit, expected: bool) -> bool {
    let current = unit
        .dependencies
        .as_ref()
        .is_some_and(|d| d.has_transitive_missing_dependencies);
    if current == expected {
        return false;
    }
    unit.dependencies
        .get_or_insert_with(Default::default)
        .has_transitive_missing_dependencies = expected;
    true
}

// ── Tests ───────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::registry::test_helpers::{id_index, unit, unit_missing, unit_with_dependencies};

    fn rank_of(unit: &CodeUnit) -> Option<i64> {
        unit.planning.as_ref().and_then(|p| p.topological_rank)
    }

    fn required_by_of(unit: &CodeUnit) -> Vec<String> {
        unit.dependencies.as_ref().map_or_else(Vec::new, |d| {
            let mut rb = d.required_by.clone();
            rb.sort_unstable();
            rb
        })
    }

    fn transitive_missing_of(unit: &CodeUnit) -> bool {
        unit.dependencies
            .as_ref()
            .is_some_and(|d| d.has_transitive_missing_dependencies)
    }

    fn predecessor_is_missing_of(unit: &CodeUnit) -> Vec<Option<bool>> {
        unit.dependencies.as_ref().map_or_else(Vec::new, |d| {
            d.depends_on.iter().map(|dep| dep.is_missing).collect()
        })
    }

    fn sorted_dirty_ids<'a>(dirty: &[usize], units: &'a [CodeUnit]) -> Vec<&'a str> {
        let mut ids: Vec<&str> = dirty
            .iter()
            .filter_map(|&i| units[i].id.as_deref())
            .collect();
        ids.sort_unstable();
        ids
    }

    // ── 1. Traversal edge cases ─────────────────────────────────────────

    #[test]
    fn predecessors_skips_none_and_unresolved() {
        let units = vec![
            unit_with_dependencies("a", &[Some("b"), None, Some("ghost")]),
            unit("b"),
        ];
        let idx = id_index(&units);

        let resolved: Vec<usize> = predecessors(&units[0], &idx).collect();
        assert_eq!(resolved, vec![1]); // only "b" resolves; None and "ghost" skipped
    }

    // ── 2–13. End-to-end refresh ────────────────────────────────────────

    #[test]
    fn refresh_empty() {
        let mut units: Vec<CodeUnit> = vec![];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        let dirty = g.refresh(false).unwrap();
        assert!(dirty.is_empty());
    }

    #[test]
    fn refresh_isolated_node() {
        let mut units = vec![unit("a")];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        let dirty = g.refresh(false).unwrap();

        assert_eq!(dirty, vec![0]);
        assert_eq!(rank_of(&units[0]), Some(0));
        assert!(units[0].dependencies.is_none());
    }

    #[test]
    fn refresh_linear_chain() {
        // a -> b -> c  (a depends on b, b depends on c)
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("c")]),
            unit("c"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert_eq!(rank_of(&units[0]), Some(2));
        assert_eq!(rank_of(&units[1]), Some(1));
        assert_eq!(rank_of(&units[2]), Some(0));

        assert_eq!(required_by_of(&units[0]), Vec::<String>::new());
        assert_eq!(required_by_of(&units[1]), vec!["a"]);
        assert_eq!(required_by_of(&units[2]), vec!["b"]);

        assert_eq!(predecessor_is_missing_of(&units[0]), vec![Some(false)]);
        assert_eq!(predecessor_is_missing_of(&units[1]), vec![Some(false)]);
        assert!(!transitive_missing_of(&units[0]));
        assert!(!transitive_missing_of(&units[1]));
    }

    #[test]
    fn refresh_diamond() {
        // a -> b -> d, a -> c -> d
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b"), Some("c")]),
            unit_with_dependencies("b", &[Some("d")]),
            unit_with_dependencies("c", &[Some("d")]),
            unit("d"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert_eq!(rank_of(&units[0]), Some(2)); // a: max(b=1, c=1) + 1
        assert_eq!(rank_of(&units[1]), Some(1)); // b: d=0 + 1
        assert_eq!(rank_of(&units[2]), Some(1)); // c: d=0 + 1
        assert_eq!(rank_of(&units[3]), Some(0)); // d: root

        assert_eq!(required_by_of(&units[3]), vec!["b", "c"]);
        assert_eq!(required_by_of(&units[1]), vec!["a"]);
        assert_eq!(required_by_of(&units[2]), vec!["a"]);
    }

    #[test]
    fn refresh_predecessor_is_missing_variants() {
        // a depends on: "ghost" (not in registry), "m" (is_missing=true), "ok" (present)
        let mut units = vec![
            unit_with_dependencies("a", &[Some("ghost"), Some("m"), Some("ok")]),
            unit_missing("m"),
            unit("ok"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert_eq!(
            predecessor_is_missing_of(&units[0]),
            vec![Some(true), Some(true), Some(false)]
        );
        assert!(transitive_missing_of(&units[0]));
    }

    #[test]
    fn refresh_transitive_missing_chain() {
        // a -> b -> "missing" (not in registry)
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("missing")]),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert!(transitive_missing_of(&units[1])); // b: direct missing dep
        assert!(transitive_missing_of(&units[0])); // a: inherited from b
    }

    #[test]
    fn refresh_cycle_strict() {
        let mut units = vec![
            unit_with_dependencies("x", &[Some("y")]),
            unit_with_dependencies("y", &[Some("x")]),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);

        let err = g.refresh(true).unwrap_err();
        assert_eq!(err.error_code_i32(), 1014);
    }

    #[test]
    fn refresh_cycle_best_effort() {
        let mut units = vec![
            unit_with_dependencies("x", &[Some("y")]),
            unit_with_dependencies("y", &[Some("x")]),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert_eq!(rank_of(&units[0]), Some(-1));
        assert_eq!(rank_of(&units[1]), Some(-1));
        assert!(transitive_missing_of(&units[0]));
        assert!(transitive_missing_of(&units[1]));
    }

    #[test]
    fn refresh_cycle_affects_downstream() {
        // a -> b -> a (cycle), c -> a (downstream of cycle), r (disconnected)
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("a")]),
            unit_with_dependencies("c", &[Some("a")]),
            unit("r"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert_eq!(rank_of(&units[0]), Some(-1)); // a: in cycle
        assert_eq!(rank_of(&units[1]), Some(-1)); // b: in cycle
        assert_eq!(rank_of(&units[2]), Some(-1)); // c: depends on cycle, also stuck
        assert_eq!(rank_of(&units[3]), Some(0)); // r: disconnected, unaffected

        assert!(transitive_missing_of(&units[2]));
        assert!(!transitive_missing_of(&units[3]));
    }

    #[test]
    fn refresh_self_loop() {
        let mut units = vec![unit_with_dependencies("a", &[Some("a")])];
        let idx = id_index(&units);

        RegistryGraph::new(&mut units, &idx).refresh(true).unwrap();

        assert_eq!(rank_of(&units[0]), Some(0));
        assert_eq!(required_by_of(&units[0]), Vec::<String>::new());
        assert_eq!(predecessor_is_missing_of(&units[0]), vec![Some(false)]);
        assert!(!transitive_missing_of(&units[0]));
    }

    #[test]
    fn refresh_self_loop_does_not_mask_real_cycle() {
        // `d` is unrelated — it must still deploy even though a/b form a real cycle.
        let mut units = vec![
            unit_with_dependencies("a", &[Some("a"), Some("b")]),
            unit_with_dependencies("b", &[Some("a")]),
            unit("d"),
        ];
        let idx = id_index(&units);

        let err = RegistryGraph::new(&mut units, &idx)
            .refresh(true)
            .unwrap_err();
        assert_eq!(err.error_code_i32(), 1014);

        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();
        assert_eq!(rank_of(&units[idx["a"]]), Some(-1));
        assert_eq!(rank_of(&units[idx["b"]]), Some(-1));
        assert!(transitive_missing_of(&units[idx["a"]]));
        assert!(transitive_missing_of(&units[idx["b"]]));
        assert_eq!(graph_deployable_ids(&units), vec!["d"]);
    }

    // ── Deployment-ordering contract: self-references & cycles ──────────
    //
    // Guards SNOW-3659875: self-references must NOT be treated as deployment
    // cycles. `graph_deployable_ids` mirrors the consumer's rank != -1 filter.

    /// Returns IDs of units deployable from the graph's perspective (rank present and != -1).
    fn graph_deployable_ids(units: &[CodeUnit]) -> Vec<String> {
        let mut ids: Vec<String> = units
            .iter()
            .filter(|u| matches!(rank_of(u), Some(r) if r != -1))
            .filter_map(|u| u.id.clone())
            .collect();
        ids.sort_unstable();
        ids
    }

    #[test]
    fn self_fk_table_and_its_dependents_are_deployable() {
        // orders has a self-FK. Pre-fix it was a self-cycle (rank -1) and dragged dependents down.
        let mut units = vec![
            unit_with_dependencies("orders", &[Some("orders"), Some("customers")]),
            unit_with_dependencies("order_items", &[Some("orders"), Some("products")]),
            unit("customers"),
            unit("products"),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        assert_eq!(
            graph_deployable_ids(&units),
            vec!["customers", "order_items", "orders", "products"],
            "self-FK table and its dependents must all be deployable"
        );
        // Self edge ignored: ranks off `customers` only.
        assert_eq!(rank_of(&units[idx["orders"]]), Some(1));
        assert_eq!(rank_of(&units[idx["order_items"]]), Some(2));
        assert!(!transitive_missing_of(&units[idx["orders"]]));
    }

    #[test]
    fn dbt_incremental_self_reference_part_deploys_with_dependents() {
        // Regression (SNOW-3659875): pre-fix, part-origin self-refs were untreated — orders_inc got rank -1.
        // orders_inc has a part self-ref (`{{ this }}`) plus a real upstream; self-edge must be ignored.
        use crate::registry::test_helpers::etl_unit_with_part_deps;
        let mut units = vec![
            etl_unit_with_part_deps(
                "orders_inc",
                &[("flow", &[Some("orders_inc"), Some("stg_orders")])],
            ),
            unit("stg_orders"),
            etl_unit_with_part_deps("orders_mart", &[("flow", &[Some("orders_inc")])]),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        assert_eq!(
            graph_deployable_ids(&units),
            vec!["orders_inc", "orders_mart", "stg_orders"]
        );
        // Self-edge ignored: orders_inc ranks off stg_orders only.
        assert_eq!(rank_of(&units[idx["stg_orders"]]), Some(0));
        assert_eq!(rank_of(&units[idx["orders_inc"]]), Some(1));
        assert_eq!(rank_of(&units[idx["orders_mart"]]), Some(2));
    }

    #[test]
    fn extract_then_convert_keeps_self_fk_set_deployable() {
        // Full extract refresh then scoped convert refresh; deployable set must be stable.
        // ecommerce DAG with two self-FK tables (employees, categories).
        let build = || {
            vec![
                unit_with_dependencies("employees", &[Some("employees")]),
                unit_with_dependencies("categories", &[Some("categories")]),
                unit("customers"),
                unit("products"),
                unit_with_dependencies("orders", &[Some("customers"), Some("employees")]),
                unit_with_dependencies("order_items", &[Some("orders"), Some("products")]),
                unit_with_dependencies("product_cat", &[Some("products"), Some("categories")]),
                unit_with_dependencies("v_org_chart", &[Some("employees")]),
            ]
        };
        let all = vec![
            "categories",
            "customers",
            "employees",
            "order_items",
            "orders",
            "product_cat",
            "products",
            "v_org_chart",
        ];

        // Phase 1 — full extraction.
        let mut units = build();
        let idx = id_index(&units);
        assert!(units.iter().all(|u| u.planning.is_none()));
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert_eq!(
            graph_deployable_ids(&units),
            all,
            "after full extract refresh"
        );

        // Phase 2 — scoped conversion; deployable set must hold.
        RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[idx["order_items"]], false)
            .unwrap();
        assert_eq!(
            graph_deployable_ids(&units),
            all,
            "after scoped convert refresh"
        );
    }

    #[test]
    fn refresh_creates_structs_when_none() {
        // c starts with planning=None, dependencies=None.
        // After refresh, c should get planning (rank=0) and dependencies (required_by=["b"]).
        let mut units = vec![unit_with_dependencies("b", &[Some("c")]), unit("c")];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        assert!(units[1].planning.is_some());
        assert_eq!(rank_of(&units[1]), Some(0));

        assert!(units[1].dependencies.is_some());
        assert_eq!(required_by_of(&units[1]), vec!["b"]);
    }

    #[test]
    fn refresh_idempotent() {
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("missing")]),
        ];
        let idx = id_index(&units);

        let dirty1 = RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert!(!dirty1.is_empty());

        let dirty2 = RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert!(dirty2.is_empty());
    }

    // ── 14. Scoped refresh ──────────────────────────────────────────────

    #[test]
    fn scoped_refresh() {
        // Two disconnected components: (a -> b) and (c -> d)
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit("b"),
            unit_with_dependencies("c", &[Some("d")]),
            unit("d"),
        ];
        let idx = id_index(&units);

        // Full refresh first to set baseline.
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // Reset component 1 to clear derived state.
        units[0].planning = None;
        units[0].dependencies.as_mut().unwrap().depends_on[0].is_missing = None;
        units[1].planning = None;
        units[1].dependencies = None;

        // Scoped refresh seeded on "a" should only touch component 1.
        let a_idx = idx["a"];
        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[a_idx], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b"]);

        // Component 1 correctly refreshed.
        assert_eq!(rank_of(&units[0]), Some(1));
        assert_eq!(rank_of(&units[1]), Some(0));

        // Component 2 unchanged (still has values from full refresh).
        assert_eq!(rank_of(&units[2]), Some(1));
        assert_eq!(rank_of(&units[3]), Some(0));
    }

    #[test]
    fn scoped_refresh_expands_via_successors() {
        // a -> b -> c (a depends on b, b depends on c)
        // Full refresh first to populate requiredBy edges (they're derived).
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("c")]),
            unit("c"),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // Mark c as missing — this should propagate up to b and a.
        units[2].is_missing = true;

        // Seed on "c" (leaf). expand_scope follows successors upward to reach b and a.
        let c_idx = idx["c"];
        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[c_idx], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b"]);

        assert!(transitive_missing_of(&units[0])); // a: inherited from b
        assert!(transitive_missing_of(&units[1])); // b: direct dep c is now missing
        assert_eq!(predecessor_is_missing_of(&units[1]), vec![Some(true)]);
    }

    // ── 16. Dirty tracking ──────────────────────────────────────────────

    #[test]
    fn dirty_after_mutation() {
        // a -> b -> c
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("c")]),
            unit("c"),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // Mutate: mark c as missing.
        units[2].is_missing = true;

        let dirty = RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // b's predecessor_is_missing changed (c now missing), a's transitive_missing changed.
        // c itself is only dirty if required_by or rank changed — they didn't.
        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b"]);
    }

    // ── 17–23. Scoped refresh edge cases ─────────────────────────────────

    #[test]
    fn scoped_refresh_dep_added() {
        // A and B exist independently. Simulate adding A -> B, then scoped refresh from [A].
        let mut units = vec![unit("a"), unit("b")];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // Mutate: add A -> B dependency.
        units[0] = unit_with_dependencies("a", &[Some("b")]);

        let a_idx = idx["a"];
        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[a_idx], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b"]);

        assert_eq!(rank_of(&units[0]), Some(1)); // a depends on b
        assert_eq!(rank_of(&units[1]), Some(0));
        assert_eq!(required_by_of(&units[1]), vec!["a"]);
    }

    #[test]
    fn scoped_refresh_dep_removed() {
        // A -> B, full refresh. Then remove A's dep on B.
        // Scoped refresh seeded on [A, B] (old dep B explicitly seeded).
        let mut units = vec![unit_with_dependencies("a", &[Some("b")]), unit("b")];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert_eq!(required_by_of(&units[1]), vec!["a"]);

        // Mutate: remove dependency.
        units[0] = unit("a");

        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[idx["a"], idx["b"]], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b"]);

        assert_eq!(rank_of(&units[0]), Some(0)); // a is now a root
        assert_eq!(required_by_of(&units[1]), Vec::<String>::new()); // b no longer required by a
    }

    #[test]
    fn scoped_refresh_dep_swapped() {
        // A -> B, full refresh. Then change A to depend on C instead.
        // Seeds = [A, B]. C is reached via A's new predecessors().
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit("b"),
            unit("c"),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert_eq!(required_by_of(&units[1]), vec!["a"]);

        // Mutate: swap B for C.
        units[0] = unit_with_dependencies("a", &[Some("c")]);

        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[idx["a"], idx["b"]], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b", "c"]);

        assert_eq!(required_by_of(&units[1]), Vec::<String>::new()); // b cleared
        assert_eq!(required_by_of(&units[2]), vec!["a"]); // c now required by a
        assert_eq!(rank_of(&units[0]), Some(1));
    }

    #[test]
    fn scoped_refresh_diamond_reaches_full_component() {
        // Diamond: a -> b -> d, a -> c -> d. Full refresh, then mark d as missing.
        // Seed on [d] -- expand_scope should reach all 4 nodes.
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b"), Some("c")]),
            unit_with_dependencies("b", &[Some("d")]),
            unit_with_dependencies("c", &[Some("d")]),
            unit("d"),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();
        assert!(!transitive_missing_of(&units[0]));

        // Mutate: mark d as missing.
        units[3].is_missing = true;

        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[idx["d"]], false)
            .unwrap();

        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["a", "b", "c"]);

        assert!(transitive_missing_of(&units[0])); // a: transitive
        assert!(transitive_missing_of(&units[1])); // b: direct dep d missing
        assert!(transitive_missing_of(&units[2])); // c: direct dep d missing
    }

    #[test]
    fn scoped_refresh_cycle_in_scope() {
        // A -> B -> A (cycle). Full refresh first, then scoped refresh from [A].
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("a")]),
        ];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        // Reset ranks to force recomputation.
        units[0].planning = None;
        units[1].planning = None;

        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[idx["a"]], false)
            .unwrap();

        assert_eq!(dirty.len(), 2);
        assert_eq!(rank_of(&units[0]), Some(-1));
        assert_eq!(rank_of(&units[1]), Some(-1));
        assert!(transitive_missing_of(&units[0]));
        assert!(transitive_missing_of(&units[1]));
    }

    #[test]
    fn scoped_refresh_empty_seeds() {
        let mut units = vec![unit("a"), unit("b")];
        let idx = id_index(&units);
        RegistryGraph::new(&mut units, &idx).refresh(false).unwrap();

        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[], false)
            .unwrap();
        assert!(dirty.is_empty());
    }

    #[test]
    fn scoped_refresh_first_call_no_successors() {
        // A -> B -> C, no prior refresh. requiredBy is empty, so no successors.
        // Seed on [C] -- expand_scope can't traverse upward, scope = {C} only.
        let mut units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("c")]),
            unit("c"),
        ];
        let idx = id_index(&units);

        let c_idx = idx["c"];
        let dirty = RegistryGraph::new(&mut units, &idx)
            .refresh_scoped(&[c_idx], false)
            .unwrap();

        // Only c was in scope, so only c gets derived fields.
        assert_eq!(sorted_dirty_ids(&dirty, &units), vec!["c"]);
        assert_eq!(rank_of(&units[2]), Some(0));

        // a and b remain unrefreshed.
        assert!(units[0].planning.is_none());
        assert!(units[1].planning.is_none());
    }

    // ── Part-level dependency coverage ───────────────────────────────────

    #[test]
    fn refresh_with_part_level_dependencies() {
        use crate::registry::test_helpers::etl_unit_with_part_deps;

        // ETL unit "etl" has two parts:
        //   part-a → depends on "b"
        //   part-c → depends on "d"
        // "b" and "d" are independent leaves.
        let mut units = vec![
            etl_unit_with_part_deps("etl", &[("part-a", &[Some("b")]), ("part-c", &[Some("d")])]),
            unit("b"),
            unit("d"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        // Both leaves should be rank 0; ETL unit should be rank 1 (max of b,d = 0 + 1).
        assert_eq!(rank_of(&units[0]), Some(1));
        assert_eq!(rank_of(&units[1]), Some(0));
        assert_eq!(rank_of(&units[2]), Some(0));

        // "etl" is a requiredBy of "b" and "d".
        assert_eq!(required_by_of(&units[1]), vec!["etl"]);
        assert_eq!(required_by_of(&units[2]), vec!["etl"]);

        // Neither leaf is missing, so no transitive-missing propagation.
        assert!(!transitive_missing_of(&units[0]));
    }

    #[test]
    fn set_predecessor_missing_zips_root_and_parts() {
        use crate::registry::test_helpers::etl_unit_with_part_deps;

        // ETL unit with two parts. part-a has two deps (one missing), part-b has one dep (present).
        let mut units = vec![
            etl_unit_with_part_deps(
                "etl",
                &[
                    ("part-a", &[Some("ghost"), Some("present")]),
                    ("part-b", &[Some("present")]),
                ],
            ),
            unit("present"),
        ];
        let idx = id_index(&units);
        let mut g = RegistryGraph::new(&mut units, &idx);
        g.refresh(false).unwrap();

        // Verify each dep got the correct is_missing flag — order: part-a[0], part-a[1], part-b[0].
        let part_a_flags: Vec<Option<bool>> = units[0].parts.as_ref().unwrap()[0]
            .dependencies
            .as_ref()
            .unwrap()
            .depends_on
            .iter()
            .map(|d| d.is_missing)
            .collect();
        let part_b_flags: Vec<Option<bool>> = units[0].parts.as_ref().unwrap()[1]
            .dependencies
            .as_ref()
            .unwrap()
            .depends_on
            .iter()
            .map(|d| d.is_missing)
            .collect();

        assert_eq!(part_a_flags, vec![Some(true), Some(false)]);
        assert_eq!(part_b_flags, vec![Some(false)]);

        // Transitive-missing propagates up because of the ghost dep on part-a.
        assert!(transitive_missing_of(&units[0]));
    }
}
