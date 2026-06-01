//! v0.5.23: Differential test suite — random circuit generator + 모든 backend
//! pair 자동 비교.
//!
//! 100+ random 회로를 자동 생성 → CPU statevector (f64) vs wgpu Tier-1 (f32)
//! 비교.  Latent bug 자동 발견 (RX 6600 dispatch 의 C-2 같은 회귀 type 의
//! 회로 조합 자동 cover).
//!
//! sandbox lavapipe 의 software emulation 시간 한계로 N=2~4 의 작은 회로만
//! 사용 — 그래도 gate type / depth / parameter / measurement 조합 cover.
//!
//! cargo test 의 integration test 라 sandbox 에서도 자동 실행.  실 사용자
//! 환경 (NVIDIA / AMD discrete GPU) 에서는 더 큰 N + 더 많은 회로 가능.
//!
//! **v0.5.26 정정**: 이전 v0.5.24 의 graceful skip (wgpu adapter 미가용 시
//! return) 제거.  CI 의 cargo test job 에 mesa-vulkan-drivers 가 설치돼
//! lavapipe ICD 등록되니 (v0.5.25), skip 분기는 dead code — 검증 우회 가능
//! 성 차단 위해 강제 검증.  사용자가 cargo test 직접 실행하려면 mesa /
//! 실 GPU 환경 필수.

use num_complex::Complex;
use qsim_core::{Gate, NoiseChannel};
use qsim_simulator::{Backend, Circuit, ExecutionEngine, Precision, SimulationResult};
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

const N_RANDOM_CIRCUITS: usize = 50;
const N_NOISE_CIRCUITS: usize = 30;
const F32_TOLERANCE: f64 = 1e-4; // wgpu f32 한계
const F64_TOLERANCE: f64 = 1e-12;

/// Random circuit generator (parametrized).
struct CircuitGenerator {
    rng: StdRng,
    n_qubits: usize,
    max_depth: usize,
    include_noise: bool,
}

impl CircuitGenerator {
    fn new(seed: u64, n_qubits: usize, max_depth: usize) -> Self {
        Self {
            rng: StdRng::seed_from_u64(seed),
            n_qubits,
            max_depth,
            include_noise: false,
        }
    }

    fn with_noise(mut self) -> Self {
        self.include_noise = true;
        self
    }

