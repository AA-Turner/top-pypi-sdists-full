//! # qsim-tensornet
//!
//! Tensor Network Contraction 시뮬레이터 — 양자 *회로* 를 tensor network 으로
//! 표현하고 contraction path 최적화로 deep / random 회로의 amplitude·expectation·
//! sampling 을 계산한다 (MPS 가 못 하는 high-entanglement deep 회로 영역;
//! Quantum Rings / cuTensorNet 영역).
//!
//! 구성:
//! - [`tensor`]: 라벨드 dense 복소 텐서 + pairwise contraction (permute+matmul).
//! - [`network`]: 회로 → tensor network (amplitude / statevector).
//! - [`path`]: contraction path 최적화 (greedy / random-greedy / simulated
//!   annealing) + SSA 실행.
//! - [`slicing`]: 메모리 한계 우회를 위한 index slicing.
//!
//! cross-platform GPU contraction (wgpu) 은 별도 (`qsim-gpu`) — contraction
//! 커널이 batched matmul 로 환원되므로 동일 path 를 GPU 로 실행한다.

use std::collections::HashMap;

use num_complex::Complex64;

pub mod network;
pub mod optimal;
pub mod partition;
pub mod path;
pub mod reconfigure;
pub mod slicing;
pub mod tensor;

pub use network::{build_amplitude_network, build_statevector_network, CircuitNetwork, GateOp};
pub use path::{
    contract_ssa, contract_ssa_with, estimate_cost, greedy_path, random_greedy_path,
    simulated_annealing_path, PathCost, SsaPath,
};
pub use reconfigure::subtree_reconfigure;
pub use tensor::{contract_pair, contract_pair_with, CpuMatmul, MatmulProvider, Tensor};

/// contraction path 탐색 전략.
#[derive(Debug, Clone, Copy)]
pub enum PathOptimizer {
    /// 단일 greedy (가장 빠름, 중간 규모).
    Greedy,
    /// randomized greedy `trials` 회 중 최선.
    RandomGreedy { trials: usize, seed: u64 },
    /// simulated annealing (deep / 큰 회로 contraction cost 최소화).
    SimulatedAnnealing {
        iters: usize,
        restarts: usize,
        seed: u64,
    },
    /// hypergraph-partition 재귀 이분할 (FM 정제) `trials` 회 중 최선 — high-
    /// treewidth (2D / random / supremacy) 회로의 width 최소화.
    Partition { trials: usize, seed: u64 },
    /// 모든 방법 (greedy + random-greedy + SA + partition) 을 돌려 estimate_cost
    /// 가 최소인 path 선택 — cotengra 식 hyper-optimization.
    Hyper { effort: usize, seed: u64 },
    /// Held-Karp DP 로 provably-optimal (작은 네트워크 ≤ ~13 텐서 전용).
    Optimal,
}

impl Default for PathOptimizer {
    fn default() -> Self {
        PathOptimizer::RandomGreedy {
            trials: 32,
            seed: 0,
        }
    }
}

/// 네트워크의 인덱스 → 차원 맵.
pub fn dims_of(net: &CircuitNetwork) -> HashMap<usize, usize> {
    let mut d = HashMap::new();
    for t in &net.tensors {
        for (k, &idx) in t.indices.iter().enumerate() {
            d.insert(idx, t.dims[k]);
        }
    }
    d
}

fn tensor_index_sets(net: &CircuitNetwork) -> Vec<Vec<usize>> {
    net.tensors.iter().map(|t| t.indices.clone()).collect()
}

/// 주어진 전략으로 contraction path 를 찾는다.
///
/// 어떤 optimizer 든 마지막에 **subtree reconfiguration** 으로 한 번 더 정제한다
/// (cotengra 식) — 국소 서브트리를 optimal DP 로 재최적화해 (peak-width 우선,
/// flops 보조) 더 싼 경우에만 채택하므로 결과는 절대 나빠지지 않는다.
pub fn find_path(net: &CircuitNetwork, opt: PathOptimizer) -> SsaPath {
    let ti = tensor_index_sets(net);
    let dims = dims_of(net);
    let path = match opt {
        PathOptimizer::Greedy => greedy_path(&ti, &dims),
        PathOptimizer::RandomGreedy { trials, seed } => {
            random_greedy_path(&ti, &dims, trials, seed)
        }
        PathOptimizer::SimulatedAnnealing {
            iters,
            restarts,
            seed,
        } => simulated_annealing_path(&ti, &dims, iters, restarts, seed),
        PathOptimizer::Partition { trials, seed } => best_partition_path(&ti, &dims, trials, seed),
        PathOptimizer::Hyper { effort, seed } => hyper_path(&ti, &dims, effort, seed),
        PathOptimizer::Optimal => return optimal::optimal_path(&ti, &dims), // 이미 최적.
    };
    refine_path(&ti, &dims, path)
}

