//! Index slicing — 메모리 한계 우회.
//!
//! 중간 텐서가 너무 클 때, 일부 인덱스를 고정값으로 "slice" 하면 각 slice 의
//! contraction 은 더 작은 메모리로 수행되고 결과를 합산한다.  슬라이스 대상
//! 인덱스 집합 `S` 에 대해 `2^{|S|}` 개 slice 를 (병렬) 계산해 더한다.
//!
//! `⟨x|C|0⟩ = Σ_{s ∈ {0,1}^{|S|}} ⟨x|C|0⟩|_{S=s}` — 슬라이스 인덱스를 각 값으로
//! 고정한 sub-network 들의 합.  슬라이스는 내부 (open 이 아닌) bond 인덱스만
//! 대상으로 한다.

use std::collections::HashMap;

use num_complex::Complex64;
use rayon::prelude::*;

use crate::network::CircuitNetwork;
use crate::path::{contract_ssa, estimate_cost, SsaPath};
use crate::tensor::Tensor;

/// 슬라이스할 인덱스를 고정값으로 잘라낸 텐서를 만든다.  텐서가 그 인덱스를
/// 포함하면 해당 축을 `value` 로 고정 (차원 1 축소), 아니면 그대로 둔다.
fn slice_tensor(t: &Tensor, sliced: &HashMap<usize, usize>) -> Tensor {
    // 이 텐서에 등장하는 슬라이스 인덱스.
    let positions: Vec<(usize, usize)> = t
        .indices
        .iter()
        .enumerate()
        .filter_map(|(p, idx)| sliced.get(idx).map(|&v| (p, v)))
        .collect();
    if positions.is_empty() {
        return t.clone();
    }
    // 남는 축.
    let keep_pos: Vec<usize> = (0..t.rank())
        .filter(|p| !positions.iter().any(|&(pp, _)| pp == *p))
        .collect();
    let new_indices: Vec<usize> = keep_pos.iter().map(|&p| t.indices[p]).collect();
    let new_dims: Vec<usize> = keep_pos.iter().map(|&p| t.dims[p]).collect();
    let new_size: usize = new_dims.iter().product::<usize>().max(1);

    // 기존 row-major strides.
    let r = t.rank();
    let mut old_strides = vec![1usize; r];
    for k in (0..r.saturating_sub(1)).rev() {
        old_strides[k] = old_strides[k + 1] * t.dims[k + 1];
    }
    let keep_strides: Vec<usize> = {
        let mut s = vec![1usize; keep_pos.len()];
        for k in (0..keep_pos.len().saturating_sub(1)).rev() {
            s[k] = s[k + 1] * new_dims[k + 1];
        }
        s
    };
    // 고정 축이 기여하는 base offset.
    let base: usize = positions.iter().map(|&(p, v)| v * old_strides[p]).sum();

    let data: Vec<Complex64> = (0..new_size)
        .map(|new_flat| {
            let mut rem = new_flat;
            let mut old_flat = base;
            for (kp, &p) in keep_pos.iter().enumerate() {
                let coord = rem / keep_strides[kp];
                rem %= keep_strides[kp];
                old_flat += coord * old_strides[p];
            }
            t.data[old_flat]
        })
        .collect();

    Tensor::new(new_indices, new_dims, data)
}

/// 슬라이스 인덱스 집합으로 네트워크를 contraction (스칼라 결과 가정 — amplitude).
///
/// 각 slice 설정에 대해 sub-network 를 만들어 동일 `path` 로 수축하고 합산한다.
/// 슬라이스를 병렬 (rayon) 처리해 peak 메모리를 `2^{-|sliced|}` 로 낮춘다.
pub fn contract_sliced_amplitude(
    net: &CircuitNetwork,
    path: &SsaPath,
    sliced_indices: &[usize],
) -> Complex64 {
    let configs = 1u64 << sliced_indices.len();
    contract_sliced_amplitude_range(net, path, sliced_indices, 0, configs)
}

