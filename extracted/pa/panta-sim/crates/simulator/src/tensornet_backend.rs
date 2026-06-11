//! Tensor Network Contraction 백엔드 (v0.8, qsim-tensornet 통합).
//!
//! 회로의 게이트를 [`qsim_tensornet::GateOp`] 로 변환해 tensor network 으로
//! contraction 한다.  MPS 가 못 하는 deep / high-entanglement 회로의
//! amplitude·statevector·sampling 을 계산한다 (Quantum Rings / cuTensorNet 영역).
//!
//! 게이트 행렬은 기존 [`apply_gate_typed`]/[`apply_unitary_typed`] 로 basis state
//! 에 작용시켜 추출하므로 모든 게이트 정의를 재사용한다 (컨벤션 안전).  tensornet
//! 은 `qubits[0]=MSB`, panta statevector 는 `qubit 0=LSB` 이므로 인덱스 bit-
//! reversal 로 변환한다.

use std::collections::HashMap;

use num_complex::Complex64;
use qsim_core::StateVector;
use qsim_tensornet::{
    build_amplitude_network, build_statevector_network, contract_ssa, contract_ssa_with, dims_of,
    estimate_cost, find_path, GateOp, MatmulProvider, PathOptimizer,
};
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

use crate::engine::{apply_gate_typed, apply_unitary_typed};
use crate::instruction::Instruction;
use crate::Circuit;

/// k-bit 정수의 bit reversal (panta LSB ↔ tensornet MSB 컨벤션 변환).
fn bitrev(x: usize, k: usize) -> usize {
    let mut r = 0usize;
    for b in 0..k {
        if (x >> b) & 1 == 1 {
            r |= 1 << (k - 1 - b);
        }
    }
    r
}

/// 단일 게이트/유니터리를 MSB-컨벤션 `2^k × 2^k` row-major 행렬로 추출한다.
/// `apply` 는 로컬 큐비트 `0..k` 에 연산을 작용시키는 클로저.
fn extract_msb_matrix<A>(k: usize, apply: A) -> Vec<Complex64>
where
    A: Fn(&mut StateVector<f64>, &[usize]),
{
    let dim = 1usize << k;
    let locals: Vec<usize> = (0..k).collect();
    let mut m = vec![Complex64::new(0.0, 0.0); dim * dim];
    for col in 0..dim {
        let mut psi = StateVector::<f64>::new(k);
        let amps = psi.amplitudes_mut();
        amps[0] = Complex64::new(0.0, 0.0);
        amps[bitrev(col, k)] = Complex64::new(1.0, 0.0); // |MSB=col⟩
        apply(&mut psi, &locals);
        let out = psi.amplitudes();
        for (a, &amp) in out.iter().enumerate() {
            m[bitrev(a, k) * dim + col] = amp;
        }
    }
    m
}

/// 회로의 unitary 게이트들을 [`GateOp`] 시퀀스로 변환한다.  측정 (`Measure`/
/// `MeasureAll`) 은 무시 (sampling 에서 별도 처리), 노이즈/동적 instruction 은
/// `Err`.
pub fn circuit_to_gateops(circuit: &Circuit) -> Result<Vec<GateOp>, String> {
    // 비-trailing (mid-circuit) 측정은 collapse 시맨틱이 필요한데 TN 은 순수
    // 유니터리 contraction 이라 표현할 수 없다 — 조용히 무시하면 잘못된
    // 분포/진폭이 나오므로 명시적으로 거부한다 (trailing 측정 묶음만 허용).
    let insts = circuit.instructions();
    for (i, inst) in insts.iter().enumerate() {
        if matches!(inst, Instruction::Measure { .. } | Instruction::MeasureAll)
            && insts[i + 1..].iter().any(|later| {
                !matches!(later, Instruction::Measure { .. } | Instruction::MeasureAll)
            })
        {
            return Err("tensornet: mid-circuit 측정 미지원 (회로 끝 trailing 측정만 가능)".into());
        }
    }
    let mut ops = Vec::new();
    for inst in circuit.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                let g = gate.clone();
                let mat = extract_msb_matrix(targets.len(), |psi, locals| {
                    apply_gate_typed(psi, &g, locals)
                });
                ops.push(GateOp::new(mat, targets.clone()));
            }
            Instruction::ApplyUnitary { matrix, targets } => {
                let mtx = matrix.clone();
                let mat = extract_msb_matrix(targets.len(), |psi, locals| {
                    apply_unitary_typed(psi, &mtx, locals)
                });
                ops.push(GateOp::new(mat, targets.clone()));
            }
            Instruction::Measure { .. } | Instruction::MeasureAll => {}
            Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. } => {
                return Err("tensornet: 노이즈 회로 미지원 (순수 유니터리만)".into());
            }
            _ => {
                return Err("tensornet: 동적 instruction (reset/측정 기반 제어흐름) 미지원".into());
            }
        }
    }
    Ok(ops)
}

