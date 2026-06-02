//! Subtree reconfiguration — 임의 contraction tree (SSA path) 를 받아 국소
//! 서브트리를 optimal Held-Karp DP 로 재최적화한다.
//!
//! cotengra 의 `subtree_reconfigure` 에 해당하는, **모든 optimizer 결과를 한 단계
//! 더 개선** 하는 정제 패스다.  greedy / random-greedy / partition / SA 가 만든
//! 트리는 국소적으로는 최적이 아닐 수 있다 — 트리의 각 내부 노드에서 그 아래
//! 서브트리를 최대 `max_units` 개의 atomic unit 으로 펼친 뒤, 그 unit 들 사이의
//! 수축 순서만 optimal DP (`O(3^u)`) 로 다시 풀어 더 싼 경우에만 채택한다.
//!
//! - **항상 비용 비증가**: 재구성 path 가 원본보다 (peak-width 우선, flops 보조)
//!   나쁘면 원본을 유지한다.
//! - **결과 보존**: unit 분할은 트리 구조를 따르므로 최종 수축 결과 텐서는 동일.
//!   (회로 amplitude/statevector 망처럼 bond 가 degree-2 인 경우 — optimal DP 의
//!   가정과 동일.)

use std::collections::HashMap;

use crate::optimal::optimal_emit;
use crate::path::{estimate_cost, sym_contract, SsaPath};

/// 입력 `path` 의 contraction tree 를 국소 재최적화한 (같거나 더 싼) SSA path.
///
/// `max_units` 는 각 노드에서 한 번에 재최적화하는 unit 수 상한 (optimal DP 가
/// `O(3^u)` 이므로 `≲ 12`).  `sweeps` 번 반복하며, 개선이 멈추면 조기 종료한다.
pub fn subtree_reconfigure(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    path: &SsaPath,
    max_units: usize,
    sweeps: usize,
) -> SsaPath {
    let k = tensor_indices.len();
    if k <= 2 || path.len() + 1 != k {
        // 단일/쌍 텐서거나 path 가 완전 수축 (k-1 step) 이 아니면 그대로.
        return path.clone();
    }
    // 안전장치: pairwise sym_contract (및 optimal DP) 는 bond 가 ≤2 텐서를 잇는
    // 경우만 결과를 보존한다.  degree-3+ 인덱스 (hyperedge) 가 있으면 재배열이
    // 수축 결과를 바꿀 수 있으므로 재구성하지 않는다 (회로 amplitude/statevector
    // 망은 항상 degree-2 라 영향 없음).
    if has_hyperedge(tensor_indices) {
        return path.clone();
    }
    let max_units = max_units.clamp(2, 12);
    let mut best = path.clone();
    let mut best_cost = estimate_cost(tensor_indices, dims, &best);
    for _ in 0..sweeps.max(1) {
        let Some(cand) = reconfigure_once(tensor_indices, dims, &best, max_units) else {
            break;
        };
        let cand_cost = estimate_cost(tensor_indices, dims, &cand);
        // (peak-width 우선, flops 보조) 사전식으로 개선될 때만 채택.
        let improved = cand_cost.log2_width < best_cost.log2_width - 1e-9
            || (cand_cost.log2_width < best_cost.log2_width + 1e-9
                && cand_cost.log10_flops < best_cost.log10_flops - 1e-9);
        if improved {
            best = cand;
            best_cost = cand_cost;
        } else {
            break;
        }
    }
    best
}

/// 어떤 인덱스가 3개 이상의 텐서에 나타나면 (hyperedge) `true`.
fn has_hyperedge(tensor_indices: &[Vec<usize>]) -> bool {
    let mut deg: HashMap<usize, usize> = HashMap::new();
    for inds in tensor_indices {
        for &i in inds {
            *deg.entry(i).or_insert(0) += 1;
        }
    }
    deg.values().any(|&d| d > 2)
}

/// 트리: leaf (id < k) 또는 internal (children).  노드 id 는 SSA id 와 동일.
struct Tree {
    k: usize,
    children: Vec<Option<(usize, usize)>>,
    indices: Vec<Vec<usize>>,
    /// 서브트리 내 leaf 개수 (unit 확장 우선순위용).
    leaf_count: Vec<usize>,
    root: usize,
}