/// **분산 슬라이싱**: slice 설정 인덱스 범위 `[start, end)` 만 수축해 부분합을
/// 반환한다.  각 slice 는 독립적 (통신 불필요) 이므로 worker/노드가 서로 다른
/// 범위를 계산하고 마지막에 부분합을 더하면 전체 amplitude 가 된다 — cuQuantum /
/// cotengra 의 distributed slicing 모델.  각 slice 의 peak 메모리는 sliced
/// contraction width (전체 N 무관) 이라 노드 RAM 에 맞춰 `max_width` 로 제어한다.
pub fn contract_sliced_amplitude_range(
    net: &CircuitNetwork,
    path: &SsaPath,
    sliced_indices: &[usize],
    start: u64,
    end: u64,
) -> Complex64 {
    (start..end)
        .into_par_iter()
        .map(|cfg| {
            let mut sliced = HashMap::new();
            for (b, &idx) in sliced_indices.iter().enumerate() {
                sliced.insert(idx, ((cfg >> b) & 1) as usize);
            }
            let sub: Vec<Tensor> = net
                .tensors
                .iter()
                .map(|t| slice_tensor(t, &sliced))
                .collect();
            let r = contract_ssa(&sub, path);
            debug_assert_eq!(r.rank(), 0);
            r.data[0]
        })
        .reduce(|| Complex64::new(0.0, 0.0), |a, b| a + b)
}

/// SSA path 를 symbolic 으로 시뮬레이션해 각 contraction 단계의 **중간 텐서
/// 인덱스 집합** 들을 반환한다 (`sliced` 인덱스는 제거).  peak-targeting slice
/// 선택에 쓰인다.
fn intermediate_index_sets(
    ti: &[Vec<usize>],
    path: &SsaPath,
    sliced: &std::collections::HashSet<usize>,
) -> Vec<Vec<usize>> {
    let mut store: Vec<Option<Vec<usize>>> = ti
        .iter()
        .map(|t| Some(t.iter().copied().filter(|x| !sliced.contains(x)).collect()))
        .collect();
    let mut inters = Vec::new();
    for &(i, j) in path {
        let a = store[i].take().expect("ssa consumed");
        let b = store[j].take().expect("ssa consumed");
        let res: Vec<usize> = a
            .iter()
            .chain(b.iter())
            .copied()
            .filter(|x| a.contains(x) != b.contains(x))
            .collect::<std::collections::BTreeSet<_>>()
            .into_iter()
            .collect();
        inters.push(res.clone());
        store.push(Some(res));
    }
    inters
}

/// 슬라이스 인덱스 선택 — **peak intermediate targeting**.  contraction width 가
/// `max_log2_width` 이하가 될 때까지, 예산 초과 중간 텐서들에 가장 많이 나타나는
/// bond 인덱스를 반복 slice (그 단계의 width 를 확실히 1 씩 낮춤).
pub fn choose_slices(
    net: &CircuitNetwork,
    path: &SsaPath,
    max_log2_width: f64,
    max_slices: usize,
) -> Vec<usize> {
    let dims = crate::dims_of(net);
    let ti: Vec<Vec<usize>> = net.tensors.iter().map(|t| t.indices.clone()).collect();

    // 후보: 내부 bond (2회 이상 등장).
    let mut count: HashMap<usize, usize> = HashMap::new();
    for t in &ti {
        for &i in t {
            *count.entry(i).or_insert(0) += 1;
        }
    }
    let candidate_set: std::collections::HashSet<usize> = count
        .iter()
        .filter(|(_, &c)| c >= 2)
        .map(|(&i, _)| i)
        .collect();

    let width_log2 = |set: &[usize]| -> f64 {
        set.iter()
            .map(|&i| (*dims.get(&i).unwrap_or(&2) as f64).log2())
            .sum()
    };

    let mut chosen_set: std::collections::HashSet<usize> = std::collections::HashSet::new();
    let mut chosen: Vec<usize> = Vec::new();
    while chosen.len() < max_slices {
        let inters = intermediate_index_sets(&ti, path, &chosen_set);
        let cur_max = inters.iter().map(|s| width_log2(s)).fold(0.0f64, f64::max);
        if cur_max <= max_log2_width + 1e-9 {
            break;
        }
        // 예산 초과 중간 텐서들에 등장하는 후보 인덱스의 빈도.
        let mut freq: HashMap<usize, usize> = HashMap::new();
        for s in &inters {
            if width_log2(s) > max_log2_width + 1e-9 {
                for &idx in s {
                    if candidate_set.contains(&idx) && !chosen_set.contains(&idx) {
                        *freq.entry(idx).or_insert(0) += 1;
                    }
                }
            }
        }
        // 가장 많은 초과 단계에 나타나는 인덱스 (tie: 작은 id).
        let pick = freq
            .into_iter()
            .max_by(|a, b| a.1.cmp(&b.1).then(b.0.cmp(&a.0)));
        match pick {
            Some((idx, _)) => {
                chosen.push(idx);
                chosen_set.insert(idx);
            }
            None => break, // 초과 단계에 sliceable 후보 없음.
        }
    }
    let _ = estimate_cost; // (peak-targeting 으로 대체; 비용 추정은 plan 단계에서)
    chosen
}

