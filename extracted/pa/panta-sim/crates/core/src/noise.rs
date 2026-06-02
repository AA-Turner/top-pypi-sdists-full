//! 단일 큐비트 노이즈 채널 (v0.4 stochastic trajectory).
//!
//! 4 종 표준 채널의 Kraus 연산자를 정의하고, trajectory 모드에서 무작위
//! Kraus 연산자를 샘플링·적용하는 [`apply_kraus_single_qubit`] 를 제공한다.
//! Density matrix 백엔드는 v0.5 (GPU 와 함께) 의 범위.
//!
//! 참고 (refs.md):
//! - #15 노이즈 수학적 모델링 (depolarizing / amplitude damping 정의).
//! - #16 효율적 depolarization (단일 Kraus 형태 6→4 행렬곱; v0.4 표준 형태로 시작).
//! - §G3 QuantRS2 — 동일 4 채널 + QEC 구현 패턴 reference.

use num_complex::Complex;
use num_traits::NumCast;
use rand::Rng;
use std::sync::Arc;

use crate::complex::{complex, real, zero, Real};
use crate::gates::{Matrix2x2, Matrix4x4};
use crate::operations::{apply_single_qubit_gate, apply_two_qubit_gate};
use crate::statevector::StateVector;

/// 단일 큐비트 노이즈 채널.
///
/// 모든 채널은 **trace-preserving**: `Σ K_i† K_i = I`. 파라미터는 `validate()` 또는
/// 컨스트럭터 (`bit_flip`, `phase_flip`, ...) 에서 범위 검증된다.
///
/// 4 채널의 Kraus 연산자 (refs #15):
/// - **BitFlip(p)**: `K_0 = √(1-p) I`, `K_1 = √p X`
/// - **PhaseFlip(p)**: `K_0 = √(1-p) I`, `K_1 = √p Z`
/// - **Depolarizing(p)**: `K_0 = √(1-3p/4) I`, `K_1 = √(p/4) X`, `K_2 = √(p/4) Y`, `K_3 = √(p/4) Z`
/// - **AmplitudeDamping(γ)**: `K_0 = [[1,0],[0,√(1-γ)]]`, `K_1 = [[0,√γ],[0,0]]`
#[derive(Debug, Clone, PartialEq)]
pub enum NoiseChannel {
    /// Bit-flip 노이즈. 확률 `p` 로 X 적용. p ∈ [0, 1].
    BitFlip { p: f64 },
    /// Phase-flip 노이즈. 확률 `p` 로 Z 적용. p ∈ [0, 1].
    PhaseFlip { p: f64 },
    /// Depolarizing 노이즈. 확률 `p` 로 {X, Y, Z} 균등 적용. p ∈ [0, 1].
    Depolarizing { p: f64 },
    /// Amplitude-damping 노이즈. T1 (에너지 손실) 모델링. γ ∈ [0, 1].
    AmplitudeDamping { gamma: f64 },
    /// Phase damping (dephasing).  `K_0 = diag(1, √(1-γ))`,
    /// `K_1 = diag(0, √γ)`.  Off-diagonal coherence를 감쇠시키되 population
    /// (⟨Z⟩) 은 보존한다 — `T_2` 디코히어런스 모델.  γ ∈ [0, 1].
    PhaseDamping { gamma: f64 },
    /// Generalized amplitude damping (유한 온도 `T_1`).  damping rate γ 와 평형
    /// population 파라미터 `p` (p=1 이면 순수 amplitude damping = 0온도).  4개
    /// Kraus: `K_0=√p·diag(1,√(1-γ))`, `K_1=√p·√γ|0⟩⟨1|`,
    /// `K_2=√(1-p)·diag(√(1-γ),1)`, `K_3=√(1-p)·√γ|1⟩⟨0|`.  γ, p ∈ [0, 1].
    GeneralizedAmplitudeDamping { gamma: f64, p: f64 },
    /// 사용자 정의 단일 큐비트 Kraus 채널 (v0.7.1).  임의의 2×2 Kraus 연산자
    /// 집합 `{K_i}` 를 직접 지정한다.  trace-preserving (`Σ K_i† K_i = I`) 은
    /// [`NoiseChannel::custom`] 에서 검증된다.  `Arc` 로 보관해 `Instruction`
    /// 복제 시 행렬을 복사하지 않는다.
    Custom {
        kraus_ops: Arc<Vec<[[Complex<f64>; 2]; 2]>>,
    },
}

impl NoiseChannel {
    /// BitFlip 채널 생성 (파라미터 검증 포함).
    pub fn bit_flip(p: f64) -> Result<Self, String> {
        validate_prob("bit_flip", "p", p)?;
        Ok(Self::BitFlip { p })
    }

    /// PhaseFlip 채널 생성 (파라미터 검증 포함).
    pub fn phase_flip(p: f64) -> Result<Self, String> {
        validate_prob("phase_flip", "p", p)?;
        Ok(Self::PhaseFlip { p })
    }

    /// Depolarizing 채널 생성 (파라미터 검증 포함).
    pub fn depolarizing(p: f64) -> Result<Self, String> {
        validate_prob("depolarizing", "p", p)?;
        Ok(Self::Depolarizing { p })
    }

