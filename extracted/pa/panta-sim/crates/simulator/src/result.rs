use qsim_core::{DensityMatrix, StateVector};
use std::collections::HashMap;

// Re-export so user crates can write `qsim_simulator::Backend::WgpuDensity`.

/// 시뮬레이션 정밀도 선택. 기본값은 `F64` (v0.2.0 호환).
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum Precision {
    /// 32비트 단일 정밀도 — amplitude 8 bytes, ~50% 메모리 절감, ~1e-6 정확도.
    F32,
    /// 64비트 배 정밀도 — amplitude 16 bytes, ~1e-15 정확도 (default).
    #[default]
    F64,
}

impl Precision {
    /// 사용자 친화 문자열 표현.
    pub fn as_str(&self) -> &'static str {
        match self {
            Precision::F32 => "f32",
            Precision::F64 => "f64",
        }
    }
}

/// 시뮬레이션 백엔드 선택 (v0.5.0).
///
/// `(method, backend)` 의 cross product:
/// - method ∈ {statevector, density_matrix}
/// - backend ∈ {cpu, wgpu, cuda} (v0.5.0 cuda 는 후속 cut)
///
/// 백엔드별 의미:
/// - `CpuStatevector` (default): 기존 statevector 경로.  noise 가 있으면 자동
///   trajectory 모드.  f32 / f64.
/// - `CpuDensity`: density matrix ρ 직접 진화.  noise deterministic Kraus —
///   Aer `method="density_matrix"` 와 동일 의미.  메모리 4ⁿ → N≤14.  f32 / f64.
/// - `WgpuStatevector`: wgpu Tier-1 GPU statevector.  WGSL compute shader.
///   현재 f32 만 (wgpu 29.x 의 storage f64 제약).  noise 미지원 (statevector
///   trajectory 모드는 GPU 에서 batching 어려워 v0.5.x patch 로 deferred).
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum Backend {
    /// State vector 백엔드 — CPU rayon (default).
    #[default]
    CpuStatevector,
    /// Density matrix 백엔드 — CPU.
    CpuDensity,
    /// State vector 백엔드 — wgpu GPU (Tier-1, v0.5.0).
    WgpuStatevector,
    /// Density matrix 백엔드 — wgpu GPU (Tier-1, v0.5.0 Cut E).
    WgpuDensity,
    /// State vector 백엔드 — NVIDIA cuStateVec (Tier-2, v0.5.0 Cut G).
    /// Cargo feature `gpu-cuda` 가 켜져야 동작 — NVIDIA driver + cuQuantum SDK 필요.
    /// feature off 환경에선 panic / NotImplementedError.
    CudaStatevector,
    /// Matrix Product State (MPS) 백엔드 — CPU (v0.6.0).
    ///
    /// 1D tensor network 시뮬레이션.  내부적으로 회로 끝에서 dense
    /// statevector 로 contract 하므로 v0.6.0 시점에선 N ≤ 20 만 의미 있음
    /// (sampling-via-MPS 는 v0.6.1).  noise / dynamic / non-adjacent 2q /
    /// 3q gate 는 v0.6.0 미지원 — 사전 검증으로 명시적 ValueError.
    /// f64 only — f32 generic 리팩터는 v0.6.x patch 에서 단위 테스트 회귀
    /// 가드와 함께 도입.
    CpuMps,
    /// Matrix Product State (MPS) 백엔드 — wgpu GPU (Tier-1, v0.6.6).
    ///
    /// CPU MPS 와 동일 의미이되 SVD 호출 두 곳 (apply_two_qubit_adjacent
    /// 와 right_canonicalize) 을 WGSL one-sided Jacobi compute shader 로
    /// offload.  cross-platform (NVIDIA / AMD / Apple Metal / Intel /
    /// lavapipe).  wgpu storage f64 미지원으로 **f32 only** — precision
    /// 인자는 무시되고 항상 f32 path.
    ///
    /// v0.6.6 Cut 1 시점에서는 wiring 만 완료, 실제 SVD 는 아직 CPU
    /// fallback (qsim_mps).  Cut 6 부터 GPU 경로 실제 통합.
    WgpuMps,
}