/// (legacy) width-reduction greedy — 보존용 미사용.
#[allow(dead_code)]
fn choose_slices_legacy(
    net: &CircuitNetwork,
    path: &SsaPath,
    max_log2_width: f64,
    max_slices: usize,
) -> Vec<usize> {
    let dims = crate::dims_of(net);
    let ti: Vec<Vec<usize>> = net.tensors.iter().map(|t| t.indices.clone()).collect();
    let mut count: HashMap<usize, usize> = HashMap::new();
    for t in &ti {
        for &i in t {
            *count.entry(i).or_insert(0) += 1;
        }
    }
    let mut candidates: Vec<usize> = count
        .iter()
        .filter(|(_, &c)| c >= 2)
        .map(|(&i, _)| i)
        .collect();
    candidates.sort_unstable();

    let mut chosen: Vec<usize> = Vec::new();
    let mut cur_cost = estimate_cost(&ti, &dims, path);

    while cur_cost.log2_width > max_log2_width && chosen.len() < max_slices {
        // 각 후보를 슬라이스했을 때 width 추정 — **이미 선택된 인덱스도 함께**
        // 제거해 누적 효과를 반영 (그래야 한 번에 한 인덱스씩 width 가 계속 감소).
        let mut best: Option<usize> = None;
        // (width, flops) 사전식 최소 후보 — slicing 은 width 를 늘리지 않으므로
        // 매 반복 최선을 무조건 수락 (monotone 비증가).  width 가 plateau 여도
        // flops 가 줄며 결국 peak step 의 인덱스가 충분히 제거되면 width 감소.
        let mut best_key = (f64::INFINITY, f64::INFINITY);
        for &cand in &candidates {
            if chosen.contains(&cand) {
                continue;
            }
            let sliced_ti: Vec<Vec<usize>> = ti
                .iter()
                .map(|t| {
                    t.iter()
                        .copied()
                        .filter(|&x| x != cand && !chosen.contains(&x))
                        .collect()
                })
                .collect();
            let c = estimate_cost(&sliced_ti, &dims, path);
            let key = (c.log2_width, c.log10_flops);
            if key < best_key {
                best_key = key;
                best = Some(cand);
            }
        }
        match best {
            Some(idx) => {
                chosen.push(idx);
                cur_cost = {
                    let sliced_ti: Vec<Vec<usize>> = ti
                        .iter()
                        .map(|t| t.iter().copied().filter(|x| !chosen.contains(x)).collect())
                        .collect();
                    estimate_cost(&sliced_ti, &dims, path)
                };
            }
            None => break, // 후보 소진.
        }
    }
    chosen
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::network::{build_amplitude_network, GateOp};
    use crate::path::greedy_path;
    use crate::{dims_of, PathOptimizer};
    use num_complex::Complex64 as C;

    fn h_mat() -> Vec<C> {
        let s = 1.0 / 2.0_f64.sqrt();
        vec![C::new(s, 0.), C::new(s, 0.), C::new(s, 0.), C::new(-s, 0.)]
    }
    fn cnot_mat() -> Vec<C> {
        let mut m = vec![C::new(0., 0.); 16];
        m[0] = C::new(1., 0.);
        m[5] = C::new(1., 0.);
        m[11] = C::new(1., 0.);
        m[14] = C::new(1., 0.);
        m
    }

    #[test]
    fn sliced_amplitude_matches_unsliced() {
        // Bell: amplitude(00) = 1/√2.  슬라이스 유/무가 동일해야.
        let ops = vec![
            GateOp::new(h_mat(), vec![0]),
            GateOp::new(cnot_mat(), vec![0, 1]),
        ];
        let net = build_amplitude_network(2, &ops, &[0, 0]);
        let dims = dims_of(&net);
        let ti: Vec<Vec<usize>> = net.tensors.iter().map(|t| t.indices.clone()).collect();
        let path = greedy_path(&ti, &dims);
        let full = crate::simulate_amplitude(2, &ops, &[0, 0], PathOptimizer::Greedy);
        // 내부 bond 하나를 슬라이스.
        let mut counts: HashMap<usize, usize> = HashMap::new();
        for t in &ti {
            for &i in t {
                *counts.entry(i).or_insert(0) += 1;
            }
        }
        let bond = *counts.iter().find(|(_, &c)| c >= 2).unwrap().0;
        let sliced = contract_sliced_amplitude(&net, &path, &[bond]);
        assert!(
            (full - sliced).norm() < 1e-12,
            "full={full} sliced={sliced}"
        );
    }
}