/// subtree reconfiguration 정제 (size guard 포함).  optimal DP 가 unit 당
/// `O(3^u)` 이므로 텐서 수가 매우 많으면 unit/sweep 을 줄여 비용을 억제한다.
fn refine_path(ti: &[Vec<usize>], dims: &HashMap<usize, usize>, path: SsaPath) -> SsaPath {
    let k = ti.len();
    if k <= 3 {
        return path;
    }
    // 큰 망에서는 보수적으로 (재구성 자체 비용 억제).
    let (max_units, sweeps) = if k <= 400 { (10, 8) } else { (8, 4) };
    reconfigure::subtree_reconfigure(ti, dims, &path, max_units, sweeps)
}

/// partition optimizer: `trials` 회 (서로 다른 seed) 중 cost 최소 path.
fn best_partition_path(
    ti: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    trials: usize,
    seed: u64,
) -> SsaPath {
    let mut best = partition::partition_path_seeded(ti, dims, seed);
    let mut best_cost = path_score(&estimate_cost(ti, dims, &best));
    for t in 1..trials.max(1) {
        let p = partition::partition_path_seeded(ti, dims, seed.wrapping_add(t as u64));
        let c = path_score(&estimate_cost(ti, dims, &p));
        if c < best_cost {
            best_cost = c;
            best = p;
        }
    }
    best
}

/// width 우선, flops 보조의 scalar cost (optimizer 간 비교용).
fn path_score(c: &PathCost) -> f64 {
    c.log2_width * 1e3 + c.log10_flops
}

/// slice-aware path 선택을 위한 후보 path 들 (greedy + random-greedy + SA +
/// partition).  결정론적 (seeded) — 분산 worker 들이 동일 후보를 재구성한다.
pub fn candidate_paths(
    tensor_indices: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    effort: usize,
    seed: u64,
) -> Vec<SsaPath> {
    let e = effort.max(1);
    vec![
        greedy_path(tensor_indices, dims),
        random_greedy_path(tensor_indices, dims, 8 * e, seed),
        simulated_annealing_path(tensor_indices, dims, 40 * e, 2, seed.wrapping_add(101)),
        // partition 은 high-treewidth 에서 가장 강력 — 서로 다른 seed 2 개로
        // randomized 휴리스틱의 분산을 흡수 (각 넉넉한 trial).
        best_partition_path(tensor_indices, dims, 12 * e, seed),
        best_partition_path(tensor_indices, dims, 12 * e, seed.wrapping_add(202)),
    ]
}

/// hyper-optimization: greedy + random-greedy + SA + partition 을 모두 돌리되,
/// **각 후보를 subtree reconfiguration 으로 정제한 뒤** estimate_cost 최소 path 를
/// 고른다.  raw 후보 best 를 골라 정제하는 것보다, 후보마다 정제 잠재력이 달라
/// (raw 로는 차선이어도 정제 후 최적일 수 있음) 더 나은 path 를 얻는다.
fn hyper_path(
    ti: &[Vec<usize>],
    dims: &HashMap<usize, usize>,
    effort: usize,
    seed: u64,
) -> SsaPath {
    let (max_units, sweeps) = if ti.len() <= 400 { (10, 8) } else { (8, 4) };
    candidate_paths(ti, dims, effort, seed)
        .into_iter()
        .map(|p| reconfigure::subtree_reconfigure(ti, dims, &p, max_units, sweeps))
        .min_by(|a, b| {
            let ca = path_score(&estimate_cost(ti, dims, a));
            let cb = path_score(&estimate_cost(ti, dims, b));
            ca.partial_cmp(&cb).unwrap()
        })
        .unwrap()
}

/// amplitude `⟨bitstring|C|0…0⟩` 를 계산한다.
pub fn simulate_amplitude(
    n_qubits: usize,
    ops: &[GateOp],
    bitstring: &[u8],
    opt: PathOptimizer,
) -> Complex64 {
    let net = build_amplitude_network(n_qubits, ops, bitstring);
    let path = find_path(&net, opt);
    let result = contract_ssa(&net.tensors, &path);
    debug_assert_eq!(result.rank(), 0, "amplitude 는 스칼라여야 함");
    result.data[0]
}