impl Backend {
    /// 사용자 친화 (method, backend) tuple 표현.
    pub fn method_str(&self) -> &'static str {
        match self {
            Backend::CpuStatevector | Backend::WgpuStatevector | Backend::CudaStatevector => {
                "statevector"
            }
            Backend::CpuDensity | Backend::WgpuDensity => "density_matrix",
            Backend::CpuMps | Backend::WgpuMps => "mps",
        }
    }

    /// 사용자 친화 backend 문자열 ("cpu" / "wgpu" / "cuda").
    pub fn backend_str(&self) -> &'static str {
        match self {
            Backend::CpuStatevector | Backend::CpuDensity | Backend::CpuMps => "cpu",
            Backend::WgpuStatevector | Backend::WgpuDensity | Backend::WgpuMps => "wgpu",
            Backend::CudaStatevector => "cuda",
        }
    }

    /// 호환성 alias — Python 의 `result.backend` 가 method_str 을 반환 (Cut C 호환).
    pub fn as_str(&self) -> &'static str {
        self.method_str()
    }
}

/// 시뮬레이션 실행 결과. 정밀도별로 내부 state vector 의 타입이 다르므로 enum 으로 분기한다.
#[derive(Debug, Clone)]
pub enum SimulationResult {
    /// 32비트 정밀도 statevector 결과.
    F32 {
        counts: HashMap<String, usize>,
        statevector: StateVector<f32>,
    },
    /// 64비트 정밀도 statevector 결과 (default).
    F64 {
        counts: HashMap<String, usize>,
        statevector: StateVector<f64>,
    },
    /// 32비트 정밀도 density matrix 결과 (v0.5.0).
    DensityF32 {
        counts: HashMap<String, usize>,
        density: DensityMatrix<f32>,
    },
    /// 64비트 정밀도 density matrix 결과 (v0.5.0).
    DensityF64 {
        counts: HashMap<String, usize>,
        density: DensityMatrix<f64>,
    },
    /// MPS 백엔드 결과 (v0.6.0 / v0.6.1).
    ///
    /// `statevector: Option<StateVector<f64>>`:
    /// - `Some(_)` — N ≤ 20 의 경우 회로 끝에서 dense SV 로 contract 한 결과.
    /// - `None` — N > 20 의 경우 dense SV 가 메모리상 불가능 → counts 만
    ///   생성됨 (v0.6.1 sampling-via-MPS).
    ///
    /// `max_bond_dim` 은 사용자가 지정한 χ_max, `final_norm_sq` 는 SVD
    /// truncation 후 남은 squared norm — 1.0 보다 작으면 truncation 에 의한
    /// 정보 손실을 의미한다 (자동 재정규화 안 함).
    ///
    /// `truncation_error_sum` (v0.6.3) 은 회로 실행 중 누적된 SVD discarded
    /// weight `Σ_{SVDs} Σ_{j>=keep} sv_j²` — Schollwöck 2011 §4.5.3 표준
    /// 절대 metric.  `final_norm_sq` 가 잘려나간 *최종 norm* 만 보고하는
    /// 반면, 이 값은 모든 truncating SVD 의 손실을 합산해 회로 전체의
    /// 누적 정확도를 정량화.  `1.0 - final_norm_sq` 와 일반적으로 일치하지
    /// 않을 수 있다 (truncation 후 후속 게이트가 norm 을 다시 흩뜨릴 수
    /// 있음).
    ///
    /// `trunc_threshold` (v0.6.5) 는 사용자가 지정한 singular-value cutoff
    /// (`0.0` = disabled).  `observed_max_bond_dim` 은 회로 종료 시점에 실제
    /// 로 발생한 최대 internal bond dimension — adaptive truncation 활성
    /// 시 `max_bond_dim` 보다 보통 작다 (Schollwöck §4.5.3 ε-rank cutoff).
    MpsF64 {
        counts: HashMap<String, usize>,
        statevector: Option<StateVector<f64>>,
        max_bond_dim: usize,
        trunc_threshold: f64,
        final_norm_sq: f64,
        truncation_error_sum: f64,
        observed_max_bond_dim: usize,
    },
    /// 32-bit precision MPS 결과 (v0.6.5).  메타데이터 의미는 [`MpsF64`]
    /// 와 동일 — 차이는 statevector 의 element type 뿐.  ``f32`` SVD 의
    /// 정밀도가 ~1e-7 이므로 ``trunc_threshold`` 권장값이 ``1e-4`` 로
    /// 더 큰 점에 유의.
    MpsF32 {
        counts: HashMap<String, usize>,
        statevector: Option<StateVector<f32>>,
        max_bond_dim: usize,
        trunc_threshold: f64,
        final_norm_sq: f64,
        truncation_error_sum: f64,
        observed_max_bond_dim: usize,
    },
}

