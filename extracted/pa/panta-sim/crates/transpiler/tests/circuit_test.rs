//! Z-Y-Z 분해 + global_phase 가 simulator 의 statevector 수준에서 정확히
//! 입력 unitary 의 동작과 일치하는지 검증.

use num_complex::Complex;
use qsim_simulator::{Circuit, ExecutionEngine};
use qsim_transpiler::{append_unitary, Matrix2};

fn c(re: f64, im: f64) -> Complex<f64> {
    Complex::new(re, im)
}

/// 1큐비트 회로의 statevector |ψ⟩ 를 직접 얻는다 (shots=0, 측정 없음).
fn statevector(circuit: &Circuit) -> Vec<Complex<f64>> {
    let engine = ExecutionEngine::new();
    let result = engine.run(circuit, 0);
    result
        .statevector_f64()
        .expect("default precision is f64")
        .amplitudes()
        .to_vec()
}

/// `m·|0⟩` 를 직접 계산.
fn matrix_times_zero(m: &Matrix2) -> Vec<Complex<f64>> {
    vec![m[0][0], m[1][0]]
}

/// `m·|1⟩` 를 직접 계산.
fn matrix_times_one(m: &Matrix2) -> Vec<Complex<f64>> {
    vec![m[0][1], m[1][1]]
}

fn close_amplitudes(a: &[Complex<f64>], b: &[Complex<f64>], tol: f64) -> bool {
    a.len() == b.len() && a.iter().zip(b.iter()).all(|(x, y)| (x - y).norm() < tol)
}

#[test]
fn test_append_x_matches_x_gate_on_zero() {
    let mut qc = Circuit::new(1);
    let x = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
    append_unitary(&mut qc, &x, 0);

    let got = statevector(&qc);
    let expected = matrix_times_zero(&x); // [0, 1]
    assert!(
        close_amplitudes(&got, &expected, 1e-10),
        "got {got:?}, expected {expected:?}"
    );
}

#[test]
fn test_append_z_matches_z_gate_on_zero() {
    let mut qc = Circuit::new(1);
    let z = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(-1.0, 0.0)]];
    append_unitary(&mut qc, &z, 0);

    let got = statevector(&qc);
    let expected = matrix_times_zero(&z); // [1, 0]
    assert!(close_amplitudes(&got, &expected, 1e-10));
}

#[test]
fn test_append_z_matches_z_gate_on_one() {
    // |1⟩ 입력에서 Z 의 동작 확인 → -|1⟩.
    let mut qc = Circuit::new(1);
    qc.x(0); // |0⟩ → |1⟩
    let z = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(-1.0, 0.0)]];
    append_unitary(&mut qc, &z, 0);

    let got = statevector(&qc);
    // X|0⟩ = |1⟩, then Z|1⟩ = -|1⟩.  Note: X has det=-1 (global phase contribution).
    // 우리 native X 게이트는 글로벌 phase 를 추가하지 않으므로 Z·X|0⟩ = -|1⟩.
    let expected = matrix_times_one(&z); // [0, -1]
    assert!(
        close_amplitudes(&got, &expected, 1e-10),
        "got {got:?}, expected {expected:?}"
    );
}

#[test]
fn test_append_hadamard_matches_h_gate() {
    use std::f64::consts::FRAC_1_SQRT_2;
    let mut qc = Circuit::new(1);
    let s = FRAC_1_SQRT_2;
    let h = [[c(s, 0.0), c(s, 0.0)], [c(s, 0.0), c(-s, 0.0)]];
    append_unitary(&mut qc, &h, 0);

    let got = statevector(&qc);
    let expected = matrix_times_zero(&h);
    assert!(close_amplitudes(&got, &expected, 1e-10));
}

#[test]
fn test_append_random_su2_matches_matrix_times_zero() {
    use std::f64::consts::PI;
    // SU(2) (det=1) 6개. global_phase 가 0 인 케이스.
    let cases: &[(f64, f64, f64)] = &[
        (0.31, 0.5, 0.7),
        (1.7, 0.1, -0.5),
        (PI / 2.0, PI / 3.0, PI / 4.0),
        (-1.0, 1.5, 0.2),
        (0.0, PI, 0.0),
        (PI / 6.0, PI / 8.0, PI / 7.0),
    ];

    for (i, &(beta, gamma, delta)) in cases.iter().enumerate() {
        let cb = (gamma / 2.0).cos();
        let sb = (gamma / 2.0).sin();
        let half_plus = 0.5 * (beta + delta);
        let half_minus = 0.5 * (beta - delta);
        let m = [
            [
                Complex::from_polar(cb, -half_plus),
                Complex::from_polar(-sb, -half_minus),
            ],
            [
                Complex::from_polar(sb, half_minus),
                Complex::from_polar(cb, half_plus),
            ],
        ];

        let mut qc = Circuit::new(1);
        append_unitary(&mut qc, &m, 0);

        let got = statevector(&qc);
        let expected = matrix_times_zero(&m);
        assert!(
            close_amplitudes(&got, &expected, 1e-10),
            "case {i}: got {got:?}, expected {expected:?}"
        );
    }
}

#[test]
fn test_append_unitary_with_nonzero_global_phase() {
    // U = e^(iπ/3)·X. det(U) = e^(2iπ/3)·(-1).
    use std::f64::consts::PI;
    let phase = Complex::from_polar(1.0, PI / 3.0);
    let x = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
    let u = [
        [phase * x[0][0], phase * x[0][1]],
        [phase * x[1][0], phase * x[1][1]],
    ];

    let mut qc = Circuit::new(1);
    append_unitary(&mut qc, &u, 0);

    let got = statevector(&qc);
    let expected = matrix_times_zero(&u); // [0, e^(iπ/3)]
    assert!(
        close_amplitudes(&got, &expected, 1e-10),
        "got {got:?}, expected {expected:?}"
    );
}

#[test]
fn test_global_phase_preserved_for_two_qubit_circuit() {
    use std::f64::consts::PI;
    // 2큐비트 회로에 1큐비트 unitary 를 추가. global_phase 는 전체 statevector 에 적용.
    let mut qc = Circuit::new(2);
    qc.h(0);
    qc.cx(0, 1);
    // Bell 상태에 1큐비트 unitary (글로벌 phase 포함) 적용
    let phase = Complex::from_polar(1.0, PI / 4.0);
    let z = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(-1.0, 0.0)]];
    let u = [
        [phase * z[0][0], phase * z[0][1]],
        [phase * z[1][0], phase * z[1][1]],
    ];
    append_unitary(&mut qc, &u, 0);

    let got = statevector(&qc);
    // 정규화 유지 확인.
    let total_norm: f64 = got.iter().map(|a| a.norm_sqr()).sum();
    assert!((total_norm - 1.0).abs() < 1e-10);
    // global_phase 누적 확인 (정확한 값은 분해 알고리즘이 결정 — 0 이 아니어야 함).
    assert!(qc.global_phase().abs() > 1e-12);
}
