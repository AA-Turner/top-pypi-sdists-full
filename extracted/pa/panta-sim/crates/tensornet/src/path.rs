//! Contraction path 최적화 (NP-hard) + 실행.
//!
//! Path 는 **SSA (static single assignment)** 형식: 초기 텐서 `0..m`, 각 수축이
//! 새 id `m, m+1, …` 를 생성하고 `(i, j)` 쌍을 기록한다 (cotengra ssa_path 와
//! 동일).  symbolic 인덱스 집합으로 실행 없이 비용 (총 FLOPs, 최대 중간 텐서
//! width) 을 추정하고, greedy / random-greedy / simulated annealing 으로 path 를
//! 탐색한다.

use std::collections::HashMap;

use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

use crate::tensor::{contract_pair, contract_pair_with, MatmulProvider, Tensor};

/// 수축 순서 (SSA 쌍 리스트).
pub type SsaPath = Vec<(usize, usize)>;

/// symbolic 텐서: 인덱스 라벨 집합 (정렬된 Vec).
#[derive(Clone)]
struct SymTensor {
    indices: Vec<usize>,
}

/// path 비용 요약.
#[derive(Debug, Clone, Copy)]
pub struct PathCost {
    /// 총 곱셈-덧셈 연산 수 (log10).
    pub log10_flops: f64,
    /// 가장 큰 중간 텐서의 원소 수 (log2) — 메모리/슬라이싱 지표 (contraction
    /// width).
    pub log2_width: f64,
}

fn index_dim(dims: &HashMap<usize, usize>, i: usize) -> usize {
    *dims.get(&i).unwrap_or(&2)
}

fn set_union(a: &[usize], b: &[usize]) -> Vec<usize> {
    let mut out = a.to_vec();
    for &x in b {
        if !a.contains(&x) {
            out.push(x);
        }
    }
    out
}

/// 두 symbolic 텐서 수축의 결과 인덱스 (대칭 차집합) + (flops, result_size) 추정.
pub(crate) fn sym_contract(
    a: &[usize],
    b: &[usize],
    dims: &HashMap<usize, usize>,
) -> (Vec<usize>, f64, usize) {
    let union = set_union(a, b);
    let flops: f64 = union.iter().map(|&i| index_dim(dims, i) as f64).product();
    let result: Vec<usize> = union
        .iter()
        .copied()
        .filter(|i| a.contains(i) != b.contains(i)) // a XOR b (소거되지 않은 것)
        .collect();
    let result_size: usize = result
        .iter()
        .map(|&i| index_dim(dims, i))
        .product::<usize>()
        .max(1);
    (result, flops, result_size)
}

/// path 비용을 실행 없이 추정.
pub fn estimate_cost(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    path: &SsaPath,
) -> PathCost {
    let mut sym: Vec<Option<Vec<usize>>> = tensor_indices.iter().map(|t| Some(t.clone())).collect();
    let mut total_flops = 0.0f64;
    let mut max_width = 1usize;
    for &(i, j) in path {
        let a = sym[i].take().expect("ssa: tensor already consumed");
        let b = sym[j].take().expect("ssa: tensor already consumed");
        let (res, flops, size) = sym_contract(&a, &b, dims);
        total_flops += flops;
        max_width = max_width.max(size);
        sym.push(Some(res));
    }
    PathCost {
        log10_flops: if total_flops > 0.0 {
            total_flops.log10()
        } else {
            0.0
        },
        log2_width: (max_width as f64).log2(),
    }
}

/// 인덱스 → 그 인덱스를 포함하는 살아있는 텐서 id 들의 인접 구조.
struct Adjacency {
    tensors: Vec<Option<SymTensor>>,
    dims: HashMap<usize, usize>,
}

impl Adjacency {
    fn new(tensor_indices: &[Vec<usize>], dims: HashMap<usize, usize>) -> Self {
        Adjacency {
            tensors: tensor_indices
                .iter()
                .map(|t| Some(SymTensor { indices: t.clone() }))
                .collect(),
            dims,
        }
    }

    fn alive(&self) -> Vec<usize> {
        (0..self.tensors.len())
            .filter(|&i| self.tensors[i].is_some())
            .collect()
    }

    /// 인덱스를 공유하는 살아있는 쌍들 (i<j).
    fn connected_pairs(&self) -> Vec<(usize, usize)> {
        let alive = self.alive();
        let mut pairs = Vec::new();
        for a in 0..alive.len() {
            for b in (a + 1)..alive.len() {
                let (i, j) = (alive[a], alive[b]);
                let ti = self.tensors[i].as_ref().unwrap();
                let tj = self.tensors[j].as_ref().unwrap();
                if ti.indices.iter().any(|x| tj.indices.contains(x)) {
                    pairs.push((i, j));
                }
            }
        }
        pairs
    }

