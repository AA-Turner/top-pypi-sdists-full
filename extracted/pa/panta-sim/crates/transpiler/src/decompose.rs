//! Z-Y-Z (Euler) 분해.
//!
//! 임의 1큐비트 unitary `U ∈ U(2)` 는 Nielsen-Chuang Theorem 4.1 에 따라
//! 네 실수 `(α, β, γ, δ)` 로 다음과 같이 분해된다:
//!
//! ```text
//! U = e^(iα) · Rz(β) · Ry(γ) · Rz(δ)
//! ```
//!
//! 여기서 `Rz(θ) = diag(e^(-iθ/2), e^(iθ/2))`, `Ry(θ)` 는 표준 정의.
//!
//! 회로에 적용할 때는 실제 게이트 적용 순서가 행렬 곱의 역순이므로
//! `Rz(δ); Ry(γ); Rz(β)` 순으로 추가한다 ([`append_unitary`] 참조).
//! `α` 는 Circuit 의 global_phase 에 누적된다.

use num_complex::Complex;
use qsim_simulator::Circuit;

/// 2×2 복소 행렬.
pub type Matrix2 = [[Complex<f64>; 2]; 2];

/// `U = e^(iα) · Rz(β) · Ry(γ) · Rz(δ)` 의 네 파라미터.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ZyzDecomposition {
    /// 글로벌 phase.
    pub alpha: f64,
    /// 첫 번째 (왼쪽) Rz 각도.
    pub beta: f64,
    /// Ry 각도. 항상 `[0, π]` 범위.
    pub gamma: f64,
    /// 두 번째 (오른쪽) Rz 각도.
    pub delta: f64,
}

/// 분기 기준 허용 오차.
const ZYZ_EPS: f64 = 1e-12;

/// 임의 2×2 unitary 를 Z-Y-Z 분해한다.
///
/// 입력은 unitary 라고 가정한다 (검증은 [`crate::validate::is_unitary_2x2`] 가
/// 별도 담당). 비-unitary 입력에 대한 동작은 정의되지 않는다.
pub fn decompose_unitary_zyz(u: &Matrix2) -> ZyzDecomposition {
    let u00 = u[0][0];
    let u01 = u[0][1];
    let u10 = u[1][0];
    let u11 = u[1][1];

    // det(U) = e^(2iα). U(2) 에서 |det| = 1.
    let det = u00 * u11 - u01 * u10;
    let alpha = det.arg() / 2.0;

    // V = e^(-iα) · U  →  det(V) = 1, V ∈ SU(2).
    let phase = Complex::new(alpha.cos(), -alpha.sin()); // e^(-iα)
    let v00 = phase * u00;
    let v01 = phase * u01;
    let v10 = phase * u10;
    let v11 = phase * u11;

    // SU(2) 매개변수화:
    //   V = [[ cos(γ/2)·e^(-i(β+δ)/2), -sin(γ/2)·e^(-i(β-δ)/2)],
    //        [ sin(γ/2)·e^( i(β-δ)/2),  cos(γ/2)·e^( i(β+δ)/2)]]
    //
    // ⇒ |v00| = |v11| = cos(γ/2),  |v10| = |v01| = sin(γ/2).
    let abs_v00 = v00.norm();
    let abs_v10 = v10.norm();

    // γ ∈ [0, π] 이므로 atan2 결과를 두 배 한 값.
    let gamma = 2.0 * abs_v10.atan2(abs_v00);

    // β+δ 는 v11 의 위상에서 (= 2·arg(v11)),  β-δ 는 v10 의 위상에서
    // (= 2·arg(v10)) 직접 회수한다. `arg(v11) - arg(v00)` 형태는 v00, v11
    // 둘 다 음의 실수축 위 (arg = π) 일 때 wraparound 으로 0 이 되어버리는
    // 버그가 있어 사용하지 않는다 (예: V = -I).
    let (beta, delta) = if abs_v00 > ZYZ_EPS && abs_v10 > ZYZ_EPS {
        // 일반 케이스: γ ∈ (0, π) 엄격.
        let sum = 2.0 * v11.arg(); // β + δ
        let diff = 2.0 * v10.arg(); // β − δ
        (0.5 * (sum + diff), 0.5 * (sum - diff))
    } else if abs_v10 < ZYZ_EPS {
        // γ ≈ 0: V 는 대각. β+δ 만 의미 있음, δ = 0 으로 gauge fix.
        let sum = 2.0 * v11.arg();
        (sum, 0.0)
    } else {
        // |v00| < ZYZ_EPS, γ ≈ π: V 는 반대각. β-δ 만 의미 있음, δ = 0 으로 gauge fix.
        let diff = 2.0 * v10.arg();
        (diff, 0.0)
    };

    // v01 은 위 분기에서 직접 사용되지 않지만, 향후 cross-validation 용으로 남겨둔다.
    let _ = v01;

    ZyzDecomposition {
        alpha,
        beta,
        gamma,
        delta,
    }
}

