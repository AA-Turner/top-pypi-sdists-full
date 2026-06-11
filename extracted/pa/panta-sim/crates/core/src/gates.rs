use num_complex::Complex;

use crate::complex::{complex, imag_unit, one, real, zero, Real};

/// 2×2 유니터리 행렬 (행 우선), 정밀도 `F`.
pub type Matrix2x2<F> = [[Complex<F>; 2]; 2];

/// 4×4 유니터리 행렬 (행 우선), 정밀도 `F`.
pub type Matrix4x4<F> = [[Complex<F>; 4]; 4];

/// 양자 게이트 정의.
///
/// 회전 각도는 항상 `f64` 로 저장한다. 행렬을 빌드할 때 trig (cos/sin) 도
/// `f64` 로 계산한 뒤 결과만 `F` 로 다운캐스트해야 깊은 회로의 phase 누적 오차를 방지할 수 있다.
#[derive(Debug, Clone)]
pub enum Gate {
    // 단일 큐비트 게이트
    H,
    X,
    Y,
    Z,
    S,
    Sdg,
    T,
    Tdg,
    /// √X (sqrt-X) — IBM Falcon/Eagle hardware-native single-qubit Clifford+T 게이트.
    /// 행렬: `(1/2) · [[1+i, 1-i], [1-i, 1+i]]`. `Sx² = X`, `Sx · Sxdg = I`.
    Sx,
    /// √X† — `Sx` 의 adjoint.  `Sxdg² = X`.
    /// 행렬: `(1/2) · [[1-i, 1+i], [1+i, 1-i]]`.
    Sxdg,
    Rx(f64),
    Ry(f64),
    Rz(f64),
    /// OpenQASM 2.0 `u1(λ)` 의 phase gate (= Qiskit `u1(λ)`).
    /// `p(λ)` (3.0) / `U(0, 0, λ)` 와 동치.  Diagonal 형태로 native 구현해
    /// `_ops` / `draw()` / `to_qasm()` 에서 이름이 보존된다.
    /// 행렬: `diag(1, e^(iλ))`.
    P(f64),
    /// OpenQASM 2.0 `u2(φ, λ)` (= Qiskit `u2(φ, λ)`).
    /// `U(π/2, φ, λ)` 와 동치.  Hadamard-like 자주 쓰여 native 보존.
    /// 행렬: `(1/√2) · [[1, -e^(iλ)], [e^(iφ), e^(i(φ+λ))]]`.
    U2(f64, f64),
    /// OpenQASM `U(θ,φ,λ)` 의 일반 1-큐비트 유니터리.
    /// Qiskit 의 `u3(θ,φ,λ)` / 3.0 의 `u(θ,φ,λ)` / `p(λ) = U(0,0,λ)` / `u1(λ) = U(0,0,λ)` 와 동일.
    /// 행렬: `[[cos(θ/2), -e^(iλ)sin(θ/2)], [e^(iφ)sin(θ/2), e^(i(φ+λ))cos(θ/2)]]`.
    /// 글로벌 phase 까지 정확히 Qiskit 정의 (statevector 1e-10 cross-check 용).
    U(f64, f64, f64),
    Id,
    // 2큐비트 게이트
    CNOT,
    CZ,
    /// Controlled-Y. CNOT 와 같은 컨트롤 패턴, target 에 Y 적용.
    /// 행렬 (computational basis |c t⟩): `block_diag(I, Y)` w.r.t. control 비트.
    CY,
    /// Controlled-H. Hadamard 의 controlled 변종.
    CH,
    /// Controlled-Rx(θ). 4×4 controlled rotation.
    CRx(f64),
    /// Controlled-Ry(θ).
    CRy(f64),
    /// Controlled-Rz(θ).
    CRz(f64),
    /// Controlled-Phase(λ).  `diag(1, 1, 1, e^(iλ))`.  Qiskit `cp(λ)` / `cu1(λ)` 와 동일.
    CP(f64),
    /// Controlled-U(θ,φ,λ). Qiskit `cu3(θ,φ,λ)`.  control=1 일 때 target 에 U(θ,φ,λ).
    CU3(f64, f64, f64),
    /// Controlled-U(θ,φ,λ,γ). Qiskit `cu(θ,φ,λ,γ)`.  control=1 일 때 target 에 U(θ,φ,λ)
    /// + control 비트 자체에 e^(iγ) phase (즉 |1c⟩ amplitude 에 e^(iγ) 곱).
    CU(f64, f64, f64, f64),
    SWAP,
    /// iSWAP — |01⟩↔|10⟩ 교환 + i phase.  초전도 큐비트 native.
    /// 행렬: `[[1,0,0,0],[0,0,i,0],[0,i,0,0],[0,0,0,1]]`.
    ISwap,
    /// `RXX(θ) = exp(-iθ/2 · X⊗X)`.  이온트랩 (Mølmer–Sørensen) native.
    Rxx(f64),
    /// `RYY(θ) = exp(-iθ/2 · Y⊗Y)`.
    Ryy(f64),
    /// `RZZ(θ) = exp(-iθ/2 · Z⊗Z)` = `diag(e^{-iθ/2}, e^{iθ/2}, e^{iθ/2}, e^{-iθ/2})`.
    /// QAOA / Ising 시뮬레이션의 기본 2-큐비트 회전.
    Rzz(f64),
    /// DCX — double-CNOT (`cx(a,b)·cx(b,a)`).  `[[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]]`.
    Dcx,
    /// ECR — echoed cross-resonance (IBM Eagle/Falcon native).
    /// `(1/√2)·[[0,1,0,i],[1,0,-i,0],[0,i,0,1],[-i,0,1,0]]`.
    Ecr,
    /// `RZX(θ) = exp(-iθ/2 · Z⊗X)`.  cross-resonance building block.
    Rzx(f64),
    /// `XXPlusYY(θ) = exp(-iθ/2 · (XX+YY)/2)` (β=0).  excitation-preserving
    /// (|01⟩↔|10⟩ 부분공간 회전) — 화학/HEA ansatz.
    XxPlusYy(f64),
    /// `XXMinusYY(θ) = exp(-iθ/2 · (XX−YY)/2)` (β=0).  |00⟩↔|11⟩ 부분공간 회전.
    XxMinusYy(f64),
    // 3큐비트 게이트
    Toffoli,
    Fredkin,
}