    fn contract(&mut self, i: usize, j: usize) -> usize {
        let a = self.tensors[i].take().unwrap();
        let b = self.tensors[j].take().unwrap();
        let (res, _, _) = sym_contract(&a.indices, &b.indices, &self.dims);
        self.tensors.push(Some(SymTensor { indices: res }));
        self.tensors.len() - 1
    }
}

/// 결과 텐서 크기 (cost 휴리스틱).
fn pair_result_size(adj: &Adjacency, i: usize, j: usize) -> (usize, f64) {
    let a = &adj.tensors[i].as_ref().unwrap().indices;
    let b = &adj.tensors[j].as_ref().unwrap().indices;
    let (_, flops, size) = sym_contract(a, b, &adj.dims);
    (size, flops)
}

/// Greedy path: 매 단계 결과 텐서 크기가 최소인 (인덱스 공유) 쌍을 수축.
/// 동률은 FLOPs 최소.  disconnected 면 outer product (size 최소) 로 합침.
pub fn greedy_path(tensor_indices: &[Vec<usize>], dims: &HashMap<usize, usize>) -> SsaPath {
    greedy_path_seeded(tensor_indices, dims, None)
}

/// Greedy with optional random tie-break (random-greedy 의 한 trial).
fn greedy_path_seeded(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    rng: Option<&mut StdRng>,
) -> SsaPath {
    greedy_path_jitter(tensor_indices, dims, rng, 0.15)
}

/// Greedy with temperature-scaled jitter (jitter_mag) on the selection score.
fn greedy_path_jitter(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    rng: Option<&mut StdRng>,
    jitter_mag: f64,
) -> SsaPath {
    let mut adj = Adjacency::new(tensor_indices, dims.clone());
    let mut path = Vec::new();
    let mut jitter: Option<&mut StdRng> = rng;

    loop {
        let alive = adj.alive();
        if alive.len() <= 1 {
            break;
        }
        let pairs = adj.connected_pairs();
        let candidates = if pairs.is_empty() {
            // disconnected — outer product 가 불가피.  모든 쌍 고려.
            let mut all = Vec::new();
            for a in 0..alive.len() {
                for b in (a + 1)..alive.len() {
                    all.push((alive[a], alive[b]));
                }
            }
            all
        } else {
            pairs
        };

        // 결과 크기 최소 (동률 FLOPs 최소) 쌍 선택.  jitter 면 score 에 noise.
        let mut best: Option<(usize, usize)> = None;
        let mut best_key = f64::INFINITY;
        for &(i, j) in &candidates {
            let (size, flops) = pair_result_size(&adj, i, j);
            let mut key = (size as f64) * 1e6 + flops.log10().max(0.0);
            if let Some(ref mut r) = jitter {
                if jitter_mag > 0.0 {
                    key *= 1.0 + r.gen_range(-jitter_mag..jitter_mag);
                }
            }
            if key < best_key {
                best_key = key;
                best = Some((i, j));
            }
        }
        let (i, j) = best.unwrap();
        adj.contract(i, j);
        path.push((i, j));
    }
    path
}

/// path 의 scalar 비용 (width 우선, flops 보조) — 최적화 목적함수.
fn cost_scalar(c: &PathCost) -> f64 {
    c.log2_width * 1e3 + c.log10_flops
}

/// Random-greedy: `trials` 회 randomized greedy 중 비용 (flops) 최소 path.
pub fn random_greedy_path(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    trials: usize,
    seed: u64,
) -> SsaPath {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut best = greedy_path(tensor_indices, dims);
    let mut best_cost = estimate_cost(tensor_indices, dims, &best);
    for t in 0..trials {
        let mut trial_rng = StdRng::seed_from_u64(seed.wrapping_add(t as u64 + 1));
        let p = greedy_path_seeded(tensor_indices, dims, Some(&mut trial_rng));
        let c = estimate_cost(tensor_indices, dims, &p);
        // width (메모리) 우선, 그다음 flops.
        if (c.log2_width, c.log10_flops) < (best_cost.log2_width, best_cost.log10_flops) {
            best = p;
            best_cost = c;
        }
    }
    let _ = &mut rng;
    best
}