impl SimulationResult {
    /// f64 정밀도 결과 생성자. 기존 v0.2.0 API 호환.
    pub fn new(counts: HashMap<String, usize>, statevector: StateVector<f64>) -> Self {
        SimulationResult::F64 {
            counts,
            statevector,
        }
    }

    /// f32 정밀도 결과 생성자.
    pub fn new_f32(counts: HashMap<String, usize>, statevector: StateVector<f32>) -> Self {
        SimulationResult::F32 {
            counts,
            statevector,
        }
    }

    /// f64 정밀도 density matrix 결과 생성자 (v0.5.0).
    pub fn new_density_f64(counts: HashMap<String, usize>, density: DensityMatrix<f64>) -> Self {
        SimulationResult::DensityF64 { counts, density }
    }

    /// f32 정밀도 density matrix 결과 생성자 (v0.5.0).
    pub fn new_density_f32(counts: HashMap<String, usize>, density: DensityMatrix<f32>) -> Self {
        SimulationResult::DensityF32 { counts, density }
    }

    /// 정밀도 enum 반환.
    pub fn precision(&self) -> Precision {
        match self {
            SimulationResult::F32 { .. }
            | SimulationResult::DensityF32 { .. }
            | SimulationResult::MpsF32 { .. } => Precision::F32,
            SimulationResult::F64 { .. }
            | SimulationResult::DensityF64 { .. }
            | SimulationResult::MpsF64 { .. } => Precision::F64,
        }
    }

    /// 백엔드 enum 반환 (v0.5.0).
    ///
    /// statevector / MPS 결과는 cpu 변종 (`CpuStatevector` / `CpuMps`) 로
    /// 보고됨 — wgpu 결과도 CPU 로 다운로드된 statevector 라 사용자 시각에서
    /// 동일.  실제 사용된 GPU 백엔드는 호출자가 알 수 있음 (run 시 backend
    /// 인자).  엄격한 구분이 필요하면 별도 metadata 추가 (v0.5.x).  v0.6.6
    /// `WgpuMps` 도 동일 정책 — `MpsF32` 결과만 보면 CPU/GPU 구분 불가.
    ///
    /// `MpsF64` 는 method 가 보존된 유일한 statevector 변종 — Python 사용자가
    /// `result.backend == 'mps'` 로 어떤 method 를 썼는지 식별 가능.
    pub fn backend(&self) -> Backend {
        match self {
            SimulationResult::F32 { .. } | SimulationResult::F64 { .. } => Backend::CpuStatevector,
            SimulationResult::DensityF32 { .. } | SimulationResult::DensityF64 { .. } => {
                Backend::CpuDensity
            }
            SimulationResult::MpsF64 { .. } | SimulationResult::MpsF32 { .. } => Backend::CpuMps,
        }
    }

    /// 큐비트 수 반환.
    ///
    /// MPS 백엔드 (`MpsF64`) 의 경우 `statevector` 가 `None` 일 수 있으므로
    /// 별도 `n_qubits` 필드는 두지 않고 — caller 가 알 수 있는 정보 (회로
    /// 자체로부터) — 이 getter 는 N>20 MPS 결과에선 `panic` 한다.  Python
    /// 측에서 `result.num_qubits` getter 가 필요하면 별도 wiring 필요.
    pub fn num_qubits(&self) -> usize {
        match self {
            SimulationResult::F32 { statevector, .. } => statevector.num_qubits(),
            SimulationResult::F64 { statevector, .. } => statevector.num_qubits(),
            SimulationResult::DensityF32 { density, .. } => density.num_qubits(),
            SimulationResult::DensityF64 { density, .. } => density.num_qubits(),
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => sv.num_qubits(),
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => sv.num_qubits(),
            SimulationResult::MpsF64 {
                statevector: None, ..
            }
            | SimulationResult::MpsF32 {
                statevector: None, ..
            } => panic!(
                "num_qubits(): MPS result with N>20 has no dense statevector — \
                 query the original Circuit::num_qubits() instead"
            ),
        }
    }