/// 전체 statevector 를 tensor network contraction 으로 계산 (작은 N).  결과는
/// panta 컨벤션 (qubit 0 = LSB).
pub fn run_statevector(circuit: &Circuit, opt: PathOptimizer) -> Result<StateVector<f64>, String> {
    let n = circuit.num_qubits();
    let ops = circuit_to_gateops(circuit)?;
    let net = build_statevector_network(n, &ops);
    let path = find_path(&net, opt);
    let result = contract_ssa(&net.tensors, &path);
    // 결과 인덱스를 큐비트 순서로 permute → MSB row-major.
    let perm: Vec<usize> = net
        .open_indices
        .iter()
        .map(|idx| result.indices.iter().position(|x| x == idx).unwrap())
        .collect();
    let tn_data = result.permute(&perm).data;
    // MSB → panta LSB: panta[i] = tn[bitrev(i)].
    let mut sv = StateVector::<f64>::new(n);
    let phase = global_phase_factor(circuit);
    let amps = sv.amplitudes_mut();
    for (i, slot) in amps.iter_mut().enumerate() {
        *slot = tn_data[bitrev(i, n)] * phase;
    }
    Ok(sv)
}

/// `Circuit::global_phase` 의 위상 인자 `e^{iλ}`.
///
/// 다른 statevector 경로 (`apply_global_phase`) 와 달리 TN contraction 은
/// 게이트 행렬만 보므로, KAK/QSD 분해·inverse·transpile 이 기록한 전역 위상을
/// 결과에 곱해 줘야 백엔드 간 진폭이 bit-exact 로 일치한다.
fn global_phase_factor(circuit: &Circuit) -> num_complex::Complex<f64> {
    let lambda = circuit.global_phase();
    if lambda == 0.0 {
        num_complex::Complex::new(1.0, 0.0)
    } else {
        num_complex::Complex::from_polar(1.0, lambda)
    }
}

/// amplitude `⟨bitstring|C|0…0⟩`.  `bitstring[q]` = 큐비트 `q` 측정값 (panta 순서).
pub fn run_amplitude(
    circuit: &Circuit,
    bitstring: &[u8],
    opt: PathOptimizer,
) -> Result<Complex64, String> {
    let n = circuit.num_qubits();
    if bitstring.len() != n {
        return Err(format!(
            "tensornet amplitude: bitstring 길이 {} != n_qubits {}",
            bitstring.len(),
            n
        ));
    }
    let ops = circuit_to_gateops(circuit)?;
    let net = build_amplitude_network(n, &ops, bitstring);
    let path = find_path(&net, opt);
    let result = contract_ssa(&net.tensors, &path);
    debug_assert_eq!(result.rank(), 0);
    Ok(result.data[0] * global_phase_factor(circuit))
}

/// 여러 비트열의 amplitude `⟨xᵢ|C|0…0⟩` 를 한 번에 계산한다 (v0.8.4).
///
/// amplitude network 의 **인덱스 구조는 비트열과 무관** (boundary projector 의
/// *값* 만 다름) 하므로, contraction path 를 **첫 비트열로 한 번만** 최적화하고
/// 모든 비트열에 재사용한다.  path 탐색 (hyper / SA 는 비쌈) 을 N_bitstrings 회
/// → 1 회로 줄이고, 각 비트열 contraction 은 rayon 병렬로 수행한다.  XEB 처럼
/// 수백~수천 비트열의 amplitude 를 구할 때 큰 속도 향상.
pub fn run_amplitude_batch(
    circuit: &Circuit,
    bitstrings: &[Vec<u8>],
    opt: PathOptimizer,
) -> Result<Vec<Complex64>, String> {
    use rayon::prelude::*;
    let n = circuit.num_qubits();
    for bs in bitstrings {
        if bs.len() != n {
            return Err(format!(
                "tensornet amplitude batch: bitstring 길이 {} != n_qubits {}",
                bs.len(),
                n
            ));
        }
    }
    if bitstrings.is_empty() {
        return Ok(Vec::new());
    }
    let ops = circuit_to_gateops(circuit)?;
    // path 는 구조만 의존 — 첫 비트열로 한 번 최적화.
    let net0 = build_amplitude_network(n, &ops, &bitstrings[0]);
    let path = find_path(&net0, opt);
    // 각 비트열 독립 contraction (rayon 병렬).
    let phase = global_phase_factor(circuit);
    let out = bitstrings
        .par_iter()
        .map(|bs| {
            let net = build_amplitude_network(n, &ops, bs);
            contract_ssa(&net.tensors, &path).data[0] * phase
        })
        .collect();
    Ok(out)
}