/// 임의 2×2 unitary 행렬을 회로의 `qubit` 큐비트에 적용한다.
///
/// 분해 결과 `Rz(δ); Ry(γ); Rz(β)` 를 순서대로 회로에 추가하고, 글로벌 phase
/// `α` 는 `circuit.add_global_phase(α)` 로 누적한다.
///
/// 입력 행렬의 unitarity 는 검증하지 않는다 — 호출자가
/// [`crate::validate::is_unitary_2x2`] 로 사전 검사해야 한다.
pub fn append_unitary(circuit: &mut Circuit, u: &Matrix2, qubit: usize) {
    let zyz = decompose_unitary_zyz(u);
    circuit.rz(zyz.delta, qubit);
    circuit.ry(zyz.gamma, qubit);
    circuit.rz(zyz.beta, qubit);
    circuit.add_global_phase(zyz.alpha);
}

/// `Rz(β) · Ry(γ) · Rz(δ)` 를 직접 곱해 SU(2) 행렬을 재구성한다 (테스트용).
#[cfg(test)]
fn rebuild_su2(beta: f64, gamma: f64, delta: f64) -> Matrix2 {
    let cb = (gamma / 2.0).cos();
    let sb = (gamma / 2.0).sin();
    let half_plus = 0.5 * (beta + delta);
    let half_minus = 0.5 * (beta - delta);
    let m00 = Complex::from_polar(cb, -half_plus);
    let m01 = Complex::from_polar(-sb, -half_minus);
    let m10 = Complex::from_polar(sb, half_minus);
    let m11 = Complex::from_polar(cb, half_plus);
    [[m00, m01], [m10, m11]]
}

/// 분해 결과를 다시 곱해 `e^(iα)·Rz(β)·Ry(γ)·Rz(δ)` 를 만든다 (테스트용).
#[cfg(test)]
fn rebuild_full(zyz: &ZyzDecomposition) -> Matrix2 {
    let su2 = rebuild_su2(zyz.beta, zyz.gamma, zyz.delta);
    let phase = Complex::from_polar(1.0, zyz.alpha);
    [
        [phase * su2[0][0], phase * su2[0][1]],
        [phase * su2[1][0], phase * su2[1][1]],
    ]
}