const FRAC_1_SQRT2: f64 = std::f64::consts::FRAC_1_SQRT_2;

impl Gate {
    /// 단일 큐비트 게이트의 2×2 유니터리 행렬을 정밀도 `F` 로 반환한다.
    ///
    /// trig 연산은 `f64` 에서 수행한 뒤 `F` 로 다운캐스트한다 (정밀도 보존).
    pub fn matrix_2x2<F: Real>(&self) -> Matrix2x2<F> {
        match self {
            Gate::H => {
                let s = real::<F>(FRAC_1_SQRT2);
                let neg_s = real::<F>(-FRAC_1_SQRT2);
                [[s, s], [s, neg_s]]
            }
            Gate::X => [[zero(), one()], [one(), zero()]],
            Gate::Y => {
                let neg_i: Complex<F> = -imag_unit::<F>();
                let i = imag_unit::<F>();
                [[zero(), neg_i], [i, zero()]]
            }
            Gate::Z => [[one(), zero()], [zero(), real::<F>(-1.0)]],
            Gate::S => [[one(), zero()], [zero(), imag_unit()]],
            Gate::Sdg => {
                let neg_i: Complex<F> = -imag_unit::<F>();
                [[one(), zero()], [zero(), neg_i]]
            }
            Gate::T => {
                // exp(iπ/4) = (1 + i)/√2
                let phase = complex::<F>(FRAC_1_SQRT2, FRAC_1_SQRT2);
                [[one(), zero()], [zero(), phase]]
            }
            Gate::Tdg => {
                // exp(-iπ/4) = (1 - i)/√2
                let phase = complex::<F>(FRAC_1_SQRT2, -FRAC_1_SQRT2);
                [[one(), zero()], [zero(), phase]]
            }
            Gate::Sx => {
                // √X = (1/2) · [[1+i, 1-i], [1-i, 1+i]]
                // Qiskit 정의 그대로 (글로벌 phase 까지 일치).
                let plus = complex::<F>(0.5, 0.5); // (1+i)/2
                let minus = complex::<F>(0.5, -0.5); // (1-i)/2
                [[plus, minus], [minus, plus]]
            }
            Gate::Sxdg => {
                // √X† = (1/2) · [[1-i, 1+i], [1+i, 1-i]]
                let minus = complex::<F>(0.5, -0.5);
                let plus = complex::<F>(0.5, 0.5);
                [[minus, plus], [plus, minus]]
            }
            Gate::P(lambda) => {
                // diag(1, e^(iλ))
                let phase = complex::<F>(lambda.cos(), lambda.sin());
                [[one(), zero()], [zero(), phase]]
            }
            Gate::U2(phi, lambda) => {
                // (1/√2) · [[1, -e^(iλ)], [e^(iφ), e^(i(φ+λ))]]
                let s = FRAC_1_SQRT2;
                let m00 = real::<F>(s);
                let m01 = complex::<F>(-s * lambda.cos(), -s * lambda.sin());
                let m10 = complex::<F>(s * phi.cos(), s * phi.sin());
                let phi_plus_lambda = phi + lambda;
                let m11 = complex::<F>(s * phi_plus_lambda.cos(), s * phi_plus_lambda.sin());
                [[m00, m01], [m10, m11]]
            }
            Gate::U(theta, phi, lambda) => {
                // Qiskit u3 정의: [[cos(θ/2),       -e^(iλ)·sin(θ/2)],
                //                  [e^(iφ)·sin(θ/2), e^(i(φ+λ))·cos(θ/2)]]
                // -e^(iλ)·sin = -(cos λ + i sin λ)·s = (-s cos λ) + i(-s sin λ)
                let c = (theta / 2.0).cos();
                let s = (theta / 2.0).sin();
                let phi_plus_lambda = phi + lambda;
                let m00 = real::<F>(c);
                let m01 = complex::<F>(-s * lambda.cos(), -s * lambda.sin());
                let m10 = complex::<F>(s * phi.cos(), s * phi.sin());
                let m11 = complex::<F>(c * phi_plus_lambda.cos(), c * phi_plus_lambda.sin());
                [[m00, m01], [m10, m11]]
            }
            Gate::Rx(theta) => {
                let c = (theta / 2.0).cos();
                let s = (theta / 2.0).sin();
                let cos_term = real::<F>(c);
                let neg_i_sin = complex::<F>(0.0, -s);
                [[cos_term, neg_i_sin], [neg_i_sin, cos_term]]
            }
            Gate::Ry(theta) => {
                let c = (theta / 2.0).cos();
                let s = (theta / 2.0).sin();
                let cos_term = real::<F>(c);
                let sin_term = real::<F>(s);
                let neg_sin = real::<F>(-s);
                [[cos_term, neg_sin], [sin_term, cos_term]]
            }
            Gate::Rz(theta) => {
                let neg_phase = complex::<F>((-theta / 2.0).cos(), (-theta / 2.0).sin());
                let pos_phase = complex::<F>((theta / 2.0).cos(), (theta / 2.0).sin());
                [[neg_phase, zero()], [zero(), pos_phase]]
            }
            Gate::Id => [[one(), zero()], [zero(), one()]],
            _ => panic!("matrix_2x2는 단일 큐비트 게이트에만 사용 가능"),
        }
    }

