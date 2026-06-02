//! Hypergraph-partition 기반 contraction path (cotengra 식 고급 optimizer).
//!
//! greedy / random-greedy 는 local 휴리스틱이라 high-treewidth (2D / random)
//! 네트워크에서 contraction width 가 폭발한다.  cotengra 가 KaHyPar 로 하는
//! **재귀적 balanced min-cut 이분할** 을 자체 구현 (Fiduccia-Mattheyses 정제) 해
//! contraction tree 를 만든다 — 각 이분할의 cut 이 그 단계 intermediate 텐서의
//! rank(=width) 를 결정하므로, cut 을 최소화하면 width 가 작아진다.
//!
//! tree → SSA path: post-order 순회 (왼쪽 서브트리 수축 → 오른쪽 → 둘을 수축).

use std::collections::HashMap;

use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::{Rng, SeedableRng};

use crate::optimal::optimal_emit;
use crate::path::SsaPath;

/// 텐서 간 interaction 그래프의 가중 인접: `weight[(i,j)]` = 공유 인덱스의
/// `Σ log2(dim)` (= 그 bond 를 가로지를 때의 rank 기여).
struct InteractionGraph {
    /// node → [(neighbor, weight)].
    adj: Vec<Vec<(usize, f64)>>,
    n: usize,
}

impl InteractionGraph {
    fn build(tensor_indices: &[Vec<usize>], dims: &HashMap<usize, usize>) -> Self {
        let n = tensor_indices.len();
        // 인덱스 → 그 인덱스를 포함하는 텐서들.
        let mut idx_to_tensors: HashMap<usize, Vec<usize>> = HashMap::new();
        for (t, inds) in tensor_indices.iter().enumerate() {
            for &i in inds {
                idx_to_tensors.entry(i).or_default().push(t);
            }
        }
        let mut weight: HashMap<(usize, usize), f64> = HashMap::new();
        for (idx, tensors) in &idx_to_tensors {
            let w = (*dims.get(idx).unwrap_or(&2) as f64).log2();
            // bond 가 정확히 2 텐서를 잇는 경우 (대부분) 만 edge.  3+ 는
            // hyperedge — 모든 쌍에 분산 (근사).
            for a in 0..tensors.len() {
                for b in (a + 1)..tensors.len() {
                    let (i, j) = (tensors[a], tensors[b]);
                    let key = if i < j { (i, j) } else { (j, i) };
                    *weight.entry(key).or_insert(0.0) += w;
                }
            }
        }
        let mut adj = vec![Vec::new(); n];
        for (&(i, j), &w) in &weight {
            adj[i].push((j, w));
            adj[j].push((i, w));
        }
        // 결정론적 순서 (HashMap 반복 순서는 비결정적이므로 정렬) — distributed
        // 슬라이싱에서 worker 들이 동일 path 를 독립 재구성하도록 보장.
        for a in adj.iter_mut() {
            a.sort_by_key(|x| x.0);
        }
        InteractionGraph { adj, n }
    }
}

/// 부분집합 `nodes` 를 balanced min-cut 으로 두 그룹으로 이분할.
/// **Multilevel** (heavy-edge coarsening → coarse 분할 → uncoarsen + 가중 FM
/// 정제) — KaHyPar/Metis 식.  단일레벨 FM 의 local minima 를 회피.
fn bisect(nodes: &[usize], graph: &InteractionGraph, rng: &mut StdRng) -> (Vec<usize>, Vec<usize>) {
    let m = nodes.len();
    if m <= 1 {
        return (nodes.to_vec(), vec![]);
    }
    // 로컬 인덱스 0..m ↔ 전역 node id, 로컬 가중 인접.
    let local: HashMap<usize, usize> = nodes.iter().enumerate().map(|(l, &g)| (g, l)).collect();
    let mut ladj: Vec<Vec<(usize, f64)>> = vec![Vec::new(); m];
    for (l, &g) in nodes.iter().enumerate() {
        for &(nb, w) in &graph.adj[g] {
            if let Some(&ln) = local.get(&nb) {
                ladj[l].push((ln, w));
            }
        }
    }
    let wt = vec![1.0f64; m];
    let side = bisect_local(&ladj, &wt, rng);

    let mut a = Vec::new();
    let mut b = Vec::new();
    for (l, &g) in nodes.iter().enumerate() {
        if side[l] == 0 {
            a.push(g);
        } else {
            b.push(g);
        }
    }
    // 한쪽이 비면 강제 분할 (재귀 종료 보장).
    if a.is_empty() || b.is_empty() {
        let mid = m / 2;
        a = nodes[..mid].to_vec();
        b = nodes[mid..].to_vec();
    }
    (a, b)
}

/// coarsening base: 이 크기 이하면 직접 (BFS-seeded + FM) 이분할.
const COARSEN_BASE: usize = 30;