impl Tree {
    fn from_path(
        tensor_indices: &[Vec<usize>],
        dims: &HashMap<usize, usize>,
        path: &SsaPath,
    ) -> Self {
        let k = tensor_indices.len();
        let mut children: Vec<Option<(usize, usize)>> = vec![None; k];
        let mut indices: Vec<Vec<usize>> = tensor_indices.to_vec();
        let mut leaf_count: Vec<usize> = vec![1; k];
        for &(i, j) in path {
            let (res, _, _) = sym_contract(&indices[i], &indices[j], dims);
            children.push(Some((i, j)));
            indices.push(res);
            leaf_count.push(leaf_count[i] + leaf_count[j]);
        }
        let root = children.len() - 1;
        Tree {
            k,
            children,
            indices,
            leaf_count,
            root,
        }
    }
}

/// 한 번의 재구성 sweep: 트리를 post-order 로 재방출하되, 각 내부 노드에서
/// 서브트리를 최대 `max_units` unit 으로 펼쳐 optimal DP 로 재수축한다.
fn reconfigure_once(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    path: &SsaPath,
    max_units: usize,
) -> Option<SsaPath> {
    let tree = Tree::from_path(tensor_indices, dims, path);
    let mut new_path: SsaPath = Vec::with_capacity(path.len());
    let mut next_id = tree.k;
    rebuild(
        &tree,
        tree.root,
        dims,
        max_units,
        &mut next_id,
        &mut new_path,
    );
    // 길이 sanity: 완전 수축이면 k-1 개.
    if new_path.len() + 1 == tree.k {
        Some(new_path)
    } else {
        None
    }
}

/// 노드 `v` 의 서브트리를 재방출하고 그 global SSA id 를 반환 (post-order).
fn rebuild(
    tree: &Tree,
    v: usize,
    dims: &HashMap<usize, usize>,
    max_units: usize,
    next_id: &mut usize,
    path: &mut SsaPath,
) -> usize {
    if tree.children[v].is_none() {
        return v; // leaf — 원본 id 유지.
    }
    // v 아래를 최대 max_units 개 unit 으로 펼친다 (leaf 가 많은 unit 우선 분할).
    let units = expand_units(tree, v, max_units);
    // 각 unit 의 서브트리를 먼저 (재귀적으로) 방출.
    let unit_ids: Vec<usize> = units
        .iter()
        .map(|&u| rebuild(tree, u, dims, max_units, next_id, path))
        .collect();
    if unit_ids.len() == 1 {
        return unit_ids[0];
    }
    // unit 들 사이의 수축 순서만 optimal DP 로 다시 푼다.
    let unit_indices: Vec<Vec<usize>> = units.iter().map(|&u| tree.indices[u].clone()).collect();
    optimal_emit(&unit_indices, dims, &unit_ids, next_id, path)
}