    /// CNOT 게이트의 4×4 유니터리 행렬을 반환한다.
    ///
    /// **주의 — 피연산자 순서 컨벤션**: 이 행렬은 control = 상위 비트(q1, MSB)
    /// 기준이다.  `Circuit::cx(control, target)` 는 `targets[0]` 이 control 인
    /// 반대 순서라, `apply_two_qubit_gate` 에 이 행렬을 그대로 쓰면 안 된다 —
    /// fusion.rs 가 CNOT 을 fusion 에서 제외하는 이유 (fusion.rs 참조).
    pub fn cnot_matrix<F: Real>() -> Matrix4x4<F> {
        [
            [one(), zero(), zero(), zero()],
            [zero(), one(), zero(), zero()],
            [zero(), zero(), zero(), one()],
            [zero(), zero(), one(), zero()],
        ]
    }

    /// CZ 게이트의 4×4 유니터리 행렬을 반환한다.
    pub fn cz_matrix<F: Real>() -> Matrix4x4<F> {
        let neg_one: Complex<F> = real::<F>(-1.0);
        [
            [one(), zero(), zero(), zero()],
            [zero(), one(), zero(), zero()],
            [zero(), zero(), one(), zero()],
            [zero(), zero(), zero(), neg_one],
        ]
    }