    /// PhaseDamping 채널 생성 (파라미터 검증 포함).
    pub fn phase_damping(gamma: f64) -> Result<Self, String> {
        validate_prob("PhaseDamping", "gamma", gamma)?;
        Ok(Self::PhaseDamping { gamma })
    }

    /// GeneralizedAmplitudeDamping 채널 생성 (파라미터 검증 포함).
    pub fn generalized_amplitude_damping(gamma: f64, p: f64) -> Result<Self, String> {
        validate_prob("GeneralizedAmplitudeDamping", "gamma", gamma)?;
        validate_prob("GeneralizedAmplitudeDamping", "p", p)?;
        Ok(Self::GeneralizedAmplitudeDamping { gamma, p })
    }

    /// AmplitudeDamping 채널 생성 (파라미터 검증 포함).
    pub fn amplitude_damping(gamma: f64) -> Result<Self, String> {
        validate_prob("amplitude_damping", "gamma", gamma)?;
        Ok(Self::AmplitudeDamping { gamma })
    }

    /// 사용자 정의 단일 큐비트 Kraus 채널 생성 (v0.7.1).
    ///
    /// `kraus_ops` 는 2×2 복소 행렬 (`[[a, b], [c, d]]`, row-major) 의 리스트.
    /// **trace-preserving** (`Σ K_i† K_i = I`) 을 `1e-9` 허용오차로 검증하며,
    /// 위반 시 `Err` 를 반환한다.  연산자는 1개 이상이어야 한다.
    pub fn custom(kraus_ops: Vec<[[Complex<f64>; 2]; 2]>) -> Result<Self, String> {
        if kraus_ops.is_empty() {
            return Err("custom: Kraus 연산자가 1개 이상 필요합니다".to_string());
        }
        // Σ K_i† K_i = I 검증.  (K†K)[a][b] = Σ_c conj(K[c][a]) K[c][b].
        let mut acc = [[Complex::new(0.0_f64, 0.0); 2]; 2];
        for k in &kraus_ops {
            for a in 0..2 {
                for b in 0..2 {
                    let mut s = Complex::new(0.0_f64, 0.0);
                    for row in k.iter() {
                        s += row[a].conj() * row[b];
                    }
                    acc[a][b] += s;
                }
            }
        }
        let ident = [
            [Complex::new(1.0_f64, 0.0), Complex::new(0.0, 0.0)],
            [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
        ];
        for a in 0..2 {
            for b in 0..2 {
                if (acc[a][b] - ident[a][b]).norm() > 1e-9 {
                    return Err(format!(
                        "custom: Kraus 연산자가 trace-preserving 이 아닙니다 \
                         (Σ K_i† K_i ≠ I, [{a}][{b}] 차이 {:.3e})",
                        (acc[a][b] - ident[a][b]).norm()
                    ));
                }
            }
        }
        Ok(Self::Custom {
            kraus_ops: Arc::new(kraus_ops),
        })
    }

    /// 채널을 단일 큐비트에 적용한다 (v0.4.1 fast-path).
    ///
    /// **최적화**: Pauli 채널 (BitFlip / PhaseFlip / Depolarizing) 의 Kraus
    /// 연산자는 `√p · I/X/Y/Z` 형태로 모두 unitary 의 스칼라배. 따라서
    /// `||K_i |ψ⟩||² = p_i` 가 상태와 무관 — [`kraus_norm_sq`] 의 O(2^n)
    /// 누적을 skip 하고 RNG 1 회만으로 outcome 을 샘플링할 수 있다 (25 큐비트
    /// + 4-Kraus depolarizing 회로에서 ~134M complex 곱셈 절약).
    ///
    /// AmplitudeDamping 만 K_0 가 non-unitary (diag(1, √(1-γ))) 이므로 일반
    /// Kraus path ([`apply_kraus_single_qubit`]) 로 fallback 한다.
    ///
    /// Pauli 채널 적용 후엔 state norm 이 1 그대로 (X/Y/Z 가 unitary) 이므로
    /// `normalize()` 호출도 0.
    pub fn apply_to<F: Real, R: Rng>(
        &self,
        state: &mut StateVector<F>,
        target: usize,
        rng: &mut R,
    ) {
        assert!(
            target < state.num_qubits(),
            "NoiseChannel::apply_to: target {target} 가 범위 벗어남 (n_qubits={})",
            state.num_qubits()
        );
        match self {
            Self::BitFlip { p } => {
                if rng.gen::<f64>() < *p {
                    let m = crate::gates::Gate::X.matrix_2x2::<F>();
                    apply_single_qubit_gate(state, &m, target);
                }
            }
            Self::PhaseFlip { p } => {
                if rng.gen::<f64>() < *p {
                    let m = crate::gates::Gate::Z.matrix_2x2::<F>();
                    apply_single_qubit_gate(state, &m, target);
                }
            }
            Self::Depolarizing { p } => {
                // p_I = 1 - 3p/4, p_X = p_Y = p_Z = p/4.
                let r: f64 = rng.gen();
                let p_i_end = 1.0 - 0.75 * p;
                let p_x_end = p_i_end + 0.25 * p;
                let p_y_end = p_x_end + 0.25 * p;
                let gate = if r < p_i_end {
                    return; // Identity — no-op.
                } else if r < p_x_end {
                    crate::gates::Gate::X
                } else if r < p_y_end {
                    crate::gates::Gate::Y
                } else {
                    crate::gates::Gate::Z
                };
                let m = gate.matrix_2x2::<F>();
                apply_single_qubit_gate(state, &m, target);
            }
            Self::AmplitudeDamping { .. }
            | Self::PhaseDamping { .. }
            | Self::GeneralizedAmplitudeDamping { .. }
            | Self::Custom { .. } => {
                // K_0 가 non-unitary 라 일반 Kraus path 필요.
                let kraus = self.kraus_operators::<F>();
                apply_kraus_single_qubit(state, &kraus, target, rng);
            }
        }
    }

    /// 채널의 Kraus 연산자 리스트를 정밀도 `F` 로 빌드한다.
    ///
    /// 모든 sqrt 는 `f64` 에서 평가 후 `F` 로 다운캐스트 (정밀도 보존).
    pub fn kraus_operators<F: Real>(&self) -> Vec<Matrix2x2<F>> {
        match self {
            Self::BitFlip { p } => {
                let q = (1.0 - p).sqrt();
                let s = p.sqrt();
                vec![
                    [[real::<F>(q), zero()], [zero(), real::<F>(q)]],
                    // X
                    [[zero(), real::<F>(s)], [real::<F>(s), zero()]],
                ]
            }
            Self::PhaseFlip { p } => {
                let q = (1.0 - p).sqrt();
                let s = p.sqrt();
                vec![
                    [[real::<F>(q), zero()], [zero(), real::<F>(q)]],
                    // Z
                    [[real::<F>(s), zero()], [zero(), real::<F>(-s)]],
                ]
            }
            Self::Depolarizing { p } => {
                let q = (1.0 - 0.75 * p).sqrt();
                let s = (p / 4.0).sqrt();
                vec![
                    // √(1-3p/4) I
                    [[real::<F>(q), zero()], [zero(), real::<F>(q)]],
                    // √(p/4) X
                    [[zero(), real::<F>(s)], [real::<F>(s), zero()]],
                    // √(p/4) Y = √(p/4) [[0, -i], [i, 0]]
                    [
                        [zero(), complex::<F>(0.0, -s)],
                        [complex::<F>(0.0, s), zero()],
                    ],
                    // √(p/4) Z
                    [[real::<F>(s), zero()], [zero(), real::<F>(-s)]],
                ]
            }
            Self::AmplitudeDamping { gamma } => {
                let g = (1.0 - gamma).sqrt();
                let s = gamma.sqrt();
                vec![
                    // K_0 = diag(1, √(1-γ))
                    [[real::<F>(1.0), zero()], [zero(), real::<F>(g)]],
                    // K_1 = √γ |0⟩⟨1|
                    [[zero(), real::<F>(s)], [zero(), zero()]],
                ]
            }
            Self::PhaseDamping { gamma } => {
                let g = (1.0 - gamma).sqrt();
                let s = gamma.sqrt();
                vec![
                    // K_0 = diag(1, √(1-γ))
                    [[real::<F>(1.0), zero()], [zero(), real::<F>(g)]],
                    // K_1 = diag(0, √γ)
                    [[zero(), zero()], [zero(), real::<F>(s)]],
                ]
            }
            Self::GeneralizedAmplitudeDamping { gamma, p } => {
                let g = (1.0 - gamma).sqrt();
                let s = gamma.sqrt();
                let sp = p.sqrt();
                let sq = (1.0 - p).sqrt();
                vec![
                    // K_0 = √p · diag(1, √(1-γ))
                    [[real::<F>(sp), zero()], [zero(), real::<F>(sp * g)]],
                    // K_1 = √p · √γ |0⟩⟨1|
                    [[zero(), real::<F>(sp * s)], [zero(), zero()]],
                    // K_2 = √(1-p) · diag(√(1-γ), 1)
                    [[real::<F>(sq * g), zero()], [zero(), real::<F>(sq)]],
                    // K_3 = √(1-p) · √γ |1⟩⟨0|
                    [[zero(), zero()], [real::<F>(sq * s), zero()]],
                ]
            }
            Self::Custom { kraus_ops } => kraus_ops
                .iter()
                .map(|k| {
                    [
                        [
                            complex::<F>(k[0][0].re, k[0][0].im),
                            complex::<F>(k[0][1].re, k[0][1].im),
                        ],
                        [
                            complex::<F>(k[1][0].re, k[1][0].im),
                            complex::<F>(k[1][1].re, k[1][1].im),
                        ],
                    ]
                })
                .collect(),
        }
    }
}

fn validate_prob(channel: &str, name: &str, value: f64) -> Result<(), String> {
    if !(0.0..=1.0).contains(&value) || value.is_nan() {
        return Err(format!("{channel}: {name} must be in [0, 1], got {value}"));
    }
    Ok(())
}

/// 2-큐비트 노이즈 채널 (v0.7.2, correlated noise / crosstalk).
///
/// 임의의 4×4 Kraus 연산자 집합으로 2-큐비트 상관 노이즈를 정의한다.
/// trace-preserving (`Σ K_i† K_i = I₄`) 은 [`NoiseChannel2::custom`] 에서 검증.
#[derive(Debug, Clone, PartialEq)]
pub enum NoiseChannel2 {
    /// 사용자 정의 2-큐비트 Kraus 채널.
    Custom {
        kraus_ops: Arc<Vec<[[Complex<f64>; 4]; 4]>>,
    },
}

impl NoiseChannel2 {
    /// 사용자 정의 2-큐비트 Kraus 채널 생성 (4×4 행렬, trace-preserving 검증).
    pub fn custom(kraus_ops: Vec<[[Complex<f64>; 4]; 4]>) -> Result<Self, String> {
        if kraus_ops.is_empty() {
            return Err("custom2: Kraus 연산자가 1개 이상 필요합니다".to_string());
        }
        // Σ K_i† K_i = I₄.  (K†K)[a][b] = Σ_c conj(K[c][a]) K[c][b].
        let mut acc = [[Complex::new(0.0_f64, 0.0); 4]; 4];
        for k in &kraus_ops {
            for a in 0..4 {
                for b in 0..4 {
                    let mut s = Complex::new(0.0_f64, 0.0);
                    for row in k.iter() {
                        s += row[a].conj() * row[b];
                    }
                    acc[a][b] += s;
                }
            }
        }
        for (a, acc_row) in acc.iter().enumerate() {
            for (b, &acc_ab) in acc_row.iter().enumerate() {
                let expect = if a == b { 1.0 } else { 0.0 };
                let diff = (acc_ab - Complex::new(expect, 0.0)).norm();
                if diff > 1e-9 {
                    return Err(format!(
                        "custom2: Kraus 연산자가 trace-preserving 이 아닙니다 \
                         (Σ K_i† K_i ≠ I₄, [{a}][{b}] 차이 {diff:.3e})"
                    ));
                }
            }
        }
        Ok(Self::Custom {
            kraus_ops: Arc::new(kraus_ops),
        })
    }