/// **slice-aware path 선택**: 후보 path 중 `max_width` 까지 slicing 에 필요한
/// slice 수가 최소 (동률 sliced-flops 최소) 인 (path, slice 인덱스) 를 고른다.
/// `Hyper` 가 아니면 단일 path.  결정론적 — 분산 worker 들이 동일 선택 재구성.
fn select_sliced_path(
    net: &qsim_tensornet::CircuitNetwork,
    opt: PathOptimizer,
    max_width: f64,
    max_slices: usize,
) -> (qsim_tensornet::SsaPath, Vec<usize>) {
    let dims = dims_of(net);
    let ti: Vec<Vec<usize>> = net.tensors.iter().map(|t| t.indices.clone()).collect();
    let candidates: Vec<qsim_tensornet::SsaPath> = match opt {
        PathOptimizer::Hyper { effort, seed } => {
            qsim_tensornet::candidate_paths(&ti, &dims, effort, seed)
        }
        other => vec![find_path(net, other)],
    };
    let mut best: Option<(qsim_tensornet::SsaPath, Vec<usize>, usize, f64)> = None;
    for path in candidates {
        let slices = qsim_tensornet::slicing::choose_slices(net, &path, max_width, max_slices);
        // sliced flops 추정 (slice 인덱스 제거 후 path 비용 + 2^n_slices).
        let sliced_ti: Vec<Vec<usize>> = ti
            .iter()
            .map(|t| t.iter().copied().filter(|x| !slices.contains(x)).collect())
            .collect();
        let c = estimate_cost(&sliced_ti, &dims, &path);
        let total_flops = c.log10_flops + (slices.len() as f64) * std::f64::consts::LOG10_2;
        let key = (slices.len(), total_flops);
        if best
            .as_ref()
            .map(|(_, _, ns, f)| key < (*ns, *f))
            .unwrap_or(true)
        {
            best = Some((path, slices, key.0, key.1));
        }
    }
    let (path, slices, _, _) = best.expect("at least one candidate path");
    (path, slices)
}

/// amplitude `⟨bitstring|C|0…0⟩` 를 **자동 slicing** 으로 계산한다.  contraction
/// width 가 `max_width` (log2 큐비트 수) 를 넘으면 일부 bond 인덱스를 slice 해
/// peak 메모리를 `max_width` 이하로 낮추고 slice 들을 (rayon 병렬) 합산한다.
/// 큰 2D / random 회로를 메모리 한계 안에서 계산하는 핵심 (supremacy-style).
/// `Hyper` 면 slice-aware path 선택 (slice 수 최소화).
pub fn run_amplitude_sliced(
    circuit: &Circuit,
    bitstring: &[u8],
    opt: PathOptimizer,
    max_width: f64,
    max_slices: usize,
) -> Result<Complex64, String> {
    let n = circuit.num_qubits();
    if bitstring.len() != n {
        return Err(format!(
            "tensornet amplitude: bitstring 길이 {} != n_qubits {}",
            bitstring.len(),
            n
        ));
    }
    let ops = circuit_to_gateops(circuit)?;
    let net = build_amplitude_network(n, &ops, bitstring);
    let (path, sliced) = select_sliced_path(&net, opt, max_width, max_slices);
    let phase = global_phase_factor(circuit);
    if sliced.is_empty() {
        let result = contract_ssa(&net.tensors, &path);
        Ok(result.data[0] * phase)
    } else {
        Ok(qsim_tensornet::slicing::contract_sliced_amplitude(&net, &path, &sliced) * phase)
    }
}

/// 자동 slicing 시 선택될 slice 개수 (메모리 추정용 introspection).
pub fn slice_count(
    circuit: &Circuit,
    opt: PathOptimizer,
    max_width: f64,
    max_slices: usize,
) -> Result<usize, String> {
    let n = circuit.num_qubits();
    let ops = circuit_to_gateops(circuit)?;
    let zero = vec![0u8; n];
    let net = build_amplitude_network(n, &ops, &zero);
    let path = find_path(&net, opt);
    Ok(qsim_tensornet::slicing::choose_slices(&net, &path, max_width, max_slices).len())
}