/// Simulated annealing path optimizer.
///
/// greedy-jitter 랜드스케이프 위에서 SA: 각 step 마다 현재 온도에 비례한 jitter
/// 로 greedy path 를 생성하고, scalar 비용 (width 우선) 에 Metropolis 기준으로
/// 수락한다.  `restarts` 회 독립 SA 중 전역 최선을 반환.  deep / 큰 회로의
/// contraction width 를 크게 낮춘다 (cotengra random-greedy + SA 패턴).
pub fn simulated_annealing_path(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    iters: usize,
    restarts: usize,
    seed: u64,
) -> SsaPath {
    // 시작점: 결정론적 greedy.
    let mut global_best = greedy_path(tensor_indices, dims);
    let mut global_cost = cost_scalar(&estimate_cost(tensor_indices, dims, &global_best));

    for r in 0..restarts.max(1) {
        let mut rng = StdRng::seed_from_u64(seed.wrapping_add((r as u64).wrapping_mul(0x9E3779B9)));
        let mut cur = greedy_path_jitter(tensor_indices, dims, Some(&mut rng), 0.3);
        let mut cur_cost = cost_scalar(&estimate_cost(tensor_indices, dims, &cur));
        let t0 = 1.0f64;
        let t_end = 1e-3f64;
        for it in 0..iters.max(1) {
            let frac = it as f64 / iters.max(1) as f64;
            let temp = t0 * (t_end / t0).powf(frac);
            // 온도에 비례한 jitter 로 이웃 path 생성.
            let jitter = 0.05 + 0.45 * temp;
            let cand = greedy_path_jitter(tensor_indices, dims, Some(&mut rng), jitter);
            let cand_cost = cost_scalar(&estimate_cost(tensor_indices, dims, &cand));
            let delta = cand_cost - cur_cost;
            let accept = delta < 0.0 || rng.gen::<f64>() < (-delta / (temp * 50.0 + 1e-9)).exp();
            if accept {
                cur = cand;
                cur_cost = cand_cost;
            }
            if cur_cost < global_cost {
                global_cost = cur_cost;
                global_best = cur.clone();
            }
        }
    }
    global_best
}

/// SSA path 를 실제 텐서에 실행해 최종 텐서를 반환.
pub fn contract_ssa(tensors: &[Tensor], path: &SsaPath) -> Tensor {
    if tensors.len() == 1 && path.is_empty() {
        return tensors[0].clone();
    }
    let mut store: Vec<Option<Tensor>> = tensors.iter().map(|t| Some(t.clone())).collect();
    let mut last = 0usize;
    for &(i, j) in path {
        let a = store[i].take().expect("ssa exec: consumed");
        let b = store[j].take().expect("ssa exec: consumed");
        let r = contract_pair(&a, &b);
        store.push(Some(r));
        last = store.len() - 1;
    }
    store[last].take().expect("ssa exec: no result")
}

/// SSA path 를 실행하되 `provider` 의 matmul 사용 (GPU contraction).
pub fn contract_ssa_with<M: MatmulProvider>(
    tensors: &[Tensor],
    path: &SsaPath,
    provider: &M,
) -> Tensor {
    if tensors.len() == 1 && path.is_empty() {
        return tensors[0].clone();
    }
    let mut store: Vec<Option<Tensor>> = tensors.iter().map(|t| Some(t.clone())).collect();
    let mut last = 0usize;
    for &(i, j) in path {
        let a = store[i].take().expect("ssa exec: consumed");
        let b = store[j].take().expect("ssa exec: consumed");
        let r = contract_pair_with(&a, &b, provider);
        store.push(Some(r));
        last = store.len() - 1;
    }
    store[last].take().expect("ssa exec: no result")
}

#[cfg(test)]
mod tests {
    use super::*;

    fn dims_all2(tensor_indices: &[Vec<usize>]) -> HashMap<usize, usize> {
        let mut d = HashMap::new();
        for t in tensor_indices {
            for &i in t {
                d.insert(i, 2);
            }
        }
        d
    }

    #[test]
    fn greedy_chain_path_valid() {
        // 사슬: t0[0,1] t1[1,2] t2[2,3] → 스칼라 아님, 열린 0,3.
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3]];
        let dims = dims_all2(&ti);
        let path = greedy_path(&ti, &dims);
        // 2 contractions for 3 tensors.
        assert_eq!(path.len(), 2);
        let cost = estimate_cost(&ti, &dims, &path);
        assert!(cost.log2_width.is_finite());
    }

    #[test]
    fn random_greedy_no_worse_than_greedy() {
        let ti = vec![vec![0, 1], vec![1, 2], vec![2, 3], vec![0, 3]];
        let dims = dims_all2(&ti);
        let g = estimate_cost(&ti, &dims, &greedy_path(&ti, &dims));
        let rg = estimate_cost(&ti, &dims, &random_greedy_path(&ti, &dims, 16, 1));
        assert!(rg.log2_width <= g.log2_width + 1e-9);
    }
}
