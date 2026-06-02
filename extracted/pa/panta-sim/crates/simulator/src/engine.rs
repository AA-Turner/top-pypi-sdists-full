use std::sync::Arc;

use num_complex::Complex;
use qsim_core::complex::Real;
use qsim_core::operations::{
    apply_controlled_gate, apply_controlled_swap, apply_doubly_controlled_gate,
    apply_multi_qubit_gate, apply_single_qubit_gate, apply_two_qubit_gate,
};
use qsim_core::{DensityMatrix, Gate, StateVector};
use qsim_gpu::wgpu_backend::{WgpuDensityOp, WgpuGateOp};
use qsim_gpu::{GpuError, GpuMpsTensors, GpuSvdOutput, GpuSvdProvider, GPU_CHI_THRESHOLD};
use rand::rngs::StdRng;
use rand::Rng;
use rand::SeedableRng;

use crate::circuit::{body_has_measure, Circuit};
use crate::instruction::Instruction;
use crate::measurement;
use crate::result::{Backend, Precision, SimulationResult};

/// MPS 백엔드의 default χ_max — Qiskit Aer (`max_bond_dimension=64`),
/// MIMIQ default 와 동일.  사용자가 [`ExecutionEngine::with_mps_bond_dim`]
/// 으로 override 가능.
pub const DEFAULT_MPS_MAX_BOND_DIM: usize = 64;

/// v0.6.8: arbitrary unitary (`Instruction::ApplyUnitary`) 는 현재
/// statevector 백엔드 (CPU / trajectory) 에서만 지원된다.  density / MPS /
/// GPU 경로에 도달하면 이 메시지로 panic — Python binding 이 사전 검증으로
/// 친화 ValueError 를 던지므로 정상 사용에선 도달하지 않는다.
const UNITARY_UNSUPPORTED_MSG: &str =
    "arbitrary unitary (qc.unitary) 는 현재 method='statevector' (CPU) 에서만 \
     지원됩니다 — density_matrix / mps / wgpu / cuda 백엔드는 미지원";

/// 회로 실행 엔진.
pub struct ExecutionEngine {
    seed: Option<u64>,
    precision: Precision,
    backend: Backend,
    max_bond_dim: usize,
    /// MPS 백엔드의 singular-value cutoff (v0.6.5).  `0.0` (default) =
    /// disabled — `max_bond_dim` 만으로 truncation.  > 0 일 때 adaptive
    /// bond dim 활성화 (`s_i < eps` 인 mode 추가 drop).
    mps_trunc_threshold: f64,
}

impl ExecutionEngine {
    pub fn new() -> Self {
        Self {
            seed: None,
            precision: Precision::default(),
            backend: Backend::default(),
            max_bond_dim: DEFAULT_MPS_MAX_BOND_DIM,
            mps_trunc_threshold: 0.0,
        }
    }

    /// 재현 가능한 결과를 위한 시드 설정.
    pub fn with_seed(seed: u64) -> Self {
        Self {
            seed: Some(seed),
            precision: Precision::default(),
            backend: Backend::default(),
            max_bond_dim: DEFAULT_MPS_MAX_BOND_DIM,
            mps_trunc_threshold: 0.0,
        }
    }

    /// 정밀도를 설정한 새 엔진 반환 (builder 패턴).
    pub fn with_precision(mut self, precision: Precision) -> Self {
        self.precision = precision;
        self
    }

    /// 백엔드를 설정한 새 엔진 반환 (v0.5.0 builder 패턴).
    pub fn with_backend(mut self, backend: Backend) -> Self {
        self.backend = backend;
        self
    }

    /// MPS 백엔드의 χ_max 를 설정한다 (v0.6.0).  비-MPS 백엔드에서는 무시됨.
    /// `max_bond_dim == 0` 이면 panic.
    pub fn with_mps_bond_dim(mut self, max_bond_dim: usize) -> Self {
        assert!(max_bond_dim >= 1, "max_bond_dim must be >= 1");
        self.max_bond_dim = max_bond_dim;
        self
    }

    /// MPS 백엔드의 singular-value cutoff `trunc_threshold` 를 설정 (v0.6.5).
    /// `0.0` (default) → disabled (`max_bond_dim` 만 사용).  > 0 → adaptive
    /// truncation: SVD 뒤 `s_i < eps` 인 mode 도 drop (둘 중 더 strict).
    /// Schollwöck 2011 §4.5.3.  비-MPS 백엔드에서는 무시됨.  음수 / NaN 은 panic.
    pub fn with_mps_trunc_threshold(mut self, eps: f64) -> Self {
        assert!(
            eps.is_finite() && eps >= 0.0,
            "mps_trunc_threshold must be finite and >= 0.0 (got {eps})"
        );
        self.mps_trunc_threshold = eps;
        self
    }

    /// 회로를 실행하고 결과를 반환한다.  백엔드 / 정밀도에 따라 4 경로로 dispatch:
    /// (CpuStatevector, F64) / (CpuStatevector, F32) / (CpuDensity, F64) / (CpuDensity, F32).
    pub fn run(&self, circuit: &Circuit, shots: usize) -> SimulationResult {
        match (self.backend, self.precision) {
            (Backend::CpuStatevector, Precision::F64) => {
                let (counts, sv) = self.run_typed::<f64>(circuit, shots);
                SimulationResult::F64 {
                    counts,
                    statevector: sv,
                }
            }
            (Backend::CpuStatevector, Precision::F32) => {
                let (counts, sv) = self.run_typed::<f32>(circuit, shots);
                SimulationResult::F32 {
                    counts,
                    statevector: sv,
                }
            }
            (Backend::CpuDensity, Precision::F64) => {
                let (counts, rho) = self.run_typed_density::<f64>(circuit, shots);
                SimulationResult::DensityF64 {
                    counts,
                    density: rho,
                }
            }
            (Backend::CpuDensity, Precision::F32) => {
                let (counts, rho) = self.run_typed_density::<f32>(circuit, shots);
                SimulationResult::DensityF32 {
                    counts,
                    density: rho,
                }
            }
            (Backend::WgpuStatevector, _) => match self.run_wgpu_statevector(circuit, shots) {
                Ok((counts, sv)) => SimulationResult::F32 {
                    counts,
                    statevector: sv,
                },
                Err(e) => panic!("wgpu statevector backend 실패: {e}"),
            },
            (Backend::WgpuDensity, _) => {
                // 2q correlated custom Kraus (ApplyNoise2) 는 wgpu density shader
                // 미지원 (1q Kraus 만) — CPU density (apply_kraus_2q) 로 폴백해
                // 정확한 결과를 낸다.  wgpu_mps 가 noise 를 CPU trajectory 로
                // 폴백하는 것과 동일 관례 (panic 대신 정확한 결과).
                let has_2q_kraus = circuit
                    .instructions()
                    .iter()
                    .any(|i| matches!(i, Instruction::ApplyNoise2 { .. }));
                if has_2q_kraus {
                    let (counts, rho) = self.run_typed_density::<f32>(circuit, shots);
                    SimulationResult::DensityF32 {
                        counts,
                        density: rho,
                    }
                } else {
                    match self.run_wgpu_density(circuit, shots) {
                        Ok((counts, rho)) => SimulationResult::DensityF32 {
                            counts,
                            density: rho,
                        },
                        Err(e) => panic!("wgpu density backend 실패: {e}"),
                    }
                }
            }
            (Backend::CudaStatevector, Precision::F32) => {
                match self.run_cuda_statevector(circuit, shots) {
                    Ok((counts, sv)) => SimulationResult::F32 {
                        counts,
                        statevector: sv,
                    },
                    Err(e) => panic!("cuda statevector backend 실패: {e}"),
                }
            }
            (Backend::CudaStatevector, Precision::F64) => {
                // v0.5.12: cuStateVec f64 (CUDA_C_64F) path.
                match self.run_cuda_statevector_f64(circuit, shots) {
                    Ok((counts, sv)) => SimulationResult::F64 {
                        counts,
                        statevector: sv,
                    },
                    Err(e) => panic!("cuda statevector f64 backend 실패: {e}"),
                }
            }
            (Backend::CpuMps, Precision::F64) => {
                let (counts, sv, mps, final_norm_sq, truncation_error_sum, observed_max_bond_dim) =
                    self.run_mps_typed::<f64>(circuit, shots);
                SimulationResult::MpsF64 {
                    counts,
                    statevector: sv,
                    mps: mps.map(Arc::new),
                    max_bond_dim: self.max_bond_dim,
                    trunc_threshold: self.mps_trunc_threshold,
                    final_norm_sq,
                    truncation_error_sum,
                    observed_max_bond_dim,
                }
            }
            (Backend::CpuMps, Precision::F32) => {
                let (counts, sv, mps, final_norm_sq, truncation_error_sum, observed_max_bond_dim) =
                    self.run_mps_typed::<f32>(circuit, shots);
                SimulationResult::MpsF32 {
                    counts,
                    statevector: sv,
                    mps: mps.map(Arc::new),
                    max_bond_dim: self.max_bond_dim,
                    trunc_threshold: self.mps_trunc_threshold,
                    final_norm_sq,
                    truncation_error_sum,
                    observed_max_bond_dim,
                }
            }
            // v0.6.7: GPU-resident MPS — tensors stay in GPU buffers between
            // gates.  Contraction + 1q gate on GPU, SVD on host (v0.6.6.2
            // lesson).  precision arg ignored — wgpu storage f64 미지원.
            (Backend::WgpuMps, _) => {
                let (counts, sv, final_norm_sq, truncation_error_sum, observed_max_bond_dim) =
                    self.run_wgpu_mps(circuit, shots);
                SimulationResult::MpsF32 {
                    counts,
                    statevector: sv,
                    // WgpuMps: 호스트 MPS 가 보존되지 않음 → expectation 은
                    // statevector (N≤20) 경로만.
                    mps: None,
                    max_bond_dim: self.max_bond_dim,
                    trunc_threshold: self.mps_trunc_threshold,
                    final_norm_sq,
                    truncation_error_sum,
                    observed_max_bond_dim,
                }
            }
        }
    }

    /// 회로 실행 (Result 반환).  GpuError 또는 wgpu panic 모두 caller 가 처리.
    /// PyO3 binding 에서 wgpu backend 의 친화적 에러를 위해 사용.
    ///
    /// **v0.5.1 fix**: wgpu validation error 는 wgpu-core 의 default handler 로
    /// 인해 Rust panic 으로 떨어진다 (예: buffer 한계 초과, dispatch 한계 초과).
    /// `catch_unwind` 로 감싸 GpuError 로 변환 — Python 측에서 PyValueError 로
    /// 잡힘.  이전 v0.5.0 은 PyO3 가 PanicException (BaseException) 으로 노출해
    /// 사용자가 `except Exception` 으로 못 잡았음.
    ///
    /// **v0.5.20 fix**: catch_unwind 가 panic 자체는 잡지만, default panic hook
    /// 이 stderr 에 `thread '<unnamed>' panicked at ...` 같은 메시지를 출력
    /// 한다.  사용자는 친화 ValueError 와 동시에 panic stderr 를 보게 됨 →
    /// 사용자 PC 검증 보고 (RX 6600) 에서 cosmetic noise 로 보고됨.  fix:
    /// thread-local guard 로 panta-sim 의 catch 영역 안 panic 만 silent 처리.
    pub fn run_checked(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<SimulationResult, GpuError> {
        use std::panic::AssertUnwindSafe;
        // v0.5.20: panta-sim 안의 panic 을 stderr 출력 안 하게 thread-local guard.
        install_panta_sim_panic_hook();
        let _guard = SuppressPanicGuard::new();
        match (self.backend, self.precision) {
            (Backend::WgpuStatevector, _) => {
                let result = std::panic::catch_unwind(AssertUnwindSafe(|| {
                    self.run_wgpu_statevector(circuit, shots)
                }));
                match result {
                    Ok(Ok((counts, sv))) => Ok(SimulationResult::F32 {
                        counts,
                        statevector: sv,
                    }),
                    Ok(Err(e)) => Err(e),
                    Err(p) => Err(panic_to_gpu_error("wgpu statevector", p)),
                }
            }
            (Backend::WgpuDensity, _) => {
                // 2q correlated custom Kraus 는 wgpu density shader 미지원 →
                // CPU density (apply_kraus_2q) 폴백 (정확).  run() 경로와 동일.
                let has_2q_kraus = circuit
                    .instructions()
                    .iter()
                    .any(|i| matches!(i, Instruction::ApplyNoise2 { .. }));
                if has_2q_kraus {
                    let (counts, rho) = self.run_typed_density::<f32>(circuit, shots);
                    return Ok(SimulationResult::DensityF32 {
                        counts,
                        density: rho,
                    });
                }
                let result = std::panic::catch_unwind(AssertUnwindSafe(|| {
                    self.run_wgpu_density(circuit, shots)
                }));
                match result {
                    Ok(Ok((counts, rho))) => Ok(SimulationResult::DensityF32 {
                        counts,
                        density: rho,
                    }),
                    Ok(Err(e)) => Err(e),
                    Err(p) => Err(panic_to_gpu_error("wgpu density", p)),
                }
            }
            (Backend::CudaStatevector, Precision::F32) => {
                let (counts, sv) = self.run_cuda_statevector(circuit, shots)?;
                Ok(SimulationResult::F32 {
                    counts,
                    statevector: sv,
                })
            }
            (Backend::CudaStatevector, Precision::F64) => {
                // v0.6.2 fix: 이전엔 wildcard `(CudaStatevector, _)` 가 precision 무시.
                let (counts, sv) = self.run_cuda_statevector_f64(circuit, shots)?;
                Ok(SimulationResult::F64 {
                    counts,
                    statevector: sv,
                })
            }
            _ => Ok(self.run(circuit, shots)),
        }
    }

    /// wgpu Tier-1 statevector backend 경로 (v0.5.0 Cut D.4).
    ///
    /// 회로의 ApplyGate 들을 [`WgpuGateOp`] 로 변환 후 backend.apply_circuit
    /// 으로 batch dispatch.  noise / dynamic 회로는 v0.5.x patch 로 deferred —
    /// 현재 ApplyNoise / Reset / Measure(중간) / IfEq / IfElse / WhileLoop /
    /// ForLoop / Switch 가 있으면 GpuError::Unsupported.
    ///
    /// Toffoli / Fredkin (3-qubit) 도 명시 거부 — Cut D 가 1q + 2q + controlled-1q
    /// scope.  사용자에게 transpile 권유 메시지.
    ///
    /// 측정은 statevector download 후 CPU 의 `measurement::sample` /
    /// `sample_with_cbit_map` 으로 처리 (이미 충분히 빠름).
    fn run_wgpu_statevector(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f32>), GpuError> {
        // v0.5.19: pre-flight memory warning — sv_size ≥ 4 GiB 시 stderr.
        // 사용자 환경 RAM 부족 시 OOM 발생 전에 사전 알림.
        let n_qubits = circuit.num_qubits();
        let sv_bytes: u64 = (1u64 << n_qubits).saturating_mul(8); // f32 complex = 8 byte
        let sv_gib = sv_bytes as f64 / (1u64 << 30) as f64;
        if sv_gib >= 4.0 {
            eprintln!(
                "[panta-sim] info: wgpu statevector N={n_qubits} → \
                 statevector {sv_gib:.2} GiB.  GPU/unified memory 충분한지 \
                 확인 권장 (intermediate buffer 추가 1~2 GiB 필요)."
            );
        }

        // v0.5.8: noise 회로 hybrid trajectory.
        // v0.5.9: dynamic 회로 (Reset / IfEq / IfElse / WhileLoop / ForLoop /
        // Switch / mid-circuit Measure) 도 같은 trajectory path 에서 처리.
        let has_noise = circuit.instructions().iter().any(|i| {
            matches!(
                i,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });
        let has_dynamic = circuit.has_dynamic();
        if has_noise || has_dynamic {
            return self.run_wgpu_statevector_trajectory(circuit, shots);
        }

        // dynamic / noise 없는 fast path (기존 v0.5.x).
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { .. } | Instruction::MeasureAll => {}
                Instruction::ApplyUnitary { .. } => {
                    return Err(GpuError::Unsupported(
                        "wgpu statevector 는 arbitrary unitary (qc.unitary) 를 \
                         지원하지 않습니다 — method='statevector' 사용"
                            .into(),
                    ));
                }
                Instruction::Measure { .. } => {
                    // explicit Measure 는 회로 끝의 trailing 만 허용 (cbit map).
                    // 중간 위치는 dynamic 으로 분류되므로 has_dynamic check 로 거부.
                }
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. } => {
                    unreachable!("noise 는 trajectory path")
                }
                Instruction::Reset { .. }
                | Instruction::IfEq { .. }
                | Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => unreachable!("dynamic 은 위에서 거부됨"),
            }
        }