/// 분산 슬라이싱 계획 — `(n_slices, n_configs, log2_width_per_slice,
/// log10_total_flops)`.  `n_configs = 2^n_slices` 가 worker 들에 분배할 독립
/// 작업 단위 수, `log2_width_per_slice` 가 worker 당 peak 메모리 (큐비트 수,
/// 전체 N 무관) — 노드 RAM 에 맞춰 `max_width` 로 제어.
pub fn plan_amplitude(
    circuit: &Circuit,
    opt: PathOptimizer,
    max_width: f64,
    max_slices: usize,
) -> Result<(usize, u64, f64, f64), String> {
    let n = circuit.num_qubits();
    let ops = circuit_to_gateops(circuit)?;
    let zero = vec![0u8; n];
    let net = build_amplitude_network(n, &ops, &zero);
    let (path, sliced) = select_sliced_path(&net, opt, max_width, max_slices);
    let dims = dims_of(&net);
    // sliced 인덱스를 모든 텐서에서 제거한 뒤의 width / flops.
    let ti: Vec<Vec<usize>> = net
        .tensors
        .iter()
        .map(|t| {
            t.indices
                .iter()
                .copied()
                .filter(|x| !sliced.contains(x))
                .collect()
        })
        .collect();
    let cost = estimate_cost(&ti, &dims, &path);
    let n_slices = sliced.len();
    let n_configs = 1u64 << n_slices;
    // 총 flops ≈ slice 당 flops × n_configs (log10).
    let total_flops = cost.log10_flops + (n_configs as f64).log10();
    Ok((n_slices, n_configs, cost.log2_width, total_flops))
}

/// **분산 슬라이싱 worker**: 전체 slice 작업을 `n_workers` 로 나눠 `worker_id`
/// 번째 worker 의 부분합을 반환한다.  모든 worker 가 동일 (opt+seed 결정론적)
/// 계획을 독립 재구성하므로 plan broadcast 가 불필요 — 부분합을 모두 더하면
/// 전체 amplitude (`run_amplitude_sliced` 와 동일).  멀티노드/MPI 는 이 부분합을
/// 네트워크로 reduce 하면 된다.
#[allow(clippy::too_many_arguments)]
pub fn run_amplitude_worker(
    circuit: &Circuit,
    bitstring: &[u8],
    opt: PathOptimizer,
    max_width: f64,
    max_slices: usize,
    n_workers: u64,
    worker_id: u64,
) -> Result<Complex64, String> {
    let n = circuit.num_qubits();
    if bitstring.len() != n {
        return Err(format!(
            "tensornet amplitude: bitstring 길이 {} != n_qubits {}",
            bitstring.len(),
            n
        ));
    }
    if worker_id >= n_workers.max(1) {
        return Err(format!("worker_id {worker_id} >= n_workers {n_workers}"));
    }
    let ops = circuit_to_gateops(circuit)?;
    let net = build_amplitude_network(n, &ops, bitstring);
    let (path, sliced) = select_sliced_path(&net, opt, max_width, max_slices);
    let n_configs = 1u64 << sliced.len();
    let nw = n_workers.max(1);
    // contiguous chunk [start, end) for this worker.
    let chunk = n_configs.div_ceil(nw);
    let start = (worker_id * chunk).min(n_configs);
    let end = (start + chunk).min(n_configs);
    if start >= end {
        return Ok(Complex64::new(0.0, 0.0));
    }
    // 부분합에도 위상을 곱해 둔다 — aggregator 는 worker 결과를 단순 합산
    // 하므로 (위상은 공통 인자) 전체 진폭에 e^{iλ} 가 정확히 한 번 반영된다.
    Ok(
        qsim_tensornet::slicing::contract_sliced_amplitude_range(&net, &path, &sliced, start, end)
            * global_phase_factor(circuit),
    )
}

/// GPU (wgpu) matmul provider — TN contraction 의 matmul 을 GPU 로 offload.
/// f32 정밀도 (wgpu storage 한계).  작은 matmul 은 GPU 오버헤드가 커 CPU 가
/// 빠르므로 임계 이상에서만 GPU 호출.
struct GpuMatmul {
    backend: std::sync::Arc<qsim_gpu::WgpuMatmulBackend>,
    cpu: qsim_tensornet::CpuMatmul,
}

impl MatmulProvider for GpuMatmul {
    fn matmul(
        &self,
        m: usize,
        k: usize,
        n: usize,
        a: &[Complex64],
        b: &[Complex64],
    ) -> Vec<Complex64> {
        // 작은 contraction 은 CPU (GPU 업로드/디스패치 오버헤드 회피).
        if (m * n).max(k) < 1024 {
            self.cpu.matmul(m, k, n, a, b)
        } else {
            self.backend.matmul(m, k, n, a, b)
        }
    }
}