    /// 정밀도 `F` 의 4×4 Kraus 연산자 리스트.
    pub fn kraus_operators<F: Real>(&self) -> Vec<Matrix4x4<F>> {
        match self {
            Self::Custom { kraus_ops } => kraus_ops
                .iter()
                .map(|k| {
                    let mut m = [[zero::<F>(); 4]; 4];
                    for (i, krow) in k.iter().enumerate() {
                        for (j, &c) in krow.iter().enumerate() {
                            m[i][j] = complex::<F>(c.re, c.im);
                        }
                    }
                    m
                })
                .collect(),
        }
    }

    /// 채널을 두 큐비트에 적용한다 (trajectory: ‖Kᵢψ‖² 샘플링).
    pub fn apply_to<F: Real, R: Rng>(
        &self,
        state: &mut StateVector<F>,
        q0: usize,
        q1: usize,
        rng: &mut R,
    ) {
        let kraus = self.kraus_operators::<F>();
        apply_kraus_two_qubit(state, &kraus, q0, q1, rng);
    }
}

/// 2-큐비트 Kraus 연산자 집합을 trajectory 방식으로 적용한다.
///
/// 각 `Kᵢ` 적용 후 노름 ``‖Kᵢψ‖²`` 으로 확률을 계산해 (state clone) 하나를
/// 샘플링한 뒤 적용·재정규화한다.  off-diagonal 까지 정확.
pub fn apply_kraus_two_qubit<F: Real, R: Rng>(
    state: &mut StateVector<F>,
    kraus: &[Matrix4x4<F>],
    q0: usize,
    q1: usize,
    rng: &mut R,
) {
    let norm_sq = |sv: &StateVector<F>| -> f64 {
        sv.amplitudes()
            .iter()
            .map(|a| {
                let r: f64 = NumCast::from(a.re).expect("F → f64");
                let im: f64 = NumCast::from(a.im).expect("F → f64");
                r * r + im * im
            })
            .sum()
    };
    let mut cdf = Vec::with_capacity(kraus.len());
    let mut acc = 0.0_f64;
    for k in kraus {
        let mut clone = state.clone();
        apply_two_qubit_gate(&mut clone, k, q0, q1);
        acc += norm_sq(&clone).max(0.0);
        cdf.push(acc);
    }
    let r = rng.gen::<f64>() * acc.max(1e-300);
    let idx = cdf.iter().position(|&c| r < c).unwrap_or(kraus.len() - 1);
    apply_two_qubit_gate(state, &kraus[idx], q0, q1);
    state.normalize();
}

/// Kraus 연산자 집합을 trajectory 방식으로 단일 큐비트에 적용한다.
///
/// 1. 각 K_i 에 대해 `p_i = ||K_i |ψ⟩||²` 계산 (target 큐비트 amplitude pair 순회).
/// 2. CDF + RNG 로 인덱스 샘플링.
/// 3. 선택된 K_i 를 [`apply_single_qubit_gate`] 로 적용.
/// 4. norm 보정을 위해 `normalize()`.
///
/// 채널이 trace-preserving 이면 `Σ p_i = 1` 이어야 한다 (CDF 마지막 원소 1.0 강제로
/// floating drift 방어). 누적/CDF 는 항상 f64 (큰 N 에서 f32 mantissa 손실 방지 —
/// `measurement::build_cdf` 와 동일 패턴).
pub fn apply_kraus_single_qubit<F: Real, R: Rng>(
    state: &mut StateVector<F>,
    kraus_ops: &[Matrix2x2<F>],
    target: usize,
    rng: &mut R,
) {
    assert!(
        target < state.num_qubits(),
        "apply_kraus_single_qubit: target {target} 가 범위 벗어남 (n_qubits={})",
        state.num_qubits()
    );
    assert!(
        !kraus_ops.is_empty(),
        "apply_kraus_single_qubit: kraus_ops 가 비었음"
    );

    // Step 1: 각 K_i 의 결과 norm² 합산.
    let probs: Vec<f64> = kraus_ops
        .iter()
        .map(|m| kraus_norm_sq(state, m, target))
        .collect();

    // Step 2: CDF 빌드 + 샘플링 (measurement::build_cdf 와 동일 패턴).
    let mut cdf: Vec<f64> = Vec::with_capacity(probs.len());
    let mut acc: f64 = 0.0;
    for p in &probs {
        acc += p;
        cdf.push(acc);
    }
    if let Some(last) = cdf.last_mut() {
        *last = 1.0;
    }
    let r: f64 = rng.gen();
    let chosen = cdf.partition_point(|&c| c <= r).min(cdf.len() - 1);

    // Step 3 + 4: 선택된 K_i 적용 후 정규화.
    apply_single_qubit_gate(state, &kraus_ops[chosen], target);
    state.normalize();
}

/// `||K |ψ⟩||²` 계산 — 결과 상태를 만들지 않고 norm² 만 누적 (메모리 절감).
///
/// target 큐비트 인덱스 기준 amplitude pair (a, b) 순회. K = [[m00, m01], [m10, m11]] 일 때
/// `K · (a, b)ᵀ = (m00 a + m01 b,  m10 a + m11 b)`. 두 결과 amplitude 의 norm² 합산.
fn kraus_norm_sq<F: Real>(state: &StateVector<F>, matrix: &Matrix2x2<F>, target: usize) -> f64 {
    let amps = state.amplitudes();
    let n = amps.len();
    let stride = 1usize << target;
    let m00 = matrix[0][0];
    let m01 = matrix[0][1];
    let m10 = matrix[1][0];
    let m11 = matrix[1][1];

    let mut total: f64 = 0.0;
    let mut i = 0;
    while i < n {
        for j in i..i + stride {
            let k = j + stride;
            let a = amps[j];
            let b = amps[k];
            let new_a: Complex<F> = m00 * a + m01 * b;
            let new_b: Complex<F> = m10 * a + m11 * b;
            let na: f64 = NumCast::from(new_a.norm_sqr()).expect("F → f64 변환 실패");
            let nb: f64 = NumCast::from(new_b.norm_sqr()).expect("F → f64 변환 실패");
            total += na + nb;
        }
        i += stride << 1;
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complex::{approx_eq, ONE, ZERO};
    use crate::gates::Gate;
    use crate::operations::apply_single_qubit_gate;
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    #[test]
    fn test_custom_kraus_equals_amplitude_damping() {
        // 사용자 정의 Kraus 로 amplitude damping 을 재현 → 동일 Kraus 연산자.
        let g: f64 = 0.3;
        let k0 = [
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
            [Complex::new(0.0, 0.0), Complex::new((1.0 - g).sqrt(), 0.0)],
        ];
        let k1 = [
            [Complex::new(0.0, 0.0), Complex::new(g.sqrt(), 0.0)],
            [Complex::new(0.0, 0.0), Complex::new(0.0, 0.0)],
        ];
        let custom = NoiseChannel::custom(vec![k0, k1]).unwrap();
        let builtin = NoiseChannel::AmplitudeDamping { gamma: g };
        let kc = custom.kraus_operators::<f64>();
        let kb = builtin.kraus_operators::<f64>();
        assert_eq!(kc.len(), kb.len());
        for (a, b) in kc.iter().zip(kb.iter()) {
            for i in 0..2 {
                for j in 0..2 {
                    assert!(approx_eq(a[i][j], b[i][j], 1e-12));
                }
            }
        }
    }

    #[test]
    fn test_custom_kraus_rejects_non_trace_preserving() {
        // Σ K_i† K_i ≠ I → Err.
        let bad = [
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
            [Complex::new(0.0, 0.0), Complex::new(0.5, 0.0)],
        ];
        assert!(NoiseChannel::custom(vec![bad]).is_err());
        assert!(NoiseChannel::custom(vec![]).is_err());
    }

    #[test]
    fn test_custom2_tensor_product_equals_sequential_1q_density() {
        // {A_i ⊗ B_j} 2-큐비트 Kraus (A,B = amplitude damping) 의 density 적용이
        // q0 에 A, q1 에 B 를 순차 적용한 것과 동일.
        use crate::density::DensityMatrix;
        let ga = 0.3_f64;
        let gb = 0.5_f64;
        let ad = |g: f64| {
            [
                [
                    [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new((1.0 - g).sqrt(), 0.0)],
                ],
                [
                    [Complex::new(0.0, 0.0), Complex::new(g.sqrt(), 0.0)],
                    [Complex::new(0.0, 0.0), Complex::new(0.0, 0.0)],
                ],
            ]
        };
        let a = ad(ga);
        let b = ad(gb);
        // 2-큐비트 Kraus = {A_i ⊗ B_j}, 4×4 (큐비트 0 = LSB = B, 큐비트 1 = A).
        let mut ops4: Vec<[[Complex<f64>; 4]; 4]> = Vec::new();
        for ai in &a {
            for bj in &b {
                let mut m = [[Complex::new(0.0, 0.0); 4]; 4];
                for r1 in 0..2 {
                    for r0 in 0..2 {
                        for c1 in 0..2 {
                            for c0 in 0..2 {
                                // index = 2*qubit1 + qubit0.
                                m[2 * r1 + r0][2 * c1 + c0] = ai[r1][c1] * bj[r0][c0];
                            }
                        }
                    }
                }
                ops4.push(m);
            }
        }
        // 초기 상태: H⊗H |00> 의 density.
        let mut sv = StateVector::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &h, 0);
        apply_single_qubit_gate(&mut sv, &h, 1);
        let mut rho_2q = DensityMatrix::<f64>::from_pure_state(&sv);
        rho_2q.apply_kraus_2q(
            &NoiseChannel2::custom(ops4)
                .unwrap()
                .kraus_operators::<f64>(),
            0,
            1,
        );

        let mut rho_seq = DensityMatrix::<f64>::from_pure_state(&sv);
        rho_seq.apply_kraus_1q(
            &NoiseChannel::custom(b.to_vec())
                .unwrap()
                .kraus_operators::<f64>(),
            0,
        );
        rho_seq.apply_kraus_1q(
            &NoiseChannel::custom(a.to_vec())
                .unwrap()
                .kraus_operators::<f64>(),
            1,
        );

        for i in 0..16 {
            assert!(
                approx_eq(rho_2q.data()[i], rho_seq.data()[i], 1e-12),
                "element {i} 불일치"
            );
        }
    }

    #[test]
    fn test_custom2_rejects_non_trace_preserving() {
        let mut bad = [[Complex::new(0.0, 0.0); 4]; 4];
        bad[0][0] = Complex::new(0.5, 0.0); // Σ K†K ≠ I₄.
        assert!(NoiseChannel2::custom(vec![bad]).is_err());
        assert!(NoiseChannel2::custom(vec![]).is_err());
    }

    fn h_state(qubits: usize) -> StateVector<f64> {
        let mut sv = StateVector::<f64>::new(qubits);
        let h = Gate::H.matrix_2x2::<f64>();
        for q in 0..qubits {
            apply_single_qubit_gate(&mut sv, &h, q);
        }
        sv
    }

    #[test]
    fn test_param_validation() {
        assert!(NoiseChannel::bit_flip(-0.1).is_err());
        assert!(NoiseChannel::bit_flip(1.5).is_err());
        assert!(NoiseChannel::bit_flip(f64::NAN).is_err());
        assert!(NoiseChannel::bit_flip(0.0).is_ok());
        assert!(NoiseChannel::bit_flip(1.0).is_ok());
        assert!(NoiseChannel::depolarizing(0.5).is_ok());
        assert!(NoiseChannel::amplitude_damping(0.7).is_ok());
    }

    /// 모든 채널의 Kraus 연산자가 trace-preserving (Σ K_i† K_i = I) 인지.
    fn assert_trace_preserving(channel: NoiseChannel) {
        let kraus = channel.kraus_operators::<f64>();
        // Σ K_i† K_i 계산.
        let mut sum: [[Complex<f64>; 2]; 2] = [[ZERO, ZERO], [ZERO, ZERO]];
        for k in &kraus {
            // K† 계산 (adjoint).
            let kdg = [
                [k[0][0].conj(), k[1][0].conj()],
                [k[0][1].conj(), k[1][1].conj()],
            ];
            // K† · K
            for i in 0..2 {
                for j in 0..2 {
                    let s = (0..2).map(|m| kdg[i][m] * k[m][j]).sum::<Complex<f64>>();
                    sum[i][j] += s;
                }
            }
        }
        assert!(approx_eq(sum[0][0], ONE, 1e-12), "{channel:?}: (0,0) ≠ 1");
        assert!(approx_eq(sum[1][1], ONE, 1e-12), "{channel:?}: (1,1) ≠ 1");
        assert!(approx_eq(sum[0][1], ZERO, 1e-12), "{channel:?}: (0,1) ≠ 0");
        assert!(approx_eq(sum[1][0], ZERO, 1e-12), "{channel:?}: (1,0) ≠ 0");
    }

    #[test]
    fn test_bit_flip_trace_preserving() {
        for p in [0.0, 0.1, 0.5, 0.9, 1.0] {
            assert_trace_preserving(NoiseChannel::BitFlip { p });
        }
    }

    #[test]
    fn test_phase_flip_trace_preserving() {
        for p in [0.0, 0.1, 0.5, 0.9, 1.0] {
            assert_trace_preserving(NoiseChannel::PhaseFlip { p });
        }
    }

    #[test]
    fn test_phase_damping_trace_preserving() {
        for gamma in [0.0, 0.1, 0.5, 0.9, 1.0] {
            assert_trace_preserving(NoiseChannel::PhaseDamping { gamma });
        }
        assert!(NoiseChannel::phase_damping(0.3).is_ok());
        assert!(NoiseChannel::phase_damping(-0.1).is_err());
    }

    #[test]
    fn test_generalized_amplitude_damping_trace_preserving() {
        for gamma in [0.0, 0.3, 0.7, 1.0] {
            for p in [0.0, 0.25, 0.5, 1.0] {
                assert_trace_preserving(NoiseChannel::GeneralizedAmplitudeDamping { gamma, p });
            }
        }
        assert!(NoiseChannel::generalized_amplitude_damping(0.3, 0.5).is_ok());
        assert!(NoiseChannel::generalized_amplitude_damping(0.3, 1.5).is_err());
    }

    #[test]
    fn test_gad_p1_reduces_to_amplitude_damping() {
        // p=1 이면 generalized amplitude damping = amplitude damping.
        let gad = NoiseChannel::GeneralizedAmplitudeDamping { gamma: 0.4, p: 1.0 }
            .kraus_operators::<f64>();
        let ad = NoiseChannel::AmplitudeDamping { gamma: 0.4 }.kraus_operators::<f64>();
        // GAD 의 K_0,K_1 가 AD 의 K_0,K_1 와 일치 (K_2,K_3 는 0).
        for i in 0..2 {
            for j in 0..2 {
                assert!(approx_eq(gad[0][i][j], ad[0][i][j], 1e-12));
                assert!(approx_eq(gad[1][i][j], ad[1][i][j], 1e-12));
                assert!(approx_eq(gad[2][i][j], ZERO, 1e-12));
                assert!(approx_eq(gad[3][i][j], ZERO, 1e-12));
            }
        }
    }

    #[test]
    fn test_depolarizing_trace_preserving() {
        for p in [0.0, 0.1, 0.5, 0.9, 1.0] {
            assert_trace_preserving(NoiseChannel::Depolarizing { p });
        }
    }

    #[test]
    fn test_amplitude_damping_trace_preserving() {
        for gamma in [0.0, 0.1, 0.5, 0.9, 1.0] {
            assert_trace_preserving(NoiseChannel::AmplitudeDamping { gamma });
        }
    }

    /// p=0: identity 채널 → state 무변화.
    #[test]
    fn test_bit_flip_p_zero_identity() {
        let mut sv = h_state(1);
        let before = sv.amplitudes().to_vec();
        let kraus = NoiseChannel::BitFlip { p: 0.0 }.kraus_operators::<f64>();
        let mut rng = StdRng::seed_from_u64(42);
        apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
        for (a, b) in sv.amplitudes().iter().zip(before.iter()) {
            assert!(approx_eq(*a, *b, 1e-12));
        }
    }

    /// p=1: BitFlip 은 항상 X 적용 → |0⟩ → |1⟩.
    #[test]
    fn test_bit_flip_p_one_is_x() {
        let mut sv = StateVector::<f64>::new(1);
        let kraus = NoiseChannel::BitFlip { p: 1.0 }.kraus_operators::<f64>();
        let mut rng = StdRng::seed_from_u64(42);
        apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-12));
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-12));
    }

    /// p=1: PhaseFlip 은 항상 Z 적용 → |+⟩ → |−⟩.
    #[test]
    fn test_phase_flip_p_one_is_z() {
        let mut sv = h_state(1); // |+⟩
        let kraus = NoiseChannel::PhaseFlip { p: 1.0 }.kraus_operators::<f64>();
        let mut rng = StdRng::seed_from_u64(42);
        apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
        let inv_sqrt2 = std::f64::consts::FRAC_1_SQRT_2;
        assert!(approx_eq(
            sv.amplitudes()[0],
            Complex::new(inv_sqrt2, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            sv.amplitudes()[1],
            Complex::new(-inv_sqrt2, 0.0),
            1e-12
        ));
    }

    /// γ=1: AmplitudeDamping 은 |1⟩ → |0⟩ 강제 (T1 = 0 한계).
    #[test]
    fn test_amplitude_damping_gamma_one_decays_to_ground() {
        let mut sv = StateVector::<f64>::new(1);
        // |1⟩ 상태 만들기.
        let x = Gate::X.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &x, 0);
        let kraus = NoiseChannel::AmplitudeDamping { gamma: 1.0 }.kraus_operators::<f64>();
        let mut rng = StdRng::seed_from_u64(42);
        apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
        assert!(approx_eq(sv.amplitudes()[0], ONE, 1e-12));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-12));
    }

    /// p=0.5 BitFlip on |0⟩: 큰 shots 에서 ratio ≈ 0.5 ± 3σ binomial.
    #[test]
    fn test_bit_flip_statistical() {
        let trials = 10_000;
        let p = 0.3;
        let mut count_one = 0;
        let mut rng = StdRng::seed_from_u64(123);
        for _ in 0..trials {
            let mut sv = StateVector::<f64>::new(1);
            let kraus = NoiseChannel::BitFlip { p }.kraus_operators::<f64>();
            apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
            // |1⟩ 상태인지: amplitude[1] ≈ 1 인지 (BitFlip 결과는 |0⟩ 또는 |1⟩ 둘 중 하나).
            if sv.amplitudes()[1].norm_sqr() > 0.5 {
                count_one += 1;
            }
        }
        let observed_p = count_one as f64 / trials as f64;
        // 3σ binomial bound = 3 √(p(1-p)/N) ≈ 0.014 at p=0.3, N=10000.
        assert!(
            (observed_p - p).abs() < 0.02,
            "BitFlip(p={p}) 통계적 ratio {observed_p} 가 기대값 {p} 와 너무 다름"
        );
    }

    /// f32 경로도 동일 동작.
    #[test]
    fn test_kraus_works_with_f32() {
        let mut sv = StateVector::<f32>::new(1);
        let kraus = NoiseChannel::BitFlip { p: 1.0 }.kraus_operators::<f32>();
        let mut rng = StdRng::seed_from_u64(7);
        apply_kraus_single_qubit(&mut sv, &kraus, 0, &mut rng);
        assert!(sv.amplitudes()[0].norm_sqr() < 1e-6);
        assert!((sv.amplitudes()[1].norm_sqr() - 1.0).abs() < 1e-6);
    }

    // ===== v0.4.1 Cut B: Pauli channel fast-path =====

    /// Pauli fast-path 도 boundary 에서 결정론적이어야.
    #[test]
    fn test_apply_to_bit_flip_p_one_is_x() {
        let mut sv = StateVector::<f64>::new(1);
        let mut rng = StdRng::seed_from_u64(42);
        NoiseChannel::BitFlip { p: 1.0 }.apply_to(&mut sv, 0, &mut rng);
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-12));
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-12));
    }

    #[test]
    fn test_apply_to_phase_flip_p_one_is_z_on_plus() {
        let mut sv = h_state(1);
        let mut rng = StdRng::seed_from_u64(42);
        NoiseChannel::PhaseFlip { p: 1.0 }.apply_to(&mut sv, 0, &mut rng);
        let inv_sqrt2 = std::f64::consts::FRAC_1_SQRT_2;
        assert!(approx_eq(
            sv.amplitudes()[0],
            Complex::new(inv_sqrt2, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            sv.amplitudes()[1],
            Complex::new(-inv_sqrt2, 0.0),
            1e-12
        ));
    }

    /// Pauli fast-path 통계: BitFlip(p=0.3) on |0⟩ trial 평균이 ≈ 0.3.
    #[test]
    fn test_apply_to_bit_flip_statistical() {
        let trials = 10_000;
        let p = 0.3;
        let mut count_one = 0;
        let mut rng = StdRng::seed_from_u64(2024);
        for _ in 0..trials {
            let mut sv = StateVector::<f64>::new(1);
            NoiseChannel::BitFlip { p }.apply_to(&mut sv, 0, &mut rng);
            if sv.amplitudes()[1].norm_sqr() > 0.5 {
                count_one += 1;
            }
        }
        let observed = count_one as f64 / trials as f64;
        assert!(
            (observed - p).abs() < 0.02,
            "BitFlip apply_to(p={p}) statistical: observed {observed}"
        );
    }

    /// Pauli 적용 후 state norm 이 1 그대로 (normalize 호출 0).
    #[test]
    fn test_apply_to_pauli_preserves_norm() {
        let mut sv = h_state(2); // |+⟩|+⟩, norm 1
        let mut rng = StdRng::seed_from_u64(7);
        NoiseChannel::Depolarizing { p: 0.5 }.apply_to(&mut sv, 1, &mut rng);
        let norm_sq: f64 = sv.amplitudes().iter().map(|a| a.norm_sqr()).sum();
        assert!((norm_sq - 1.0).abs() < 1e-12);
    }

    /// AmplitudeDamping 은 fast-path 가 아니라 일반 Kraus path 로 fallback.
    /// γ=1, |1⟩ → |0⟩ 강제.
    #[test]
    fn test_apply_to_amplitude_damping_uses_kraus_path() {
        let mut sv = StateVector::<f64>::new(1);
        let x = crate::gates::Gate::X.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &x, 0);
        let mut rng = StdRng::seed_from_u64(42);
        NoiseChannel::AmplitudeDamping { gamma: 1.0 }.apply_to(&mut sv, 0, &mut rng);
        assert!(approx_eq(sv.amplitudes()[0], ONE, 1e-12));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-12));
    }
}