        // Gate → WgpuGateOp 변환.
        let mut ops: Vec<WgpuGateOp> = Vec::new();
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    convert_gate_to_wgpu_ops(gate, targets, &mut ops)?;
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => {
                    has_measure_all = true;
                }
                _ => unreachable!("dynamic instruction 은 이미 거부됨"),
            }
        }

        // Backend 가져오기 (v0.5.1: process-wide cached singleton — 첫 호출만 ~수백 ms).
        let backend = qsim_gpu::cached_wgpu_statevector_backend()?;
        let n = circuit.num_qubits();
        let dim = 1usize << n;
        let mut sv_data: Vec<Complex<f32>> = vec![Complex::new(0.0, 0.0); dim];
        sv_data[0] = Complex::new(1.0, 0.0);
        backend.apply_circuit(&mut sv_data, &ops)?;

        // global_phase 적용.
        let lambda = circuit.global_phase();
        if lambda != 0.0 {
            let phase = Complex::new(lambda.cos() as f32, lambda.sin() as f32);
            for amp in &mut sv_data {
                *amp *= phase;
            }
        }

        // CPU StateVector 로 wrap.
        let mut state = StateVector::<f32>::new(n);
        state.amplitudes_mut().copy_from_slice(&sv_data);

        // RNG + sampling.
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        let counts = if shots == 0 {
            std::collections::HashMap::new()
        } else if has_measure_all {
            measurement::sample(&state, shots, &mut rng)
        } else if !explicit_measures.is_empty() {
            measurement::sample_with_cbit_map(
                &state,
                shots,
                &explicit_measures,
                circuit.num_cbits(),
                &mut rng,
            )
        } else {
            std::collections::HashMap::new()
        };
        Ok((counts, state))
    }

    /// v0.5.8/v0.5.9: wgpu statevector + noise/dynamic hybrid trajectory path.
    ///
    /// 매 shot 마다 GPU 에서 |0⟩ init → consecutive gates 를 batch dispatch →
    /// `ApplyNoise` / dynamic instruction (Reset / IfEq / IfElse / WhileLoop /
    /// ForLoop / Switch / mid-circuit Measure) 만나면 batch flush + GPU →
    /// CPU download → CPU 에서 dispatch_instruction (Kraus / measure /
    /// classical control 모두 처리) → upload → 다음 batch.  회로 끝에서
    /// final download + CPU sampling.
    ///
    /// 성능: dynamic op 가 적은 큰 회로 (N≥20) 에서 GPU 가속 의미 있음.
    /// 잦으면 round-trip 비용 ↑ — 작은 N 은 `backend='cpu'` 권장.
    /// v0.6.10: GPU-resident trajectory.  적격 (mid-circuit Measure/Reset 전용
    /// dynamic 회로, N≤27, noise/control-flow/MeasureAll 없음) 이면
    /// `Some(Ok((counts, sv)))`, 부적격이면 `Ok(None)` 을 반환해 호출자가
    /// 기존 경로로 폴백하게 한다.
    ///
    /// state 를 [`create_zero_state_buffer`] 로 GPU 에 두고, gate batch 는
    /// [`apply_ops_to_buffer`], 측정은 [`measure_qubit_gpu`] (GPU prob 계산 +
    /// GPU Philox uniform) 로 처리 — instruction 사이에 statevector 를
    /// download/upload 하지 않는다.  counts 는 기존 trajectory 와 동일하게 cbit
    /// register (LSB-first) 에서 만든다.
    ///
    /// [`create_zero_state_buffer`]: qsim_gpu::WgpuStatevectorBackend::create_zero_state_buffer
    /// [`apply_ops_to_buffer`]: qsim_gpu::WgpuStatevectorBackend::apply_ops_to_buffer
    /// [`measure_qubit_gpu`]: qsim_gpu::WgpuStatevectorBackend::measure_qubit_gpu
    #[allow(clippy::type_complexity)]
    fn try_wgpu_resident_trajectory(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<Option<(std::collections::HashMap<String, usize>, StateVector<f32>)>, GpuError>
    {
        let n = circuit.num_qubits();
        // K=1 (single buffer) 만 — N>27 은 buffer-split 이라 GPU-resident measure
        // (single state_buffer) 불가.
        if n > 27 {
            return Ok(None);
        }
        // 적격성: 모든 instruction 이 ApplyGate / Measure / Reset 이고, Measure
        // 또는 Reset 이 하나 이상 (dynamic).  noise / control-flow / MeasureAll /
        // ApplyUnitary 가 있으면 부적격.
        let mut n_measure_reset = 0usize;
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { .. } => {}
                Instruction::Measure { .. } | Instruction::Reset { .. } => n_measure_reset += 1,
                _ => return Ok(None),
            }
        }
        if n_measure_reset == 0 {
            return Ok(None);
        }

        let backend = qsim_gpu::cached_wgpu_statevector_backend()?;
        let dim = 1usize << n;
        let n_cbits = circuit.num_cbits();
        let lambda = circuit.global_phase();
        let phase = if lambda != 0.0 {
            Some(Complex::new(lambda.cos() as f32, lambda.sin() as f32))
        } else {
            None
        };
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        // f32 X matrix (Reset 의 |1⟩→|0⟩ flip 용).
        let x_op = |q: usize| WgpuGateOp::Single {
            matrix: [
                [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
                [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
            ],
            target: q,
        };

        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_sv: Vec<Complex<f32>> = vec![Complex::new(0.0, 0.0); dim];
        let trajectories = shots.max(1);

        for _shot in 0..trajectories {
            let storage = backend.create_zero_state_buffer(dim);
            let mut cbits: Vec<u8> = vec![0; n_cbits];
            // 이 shot 의 measure/reset uniform 을 GPU Philox 로 한 번에 생성.
            let shot_seed: u64 = rng.gen();
            let uniforms = backend.generate_uniforms(shot_seed, n_measure_reset)?;
            let mut u_idx = 0usize;
            let mut pending: Vec<WgpuGateOp> = Vec::new();

            for inst in circuit.instructions() {
                match inst {
                    Instruction::ApplyGate { gate, targets } => {
                        convert_gate_to_wgpu_ops(gate, targets, &mut pending)?;
                    }
                    Instruction::Measure { qubit, cbit } => {
                        if !pending.is_empty() {
                            backend.apply_ops_to_buffer(&storage, &pending, dim)?;
                            pending.clear();
                        }
                        let u = uniforms[u_idx];
                        u_idx += 1;
                        let outcome = backend.measure_qubit_gpu(&storage, dim, *qubit, u)?;
                        if *cbit < cbits.len() {
                            cbits[*cbit] = outcome;
                        }
                    }
                    Instruction::Reset { qubit } => {
                        if !pending.is_empty() {
                            backend.apply_ops_to_buffer(&storage, &pending, dim)?;
                            pending.clear();
                        }
                        let u = uniforms[u_idx];
                        u_idx += 1;
                        let outcome = backend.measure_qubit_gpu(&storage, dim, *qubit, u)?;
                        if outcome == 1 {
                            backend.apply_ops_to_buffer(&storage, &[x_op(*qubit)], dim)?;
                        }
                    }
                    _ => unreachable!("eligibility 가 다른 instruction 을 배제함"),
                }
            }
            if !pending.is_empty() {
                backend.apply_ops_to_buffer(&storage, &pending, dim)?;
            }

            let mut sv = backend.download_state_buffer(&storage, dim)?;
            if let Some(p) = phase {
                for amp in &mut sv {
                    *amp *= p;
                }
            }

            if shots > 0 && n_cbits > 0 {
                let bits: String = (0..n_cbits)
                    .rev()
                    .map(|i| if cbits[i] != 0 { '1' } else { '0' })
                    .collect();
                *counts.entry(bits).or_insert(0) += 1;
            }
            last_sv = sv;
        }

        let mut final_state = StateVector::<f32>::new(n);
        final_state.amplitudes_mut().copy_from_slice(&last_sv);
        Ok(Some((counts, final_state)))
    }

    fn run_wgpu_statevector_trajectory(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f32>), GpuError> {
        // v0.6.10: GPU-resident fast path — mid-circuit Measure/Reset 만 있는
        // dynamic 회로 (noise / control-flow / MeasureAll 없음, N≤27) 는 state
        // 를 GPU 버퍼에 상주시킨 채 gate batch + measure_qubit_gpu (GPU prob +
        // GPU Philox uniform) 로 처리해 instruction 마다의 full round-trip 을
        // 제거한다.  부적격이면 None → 기존 CPU-hybrid 경로로 폴백.
        if let Some(res) = self.try_wgpu_resident_trajectory(circuit, shots)? {
            return Ok(res);
        }
        let backend = qsim_gpu::cached_wgpu_statevector_backend()?;
        let n = circuit.num_qubits();
        let dim = 1usize << n;

        // trailing Measure (cbit map) 와 MeasureAll 수집.
        // **v0.5.21 fix**: 이전 버전은 `if !has_dyn` 안에서만 collection 했음 —
        // dynamic 회로 (예: reset 포함) + measure_all 조합 시 has_measure_all
        // 가 false 인 채로 final sampling 진입 → cbit register branch (모두
        // default 0) 가 활성돼 잘못된 "0..." 결과.  RX 6600 dispatch 검증의
        // C-2 (multi-reset) issue 가 이 bug.  fix: 항상 collection.
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        let has_dyn = circuit.has_dynamic();
        for inst in circuit.instructions() {
            match inst {
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => {
                    has_measure_all = true;
                }
                _ => {}
            }
        }

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        let lambda = circuit.global_phase();
        let phase = if lambda != 0.0 {
            Some(Complex::new(lambda.cos() as f32, lambda.sin() as f32))
        } else {
            None
        };

        let n_cbits = circuit.num_cbits();
        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_sv: Vec<Complex<f32>> = vec![Complex::new(0.0, 0.0); dim];
        let trajectories = shots.max(1);

        for _shot in 0..trajectories {
            let mut sv: Vec<Complex<f32>> = vec![Complex::new(0.0, 0.0); dim];
            sv[0] = Complex::new(1.0, 0.0);
            let mut cbits: Vec<u8> = vec![0; n_cbits];

            // Gate batch 누적, dynamic / noise 만나면 flush + CPU dispatch.
            let mut pending_ops: Vec<WgpuGateOp> = Vec::new();
            for inst in circuit.instructions() {
                match inst {
                    Instruction::ApplyGate { gate, targets } => {
                        convert_gate_to_wgpu_ops(gate, targets, &mut pending_ops)?;
                    }
                    // 회로 끝의 trailing measure 는 final 단계에서 sampling.
                    Instruction::MeasureAll if !has_dyn => {}
                    Instruction::Measure { .. } if !has_dyn => {}
                    // 그 외 모두 (noise, dynamic) → flush + CPU dispatch.
                    _ => {
                        if !pending_ops.is_empty() {
                            backend.apply_circuit(&mut sv, &pending_ops)?;
                            pending_ops.clear();
                        }
                        let mut state_cpu = StateVector::<f32>::new(n);
                        state_cpu.amplitudes_mut().copy_from_slice(&sv);
                        Self::dispatch_instruction::<f32>(
                            inst,
                            &mut state_cpu,
                            &mut cbits,
                            &mut rng,
                        );
                        sv.copy_from_slice(state_cpu.amplitudes());
                    }
                }
            }
            if !pending_ops.is_empty() {
                backend.apply_circuit(&mut sv, &pending_ops)?;
            }
            if let Some(p) = phase {
                for amp in &mut sv {
                    *amp *= p;
                }
            }

            // Sample 한 trajectory.
            if shots > 0 {
                if has_dyn {
                    // **v0.5.21 fix**: has_measure_all 우선 — measure_all 는 회로
                    // 끝의 final 큐비트 register sampling 의도 (Qiskit/Aer 와 동일).
                    // cbit register 는 explicit Measure(qubit, cbit) 가 mid-circuit
                    // 결과 저장에 활용된 경우만.  이전 버전은 n_cbits>0 우선이라
                    // measure_all + reset 조합에서 cbit register 의 default 0 만
                    // 반환 → 잘못된 결과 (RX 6600 C-2 issue).
                    if has_measure_all {
                        let mut state_cpu = StateVector::<f32>::new(n);
                        state_cpu.amplitudes_mut().copy_from_slice(&sv);
                        let bits = measurement::sample_once(&state_cpu, &mut rng);
                        *counts.entry(bits).or_insert(0) += 1;
                    } else if n_cbits > 0 {
                        // dynamic 회로의 cbit register 를 LSB-first bitstring 으로.
                        let bits: String = (0..n_cbits)
                            .rev()
                            .map(|i| if cbits[i] != 0 { '1' } else { '0' })
                            .collect();
                        *counts.entry(bits).or_insert(0) += 1;
                    }
                } else {
                    let mut state_cpu = StateVector::<f32>::new(n);
                    state_cpu.amplitudes_mut().copy_from_slice(&sv);
                    if has_measure_all {
                        let bits = measurement::sample_once(&state_cpu, &mut rng);
                        *counts.entry(bits).or_insert(0) += 1;
                    } else if !explicit_measures.is_empty() {
                        let one = measurement::sample_with_cbit_map(
                            &state_cpu,
                            1,
                            &explicit_measures,
                            n_cbits,
                            &mut rng,
                        );
                        for (k, v) in one {
                            *counts.entry(k).or_insert(0) += v;
                        }
                    }
                }
            }

            last_sv = sv;
        }

        let mut final_state = StateVector::<f32>::new(n);
        final_state.amplitudes_mut().copy_from_slice(&last_sv);
        Ok((counts, final_state))
    }

    /// 정밀도 `F` 로 회로 실행. f32/f64 경로 모두 동일 코드 (monomorphized).
    ///
    /// 회로에 [`Instruction::ApplyNoise`] 또는 dynamic instruction (`Reset`/`IfEq`/
    /// 위치별 `Measure`) 이 하나라도 있으면 **trajectory 모드** 로 전환된다
    /// (각 shot 마다 회로 fresh 재실행 + cbit register + 위치별 즉시 처리).
    /// 둘 다 없으면 기존 fast path (1회 unitary evolution + N shot 샘플링).
    ///
    /// 반환되는 statevector 는 trajectory 모드일 땐 *마지막 trajectory* 의 것
    /// (디버깅 용, mixed state 를 대표하지 않음 — 사용자는 counts 를 사용).
    fn run_typed<F: Real>(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> (std::collections::HashMap<String, usize>, StateVector<F>) {
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        let has_noise = circuit.instructions().iter().any(|i| {
            matches!(
                i,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });

        if has_noise || circuit.has_dynamic() {
            self.run_typed_trajectory::<F>(circuit, shots, &mut rng)
        } else {
            self.run_typed_unitary::<F>(circuit, shots, &mut rng)
        }
    }

    /// Noise / dynamic 없는 경로 (fast): 1회 evolution → N shot 샘플링.
    ///
    /// **샘플러 분기 (v0.4.5.1)**:
    /// - `MeasureAll` 만 → [`measurement::sample`] (`n_qubits` 폭 비트열).
    /// - explicit `Measure { qubit, cbit }` 묶음만 → [`measurement::sample_with_cbit_map`]
    ///   (`n_cbits` 폭 + cbit 매핑 적용). v0.4.5.0 에서는 이 경로도 [`sample`] 을
    ///   썼는데 cbit 매핑이 무시돼 partial measure / cbit reorder / 동일 큐비트
    ///   두 번 측정 시 잘못된 결과를 냈음. v0.4.5.1 에서 정정.
    /// - 두 변종이 섞이면 (드문 케이스) 안전하게 [`Circuit::has_dynamic`] 가
    ///   true 를 반환하도록 빌더에서 막혀 있어 여기 도달 안 함 (실제로는 둘 다
    ///   trailing 일 수 있어 dynamic 분류 안 됨 — 이 경우 MeasureAll 우선).
    fn run_typed_unitary<F: Real>(
        &self,
        circuit: &Circuit,
        shots: usize,
        rng: &mut StdRng,
    ) -> (std::collections::HashMap<String, usize>, StateVector<F>) {
        let mut state: StateVector<F> = StateVector::new(circuit.num_qubits());
        let mut has_measure_all = false;
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();

        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    apply_gate_typed(&mut state, gate, targets);
                }
                Instruction::ApplyUnitary { matrix, targets } => {
                    apply_unitary_typed(&mut state, matrix, targets);
                }
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. } => {
                    unreachable!("run_typed_unitary called with noise instruction")
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => {
                    has_measure_all = true;
                }
                Instruction::Reset { .. }
                | Instruction::IfEq { .. }
                | Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => {
                    unreachable!("run_typed_unitary called with dynamic instruction")
                }
            }
        }

        apply_global_phase::<F>(&mut state, circuit.global_phase());

        let counts = if shots == 0 {
            std::collections::HashMap::new()
        } else if has_measure_all {
            // MeasureAll 우선 (둘 다 trailing 인 드문 경우 포함).
            measurement::sample(&state, shots, rng)
        } else if !explicit_measures.is_empty() {
            measurement::sample_with_cbit_map(
                &state,
                shots,
                &explicit_measures,
                circuit.num_cbits(),
                rng,
            )
        } else {
            std::collections::HashMap::new()
        };

        (counts, state)
    }

    /// Noise / dynamic 경로 (trajectory): shot 마다 회로 재실행 + cbit register +
    /// 위치별 Measure 즉시 처리 + Reset / IfEq dispatch.
    ///
    /// `shots == 0` 이면 단일 trajectory 만 실행하고 counts 는 비워서 반환 (statevector
    /// 디버깅 용도). `shots > 0` 이면 각 trajectory 마다 cbit register 를 LSB-first
    /// 패킹해 outcome 문자열로 만들어 누적. 회로에 위치별 측정만 있고 `MeasureAll` 없는
    /// 경우 cbit register 그대로 outcome (creg width = `num_cbits`).  `MeasureAll` 이
    /// 끝에 있으면 trajectory 끝 상태에서 한 번 더 sampling (기존 v0.4.0 호환).
    fn run_typed_trajectory<F: Real>(
        &self,
        circuit: &Circuit,
        shots: usize,
        rng: &mut StdRng,
    ) -> (std::collections::HashMap<String, usize>, StateVector<F>) {
        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_state: Option<StateVector<F>> = None;

        let has_measure_all = circuit
            .instructions()
            .iter()
            .any(|i| matches!(i, Instruction::MeasureAll));
        // v0.6.2: control-flow body 안의 Measure 도 final counts 에 반영되도록
        // 재귀 검사.  이전엔 top-level Measure 만 봐서 IfElse 안의 measure 결과
        // 가 counts 에 안 잡혔음.
        let has_explicit_measure = body_has_measure(circuit.instructions());

        let n_trajectories = if shots == 0 { 1 } else { shots };
        let lambda = circuit.global_phase();
        let n_cbits = circuit.num_cbits();
        let n_qubits = circuit.num_qubits();

        for _ in 0..n_trajectories {
            let mut state: StateVector<F> = StateVector::new(n_qubits);
            let mut cbits: Vec<u8> = vec![0; n_cbits];
            for inst in circuit.instructions() {
                Self::dispatch_instruction::<F>(inst, &mut state, &mut cbits, rng);
            }
            apply_global_phase::<F>(&mut state, lambda);

            if shots > 0 && (has_measure_all || has_explicit_measure) {
                // creg 의 cbits 를 LSB-first packed bit string 으로.
                // MSB = cbits[n_cbits-1], LSB = cbits[0] — Qiskit counts 표기와 동일.
                // MeasureAll 도 dispatch 단계에서 cbits 에 기록되므로 동일 path.
                let mut s = String::with_capacity(n_cbits);
                for &b in cbits.iter().rev() {
                    s.push(if b == 0 { '0' } else { '1' });
                }
                *counts.entry(s).or_insert(0) += 1;
            }
            // shots=0 이거나 측정/MeasureAll 둘 다 없으면 counts 비워둠 (statevector
            // 디버깅 path).

            last_state = Some(state);
        }

        (counts, last_state.expect("at least one trajectory"))
    }

    /// 단일 instruction 을 trajectory 상태에 dispatch.
    /// `IfEq` 의 body 재귀 적용 시에도 동일 함수 호출.
    fn dispatch_instruction<F: Real>(
        inst: &Instruction,
        state: &mut StateVector<F>,
        cbits: &mut [u8],
        rng: &mut StdRng,
    ) {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                apply_gate_typed(state, gate, targets);
            }
            Instruction::ApplyUnitary { matrix, targets } => {
                apply_unitary_typed(state, matrix, targets);
            }
            Instruction::ApplyNoise { channel, target } => {
                channel.apply_to(state, *target, rng);
            }
            Instruction::ApplyNoise2 { channel, q0, q1 } => {
                channel.apply_to(state, *q0, *q1, rng);
            }
            Instruction::Measure { qubit, cbit } => {
                let outcome = measurement::measure_qubit_inplace(state, *qubit, rng);
                // 빌더가 cbit register 폭을 항상 grow 하므로 정상 path 에서는
                // *cbit < cbits.len().  v0.6.2 부터 control-flow body cbit 도
                // outer 가 propagate (`scan_body_max_cbit`) 하므로 도달 불가.
                debug_assert!(
                    *cbit < cbits.len(),
                    "Measure cbit={cbit} >= n_cbits={} — circuit 빌더가 propagate 누락",
                    cbits.len()
                );
                if *cbit < cbits.len() {
                    cbits[*cbit] = outcome;
                }
            }
            Instruction::MeasureAll => {
                // 모든 qubit 을 순차 측정 → collapse → cbits[q] 에 기록.
                // mid-circuit MeasureAll 후에 게이트가 더 있어도 정상 동작.
                let n = state.num_qubits();
                for q in 0..n {
                    let outcome = measurement::measure_qubit_inplace(state, q, rng);
                    if q < cbits.len() {
                        cbits[q] = outcome;
                    }
                }
            }
            Instruction::Reset { qubit } => {
                measurement::reset_qubit(state, *qubit, rng);
            }
            Instruction::IfEq {
                cbit_indices,
                value,
                body,
            } => {
                if pack_cbits(cbit_indices, cbits) == *value {
                    Self::dispatch_instruction::<F>(body, state, cbits, rng);
                }
            }
            Instruction::IfElse {
                cbit_indices,
                value,
                then_body,
                else_body,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let body: Option<&[Instruction]> = if packed == *value {
                    Some(then_body.as_slice())
                } else {
                    else_body.as_deref()
                };
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction::<F>(inst, state, cbits, rng);
                    }
                }
            }
            Instruction::WhileLoop {
                cbit_indices,
                value,
                body,
                max_iters,
            } => {
                // cond 가 true 인 동안 body 반복. max_iters 안전 bound.
                for _ in 0..*max_iters {
                    if pack_cbits(cbit_indices, cbits) != *value {
                        break;
                    }
                    for inst in body {
                        Self::dispatch_instruction::<F>(inst, state, cbits, rng);
                    }
                }
            }
            Instruction::ForLoop { iterations, body } => {
                for _ in 0..*iterations {
                    for inst in body {
                        Self::dispatch_instruction::<F>(inst, state, cbits, rng);
                    }
                }
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let mut chosen: Option<&Vec<Instruction>> = None;
                let mut default: Option<&Vec<Instruction>> = None;
                for (label, body) in cases {
                    match label {
                        Some(v) if *v == packed => {
                            chosen = Some(body);
                            break;
                        }
                        None => default = Some(body),
                        _ => {}
                    }
                }
                let body = chosen.or(default);
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction::<F>(inst, state, cbits, rng);
                    }
                }
            }
        }
    }

    /// Density matrix 백엔드 경로 (v0.5.0).
    ///
    /// 회로의 모든 instruction 을 순서대로 ρ 에 dispatch 한다.  noise 가 있어도
    /// trajectory 가 아닌 결정적 Kraus 적용 — Aer `method="density_matrix"` 와
    /// 동일 의미.  shots > 0 이고 측정이 있으면 단일 evolution 끝에서 N 회
    /// CDF 샘플링 (각 trajectory 재실행 X).
    ///
    /// dynamic 회로 (Reset / IfEq / IfElse / WhileLoop / ForLoop / Switch /
    /// 위치별 Measure) 는 측정 outcome 이 cbit 에 들어가야 다음 분기가 결정되므로
    /// shot 당 fresh ρ 진화 + 위치별 measure_collapse + cbit register.  shots=0
    /// 은 단일 trajectory 의 ρ 만 반환.
    ///
    /// counts 표기 (statevector 경로와 동일):
    /// - MeasureAll 만: `n_qubits` 폭 LSB-first 비트열.
    /// - explicit Measure 만: `n_cbits` 폭 LSB-first.
    /// - 둘 다 없음: counts 비움 (디버깅 용 ρ 만).
    fn run_typed_density<F: Real>(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> (std::collections::HashMap<String, usize>, DensityMatrix<F>) {
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        let n_qubits = circuit.num_qubits();
        let n_cbits = circuit.num_cbits();
        let lambda = circuit.global_phase();

        let has_measure_all = circuit
            .instructions()
            .iter()
            .any(|i| matches!(i, Instruction::MeasureAll));
        let has_dynamic = circuit.has_dynamic();
        let has_noise = circuit.instructions().iter().any(|i| {
            matches!(
                i,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });

        // Dynamic 회로는 cbit 분기가 측정 결과에 의존 → trajectory 모드.
        // 그렇지 않으면 단일 ρ 진화 + (있다면) 끝에서 sampling.
        if has_dynamic {
            self.run_typed_density_trajectory::<F>(circuit, shots, &mut rng)
        } else {
            // Static 경로: ρ 한 번 진화 후 끝에서 sampling.
            let mut rho: DensityMatrix<F> = DensityMatrix::new(n_qubits);
            let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
            for inst in circuit.instructions() {
                match inst {
                    Instruction::ApplyGate { gate, targets } => {
                        apply_gate_typed_density(&mut rho, gate, targets);
                    }
                    Instruction::ApplyUnitary { .. } => {
                        panic!("{}", UNITARY_UNSUPPORTED_MSG);
                    }
                    Instruction::ApplyNoise { channel, target } => {
                        let kraus = channel.kraus_operators::<F>();
                        rho.apply_kraus_1q(&kraus, *target);
                    }
                    Instruction::ApplyNoise2 { channel, q0, q1 } => {
                        let kraus = channel.kraus_operators::<F>();
                        rho.apply_kraus_2q(&kraus, *q0, *q1);
                    }
                    Instruction::Measure { qubit, cbit } => {
                        explicit_measures.push((*qubit, *cbit));
                    }
                    Instruction::MeasureAll => {}
                    // dynamic instruction 은 has_dynamic 분기에서 처리.
                    Instruction::Reset { .. }
                    | Instruction::IfEq { .. }
                    | Instruction::IfElse { .. }
                    | Instruction::WhileLoop { .. }
                    | Instruction::ForLoop { .. }
                    | Instruction::Switch { .. } => {
                        unreachable!("density static path with dynamic instruction")
                    }
                }
            }
            apply_global_phase_density::<F>(&mut rho, lambda);

            let counts = if shots == 0 {
                std::collections::HashMap::new()
            } else if has_measure_all {
                sample_density(&rho, shots, n_qubits, &mut rng)
            } else if !explicit_measures.is_empty() {
                sample_density_with_cbit_map(&rho, shots, &explicit_measures, n_cbits, &mut rng)
            } else {
                std::collections::HashMap::new()
            };
            // noise 없는 회로는 결정적 (RNG 사용 안함) — 빠른 path.
            // noise 있어도 ρ 는 결정적, RNG 는 sampling 에만 사용.
            let _ = has_noise; // 위 분기에서 자동 처리.
            (counts, rho)
        }
    }

    /// Density 백엔드 의 dynamic 회로 경로 (shot 당 fresh ρ).
    fn run_typed_density_trajectory<F: Real>(
        &self,
        circuit: &Circuit,
        shots: usize,
        rng: &mut StdRng,
    ) -> (std::collections::HashMap<String, usize>, DensityMatrix<F>) {
        let n_qubits = circuit.num_qubits();
        let n_cbits = circuit.num_cbits();
        let lambda = circuit.global_phase();
        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_rho: Option<DensityMatrix<F>> = None;

        let has_measure_all = circuit
            .instructions()
            .iter()
            .any(|i| matches!(i, Instruction::MeasureAll));
        // v0.6.2: control-flow body 의 measure 도 검출.
        let has_explicit_measure = body_has_measure(circuit.instructions());
        let n_trajectories = if shots == 0 { 1 } else { shots };

        for _ in 0..n_trajectories {
            let mut rho: DensityMatrix<F> = DensityMatrix::new(n_qubits);
            let mut cbits: Vec<u8> = vec![0; n_cbits];
            for inst in circuit.instructions() {
                Self::dispatch_instruction_density::<F>(inst, &mut rho, &mut cbits, rng);
            }
            apply_global_phase_density::<F>(&mut rho, lambda);

            if shots > 0 && (has_measure_all || has_explicit_measure) {
                // MeasureAll 도 dispatch 단계에서 cbits 에 기록되므로 동일 path.
                let mut s = String::with_capacity(n_cbits);
                for &b in cbits.iter().rev() {
                    s.push(if b == 0 { '0' } else { '1' });
                }
                *counts.entry(s).or_insert(0) += 1;
            }
            last_rho = Some(rho);
        }
        (counts, last_rho.expect("at least one trajectory"))
    }

    /// Density 백엔드 의 instruction dispatch.  statevector 의
    /// [`dispatch_instruction`](Self::dispatch_instruction) 와 평행 구조.
    fn dispatch_instruction_density<F: Real>(
        inst: &Instruction,
        rho: &mut DensityMatrix<F>,
        cbits: &mut [u8],
        rng: &mut StdRng,
    ) {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                apply_gate_typed_density(rho, gate, targets);
            }
            Instruction::ApplyUnitary { .. } => {
                panic!("{}", UNITARY_UNSUPPORTED_MSG);
            }
            Instruction::ApplyNoise { channel, target } => {
                let kraus = channel.kraus_operators::<F>();
                rho.apply_kraus_1q(&kraus, *target);
            }
            Instruction::ApplyNoise2 { channel, q0, q1 } => {
                let kraus = channel.kraus_operators::<F>();
                rho.apply_kraus_2q(&kraus, *q0, *q1);
            }
            Instruction::Measure { qubit, cbit } => {
                let outcome = rho.measure_collapse(*qubit, rng);
                // v0.6.2: 빌더 propagate invariant 검증 (debug only).
                debug_assert!(
                    *cbit < cbits.len(),
                    "Measure cbit={cbit} >= n_cbits={} — circuit 빌더가 propagate 누락",
                    cbits.len()
                );
                if *cbit < cbits.len() {
                    cbits[*cbit] = outcome;
                }
            }
            Instruction::MeasureAll => {
                // 모든 qubit 을 순차 측정 → collapse → cbits[q] 에 기록.
                // mid-circuit MeasureAll 후에 게이트가 더 있어도 정상 동작.
                let n = rho.num_qubits();
                for q in 0..n {
                    let outcome = rho.measure_collapse(q, rng);
                    if q < cbits.len() {
                        cbits[q] = outcome;
                    }
                }
            }
            Instruction::Reset { qubit } => {
                rho.reset_qubit(*qubit);
            }
            Instruction::IfEq {
                cbit_indices,
                value,
                body,
            } => {
                if pack_cbits(cbit_indices, cbits) == *value {
                    Self::dispatch_instruction_density::<F>(body, rho, cbits, rng);
                }
            }
            Instruction::IfElse {
                cbit_indices,
                value,
                then_body,
                else_body,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let body: Option<&[Instruction]> = if packed == *value {
                    Some(then_body.as_slice())
                } else {
                    else_body.as_deref()
                };
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction_density::<F>(inst, rho, cbits, rng);
                    }
                }
            }
            Instruction::WhileLoop {
                cbit_indices,
                value,
                body,
                max_iters,
            } => {
                for _ in 0..*max_iters {
                    if pack_cbits(cbit_indices, cbits) != *value {
                        break;
                    }
                    for inst in body {
                        Self::dispatch_instruction_density::<F>(inst, rho, cbits, rng);
                    }
                }
            }
            Instruction::ForLoop { iterations, body } => {
                for _ in 0..*iterations {
                    for inst in body {
                        Self::dispatch_instruction_density::<F>(inst, rho, cbits, rng);
                    }
                }
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let mut chosen: Option<&Vec<Instruction>> = None;
                let mut default: Option<&Vec<Instruction>> = None;
                for (label, body) in cases {
                    match label {
                        Some(v) if *v == packed => {
                            chosen = Some(body);
                            break;
                        }
                        None => default = Some(body),
                        _ => {}
                    }
                }
                let body = chosen.or(default);
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction_density::<F>(inst, rho, cbits, rng);
                    }
                }
            }
        }
    }

    /// cuStateVec Tier-2 statevector backend 경로 (Cut G, feature `gpu-cuda`).
    ///
    /// `gpu-cuda` feature off 일 때 (sandbox / non-NVIDIA) 는 GpuError::Unsupported
    /// 반환 — Python 측 PyValueError 로 변환되어 사용자에게 안내.  NVIDIA + cuQuantum
    /// 환경에선 `CudaStatevectorBackend::apply_circuit` 으로 dispatch.
    #[cfg(feature = "gpu-cuda")]
    fn run_cuda_statevector(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f32>), GpuError> {
        use qsim_gpu::cuda::{CudaGateOp, CudaStatevectorBackend};

        // v0.5.12: noise / dynamic 회로는 hybrid trajectory path 진입 (wgpu
        // v0.5.8/9 패턴 복제 — cuda 호출 swap).
        let has_noise = circuit.instructions().iter().any(|i| {
            matches!(
                i,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });
        let has_dynamic = circuit.has_dynamic();
        if has_noise || has_dynamic {
            return self.run_cuda_statevector_trajectory(circuit, shots);
        }

        let mut ops: Vec<CudaGateOp> = Vec::new();
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    convert_gate_to_cuda_ops(gate, targets, &mut ops)?;
                }
                Instruction::ApplyNoise { .. } => unreachable!("noise 는 trajectory path"),
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => has_measure_all = true,
                _ => unreachable!("dynamic instruction 은 이미 거부됨"),
            }
        }

        let n = circuit.num_qubits();
        let dim = 1usize << n;
        let mut sv_data: Vec<num_complex::Complex<f32>> =
            vec![num_complex::Complex::new(0.0, 0.0); dim];
        sv_data[0] = num_complex::Complex::new(1.0, 0.0);

        let backend = CudaStatevectorBackend::new()?;
        backend.apply_circuit(&mut sv_data, &ops)?;

        let lambda = circuit.global_phase();
        if lambda != 0.0 {
            let phase = num_complex::Complex::new(lambda.cos() as f32, lambda.sin() as f32);
            for amp in &mut sv_data {
                *amp *= phase;
            }
        }

        let mut state = StateVector::<f32>::new(n);
        state.amplitudes_mut().copy_from_slice(&sv_data);

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        let counts = if shots == 0 {
            std::collections::HashMap::new()
        } else if has_measure_all {
            measurement::sample(&state, shots, &mut rng)
        } else if !explicit_measures.is_empty() {
            measurement::sample_with_cbit_map(
                &state,
                shots,
                &explicit_measures,
                circuit.num_cbits(),
                &mut rng,
            )
        } else {
            std::collections::HashMap::new()
        };
        Ok((counts, state))
    }

    /// v0.5.12: cuda statevector + noise/dynamic hybrid trajectory path.
    /// wgpu trajectory (v0.5.8/9) 와 동일 패턴 — 매 trajectory 마다 GPU 에서
    /// gate batch dispatch + ApplyNoise/dynamic 만나면 download + CPU
    /// dispatch_instruction + upload.  사용자 NVIDIA PC 검증 대기.
    #[cfg(feature = "gpu-cuda")]
    fn run_cuda_statevector_trajectory(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f32>), GpuError> {
        use qsim_gpu::cuda::CudaStatevectorBackend;

        let backend = CudaStatevectorBackend::new()?;
        let n = circuit.num_qubits();
        let dim = 1usize << n;

        // **v0.5.21 fix**: 항상 collection (wgpu trajectory 와 동일).
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        let has_dyn = circuit.has_dynamic();
        for inst in circuit.instructions() {
            match inst {
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => has_measure_all = true,
                _ => {}
            }
        }

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        let lambda = circuit.global_phase();
        let phase = if lambda != 0.0 {
            Some(num_complex::Complex::new(
                lambda.cos() as f32,
                lambda.sin() as f32,
            ))
        } else {
            None
        };

        let n_cbits = circuit.num_cbits();
        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_sv: Vec<num_complex::Complex<f32>> =
            vec![num_complex::Complex::new(0.0, 0.0); dim];
        let trajectories = shots.max(1);

        for _shot in 0..trajectories {
            let mut sv: Vec<num_complex::Complex<f32>> =
                vec![num_complex::Complex::new(0.0, 0.0); dim];
            sv[0] = num_complex::Complex::new(1.0, 0.0);
            let mut cbits: Vec<u8> = vec![0; n_cbits];

            let mut pending_ops: Vec<qsim_gpu::cuda::CudaGateOp> = Vec::new();
            for inst in circuit.instructions() {
                match inst {
                    Instruction::ApplyGate { gate, targets } => {
                        convert_gate_to_cuda_ops(gate, targets, &mut pending_ops)?;
                    }
                    Instruction::MeasureAll if !has_dyn => {}
                    Instruction::Measure { .. } if !has_dyn => {}
                    _ => {
                        if !pending_ops.is_empty() {
                            backend.apply_circuit(&mut sv, &pending_ops)?;
                            pending_ops.clear();
                        }
                        let mut state_cpu = StateVector::<f32>::new(n);
                        state_cpu.amplitudes_mut().copy_from_slice(&sv);
                        Self::dispatch_instruction::<f32>(
                            inst,
                            &mut state_cpu,
                            &mut cbits,
                            &mut rng,
                        );
                        sv.copy_from_slice(state_cpu.amplitudes());
                    }
                }
            }
            if !pending_ops.is_empty() {
                backend.apply_circuit(&mut sv, &pending_ops)?;
            }
            if let Some(p) = phase {
                for amp in &mut sv {
                    *amp *= p;
                }
            }

            if shots > 0 {
                if has_dyn {
                    // **v0.5.21 fix**: has_measure_all 우선 (wgpu trajectory 와 동일).
                    if has_measure_all {
                        let mut state_cpu = StateVector::<f32>::new(n);
                        state_cpu.amplitudes_mut().copy_from_slice(&sv);
                        let bits = measurement::sample_once(&state_cpu, &mut rng);
                        *counts.entry(bits).or_insert(0) += 1;
                    } else if n_cbits > 0 {
                        let bits: String = (0..n_cbits)
                            .rev()
                            .map(|i| if cbits[i] != 0 { '1' } else { '0' })
                            .collect();
                        *counts.entry(bits).or_insert(0) += 1;
                    }
                } else {
                    let mut state_cpu = StateVector::<f32>::new(n);
                    state_cpu.amplitudes_mut().copy_from_slice(&sv);
                    if has_measure_all {
                        let bits = measurement::sample_once(&state_cpu, &mut rng);
                        *counts.entry(bits).or_insert(0) += 1;
                    } else if !explicit_measures.is_empty() {
                        let one = measurement::sample_with_cbit_map(
                            &state_cpu,
                            1,
                            &explicit_measures,
                            n_cbits,
                            &mut rng,
                        );
                        for (k, v) in one {
                            *counts.entry(k).or_insert(0) += v;
                        }
                    }
                }
            }

            last_sv = sv;
        }

        let mut final_state = StateVector::<f32>::new(n);
        final_state.amplitudes_mut().copy_from_slice(&last_sv);
        Ok((counts, final_state))
    }

    /// v0.5.12: cuStateVec f64 (CUDA_C_64F) statevector path.
    ///
    /// 양자 화학 / VQE 같은 정밀 계산 (norm error < 1e-12) 영역.  Apple Metal
    /// 의 wgpu 는 f64 미지원 — cuStateVec Tier-2 에서만 가용.  noise / dynamic
    /// 회로는 v0.5.x 후속 patch — 현재 거부.
    #[cfg(feature = "gpu-cuda")]
    fn run_cuda_statevector_f64(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f64>), GpuError> {
        use qsim_gpu::cuda::{CudaGateOpF64, CudaStatevectorBackend};

        if circuit.has_dynamic() {
            return Err(GpuError::Unsupported(
                "cuda statevector f64: dynamic 회로는 v0.5.x patch — \
                 backend='cpu' precision='double' 사용"
                    .into(),
            ));
        }
        let has_noise = circuit.instructions().iter().any(|i| {
            matches!(
                i,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });
        if has_noise {
            return Err(GpuError::Unsupported(
                "cuda statevector f64: noise 회로는 v0.5.x patch — \
                 backend='cpu' precision='double' 사용"
                    .into(),
            ));
        }

        let mut ops: Vec<CudaGateOpF64> = Vec::new();
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    convert_gate_to_cuda_ops_f64(gate, targets, &mut ops)?;
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => has_measure_all = true,
                _ => unreachable!("noise / dynamic 은 위에서 거부됨"),
            }
        }

        let n = circuit.num_qubits();
        let dim = 1usize << n;
        let mut sv_data: Vec<num_complex::Complex<f64>> =
            vec![num_complex::Complex::new(0.0, 0.0); dim];
        sv_data[0] = num_complex::Complex::new(1.0, 0.0);

        let backend = CudaStatevectorBackend::new()?;
        backend.apply_circuit_f64(&mut sv_data, &ops)?;

        let lambda = circuit.global_phase();
        if lambda != 0.0 {
            let phase = num_complex::Complex::new(lambda.cos(), lambda.sin());
            for amp in &mut sv_data {
                *amp *= phase;
            }
        }

        let mut state = StateVector::<f64>::new(n);
        state.amplitudes_mut().copy_from_slice(&sv_data);

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        let counts = if shots == 0 {
            std::collections::HashMap::new()
        } else if has_measure_all {
            measurement::sample(&state, shots, &mut rng)
        } else if !explicit_measures.is_empty() {
            measurement::sample_with_cbit_map(
                &state,
                shots,
                &explicit_measures,
                circuit.num_cbits(),
                &mut rng,
            )
        } else {
            std::collections::HashMap::new()
        };
        Ok((counts, state))
    }

    /// f64 stub (gpu-cuda feature off 시).
    #[cfg(not(feature = "gpu-cuda"))]
    fn run_cuda_statevector_f64(
        &self,
        _circuit: &Circuit,
        _shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f64>), GpuError> {
        Err(GpuError::Unsupported(
            "cuda statevector f64: panta-sim 이 'gpu-cuda' feature 없이 빌드됨".into(),
        ))
    }

    /// `gpu-cuda` feature off 시의 stub.  Python / cargo 사용자에게 친화적 에러.
    #[cfg(not(feature = "gpu-cuda"))]
    fn run_cuda_statevector(
        &self,
        _circuit: &Circuit,
        _shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, StateVector<f32>), GpuError> {
        Err(GpuError::Unsupported(
            "cuda statevector: panta-sim 이 'gpu-cuda' feature 없이 빌드됨. \
             NVIDIA + cuQuantum 환경에서 `cargo build --features gpu-cuda` 또는 \
             maturin develop --features gpu-cuda 로 다시 빌드 필요"
                .into(),
        ))
    }

    /// wgpu Tier-1 density backend 경로 (Cut E).
    ///
    /// 회로의 ApplyGate / ApplyNoise 를 WgpuDensityOp 로 변환 후
    /// `apply_circuit` 에 dispatch.  noise 는 deterministic Kraus
    /// (Aer method=density_matrix 와 동일 의미).
    ///
    /// dynamic 회로 (Reset / IfEq / Measure / IfElse / WhileLoop / ForLoop /
    /// Switch) 와 3-qubit gate (Toffoli, Fredkin) 은 거부 — v0.5.x patch.
    /// MeasureAll 은 ρ 끝의 sampling 으로 처리.
    fn run_wgpu_density(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> Result<(std::collections::HashMap<String, usize>, DensityMatrix<f32>), GpuError> {
        if circuit.has_dynamic() {
            return Err(GpuError::Unsupported(
                "wgpu density: dynamic 회로 (reset / classical control / loops) \
                 는 v0.5.x patch — backend='cpu' + method='density_matrix' 사용"
                    .into(),
            ));
        }
        let mut ops: Vec<WgpuDensityOp> = Vec::new();
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();
        let mut has_measure_all = false;
        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    convert_gate_to_density_ops(gate, targets, &mut ops)?;
                }
                Instruction::ApplyNoise { channel, target } => {
                    let kraus_f32 = channel.kraus_operators::<f32>();
                    ops.push(WgpuDensityOp::Kraus1q {
                        kraus: kraus_f32,
                        target: *target,
                    });
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => has_measure_all = true,
                // 2q correlated Kraus (ApplyNoise2) 는 호출부에서 CPU density 로
                // 라우팅되므로 여기 도달하지 않는다 (up-front 검사).
                _ => unreachable!("dynamic instruction 은 이미 거부됨"),
            }
        }

        let n = circuit.num_qubits();
        let dim = 1usize << n;
        let mut rho_data = vec![Complex::<f32>::new(0.0, 0.0); dim * dim];
        rho_data[0] = Complex::new(1.0, 0.0);

        // v0.5.1: process-wide cached singleton.
        let backend = qsim_gpu::cached_wgpu_density_backend()?;
        backend.apply_circuit(&mut rho_data, n, &ops)?;

        // CPU DensityMatrix wrapper 로 변환.
        let mut rho = DensityMatrix::<f32>::new(n);
        rho.data_mut().copy_from_slice(&rho_data);

        // global_phase: density 에서는 ρ → e^(iλ) ρ e^(-iλ) = ρ — no-op.
        let _ = circuit.global_phase();

        // Sampling: density 의 diagonal 분포에서 RNG.
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };
        let counts = if shots == 0 {
            std::collections::HashMap::new()
        } else if has_measure_all {
            sample_density(&rho, shots, n, &mut rng)
        } else if !explicit_measures.is_empty() {
            sample_density_with_cbit_map(
                &rho,
                shots,
                &explicit_measures,
                circuit.num_cbits(),
                &mut rng,
            )
        } else {
            std::collections::HashMap::new()
        };
        Ok((counts, rho))
    }

    /// Matrix Product State 백엔드 (v0.6.0).
    ///
    /// 작업 흐름:
    /// 1. 회로의 instruction 을 순회하며 [`qsim_mps::Mps`] 에 적용.
    /// 2. 1q gate → `Mps::apply_one_qubit`.
    /// 3. 2q gate → 4×4 matrix 변환 후 `Mps::apply_two_qubit_adjacent`.
    ///    Stage 1 의 인접 제약 (`|q0 - q1| == 1`) 위반 / 3q gate /
    ///    noise / dynamic / `Reset` / `IfEq` / `IfElse` / `WhileLoop` /
    ///    `ForLoop` / `Switch` 는 모두 panic.  Python binding 에서 사전
    ///    검증해 친화 ValueError 로 노출되므로 여기까지 도달하면 사용자
    ///    실수가 아닌 회로 빌더 버그.
    /// 4. 회로 끝에서 `Mps::statevector()` (n ≤ 20 enforced) 로 dense SV
    ///    복원 → 기존 `measurement::sample` / `sample_with_cbit_map` 재사용.
    ///
    /// `final_norm_sq` 는 SVD truncation 후 남은 `<ψ|ψ>` (direct contraction —
    /// 큰 N 안전).  `truncation_error_sum` (v0.6.3) 은 회로 실행 중 누적된
    /// SVD discarded weight (Schollwöck 2011 §4.5.3).  반환 statevector 는
    /// `Option`:
    /// - `Some(_)` — N ≤ 20: 기존 dense SV contract 경로 (회귀 0).
    /// - `None` — N > 20: dense SV 메모리 불가 → counts 만 (sampling-via-MPS).
    ///
    /// v0.6.5: generic over [`qsim_mps::MpsScalar`] (`f32` / `f64`).
    /// Body is the v0.6.3 logic with `Mps<F>` everywhere; gate matrices
    /// flow through `apply_gate_to_mps::<F>` which converts on entry.
    #[allow(clippy::type_complexity)]
    fn run_mps_typed<F: qsim_mps::MpsScalar>(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> (
        std::collections::HashMap<String, usize>,
        Option<StateVector<F>>,
        Option<qsim_mps::Mps<F>>,
        f64,
        f64,
        usize,
    ) {
        self.run_mps_typed_with_provider::<F>(circuit, shots, None)
    }

    /// v0.6.6 Cut 6: run_mps_typed with optional SVD provider injection.
    /// v0.6.7: `Backend::WgpuMps` now uses `run_wgpu_mps` (GPU-resident).
    #[allow(clippy::type_complexity)]
    fn run_mps_typed_with_provider<F: qsim_mps::MpsScalar>(
        &self,
        circuit: &Circuit,
        shots: usize,
        svd_provider: Option<Arc<dyn qsim_mps::MpsSvdProvider<F>>>,
    ) -> (
        std::collections::HashMap<String, usize>,
        Option<StateVector<F>>,
        Option<qsim_mps::Mps<F>>,
        f64,
        f64,
        usize,
    ) {
        let n_qubits = circuit.num_qubits();

        // v0.6.5: detect noise / dynamic instructions and route to the
        // trajectory engine.  Static circuits (no noise, no dynamic ops)
        // take the cheaper v0.6.3 fast path immediately below.
        let has_noise = circuit.instructions().iter().any(|inst| {
            matches!(
                inst,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });
        let has_dynamic = circuit.instructions().iter().any(|inst| {
            matches!(
                inst,
                Instruction::Reset { .. }
                    | Instruction::IfEq { .. }
                    | Instruction::IfElse { .. }
                    | Instruction::WhileLoop { .. }
                    | Instruction::ForLoop { .. }
                    | Instruction::Switch { .. }
            )
        });
        if has_noise || has_dynamic {
            // trajectory 결과는 mixed state → observable 기댓값이 정의되지 않음.
            // mps = None (expectation 미지원).
            let (counts, sv, fnorm, terr, obs) =
                self.run_mps_trajectory_with_provider::<F>(circuit, shots, svd_provider);
            return (counts, sv, None, fnorm, terr, obs);
        }

        let mut mps = qsim_mps::Mps::<F>::with_threshold(
            n_qubits,
            self.max_bond_dim,
            self.mps_trunc_threshold,
        );
        if let Some(provider) = svd_provider {
            mps.set_svd_provider(provider);
        }
        let mut has_measure_all = false;
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();

        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    apply_gate_to_mps::<F>(&mut mps, gate, targets);
                }
                Instruction::ApplyUnitary { .. } => {
                    panic!("{}", UNITARY_UNSUPPORTED_MSG);
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => {
                    has_measure_all = true;
                }
                Instruction::ApplyNoise { .. }
                | Instruction::ApplyNoise2 { .. }
                | Instruction::Reset { .. }
                | Instruction::IfEq { .. }
                | Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => {
                    unreachable!("noise/dynamic ops routed to trajectory engine above");
                }
            }
        }

        // norm_squared() is a direct contraction (O(N · χ³)) — safe for any N.
        let final_norm_sq = mps.norm_squared();
        // v0.6.3: cumulative discarded-weight metric (Schollwöck §4.5.3).
        let truncation_error_sum = mps.truncation_error_sum();

        // Branch: shots == 0.  N ≤ 20 → dense-SV contract (debug + expectation).
        // v0.7: N > 20 → no dense SV (would OOM); keep the MPS so observable
        // expectation (`expectation_pauli`, O(N·χ³)) still works for large-N VQE.
        if shots == 0 {
            let observed = mps.observed_max_bond_dim();
            if n_qubits <= 20 {
                let mps_amplitudes = mps.statevector();
                let mut state: StateVector<F> = StateVector::new(n_qubits);
                state.amplitudes_mut().copy_from_slice(&mps_amplitudes);
                apply_global_phase::<F>(&mut state, circuit.global_phase());
                return (
                    std::collections::HashMap::new(),
                    Some(state),
                    Some(mps),
                    final_norm_sq,
                    truncation_error_sum,
                    observed,
                );
            }
            return (
                std::collections::HashMap::new(),
                None,
                Some(mps),
                final_norm_sq,
                truncation_error_sum,
                observed,
            );
        }

        // shots > 0.  N ≤ 20 → keep the v0.6.0 dense-SV path (cheap + zero
        // regression vs existing measurement::sample / sample_with_cbit_map);
        // N > 20 → MPS-direct sampling (v0.6.1).
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        if n_qubits <= 20 {
            let observed = mps.observed_max_bond_dim();
            let mps_amplitudes = mps.statevector();
            let mut state: StateVector<F> = StateVector::new(n_qubits);
            state.amplitudes_mut().copy_from_slice(&mps_amplitudes);
            apply_global_phase::<F>(&mut state, circuit.global_phase());

            let counts = if has_measure_all {
                measurement::sample(&state, shots, &mut rng)
            } else if !explicit_measures.is_empty() {
                measurement::sample_with_cbit_map(
                    &state,
                    shots,
                    &explicit_measures,
                    circuit.num_cbits(),
                    &mut rng,
                )
            } else {
                std::collections::HashMap::new()
            };
            return (
                counts,
                Some(state),
                Some(mps),
                final_norm_sq,
                truncation_error_sum,
                observed,
            );
        }

        // N > 20: direct MPS sampling.  Bring the MPS to right-canonical form
        // (precondition for sample_once), then loop shots.  Encode outcomes
        // to bitstrings using the same LSB-first / cbit-mapped convention as
        // measurement::sample.
        mps.right_canonicalize();
        // v0.6.5: bonds may shrink during canonicalize when eps > 0 — read
        // observed bond dim AFTER canonicalize to reflect what the sampler
        // sees.  truncation_error_sum is re-read for the same reason.
        let observed = mps.observed_max_bond_dim();
        let truncation_error_sum = mps.truncation_error_sum();
        let raw_counts = mps.sample(shots, &mut rng);

        let counts = if has_measure_all {
            encode_mps_counts_measure_all(&raw_counts, n_qubits)
        } else if !explicit_measures.is_empty() {
            encode_mps_counts_with_cbits(&raw_counts, &explicit_measures, circuit.num_cbits())
        } else {
            std::collections::HashMap::new()
        };

        // v0.7: retain the (right-canonicalised) MPS so observable expectation
        // works at N > 20 even though no dense statevector is built.
        (
            counts,
            None,
            Some(mps),
            final_norm_sq,
            truncation_error_sum,
            observed,
        )
    }

    /// v0.6.7: GPU-resident MPS — all site tensors stay in GPU buffers.
    ///
    /// Gate dispatch:
    /// - 1q gates: GPU in-place shader (zero host transfer).
    /// - 2q gates (adjacent or non-adjacent SWAP chain):
    ///   GPU contraction shader → host SVD → upload new tensors.
    /// - χ < 8 threshold: CPU fallback to avoid GPU dispatch overhead.
    ///
    /// Measurement: GPU hybrid right-canonicalize → download to host MPS →
    /// MPS-direct sampling.
    ///
    /// For noise/dynamic circuits, falls back to CPU MPS trajectory (the
    /// wgpu MPS trajectory is Cut 8c).
    fn run_wgpu_mps(
        &self,
        circuit: &Circuit,
        shots: usize,
    ) -> (
        std::collections::HashMap<String, usize>,
        Option<StateVector<f32>>,
        f64,
        f64,
        usize,
    ) {
        let n_qubits = circuit.num_qubits();

        // Detect noise/dynamic: fall back to CPU MPS trajectory.
        let has_noise = circuit.instructions().iter().any(|inst| {
            matches!(
                inst,
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. }
            )
        });
        let has_dynamic = circuit.instructions().iter().any(|inst| {
            matches!(
                inst,
                Instruction::Reset { .. }
                    | Instruction::IfEq { .. }
                    | Instruction::IfElse { .. }
                    | Instruction::WhileLoop { .. }
                    | Instruction::ForLoop { .. }
                    | Instruction::Switch { .. }
            )
        });
        if has_noise || has_dynamic {
            // v0.6.7: trajectory on GPU MPS is Cut 8c.  For now, fall
            // back to CPU MPS trajectory with host SVD.
            return self.run_mps_trajectory_with_provider::<f32>(circuit, shots, None);
        }

        // Phase 1: Initialize GPU-resident state.
        let gpu_backend =
            qsim_gpu::cached_wgpu_mps_backend().expect("wgpu MPS backend init failed");
        let svd = CpuSvdAdapter;
        let mut mps = qsim_mps::Mps::<f32>::with_threshold(
            n_qubits,
            self.max_bond_dim,
            self.mps_trunc_threshold,
        );
        let mut gpu = GpuMpsTensors::new(gpu_backend, n_qubits, self.max_bond_dim);

        // Upload |0...0⟩.
        for i in 0..n_qubits {
            let data = mps.tensor_data_slice(i);
            let (left, right) = mps.tensor_dims(i);
            gpu.upload_tensor(i, data, left, right);
        }

        // Phase 2: Gate loop.
        let mut has_measure_all = false;
        let mut explicit_measures: Vec<(usize, usize)> = Vec::new();

        for inst in circuit.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    apply_gate_to_gpu_mps(
                        &mut gpu,
                        &mut mps,
                        gate,
                        targets,
                        self.max_bond_dim,
                        self.mps_trunc_threshold,
                        &svd,
                    );
                }
                Instruction::ApplyUnitary { .. } => {
                    panic!("{}", UNITARY_UNSUPPORTED_MSG);
                }
                Instruction::Measure { qubit, cbit } => {
                    explicit_measures.push((*qubit, *cbit));
                }
                Instruction::MeasureAll => {
                    has_measure_all = true;
                }
                Instruction::ApplyNoise { .. }
                | Instruction::ApplyNoise2 { .. }
                | Instruction::Reset { .. }
                | Instruction::IfEq { .. }
                | Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => {
                    unreachable!("noise/dynamic routed to trajectory engine above");
                }
            }
        }

        // Phase 3: Measurement.
        // Sync GPU state back to host MPS for norm + sampling.
        let all_tensors = gpu.download_all();
        for (i, (data, left, right)) in all_tensors.into_iter().enumerate() {
            mps.set_tensor(i, left, right, data);
        }

        let final_norm_sq = mps.norm_squared();
        let truncation_error_sum = mps.truncation_error_sum();

        if shots == 0 {
            assert!(
                n_qubits <= 20,
                "MPS shots=0 requires n_qubits <= 20 for statevector contract"
            );
            let observed = mps.observed_max_bond_dim();
            let mps_amplitudes = mps.statevector();
            let mut state: StateVector<f32> = StateVector::new(n_qubits);
            state.amplitudes_mut().copy_from_slice(&mps_amplitudes);
            apply_global_phase::<f32>(&mut state, circuit.global_phase());
            return (
                std::collections::HashMap::new(),
                Some(state),
                final_norm_sq,
                truncation_error_sum,
                observed,
            );
        }

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        if n_qubits <= 20 {
            let observed = mps.observed_max_bond_dim();
            let mps_amplitudes = mps.statevector();
            let mut state: StateVector<f32> = StateVector::new(n_qubits);
            state.amplitudes_mut().copy_from_slice(&mps_amplitudes);
            apply_global_phase::<f32>(&mut state, circuit.global_phase());

            let counts = if has_measure_all {
                measurement::sample(&state, shots, &mut rng)
            } else if !explicit_measures.is_empty() {
                measurement::sample_with_cbit_map(
                    &state,
                    shots,
                    &explicit_measures,
                    circuit.num_cbits(),
                    &mut rng,
                )
            } else {
                std::collections::HashMap::new()
            };
            return (
                counts,
                Some(state),
                final_norm_sq,
                truncation_error_sum,
                observed,
            );
        }

        // N > 20: right-canonicalize + MPS sampling.
        mps.right_canonicalize();
        let observed = mps.observed_max_bond_dim();
        let truncation_error_sum = mps.truncation_error_sum();
        let raw_counts = mps.sample(shots, &mut rng);

        let counts = if has_measure_all {
            encode_mps_counts_measure_all(&raw_counts, n_qubits)
        } else if !explicit_measures.is_empty() {
            encode_mps_counts_with_cbits(&raw_counts, &explicit_measures, circuit.num_cbits())
        } else {
            std::collections::HashMap::new()
        };

        (counts, None, final_norm_sq, truncation_error_sum, observed)
    }

    /// MPS trajectory dispatch — used by `run_mps_typed` when the circuit
    /// contains `ApplyNoise` or any dynamic op (`Reset` / `IfEq` /
    /// `IfElse` / `WhileLoop` / `ForLoop` / `Switch`).  v0.6.5 Cut 7 —
    /// mirrors the statevector trajectory loop in `run_typed` and the
    /// density `run_typed_density_trajectory`.
    ///
    /// Per shot: fresh `Mps::<F>::with_threshold`, fresh `cbits` register,
    /// then `dispatch_instruction_mps::<F>` walks the instruction list.
    /// At trajectory end the MPS is `right_canonicalize`d once (Risk e
    /// mitigation: per-Kraus canonicalize is O(N · χ³) and not needed
    /// for correctness — `apply_two_qubit_adjacent`'s local SVD restores
    /// canonical form on the touched bond) and the final bitstring is
    /// emitted from accumulated `cbits` (for `Measure`) or per-qubit
    /// `collapse_qubit` (for `MeasureAll`).
    ///
    /// Aggregated metadata: `final_norm_sq` and `truncation_error_sum`
    /// are taken from the **last** trajectory (matches statevector
    /// trajectory's "last state" convention — sufficient for sanity, the
    /// per-trajectory mean is not statistically meaningful for an
    /// individual run).
    /// v0.6.6 Cut 6: trajectory engine with optional SVD provider.  Default
    /// `None` => CPU SVD (matches v0.6.5).  v0.6.7: `Backend::WgpuMps`
    /// uses `run_wgpu_mps` instead; this path is for `CpuMps` only.
    fn run_mps_trajectory_with_provider<F: qsim_mps::MpsScalar>(
        &self,
        circuit: &Circuit,
        shots: usize,
        svd_provider: Option<Arc<dyn qsim_mps::MpsSvdProvider<F>>>,
    ) -> (
        std::collections::HashMap<String, usize>,
        Option<StateVector<F>>,
        f64,
        f64,
        usize,
    ) {
        let n_qubits = circuit.num_qubits();
        let n_cbits = circuit.num_cbits();
        let n_trajectories = shots.max(1);

        let has_measure_all = circuit
            .instructions()
            .iter()
            .any(|i| matches!(i, Instruction::MeasureAll));
        let has_explicit_measure = circuit
            .instructions()
            .iter()
            .any(|i| matches!(i, Instruction::Measure { .. }));

        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_entropy(),
        };

        let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
        let mut last_mps: Option<qsim_mps::Mps<F>> = None;
        let mut last_cbits: Vec<u8> = vec![0; n_cbits];

        for _ in 0..n_trajectories {
            let mut mps = qsim_mps::Mps::<F>::with_threshold(
                n_qubits,
                self.max_bond_dim,
                self.mps_trunc_threshold,
            );
            if let Some(provider) = svd_provider.as_ref() {
                mps.set_svd_provider(Arc::clone(provider));
            }
            let mut cbits: Vec<u8> = vec![0; n_cbits];

            for inst in circuit.instructions() {
                Self::dispatch_instruction_mps::<F>(inst, &mut mps, &mut cbits, &mut rng);
            }

            if shots > 0 && (has_measure_all || has_explicit_measure) {
                let s = if has_measure_all {
                    // MeasureAll already collapsed every qubit and wrote
                    // into cbits[0..n_qubits].  Emit MSB-first.
                    let mut s = String::with_capacity(n_qubits);
                    for q in (0..n_qubits).rev() {
                        let v = if q < cbits.len() { cbits[q] } else { 0 };
                        s.push(if v == 0 { '0' } else { '1' });
                    }
                    s
                } else {
                    // explicit Measure: cbits register is wider than n_qubits.
                    // Emit MSB-first (matches measurement::sample_with_cbit_map).
                    let mut s = String::with_capacity(n_cbits);
                    for &b in cbits.iter().rev() {
                        s.push(if b == 0 { '0' } else { '1' });
                    }
                    s
                };
                *counts.entry(s).or_insert(0) += 1;
            }

            last_cbits = cbits;
            last_mps = Some(mps);
        }

        let last_mps = last_mps.expect("trajectory loop ran at least once");
        let _ = last_cbits;
        let final_norm_sq = last_mps.norm_squared();
        let truncation_error_sum = last_mps.truncation_error_sum();
        let observed = last_mps.observed_max_bond_dim();

        // shots == 0 + noise/dynamic: return the last trajectory's state
        // (same convention as statevector trajectory) and skip counts.
        // shots > 0: hand back the last trajectory's dense state for
        // small-N as a debugging aid (matches v0.6.3 N≤20 dense-SV path);
        // for N>20 we return None.
        let statevector: Option<StateVector<F>> = if n_qubits <= 20 {
            let amps = last_mps.statevector();
            let mut state: StateVector<F> = StateVector::new(n_qubits);
            state.amplitudes_mut().copy_from_slice(&amps);
            apply_global_phase::<F>(&mut state, circuit.global_phase());
            Some(state)
        } else {
            None
        };

        (
            counts,
            statevector,
            final_norm_sq,
            truncation_error_sum,
            observed,
        )
    }

    /// Per-instruction dispatcher used by [`Self::run_mps_trajectory`].
    /// Mirrors [`Self::dispatch_instruction`] (statevector) but routes
    /// `ApplyGate` / `ApplyNoise` / `Measure` / `MeasureAll` / `Reset`
    /// onto the MPS via [`qsim_mps::Mps::collapse_qubit`] /
    /// [`qsim_mps::Mps::apply_one_qubit`] / [`qsim_mps::Mps::normalize`].
    ///
    /// All control-flow ops (`IfEq` / `IfElse` / `WhileLoop` / `ForLoop`
    /// / `Switch`) recurse into the body, reusing the statevector
    /// dispatch's `pack_cbits` helper.  v0.6.5.
    fn dispatch_instruction_mps<F: qsim_mps::MpsScalar>(
        inst: &Instruction,
        mps: &mut qsim_mps::Mps<F>,
        cbits: &mut [u8],
        rng: &mut StdRng,
    ) {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                apply_gate_to_mps::<F>(mps, gate, targets);
            }
            Instruction::ApplyUnitary { .. } => {
                panic!("{}", UNITARY_UNSUPPORTED_MSG);
            }
            Instruction::ApplyNoise { channel, target } => {
                apply_noise_to_mps::<F, _>(mps, channel, *target, rng);
            }
            Instruction::ApplyNoise2 { channel, q0, q1 } => {
                apply_noise2_to_mps::<F, _>(mps, channel, *q0, *q1, rng);
            }
            Instruction::Measure { qubit, cbit } => {
                // Single-qubit measure: needs right-canonical form for
                // single_qubit_probability.  We re-canonicalize before
                // every Measure — the cost is O(N · χ³) but
                // mid-circuit measurements are typically rare.
                mps.right_canonicalize();
                let p1 = mps.single_qubit_probability(*qubit).to_f64().unwrap_or(0.0);
                let r: f64 = rng.gen();
                let outcome = r < p1;
                mps.collapse_qubit(*qubit, outcome);
                if *cbit < cbits.len() {
                    cbits[*cbit] = u8::from(outcome);
                }
            }
            Instruction::MeasureAll => {
                let n = mps.num_qubits();
                mps.right_canonicalize();
                for q in 0..n {
                    let p1 = mps.single_qubit_probability(q).to_f64().unwrap_or(0.0);
                    let r: f64 = rng.gen();
                    let outcome = r < p1;
                    mps.collapse_qubit(q, outcome);
                    if q < cbits.len() {
                        cbits[q] = u8::from(outcome);
                    }
                }
            }
            Instruction::Reset { qubit } => {
                mps.right_canonicalize();
                let p1 = mps.single_qubit_probability(*qubit).to_f64().unwrap_or(0.0);
                let r: f64 = rng.gen();
                let outcome = r < p1;
                mps.collapse_qubit(*qubit, outcome);
                if outcome {
                    let x = Gate::X.matrix_2x2::<f64>();
                    mps.apply_one_qubit(&x, *qubit);
                }
            }
            Instruction::IfEq {
                cbit_indices,
                value,
                body,
            } => {
                if pack_cbits(cbit_indices, cbits) == *value {
                    Self::dispatch_instruction_mps::<F>(body, mps, cbits, rng);
                }
            }
            Instruction::IfElse {
                cbit_indices,
                value,
                then_body,
                else_body,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let body: Option<&[Instruction]> = if packed == *value {
                    Some(then_body.as_slice())
                } else {
                    else_body.as_deref()
                };
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction_mps::<F>(inst, mps, cbits, rng);
                    }
                }
            }
            Instruction::WhileLoop {
                cbit_indices,
                value,
                body,
                max_iters,
            } => {
                for _ in 0..*max_iters {
                    if pack_cbits(cbit_indices, cbits) != *value {
                        break;
                    }
                    for inst in body {
                        Self::dispatch_instruction_mps::<F>(inst, mps, cbits, rng);
                    }
                }
            }
            Instruction::ForLoop { iterations, body } => {
                for _ in 0..*iterations {
                    for inst in body {
                        Self::dispatch_instruction_mps::<F>(inst, mps, cbits, rng);
                    }
                }
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                let packed = pack_cbits(cbit_indices, cbits);
                let mut chosen: Option<&Vec<Instruction>> = None;
                let mut default: Option<&Vec<Instruction>> = None;
                for (label, body) in cases {
                    match label {
                        Some(v) if *v == packed => {
                            chosen = Some(body);
                            break;
                        }
                        None => default = Some(body),
                        _ => {}
                    }
                }
                let body = chosen.or(default);
                if let Some(insts) = body {
                    for inst in insts {
                        Self::dispatch_instruction_mps::<F>(inst, mps, cbits, rng);
                    }
                }
            }
        }
    }
}