#[cfg(test)]
fn matrix_close(a: &Matrix2, b: &Matrix2, tol: f64) -> bool {
    for r in 0..2 {
        for c in 0..2 {
            if (a[r][c] - b[r][c]).norm() > tol {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::f64::consts::{FRAC_1_SQRT_2, PI};

    fn c(re: f64, im: f64) -> Complex<f64> {
        Complex::new(re, im)
    }

    #[test]
    fn test_decompose_identity_round_trip() {
        let u = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_pauli_x() {
        let u = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!((zyz.gamma - PI).abs() < 1e-12);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_pauli_z() {
        let u = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(-1.0, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!(zyz.gamma.abs() < 1e-12); // 대각
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_pauli_y() {
        let u = [[c(0.0, 0.0), c(0.0, -1.0)], [c(0.0, 1.0), c(0.0, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_hadamard() {
        let s = FRAC_1_SQRT_2;
        let u = [[c(s, 0.0), c(s, 0.0)], [c(s, 0.0), c(-s, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_diagonal_phase() {
        let theta: f64 = 0.73;
        let u = [
            [c(1.0, 0.0), c(0.0, 0.0)],
            [c(0.0, 0.0), c(theta.cos(), theta.sin())],
        ];
        let zyz = decompose_unitary_zyz(&u);
        assert!(zyz.gamma.abs() < 1e-12);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_antidiagonal() {
        // [[0, e^(iφ)], [e^(iψ), 0]]: γ = π 분기.
        let phi = 0.4;
        let psi = -1.1;
        let u = [
            [c(0.0, 0.0), Complex::from_polar(1.0, phi)],
            [Complex::from_polar(1.0, psi), c(0.0, 0.0)],
        ];
        let zyz = decompose_unitary_zyz(&u);
        assert!((zyz.gamma - PI).abs() < 1e-12);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_rz_rotation() {
        // Rz(θ) = diag(e^(-iθ/2), e^(iθ/2))
        let theta: f64 = 1.7;
        let u = [
            [Complex::from_polar(1.0, -theta / 2.0), c(0.0, 0.0)],
            [c(0.0, 0.0), Complex::from_polar(1.0, theta / 2.0)],
        ];
        let zyz = decompose_unitary_zyz(&u);
        assert!(zyz.gamma.abs() < 1e-12);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_ry_rotation() {
        // Ry(θ) = [[cos(θ/2), -sin(θ/2)], [sin(θ/2), cos(θ/2)]]
        let theta: f64 = 0.9;
        let cb = (theta / 2.0).cos();
        let sb = (theta / 2.0).sin();
        let u = [[c(cb, 0.0), c(-sb, 0.0)], [c(sb, 0.0), c(cb, 0.0)]];
        let zyz = decompose_unitary_zyz(&u);
        assert!((zyz.gamma - theta).abs() < 1e-12);
        assert!(matrix_close(&rebuild_full(&zyz), &u, 1e-12));
    }

    #[test]
    fn test_decompose_random_haar_unitaries() {
        // Haar-random SU(2) ∼ axis-angle on Bloch sphere.
        // 시드 고정으로 회귀 케이스 포함.
        let seeds: &[(f64, f64, f64, f64)] = &[
            (0.31, 0.42, 0.53, 0.64),
            (1.7, 0.1, -0.5, 2.2),
            (3.0, -1.0, 0.7, -0.3),
            (0.001, 0.001, 0.001, 0.001), // 거의 항등
            (PI - 1e-10, 0.5, -0.7, 0.2), // γ ≈ π 경계
            (1e-10, 0.5, -0.7, 0.2),      // γ ≈ 0 경계
            (0.5, 0.5, 0.5, 0.5),
            (-0.3, 1.4, -2.1, 0.8),
            (2.5, 1.2, -0.4, -1.9),
            (0.123, -0.456, 0.789, 1.234),
            (PI / 2.0, PI / 3.0, PI / 4.0, PI / 5.0),
            (-PI / 2.0, -PI / 3.0, PI / 4.0, -PI / 5.0),
            (1.0, 2.0, 3.0, 4.0),
            (-1.0, -2.0, -3.0, -4.0),
            (0.05, 0.1, 0.15, 0.2),
            (PI, 0.0, 0.0, 0.0), // 순수 X 비슷
            (0.0, PI / 4.0, 0.0, 0.0),
            (0.7, 1.3, -0.6, 0.4),
            (1.111, 2.222, -3.333, 0.444),
            (0.6, -1.8, 2.4, -0.2),
        ];

        for (i, &(alpha, beta, gamma, delta)) in seeds.iter().enumerate() {
            // 입력 행렬을 e^(iα)·Rz(β)·Ry(γ)·Rz(δ) 로 합성.
            let su2 = rebuild_su2(beta, gamma, delta);
            let phase = Complex::from_polar(1.0, alpha);
            let u = [
                [phase * su2[0][0], phase * su2[0][1]],
                [phase * su2[1][0], phase * su2[1][1]],
            ];

            let zyz = decompose_unitary_zyz(&u);
            let rebuilt = rebuild_full(&zyz);
            assert!(
                matrix_close(&rebuilt, &u, 1e-12),
                "case {i}: rebuild mismatch (input α={alpha}, β={beta}, γ={gamma}, δ={delta})"
            );
        }
    }

    #[test]
    fn test_append_unitary_x_matches_x_gate() {
        // X 행렬을 append_unitary 로 추가하고 statevector 가 X|0⟩ = |1⟩ 인지 확인.
        let mut qc = Circuit::new(1);
        let x_matrix = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
        append_unitary(&mut qc, &x_matrix, 0);

        // global_phase 도 누적되었어야 X 의 정확한 행렬 (e^(iπ/2)·SU(2)) 가 됨.
        // 검증은 통합 테스트 (tests/circuit_test.rs) 에서 statevector 비교.
        assert_eq!(qc.instructions().len(), 3); // Rz, Ry, Rz
    }
}