/// 전체 statevector 를 계산한다 (작은 N).  반환 벡터는 **큐비트 0 = MSB** 컨벤션
/// (index = Σ_q bit_q · 2^{n-1-q}).
pub fn simulate_statevector(n_qubits: usize, ops: &[GateOp], opt: PathOptimizer) -> Vec<Complex64> {
    let net = build_statevector_network(n_qubits, ops);
    let path = find_path(&net, opt);
    let result = contract_ssa(&net.tensors, &path);
    // 결과 인덱스를 큐비트 순서 (open_indices) 로 permute → row-major = MSB 컨벤션.
    let perm: Vec<usize> = net
        .open_indices
        .iter()
        .map(|idx| result.indices.iter().position(|x| x == idx).unwrap())
        .collect();
    result.permute(&perm).data
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_complex::Complex64 as C;

    fn h_mat() -> Vec<C> {
        let s = 1.0 / 2.0_f64.sqrt();
        vec![C::new(s, 0.), C::new(s, 0.), C::new(s, 0.), C::new(-s, 0.)]
    }
    fn x_mat() -> Vec<C> {
        vec![
            C::new(0., 0.),
            C::new(1., 0.),
            C::new(1., 0.),
            C::new(0., 0.),
        ]
    }
    // CNOT (control=qubits[0]=MSB, target=qubits[1]): 4x4 row-major.
    fn cnot_mat() -> Vec<C> {
        let mut m = vec![C::new(0., 0.); 16];
        let set = |m: &mut Vec<C>, r: usize, c: usize| m[r * 4 + c] = C::new(1., 0.);
        set(&mut m, 0, 0);
        set(&mut m, 1, 1);
        set(&mut m, 2, 3);
        set(&mut m, 3, 2);
        m
    }

    #[test]
    fn bell_statevector_matches() {
        // H on q0, CNOT(q0,q1) → (|00>+|11>)/√2.
        let ops = vec![
            GateOp::new(h_mat(), vec![0]),
            GateOp::new(cnot_mat(), vec![0, 1]),
        ];
        let sv = simulate_statevector(2, &ops, PathOptimizer::Greedy);
        let s = 1.0 / 2.0_f64.sqrt();
        assert!((sv[0].re - s).abs() < 1e-12);
        assert!((sv[3].re - s).abs() < 1e-12);
        assert!(sv[1].norm() < 1e-12 && sv[2].norm() < 1e-12);
    }

    #[test]
    fn bell_amplitudes_match() {
        let ops = vec![
            GateOp::new(h_mat(), vec![0]),
            GateOp::new(cnot_mat(), vec![0, 1]),
        ];
        let s = 1.0 / 2.0_f64.sqrt();
        let a00 = simulate_amplitude(2, &ops, &[0, 0], PathOptimizer::Greedy);
        let a11 = simulate_amplitude(2, &ops, &[1, 1], PathOptimizer::Greedy);
        let a01 = simulate_amplitude(2, &ops, &[0, 1], PathOptimizer::Greedy);
        assert!((a00.re - s).abs() < 1e-12);
        assert!((a11.re - s).abs() < 1e-12);
        assert!(a01.norm() < 1e-12);
    }

    #[test]
    fn x_flips_qubit() {
        // X on q1 of 2-qubit |00> → |01> (q1=1).  MSB=q0 → index 01 = 1.
        let ops = vec![GateOp::new(x_mat(), vec![1])];
        let sv = simulate_statevector(2, &ops, PathOptimizer::Greedy);
        assert!((sv[1].re - 1.0).abs() < 1e-12);
        assert!(sv[0].norm() < 1e-12);
    }

    #[test]
    fn optimizers_agree() {
        // 더 큰 회로에서 greedy / random-greedy / SA 가 같은 statevector.
        let ops = vec![
            GateOp::new(h_mat(), vec![0]),
            GateOp::new(cnot_mat(), vec![0, 1]),
            GateOp::new(h_mat(), vec![2]),
            GateOp::new(cnot_mat(), vec![1, 2]),
            GateOp::new(cnot_mat(), vec![2, 3]),
        ];
        let g = simulate_statevector(4, &ops, PathOptimizer::Greedy);
        let rg = simulate_statevector(4, &ops, PathOptimizer::RandomGreedy { trials: 8, seed: 1 });
        let sa = simulate_statevector(
            4,
            &ops,
            PathOptimizer::SimulatedAnnealing {
                iters: 50,
                restarts: 2,
                seed: 1,
            },
        );
        for i in 0..g.len() {
            assert!((g[i] - rg[i]).norm() < 1e-12, "greedy vs rg @ {i}");
            assert!((g[i] - sa[i]).norm() < 1e-12, "greedy vs sa @ {i}");
        }
    }
}