/// Apply a single-qubit noise channel to an MPS in trajectory mode (v0.6.5).
///
/// Strategy:
/// - Pauli channels (`BitFlip` / `PhaseFlip` / `Depolarizing`) sample a
///   unitary Pauli gate with the channel's per-branch probability — no
///   renormalization needed.
/// - `AmplitudeDamping` (non-unitary K_0/K_1) uses
///   `p_{K_1} = γ · p(|1⟩_target)` computed via
///   [`qsim_mps::Mps::single_qubit_probability`] (requires
///   right-canonical form, which we ensure here).  After applying the
///   sampled K, the MPS is renormalized via [`qsim_mps::Mps::normalize`].
fn apply_noise_to_mps<F: qsim_mps::MpsScalar, R: Rng>(
    mps: &mut qsim_mps::Mps<F>,
    channel: &qsim_core::NoiseChannel,
    target: usize,
    rng: &mut R,
) {
    use qsim_core::NoiseChannel;
    match channel {
        NoiseChannel::BitFlip { p } => {
            if rng.gen::<f64>() < *p {
                let x = Gate::X.matrix_2x2::<f64>();
                mps.apply_one_qubit(&x, target);
            }
        }
        NoiseChannel::PhaseFlip { p } => {
            if rng.gen::<f64>() < *p {
                let z = Gate::Z.matrix_2x2::<f64>();
                mps.apply_one_qubit(&z, target);
            }
        }
        NoiseChannel::Depolarizing { p } => {
            let r: f64 = rng.gen();
            let p_i_end = 1.0 - 0.75 * p;
            let p_x_end = p_i_end + 0.25 * p;
            let p_y_end = p_x_end + 0.25 * p;
            let gate = if r < p_i_end {
                return;
            } else if r < p_x_end {
                Gate::X
            } else if r < p_y_end {
                Gate::Y
            } else {
                Gate::Z
            };
            let m = gate.matrix_2x2::<f64>();
            mps.apply_one_qubit(&m, target);
        }
        NoiseChannel::AmplitudeDamping { gamma } => {
            // Need right-canonical for single_qubit_probability.
            mps.right_canonicalize();
            let p_one = mps.single_qubit_probability(target).to_f64().unwrap_or(0.0);
            let p_k1 = gamma * p_one;
            let r: f64 = rng.gen();
            use num_complex::Complex;
            if r < p_k1 {
                // K_1 = √γ |0⟩⟨1|.  As 2x2: [[0, √γ], [0, 0]].
                let s = gamma.sqrt();
                let k1: [[Complex<f64>; 2]; 2] = [
                    [Complex::new(0.0, 0.0), Complex::new(s, 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new(0.0, 0.0)],
                ];
                mps.apply_one_qubit(&k1, target);
            } else {
                // K_0 = diag(1, √(1-γ)).
                let g = (1.0 - gamma).sqrt();
                let k0: [[Complex<f64>; 2]; 2] = [
                    [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new(g, 0.0)],
                ];
                mps.apply_one_qubit(&k0, target);
            }
            mps.normalize();
        }
        NoiseChannel::PhaseDamping { gamma } => {
            // K_0 = diag(1, √(1-γ)), K_1 = diag(0, √γ).  p(K_1) = γ·p_one.
            mps.right_canonicalize();
            let p_one = mps.single_qubit_probability(target).to_f64().unwrap_or(0.0);
            let p_k1 = gamma * p_one;
            let r: f64 = rng.gen();
            use num_complex::Complex;
            if r < p_k1 {
                // K_1 = diag(0, √γ) — projects onto |1⟩.
                let s = gamma.sqrt();
                let k1: [[Complex<f64>; 2]; 2] = [
                    [Complex::new(0.0, 0.0), Complex::new(0.0, 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new(s, 0.0)],
                ];
                mps.apply_one_qubit(&k1, target);
            } else {
                // K_0 = diag(1, √(1-γ)).
                let g = (1.0 - gamma).sqrt();
                let k0: [[Complex<f64>; 2]; 2] = [
                    [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new(g, 0.0)],
                ];
                mps.apply_one_qubit(&k0, target);
            }
            mps.normalize();
        }
        NoiseChannel::GeneralizedAmplitudeDamping { gamma, p } => {
            // 4 Kraus.  trajectory: ‖K_iψ‖² from single-qubit marginal (p0,p1).
            mps.right_canonicalize();
            let p1 = mps.single_qubit_probability(target).to_f64().unwrap_or(0.0);
            let p0 = 1.0 - p1;
            let n0 = p * (p0 + (1.0 - gamma) * p1);
            let n1 = p * gamma * p1;
            let n2 = (1.0 - p) * ((1.0 - gamma) * p0 + p1);
            // n3 = (1-p)·γ·p0 — remainder.
            use num_complex::Complex;
            let g = (1.0 - gamma).sqrt();
            let s = gamma.sqrt();
            let z = Complex::new(0.0, 0.0);
            let c = |x: f64| Complex::new(x, 0.0);
            let r: f64 = rng.gen();
            let k: [[Complex<f64>; 2]; 2] = if r < n0 {
                // K_0 ∝ diag(1, √(1-γ)).
                [[c(1.0), z], [z, c(g)]]
            } else if r < n0 + n1 {
                // K_1 ∝ √γ |0⟩⟨1|.
                [[z, c(s)], [z, z]]
            } else if r < n0 + n1 + n2 {
                // K_2 ∝ diag(√(1-γ), 1).
                [[c(g), z], [z, c(1.0)]]
            } else {
                // K_3 ∝ √γ |1⟩⟨0|.
                [[z, z], [c(s), z]]
            };
            mps.apply_one_qubit(&k, target);
            mps.normalize();
        }
        NoiseChannel::Custom { kraus_ops } => {
            // 일반 단일 큐비트 Kraus: ‖K_iψ‖² 를 K_i 적용 클론의 norm 으로
            // 계산 (off-diagonal 까지 정확).  trace-preserving 이면 Σ pᵢ = 1.
            let mut cdf = Vec::with_capacity(kraus_ops.len());
            let mut acc = 0.0_f64;
            for k in kraus_ops.iter() {
                let mut clone = mps.clone();
                clone.apply_one_qubit(k, target);
                acc += clone.norm_squared().max(0.0);
                cdf.push(acc);
            }
            let r: f64 = rng.gen::<f64>() * acc.max(1e-300);
            let idx = cdf
                .iter()
                .position(|&c| r < c)
                .unwrap_or(kraus_ops.len() - 1);
            mps.apply_one_qubit(&kraus_ops[idx], target);
            mps.normalize();
        }
    }
}

/// 2-큐비트 상관 노이즈를 MPS trajectory 로 적용한다 (v0.7.2).
///
/// 각 4×4 Kraus 를 (SWAP chain 으로 임의 q0,q1 지원하는) `apply_two_qubit_to_mps`
/// 로 클론에 적용해 ‖Kᵢψ‖² 를 구하고, 하나를 샘플링·적용·재정규화한다.
fn apply_noise2_to_mps<F: qsim_mps::MpsScalar, R: Rng>(
    mps: &mut qsim_mps::Mps<F>,
    channel: &qsim_core::NoiseChannel2,
    q0: usize,
    q1: usize,
    rng: &mut R,
) {
    let kraus = channel.kraus_operators::<f64>();
    let mut cdf = Vec::with_capacity(kraus.len());
    let mut acc = 0.0_f64;
    for k in &kraus {
        let mut clone = mps.clone();
        apply_two_qubit_to_mps(&mut clone, k, q0, q1);
        acc += clone.norm_squared().max(0.0);
        cdf.push(acc);
    }
    let r: f64 = rng.gen::<f64>() * acc.max(1e-300);
    let idx = cdf.iter().position(|&c| r < c).unwrap_or(kraus.len() - 1);
    apply_two_qubit_to_mps(mps, &kraus[idx], q0, q1);
    mps.normalize();
}

/// MPS-direct sampling 의 `Vec<bool>` outcome (v0.6.3, was u64 in v0.6.1)
/// 을 `MeasureAll` 의 N-width 비트 문자열로 변환.  `measurement::sample`
/// 출력 컨벤션과 동일 — 앞쪽이 큐비트 N-1 (MSB), 끝쪽이 큐비트 0 (LSB).
fn encode_mps_counts_measure_all(
    raw: &std::collections::HashMap<Vec<bool>, usize>,
    n_qubits: usize,
) -> std::collections::HashMap<String, usize> {
    let mut out = std::collections::HashMap::with_capacity(raw.len());
    for (outcome, &count) in raw {
        debug_assert_eq!(outcome.len(), n_qubits);
        let mut s = String::with_capacity(n_qubits);
        for q in (0..n_qubits).rev() {
            s.push(if outcome[q] { '1' } else { '0' });
        }
        out.insert(s, count);
    }
    out
}

/// MPS-direct sampling 의 `Vec<bool>` outcome 을 explicit
/// `Measure(qubit, cbit)` 매핑에 따라 `n_cbits`-width 비트 문자열로 변환.
/// `measurement::sample_with_cbit_map` 와 동일 LSB-first 패킹.
///
/// v0.6.3: `creg` 는 `Vec<bool>` 로 표현 — N>64 도 지원.
fn encode_mps_counts_with_cbits(
    raw: &std::collections::HashMap<Vec<bool>, usize>,
    cbit_map: &[(usize, usize)],
    n_cbits: usize,
) -> std::collections::HashMap<String, usize> {
    let mut out: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for (outcome, &count) in raw {
        let mut creg = vec![false; n_cbits];
        for &(qubit, cbit) in cbit_map {
            // Later writes to the same cbit overwrite earlier writes (Qiskit semantics).
            creg[cbit] = outcome[qubit];
        }
        let mut s = String::with_capacity(n_cbits);
        for c in (0..n_cbits).rev() {
            s.push(if creg[c] { '1' } else { '0' });
        }
        *out.entry(s).or_insert(0) += count;
    }
    out
}

/// `panta-sim` Gate → MPS dispatch.  v0.6.0 Stage 2 Cut 7.
///
/// 1q gate 는 `Gate::matrix_2x2::<f64>()` 그대로 사용.  2q gate 는 LSB
/// (`col = q1·2 + q0`) 컨벤션의 4×4 행렬을 만들어 `apply_two_qubit_adjacent`
/// 에 전달.  v0.6.8: 3q gate (`Toffoli`/`Fredkin`) 는 1q + CNOT 표준 분해
/// ([`decompose_toffoli_to_mps`]) 로 처리 — 각 2q step 이 SVD 를 거치므로 빠듯한
/// chi_max 에선 `truncation_error_sum` 이 누적될 수 있다.
fn apply_gate_to_mps<F: qsim_mps::MpsScalar>(
    mps: &mut qsim_mps::Mps<F>,
    gate: &Gate,
    targets: &[usize],
) {
    use num_complex::Complex;
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            let m = gate.matrix_2x2::<f64>();
            mps.apply_one_qubit(&m, targets[0]);
        }
        Gate::CNOT => {
            let x = Gate::X.matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &x, targets[0], targets[1]);
        }
        Gate::CY => {
            let m = Gate::Y.matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CH => {
            let m = Gate::H.matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CRx(theta) => {
            let m = Gate::Rx(*theta).matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CRy(theta) => {
            let m = Gate::Ry(*theta).matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CRz(theta) => {
            let m = Gate::Rz(*theta).matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CP(lambda) => {
            let m = Gate::P(*lambda).matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CU3(theta, phi, lambda) => {
            let m = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>();
            let phase = Complex::new(gamma.cos(), gamma.sin());
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            apply_controlled_to_mps(mps, &m, targets[0], targets[1]);
        }
        Gate::CZ => {
            let cz = Gate::cz_matrix::<f64>();
            apply_two_qubit_to_mps(mps, &cz, targets[0], targets[1]);
        }
        Gate::SWAP => {
            let swap = Gate::swap_matrix::<f64>();
            apply_two_qubit_to_mps(mps, &swap, targets[0], targets[1]);
        }
        Gate::ISwap => {
            apply_two_qubit_to_mps(mps, &Gate::iswap_matrix::<f64>(), targets[0], targets[1]);
        }
        Gate::Rxx(t) => {
            apply_two_qubit_to_mps(mps, &Gate::rxx_matrix::<f64>(*t), targets[0], targets[1]);
        }
        Gate::Ryy(t) => {
            apply_two_qubit_to_mps(mps, &Gate::ryy_matrix::<f64>(*t), targets[0], targets[1]);
        }
        Gate::Rzz(t) => {
            apply_two_qubit_to_mps(mps, &Gate::rzz_matrix::<f64>(*t), targets[0], targets[1]);
        }
        Gate::Dcx => {
            apply_two_qubit_to_mps(mps, &Gate::dcx_matrix::<f64>(), targets[0], targets[1]);
        }
        Gate::Ecr => {
            apply_two_qubit_to_mps(mps, &Gate::ecr_matrix::<f64>(), targets[0], targets[1]);
        }
        Gate::Rzx(t) => {
            apply_two_qubit_to_mps(mps, &Gate::rzx_matrix::<f64>(*t), targets[0], targets[1]);
        }
        Gate::XxPlusYy(t) => {
            apply_two_qubit_to_mps(
                mps,
                &Gate::xx_plus_yy_matrix::<f64>(*t),
                targets[0],
                targets[1],
            );
        }
        Gate::XxMinusYy(t) => {
            apply_two_qubit_to_mps(
                mps,
                &Gate::xx_minus_yy_matrix::<f64>(*t),
                targets[0],
                targets[1],
            );
        }
        Gate::Toffoli => {
            // v0.6.8: 3-qubit gate 를 1q + 2q (CNOT) 로 분해해 MPS 에 적용.
            // targets = [control1, control2, target].
            decompose_toffoli_to_mps(mps, targets[0], targets[1], targets[2]);
        }
        Gate::Fredkin => {
            // v0.6.8: Fredkin(c, t1, t2) = CNOT(t2→t1) · Toffoli(c, t1, t2) · CNOT(t2→t1).
            // targets = [control, target1, target2].
            let (c, t1, t2) = (targets[0], targets[1], targets[2]);
            let x = Gate::X.matrix_2x2::<f64>();
            apply_controlled_to_mps(mps, &x, t2, t1);
            decompose_toffoli_to_mps(mps, c, t1, t2);
            apply_controlled_to_mps(mps, &x, t2, t1);
        }
    }
}

/// v0.6.8: Toffoli(c1, c2, t) 를 6-CNOT 표준 분해 (Nielsen & Chuang Fig 4.9)
/// 로 MPS 에 적용.  모든 게이트가 1q (H/T/Tdg) 또는 CNOT 이므로 기존 MPS
/// helper 를 재사용하며, 비인접 큐비트는 `apply_controlled_to_mps` 내부의
/// SWAP chain 으로 자동 처리된다.  각 2q gate 가 SVD 를 거치므로 chi_max 가
/// 빠듯하면 `truncation_error_sum` 이 누적될 수 있다.
fn decompose_toffoli_to_mps<F: qsim_mps::MpsScalar>(
    mps: &mut qsim_mps::Mps<F>,
    c1: usize,
    c2: usize,
    t: usize,
) {
    let h = Gate::H.matrix_2x2::<f64>();
    let t_gate = Gate::T.matrix_2x2::<f64>();
    let tdg = Gate::Tdg.matrix_2x2::<f64>();
    let x = Gate::X.matrix_2x2::<f64>();

    mps.apply_one_qubit(&h, t);
    apply_controlled_to_mps(mps, &x, c2, t);
    mps.apply_one_qubit(&tdg, t);
    apply_controlled_to_mps(mps, &x, c1, t);
    mps.apply_one_qubit(&t_gate, t);
    apply_controlled_to_mps(mps, &x, c2, t);
    mps.apply_one_qubit(&tdg, t);
    apply_controlled_to_mps(mps, &x, c1, t);
    mps.apply_one_qubit(&t_gate, c2);
    mps.apply_one_qubit(&t_gate, t);
    apply_controlled_to_mps(mps, &x, c1, c2);
    mps.apply_one_qubit(&h, t);
    mps.apply_one_qubit(&t_gate, c1);
    mps.apply_one_qubit(&tdg, c2);
    apply_controlled_to_mps(mps, &x, c1, c2);
}

/// 2-큐비트 게이트의 일반 4×4 형태를 MPS 에 dispatch.
///
/// `qsim_core::operations::apply_two_qubit_gate(state, matrix, q0, q1)` 와 동일
/// 컨벤션: 4×4 인덱스가 `|q1 q0⟩` 순서, q0 = LSB.  `q0` 와 `q1` 의 입력 순서는
/// 자유 (CZ / SWAP 은 대칭).  비대칭 controlled-1q 는
/// [`apply_controlled_to_mps`] 가 별도 처리.
///
/// v0.6.3 (was v0.6.4 deferred): 비인접 qubit 도 자동 처리 — 내부적으로 SWAP
/// chain 으로 두 큐비트를 인접 site 까지 끌어와 게이트 적용 후 되돌림
/// ([`apply_two_qubit_via_swap_chain`]).  SWAP 자체도 SVD 를 거치므로 chi 가
/// 자라며, 부족한 chi_max 에선 `truncation_error_sum` 이 누적된다.
fn apply_two_qubit_to_mps<F: qsim_mps::MpsScalar>(
    mps: &mut qsim_mps::Mps<F>,
    matrix: &[[num_complex::Complex<f64>; 4]; 4],
    q0: usize,
    q1: usize,
) {
    debug_assert_ne!(q0, q1);
    let lo = q0.min(q1);
    let hi = q0.max(q1);

    // Normalize so that the gate's q0 (LSB) refers to the lower site `lo`
    // and q1 (MSB) to the upper site `hi`.  swap_4x4_axes is its own
    // inverse; applying it unconditionally to "lower=q0, upper=q1" is a
    // no-op only for symmetric gates, so we still gate it.
    let m_norm = if (lo, hi) == (q0, q1) {
        *matrix
    } else {
        swap_4x4_axes(matrix)
    };

    apply_two_qubit_via_swap_chain(mps, &m_norm, lo, hi);
}

/// Controlled-1q (CNOT/CY/CH/CRx/CRy/CRz/CP/CU3/CU) → MPS.
///
/// Builds the LSB-ordered 4×4 matrix where:
/// - `ctrl < tgt` (control = lower site = q0): U is applied to q1 when q0 = 1.
/// - `ctrl > tgt` (control = higher site = q1): U is applied to q0 when q1 = 1.
fn apply_controlled_to_mps<F: qsim_mps::MpsScalar>(
    mps: &mut qsim_mps::Mps<F>,
    u: &[[num_complex::Complex<f64>; 2]; 2],
    ctrl: usize,
    tgt: usize,
) {
    use num_complex::Complex;
    debug_assert_ne!(ctrl, tgt);
    let lo = ctrl.min(tgt);
    let hi = ctrl.max(tgt);
    let zero = Complex::new(0.0, 0.0);
    let one = Complex::new(1.0, 0.0);
    let mut m = [[zero; 4]; 4];
    if ctrl == hi {
        // q1 (upper) = control, q0 (lower) = target.  Identity on (q0=*) when
        // q1 = 0; apply U to q0 when q1 = 1.
        m[0][0] = one;
        m[1][1] = one;
        m[2][2] = u[0][0];
        m[2][3] = u[0][1];
        m[3][2] = u[1][0];
        m[3][3] = u[1][1];
    } else {
        // q0 (lower) = control, q1 (upper) = target.  Identity on (q1=*) when
        // q0 = 0; apply U to q1 when q0 = 1.
        m[0][0] = one;
        m[2][2] = one;
        m[1][1] = u[0][0];
        m[1][3] = u[0][1];
        m[3][1] = u[1][0];
        m[3][3] = u[1][1];
    }
    // v0.6.3: 비인접 ctrl/tgt 도 internal SWAP chain 으로 처리.
    apply_two_qubit_via_swap_chain(mps, &m, lo, hi);
}

/// Apply a 4×4 gate `matrix` (in `|hi lo⟩`-LSB convention) to qubits
/// `lo` and `hi` (`lo < hi`) via internal SWAP chain when they are not
/// adjacent.  v0.6.3 — replaces the v0.6.0 hard-fail on non-adjacent
/// 2q gates (originally deferred to v0.6.4).
///
/// Algorithm:
/// 1. Move the upper qubit `hi` down to site `lo + 1` by applying SWAPs
///    at sites `(lo+1, lo+2), (lo+2, lo+3), ..., (hi-1, hi)` in reverse.
///    Now logical qubit `hi` lives at physical site `lo + 1` and the
///    sites in between hold the original logical qubits `lo+1..hi-1`
///    shifted up by one (their order among themselves is preserved).
/// 2. Apply `matrix` to the now-adjacent pair `(lo, lo+1)`.
/// 3. Undo the SWAP chain in the reverse order, restoring every other
///    qubit to its original site.
///
/// Each SWAP itself goes through `apply_two_qubit_adjacent`, which uses
/// SVD and may truncate against `max_bond_dim` — this is the price of
/// long-range gates.  The cumulative discarded weight is reflected in
/// `Mps::truncation_error_sum()`.  For tight `chi_max` the user should
/// keep long-range gates rare; the example
/// `examples/mps/qaoa_maxcut_ring.py` demonstrates a workload where
/// truncation stays small even with one wraparound edge.
fn apply_two_qubit_via_swap_chain<F: qsim_mps::MpsScalar>(
    mps: &mut qsim_mps::Mps<F>,
    matrix: &[[num_complex::Complex<f64>; 4]; 4],
    lo: usize,
    hi: usize,
) {
    debug_assert!(lo < hi);
    if hi - lo == 1 {
        mps.apply_two_qubit_adjacent(matrix, lo);
        return;
    }
    let swap = swap_matrix_4x4();
    // Step 1: move qubit `hi` down to site `lo + 1`.
    for s in (lo + 1..hi).rev() {
        mps.apply_two_qubit_adjacent(&swap, s);
    }
    // Step 2: apply the gate at the now-adjacent pair (lo, lo + 1).
    mps.apply_two_qubit_adjacent(matrix, lo);
    // Step 3: undo the SWAP chain.
    for s in lo + 1..hi {
        mps.apply_two_qubit_adjacent(&swap, s);
    }
}

/// v0.6.7: adapter — bridges `qsim_gpu::GpuSvdProvider` to
/// `qsim_mps::CpuSvdProvider`.  Used by `run_wgpu_mps` to provide host
/// SVD to `GpuMpsTensors` without the gpu crate depending on qsim-mps.
#[derive(Debug, Default, Clone, Copy)]
struct CpuSvdAdapter;

impl GpuSvdProvider for CpuSvdAdapter {
    fn thin_svd(
        &self,
        m_row_major: &[Complex<f32>],
        rows: usize,
        cols: usize,
        max_keep: usize,
        trunc_threshold: f64,
    ) -> GpuSvdOutput {
        use qsim_mps::MpsSvdProvider as _;
        let out =
            qsim_mps::CpuSvdProvider.thin_svd(m_row_major, rows, cols, max_keep, trunc_threshold);
        GpuSvdOutput {
            u_row_major: out.u_row_major,
            s: out.s,
            vt_row_major: out.vt_row_major,
            trunc_error_sq: out.trunc_error_sq,
            keep: out.keep,
        }
    }
}

/// v0.6.7: dispatch a gate to the GPU-resident MPS, with CPU fallback
/// for small χ.
fn apply_gate_to_gpu_mps(
    gpu: &mut GpuMpsTensors,
    mps: &mut qsim_mps::Mps<f32>,
    gate: &Gate,
    targets: &[usize],
    max_bond_dim: usize,
    trunc_threshold: f64,
    svd: &dyn GpuSvdProvider,
) {
    match gate {
        // One-qubit gates.
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            let m = gate.matrix_2x2::<f64>();
            gpu.apply_one_qubit(targets[0], &m);
            // Update host bond dims (1q doesn't change bonds).
        }
        // Two-qubit gates — dispatch via GPU.
        Gate::CNOT => {
            let u = Gate::X.matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CY => {
            let u = Gate::Y.matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CH => {
            let u = Gate::H.matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CRx(theta) => {
            let u = Gate::Rx(*theta).matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CRy(theta) => {
            let u = Gate::Ry(*theta).matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CRz(theta) => {
            let u = Gate::Rz(*theta).matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CP(lambda) => {
            let u = Gate::P(*lambda).matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CU3(theta, phi, lambda) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u_base = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>();
            let phase = Complex::new(gamma.cos(), gamma.sin());
            let u = [
                [u_base[0][0] * phase, u_base[0][1] * phase],
                [u_base[1][0] * phase, u_base[1][1] * phase],
            ];
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &u,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::CZ => {
            let cz = Gate::cz_matrix::<f64>();
            dispatch_2q_to_gpu_mps(
                gpu,
                mps,
                &cz,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::SWAP => {
            let swap = Gate::swap_matrix::<f64>();
            dispatch_2q_to_gpu_mps(
                gpu,
                mps,
                &swap,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::ISwap
        | Gate::Rxx(_)
        | Gate::Ryy(_)
        | Gate::Rzz(_)
        | Gate::Dcx
        | Gate::Ecr
        | Gate::Rzx(_)
        | Gate::XxPlusYy(_)
        | Gate::XxMinusYy(_) => {
            let m = match gate {
                Gate::ISwap => Gate::iswap_matrix::<f64>(),
                Gate::Rxx(t) => Gate::rxx_matrix::<f64>(*t),
                Gate::Ryy(t) => Gate::ryy_matrix::<f64>(*t),
                Gate::Rzz(t) => Gate::rzz_matrix::<f64>(*t),
                Gate::Dcx => Gate::dcx_matrix::<f64>(),
                Gate::Ecr => Gate::ecr_matrix::<f64>(),
                Gate::Rzx(t) => Gate::rzx_matrix::<f64>(*t),
                Gate::XxPlusYy(t) => Gate::xx_plus_yy_matrix::<f64>(*t),
                Gate::XxMinusYy(t) => Gate::xx_minus_yy_matrix::<f64>(*t),
                _ => unreachable!(),
            };
            dispatch_2q_to_gpu_mps(
                gpu,
                mps,
                &m,
                targets[0],
                targets[1],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::Toffoli => {
            // v0.6.8: 1q + CNOT 분해 (CPU MPS 와 동일 시퀀스, GPU helper 사용).
            decompose_toffoli_to_gpu_mps(
                gpu,
                mps,
                targets[0],
                targets[1],
                targets[2],
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
        Gate::Fredkin => {
            let (c, t1, t2) = (targets[0], targets[1], targets[2]);
            let x = Gate::X.matrix_2x2::<f64>();
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &x,
                t2,
                t1,
                max_bond_dim,
                trunc_threshold,
                svd,
            );
            decompose_toffoli_to_gpu_mps(gpu, mps, c, t1, t2, max_bond_dim, trunc_threshold, svd);
            dispatch_controlled_to_gpu_mps(
                gpu,
                mps,
                &x,
                t2,
                t1,
                max_bond_dim,
                trunc_threshold,
                svd,
            );
        }
    }
}

/// v0.6.8: GPU MPS 용 Toffoli 분해 (6-CNOT 표준, [`decompose_toffoli_to_mps`] 와 동일).
#[allow(clippy::too_many_arguments)]
fn decompose_toffoli_to_gpu_mps(
    gpu: &mut GpuMpsTensors,
    mps: &mut qsim_mps::Mps<f32>,
    c1: usize,
    c2: usize,
    t: usize,
    max_bond_dim: usize,
    trunc_threshold: f64,
    svd: &dyn GpuSvdProvider,
) {
    let h = Gate::H.matrix_2x2::<f64>();
    let t_gate = Gate::T.matrix_2x2::<f64>();
    let tdg = Gate::Tdg.matrix_2x2::<f64>();
    let x = Gate::X.matrix_2x2::<f64>();
    let cx = |gpu: &mut GpuMpsTensors, mps: &mut qsim_mps::Mps<f32>, c: usize, tg: usize| {
        dispatch_controlled_to_gpu_mps(gpu, mps, &x, c, tg, max_bond_dim, trunc_threshold, svd);
    };

    gpu.apply_one_qubit(t, &h);
    cx(gpu, mps, c2, t);
    gpu.apply_one_qubit(t, &tdg);
    cx(gpu, mps, c1, t);
    gpu.apply_one_qubit(t, &t_gate);
    cx(gpu, mps, c2, t);
    gpu.apply_one_qubit(t, &tdg);
    cx(gpu, mps, c1, t);
    gpu.apply_one_qubit(c2, &t_gate);
    gpu.apply_one_qubit(t, &t_gate);
    cx(gpu, mps, c1, c2);
    gpu.apply_one_qubit(t, &h);
    gpu.apply_one_qubit(c1, &t_gate);
    gpu.apply_one_qubit(c2, &tdg);
    cx(gpu, mps, c1, c2);
}

/// Dispatch a controlled-1q gate to GPU MPS.
#[allow(clippy::too_many_arguments)]
fn dispatch_controlled_to_gpu_mps(
    gpu: &mut GpuMpsTensors,
    mps: &mut qsim_mps::Mps<f32>,
    u: &[[Complex<f64>; 2]; 2],
    ctrl: usize,
    tgt: usize,
    max_bond_dim: usize,
    trunc_threshold: f64,
    svd: &dyn GpuSvdProvider,
) {
    let lo = ctrl.min(tgt);
    let hi = ctrl.max(tgt);
    let zero = Complex::new(0.0, 0.0);
    let one = Complex::new(1.0, 0.0);
    let mut m = [[zero; 4]; 4];
    if ctrl == hi {
        m[0][0] = one;
        m[1][1] = one;
        m[2][2] = u[0][0];
        m[2][3] = u[0][1];
        m[3][2] = u[1][0];
        m[3][3] = u[1][1];
    } else {
        m[0][0] = one;
        m[2][2] = one;
        m[1][1] = u[0][0];
        m[1][3] = u[0][1];
        m[3][1] = u[1][0];
        m[3][3] = u[1][1];
    }
    dispatch_2q_gate_on_gpu(gpu, mps, &m, lo, hi, max_bond_dim, trunc_threshold, svd);
}

/// Dispatch a 2q gate (4x4 matrix) to GPU MPS, handling qubit ordering.
#[allow(clippy::too_many_arguments)]
fn dispatch_2q_to_gpu_mps(
    gpu: &mut GpuMpsTensors,
    mps: &mut qsim_mps::Mps<f32>,
    matrix: &[[Complex<f64>; 4]; 4],
    q0: usize,
    q1: usize,
    max_bond_dim: usize,
    trunc_threshold: f64,
    svd: &dyn GpuSvdProvider,
) {
    let lo = q0.min(q1);
    let hi = q0.max(q1);
    let m_norm = if (lo, hi) == (q0, q1) {
        *matrix
    } else {
        swap_4x4_axes(matrix)
    };
    dispatch_2q_gate_on_gpu(
        gpu,
        mps,
        &m_norm,
        lo,
        hi,
        max_bond_dim,
        trunc_threshold,
        svd,
    );
}

/// Core 2q gate dispatch: GPU path with χ<8 CPU fallback.
#[allow(clippy::too_many_arguments)]
fn dispatch_2q_gate_on_gpu(
    gpu: &mut GpuMpsTensors,
    mps: &mut qsim_mps::Mps<f32>,
    matrix: &[[Complex<f64>; 4]; 4],
    lo: usize,
    hi: usize,
    max_bond_dim: usize,
    trunc_threshold: f64,
    svd: &dyn GpuSvdProvider,
) {
    // Collect all sites involved (adjacent pair, or the full SWAP range).
    let involved: Vec<usize> = (lo..=hi).collect();
    let max_chi = gpu.max_chi_at(&involved);

    if max_chi < GPU_CHI_THRESHOLD {
        // CPU fallback: download, apply on host MPS, re-upload.
        for &site in &involved {
            let (data, left, right) = gpu.download_tensor(site);
            mps.set_tensor(site, left, right, data);
        }
        apply_two_qubit_via_swap_chain(mps, matrix, lo, hi);
        for &site in &involved {
            let data = mps.tensor_data_slice(site).to_vec();
            let (left, right) = mps.tensor_dims(site);
            gpu.upload_tensor(site, &data, left, right);
        }
    } else {
        // GPU path.
        let trunc_err =
            gpu.apply_two_qubit_gate(lo, hi, matrix, max_bond_dim, trunc_threshold, svd);
        mps.add_truncation_error(trunc_err);
        // Sync bond dims back to host MPS so metadata stays consistent.
        for &site in &involved {
            let (left, right) = gpu.bond_dims(site);
            // We don't update MPS tensor data yet — only metadata.
            // The actual data will be downloaded during measurement.
            // But we need to keep mps bond dims in sync for norm_squared etc.
            // We create a zero-length placeholder — set_tensor would be wasteful.
            // Actually, we don't need to update MPS tensors during the gate loop.
            // The MPS metadata (truncation_error_sum) is already updated via
            // add_truncation_error.  Bond dims in MPS won't match GPU until
            // Phase 3 download.  This is fine — we only use MPS for
            // measurement after download.
            let _ = (left, right); // bond dims tracked on GPU side
        }
    }
}

/// SWAP gate as a 4×4 matrix in the `|q1 q0⟩` LSB convention.  Used
/// only by the long-range 2q dispatch path; lifted out to avoid
/// recomputing it inside the hot loop.
fn swap_matrix_4x4() -> [[num_complex::Complex<f64>; 4]; 4] {
    use num_complex::Complex;
    let z = Complex::new(0.0, 0.0);
    let o = Complex::new(1.0, 0.0);
    [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]]
}

/// Swap `(q0, q1)` axes of a 4×4 matrix that uses the `|q1 q0⟩` indexing
/// convention.  Equivalent to conjugating with the SWAP permutation matrix.
fn swap_4x4_axes(m: &[[num_complex::Complex<f64>; 4]; 4]) -> [[num_complex::Complex<f64>; 4]; 4] {
    use num_complex::Complex;
    // perm[i] = index obtained by swapping bits 0 and 1 of i.
    const PERM: [usize; 4] = [0, 2, 1, 3];
    let mut out = [[Complex::new(0.0, 0.0); 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            out[i][j] = m[PERM[i]][PERM[j]];
        }
    }
    out
}

/// panta-sim Gate → CudaGateOp 변환 (Cut G, feature `gpu-cuda`).
///
/// Toffoli / Fredkin 은 cuStateVec 의 nTargets=3 으로 가능하지만 v0.5.0 minimum
/// scope 외 — 사용자가 transpile 후 호출.
#[cfg(feature = "gpu-cuda")]
fn convert_gate_to_cuda_ops(
    gate: &Gate,
    targets: &[usize],
    ops: &mut Vec<qsim_gpu::cuda::CudaGateOp>,
) -> Result<(), GpuError> {
    use qsim_gpu::cuda::CudaGateOp;
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            ops.push(CudaGateOp::Single {
                matrix: gate.matrix_2x2::<f32>(),
                target: targets[0],
            });
            Ok(())
        }
        Gate::CNOT => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::X.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CZ => {
            ops.push(CudaGateOp::Two {
                matrix: Gate::cz_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::SWAP => {
            ops.push(CudaGateOp::Two {
                matrix: Gate::swap_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::ISwap
        | Gate::Rxx(_)
        | Gate::Ryy(_)
        | Gate::Rzz(_)
        | Gate::Dcx
        | Gate::Ecr
        | Gate::Rzx(_)
        | Gate::XxPlusYy(_)
        | Gate::XxMinusYy(_) => {
            let matrix = match gate {
                Gate::ISwap => Gate::iswap_matrix::<f32>(),
                Gate::Rxx(t) => Gate::rxx_matrix::<f32>(*t),
                Gate::Ryy(t) => Gate::ryy_matrix::<f32>(*t),
                Gate::Rzz(t) => Gate::rzz_matrix::<f32>(*t),
                Gate::Dcx => Gate::dcx_matrix::<f32>(),
                Gate::Ecr => Gate::ecr_matrix::<f32>(),
                Gate::Rzx(t) => Gate::rzx_matrix::<f32>(*t),
                Gate::XxPlusYy(t) => Gate::xx_plus_yy_matrix::<f32>(*t),
                Gate::XxMinusYy(t) => Gate::xx_minus_yy_matrix::<f32>(*t),
                _ => unreachable!(),
            };
            ops.push(CudaGateOp::Two {
                matrix,
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::CY => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::Y.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CH => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::H.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRx(theta) => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::Rx(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRy(theta) => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::Ry(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRz(theta) => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::Rz(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CP(lambda) => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::P(*lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU3(theta, phi, lambda) => {
            ops.push(CudaGateOp::Controlled1q {
                matrix: Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>();
            let phase = Complex::new(gamma.cos() as f32, gamma.sin() as f32);
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            ops.push(CudaGateOp::Controlled1q {
                matrix: m,
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::Toffoli => {
            // v0.5.10: cuStateVec native (n_controls=2 + X matrix).
            if targets.len() != 3 {
                return Err(GpuError::Unsupported(format!(
                    "Toffoli expects 3 targets, got {}",
                    targets.len()
                )));
            }
            ops.push(CudaGateOp::Toffoli {
                c0: targets[0],
                c1: targets[1],
                tgt: targets[2],
            });
            Ok(())
        }
        Gate::Fredkin => {
            // v0.5.10: cuStateVec native (n_controls=1 + SWAP matrix).
            if targets.len() != 3 {
                return Err(GpuError::Unsupported(format!(
                    "Fredkin expects 3 targets, got {}",
                    targets.len()
                )));
            }
            ops.push(CudaGateOp::Fredkin {
                ctrl: targets[0],
                t0: targets[1],
                t1: targets[2],
            });
            Ok(())
        }
    }
}

/// v0.5.12: f64 변종 convert.  동일 패턴이지만 matrix 가 f64 + CudaGateOpF64.
#[cfg(feature = "gpu-cuda")]
fn convert_gate_to_cuda_ops_f64(
    gate: &Gate,
    targets: &[usize],
    ops: &mut Vec<qsim_gpu::cuda::CudaGateOpF64>,
) -> Result<(), GpuError> {
    use qsim_gpu::cuda::CudaGateOpF64;
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            ops.push(CudaGateOpF64::Single {
                matrix: gate.matrix_2x2::<f64>(),
                target: targets[0],
            });
            Ok(())
        }
        Gate::CNOT => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::X.matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CZ => {
            ops.push(CudaGateOpF64::Two {
                matrix: Gate::cz_matrix::<f64>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::SWAP => {
            ops.push(CudaGateOpF64::Two {
                matrix: Gate::swap_matrix::<f64>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::ISwap
        | Gate::Rxx(_)
        | Gate::Ryy(_)
        | Gate::Rzz(_)
        | Gate::Dcx
        | Gate::Ecr
        | Gate::Rzx(_)
        | Gate::XxPlusYy(_)
        | Gate::XxMinusYy(_) => {
            let matrix = match gate {
                Gate::ISwap => Gate::iswap_matrix::<f64>(),
                Gate::Rxx(t) => Gate::rxx_matrix::<f64>(*t),
                Gate::Ryy(t) => Gate::ryy_matrix::<f64>(*t),
                Gate::Rzz(t) => Gate::rzz_matrix::<f64>(*t),
                Gate::Dcx => Gate::dcx_matrix::<f64>(),
                Gate::Ecr => Gate::ecr_matrix::<f64>(),
                Gate::Rzx(t) => Gate::rzx_matrix::<f64>(*t),
                Gate::XxPlusYy(t) => Gate::xx_plus_yy_matrix::<f64>(*t),
                Gate::XxMinusYy(t) => Gate::xx_minus_yy_matrix::<f64>(*t),
                _ => unreachable!(),
            };
            ops.push(CudaGateOpF64::Two {
                matrix,
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::CY => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::Y.matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CH => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::H.matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRx(theta) => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::Rx(*theta).matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRy(theta) => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::Ry(*theta).matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRz(theta) => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::Rz(*theta).matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CP(lambda) => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::P(*lambda).matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU3(theta, phi, lambda) => {
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f64>();
            let phase = Complex::new(gamma.cos(), gamma.sin());
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            ops.push(CudaGateOpF64::Controlled1q {
                matrix: m,
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::Toffoli => {
            if targets.len() != 3 {
                return Err(GpuError::Unsupported(format!(
                    "Toffoli expects 3 targets, got {}",
                    targets.len()
                )));
            }
            ops.push(CudaGateOpF64::Toffoli {
                c0: targets[0],
                c1: targets[1],
                tgt: targets[2],
            });
            Ok(())
        }
        Gate::Fredkin => {
            if targets.len() != 3 {
                return Err(GpuError::Unsupported(format!(
                    "Fredkin expects 3 targets, got {}",
                    targets.len()
                )));
            }
            ops.push(CudaGateOpF64::Fredkin {
                ctrl: targets[0],
                t0: targets[1],
                t1: targets[2],
            });
            Ok(())
        }
    }
}

// v0.5.20: panta-sim 안의 panic stderr 출력 억제.  catch_unwind 만으로는
// default panic hook 의 stderr 출력을 못 막아 사용자가 친화 ValueError 와
// 동시에 `thread '<unnamed>' panicked at ...` 메시지를 보게 됨.
//
// 해결: thread-local guard 로 panta-sim 의 catch_unwind 영역 안 panic 만
// silent 처리.  외부 panic (panta-sim 외부 또는 사용자 코드 panic) 은
// 정상 출력 유지.
thread_local! {
    static SUPPRESS_PANIC_OUTPUT: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}

/// v0.5.20: panic hook 첫 호출 시 1회 install — wgpu panic stderr 억제.
fn install_panta_sim_panic_hook() {
    static INSTALL: std::sync::Once = std::sync::Once::new();
    INSTALL.call_once(|| {
        let prev = std::panic::take_hook();
        std::panic::set_hook(Box::new(move |info| {
            let suppress = SUPPRESS_PANIC_OUTPUT.with(|c| c.get());
            if !suppress {
                prev(info);
            }
            // suppress=true 면 silent — catch_unwind 가 잡고 친화 ValueError 로 변환.
        }));
    });
}

/// v0.5.20: RAII guard — catch_unwind 영역 진입 시 suppress=true, 빠질 때 false.
/// panic 으로 unwind 되어도 Drop 자동 호출되어 flag 정상 복귀.
struct SuppressPanicGuard;

impl SuppressPanicGuard {
    fn new() -> Self {
        SUPPRESS_PANIC_OUTPUT.with(|c| c.set(true));
        Self
    }
}

impl Drop for SuppressPanicGuard {
    fn drop(&mut self) {
        SUPPRESS_PANIC_OUTPUT.with(|c| c.set(false));
    }
}

/// wgpu validation error 같은 panic payload 를 사용자 친화적 GpuError 로 변환 (v0.5.1).
///
/// wgpu-core 가 validation 실패 시 default handler 로 panic 한다 — caller 가
/// `catch_unwind` 로 잡아 이 함수에 panic payload 전달.  Python 측에서 PyValueError
/// 로 떨어져 일반 `except Exception` / `except ValueError` 로 잡힘.
///
/// **v0.5.19**: OOM (Out of Memory) panic 의 친화 메시지 추가 — N / sv_size /
/// 다른 프로세스 종료 권장 등의 가이드 포함.
fn panic_to_gpu_error(context: &str, payload: Box<dyn std::any::Any + Send>) -> GpuError {
    let msg = if let Some(s) = payload.downcast_ref::<String>() {
        s.clone()
    } else if let Some(s) = payload.downcast_ref::<&'static str>() {
        (*s).to_string()
    } else {
        "(non-string panic payload)".to_string()
    };
    // 흔한 wgpu validation error 에 대해 사용자 친화 안내 추가.
    let hint = if is_oom_message(&msg) {
        " — GPU/unified memory 부족.  다른 프로세스 종료 후 재시도 또는 \
         method='statevector' (CPU 호스트 RAM) 사용 권장.  \
         사용자 환경에 따라 N 별 sv 크기는 N=28→2 GiB, N=29→4 GiB, \
         N=30→8 GiB, N=31→16 GiB, N=32→32 GiB (f32) — \
         intermediate buffer 추가 1~2 GiB 필요"
    } else if msg.contains("Buffer size") || msg.contains("max buffer size") {
        " — 회로 크기가 GPU buffer 한계 초과.  더 작은 N 으로 시도하거나 method='statevector' (CPU) 사용."
    } else if msg.contains("dispatch group size") || msg.contains("workgroups_per_dimension") {
        " — workgroup dispatch 한계 초과.  실 GPU 에선 보통 풀려있음 — driver 업데이트 시도, 또는 method='statevector' (CPU) 사용."
    } else if msg.contains("buffer_binding_size") || msg.contains("Buffer binding") {
        " — storage buffer binding 한계 초과.  더 작은 N 으로 시도하거나 method='statevector' (CPU) 사용."
    } else {
        ""
    };
    GpuError::Other(format!(
        "{context} panic: {msg}{hint}\n  (이 에러는 v0.5.1 부터 PyValueError 로 노출됨)"
    ))
}

/// v0.5.19: wgpu OOM panic message 감지.  AMD / NVIDIA / Apple Metal / lavapipe
/// 의 driver 별 OOM 메시지 형식이 약간 다름 — 가장 흔한 패턴들 모두 매칭.
fn is_oom_message(msg: &str) -> bool {
    let lower = msg.to_ascii_lowercase();
    lower.contains("out of memory")
        || lower.contains("outofmemory")
        || lower.contains("oom")
        || lower.contains("not enough memory")
        || lower.contains("memory allocation failed")
}

/// panta-sim Gate → WgpuDensityOp 변환 (Cut E).
fn convert_gate_to_density_ops(
    gate: &Gate,
    targets: &[usize],
    ops: &mut Vec<WgpuDensityOp>,
) -> Result<(), GpuError> {
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            ops.push(WgpuDensityOp::Single {
                matrix: gate.matrix_2x2::<f32>(),
                target: targets[0],
            });
            Ok(())
        }
        Gate::CNOT => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::X.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CZ => {
            ops.push(WgpuDensityOp::Two {
                matrix: Gate::cz_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::SWAP => {
            ops.push(WgpuDensityOp::Two {
                matrix: Gate::swap_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::ISwap
        | Gate::Rxx(_)
        | Gate::Ryy(_)
        | Gate::Rzz(_)
        | Gate::Dcx
        | Gate::Ecr
        | Gate::Rzx(_)
        | Gate::XxPlusYy(_)
        | Gate::XxMinusYy(_) => {
            let matrix = match gate {
                Gate::ISwap => Gate::iswap_matrix::<f32>(),
                Gate::Rxx(t) => Gate::rxx_matrix::<f32>(*t),
                Gate::Ryy(t) => Gate::ryy_matrix::<f32>(*t),
                Gate::Rzz(t) => Gate::rzz_matrix::<f32>(*t),
                Gate::Dcx => Gate::dcx_matrix::<f32>(),
                Gate::Ecr => Gate::ecr_matrix::<f32>(),
                Gate::Rzx(t) => Gate::rzx_matrix::<f32>(*t),
                Gate::XxPlusYy(t) => Gate::xx_plus_yy_matrix::<f32>(*t),
                Gate::XxMinusYy(t) => Gate::xx_minus_yy_matrix::<f32>(*t),
                _ => unreachable!(),
            };
            ops.push(WgpuDensityOp::Two {
                matrix,
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::CY => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::Y.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CH => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::H.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRx(theta) => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::Rx(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRy(theta) => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::Ry(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRz(theta) => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::Rz(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CP(lambda) => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::P(*lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU3(theta, phi, lambda) => {
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>();
            let phase = Complex::new(gamma.cos() as f32, gamma.sin() as f32);
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            ops.push(WgpuDensityOp::Controlled1q {
                matrix: m,
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::Toffoli | Gate::Fredkin => Err(GpuError::Unsupported(format!(
            "wgpu density: 3-qubit gate {gate:?} 는 v0.5.x — backend='cpu' 사용"
        ))),
    }
}

/// panta-sim Gate → WgpuGateOp 변환 (Cut D.4).
///
/// 1q gate → Single, controlled-1q (CNOT/CY/CH/CRx/CRy/CRz/CP/CU3/CU) →
/// Controlled1q, 2q (CZ/SWAP) → Two.  Toffoli / Fredkin 은 명시 거부 (v0.5.x).
fn convert_gate_to_wgpu_ops(
    gate: &Gate,
    targets: &[usize],
    ops: &mut Vec<WgpuGateOp>,
) -> Result<(), GpuError> {
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            ops.push(WgpuGateOp::Single {
                matrix: gate.matrix_2x2::<f32>(),
                target: targets[0],
            });
            Ok(())
        }
        Gate::CNOT => {
            let m = Gate::X.matrix_2x2::<f32>();
            ops.push(WgpuGateOp::Controlled1q {
                matrix: m,
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CZ => {
            ops.push(WgpuGateOp::Two {
                matrix: Gate::cz_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::SWAP => {
            ops.push(WgpuGateOp::Two {
                matrix: Gate::swap_matrix::<f32>(),
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::ISwap
        | Gate::Rxx(_)
        | Gate::Ryy(_)
        | Gate::Rzz(_)
        | Gate::Dcx
        | Gate::Ecr
        | Gate::Rzx(_)
        | Gate::XxPlusYy(_)
        | Gate::XxMinusYy(_) => {
            let matrix = match gate {
                Gate::ISwap => Gate::iswap_matrix::<f32>(),
                Gate::Rxx(t) => Gate::rxx_matrix::<f32>(*t),
                Gate::Ryy(t) => Gate::ryy_matrix::<f32>(*t),
                Gate::Rzz(t) => Gate::rzz_matrix::<f32>(*t),
                Gate::Dcx => Gate::dcx_matrix::<f32>(),
                Gate::Ecr => Gate::ecr_matrix::<f32>(),
                Gate::Rzx(t) => Gate::rzx_matrix::<f32>(*t),
                Gate::XxPlusYy(t) => Gate::xx_plus_yy_matrix::<f32>(*t),
                Gate::XxMinusYy(t) => Gate::xx_minus_yy_matrix::<f32>(*t),
                _ => unreachable!(),
            };
            ops.push(WgpuGateOp::Two {
                matrix,
                q0: targets[0],
                q1: targets[1],
            });
            Ok(())
        }
        Gate::CY => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::Y.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CH => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::H.matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRx(theta) => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::Rx(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRy(theta) => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::Ry(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CRz(theta) => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::Rz(*theta).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CP(lambda) => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::P(*lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU3(theta, phi, lambda) => {
            ops.push(WgpuGateOp::Controlled1q {
                matrix: Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>(),
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<f32>();
            let phase = Complex::new(gamma.cos() as f32, gamma.sin() as f32);
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            ops.push(WgpuGateOp::Controlled1q {
                matrix: m,
                ctrl: targets[0],
                tgt: targets[1],
            });
            Ok(())
        }
        Gate::Toffoli | Gate::Fredkin => Err(GpuError::Unsupported(format!(
            "wgpu statevector: 3-qubit gate {gate:?} 는 v0.5.x patch — \
             qc.transpile() 으로 분해 후 backend='wgpu' 사용 또는 backend='cpu' 사용"
        ))),
    }
}

/// Density backend 의 게이트 dispatch.  [`apply_gate_typed`] 와 평행 구조,
/// 모든 게이트가 density `ρ → U ρ U†` 패턴.  3-큐비트 (Toffoli, Fredkin) 도 native.
fn apply_gate_typed_density<F: Real>(rho: &mut DensityMatrix<F>, gate: &Gate, targets: &[usize]) {
    match gate {
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            let m = gate.matrix_2x2::<F>();
            rho.apply_unitary_1q(&m, targets[0]);
        }
        Gate::CNOT => {
            let x = Gate::X.matrix_2x2::<F>();
            rho.apply_controlled_1q(&x, targets[0], targets[1]);
        }
        Gate::CZ => {
            let cz = Gate::cz_matrix::<F>();
            rho.apply_unitary_2q(&cz, targets[0], targets[1]);
        }
        Gate::SWAP => {
            let sw = Gate::swap_matrix::<F>();
            rho.apply_unitary_2q(&sw, targets[0], targets[1]);
        }
        Gate::ISwap => {
            rho.apply_unitary_2q(&Gate::iswap_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Rxx(t) => {
            rho.apply_unitary_2q(&Gate::rxx_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Ryy(t) => {
            rho.apply_unitary_2q(&Gate::ryy_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Rzz(t) => {
            rho.apply_unitary_2q(&Gate::rzz_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Dcx => {
            rho.apply_unitary_2q(&Gate::dcx_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Ecr => {
            rho.apply_unitary_2q(&Gate::ecr_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Rzx(t) => {
            rho.apply_unitary_2q(&Gate::rzx_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::XxPlusYy(t) => {
            rho.apply_unitary_2q(&Gate::xx_plus_yy_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::XxMinusYy(t) => {
            rho.apply_unitary_2q(&Gate::xx_minus_yy_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::CY => {
            let m = Gate::Y.matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CH => {
            let m = Gate::H.matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CRx(theta) => {
            let m = Gate::Rx(*theta).matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CRy(theta) => {
            let m = Gate::Ry(*theta).matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CRz(theta) => {
            let m = Gate::Rz(*theta).matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CP(lambda) => {
            let m = Gate::P(*lambda).matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CU3(theta, phi, lambda) => {
            let m = Gate::U(*theta, *phi, *lambda).matrix_2x2::<F>();
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<F>();
            let phase = qsim_core::complex::complex::<F>(gamma.cos(), gamma.sin());
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            rho.apply_controlled_1q(&m, targets[0], targets[1]);
        }
        Gate::Toffoli => {
            let x = Gate::X.matrix_2x2::<F>();
            rho.apply_doubly_controlled_1q(&x, targets[0], targets[1], targets[2]);
        }
        Gate::Fredkin => {
            rho.apply_controlled_swap(targets[0], targets[1], targets[2]);
        }
    }
}

/// Density 의 모든 amplitude 에 e^(iλ) 곱.  ρ 에는 `ρ → U ρ U†` 에서 phase 가
/// 상쇄돼 사실상 무영향이지만, statevector 경로와 의미를 통일하기 위해 동일
/// API 호출 — 실제 구현은 no-op (ρ 의 global phase 는 자명).
#[inline]
fn apply_global_phase_density<F: Real>(_rho: &mut DensityMatrix<F>, _lambda: f64) {
    // ρ → e^(iλ) ρ e^(-iλ) = ρ.  no-op.
}

/// Density 에서 measurement sampling — `n_qubits` 폭 LSB-first 비트열.
fn sample_density<F: Real, R: Rng>(
    rho: &DensityMatrix<F>,
    shots: usize,
    n_qubits: usize,
    rng: &mut R,
) -> std::collections::HashMap<String, usize> {
    let probs = rho.diagonal_probabilities();
    let cdf = build_cdf(&probs);
    let mut counts = std::collections::HashMap::new();
    for _ in 0..shots {
        let outcome = sample_from_cdf(&cdf, rng);
        let s = format_bits(outcome, n_qubits);
        *counts.entry(s).or_insert(0) += 1;
    }
    counts
}

/// Density 에서 explicit `Measure { qubit, cbit }` 매핑 sampling.
fn sample_density_with_cbit_map<F: Real, R: Rng>(
    rho: &DensityMatrix<F>,
    shots: usize,
    measures: &[(usize, usize)],
    n_cbits: usize,
    rng: &mut R,
) -> std::collections::HashMap<String, usize> {
    let probs = rho.diagonal_probabilities();
    let cdf = build_cdf(&probs);
    let mut counts = std::collections::HashMap::new();
    for _ in 0..shots {
        let outcome = sample_from_cdf(&cdf, rng);
        let mut cbits: Vec<u8> = vec![0; n_cbits];
        for &(q, c) in measures {
            if c < n_cbits {
                cbits[c] = ((outcome >> q) & 1) as u8;
            }
        }
        let mut s = String::with_capacity(n_cbits);
        for &b in cbits.iter().rev() {
            s.push(if b == 0 { '0' } else { '1' });
        }
        *counts.entry(s).or_insert(0) += 1;
    }
    counts
}

/// 누적 분포 빌드.  마지막 원소를 1.0 으로 강제 (floating drift 방어).
#[inline]
fn build_cdf(probs: &[f64]) -> Vec<f64> {
    let mut cdf = Vec::with_capacity(probs.len());
    let mut acc = 0.0;
    for &p in probs {
        acc += p.max(0.0);
        cdf.push(acc);
    }
    if let Some(last) = cdf.last_mut() {
        *last = 1.0;
    }
    cdf
}

#[inline]
fn sample_from_cdf<R: Rng>(cdf: &[f64], rng: &mut R) -> usize {
    let r: f64 = rng.gen();
    cdf.partition_point(|&c| c <= r).min(cdf.len() - 1)
}

#[inline]
fn format_bits(outcome: usize, n: usize) -> String {
    let mut s = String::with_capacity(n);
    for i in (0..n).rev() {
        s.push(if (outcome >> i) & 1 == 1 { '1' } else { '0' });
    }
    s
}

/// `cbit_indices` 의 cbit 들을 LSB-first packed 정수로 만든다 (v0.4.7).
///
/// `cbit_indices[0]` = LSB, `cbit_indices[k]` = bit k.  cbit register 범위
/// 밖 인덱스는 0 으로 처리 (out-of-bounds 안전).
#[inline]
fn pack_cbits(cbit_indices: &[usize], cbits: &[u8]) -> u64 {
    let mut packed: u64 = 0;
    for (bit_pos, &ci) in cbit_indices.iter().enumerate() {
        if ci < cbits.len() && cbits[ci] != 0 {
            packed |= 1u64 << bit_pos;
        }
    }
    packed
}

fn apply_global_phase<F: Real>(state: &mut StateVector<F>, lambda: f64) {
    if lambda != 0.0 {
        let phase = qsim_core::complex::complex::<F>(lambda.cos(), lambda.sin());
        for amp in state.amplitudes_mut() {
            *amp = *amp * phase;
        }
    }
}

impl Default for ExecutionEngine {
    fn default() -> Self {
        Self::new()
    }
}

/// generic 게이트 적용. f32/f64 양쪽에 monomorphize 된다.
/// v0.6.8: 임의 k-큐비트 유니터리를 statevector 에 적용.  instruction 에
/// 저장된 `f64` 행렬을 정밀도 `F` 로 다운캐스트한 뒤
/// [`apply_multi_qubit_gate`] 에 위임한다.
pub(crate) fn apply_unitary_typed<F: Real>(
    state: &mut StateVector<F>,
    matrix: &[Complex<f64>],
    targets: &[usize],
) {
    let conv: Vec<Complex<F>> = matrix
        .iter()
        .map(|c| {
            Complex::new(
                F::from(c.re).expect("f64→F cast"),
                F::from(c.im).expect("f64→F cast"),
            )
        })
        .collect();
    apply_multi_qubit_gate(state, &conv, targets);
}

pub(crate) fn apply_gate_typed<F: Real>(
    state: &mut StateVector<F>,
    gate: &Gate,
    targets: &[usize],
) {
    match gate {
        // 단일 큐비트 게이트
        Gate::H
        | Gate::X
        | Gate::Y
        | Gate::Z
        | Gate::S
        | Gate::Sdg
        | Gate::T
        | Gate::Tdg
        | Gate::Sx
        | Gate::Sxdg
        | Gate::Rx(_)
        | Gate::Ry(_)
        | Gate::Rz(_)
        | Gate::P(_)
        | Gate::U2(_, _)
        | Gate::U(_, _, _)
        | Gate::Id => {
            let matrix = gate.matrix_2x2::<F>();
            apply_single_qubit_gate(state, &matrix, targets[0]);
        }
        // 2큐비트 게이트 — 기본
        Gate::CNOT => {
            let x = Gate::X.matrix_2x2::<F>();
            apply_controlled_gate(state, &x, targets[0], targets[1]);
        }
        Gate::CZ => {
            let cz = Gate::cz_matrix::<F>();
            apply_two_qubit_gate(state, &cz, targets[0], targets[1]);
        }
        Gate::SWAP => {
            let swap = Gate::swap_matrix::<F>();
            apply_two_qubit_gate(state, &swap, targets[0], targets[1]);
        }
        Gate::ISwap => {
            apply_two_qubit_gate(state, &Gate::iswap_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Rxx(t) => {
            apply_two_qubit_gate(state, &Gate::rxx_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Ryy(t) => {
            apply_two_qubit_gate(state, &Gate::ryy_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Rzz(t) => {
            apply_two_qubit_gate(state, &Gate::rzz_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::Dcx => {
            apply_two_qubit_gate(state, &Gate::dcx_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Ecr => {
            apply_two_qubit_gate(state, &Gate::ecr_matrix::<F>(), targets[0], targets[1]);
        }
        Gate::Rzx(t) => {
            apply_two_qubit_gate(state, &Gate::rzx_matrix::<F>(*t), targets[0], targets[1]);
        }
        Gate::XxPlusYy(t) => {
            apply_two_qubit_gate(
                state,
                &Gate::xx_plus_yy_matrix::<F>(*t),
                targets[0],
                targets[1],
            );
        }
        Gate::XxMinusYy(t) => {
            apply_two_qubit_gate(
                state,
                &Gate::xx_minus_yy_matrix::<F>(*t),
                targets[0],
                targets[1],
            );
        }
        // 2큐비트 controlled-1q 게이트 (v0.4.6) — apply_controlled_gate 패턴 재사용.
        // 1q matrix 를 만들어 control / target 인덱스로 그대로 위임.
        Gate::CY => {
            let m = Gate::Y.matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CH => {
            let m = Gate::H.matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CRx(theta) => {
            let m = Gate::Rx(*theta).matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CRy(theta) => {
            let m = Gate::Ry(*theta).matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CRz(theta) => {
            let m = Gate::Rz(*theta).matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CP(lambda) => {
            let m = Gate::P(*lambda).matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CU3(theta, phi, lambda) => {
            let m = Gate::U(*theta, *phi, *lambda).matrix_2x2::<F>();
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            // Qiskit cu(θ,φ,λ,γ) 의 4×4 matrix 는 controlled-(e^(iγ) · U(θ,φ,λ)).
            // 1q matrix M = e^(iγ) · U(θ,φ,λ) 를 만들어 controlled-gate 로 적용한다.
            let u = Gate::U(*theta, *phi, *lambda).matrix_2x2::<F>();
            let phase = qsim_core::complex::complex::<F>(gamma.cos(), gamma.sin());
            let m = [
                [u[0][0] * phase, u[0][1] * phase],
                [u[1][0] * phase, u[1][1] * phase],
            ];
            apply_controlled_gate(state, &m, targets[0], targets[1]);
        }
        // 3큐비트 게이트
        Gate::Toffoli => {
            let x = Gate::X.matrix_2x2::<F>();
            apply_doubly_controlled_gate(state, &x, targets[0], targets[1], targets[2]);
        }
        Gate::Fredkin => {
            apply_controlled_swap(state, targets[0], targets[1], targets[2]);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use qsim_core::complex::approx_eq;
    use qsim_core::C64;

    #[test]
    fn test_bell_circuit_execution() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 1000);

        let counts = result.counts();
        assert!(counts.contains_key("00"));
        assert!(counts.contains_key("11"));
        assert!(!counts.contains_key("01"));
        assert!(!counts.contains_key("10"));

        let expected = C64::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
        let sv = result.statevector_f64().expect("default precision is f64");
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], expected, 1e-10));
    }

    #[test]
    fn test_bell_circuit_execution_f32() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(42).with_precision(Precision::F32);
        let result = engine.run(&circuit, 1000);

        assert_eq!(result.precision(), Precision::F32);
        let counts = result.counts();
        assert!(counts.contains_key("00"));
        assert!(counts.contains_key("11"));

        let sv = result.statevector_f32().expect("expected f32 statevector");
        let expected = num_complex::Complex::new(std::f32::consts::FRAC_1_SQRT_2, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-6_f32));
        assert!(approx_eq(sv.amplitudes()[3], expected, 1e-6_f32));
    }

    #[test]
    fn test_ghz_circuit_execution() {
        let mut circuit = Circuit::new(3);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.cx(0, 2);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(123);
        let result = engine.run(&circuit, 2000);

        let counts = result.counts();
        assert!(counts.contains_key("000"));
        assert!(counts.contains_key("111"));
        let total: usize = counts.values().sum();
        assert_eq!(total, 2000);
        for key in counts.keys() {
            assert!(key == "000" || key == "111", "unexpected outcome: {key}");
        }
    }

    #[test]
    fn test_toffoli_circuit() {
        let mut circuit = Circuit::new(3);
        circuit.x(0);
        circuit.x(1);
        circuit.ccx(0, 1, 2);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);

        let counts = result.counts();
        assert_eq!(counts.get("111"), Some(&100));
    }

    /// v0.6.8: MPS 백엔드의 3-qubit gate 분해가 statevector 와 일치하는지 검증.
    /// 모든 입력 basis 상태 (3큐비트 = 8개) 에 대해 Toffoli 의 MPS statevector
    /// 가 CpuStatevector 결과와 1e-10 이내로 일치해야 한다.
    #[test]
    fn test_mps_toffoli_matches_statevector() {
        for input in 0u8..8 {
            let build = || {
                let mut c = Circuit::new(3);
                if input & 1 != 0 {
                    c.x(0);
                }
                if input & 2 != 0 {
                    c.x(1);
                }
                if input & 4 != 0 {
                    c.x(2);
                }
                c.ccx(0, 1, 2);
                c
            };
            let sv = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuStatevector)
                .run(&build(), 0);
            let mps = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuMps)
                .with_mps_bond_dim(8)
                .run(&build(), 0);
            let sv_amps = sv.statevector_f64().unwrap().amplitudes().to_vec();
            let mps_amps = mps
                .statevector_f64()
                .expect("N=3 MPS returns dense statevector")
                .amplitudes()
                .to_vec();
            for (a, b) in sv_amps.iter().zip(mps_amps.iter()) {
                assert!(
                    (a - b).norm() < 1e-10,
                    "Toffoli MPS mismatch for input {input}: {a} vs {b}"
                );
            }
        }
    }

    /// v0.6.8: MPS 백엔드의 Fredkin (controlled-SWAP) 분해 검증.
    #[test]
    fn test_mps_fredkin_matches_statevector() {
        for input in 0u8..8 {
            let build = || {
                let mut c = Circuit::new(3);
                if input & 1 != 0 {
                    c.x(0);
                }
                if input & 2 != 0 {
                    c.x(1);
                }
                if input & 4 != 0 {
                    c.x(2);
                }
                // Fredkin(control=0, target1=1, target2=2).
                c.cswap(0, 1, 2);
                c
            };
            let sv = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuStatevector)
                .run(&build(), 0);
            let mps = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuMps)
                .with_mps_bond_dim(8)
                .run(&build(), 0);
            let sv_amps = sv.statevector_f64().unwrap().amplitudes().to_vec();
            let mps_amps = mps
                .statevector_f64()
                .expect("N=3 MPS returns dense statevector")
                .amplitudes()
                .to_vec();
            for (a, b) in sv_amps.iter().zip(mps_amps.iter()) {
                assert!(
                    (a - b).norm() < 1e-10,
                    "Fredkin MPS mismatch for input {input}: {a} vs {b}"
                );
            }
        }
    }

    /// v0.6.8: arbitrary unitary 직접 적용이 동등 native 게이트와 일치.
    /// 2-큐비트 CNOT 행렬을 `circuit.unitary` 로 적용한 결과가 `circuit.cx`
    /// 와 statevector 1e-12 이내로 같아야 한다.
    #[test]
    fn test_apply_unitary_matches_native_cnot() {
        use num_complex::Complex;
        let cnot = Gate::cnot_matrix::<f64>();
        let flat: Vec<Complex<f64>> = cnot.iter().flat_map(|r| r.iter().copied()).collect();

        for &(q0, q1) in &[(0usize, 1usize), (1, 0)] {
            let mut via_gate = Circuit::new(2);
            via_gate.h(0);
            via_gate.h(1);
            via_gate.cx(q0, q1);

            let mut via_unitary = Circuit::new(2);
            via_unitary.h(0);
            via_unitary.h(1);
            via_unitary.unitary(flat.clone(), vec![q0, q1]);

            let a = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuStatevector)
                .run(&via_gate, 0);
            let b = ExecutionEngine::with_seed(1)
                .with_backend(Backend::CpuStatevector)
                .run(&via_unitary, 0);
            let aa = a.statevector_f64().unwrap().amplitudes().to_vec();
            let bb = b.statevector_f64().unwrap().amplitudes().to_vec();
            for (x, y) in aa.iter().zip(bb.iter()) {
                assert!((x - y).norm() < 1e-12, "unitary≠cnot q0={q0} q1={q1}");
            }
        }
    }

    /// v0.6.8: 단일 큐비트 arbitrary unitary 도 동등 native (H) 와 일치.
    #[test]
    fn test_apply_unitary_single_qubit() {
        let h = Gate::H.matrix_2x2::<f64>();
        let flat = vec![h[0][0], h[0][1], h[1][0], h[1][1]];
        let mut via_unitary = Circuit::new(1);
        via_unitary.unitary(flat, vec![0]);
        let mut via_gate = Circuit::new(1);
        via_gate.h(0);
        let a = ExecutionEngine::with_seed(1).run(&via_gate, 0);
        let b = ExecutionEngine::with_seed(1).run(&via_unitary, 0);
        let aa = a.statevector_f64().unwrap().amplitudes().to_vec();
        let bb = b.statevector_f64().unwrap().amplitudes().to_vec();
        for (x, y) in aa.iter().zip(bb.iter()) {
            assert!((x - y).norm() < 1e-12);
        }
    }

    #[test]
    fn test_swap_circuit() {
        let mut circuit = Circuit::new(2);
        circuit.x(0);
        circuit.swap(0, 1);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);

        assert_eq!(result.counts().get("10"), Some(&100));
    }

    #[test]
    fn test_no_measurement_empty_counts() {
        let mut circuit = Circuit::new(1);
        circuit.h(0);

        let engine = ExecutionEngine::new();
        let result = engine.run(&circuit, 100);

        assert!(result.counts().is_empty());
    }

    #[test]
    fn test_statevector_without_measurement() {
        let mut circuit = Circuit::new(1);
        circuit.x(0);

        let engine = ExecutionEngine::new();
        let result = engine.run(&circuit, 0);

        let sv = result.statevector_f64().unwrap();
        assert!(approx_eq(
            sv.amplitudes()[1],
            qsim_core::complex::ONE,
            1e-10
        ));
    }

    #[test]
    fn test_rotation_gate_circuit() {
        use std::f64::consts::PI;

        let mut circuit = Circuit::new(1);
        circuit.rx(PI, 0);

        let engine = ExecutionEngine::new();
        let result = engine.run(&circuit, 0);

        let sv = result.statevector_f64().unwrap();
        assert!((sv.probability(0)).abs() < 1e-10);
        assert!((sv.probability(1) - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_fredkin_circuit() {
        let mut circuit = Circuit::new(3);
        circuit.x(0);
        circuit.x(2);
        circuit.cswap(0, 1, 2);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);

        assert_eq!(result.counts().get("011"), Some(&100));
    }

    #[test]
    fn test_bell_state_statistical_distribution() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();

        let engine = ExecutionEngine::with_seed(999);
        let result = engine.run(&circuit, 10000);

        let counts = result.counts();
        let c00 = *counts.get("00").unwrap_or(&0) as f64;
        let c11 = *counts.get("11").unwrap_or(&0) as f64;
        let ratio = c00 / (c00 + c11);
        assert!(ratio > 0.45 && ratio < 0.55, "ratio was {ratio}");
    }

    #[test]
    fn test_precision_default_is_f64() {
        let engine = ExecutionEngine::new();
        let mut circuit = Circuit::new(1);
        circuit.h(0);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.precision(), Precision::F64);
    }

    // ========================================================================
    // v0.4 noise integration tests
    // ========================================================================

    #[test]
    fn test_noise_p_zero_is_identity() {
        // BitFlip(p=0) 는 항상 identity → Bell 회로 결과 변동 없음.
        let mut clean = Circuit::new(2);
        clean.h(0);
        clean.cx(0, 1);
        clean.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let baseline = engine.run(&clean, 1000);

        let mut noisy = Circuit::new(2);
        noisy.h(0);
        noisy.add_noise(qsim_core::NoiseChannel::BitFlip { p: 0.0 }, 0);
        noisy.cx(0, 1);
        noisy.add_noise(qsim_core::NoiseChannel::BitFlip { p: 0.0 }, 1);
        noisy.measure_all();
        let result = engine.run(&noisy, 1000);

        let counts = result.counts();
        // p=0 이면 baseline 과 동일 분포 (ApplyNoise 가 RNG 를 한 번 더 소비하므로
        // shot RNG sequence 가 달라질 수 있어 정확 동일 비교는 안 됨 — Bell 분포만 검증).
        assert!(counts.contains_key("00") && counts.contains_key("11"));
        assert!(!counts.contains_key("01") && !counts.contains_key("10"));
        let total: usize = counts.values().sum();
        assert_eq!(total, 1000);
        let _ = baseline; // 사용. 비교는 아니지만 회로 빌드 검증.
    }

    #[test]
    fn test_noise_bit_flip_p_one_flips_state() {
        // BitFlip(p=1) on |0⟩: 항상 X 적용 → 측정 시 항상 "1".
        let mut circuit = Circuit::new(1);
        circuit.add_noise(qsim_core::NoiseChannel::BitFlip { p: 1.0 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);
        assert_eq!(result.counts().get("1"), Some(&100));
    }

    #[test]
    fn test_noise_amplitude_damping_gamma_one() {
        // |1⟩ 에 AmplitudeDamping(γ=1) → |0⟩ 강제. 측정 시 항상 "0".
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.add_noise(qsim_core::NoiseChannel::AmplitudeDamping { gamma: 1.0 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);
        assert_eq!(result.counts().get("0"), Some(&100));
    }

    // ========================================================================
    // v0.4.6 신규 게이트 — engine 통합 테스트
    // ========================================================================

    /// Sx 게이트가 Hadamard-like 동작 (X-axis π/2 rotation up to phase).
    /// |0⟩ → (1+i)/2 |0⟩ + (1-i)/2 |1⟩, P(0) = P(1) = 1/2.
    #[test]
    fn test_sx_gate_creates_x_eigen_superposition() {
        let mut c = Circuit::new(1);
        c.sx(0);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 5000);
        let c0 = *result.counts().get("0").unwrap_or(&0) as f64;
        let ratio = c0 / 5000.0;
        assert!((ratio - 0.5).abs() < 0.03, "Sx ratio {ratio}");
    }

    /// Sx · Sx = X: |0⟩ → Sx → · → Sx → |1⟩ (결정론).
    #[test]
    fn test_sx_squared_equals_x() {
        let mut c = Circuit::new(1);
        c.sx(0);
        c.sx(0);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        assert_eq!(result.counts().get("1"), Some(&100));
    }

    /// Sxdg · Sx = I.
    #[test]
    fn test_sxdg_sx_identity() {
        let mut c = Circuit::new(1);
        c.sx(0);
        c.sxdg(0);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        assert_eq!(result.counts().get("0"), Some(&100));
    }

    /// P(π) on |+⟩ = |−⟩ (검출 H 후 X 측정 = "1").
    #[test]
    fn test_p_pi_on_plus_gives_minus() {
        let mut c = Circuit::new(1);
        c.h(0); // |+⟩
        c.p(std::f64::consts::PI, 0); // P(π) = Z, |+⟩ → |−⟩
        c.h(0); // |−⟩ → |1⟩
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        assert_eq!(result.counts().get("1"), Some(&100));
    }

    /// CY: |10⟩ (control=q1=1) → CY → |11⟩ 의 Y 적용 phase = i, 측정 시 q1=1 q0=1 → "11".
    #[test]
    fn test_cy_flips_target_with_phase() {
        let mut c = Circuit::new(2);
        c.x(1); // |10⟩
        c.cy(1, 0); // q1 control, q0 target. Y|0⟩ = i|1⟩.  state → i|11⟩.
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        assert_eq!(result.counts().get("11"), Some(&100));
    }

    /// CH: |10⟩ → CH(1, 0) → (|10⟩+|11⟩)/√2.  Q1=1 결정론, q0 marginal 50:50.
    #[test]
    fn test_ch_creates_superposition_when_control_one() {
        let mut c = Circuit::new(2);
        c.x(1);
        c.ch(1, 0);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(2024);
        let result = engine.run(&c, 5000);
        let counts = result.counts();
        let c10 = *counts.get("10").unwrap_or(&0) as f64;
        let c11 = *counts.get("11").unwrap_or(&0) as f64;
        let other: usize = counts
            .iter()
            .filter(|(k, _)| k.as_str() != "10" && k.as_str() != "11")
            .map(|(_, v)| *v)
            .sum();
        assert_eq!(other, 0);
        assert_eq!((c10 + c11) as usize, 5000);
        assert!(((c10 / 5000.0) - 0.5).abs() < 0.03);
    }

    /// CRz(π) 의 controlled-Z 동치 검증: control=1+target=1 amplitude 에 e^(-iπ/2) 추가.
    /// Bell state (|00⟩+|11⟩)/√2 에 CRz(π) 적용 → (|00⟩+e^(-iπ/2)·... wait 아니 Rz(π) on |1⟩
    /// = e^(iπ/2)|1⟩.  (|00⟩+|11⟩)/√2 의 |11⟩ 만 e^(iπ/2)|11⟩ → norm 보존. 측정 분포는
    /// 영향 없음.  여기선 CRz(0) = I 회귀 검증.
    #[test]
    fn test_crz_zero_is_identity() {
        let mut c = Circuit::new(2);
        c.h(0);
        c.cx(0, 1);
        c.crz(0.0, 0, 1);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 1000);
        let c00 = *result.counts().get("00").unwrap_or(&0);
        let c11 = *result.counts().get("11").unwrap_or(&0);
        let other: usize = result
            .counts()
            .iter()
            .filter(|(k, _)| k.as_str() != "00" && k.as_str() != "11")
            .map(|(_, v)| *v)
            .sum();
        assert_eq!(other, 0);
        assert_eq!(c00 + c11, 1000);
    }

    /// CP(π) 는 CZ 와 등가.  Bell-X = (|00⟩+|10⟩)/√2 → CP(π) → (|00⟩−|10⟩)/√2 (no measure 분포 변화)
    /// 그래도 나중 H 적용으로 detect 가능.  여기선 CP(0)=I 만 회귀.
    #[test]
    fn test_cp_zero_is_identity() {
        let mut c = Circuit::new(2);
        c.h(0);
        c.h(1);
        c.cp(0.0, 0, 1);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 1000);
        let total: usize = result.counts().values().sum();
        assert_eq!(total, 1000);
    }

    /// CU3(π, 0, π) on |10⟩ = controlled-X = CNOT.  |10⟩ → |11⟩.
    #[test]
    fn test_cu3_pi_zero_pi_equals_cnot() {
        let mut c = Circuit::new(2);
        c.x(0);
        c.cu3(std::f64::consts::PI, 0.0, std::f64::consts::PI, 0, 1);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        // q0=1 control, q1 target=X|0⟩=|1⟩.  state |11⟩.
        assert_eq!(result.counts().get("11"), Some(&100));
    }

    /// CU(π, 0, π, 0) = CNOT (γ=0).
    #[test]
    fn test_cu_zero_gamma_equals_cu3() {
        let mut c = Circuit::new(2);
        c.x(0);
        c.cu(std::f64::consts::PI, 0.0, std::f64::consts::PI, 0.0, 0, 1);
        c.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&c, 100);
        assert_eq!(result.counts().get("11"), Some(&100));
    }

    #[test]
    fn test_noise_depolarizing_statistical() {
        // Depolarizing(p=1) on |0⟩: 4 outcome {I, X, Y, Z} 균등.
        // I: |0⟩, X: |1⟩, Y: i|1⟩, Z: |0⟩ (단 |0⟩ 이므로 Z 도 |0⟩).
        // → 측정 시 "0" 50%, "1" 50%.
        let mut circuit = Circuit::new(1);
        circuit.add_noise(qsim_core::NoiseChannel::Depolarizing { p: 1.0 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(2024);
        let result = engine.run(&circuit, 10_000);
        let c0 = *result.counts().get("0").unwrap_or(&0) as f64;
        let c1 = *result.counts().get("1").unwrap_or(&0) as f64;
        let ratio = c0 / (c0 + c1);
        // Each shot rebuilds state from |0⟩ then noise → I/X/Y/Z 각각 25%.
        // I, Z → "0" / X, Y → "1" → 50% 50% 기대. 3σ binomial bound ≈ 0.015.
        assert!(
            (ratio - 0.5).abs() < 0.02,
            "Depolarizing(p=1) ratio {ratio} 가 0.5 와 너무 다름"
        );
    }

    // ====================================================================
    // v0.5.0: Density matrix backend integration tests
    // ====================================================================

    #[test]
    fn density_bell_state() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        let engine = ExecutionEngine::with_seed(42).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.backend(), Backend::CpuDensity);
        let rho = result.density_f64().expect("density f64 result");
        // ρ_Bell: ρ[0][0] = ρ[3][3] = 0.5, ρ[0][3] = ρ[3][0] = 0.5, 나머지 0.
        let half = num_complex::Complex::new(0.5_f64, 0.0);
        let expect_pairs: [(usize, usize); 4] = [(0, 0), (0, 3), (3, 0), (3, 3)];
        for i in 0..4 {
            for j in 0..4 {
                let v = rho.data()[i * 4 + j];
                if expect_pairs.contains(&(i, j)) {
                    assert!(approx_eq(v, half, 1e-12), "Bell density ({i},{j}) = {v:?}");
                } else {
                    assert!(approx_eq(v, qsim_core::complex::zero::<f64>(), 1e-12));
                }
            }
        }
    }

    #[test]
    fn density_measure_all_bell_counts() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(123).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 1000);
        let counts = result.counts();
        // Bell 분포: |00⟩, |11⟩ 각각 ~50%.
        let c00 = *counts.get("00").unwrap_or(&0) as f64;
        let c11 = *counts.get("11").unwrap_or(&0) as f64;
        let total = c00 + c11;
        assert!(total > 950.0, "Bell counts 의 |00⟩/|11⟩ 합 = {total}");
        assert!(
            (c00 / total - 0.5).abs() < 0.06,
            "|00⟩ ratio = {}",
            c00 / total
        );
    }

    #[test]
    fn density_noise_deterministic_vs_trajectory() {
        // BitFlip(p=0.3) on |0⟩: density ρ' = diag(0.7, 0.3) deterministic.
        // statevector trajectory 는 통계적이라 ±2% binomial — 비교 위해 큰 shots.
        let mut circuit = Circuit::new(1);
        circuit.add_noise(qsim_core::NoiseChannel::BitFlip { p: 0.3 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(777).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 0);
        let rho = result.density_f64().expect("density f64");
        // ρ[0][0] = 0.7, ρ[1][1] = 0.3, off-diagonal 0.
        let z = qsim_core::complex::zero::<f64>();
        assert!(approx_eq(
            rho.data()[0],
            num_complex::Complex::new(0.7_f64, 0.0),
            1e-12
        ));
        assert!(approx_eq(rho.data()[1], z, 1e-12));
        assert!(approx_eq(rho.data()[2], z, 1e-12));
        assert!(approx_eq(
            rho.data()[3],
            num_complex::Complex::new(0.3_f64, 0.0),
            1e-12
        ));
    }

    #[test]
    fn density_depolarizing_to_max_mixed() {
        // Depolarizing(p=1) on |0⟩ → ρ = I/2.
        let mut circuit = Circuit::new(1);
        circuit.add_noise(qsim_core::NoiseChannel::Depolarizing { p: 1.0 }, 0);
        let engine = ExecutionEngine::with_seed(1).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 0);
        let rho = result.density_f64().unwrap();
        let half = num_complex::Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(rho.data()[0], half, 1e-12));
        assert!(approx_eq(rho.data()[3], half, 1e-12));
    }

    #[test]
    fn density_toffoli_native() {
        // |011⟩ → Toffoli (c1=q0, c2=q1, tgt=q2) → |111⟩.
        let mut circuit = Circuit::new(3);
        circuit.x(0);
        circuit.x(1);
        circuit.ccx(0, 1, 2);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 100);
        assert_eq!(result.counts().get("111"), Some(&100));
    }

    #[test]
    fn density_fredkin_native() {
        // |101⟩ → Fredkin(ctrl=q2, t1=q0, t2=q1) → |110⟩.
        let mut circuit = Circuit::new(3);
        circuit.x(0);
        circuit.x(2);
        circuit.cswap(2, 0, 1);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 100);
        assert_eq!(result.counts().get("110"), Some(&100));
    }

    #[test]
    fn density_reset_on_entangled() {
        // Bell + reset q=0 → q=1 marginal = I/2.
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.reset(0);
        let engine = ExecutionEngine::with_seed(99).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 0);
        let rho = result.density_f64().unwrap();
        // q=0 의 모든 row/col 이 0 인 부분만 살아남아야.  Tr_q0 (ρ) = I/2.
        let reduced = rho.partial_trace(0);
        let half = num_complex::Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(reduced.data()[0], half, 1e-12));
        assert!(approx_eq(reduced.data()[3], half, 1e-12));
    }

    #[test]
    fn density_classical_control_c_if() {
        // |0⟩ → measure → c_if(c==0) X → 결과 항상 |1⟩.
        let mut circuit = Circuit::new(1);
        circuit.measure(0, 0);
        circuit.x(0);
        circuit.c_if_last(vec![0], 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42).with_backend(Backend::CpuDensity);
        let result = engine.run(&circuit, 100);
        // measure 가 cbit map 으로 바뀌면 0 측정 → c_if fires → X 적용 → measure_all → 1.
        // counts key: 1.
        assert_eq!(result.counts().get("1"), Some(&100));
    }

    #[test]
    fn density_f32_path() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        let engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuDensity)
            .with_precision(Precision::F32);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.precision(), Precision::F32);
        assert_eq!(result.backend(), Backend::CpuDensity);
        let rho = result.density_f32().unwrap();
        let tr = rho.trace();
        assert!((tr.re - 1.0).abs() < 1e-5);
    }

    #[test]
    fn density_matches_statevector_for_pure_circuit() {
        // Noise 없는 회로: density backend 의 ρ = |ψ⟩⟨ψ| (statevector backend 와 동치).
        let mut circuit = Circuit::new(3);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.cx(1, 2);
        circuit.rz(0.7, 0);

        let engine_sv = ExecutionEngine::with_seed(42);
        let res_sv = engine_sv.run(&circuit, 0);
        let sv = res_sv.statevector_f64().unwrap();

        let engine_dm = ExecutionEngine::with_seed(42).with_backend(Backend::CpuDensity);
        let res_dm = engine_dm.run(&circuit, 0);
        let rho = res_dm.density_f64().unwrap();

        // 비교: ρ[i][j] vs sv[i] · conj(sv[j]).
        let dim = sv.dim();
        for i in 0..dim {
            for j in 0..dim {
                let expect = sv.amplitudes()[i] * sv.amplitudes()[j].conj();
                let got = rho.data()[i * dim + j];
                assert!(
                    approx_eq(got, expect, 1e-12),
                    "density vs |ψ⟩⟨ψ| diff at ({i},{j})"
                );
            }
        }
    }

    // =====================================================================
    // v0.5.8: wgpu statevector + noise hybrid trajectory tests.
    // sandbox lavapipe / 사용자 GPU adapter 둘 다 동작해야 함.
    // adapter 없으면 NoAdapter 로 skip.
    // =====================================================================

    fn make_wgpu_engine(seed: u64) -> Option<ExecutionEngine> {
        // wgpu adapter 가용성 확인 — backend init 미리 시도.
        match qsim_gpu::cached_wgpu_statevector_backend() {
            Ok(_) => Some(
                ExecutionEngine::with_seed(seed)
                    .with_backend(crate::engine::Backend::WgpuStatevector),
            ),
            Err(_) => None, // sandbox 에 GPU 없을 때 skip.
        }
    }

    #[test]
    fn wgpu_statevector_bitflip_p1_flips_qubit() {
        // BitFlip(p=1.0) 회로: |0⟩ → |1⟩.  trajectory path 가 noise 처리하는지.
        let Some(engine) = make_wgpu_engine(42) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.add_noise(qsim_core::NoiseChannel::BitFlip { p: 1.0 }, 0);
        circuit.measure_all();
        let result = engine.run(&circuit, 100);
        if let SimulationResult::F32 { counts, .. } = result {
            // BitFlip(p=1) 은 deterministic — 모든 shot 이 "1".
            assert_eq!(counts.get("1").copied().unwrap_or(0), 100);
            assert_eq!(counts.get("0").copied().unwrap_or(0), 0);
        } else {
            panic!("expected F32 statevector result");
        }
    }

    #[test]
    fn wgpu_statevector_noise_with_gates_matches_cpu() {
        // H q0 + CX(0,1) + Depolarizing(1.0) on q0 + Measure.
        // Depolarizing(p=1.0) 은 maximally mixed → 4 outcome 거의 동등.
        // 정확 분포 일치는 trajectory 분산 때문에 어려우니 totals 만 확인.
        let Some(engine) = make_wgpu_engine(123) else {
            return;
        };
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.add_noise(qsim_core::NoiseChannel::Depolarizing { p: 1.0 }, 0);
        circuit.measure_all();
        let result = engine.run(&circuit, 200);
        if let SimulationResult::F32 { counts, .. } = result {
            let total: usize = counts.values().sum();
            assert_eq!(total, 200);
            // 4 outcome 모두 적어도 한 번은 (Depolarizing(1.0) 의 fully mixed).
            assert!(counts.len() >= 2, "expected mixed counts, got {counts:?}");
        } else {
            panic!("expected F32 result");
        }
    }

    #[test]
    fn wgpu_statevector_amplitude_damping_full_decay() {
        // |1⟩ → AmplitudeDamping(γ=1.0) → |0⟩ (T1 fully relaxed).
        let Some(engine) = make_wgpu_engine(7) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.add_noise(qsim_core::NoiseChannel::AmplitudeDamping { gamma: 1.0 }, 0);
        circuit.measure_all();
        let result = engine.run(&circuit, 100);
        if let SimulationResult::F32 { counts, .. } = result {
            assert_eq!(counts.get("0").copied().unwrap_or(0), 100);
        } else {
            panic!("expected F32 result");
        }
    }

    // =====================================================================
    // v0.5.9: wgpu statevector + dynamic (Reset / IfEq / mid-circuit Measure)
    // hybrid trajectory tests.
    // =====================================================================

    #[test]
    fn wgpu_statevector_reset_returns_to_ground() {
        // |1⟩ → Reset q0 → |0⟩.  Reset 가 GPU trajectory path 의 dynamic
        // dispatch_instruction 으로 처리되는지.
        let Some(engine) = make_wgpu_engine(11) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.reset(0);
        circuit.measure_all();
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F32 { counts, .. } = result {
            assert_eq!(counts.get("0").copied().unwrap_or(0), 50);
            assert_eq!(counts.get("1").copied().unwrap_or(0), 0);
        } else {
            panic!("expected F32 result");
        }
    }

    #[test]
    fn wgpu_statevector_mid_circuit_measure_classical_register() {
        // H q0 → measure q0 → c0.  c0 의 분포 확인 (Bernoulli 1/2).
        let Some(engine) = make_wgpu_engine(101) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.h(0);
        circuit.measure(0, 0); // mid-circuit
        let result = engine.run(&circuit, 200);
        if let SimulationResult::F32 { counts, .. } = result {
            let zeros = counts.get("0").copied().unwrap_or(0);
            let ones = counts.get("1").copied().unwrap_or(0);
            assert_eq!(zeros + ones, 200);
            // 50:50 ± reasonable tolerance (분산 보정).
            assert!(zeros > 50 && zeros < 150, "zeros={zeros} ones={ones}");
        } else {
            panic!("expected F32 result");
        }
    }

    // =====================================================================
    // v0.5.19: OOM message 친화 변환 tests.
    // =====================================================================

    #[test]
    fn oom_message_detect_variants() {
        // 다양한 driver 의 OOM 메시지 형식 매칭 검증.
        assert!(super::is_oom_message("wgpu error: Out of Memory"));
        assert!(super::is_oom_message("wgpu error: out of memory"));
        assert!(super::is_oom_message("OutOfMemory"));
        assert!(super::is_oom_message("OOM during buffer allocation"));
        assert!(super::is_oom_message("not enough memory"));
        assert!(super::is_oom_message("Memory allocation failed for buffer"));

        // 비-OOM 메시지는 false.
        assert!(!super::is_oom_message(
            "Buffer binding 0 range exceeds limit"
        ));
        assert!(!super::is_oom_message("dispatch group size too large"));
        assert!(!super::is_oom_message("validation error"));
        assert!(!super::is_oom_message(""));
    }

    #[test]
    fn suppress_panic_guard_thread_local() {
        // v0.5.20: SuppressPanicGuard 가 thread-local flag 정확히 toggle 하는지.
        // 시작 false, guard 안 true, drop 후 false.
        super::SUPPRESS_PANIC_OUTPUT.with(|c| {
            assert!(!c.get(), "초기 false");
        });
        {
            let _g = super::SuppressPanicGuard::new();
            super::SUPPRESS_PANIC_OUTPUT.with(|c| {
                assert!(c.get(), "guard 안 true");
            });
        } // drop
        super::SUPPRESS_PANIC_OUTPUT.with(|c| {
            assert!(!c.get(), "drop 후 false");
        });
    }

    #[test]
    fn suppress_panic_guard_unwind_safe() {
        // panic 으로 unwind 시에도 Drop 호출되어 flag 복귀.
        let _ = std::panic::catch_unwind(|| {
            let _g = super::SuppressPanicGuard::new();
            assert!(super::SUPPRESS_PANIC_OUTPUT.with(|c| c.get()));
            panic!("test panic");
        });
        // unwind 후에도 false.
        super::SUPPRESS_PANIC_OUTPUT.with(|c| {
            assert!(!c.get(), "unwind 후 flag 복귀");
        });
    }

    #[test]
    fn oom_panic_to_friendly_error() {
        // panic_to_gpu_error 가 OOM message 를 친화 hint 로 변환하는지.
        let payload: Box<dyn std::any::Any + Send> =
            Box::new(String::from("wgpu error: Out of Memory"));
        let err = super::panic_to_gpu_error("wgpu statevector", payload);
        let msg = format!("{err}");
        assert!(msg.contains("GPU/unified memory 부족"));
        assert!(msg.contains("backend='cpu'") || msg.contains("statevector"));
        // sv 크기 가이드 (N→GiB 표) 포함.
        assert!(msg.contains("N=29") || msg.contains("N=32"));
    }

    #[test]
    fn wgpu_statevector_multi_reset_x_v0_5_21() {
        // RX 6600 dispatch 의 C-2 회귀 — `X; Reset; X; Reset; X; measure_all`
        // 가 |1⟩ 반환 (이전 v0.5.20 까지 has_dyn=true + measure_all 조합에서
        // cbit register branch 의 default 0 만 반환하던 bug).  v0.5.21 fix.
        let Some(engine) = make_wgpu_engine(42) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.reset(0);
        circuit.x(0);
        circuit.reset(0);
        circuit.x(0);
        circuit.measure_all();
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F32 { counts, .. } = result {
            assert_eq!(counts.get("1").copied().unwrap_or(0), 50, "got {counts:?}");
            assert_eq!(counts.get("0").copied().unwrap_or(0), 0);
        } else {
            panic!("expected F32 result");
        }
    }

    #[test]
    fn wgpu_statevector_reset_x_measure_all_v0_5_21() {
        // 더 단순 케이스 — `Reset; X; measure_all` 도 같은 has_dyn + measure_all
        // bug 영향.  v0.5.21 fix 후 |1⟩ 반환.
        let Some(engine) = make_wgpu_engine(7) else {
            return;
        };
        let mut circuit = Circuit::new(1);
        circuit.reset(0);
        circuit.x(0);
        circuit.measure_all();
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F32 { counts, .. } = result {
            assert_eq!(counts.get("1").copied().unwrap_or(0), 50, "got {counts:?}");
        } else {
            panic!("expected F32 result");
        }
    }

    #[test]
    fn wgpu_statevector_c_if_classical_control() {
        // Bell 측정 후 |00⟩ 또는 |11⟩.
        // c0=0: X 안 적용 → q1 그대로 |0⟩ → c1=0.
        // c0=1: X 적용 → |11⟩ → |10⟩ → c1=0 (q1 = 0 after flip).
        // 결과 c1 항상 0.
        let Some(engine) = make_wgpu_engine(7) else {
            return;
        };
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure(0, 0);
        circuit.x(1);
        circuit.c_if_last(vec![0], 1);
        circuit.measure(1, 1);
        let result = engine.run(&circuit, 100);
        if let SimulationResult::F32 { counts, .. } = result {
            let total: usize = counts.values().sum();
            assert_eq!(total, 100);
            // num_cbits=2.  LSB-first reverse → c1 이 첫 자리, c0 이 둘째.
            // 모든 outcome 의 c1=0.
            for key in counts.keys() {
                assert!(
                    key.starts_with('0'),
                    "expected c1=0 in all outcomes, got {key}"
                );
            }
        } else {
            panic!("expected F32 result");
        }
    }

    // =====================================================================
    // v0.5.22: Edge case 의식적 list (16 항목)
    //
    // RX 6600 dispatch 의 C-2 (multi-reset + measure_all) 같은 latent bug
    // 자동 노출 위해 의식적 edge case 단위 테스트.  CPU vs wgpu 비교가
    // 가장 유효 (가능한 곳).
    // =====================================================================

    /// EC-1: N=1 회로 의 모든 backend 정상 동작.
    #[test]
    fn edge_n1_x_measure() {
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("1").copied().unwrap_or(0), 50);
        } else {
            panic!("expected F64 result");
        }
    }

    /// EC-2: depth 0 회로 (gate 0 + measure_all).  state |0⟩ → 모두 "0".
    #[test]
    fn edge_depth0_measure_all() {
        let mut circuit = Circuit::new(2);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("00").copied().unwrap_or(0), 50);
        } else {
            panic!("expected F64 result");
        }
    }

    /// EC-3: shots=0 (statevector only).  empty counts + state 정확.
    #[test]
    fn edge_shots0_statevector_only() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        // measure_all 없음
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 0);
        if let SimulationResult::F64 {
            counts,
            statevector,
            ..
        } = result
        {
            assert!(counts.is_empty());
            // Bell state amp[0] = amp[3] = 1/√2.
            let inv = 1.0 / 2.0_f64.sqrt();
            assert!((statevector.amplitudes()[0] - C64::new(inv, 0.0)).norm() < 1e-12);
            assert!((statevector.amplitudes()[3] - C64::new(inv, 0.0)).norm() < 1e-12);
        }
    }

    /// EC-4: measure 없는 shots>0.  empty counts (sampling 안 함).
    #[test]
    fn edge_no_measure_shots_positive() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 100);
        if let SimulationResult::F64 { counts, .. } = result {
            assert!(
                counts.is_empty(),
                "no measure → empty counts, got {counts:?}"
            );
        }
    }

    /// EC-5: same qubit 다중 X (X X = I).  state |0⟩ 그대로.
    #[test]
    fn edge_xxx_self_inverse() {
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.x(0);
        circuit.x(0);
        circuit.x(0); // 짝수 → |0⟩
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 30);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("0").copied().unwrap_or(0), 30);
        }
    }

    /// EC-6: empty circuit (gate 0 + measure 0).  shots=0 → state |0⟩.
    #[test]
    fn edge_empty_circuit() {
        let circuit = Circuit::new(2);
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 0);
        if let SimulationResult::F64 {
            counts,
            statevector,
            ..
        } = result
        {
            assert!(counts.is_empty());
            assert_eq!(statevector.amplitudes()[0], C64::new(1.0, 0.0));
            for amp in statevector.amplitudes().iter().skip(1) {
                assert_eq!(*amp, C64::new(0.0, 0.0));
            }
        }
    }

    /// EC-7: global_phase 적용된 회로.  사용자에게 visible 안 하지만 sv 에 영향.
    #[test]
    fn edge_global_phase() {
        let mut circuit = Circuit::new(1);
        circuit.add_global_phase(std::f64::consts::PI / 2.0); // exp(iπ/2) = i
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 0);
        if let SimulationResult::F64 { statevector, .. } = result {
            // |0⟩ × i = (0+1i, 0).
            let amp0 = statevector.amplitudes()[0];
            assert!((amp0.re).abs() < 1e-12, "Re ≈ 0, got {}", amp0.re);
            assert!((amp0.im - 1.0).abs() < 1e-12, "Im ≈ 1, got {}", amp0.im);
        }
    }

    /// EC-8: noise(p=0) — no-op.  X|0⟩ + BitFlip(0) = |1⟩.
    #[test]
    fn edge_noise_p0_noop() {
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.add_noise(qsim_core::NoiseChannel::BitFlip { p: 0.0 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("1").copied().unwrap_or(0), 50);
        }
    }

    /// EC-9: noise(p=1) — deterministic.  X|0⟩ + BitFlip(1) = |0⟩.
    #[test]
    fn edge_noise_p1_deterministic() {
        let mut circuit = Circuit::new(1);
        circuit.x(0);
        circuit.add_noise(qsim_core::NoiseChannel::BitFlip { p: 1.0 }, 0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("0").copied().unwrap_or(0), 50);
        }
    }

    /// EC-10: Toffoli 8 input cases — control 두 비트 따라 정확한 동작.
    #[test]
    fn edge_toffoli_truth_table() {
        // |c0 c1 t⟩ → |c0 c1 (t XOR (c0 AND c1))⟩
        for c0 in 0..2 {
            for c1 in 0..2 {
                for t in 0..2 {
                    let mut circuit = Circuit::new(3);
                    if c0 == 1 {
                        circuit.x(0);
                    }
                    if c1 == 1 {
                        circuit.x(1);
                    }
                    if t == 1 {
                        circuit.x(2);
                    }
                    circuit.ccx(0, 1, 2);
                    circuit.measure_all();
                    let engine = ExecutionEngine::with_seed(42);
                    let result = engine.run(&circuit, 10);
                    let expected_t = t ^ (c0 & c1);
                    let expected_bits = format!("{}{}{}", expected_t, c1, c0); // LSB-first reverse
                    if let SimulationResult::F64 { counts, .. } = result {
                        assert_eq!(
                            counts.get(&expected_bits).copied().unwrap_or(0),
                            10,
                            "Toffoli c0={c0} c1={c1} t={t} → expected {expected_bits} got {counts:?}"
                        );
                    }
                }
            }
        }
    }

    /// EC-11: Fredkin 의 모든 input.  CSWAP(c, t0, t1).
    #[test]
    fn edge_fredkin_truth_table() {
        for c in 0..2 {
            for t0 in 0..2 {
                for t1 in 0..2 {
                    let mut circuit = Circuit::new(3);
                    if c == 1 {
                        circuit.x(0);
                    }
                    if t0 == 1 {
                        circuit.x(1);
                    }
                    if t1 == 1 {
                        circuit.x(2);
                    }
                    circuit.cswap(0, 1, 2);
                    circuit.measure_all();
                    let engine = ExecutionEngine::with_seed(42);
                    let result = engine.run(&circuit, 10);
                    let (expected_t0, expected_t1) = if c == 1 { (t1, t0) } else { (t0, t1) };
                    let expected_bits = format!("{}{}{}", expected_t1, expected_t0, c);
                    if let SimulationResult::F64 { counts, .. } = result {
                        assert_eq!(
                            counts.get(&expected_bits).copied().unwrap_or(0),
                            10,
                            "Fredkin c={c} t0={t0} t1={t1} → expected {expected_bits}"
                        );
                    }
                }
            }
        }
    }

    /// EC-12: reset 후 c_if.  reset 으로 |0⟩ 보장 후 c0=0 → X 적용 안 함.
    #[test]
    fn edge_reset_then_c_if() {
        let mut circuit = Circuit::new(1);
        circuit.x(0); // |1⟩
        circuit.reset(0); // |0⟩
        circuit.measure(0, 0); // c0=0
        circuit.x(0);
        circuit.c_if_last(vec![0], 1); // c0==1 일 때만 fire — 0 이므로 skip
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 30);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(
                counts.get("0").copied().unwrap_or(0),
                30,
                "reset + c_if(c0==1) skip → |0⟩, got {counts:?}"
            );
        }
    }

    /// EC-13: empty cbits register (n_cbits=0) + dynamic 없음 + measure_all.
    /// 명확히 simple 한 회로.
    #[test]
    fn edge_no_cbits_measure_all() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();
        // num_cbits 는 measure_all 에 의해 2 로 set 됨.
        // 기존 path (no dynamic) 가 정상 동작 확인.
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 200);
        if let SimulationResult::F64 { counts, .. } = result {
            let total: usize = counts.values().sum();
            assert_eq!(total, 200);
            let p00 = counts.get("00").copied().unwrap_or(0);
            let p11 = counts.get("11").copied().unwrap_or(0);
            assert!(p00 > 50 && p11 > 50, "Bell distribution, got {counts:?}");
            assert!(counts.get("01").copied().unwrap_or(0) == 0);
            assert!(counts.get("10").copied().unwrap_or(0) == 0);
        }
    }

    /// EC-14: same qubit 의 H H = I.  |0⟩ → |+⟩ → |0⟩.
    #[test]
    fn edge_hh_self_inverse() {
        let mut circuit = Circuit::new(1);
        circuit.h(0);
        circuit.h(0);
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 50);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(counts.get("0").copied().unwrap_or(0), 50);
        }
    }

    /// EC-15: reset 후 measure_all 단독 (RX 6600 C-2 회귀 — v0.5.21 fix 확인).
    #[test]
    fn edge_reset_then_measure_all_v0_5_21_regression() {
        let mut circuit = Circuit::new(1);
        circuit.x(0); // |1⟩
        circuit.reset(0); // |0⟩
        circuit.x(0); // |1⟩
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 30);
        if let SimulationResult::F64 { counts, .. } = result {
            assert_eq!(
                counts.get("1").copied().unwrap_or(0),
                30,
                "v0.5.21 fix 회귀, got {counts:?}"
            );
        }
    }

    /// EC-16: explicit Measure(qubit, cbit) 만 (measure_all 없음).
    /// cbit register 활용 path.
    #[test]
    fn edge_explicit_measure_only() {
        let mut circuit = Circuit::new(2);
        circuit.x(0); // q0=|1⟩
        circuit.measure(0, 0); // c0=1
        circuit.measure(1, 1); // c1=0
        let engine = ExecutionEngine::with_seed(42);
        let result = engine.run(&circuit, 30);
        if let SimulationResult::F64 { counts, .. } = result {
            // LSB-first reverse → "c1 c0" = "01".
            assert_eq!(
                counts.get("01").copied().unwrap_or(0),
                30,
                "explicit measure → cbit register, got {counts:?}"
            );
        }
    }

    // -------- v0.6.0 Stage 2 Cut 7: MPS backend integration --------

    fn run_mps_engine(
        circuit: &Circuit,
        shots: usize,
        max_bond_dim: usize,
        seed: u64,
    ) -> SimulationResult {
        let engine = ExecutionEngine::with_seed(seed)
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(max_bond_dim);
        engine.run(circuit, shots)
    }

    #[test]
    fn mps_bell_matches_statevector() {
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();

        let mps_result = run_mps_engine(&circuit, 1000, 64, 42);
        assert_eq!(mps_result.backend(), Backend::CpuMps);
        assert_eq!(mps_result.precision(), Precision::F64);
        assert_eq!(mps_result.mps_max_bond_dim(), Some(64));
        let final_norm = mps_result.mps_final_norm_sq().expect("MpsF64 variant");
        assert!(
            (final_norm - 1.0).abs() < 1e-12,
            "Bell MPS norm² should be 1.0, got {final_norm}"
        );
        let mps_sv = mps_result
            .statevector_f64()
            .expect("MpsF64 has statevector");
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        let amps = mps_sv.amplitudes();
        assert!(approx_eq(amps[0], C64::new(inv, 0.0), 1e-12));
        assert!(approx_eq(amps[3], C64::new(inv, 0.0), 1e-12));
        assert!(approx_eq(amps[1], C64::new(0.0, 0.0), 1e-12));
        assert!(approx_eq(amps[2], C64::new(0.0, 0.0), 1e-12));

        // Sampling sanity: only |00⟩ and |11⟩ outcomes.
        let counts = mps_result.counts();
        assert!(counts.contains_key("00"));
        assert!(counts.contains_key("11"));
        assert!(!counts.contains_key("01"));
        assert!(!counts.contains_key("10"));
    }

    #[test]
    fn mps_ghz_matches_statevector_n2_to_8() {
        for n in 2..=8 {
            let mut circuit = Circuit::new(n);
            circuit.h(0);
            for i in 0..n - 1 {
                circuit.cx(i, i + 1);
            }
            let mps_result = run_mps_engine(&circuit, 0, 64, 42);
            let mps_sv = mps_result
                .statevector_f64()
                .expect("MPS should hand back f64 statevector");

            let sv_engine = ExecutionEngine::with_seed(42);
            let sv_result = sv_engine.run(&circuit, 0);
            let ref_sv = sv_result
                .statevector_f64()
                .expect("CpuStatevector default is f64");

            for (i, (a, b)) in mps_sv
                .amplitudes()
                .iter()
                .zip(ref_sv.amplitudes().iter())
                .enumerate()
            {
                assert!((*a - *b).norm() < 1e-10, "n={n} idx={i}: MPS {a} vs SV {b}");
            }
        }
    }

    #[test]
    fn mps_truncation_chi_2_ghz_lossless() {
        // GHZ has Schmidt rank 2 → max_bond_dim = 2 must be lossless.
        for n in 2..=6 {
            let mut circuit = Circuit::new(n);
            circuit.h(0);
            for i in 0..n - 1 {
                circuit.cx(i, i + 1);
            }
            let result = run_mps_engine(&circuit, 0, 2, 42);
            let final_norm = result.mps_final_norm_sq().unwrap();
            assert!(
                (final_norm - 1.0).abs() < 1e-12,
                "GHZ-{n} chi=2 norm² = {final_norm}"
            );
        }
    }

    #[test]
    fn mps_truncation_chi_1_bell_lossy() {
        // Bell with chi_max=1 → norm² = 0.5 (one of the two equal singular
        // values is dropped).
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        let result = run_mps_engine(&circuit, 0, 1, 42);
        let final_norm = result.mps_final_norm_sq().unwrap();
        assert!(
            (final_norm - 0.5).abs() < 1e-12,
            "Bell chi=1 norm² should be 0.5, got {final_norm}"
        );
    }

    #[test]
    fn mps_swap_circuit_with_swap_gate() {
        // Symmetric 2q gate (SWAP) — exercises the symmetric branch in
        // apply_two_qubit_to_mps regardless of (q0, q1) order.
        let mut circuit = Circuit::new(2);
        circuit.x(0); // q0 = |1⟩, q1 = |0⟩  →  state |q1 q0⟩ = |01⟩  →  index 1.
        circuit.swap(0, 1);
        circuit.measure_all();
        let result = run_mps_engine(&circuit, 100, 64, 42);
        assert_eq!(result.counts().get("10"), Some(&100));
    }

    #[test]
    fn mps_cz_phases_basis_state() {
        // CZ |11⟩ = -|11⟩.
        let mut circuit = Circuit::new(2);
        circuit.x(0);
        circuit.x(1);
        circuit.cz(0, 1);
        let result = run_mps_engine(&circuit, 0, 64, 42);
        let amps = result.statevector_f64().unwrap().amplitudes();
        assert!(approx_eq(amps[3], C64::new(-1.0, 0.0), 1e-12));
    }

    #[test]
    fn mps_default_max_bond_dim_is_64() {
        let circuit = Circuit::new(2);
        let engine = ExecutionEngine::new().with_backend(Backend::CpuMps);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.mps_max_bond_dim(), Some(DEFAULT_MPS_MAX_BOND_DIM));
    }

    // -------- v0.6.5 Cut 2: trunc_threshold engine plumbing --------

    #[test]
    fn mps_trunc_threshold_default_zero() {
        // Default ExecutionEngine has trunc_threshold = 0.0 — behaviour
        // must be bit-equivalent to v0.6.3.
        let mut circuit = Circuit::new(4);
        circuit.h(0);
        for i in 0..3 {
            circuit.cx(i, i + 1);
        }
        let result = run_mps_engine(&circuit, 0, 64, 42);
        assert_eq!(result.mps_trunc_threshold(), Some(0.0));
        assert_eq!(
            result.mps_observed_max_bond_dim(),
            Some(2),
            "GHZ-4 Schmidt rank is 2"
        );
        let truncation_err = result.mps_truncation_error_sum().unwrap();
        assert!(truncation_err < 1e-14, "lossless: {truncation_err}");
    }

    #[test]
    fn mps_trunc_threshold_ghz_n12_adaptive() {
        // GHZ-12 with χ_max=64 and eps=1e-10 → adaptive bond dim should
        // collapse to the Schmidt rank (2), well below χ_max.
        let n = 12;
        let mut circuit = Circuit::new(n);
        circuit.h(0);
        for i in 0..n - 1 {
            circuit.cx(i, i + 1);
        }
        let engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(64)
            .with_mps_trunc_threshold(1e-10);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.mps_max_bond_dim(), Some(64));
        assert_eq!(result.mps_trunc_threshold(), Some(1e-10));
        assert_eq!(
            result.mps_observed_max_bond_dim(),
            Some(2),
            "eps=1e-10 must drop all but the true Schmidt rank"
        );
        // Truncation error: every dropped sv was < 1e-10 → sum < N · 1e-20.
        let err = result.mps_truncation_error_sum().unwrap();
        assert!(err < 1e-15, "adaptive truncation error tiny: {err}");
    }

    #[test]
    fn mps_trunc_threshold_passthrough_via_builder() {
        // Builder chaining preserves both bond_dim and trunc_threshold.
        let circuit = Circuit::new(2);
        let engine = ExecutionEngine::new()
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(8)
            .with_mps_trunc_threshold(1e-6);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.mps_max_bond_dim(), Some(8));
        assert_eq!(result.mps_trunc_threshold(), Some(1e-6));
    }

    #[test]
    #[should_panic(expected = "mps_trunc_threshold must be finite")]
    fn mps_trunc_threshold_rejects_negative() {
        let _ = ExecutionEngine::new()
            .with_backend(Backend::CpuMps)
            .with_mps_trunc_threshold(-1.0);
    }

    #[test]
    fn mps_shots_zero_above_20_qubits_retains_mps_for_expectation() {
        // v0.7: N>20 + shots=0 no longer panics — no dense statevector is
        // built, but the MPS is retained so observable expectation
        // (expectation_pauli) works for large-N VQE.
        let circuit = Circuit::new(21);
        let engine = ExecutionEngine::new().with_backend(Backend::CpuMps);
        let result = engine.run(&circuit, 0);
        match result {
            SimulationResult::MpsF64 {
                statevector, mps, ..
            } => {
                assert!(statevector.is_none(), "N>20 should not build dense SV");
                let mps = mps.expect("N>20 shots=0 must retain MPS");
                // |0...0>: <Z_0> = +1.
                let mut paulis = vec![0u8; 21];
                paulis[0] = 3;
                let z0 = mps.expectation_pauli(&paulis);
                assert!((z0.re - 1.0).abs() < 1e-9 && z0.im.abs() < 1e-9);
            }
            _ => panic!("expected MpsF64"),
        }
    }

    #[test]
    fn mps_n_30_ghz_runs_with_sampling() {
        // v0.6.1: N=30 GHZ via direct MPS sampling — counts only, no
        // dense SV.  Schmidt rank 2 → χ=4 lossless.
        let n = 30;
        let mut circuit = Circuit::new(n);
        circuit.h(0);
        for i in 0..n - 1 {
            circuit.cx(i, i + 1);
        }
        circuit.measure_all();
        let result = run_mps_engine(&circuit, 500, 4, 42);
        assert_eq!(result.backend(), Backend::CpuMps);
        // statevector must be None for N>20.
        assert!(result.statevector_f64().is_none());
        let counts = result.counts();
        // GHZ-30 → only "0"*30 and "1"*30 outcomes.
        let s0 = "0".repeat(30);
        let s1 = "1".repeat(30);
        for k in counts.keys() {
            assert!(*k == s0 || *k == s1, "unexpected outcome {k}");
        }
        let n0 = counts.get(&s0).copied().unwrap_or(0);
        let n1 = counts.get(&s1).copied().unwrap_or(0);
        assert_eq!(n0 + n1, 500);
        // Loose 50:50 sanity.
        assert!((n0 as f64 / 500.0 - 0.5).abs() < 0.10);
        // norm² should be ≈ 1.0 (chi=4 sufficient for GHZ).
        let norm = result.mps_final_norm_sq().unwrap();
        assert!((norm - 1.0).abs() < 1e-10, "GHZ-30 chi=4 norm² = {norm}");
    }

    #[test]
    fn mps_n_50_ghz_runs() {
        // Stretch case — N=50 (Qiskit Aer / wgpu / cuStateVec all OOM).
        let n = 50;
        let mut circuit = Circuit::new(n);
        circuit.h(0);
        for i in 0..n - 1 {
            circuit.cx(i, i + 1);
        }
        circuit.measure_all();
        let result = run_mps_engine(&circuit, 100, 4, 7);
        assert!(result.statevector_f64().is_none());
        let counts = result.counts();
        let s0 = "0".repeat(n);
        let s1 = "1".repeat(n);
        for k in counts.keys() {
            assert!(*k == s0 || *k == s1, "GHZ-{n} unexpected outcome {k}");
        }
        assert_eq!(counts.values().sum::<usize>(), 100);
    }

    #[test]
    fn mps_n_below_20_dense_sv_path_unchanged() {
        // v0.6.0 backward compat: N=8 GHZ + shots=0 → statevector_f64 Some,
        // exact amplitudes (no v0.6.1 regression on the dense-SV fast path).
        let mut circuit = Circuit::new(8);
        circuit.h(0);
        for i in 0..7 {
            circuit.cx(i, i + 1);
        }
        let result = run_mps_engine(&circuit, 0, 64, 42);
        let sv = result
            .statevector_f64()
            .expect("N=8 + shots=0 must keep dense SV");
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        let amps = sv.amplitudes();
        assert!(approx_eq(amps[0], C64::new(inv, 0.0), 1e-12));
        assert!(approx_eq(amps[(1 << 8) - 1], C64::new(inv, 0.0), 1e-12));
    }

    #[test]
    fn mps_long_range_cnot_matches_statevector() {
        // v0.6.3 (was v0.6.4 deferred): non-adjacent 2q gate is
        // automatically decomposed into a SWAP chain inside the engine.
        // The MPS result must agree with the dense statevector path.
        let mut circuit = Circuit::new(4);
        circuit.h(0);
        circuit.cx(0, 3); // long-range, two intermediate sites.
        let engine_mps = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(64);
        let res_mps = engine_mps.run(&circuit, 0);
        let sv_mps = res_mps.statevector_f64().expect("MPS shots=0 has SV");

        let engine_sv = ExecutionEngine::with_seed(42);
        let res_sv = engine_sv.run(&circuit, 0);
        let sv_ref = res_sv.statevector_f64().unwrap();

        for (a, b) in sv_mps.amplitudes().iter().zip(sv_ref.amplitudes().iter()) {
            assert!(
                (a - b).norm() < 1e-10,
                "MPS long-range CNOT amplitude diverges: {a:?} vs {b:?}"
            );
        }
    }

    #[test]
    fn mps_toffoli_now_supported_via_decomposition() {
        // v0.6.8: Toffoli (and Fredkin) are now supported on the MPS
        // backend via 1q + CNOT decomposition.  Was a hard panic in
        // v0.6.7.  Correctness vs statevector is covered by
        // test_mps_toffoli_matches_statevector.
        let mut circuit = Circuit::new(3);
        circuit.ccx(0, 1, 2);
        let engine = ExecutionEngine::new()
            .with_backend(Backend::CpuMps)
            .with_mps_bond_dim(8);
        let _ = engine.run(&circuit, 0); // must not panic.
    }

    #[test]
    fn mps_reset_now_supported_via_trajectory() {
        // v0.6.5: Reset (and other dynamic ops) are now supported via
        // the MPS trajectory engine.  This test exercises the path —
        // statistical correctness is covered in test_mps.py.
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.reset(0); // Was a hard panic in v0.6.3.
        circuit.measure_all();
        let engine = ExecutionEngine::with_seed(42).with_backend(Backend::CpuMps);
        let result = engine.run(&circuit, 100);
        assert_eq!(result.backend(), Backend::CpuMps);
        // After Reset(0): q0 deterministically |0⟩; q1 inherits the
        // post-collapse value.  Counts will be a mix of "00" and "10".
        let counts = result.counts();
        let total: usize = counts.values().sum();
        assert_eq!(total, 100);
    }

    // -------- v0.6.5 Cut 5: MPS f32 backend --------

    #[test]
    fn mps_f32_runs_and_metadata_correct() {
        // v0.6.5: precision='f32' is supported (was a panic in v0.6.3).
        use qsim_core::C32;
        let mut circuit = Circuit::new(4);
        circuit.h(0);
        for i in 0..3 {
            circuit.cx(i, i + 1);
        }
        let engine = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F32);
        let result = engine.run(&circuit, 0);
        assert_eq!(result.backend(), Backend::CpuMps);
        assert_eq!(result.precision(), Precision::F32);
        assert_eq!(result.mps_observed_max_bond_dim(), Some(2));
        let norm = result.mps_final_norm_sq().unwrap();
        assert!((norm - 1.0).abs() < 1e-5, "f32 GHZ-4 norm² = {norm}");
        // statevector_f32 returns the dense state; statevector_f64 is None.
        let sv32 = result.statevector_f32().expect("MpsF32 has SV at N≤20");
        let inv = std::f32::consts::FRAC_1_SQRT_2;
        let amps = sv32.amplitudes();
        assert!((amps[0] - C32::new(inv, 0.0)).norm() < 1e-5);
        assert!((amps[15] - C32::new(inv, 0.0)).norm() < 1e-5);
        assert!(result.statevector_f64().is_none());
    }

    #[test]
    fn mps_f32_vs_f64_fidelity_ghz_8() {
        // f32 and f64 backends on the same circuit must give fidelity
        // > 1 - 1e-4 (Schollwöck §4.5.3 ε_f32 accumulation).
        use qsim_core::C64;
        let n = 8;
        let mut circuit = Circuit::new(n);
        circuit.h(0);
        for i in 0..n - 1 {
            circuit.cx(i, i + 1);
        }
        let engine64 = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F64);
        let engine32 = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F32);
        let r64 = engine64.run(&circuit, 0);
        let r32 = engine32.run(&circuit, 0);
        let sv64 = r64.statevector_f64().unwrap().amplitudes();
        let sv32 = r32.statevector_f32().unwrap().amplitudes();
        let mut inner = C64::new(0.0, 0.0);
        for (a64, a32) in sv64.iter().zip(sv32.iter()) {
            let a32_64 = C64::new(a32.re as f64, a32.im as f64);
            inner += a64.conj() * a32_64;
        }
        let fidelity = inner.norm_sqr();
        assert!(fidelity > 1.0 - 1e-4, "fidelity = {fidelity}");
    }

    // -------- v0.6.6 Cut 1: wgpu MPS scaffolding tests --------
    //
    // Cut 1 시점에서는 `Backend::WgpuMps` arm 이 CPU MPS f32 path 로
    // 위임된다.  여기서 검증할 것은:
    //   1. method_str / backend_str 분류가 맞는지.
    //   2. 결과가 `Backend::CpuMps` + Precision::F32 와 동일 (CPU fallback).
    //   3. seed 동일 시 sample distribution 정확히 일치.
    // Cut 6 이후 실제 GPU 경로 진입 시 (2), (3) 은 ±1e-5 tolerance 로 완화 예정.

    #[test]
    fn wgpu_mps_backend_str_classification() {
        assert_eq!(Backend::WgpuMps.method_str(), "mps");
        assert_eq!(Backend::WgpuMps.backend_str(), "wgpu");
        // sanity: not equal to CpuMps despite shared method_str.
        assert_ne!(Backend::WgpuMps, Backend::CpuMps);
    }

    #[test]
    fn wgpu_mps_bell_matches_cpu_mps_cut1_fallback() {
        // Cut 1 wiring smoke test — Backend::WgpuMps 가 panic 없이 동작
        // 하고 결과가 CPU MPS f32 와 byte-identical 인지.
        let mut circuit = Circuit::new(2);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.measure_all();

        let cpu = ExecutionEngine::with_seed(42)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F32)
            .with_mps_bond_dim(64)
            .run(&circuit, 1000);
        let wgpu = ExecutionEngine::with_seed(42)
            .with_backend(Backend::WgpuMps)
            .with_mps_bond_dim(64)
            .run(&circuit, 1000);

        assert_eq!(wgpu.precision(), Precision::F32);
        // result.backend() 는 v0.5 부터 정책상 cpu 변종 반환 — WgpuMps 도 동일.
        assert_eq!(wgpu.backend(), Backend::CpuMps);
        assert_eq!(cpu.counts(), wgpu.counts());
        let cpu_sv = cpu.statevector_f32().expect("MpsF32 has SV at N=2");
        let wgpu_sv = wgpu.statevector_f32().expect("MpsF32 has SV at N=2");
        for (a, b) in cpu_sv.amplitudes().iter().zip(wgpu_sv.amplitudes().iter()) {
            assert_eq!(a, b, "Cut 1 must be byte-identical CPU fallback");
        }
    }

    #[test]
    fn wgpu_mps_ghz_n8_matches_cpu_mps_cut1_fallback() {
        let n = 8;
        let mut circuit = Circuit::new(n);
        circuit.h(0);
        for i in 0..n - 1 {
            circuit.cx(i, i + 1);
        }
        let cpu = ExecutionEngine::with_seed(123)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F32)
            .with_mps_bond_dim(32)
            .run(&circuit, 0);
        let wgpu = ExecutionEngine::with_seed(123)
            .with_backend(Backend::WgpuMps)
            .with_mps_bond_dim(32)
            .run(&circuit, 0);
        let cpu_sv = cpu.statevector_f32().unwrap().amplitudes();
        let wgpu_sv = wgpu.statevector_f32().unwrap().amplitudes();
        assert_eq!(
            cpu_sv, wgpu_sv,
            "Cut 1 fallback must match CPU MPS f32 byte-for-byte"
        );
        // trunc_threshold / observed_max_bond_dim 메타도 동일해야 함.
        assert_eq!(
            cpu.mps_trunc_threshold(),
            wgpu.mps_trunc_threshold(),
            "trunc_threshold passthrough must match"
        );
        assert_eq!(
            cpu.mps_observed_max_bond_dim(),
            wgpu.mps_observed_max_bond_dim(),
        );
    }

    // v0.6.7: CpuSvdAdapter (GpuSvdProvider impl) matches CpuSvdProvider.
    // CpuSvdAdapter wraps CpuSvdProvider, so results must be identical.
    #[test]
    fn cpu_svd_adapter_matches_cpu_svd_provider_large() {
        use qsim_gpu::GpuSvdProvider as _;
        use qsim_mps::MpsSvdProvider as _;
        let rows = 64;
        let cols = 32;
        let mut state: u64 = 0xCAFEBABE;
        let mut next_f = || -> f32 {
            state = state
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            ((state >> 32) as u32 as f32) / (u32::MAX as f32) * 2.0 - 1.0
        };
        let m: Vec<num_complex::Complex<f32>> = (0..rows * cols)
            .map(|_| num_complex::Complex::new(next_f(), next_f()))
            .collect();

        let cpu_out = qsim_mps::CpuSvdProvider.thin_svd(&m, rows, cols, 1024, 0.0);
        let adapter = super::CpuSvdAdapter;
        let gpu_out = adapter.thin_svd(&m, rows, cols, 1024, 0.0);

        assert_eq!(cpu_out.keep, gpu_out.keep);
        for i in 0..cpu_out.keep {
            assert!(
                (cpu_out.s[i] - gpu_out.s[i]).abs() < 1e-10,
                "SV[{i}] differ: cpu={} adapter={}",
                cpu_out.s[i],
                gpu_out.s[i]
            );
        }
        assert!(cpu_out.trunc_error_sq < 1e-8);
        assert!(gpu_out.trunc_error_sq < 1e-8);
    }

    #[test]
    fn cpu_svd_adapter_matches_cpu_svd_provider_small() {
        use qsim_gpu::GpuSvdProvider as _;
        use qsim_mps::MpsSvdProvider as _;
        let m: Vec<num_complex::Complex<f32>> = (0..16)
            .map(|i| num_complex::Complex::new(i as f32 * 0.1, (i as f32) * -0.05))
            .collect();
        let cpu = qsim_mps::CpuSvdProvider.thin_svd(&m, 4, 4, 16, 0.0);
        let adapter = super::CpuSvdAdapter;
        let gpu = adapter.thin_svd(&m, 4, 4, 16, 0.0);
        assert_eq!(cpu.s, gpu.s, "small matrix must match");
        assert_eq!(cpu.u_row_major, gpu.u_row_major);
        assert_eq!(cpu.vt_row_major, gpu.vt_row_major);
    }

    #[test]
    fn wgpu_mps_random_circuit_matches_cpu_within_f32_tol() {
        // 10-qubit random brickwork — chi grows beyond 32, GPU SVD path
        // active.  CPU and GPU MPS results should match within f32 SVD
        // tolerance (relative amplitude ε ~1e-4).
        let n = 10;
        let mut circuit = Circuit::new(n);
        // 3 layers of (H on all even, then CNOT adjacent).
        for _layer in 0..3 {
            for q in (0..n).step_by(2) {
                circuit.h(q);
            }
            for q in 0..n - 1 {
                circuit.cx(q, q + 1);
            }
        }
        let cpu = ExecutionEngine::with_seed(7)
            .with_backend(Backend::CpuMps)
            .with_precision(Precision::F32)
            .with_mps_bond_dim(64)
            .run(&circuit, 0);
        let gpu = ExecutionEngine::with_seed(7)
            .with_backend(Backend::WgpuMps)
            .with_mps_bond_dim(64)
            .run(&circuit, 0);
        let cpu_sv = cpu.statevector_f32().unwrap().amplitudes();
        let gpu_sv = gpu.statevector_f32().unwrap().amplitudes();
        // Fidelity > 1 - 1e-3 (f32 SVD precision + truncation differences).
        let mut inner = num_complex::Complex::<f32>::new(0.0, 0.0);
        for (a, b) in cpu_sv.iter().zip(gpu_sv.iter()) {
            inner += a.conj() * *b;
        }
        let fidelity = inner.norm_sqr();
        assert!(
            fidelity > 1.0 - 1e-3,
            "wgpu_mps fidelity vs cpu_mps: {fidelity}"
        );
    }

    #[test]
    fn wgpu_mps_precision_f64_silently_uses_f32_path() {
        // wgpu 는 storage f64 미지원 — Precision::F64 와 함께 호출돼도
        // f32 path 로 진입하고 MpsF32 결과 반환 (다른 wgpu backend 와 동일 정책).
        let mut circuit = Circuit::new(3);
        circuit.h(0);
        circuit.cx(0, 1);
        circuit.cx(1, 2);
        let result = ExecutionEngine::with_seed(7)
            .with_backend(Backend::WgpuMps)
            .with_precision(Precision::F64)
            .with_mps_bond_dim(16)
            .run(&circuit, 0);
        assert_eq!(
            result.precision(),
            Precision::F32,
            "WgpuMps must coerce to f32 regardless of precision arg"
        );
        assert!(result.statevector_f32().is_some());
    }
}