    /// 측정 결과 카운트를 반환한다 (정밀도 / 백엔드 무관).
    pub fn counts(&self) -> &HashMap<String, usize> {
        match self {
            SimulationResult::F32 { counts, .. }
            | SimulationResult::F64 { counts, .. }
            | SimulationResult::DensityF32 { counts, .. }
            | SimulationResult::DensityF64 { counts, .. }
            | SimulationResult::MpsF64 { counts, .. }
            | SimulationResult::MpsF32 { counts, .. } => counts,
        }
    }

    /// MPS 백엔드의 사용자 지정 χ_max.  비-MPS 결과면 `None`.
    pub fn mps_max_bond_dim(&self) -> Option<usize> {
        match self {
            SimulationResult::MpsF64 { max_bond_dim, .. }
            | SimulationResult::MpsF32 { max_bond_dim, .. } => Some(*max_bond_dim),
            _ => None,
        }
    }

    /// MPS 백엔드의 SVD truncation 후 squared norm.  1.0 보다 작으면 정보 손실
    /// 발생 (max_bond_dim 을 늘려야 함).  비-MPS 결과면 `None`.
    pub fn mps_final_norm_sq(&self) -> Option<f64> {
        match self {
            SimulationResult::MpsF64 { final_norm_sq, .. }
            | SimulationResult::MpsF32 { final_norm_sq, .. } => Some(*final_norm_sq),
            _ => None,
        }
    }

    /// MPS 백엔드의 누적 SVD discarded weight
    /// `Σ_{SVDs} Σ_{j>=keep} sv_j²` (Schollwöck 2011 §4.5.3, v0.6.3).
    /// 0 이면 무손실, 클수록 truncation 손실이 큼.  `final_norm_sq` 와 달리
    /// 누적값이라 회로 전체의 정확도 metric 으로 사용한다.  비-MPS 결과면
    /// `None`.
    pub fn mps_truncation_error_sum(&self) -> Option<f64> {
        match self {
            SimulationResult::MpsF64 {
                truncation_error_sum,
                ..
            }
            | SimulationResult::MpsF32 {
                truncation_error_sum,
                ..
            } => Some(*truncation_error_sum),
            _ => None,
        }
    }

    /// MPS 백엔드의 사용자 지정 singular-value cutoff (v0.6.5).  `0.0` 이면
    /// disabled — `max_bond_dim` 만으로 truncation.  비-MPS 결과면 `None`.
    pub fn mps_trunc_threshold(&self) -> Option<f64> {
        match self {
            SimulationResult::MpsF64 {
                trunc_threshold, ..
            }
            | SimulationResult::MpsF32 {
                trunc_threshold, ..
            } => Some(*trunc_threshold),
            _ => None,
        }
    }

    /// MPS 백엔드가 회로 종료 시점에 실제로 발생한 최대 internal bond
    /// dimension (v0.6.5).  adaptive truncation (`trunc_threshold > 0`)
    /// 활성 시 일반적으로 사용자가 지정한 `max_bond_dim` 보다 작다 — 회로
    /// 의 실제 entanglement 양에 자동 맞춤.  비-MPS 결과면 `None`.
    pub fn mps_observed_max_bond_dim(&self) -> Option<usize> {
        match self {
            SimulationResult::MpsF64 {
                observed_max_bond_dim,
                ..
            }
            | SimulationResult::MpsF32 {
                observed_max_bond_dim,
                ..
            } => Some(*observed_max_bond_dim),
            _ => None,
        }
    }