/// statevector 를 GPU (wgpu) contraction 으로 계산 (f32 정밀도).  GPU adapter 가
/// 없으면 `Err`.  결과는 panta 컨벤션 (qubit 0 = LSB).
pub fn run_statevector_gpu(
    circuit: &Circuit,
    opt: PathOptimizer,
) -> Result<StateVector<f64>, String> {
    let backend = qsim_gpu::cached_wgpu_matmul_backend().map_err(|e| format!("{e}"))?;
    let provider = GpuMatmul {
        backend,
        cpu: qsim_tensornet::CpuMatmul,
    };
    let n = circuit.num_qubits();
    let ops = circuit_to_gateops(circuit)?;
    let net = build_statevector_network(n, &ops);
    let path = find_path(&net, opt);
    let result = contract_ssa_with(&net.tensors, &path, &provider);
    let perm: Vec<usize> = net
        .open_indices
        .iter()
        .map(|idx| result.indices.iter().position(|x| x == idx).unwrap())
        .collect();
    let tn_data = result.permute(&perm).data;
    let mut sv = StateVector::<f64>::new(n);
    let phase = global_phase_factor(circuit);
    let amps = sv.amplitudes_mut();
    for (i, slot) in amps.iter_mut().enumerate() {
        *slot = tn_data[bitrev(i, n)] * phase;
    }
    Ok(sv)
}

/// amplitude 를 GPU (wgpu) contraction 으로 계산 (f32 정밀도).
pub fn run_amplitude_gpu(
    circuit: &Circuit,
    bitstring: &[u8],
    opt: PathOptimizer,
) -> Result<Complex64, String> {
    let backend = qsim_gpu::cached_wgpu_matmul_backend().map_err(|e| format!("{e}"))?;
    let provider = GpuMatmul {
        backend,
        cpu: qsim_tensornet::CpuMatmul,
    };
    let n = circuit.num_qubits();
    if bitstring.len() != n {
        return Err(format!(
            "tensornet amplitude: bitstring 길이 {} != n_qubits {}",
            bitstring.len(),
            n
        ));
    }
    let ops = circuit_to_gateops(circuit)?;
    let net = build_amplitude_network(n, &ops, bitstring);
    let path = find_path(&net, opt);
    let result = contract_ssa_with(&net.tensors, &path, &provider);
    Ok(result.data[0] * global_phase_factor(circuit))
}

/// GateOp 의 conjugate transpose (C† 게이트).
fn dagger_op(op: &GateOp) -> GateOp {
    let k = op.qubits.len();
    let dim = 1usize << k;
    let mut m = vec![Complex64::new(0.0, 0.0); dim * dim];
    for r in 0..dim {
        for c in 0..dim {
            m[c * dim + r] = op.matrix[r * dim + c].conj();
        }
    }
    GateOp::new(m, op.qubits.clone())
}

/// Pauli 문자열 → 1-큐비트 Pauli GateOp 들.  `pauli[n-1-q]` = 큐비트 `q` (Qiskit
/// 라벨 컨벤션: 오른쪽 끝 문자 = 큐비트 0).
fn pauli_ops(pauli: &str, n: usize) -> Result<Vec<GateOp>, String> {
    if pauli.len() != n {
        return Err(format!(
            "Pauli string 길이 {} != n_qubits {}",
            pauli.len(),
            n
        ));
    }
    let i = Complex64::new(0.0, 0.0);
    let one = Complex64::new(1.0, 0.0);
    let mut ops = Vec::new();
    for (pos, ch) in pauli.chars().enumerate() {
        let q = n - 1 - pos; // 오른쪽 끝 = 큐비트 0.
        let m = match ch {
            'I' | 'i' => continue,
            'X' | 'x' => vec![i, one, one, i],
            'Y' | 'y' => vec![i, Complex64::new(0.0, -1.0), Complex64::new(0.0, 1.0), i],
            'Z' | 'z' => vec![one, i, i, Complex64::new(-1.0, 0.0)],
            other => return Err(format!("알 수 없는 Pauli 문자 '{other}'")),
        };
        ops.push(GateOp::new(m, vec![q]));
    }
    Ok(ops)
}

/// Pauli-sum observable 의 기댓값 `⟨0|C† H C|0⟩ = Σ_i c_i ⟨0|C† P_i C|0⟩` 를
/// tensor network contraction 으로 계산한다.  각 항은 `C + P_i + C†` 회로의
/// amplitude(0…0) 와 같다 — deep 회로에서도 dense statevector 없이 계산.
pub fn run_expectation(
    circuit: &Circuit,
    terms: &[(String, Complex64)],
    opt: PathOptimizer,
) -> Result<Complex64, String> {
    let n = circuit.num_qubits();
    let ops_c = circuit_to_gateops(circuit)?;
    let ops_cdag: Vec<GateOp> = ops_c.iter().rev().map(dagger_op).collect();
    let zero = vec![0u8; n];
    let mut acc = Complex64::new(0.0, 0.0);
    for (pauli, coeff) in terms {
        let p_ops = pauli_ops(pauli, n)?;
        let mut all = ops_c.clone();
        all.extend(p_ops);
        all.extend(ops_cdag.iter().cloned());
        let net = build_amplitude_network(n, &all, &zero);
        let path = find_path(&net, opt);
        let amp = contract_ssa(&net.tensors, &path);
        acc += *coeff * amp.data[0];
    }
    Ok(acc)
}