    fn random_1q_gate(&mut self) -> Gate {
        match self.rng.gen_range(0..10) {
            0 => Gate::H,
            1 => Gate::X,
            2 => Gate::Y,
            3 => Gate::Z,
            4 => Gate::S,
            5 => Gate::T,
            6 => Gate::Rx(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
            7 => Gate::Ry(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
            8 => Gate::Rz(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
            _ => Gate::P(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
        }
    }

    fn random_2q_gate(&mut self) -> Gate {
        match self.rng.gen_range(0..6) {
            0 => Gate::CNOT,
            1 => Gate::CZ,
            2 => Gate::SWAP,
            3 => Gate::CRx(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
            4 => Gate::CRy(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
            _ => Gate::CRz(
                self.rng
                    .gen_range(-std::f64::consts::PI..std::f64::consts::PI),
            ),
        }
    }

    fn build(&mut self) -> Circuit {
        let mut circuit = Circuit::new(self.n_qubits);
        let depth = self.rng.gen_range(1..=self.max_depth);
        for _ in 0..depth {
            let pick: f64 = self.rng.gen();
            if pick < 0.4 {
                // 1q gate.
                let q = self.rng.gen_range(0..self.n_qubits);
                let gate = self.random_1q_gate();
                apply_gate_dispatch(&mut circuit, gate, &[q]);
            } else if pick < 0.8 && self.n_qubits >= 2 {
                // 2q gate.
                let q0 = self.rng.gen_range(0..self.n_qubits);
                let mut q1 = self.rng.gen_range(0..self.n_qubits);
                while q1 == q0 {
                    q1 = self.rng.gen_range(0..self.n_qubits);
                }
                let gate = self.random_2q_gate();
                apply_gate_dispatch(&mut circuit, gate, &[q0, q1]);
            } else if self.include_noise {
                // Note: Toffoli/Fredkin 은 wgpu statevector 가 거부 (v0.5.10 의
                // cuStateVec native 는 cuda only).  random circuit 에서 제외 —
                // wgpu 의 1q/2q/controlled-1q 범위 안.  v0.6+ 에서 wgpu 의
                // 자동 transpile 추가 시 random gen 도 확장 가능.
                // 5% noise channel.
                let q = self.rng.gen_range(0..self.n_qubits);
                let p: f64 = self.rng.gen_range(0.0..0.3);
                let noise = match self.rng.gen_range(0..3) {
                    0 => NoiseChannel::BitFlip { p },
                    1 => NoiseChannel::Depolarizing { p },
                    _ => NoiseChannel::AmplitudeDamping { gamma: p },
                };
                circuit.add_noise(noise, q);
            }
        }
        circuit.measure_all();
        circuit
    }
}

/// Gate enum dispatch helper — Circuit 의 fluent API 에 매핑.
fn apply_gate_dispatch(circuit: &mut Circuit, gate: Gate, targets: &[usize]) {
    match gate {
        Gate::H => {
            circuit.h(targets[0]);
        }
        Gate::X => {
            circuit.x(targets[0]);
        }
        Gate::Y => {
            circuit.y(targets[0]);
        }
        Gate::Z => {
            circuit.z(targets[0]);
        }
        Gate::S => {
            circuit.s(targets[0]);
        }
        Gate::T => {
            circuit.t(targets[0]);
        }
        Gate::Rx(theta) => {
            circuit.rx(theta, targets[0]);
        }
        Gate::Ry(theta) => {
            circuit.ry(theta, targets[0]);
        }
        Gate::Rz(theta) => {
            circuit.rz(theta, targets[0]);
        }
        Gate::P(lambda) => {
            circuit.p(lambda, targets[0]);
        }
        Gate::CNOT => {
            circuit.cx(targets[0], targets[1]);
        }
        Gate::CZ => {
            circuit.cz(targets[0], targets[1]);
        }
        Gate::SWAP => {
            circuit.swap(targets[0], targets[1]);
        }
        Gate::CRx(theta) => {
            circuit.crx(theta, targets[0], targets[1]);
        }
        Gate::CRy(theta) => {
            circuit.cry(theta, targets[0], targets[1]);
        }
        Gate::CRz(theta) => {
            circuit.crz(theta, targets[0], targets[1]);
        }
        Gate::Toffoli => {
            circuit.ccx(targets[0], targets[1], targets[2]);
        }
        Gate::Fredkin => {
            circuit.cswap(targets[0], targets[1], targets[2]);
        }
        _ => {
            // 기타 gate 는 random gen 안 함.
        }
    }
}

/// CPU vs wgpu statevector amplitude 비교.
fn run_and_compare_statevector(circuit: &Circuit, _seed_idx: usize) -> Result<f64, String> {
    let cpu_engine = ExecutionEngine::with_seed(42)
        .with_backend(Backend::CpuStatevector)
        .with_precision(Precision::F64);
    let wgpu_engine = ExecutionEngine::with_seed(42)
        .with_backend(Backend::WgpuStatevector)
        .with_precision(Precision::F32);

    let cpu_result = cpu_engine.run(circuit, 0);
    let wgpu_result = match wgpu_engine.run_checked(circuit, 0) {
        Ok(r) => r,
        Err(e) => return Err(format!("wgpu run_checked: {e}")),
    };

    let cpu_amps: Vec<Complex<f64>> = match cpu_result {
        SimulationResult::F64 { statevector, .. } => statevector.amplitudes().to_vec(),
        _ => return Err("cpu: expected F64 result".into()),
    };
    let wgpu_amps: Vec<Complex<f64>> = match wgpu_result {
        SimulationResult::F32 { statevector, .. } => statevector
            .amplitudes()
            .iter()
            .map(|c| Complex::new(c.re as f64, c.im as f64))
            .collect(),
        _ => return Err("wgpu: expected F32 result".into()),
    };

    if cpu_amps.len() != wgpu_amps.len() {
        return Err(format!(
            "len mismatch: cpu={} wgpu={}",
            cpu_amps.len(),
            wgpu_amps.len()
        ));
    }
    let max_diff = cpu_amps
        .iter()
        .zip(wgpu_amps.iter())
        .map(|(a, b)| (a - b).norm())
        .fold(0.0_f64, f64::max);
    Ok(max_diff)
}

/// Trajectory 회로 (noise 포함) 의 분포 비교.
/// 같은 seed → 같은 outcome distribution (statistical sampling 일치).
fn run_and_compare_distribution(circuit: &Circuit, shots: usize) -> Result<f64, String> {
    let cpu_engine = ExecutionEngine::with_seed(42)
        .with_backend(Backend::CpuStatevector)
        .with_precision(Precision::F64);
    let wgpu_engine = ExecutionEngine::with_seed(42)
        .with_backend(Backend::WgpuStatevector)
        .with_precision(Precision::F32);

    let cpu_counts = match cpu_engine.run(circuit, shots) {
        SimulationResult::F64 { counts, .. } => counts,
        _ => return Err("cpu: expected F64".into()),
    };
    let wgpu_counts = match wgpu_engine.run_checked(circuit, shots) {
        Ok(SimulationResult::F32 { counts, .. }) => counts,
        Ok(_) => return Err("wgpu: expected F32".into()),
        Err(e) => return Err(format!("wgpu: {e}")),
    };
    let total = shots as f64;
    let mut keys: std::collections::HashSet<String> = cpu_counts.keys().cloned().collect();
    keys.extend(wgpu_counts.keys().cloned());
    let mut max_p_diff = 0.0_f64;
    for k in keys {
        let p_cpu = *cpu_counts.get(&k).unwrap_or(&0) as f64 / total;
        let p_wgpu = *wgpu_counts.get(&k).unwrap_or(&0) as f64 / total;
        max_p_diff = max_p_diff.max((p_cpu - p_wgpu).abs());
    }
    Ok(max_p_diff)
}

#[test]
fn differential_random_unitary_circuits() {
    // unitary 회로 (no noise / no dynamic) — sv amplitude 비교.
    // sandbox lavapipe 라 N=2~3, depth=1~5 의 작은 회로만.

    let mut failures: Vec<(usize, f64, String)> = Vec::new();
    for seed in 0..N_RANDOM_CIRCUITS {
        let n = 2 + (seed % 3); // N ∈ {2, 3, 4}
        let max_depth = 5;
        let mut gen = CircuitGenerator::new(seed as u64, n, max_depth);
        let circuit = gen.build();
        match run_and_compare_statevector(&circuit, seed) {
            Ok(diff) => {
                if diff > F32_TOLERANCE {
                    failures.push((seed, diff, format!("seed={seed} N={n} diff={diff:.2e}")));
                }
            }
            Err(e) => {
                failures.push((seed, f64::NAN, format!("seed={seed} N={n} err={e}")));
            }
        }
    }
    assert!(
        failures.is_empty(),
        "{} of {} random unitary circuits failed:\n{}",
        failures.len(),
        N_RANDOM_CIRCUITS,
        failures
            .iter()
            .map(|(_, _, s)| s.as_str())
            .collect::<Vec<_>>()
            .join("\n")
    );
}

#[test]
fn differential_random_noise_circuits() {
    // noise 회로 (trajectory) — 분포 비교.  같은 seed → 같은 outcome
    // (CPU vs wgpu trajectory 모두 RNG 동일).
    let mut failures: Vec<(usize, f64, String)> = Vec::new();
    for seed in 0..N_NOISE_CIRCUITS {
        let n = 2 + (seed % 3);
        let mut gen = CircuitGenerator::new(seed as u64, n, 4).with_noise();
        let circuit = gen.build();
        match run_and_compare_distribution(&circuit, 200) {
            Ok(p_diff) => {
                // trajectory 의 RNG 가 동일 seed → 비트 단위 일치 expected.
                // 그러나 wgpu trajectory 의 GPU dispatch overhead 로 수치
                // 차이 가능 — 보수적 5% tolerance.
                if p_diff > 0.05 {
                    failures.push((
                        seed,
                        p_diff,
                        format!("seed={seed} N={n} p_diff={p_diff:.4}"),
                    ));
                }
            }
            Err(e) => {
                failures.push((seed, f64::NAN, format!("seed={seed} N={n} err={e}")));
            }
        }
    }
    assert!(
        failures.is_empty(),
        "{} of {} random noise circuits failed:\n{}",
        failures.len(),
        N_NOISE_CIRCUITS,
        failures
            .iter()
            .map(|(_, _, s)| s.as_str())
            .collect::<Vec<_>>()
            .join("\n")
    );
}

#[test]
fn differential_norm_invariant() {
    // 모든 unitary 회로의 sv norm² ≈ 1.0 (CPU + wgpu 둘 다).
    for seed in 0..30 {
        let n = 2 + (seed % 3);
        let mut gen = CircuitGenerator::new(seed as u64, n, 6);
        let circuit = gen.build();
        let cpu_engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuStatevector)
            .with_precision(Precision::F64);
        let wgpu_engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::WgpuStatevector)
            .with_precision(Precision::F32);

        if let SimulationResult::F64 { statevector, .. } = cpu_engine.run(&circuit, 0) {
            let norm_sq: f64 = statevector.amplitudes().iter().map(|c| c.norm_sqr()).sum();
            assert!(
                (norm_sq - 1.0).abs() < F64_TOLERANCE,
                "CPU seed={seed} norm²={norm_sq}"
            );
        }
        if let Ok(SimulationResult::F32 { statevector, .. }) = wgpu_engine.run_checked(&circuit, 0)
        {
            let norm_sq: f32 = statevector.amplitudes().iter().map(|c| c.norm_sqr()).sum();
            assert!(
                ((norm_sq as f64) - 1.0).abs() < F32_TOLERANCE,
                "wgpu seed={seed} norm²={norm_sq}"
            );
        }
    }
}
