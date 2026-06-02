//! 작은 네트워크의 **provably-optimal** contraction order (Held-Karp DP).
//!
//! cotengra 의 `optimal` 드라이버에 해당.  부분집합 `S ⊆ {0..k}` 마다 그 텐서들을
//! 하나로 수축하는 최적 (peak-width 우선, flops 보조) 비용을 DP 로 구한다 —
//! `cost(S) = min_{S=S1⊔S2} f(cost(S1), cost(S2), 수축(result S1, result S2))`.
//! `O(3^k)` 이라 `k ≲ 13` 까지 실용적.  partition 의 작은 leaf 서브트리를 이걸로
//! 마무리하면 subtree reconfiguration 효과 (cotengra 의 핵심 성능 요인).

use std::collections::HashMap;

use crate::path::SsaPath;

/// 두 인덱스 집합 수축의 (결과 집합, log10 flops, log2 result-size).
fn sym_contract(a: &[usize], b: &[usize], dims: &HashMap<usize, usize>) -> (Vec<usize>, f64, f64) {
    let d = |i: usize| (*dims.get(&i).unwrap_or(&2)) as f64;
    // union (flops), symmetric difference (result).
    let mut union_log = 0.0f64;
    for &i in a {
        union_log += d(i).log2();
    }
    for &i in b {
        if !a.contains(&i) {
            union_log += d(i).log2();
        }
    }
    let result: Vec<usize> = a
        .iter()
        .chain(b.iter())
        .copied()
        .filter(|i| a.contains(i) != b.contains(i))
        .collect::<std::collections::BTreeSet<_>>()
        .into_iter()
        .collect();
    let mut res_log = 0.0f64;
    for &i in &result {
        res_log += d(i).log2();
    }
    // flops(log10) = union dims 곱 → log10 = union_log2 * log10(2).
    (result, union_log * std::f64::consts::LOG10_2, res_log)
}

#[derive(Clone)]
struct Entry {
    peak_w: f64,                   // log2 peak intermediate width
    flops: f64,                    // log10 total flops
    indices: Vec<usize>,           // 결과 인덱스 집합
    split: Option<(usize, usize)>, // (submask1, submask2)
}

/// `(peak_w, flops)` 사전식 비교로 더 나은 쪽.
fn better(a: &(f64, f64), b: &(f64, f64)) -> bool {
    a.0 < b.0 - 1e-12 || (a.0 < b.0 + 1e-12 && a.1 < b.1 - 1e-12)
}

/// 부분망 (local index sets `0..k`) 의 최적 수축을 DP 로 구하고, `leaves` (global
/// id) / `next_id` 로 SSA path 에 emit, 최종 global id 반환.  `k ≤ ~13` 가정.
pub fn optimal_emit(
    local_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    leaves: &[usize],
    next_id: &mut usize,
    path: &mut SsaPath,
) -> usize {
    let k = local_indices.len();
    debug_assert_eq!(k, leaves.len());
    if k == 1 {
        return leaves[0];
    }
    let full = (1usize << k) - 1;
    let mut dp: Vec<Option<Entry>> = vec![None; 1 << k];
    // 단일 텐서 base.
    for (i, inds) in local_indices.iter().enumerate() {
        dp[1 << i] = Some(Entry {
            peak_w: 0.0,
            flops: 0.0,
            indices: inds.clone(),
            split: None,
        });
    }
    // popcount 오름차순으로 subset 처리.
    let mut masks: Vec<usize> = (1..=full).collect();
    masks.sort_by_key(|m| m.count_ones());
    for &mask in &masks {
        if mask.count_ones() < 2 {
            continue;
        }
        let mut best: Option<Entry> = None;
        let mut best_key = (f64::INFINITY, f64::INFINITY);
        // sub ⊂ mask 의 모든 분할 (sub, mask^sub), sub < complement 로 중복 제거.
        let mut sub = (mask - 1) & mask;
        while sub > 0 {
            let comp = mask ^ sub;
            if sub < comp {
                if let (Some(e1), Some(e2)) = (&dp[sub], &dp[comp]) {
                    let (res, flops_step, res_w) = sym_contract(&e1.indices, &e2.indices, dims);
                    let peak = e1.peak_w.max(e2.peak_w).max(res_w);
                    let flops = log10_add(e1.flops.max(0.0), e2.flops.max(0.0), flops_step);
                    let key = (peak, flops);
                    if best.is_none() || better(&key, &best_key) {
                        best_key = key;
                        best = Some(Entry {
                            peak_w: peak,
                            flops,
                            indices: res.clone(),
                            split: Some((sub, comp)),
                        });
                    }
                }
            }
            sub = (sub - 1) & mask;
        }
        dp[mask] = best;
    }

    // 재구성: emit(mask) → global id (post-order).
    fn emit(
        mask: usize,
        dp: &[Option<Entry>],
        leaves: &[usize],
        next_id: &mut usize,
        path: &mut SsaPath,
    ) -> usize {
        let e = dp[mask].as_ref().unwrap();
        match e.split {
            None => {
                // 단일 텐서 — 어느 leaf 인지 (mask 의 유일 bit).
                let b = mask.trailing_zeros() as usize;
                leaves[b]
            }
            Some((s1, s2)) => {
                let g1 = emit(s1, dp, leaves, next_id, path);
                let g2 = emit(s2, dp, leaves, next_id, path);
                path.push((g1, g2));
                let id = *next_id;
                *next_id += 1;
                id
            }
        }
    }
    emit(full, &dp, leaves, next_id, path)
}

/// `log10(10^a + 10^b + 10^c)` 안정적 합 (flops 누적).
fn log10_add(a: f64, b: f64, c: f64) -> f64 {
    let vals = [a, b, c];
    let m = vals.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    if m.is_infinite() {
        return 0.0;
    }
    let s: f64 = vals.iter().map(|&v| 10f64.powf(v - m)).sum();
    m + s.log10()
}

/// 전체 작은 네트워크의 최적 SSA path (leaves = `0..k`).
pub fn optimal_path(tensor_indices: &[Vec<usize>], dims: &HashMap<usize, usize>) -> SsaPath {
    let k = tensor_indices.len();
    if k <= 1 {
        return vec![];
    }
    let leaves: Vec<usize> = (0..k).collect();
    let mut next_id = k;
    let mut path = Vec::new();
    optimal_emit(tensor_indices, dims, &leaves, &mut next_id, &mut path);
    path
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::path::estimate_cost;

    fn dims2(ti: &[Vec<usize>]) -> HashMap<usize, usize> {
        let mut d = HashMap::new();
        for t in ti {
            for &i in t {
                d.insert(i, 2);
            }
        }
        d
    }

    #[test]
    fn optimal_no_worse_than_greedy() {
        // 사슬 + 닫힘 — optimal 이 greedy 보다 (같거나) 낮은 width.
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3], vec![3, 4], vec![0, 4]];
        let dims = dims2(&ti);
        let g = estimate_cost(&ti, &dims, &crate::path::greedy_path(&ti, &dims));
        let o = estimate_cost(&ti, &dims, &optimal_path(&ti, &dims));
        assert!(o.log2_width <= g.log2_width + 1e-9);
    }

    #[test]
    fn optimal_path_valid_length() {
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3]];
        let dims = dims2(&ti);
        let p = optimal_path(&ti, &dims);
        assert_eq!(p.len(), 2);
    }
}