/// contraction 비용 추정 `(log10_flops, log2_width)` — **amplitude 네트워크**
/// (all-zero bitstring, closed) 기준.  `log2_width` = peak 중간 텐서의 큐비트 수
/// (메모리 ≈ `2^width` 복소수).  amplitude / expectation contraction 의 실제
/// 비용을 반영한다 (statevector 네트워크는 출력 open leg 때문에 width ≥ N 으로
/// 항상 큼 → 부적절).
pub fn contraction_cost(circuit: &Circuit, opt: PathOptimizer) -> Result<(f64, f64), String> {
    let n = circuit.num_qubits();
    let ops = circuit_to_gateops(circuit)?;
    let zero = vec![0u8; n];
    let net = build_amplitude_network(n, &ops, &zero);
    let path = find_path(&net, opt);
    let dims = dims_of(&net);
    let ti: Vec<Vec<usize>> = net.tensors.iter().map(|t| t.indices.clone()).collect();
    let cost = estimate_cost(&ti, &dims, &path);
    Ok((cost.log10_flops, cost.log2_width))
}

/// 작은 N 에서 statevector 로부터 sampling (counts).  큰 N 의 conditional-
/// amplitude sampling 은 후속 단계.
pub fn run_sample(
    circuit: &Circuit,
    shots: usize,
    seed: Option<u64>,
    opt: PathOptimizer,
) -> Result<HashMap<String, usize>, String> {
    let n = circuit.num_qubits();
    let sv = run_statevector(circuit, opt)?;
    let amps = sv.amplitudes();

    // trailing 부분측정의 qubit→cbit 매핑 (statevector 백엔드의
    // `sample_with_cbit_map` 과 동일 시맨틱).  MeasureAll 또는 명시적 측정이
    // 없으면 전체 큐비트 비트열을 그대로 낸다 (기존 동작).
    let mut cbit_map: Vec<(usize, usize)> = Vec::new(); // (qubit, cbit)
    let mut has_measure_all = false;
    for inst in circuit.instructions() {
        match inst {
            Instruction::Measure { qubit, cbit } => cbit_map.push((*qubit, *cbit)),
            Instruction::MeasureAll => has_measure_all = true,
            _ => {}
        }
    }
    let use_cbit_map = !has_measure_all && !cbit_map.is_empty();
    let n_cbits = circuit.num_cbits();
    let mut cbit_to_qubit: Vec<Option<usize>> = vec![None; n_cbits];
    for (q, c) in &cbit_map {
        if *c < n_cbits {
            cbit_to_qubit[*c] = Some(*q);
        }
    }

    // CDF.
    let probs: Vec<f64> = amps.iter().map(|a| a.norm_sqr()).collect();
    let total: f64 = probs.iter().sum();
    let mut rng = match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_entropy(),
    };
    let mut counts: HashMap<String, usize> = HashMap::new();
    for _ in 0..shots {
        let r = rng.gen::<f64>() * total;
        let mut acc = 0.0;
        let mut idx = probs.len() - 1;
        for (i, &p) in probs.iter().enumerate() {
            acc += p;
            if r <= acc {
                idx = i;
                break;
            }
        }
        let s = if use_cbit_map {
            // creg 폭 비트열 (cbit n_cbits-1 … 0, Qiskit 표기).
            let mut s = String::with_capacity(n_cbits);
            for c in (0..n_cbits).rev() {
                let bit = cbit_to_qubit[c].map(|q| (idx >> q) & 1).unwrap_or(0);
                s.push(if bit == 1 { '1' } else { '0' });
            }
            s
        } else {
            // panta idx (qubit 0 = LSB) → bitstring (큐비트 n-1 … 0, Qiskit 표기).
            let mut s = String::with_capacity(n);
            for q in (0..n).rev() {
                s.push(if (idx >> q) & 1 == 1 { '1' } else { '0' });
            }
            s
        };
        *counts.entry(s).or_insert(0) += 1;
    }
    Ok(counts)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{Backend, ExecutionEngine, Precision};

    /// 회귀: TN contraction 이 `Circuit::global_phase` 를 떨어뜨리던 버그.
    #[test]
    fn tensornet_preserves_global_phase() {
        let mut c = Circuit::new(2);
        c.h(0);
        c.cx(0, 1);
        c.set_global_phase(1.234);
        let tn = run_statevector(&c, PathOptimizer::Greedy).unwrap();
        let amp = run_amplitude(&c, &[0, 0], PathOptimizer::Greedy).unwrap();
        let expected = Complex64::from_polar(1.0 / std::f64::consts::SQRT_2, 1.234);
        assert!(
            (tn.amplitudes()[0] - expected).norm() < 1e-12,
            "statevector 전역 위상 소실: {:?}",
            tn.amplitudes()[0]
        );
        assert!(
            (amp - expected).norm() < 1e-12,
            "amplitude 전역 위상 소실: {amp:?}"
        );
    }

    /// 회귀: TN 이 mid-circuit 측정을 조용히 무시하고 잘못된 분포를 내던 버그
    /// — 이제 명시적으로 거부한다.
    #[test]
    fn tensornet_rejects_mid_circuit_measure() {
        let mut c = Circuit::new(1);
        c.h(0);
        c.measure(0, 0);
        c.h(0);
        assert!(circuit_to_gateops(&c).is_err());
    }

    /// trailing 부분측정의 counts 가 statevector 백엔드처럼 creg 폭으로
    /// (qubit→cbit 매핑) 나오는지.
    #[test]
    fn tensornet_sample_uses_cbit_map() {
        let mut c = Circuit::new(2);
        c.x(1);
        c.measure(1, 0);
        let counts = run_sample(&c, 50, Some(1), PathOptimizer::Greedy).unwrap();
        assert_eq!(counts.len(), 1);
        assert_eq!(counts.get("1"), Some(&50), "cbit 매핑 미적용: {counts:?}");
    }

    /// 랜덤 회로에서 tensornet statevector == CPU statevector (deep 회로 포함).
    #[test]
    fn tensornet_matches_statevector_random() {
        use rand::{Rng, SeedableRng};
        let mut rng = rand::rngs::StdRng::seed_from_u64(7);
        for trial in 0..8 {
            let n = 4 + (trial % 3); // 4..6 큐비트
            let mut circuit = Circuit::new(n);
            // deep random 회로 (depth ~12) — high entanglement.
            for _ in 0..12 {
                for q in 0..n {
                    match rng.gen_range(0..3) {
                        0 => circuit.h(q),
                        1 => circuit.t(q),
                        _ => circuit.rx(rng.gen_range(0.0..std::f64::consts::TAU), q),
                    }
                }
                for q in 0..n - 1 {
                    if rng.gen::<bool>() {
                        circuit.cx(q, q + 1);
                    }
                }
            }
            let cpu = ExecutionEngine::new()
                .with_backend(Backend::CpuStatevector)
                .with_precision(Precision::F64)
                .run(&circuit, 0);
            let cpu_sv = cpu.statevector();
            let tn_sv = run_statevector(&circuit, PathOptimizer::Greedy).unwrap();
            for (a, b) in cpu_sv.amplitudes().iter().zip(tn_sv.amplitudes().iter()) {
                assert!(
                    (a - b).norm() < 1e-10,
                    "trial {trial}: TN != CPU statevector"
                );
            }
            // amplitude 도 일치 (basis state idx=3, panta LSB).
            let idx = 3usize.min((1usize << n) - 1);
            let bits: Vec<u8> = (0..n).map(|q| ((idx >> q) & 1) as u8).collect();
            let amp = run_amplitude(&circuit, &bits, PathOptimizer::Greedy).unwrap();
            assert!((amp - cpu_sv.amplitudes()[idx]).norm() < 1e-10);
        }
    }

    /// expectation ⟨ψ|H|ψ⟩ (TN) == statevector 기댓값.
    #[test]
    fn tensornet_expectation_matches_statevector() {
        use num_complex::Complex64 as C;
        let mut circuit = Circuit::new(3);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.rx(0.7, 2);
        circuit.cx(1, 2);
        // H = 1.0*ZZI + 0.5*XXX - 0.3*IIZ  (Qiskit 라벨: 오른쪽 = 큐비트 0).
        let terms = vec![
            ("ZZI".to_string(), C::new(1.0, 0.0)),
            ("XXX".to_string(), C::new(0.5, 0.0)),
            ("IIZ".to_string(), C::new(-0.3, 0.0)),
        ];
        let tn = run_expectation(&circuit, &terms, PathOptimizer::Greedy).unwrap();
        // statevector 레퍼런스: ⟨ψ|P|ψ⟩ 직접 계산.
        let cpu = ExecutionEngine::new()
            .with_backend(Backend::CpuStatevector)
            .with_precision(Precision::F64)
            .run(&circuit, 0);
        let sv = cpu.statevector().amplitudes().to_vec();
        let mut expect = C::new(0.0, 0.0);
        for (pauli, coeff) in &terms {
            // ⟨ψ|P|ψ⟩ = Σ_x conj(ψ_x) (P ψ)_x.
            let mut val = C::new(0.0, 0.0);
            for (x, &amp) in sv.iter().enumerate() {
                // P|x⟩ = phase · |x'⟩.
                let (mut xp, mut phase) = (x, C::new(1.0, 0.0));
                for (pos, ch) in pauli.chars().enumerate() {
                    let q = 3 - 1 - pos;
                    let bit = (x >> q) & 1;
                    match ch {
                        'X' => xp ^= 1 << q,
                        'Y' => {
                            xp ^= 1 << q;
                            phase *= if bit == 0 {
                                C::new(0.0, 1.0)
                            } else {
                                C::new(0.0, -1.0)
                            };
                        }
                        'Z' if bit == 1 => {
                            phase *= C::new(-1.0, 0.0);
                        }
                        _ => {}
                    }
                }
                val += sv[xp].conj() * phase * amp;
            }
            expect += *coeff * val;
        }
        assert!(
            (tn - expect).norm() < 1e-10,
            "TN expect {tn} vs ref {expect}"
        );
    }

    /// 분산 슬라이싱: worker 부분합 Σ == 단일-shot sliced amplitude == statevector.
    #[test]
    fn tensornet_distributed_workers_sum_to_full() {
        use rand::{Rng, SeedableRng};
        let mut rng = rand::rngs::StdRng::seed_from_u64(13);
        // 4x4 2D grid (검증 가능 크기).
        let n = 16;
        let cols = 4;
        let mut circuit = Circuit::new(n);
        let qid = |r: usize, c: usize| r * cols + c;
        for d in 0..4 {
            for q in 0..n {
                circuit.rx(rng.gen_range(0.0..std::f64::consts::TAU), q);
                circuit.rz(rng.gen_range(0.0..std::f64::consts::TAU), q);
            }
            if d % 2 == 0 {
                for r in 0..4 {
                    for c in 0..cols - 1 {
                        circuit.cx(qid(r, c), qid(r, c + 1));
                    }
                }
            } else {
                for c in 0..cols {
                    for r in 0..3 {
                        circuit.cx(qid(r, c), qid(r + 1, c));
                    }
                }
            }
        }
        let cpu = ExecutionEngine::new()
            .with_backend(Backend::CpuStatevector)
            .with_precision(Precision::F64)
            .run(&circuit, 0);
        let sv = cpu.statevector().amplitudes().to_vec();
        let idx = 0xACEDusize & ((1 << n) - 1);
        let bits: Vec<u8> = (0..n).map(|q| ((idx >> q) & 1) as u8).collect();
        let opt = PathOptimizer::Partition { trials: 4, seed: 1 };
        // 강제 slicing (작은 width) → 여러 slice, 여러 worker 로 분배.
        let n_workers = 5u64;
        let mut acc = Complex64::new(0.0, 0.0);
        for w in 0..n_workers {
            acc += run_amplitude_worker(&circuit, &bits, opt, 8.0, 20, n_workers, w).unwrap();
        }
        assert!(
            (acc - sv[idx]).norm() < 1e-9,
            "distributed Σ {acc} != statevector {}",
            sv[idx]
        );
    }

    /// GPU (wgpu) contraction == CPU statevector (f32 tol).  adapter 없으면 skip.
    #[test]
    fn tensornet_gpu_matches_statevector() {
        if qsim_gpu::cached_wgpu_matmul_backend().is_err() {
            eprintln!("no GPU adapter — skipping tensornet GPU test");
            return;
        }
        use rand::{Rng, SeedableRng};
        let mut rng = rand::rngs::StdRng::seed_from_u64(5);
        let n = 6;
        let mut circuit = Circuit::new(n);
        for _ in 0..10 {
            for q in 0..n {
                if rng.gen::<bool>() {
                    circuit.h(q);
                } else {
                    circuit.rx(rng.gen_range(0.0..std::f64::consts::TAU), q);
                }
            }
            for q in 0..n - 1 {
                circuit.cx(q, q + 1);
            }
        }
        let cpu = ExecutionEngine::new()
            .with_backend(Backend::CpuStatevector)
            .with_precision(Precision::F64)
            .run(&circuit, 0);
        let cpu_sv = cpu.statevector();
        let gpu_sv = run_statevector_gpu(&circuit, PathOptimizer::Greedy).unwrap();
        for (a, b) in cpu_sv.amplitudes().iter().zip(gpu_sv.amplitudes().iter()) {
            assert!((a - b).norm() < 1e-4, "GPU TN != CPU statevector (f32)");
        }
    }
}