    /// SWAP 게이트의 4×4 유니터리 행렬을 반환한다.
    pub fn swap_matrix<F: Real>() -> Matrix4x4<F> {
        [
            [one(), zero(), zero(), zero()],
            [zero(), zero(), one(), zero()],
            [zero(), one(), zero(), zero()],
            [zero(), zero(), zero(), one()],
        ]
    }

    /// iSWAP 게이트의 4×4 유니터리 행렬.  `[[1,0,0,0],[0,0,i,0],[0,i,0,0],[0,0,0,1]]`.
    pub fn iswap_matrix<F: Real>() -> Matrix4x4<F> {
        let i = imag_unit::<F>();
        [
            [one(), zero(), zero(), zero()],
            [zero(), zero(), i, zero()],
            [zero(), i, zero(), zero()],
            [zero(), zero(), zero(), one()],
        ]
    }

    /// `RXX(θ) = cos(θ/2)·I - i·sin(θ/2)·X⊗X`.  대칭 게이트.
    pub fn rxx_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let c = real::<F>((theta / 2.0).cos());
        let nis = complex::<F>(0.0, -(theta / 2.0).sin());
        [
            [c, zero(), zero(), nis],
            [zero(), c, nis, zero()],
            [zero(), nis, c, zero()],
            [nis, zero(), zero(), c],
        ]
    }

    /// `RYY(θ) = cos(θ/2)·I - i·sin(θ/2)·Y⊗Y`.  대칭 게이트.
    pub fn ryy_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let c = real::<F>((theta / 2.0).cos());
        let is = complex::<F>(0.0, (theta / 2.0).sin());
        let nis = complex::<F>(0.0, -(theta / 2.0).sin());
        // Y⊗Y = [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]] → -i sin(θ/2)·(Y⊗Y).
        [
            [c, zero(), zero(), is],
            [zero(), c, nis, zero()],
            [zero(), nis, c, zero()],
            [is, zero(), zero(), c],
        ]
    }

    /// `RZZ(θ) = diag(e^{-iθ/2}, e^{iθ/2}, e^{iθ/2}, e^{-iθ/2})`.
    pub fn rzz_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let m = complex::<F>((theta / 2.0).cos(), -(theta / 2.0).sin()); // e^{-iθ/2}
        let p = complex::<F>((theta / 2.0).cos(), (theta / 2.0).sin()); // e^{+iθ/2}
        [
            [m, zero(), zero(), zero()],
            [zero(), p, zero(), zero()],
            [zero(), zero(), p, zero()],
            [zero(), zero(), zero(), m],
        ]
    }

    /// DCX 게이트의 4×4 행렬.  `[[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]]`.
    pub fn dcx_matrix<F: Real>() -> Matrix4x4<F> {
        [
            [one(), zero(), zero(), zero()],
            [zero(), zero(), zero(), one()],
            [zero(), one(), zero(), zero()],
            [zero(), zero(), one(), zero()],
        ]
    }

    /// ECR 게이트의 4×4 행렬 (echoed cross-resonance).
    pub fn ecr_matrix<F: Real>() -> Matrix4x4<F> {
        let s = real::<F>(FRAC_1_SQRT2);
        let is = complex::<F>(0.0, FRAC_1_SQRT2);
        let nis = complex::<F>(0.0, -FRAC_1_SQRT2);
        [
            [zero(), s, zero(), is],
            [s, zero(), nis, zero()],
            [zero(), is, zero(), s],
            [nis, zero(), s, zero()],
        ]
    }

    /// `RZX(θ) = exp(-iθ/2 Z⊗X)`.
    pub fn rzx_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let c = real::<F>((theta / 2.0).cos());
        let nis = complex::<F>(0.0, -(theta / 2.0).sin());
        let is = complex::<F>(0.0, (theta / 2.0).sin());
        [
            [c, zero(), nis, zero()],
            [zero(), c, zero(), is],
            [nis, zero(), c, zero()],
            [zero(), is, zero(), c],
        ]
    }

    /// `XXPlusYY(θ)` (β=0) — `|01⟩↔|10⟩` 부분공간 회전.
    pub fn xx_plus_yy_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let c = real::<F>((theta / 2.0).cos());
        let nis = complex::<F>(0.0, -(theta / 2.0).sin());
        [
            [one(), zero(), zero(), zero()],
            [zero(), c, nis, zero()],
            [zero(), nis, c, zero()],
            [zero(), zero(), zero(), one()],
        ]
    }

    /// `XXMinusYY(θ)` (β=0) — `|00⟩↔|11⟩` 부분공간 회전.
    pub fn xx_minus_yy_matrix<F: Real>(theta: f64) -> Matrix4x4<F> {
        let c = real::<F>((theta / 2.0).cos());
        let nis = complex::<F>(0.0, -(theta / 2.0).sin());
        [
            [c, zero(), zero(), nis],
            [zero(), one(), zero(), zero()],
            [zero(), zero(), one(), zero()],
            [nis, zero(), zero(), c],
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complex::{approx_eq, ONE, ZERO};

    #[test]
    fn test_hadamard_is_unitary_f64() {
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        // H * H = I
        for i in 0..2 {
            for j in 0..2 {
                let sum: Complex<f64> = (0..2).map(|k| h[i][k] * h[k][j]).sum();
                let expected = if i == j { ONE } else { ZERO };
                assert!(approx_eq(sum, expected, 1e-10));
            }
        }
    }

    #[test]
    fn test_hadamard_is_unitary_f32() {
        let h: Matrix2x2<f32> = Gate::H.matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                let sum: Complex<f32> = (0..2).map(|k| h[i][k] * h[k][j]).sum();
                let expected = if i == j {
                    Complex::new(1.0_f32, 0.0)
                } else {
                    Complex::new(0.0_f32, 0.0)
                };
                assert!(approx_eq(sum, expected, 1e-6_f32));
            }
        }
    }

    #[test]
    fn test_x_gate() {
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        assert_eq!(x[0][1], ONE);
        assert_eq!(x[1][0], ONE);
    }

    #[test]
    #[allow(clippy::needless_range_loop)]
    fn test_sdg_is_inverse_of_s() {
        let s: Matrix2x2<f64> = Gate::S.matrix_2x2();
        let sdg: Matrix2x2<f64> = Gate::Sdg.matrix_2x2();
        // S * Sdg = I
        for i in 0..2 {
            for j in 0..2 {
                let sum: Complex<f64> = (0..2).map(|k| s[i][k] * sdg[k][j]).sum();
                let expected = if i == j { ONE } else { ZERO };
                assert!(approx_eq(sum, expected, 1e-12));
            }
        }
    }

    #[test]
    #[allow(clippy::needless_range_loop)]
    fn test_tdg_is_inverse_of_t() {
        let t: Matrix2x2<f64> = Gate::T.matrix_2x2();
        let tdg: Matrix2x2<f64> = Gate::Tdg.matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                let sum: Complex<f64> = (0..2).map(|k| t[i][k] * tdg[k][j]).sum();
                let expected = if i == j { ONE } else { ZERO };
                assert!(approx_eq(sum, expected, 1e-12));
            }
        }
    }

    #[test]
    #[allow(clippy::needless_range_loop)]
    fn test_u_gate_special_cases() {
        // U(0, 0, 0) = I
        let u: Matrix2x2<f64> = Gate::U(0.0, 0.0, 0.0).matrix_2x2();
        assert!(approx_eq(u[0][0], ONE, 1e-12));
        assert!(approx_eq(u[1][1], ONE, 1e-12));
        assert!(approx_eq(u[0][1], ZERO, 1e-12));
        assert!(approx_eq(u[1][0], ZERO, 1e-12));

        // U(0, 0, π/2) = S = diag(1, i)
        let u_s: Matrix2x2<f64> = Gate::U(0.0, 0.0, std::f64::consts::FRAC_PI_2).matrix_2x2();
        let s: Matrix2x2<f64> = Gate::S.matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                assert!(approx_eq(u_s[i][j], s[i][j], 1e-12));
            }
        }

        // U(0, 0, π) = Z (up to identity in form)
        let u_z: Matrix2x2<f64> = Gate::U(0.0, 0.0, std::f64::consts::PI).matrix_2x2();
        let z: Matrix2x2<f64> = Gate::Z.matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                assert!(approx_eq(u_z[i][j], z[i][j], 1e-12));
            }
        }

        // U(π, 0, π) = X (Qiskit u3(π, 0, π) == X exactly, no global phase)
        let u_x: Matrix2x2<f64> =
            Gate::U(std::f64::consts::PI, 0.0, std::f64::consts::PI).matrix_2x2();
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                assert!(
                    approx_eq(u_x[i][j], x[i][j], 1e-12),
                    "U(π,0,π)[{i}][{j}]={:?} ≠ X[{i}][{j}]={:?}",
                    u_x[i][j],
                    x[i][j]
                );
            }
        }
    }

    #[test]
    #[allow(clippy::needless_range_loop)]
    fn test_u_gate_matches_qiskit_u3_formula() {
        // 임의 θ, φ, λ 에서 Qiskit u3 행렬 정의와 정확히 일치하는지.
        let theta = 1.234_f64;
        let phi = -0.5_f64;
        let lambda = 2.7_f64;
        let u: Matrix2x2<f64> = Gate::U(theta, phi, lambda).matrix_2x2();
        let c = (theta / 2.0).cos();
        let s = (theta / 2.0).sin();
        let expected = [
            [
                Complex::new(c, 0.0),
                Complex::new(-s * lambda.cos(), -s * lambda.sin()),
            ],
            [
                Complex::new(s * phi.cos(), s * phi.sin()),
                Complex::new(c * (phi + lambda).cos(), c * (phi + lambda).sin()),
            ],
        ];
        for i in 0..2 {
            for j in 0..2 {
                assert!(approx_eq(u[i][j], expected[i][j], 1e-15));
            }
        }
    }

    #[test]
    fn test_rz_matches_f64_and_f32() {
        // Rz(π/8) 의 trig 결과가 f64 → f32 cast 시 ~1e-7 이내인지 확인
        let theta = std::f64::consts::PI / 8.0;
        let m64: Matrix2x2<f64> = Gate::Rz(theta).matrix_2x2();
        let m32: Matrix2x2<f32> = Gate::Rz(theta).matrix_2x2();
        for i in 0..2 {
            for j in 0..2 {
                let r_diff = (m64[i][j].re as f32 - m32[i][j].re).abs();
                let i_diff = (m64[i][j].im as f32 - m32[i][j].im).abs();
                assert!(r_diff < 1e-6 && i_diff < 1e-6, "Rz f32 cast 정밀도 손실");
            }
        }
    }

    // ====================================================================
    // v0.4.6 신규 게이트 unitarity / invariant 검증
    // ====================================================================

    #[allow(clippy::needless_range_loop)]
    fn assert_unitary(name: &str, m: Matrix2x2<f64>, tol: f64) {
        // M · M† = I 확인.  M† 는 conjugate transpose.
        for i in 0..2 {
            for j in 0..2 {
                let mut s = ZERO;
                for k in 0..2 {
                    s += m[i][k] * m[j][k].conj();
                }
                let expected = if i == j { ONE } else { ZERO };
                assert!(
                    approx_eq(s, expected, tol),
                    "{name}: not unitary at ({i},{j}): {s:?} vs {expected:?}"
                );
            }
        }
    }

    fn matmul(a: Matrix2x2<f64>, b: Matrix2x2<f64>) -> Matrix2x2<f64> {
        let mut out = [[ZERO; 2]; 2];
        for i in 0..2 {
            for j in 0..2 {
                for k in 0..2 {
                    out[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        out
    }

    fn matrix_close(a: Matrix2x2<f64>, b: Matrix2x2<f64>, tol: f64) -> bool {
        for i in 0..2 {
            for j in 0..2 {
                if !approx_eq(a[i][j], b[i][j], tol) {
                    return false;
                }
            }
        }
        true
    }

    #[test]
    fn test_sx_unitarity_and_squares_to_x() {
        let sx: Matrix2x2<f64> = Gate::Sx.matrix_2x2();
        let sxdg: Matrix2x2<f64> = Gate::Sxdg.matrix_2x2();
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        assert_unitary("Sx", sx, 1e-15);
        assert_unitary("Sxdg", sxdg, 1e-15);
        // Sx · Sx = X (글로벌 phase 까지 정확).
        assert!(matrix_close(matmul(sx, sx), x, 1e-15), "Sx² ≠ X");
        // Sxdg · Sxdg = X.
        assert!(matrix_close(matmul(sxdg, sxdg), x, 1e-15), "Sxdg² ≠ X");
        // Sx · Sxdg = I.
        let id = [[ONE, ZERO], [ZERO, ONE]];
        assert!(matrix_close(matmul(sx, sxdg), id, 1e-15));
    }

    #[test]
    fn test_p_lambda_diagonal_and_unitary() {
        for lambda in [0.0, 0.7, std::f64::consts::PI, -1.234] {
            let p: Matrix2x2<f64> = Gate::P(lambda).matrix_2x2();
            assert_unitary("P", p, 1e-15);
            // Off-diagonal 0.
            assert!(approx_eq(p[0][1], ZERO, 1e-15));
            assert!(approx_eq(p[1][0], ZERO, 1e-15));
            // Diagonal: 1, e^iλ.
            assert!(approx_eq(p[0][0], ONE, 1e-15));
            assert!(approx_eq(
                p[1][1],
                Complex::new(lambda.cos(), lambda.sin()),
                1e-15
            ));
        }
    }

    #[test]
    fn test_p_special_cases_match_existing_gates() {
        // P(0) = I.
        let id = [[ONE, ZERO], [ZERO, ONE]];
        assert!(matrix_close(Gate::P(0.0).matrix_2x2(), id, 1e-15));
        // P(π) = Z.
        assert!(matrix_close(
            Gate::P(std::f64::consts::PI).matrix_2x2(),
            Gate::Z.matrix_2x2(),
            1e-15
        ));
        // P(π/2) = S.
        assert!(matrix_close(
            Gate::P(std::f64::consts::FRAC_PI_2).matrix_2x2(),
            Gate::S.matrix_2x2(),
            1e-15
        ));
        // P(π/4) = T.
        assert!(matrix_close(
            Gate::P(std::f64::consts::FRAC_PI_4).matrix_2x2(),
            Gate::T.matrix_2x2(),
            1e-15
        ));
    }

    #[test]
    fn test_u2_matches_u_special_case() {
        // U2(φ, λ) = U(π/2, φ, λ).
        for &(phi, lambda) in &[(0.0, 0.0), (0.5, -0.3), (1.7, 2.4)] {
            let u2: Matrix2x2<f64> = Gate::U2(phi, lambda).matrix_2x2();
            let u: Matrix2x2<f64> = Gate::U(std::f64::consts::FRAC_PI_2, phi, lambda).matrix_2x2();
            assert!(
                matrix_close(u2, u, 1e-15),
                "U2({phi},{lambda}) ≠ U(π/2,φ,λ)"
            );
            assert_unitary("U2", u2, 1e-14);
        }
    }
}