/// 가중 그래프의 multilevel balanced 이분할 → side (0=A, 1=B).
fn bisect_local(adj: &[Vec<(usize, f64)>], wt: &[f64], rng: &mut StdRng) -> Vec<u8> {
    let m = adj.len();
    if m <= 1 {
        return vec![0u8; m];
    }
    if m <= COARSEN_BASE {
        let mut side = bfs_initial_split(adj, wt, rng);
        fm_refine(adj, wt, &mut side, rng);
        return side;
    }
    // 1. heavy-edge matching → coarsen.
    let matching = heavy_edge_matching(adj, rng);
    let (cadj, cwt, coarse_of) = coarsen(adj, wt, &matching);
    if cadj.len() == m {
        // 더 coarsen 안 됨 (매칭 0) → base 처리.
        let mut side = bfs_initial_split(adj, wt, rng);
        fm_refine(adj, wt, &mut side, rng);
        return side;
    }
    // 2. coarse 그래프 재귀 이분할.
    let cside = bisect_local(&cadj, &cwt, rng);
    // 3. project 후 fine 레벨 FM 정제.
    let mut side: Vec<u8> = (0..m).map(|f| cside[coarse_of[f]]).collect();
    fm_refine(adj, wt, &mut side, rng);
    side
}

/// BFS 순서로 누적 weight 가 절반이 될 때까지 A 배정 (locality 초기 분할).
fn bfs_initial_split(adj: &[Vec<(usize, f64)>], wt: &[f64], rng: &mut StdRng) -> Vec<u8> {
    let m = adj.len();
    let start = rng.gen_range(0..m);
    let mut order = Vec::with_capacity(m);
    let mut visited = vec![false; m];
    let mut queue = std::collections::VecDeque::new();
    queue.push_back(start);
    visited[start] = true;
    while let Some(u) = queue.pop_front() {
        order.push(u);
        let mut nbrs: Vec<usize> = adj[u].iter().map(|&(v, _)| v).collect();
        nbrs.shuffle(rng);
        for v in nbrs {
            if !visited[v] {
                visited[v] = true;
                queue.push_back(v);
            }
        }
    }
    for (l, &seen) in visited.iter().enumerate() {
        if !seen {
            order.push(l);
        }
    }
    let total: f64 = wt.iter().sum();
    let mut side = vec![1u8; m];
    let mut acc = 0.0;
    for &l in &order {
        if acc >= total / 2.0 {
            break;
        }
        side[l] = 0;
        acc += wt[l];
    }
    side
}

/// heavy-edge matching: 임의 순서로 미매칭 노드를 가장 무거운 미매칭 이웃과 매칭.
fn heavy_edge_matching(adj: &[Vec<(usize, f64)>], rng: &mut StdRng) -> Vec<Option<usize>> {
    let m = adj.len();
    let mut matched = vec![false; m];
    let mut partner = vec![None; m];
    let mut order: Vec<usize> = (0..m).collect();
    order.shuffle(rng);
    for &u in &order {
        if matched[u] {
            continue;
        }
        let mut best: Option<usize> = None;
        let mut best_w = f64::NEG_INFINITY;
        for &(v, w) in &adj[u] {
            if !matched[v] && v != u && w > best_w {
                best_w = w;
                best = Some(v);
            }
        }
        if let Some(v) = best {
            matched[u] = true;
            matched[v] = true;
            partner[u] = Some(v);
            partner[v] = Some(u);
        }
    }
    partner
}

/// matching 으로 그래프를 coarsen → (coarse adj, coarse wt, fine→coarse 맵).
#[allow(clippy::type_complexity)]
fn coarsen(
    adj: &[Vec<(usize, f64)>],
    wt: &[f64],
    partner: &[Option<usize>],
) -> (Vec<Vec<(usize, f64)>>, Vec<f64>, Vec<usize>) {
    let m = adj.len();
    let mut coarse_of = vec![usize::MAX; m];
    let mut ncoarse = 0;
    for u in 0..m {
        if coarse_of[u] != usize::MAX {
            continue;
        }
        let c = ncoarse;
        ncoarse += 1;
        coarse_of[u] = c;
        if let Some(v) = partner[u] {
            coarse_of[v] = c;
        }
    }
    let mut cwt = vec![0.0f64; ncoarse];
    for u in 0..m {
        cwt[coarse_of[u]] += wt[u];
    }
    let mut cmap: Vec<HashMap<usize, f64>> = vec![HashMap::new(); ncoarse];
    for (u, nbrs) in adj.iter().enumerate() {
        let cu = coarse_of[u];
        for &(v, w) in nbrs {
            let cv = coarse_of[v];
            if cu != cv {
                *cmap[cu].entry(cv).or_insert(0.0) += w;
            }
        }
    }
    let cadj: Vec<Vec<(usize, f64)>> = cmap
        .into_iter()
        .map(|hm| {
            let mut v: Vec<(usize, f64)> = hm.into_iter().collect();
            v.sort_by_key(|x| x.0); // HashMap 비결정 순서 → 정렬 (결정론).
            v
        })
        .collect();
    (cadj, cwt, coarse_of)
}