/// `v` 의 서브트리를 atomic unit 집합으로 펼친다.  `v` 의 두 자식에서 시작해,
/// `max_units` 미만인 동안 leaf 수가 가장 많은 (내부) unit 을 자식으로 분해한다.
fn expand_units(tree: &Tree, v: usize, max_units: usize) -> Vec<usize> {
    let (l, r) = tree.children[v].unwrap();
    let mut units = vec![l, r];
    loop {
        if units.len() >= max_units {
            break;
        }
        // 분해 가능한 (내부) unit 중 leaf 수 최대 선택.
        let mut pick: Option<usize> = None;
        let mut best_lc = 1;
        for (pos, &u) in units.iter().enumerate() {
            if tree.children[u].is_some() && tree.leaf_count[u] > best_lc {
                best_lc = tree.leaf_count[u];
                pick = Some(pos);
            }
        }
        let Some(pos) = pick else { break };
        let u = units[pos];
        let (a, b) = tree.children[u].unwrap();
        units.swap_remove(pos);
        units.push(a);
        units.push(b);
    }
    units
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::path::{greedy_path, random_greedy_path};

    fn dims2(ti: &[Vec<usize>]) -> HashMap<usize, usize> {
        let mut d = HashMap::new();
        for t in ti {
            for &i in t {
                d.insert(i, 2);
            }
        }
        d
    }

    /// `rows × cols` 닫힌 2D 격자 — 모든 bond 가 정확히 2 텐서를 잇는 (degree-2)
    /// high-treewidth 망.  최종 수축 결과는 스칼라.  bond id 는 unique.
    fn grid_network(rows: usize, cols: usize) -> Vec<Vec<usize>> {
        let mut next = 0usize;
        let mut hbond = vec![vec![0usize; cols]; rows]; // (r,c)-(r,c+1)
        let mut vbond = vec![vec![0usize; cols]; rows]; // (r,c)-(r+1,c)
        for r in 0..rows {
            for c in 0..cols {
                if c + 1 < cols {
                    hbond[r][c] = next;
                    next += 1;
                }
                if r + 1 < rows {
                    vbond[r][c] = next;
                    next += 1;
                }
            }
        }
        let mut ti = Vec::new();
        for r in 0..rows {
            for c in 0..cols {
                let mut inds = Vec::new();
                if c + 1 < cols {
                    inds.push(hbond[r][c]);
                }
                if c >= 1 {
                    inds.push(hbond[r][c - 1]);
                }
                if r + 1 < rows {
                    inds.push(vbond[r][c]);
                }
                if r >= 1 {
                    inds.push(vbond[r - 1][c]);
                }
                ti.push(inds);
            }
        }
        ti
    }

    fn final_indices(
        ti: &[Vec<usize>],
        dims: &HashMap<usize, usize>,
        path: &SsaPath,
    ) -> Vec<usize> {
        let mut idx: Vec<Option<Vec<usize>>> = ti.iter().map(|t| Some(t.clone())).collect();
        for &(i, j) in path {
            let a = idx[i].take().unwrap();
            let b = idx[j].take().unwrap();
            let (res, _, _) = sym_contract(&a, &b, dims);
            idx.push(Some(res));
        }
        let mut out = idx.into_iter().flatten().next_back().unwrap();
        out.sort_unstable();
        out
    }

    #[test]
    fn reconfigure_preserves_result_and_not_worse() {
        // 4×4 닫힌 격자 (degree-2, high-treewidth) — greedy 재구성 width 비증가.
        let ti = grid_network(4, 4);
        let dims = dims2(&ti);
        let g = greedy_path(&ti, &dims);
        let gc = estimate_cost(&ti, &dims, &g);
        let r = subtree_reconfigure(&ti, &dims, &g, 10, 6);
        let rc = estimate_cost(&ti, &dims, &r);
        assert_eq!(
            final_indices(&ti, &dims, &g),
            final_indices(&ti, &dims, &r),
            "재구성이 최종 결과 인덱스를 바꿈"
        );
        assert_eq!(r.len() + 1, ti.len());
        assert!(
            rc.log2_width <= gc.log2_width + 1e-9,
            "width 증가: {} -> {}",
            gc.log2_width,
            rc.log2_width
        );
    }

    #[test]
    fn reconfigure_numerically_equivalent() {
        // 실제 랜덤 텐서를 greedy / 재구성 path 로 각각 수축해 결과가 동일한지 —
        // 재구성이 수축 결과를 보존한다는 결정적 검증 (degree-2 격자, 스칼라).
        use crate::path::contract_ssa;
        use crate::tensor::Tensor;
        use num_complex::Complex64;
        use rand::rngs::StdRng;
        use rand::{Rng, SeedableRng};

        let ti = grid_network(3, 4);
        let dims = dims2(&ti);
        let mut rng = StdRng::seed_from_u64(99);
        let tensors: Vec<Tensor> = ti
            .iter()
            .map(|inds| {
                let d: Vec<usize> = inds.iter().map(|_| 2).collect();
                let n: usize = d.iter().product::<usize>().max(1);
                let data: Vec<Complex64> = (0..n)
                    .map(|_| Complex64::new(rng.gen::<f64>() - 0.5, rng.gen::<f64>() - 0.5))
                    .collect();
                Tensor::new(inds.clone(), d, data)
            })
            .collect();

        let g = greedy_path(&ti, &dims);
        let r = subtree_reconfigure(&ti, &dims, &g, 10, 6);
        // 격자는 degree-2 라 재구성이 실제로 일어나야 함 (path 가 바뀜).
        assert_ne!(g, r, "degree-2 격자에서 재구성이 적용되지 않음");

        let res_g = contract_ssa(&tensors, &g);
        let res_r = contract_ssa(&tensors, &r);
        // 스칼라 결과 (인덱스 없음).
        assert!(res_g.indices.is_empty() && res_r.indices.is_empty());
        let diff = (res_g.data[0] - res_r.data[0]).norm();
        assert!(diff < 1e-9, "수축 결과 불일치: |Δ|={diff}");
    }

    #[test]
    fn reconfigure_skips_hyperedge() {
        // degree-3 인덱스 (hyperedge) 가 있으면 재구성하지 않고 원본 반환.
        let ti = vec![vec![0, 1], vec![1, 2], vec![1, 3], vec![2, 3]]; // 인덱스 1 = degree 3
        let dims = dims2(&ti);
        let g = greedy_path(&ti, &dims);
        let r = subtree_reconfigure(&ti, &dims, &g, 8, 4);
        assert_eq!(g, r, "hyperedge 망은 재구성을 건너뛰어야 함");
    }

    /// 차선(sequential) path 를 재구성하면 (1,2,3…를 순서대로 합치는 나쁜
    /// contraction tree) width 가 크게 줄어드는지 — 재구성의 핵심 능력 검증.
    #[test]
    fn reconfigure_fixes_bad_path() {
        // 닫힌 격자.  나쁜 path: 텐서를 id 순서로 좌→우 누적 (left-deep).
        let ti = grid_network(4, 4);
        let dims = dims2(&ti);
        let bad: SsaPath = {
            let k = ti.len();
            let mut p = Vec::new();
            let mut acc = 0;
            for j in 1..k {
                p.push((acc, j));
                acc = k + (j - 1); // 새 id
            }
            p
        };
        let bc = estimate_cost(&ti, &dims, &bad);
        let r = subtree_reconfigure(&ti, &dims, &bad, 12, 10);
        let rc = estimate_cost(&ti, &dims, &r);
        // 결과 보존 + flops 감소 (격자 width 는 treewidth 로 구조적 하한이라
        // 어떤 순서든 같지만, 재구성은 총 flops 를 줄인다).
        assert_eq!(
            final_indices(&ti, &dims, &bad),
            final_indices(&ti, &dims, &r)
        );
        assert!(
            rc.log2_width <= bc.log2_width + 1e-9,
            "width 증가: {} -> {}",
            bc.log2_width,
            rc.log2_width
        );
        assert!(
            rc.log10_flops < bc.log10_flops - 0.1,
            "재구성이 차선 path 의 flops 를 못 줄임: {} -> {}",
            bc.log10_flops,
            rc.log10_flops
        );
    }

    /// `cargo test -p qsim-tensornet reconfigure_improves -- --ignored --nocapture`
    #[test]
    #[ignore]
    fn reconfigure_improves_grid_width() {
        for (rows, cols) in [(4, 4), (5, 5), (6, 6)] {
            let ti = grid_network(rows, cols);
            let dims = dims2(&ti);
            // 나쁜 left-deep path 기준 개선 폭을 본다.
            let k = ti.len();
            let mut bad = Vec::new();
            let mut acc = 0;
            for j in 1..k {
                bad.push((acc, j));
                acc = k + (j - 1);
            }
            let bc = estimate_cost(&ti, &dims, &bad);
            let r = subtree_reconfigure(&ti, &dims, &bad, 12, 12);
            let rc = estimate_cost(&ti, &dims, &r);
            let g = estimate_cost(&ti, &dims, &greedy_path(&ti, &dims));
            eprintln!(
                "{rows}×{cols}: bad log2W={:.1}/f{:.1} → reconfig log2W={:.1}/f{:.1} (greedy log2W={:.1})",
                bc.log2_width, bc.log10_flops, rc.log2_width, rc.log10_flops, g.log2_width
            );
        }
    }

    #[test]
    fn reconfigure_idempotent_on_optimal() {
        // 사슬+닫힘 — random-greedy 후 재구성, 한 번 더 재구성해도 비용 동일.
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3], vec![3, 4], vec![0, 4]];
        let dims = dims2(&ti);
        let p = random_greedy_path(&ti, &dims, 16, 1);
        let r1 = subtree_reconfigure(&ti, &dims, &p, 8, 4);
        let r2 = subtree_reconfigure(&ti, &dims, &r1, 8, 4);
        let c1 = estimate_cost(&ti, &dims, &r1);
        let c2 = estimate_cost(&ti, &dims, &r2);
        assert!((c1.log2_width - c2.log2_width).abs() < 1e-9);
        assert!((c1.log10_flops - c2.log10_flops).abs() < 1e-6);
    }
}
