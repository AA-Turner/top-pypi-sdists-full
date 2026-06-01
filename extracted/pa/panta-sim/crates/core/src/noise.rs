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

use crate::complex::{complex, real, zero, Real};
use crate::gates::Matrix2x2;
use crate::operations::apply_single_qubit_gate;
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
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum NoiseChannel {
    /// Bit-flip 노이즈. 확률 `p` 로 X 적용. p ∈ [0, 1].
    BitFlip { p: f64 },
    /// Phase-flip 노이즈. 확률 `p` 로 Z 적용. p ∈ [0, 1].
    PhaseFlip { p: f64 },
    /// Depolarizing 노이즈. 확률 `p` 로 {X, Y, Z} 균등 적용. p ∈ [0, 1].
    Depolarizing { p: f64 },
    /// Amplitude-damping 노이즈. T1 (에너지 손실) 모델링. γ ∈ [0, 1].
    AmplitudeDamping { gamma: f64 },
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

    /// AmplitudeDamping 채널 생성 (파라미터 검증 포함).
    pub fn amplitude_damping(gamma: f64) -> Result<Self, String> {
        validate_prob("amplitude_damping", "gamma", gamma)?;
        Ok(Self::AmplitudeDamping { gamma })
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
            Self::AmplitudeDamping { .. } => {
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
        }
    }
}

fn validate_prob(channel: &str, name: &str, value: f64) -> Result<(), String> {
    if !(0.0..=1.0).contains(&value) || value.is_nan() {
        return Err(format!("{channel}: {name} must be in [0, 1], got {value}"));
    }
    Ok(())
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