/// 가중 balance 제약 하의 Fiduccia-Mattheyses 정제 (in-place).
fn fm_refine(adj: &[Vec<(usize, f64)>], wt: &[f64], side: &mut [u8], _rng: &mut StdRng) {
    let m = adj.len();
    let total: f64 = wt.iter().sum();
    let lo = total * 0.4;
    let hi = total * 0.6;
    for _pass in 0..4 {
        let mut locked = vec![false; m];
        let mut best_side = side.to_vec();
        let mut best_cut = cut_weight(side, adj);
        let mut cur_cut = best_cut;
        let mut wa: f64 = (0..m).filter(|&l| side[l] == 0).map(|l| wt[l]).sum();
        let mut improved_any = false;
        for _ in 0..m {
            let mut best_gain = f64::NEG_INFINITY;
            let mut best_node = None;
            for l in 0..m {
                if locked[l] {
                    continue;
                }
                let to_a = side[l] == 1;
                let new_wa = if to_a { wa + wt[l] } else { wa - wt[l] };
                if new_wa < lo || new_wa > hi {
                    continue;
                }
                let mut internal = 0.0;
                let mut external = 0.0;
                for &(v, w) in &adj[l] {
                    if side[v] == side[l] {
                        internal += w;
                    } else {
                        external += w;
                    }
                }
                let gain = external - internal;
                if gain > best_gain {
                    best_gain = gain;
                    best_node = Some(l);
                }
            }
            match best_node {
                Some(l) => {
                    wa += if side[l] == 1 { wt[l] } else { -wt[l] };
                    side[l] ^= 1;
                    locked[l] = true;
                    cur_cut -= best_gain;
                    if cur_cut < best_cut - 1e-12 {
                        best_cut = cur_cut;
                        best_side = side.to_vec();
                        improved_any = true;
                    }
                }
                None => break,
            }
        }
        side.copy_from_slice(&best_side);
        if !improved_any {
            break;
        }
    }
}

fn cut_weight(side: &[u8], ladj: &[Vec<(usize, f64)>]) -> f64 {
    let mut cut = 0.0;
    for (l, nbrs) in ladj.iter().enumerate() {
        for &(v, w) in nbrs {
            if l < v && side[l] != side[v] {
                cut += w;
            }
        }
    }
    cut
}

/// 작은 서브트리 (≤ 이 크기) 는 partition 대신 optimal DP 로 마무리 — subtree
/// reconfiguration (cotengra 의 핵심 성능 요인).  `O(3^k)` 이라 12 가 한계.
const OPTIMAL_LEAF_THRESHOLD: usize = 12;

/// 재귀적 분할로 contraction tree → SSA path.  작은 서브트리는 optimal DP.
#[allow(clippy::too_many_arguments)]
fn build_tree(
    nodes: &[usize],
    graph: &InteractionGraph,
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    next_id: &mut usize,
    path: &mut SsaPath,
    rng: &mut StdRng,
) -> usize {
    if nodes.len() == 1 {
        return nodes[0];
    }
    // 충분히 작으면 provably-optimal 로 마무리 (subtree reconfiguration).
    if nodes.len() <= OPTIMAL_LEAF_THRESHOLD {
        let local: Vec<Vec<usize>> = nodes.iter().map(|&g| tensor_indices[g].clone()).collect();
        return optimal_emit(&local, dims, nodes, next_id, path);
    }
    let (a, b) = bisect(nodes, graph, rng);
    let id_a = build_tree(&a, graph, tensor_indices, dims, next_id, path, rng);
    let id_b = build_tree(&b, graph, tensor_indices, dims, next_id, path, rng);
    path.push((id_a, id_b));
    let id = *next_id;
    *next_id += 1;
    id
}

/// Hypergraph-partition contraction path (단일 trial).
pub fn partition_path_seeded(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    seed: u64,
) -> SsaPath {
    let graph = InteractionGraph::build(tensor_indices, dims);
    let mut rng = StdRng::seed_from_u64(seed);
    let all: Vec<usize> = (0..graph.n).collect();
    let mut path = Vec::new();
    let mut next_id = graph.n;
    if graph.n >= 2 {
        build_tree(
            &all,
            &graph,
            tensor_indices,
            dims,
            &mut next_id,
            &mut path,
            &mut rng,
        );
    }
    path
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::path::estimate_cost;

    fn dims_all2(ti: &[Vec<usize>]) -> HashMap<usize, usize> {
        let mut d = HashMap::new();
        for t in ti {
            for &i in t {
                d.insert(i, 2);
            }
        }
        d
    }

    #[test]
    fn partition_chain_valid_path() {
        // 사슬 5 텐서.
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3], vec![3, 4], vec![4, 5]];
        let dims = dims_all2(&ti);
        let path = partition_path_seeded(&ti, &dims, 1);
        assert_eq!(path.len(), 4); // 5 텐서 → 4 contraction.
        let cost = estimate_cost(&ti, &dims, &path);
        assert!(cost.log2_width.is_finite());
    }
}