    /// f64 statevector 참조. f32 / density 결과면 `None`.  MPS 결과의 경우
    /// N ≤ 20 면 회로 끝에서 contract 된 dense statevector (truncation 후
    /// norm² < 1 일 수 있음), N > 20 면 `None` — `mps_final_norm_sq()` /
    /// `counts()` 만 사용 가능.
    pub fn statevector_f64(&self) -> Option<&StateVector<f64>> {
        match self {
            SimulationResult::F64 { statevector, .. } => Some(statevector),
            SimulationResult::MpsF64 { statevector, .. } => statevector.as_ref(),
            _ => None,
        }
    }

    /// f32 statevector 참조. f64 / density 결과면 `None`.  v0.6.5 부터 MpsF32
    /// 도 dense SV (N≤20) 가 있을 때 반환.
    pub fn statevector_f32(&self) -> Option<&StateVector<f32>> {
        match self {
            SimulationResult::F32 { statevector, .. } => Some(statevector),
            SimulationResult::MpsF32 { statevector, .. } => statevector.as_ref(),
            _ => None,
        }
    }

    /// f64 density matrix 참조 (v0.5.0). statevector / f32 density 결과면 `None`.
    pub fn density_f64(&self) -> Option<&DensityMatrix<f64>> {
        match self {
            SimulationResult::DensityF64 { density, .. } => Some(density),
            _ => None,
        }
    }

    /// f32 density matrix 참조 (v0.5.0). statevector / f64 density 결과면 `None`.
    pub fn density_f32(&self) -> Option<&DensityMatrix<f32>> {
        match self {
            SimulationResult::DensityF32 { density, .. } => Some(density),
            _ => None,
        }
    }

    /// 기본 정밀도 (f64) 인 경우 `&StateVector<f64>` 를 반환. f32 / density 결과에 호출 시 panic.
    /// v0.2.0 호환용 — 새 코드는 `statevector_f64()` / `statevector_f32()` / `density_f64()` 사용 권장.
    pub fn statevector(&self) -> &StateVector<f64> {
        match self {
            SimulationResult::F64 { statevector, .. } => statevector,
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => sv,
            SimulationResult::MpsF64 {
                statevector: None, ..
            } => panic!(
                "statevector(): MPS 결과가 N>20 이라 dense statevector 가 없습니다. counts() 를 사용하세요"
            ),
            SimulationResult::F32 { .. } | SimulationResult::MpsF32 { .. } => {
                panic!("statevector(): f32 결과입니다. statevector_f32() 를 사용하세요")
            }
            SimulationResult::DensityF32 { .. } | SimulationResult::DensityF64 { .. } => {
                panic!("statevector(): density backend 결과입니다. density_f64() / density_f32() 를 사용하세요")
            }
        }
    }

    /// 각 basis state의 확률 벡터를 f64 로 반환한다 (정밀도 / 백엔드 통일).
    ///
    /// statevector 백엔드: `|ψ_b|²`.  density 백엔드: `ρ[b][b]` (대각선).
    /// MPS 백엔드 (N > 20) 는 dense SV 가 없으므로 `panic` — caller 가
    /// `counts()` 또는 `mps_final_norm_sq()` 만 사용해야 한다.
    pub fn probabilities(&self) -> Vec<f64> {
        match self {
            SimulationResult::F64 { statevector, .. } => statevector.probabilities(),
            SimulationResult::F32 { statevector, .. } => statevector
                .probabilities()
                .into_iter()
                .map(|p| p as f64)
                .collect(),
            SimulationResult::DensityF64 { density, .. } => density.diagonal_probabilities(),
            SimulationResult::DensityF32 { density, .. } => density.diagonal_probabilities(),
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => sv.probabilities(),
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => sv
                .probabilities()
                .into_iter()
                .map(|p| p as f64)
                .collect(),
            SimulationResult::MpsF64 {
                statevector: None, ..
            }
            | SimulationResult::MpsF32 {
                statevector: None, ..
            } => panic!(
                "probabilities(): MPS 결과가 N>20 이라 dense probabilities 가 없습니다. counts() 를 사용하세요"
            ),
        }
    }
}
