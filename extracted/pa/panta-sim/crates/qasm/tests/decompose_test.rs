//! qelib1/stdgates 게이트 분해의 unitary 정확성 검증.
//!
//! 각 분해를 시뮬레이터로 모든 basis 입력에 적용해 column-by-column statevector 를
//! 모은 뒤 (= 4×4 unitary), 해석적으로 계산한 expected matrix 와 1e-12 (f64) 일치
//! 하는지 확인한다.

#![allow(clippy::needless_range_loop)]

use num_complex::Complex;
use qsim_qasm::parse_qasm;
use qsim_simulator::{ExecutionEngine, Precision, SimulationResult};

type C = Complex<f64>;

fn c(re: f64, im: f64) -> C {
    Complex::new(re, im)
}

/// QASM 으로 표현된 2-큐비트 게이트의 4×4 행렬을 추출한다.
/// 각 basis state |j⟩ 를 X-게이트로 준비하고 회로를 적용해 결과 statevector 의 j 번째 column 으로 사용.
fn extract_2q_matrix(qasm_body: &str) -> [[C; 4]; 4] {
    let mut mat: [[C; 4]; 4] = [[c(0.0, 0.0); 4]; 4];
    for j in 0..4 {
        let mut prep = String::from("OPENQASM 2.0;\nqreg q[2];\n");
        if j & 1 != 0 {
            prep.push_str("x q[0];\n");
        }
        if j & 2 != 0 {
            prep.push_str("x q[1];\n");
        }
        prep.push_str(qasm_body);
        let circuit = parse_qasm(&prep).expect("parse");
        let engine = ExecutionEngine::new().with_precision(Precision::F64);
        let result = engine.run(&circuit, 0);
        let sv = match result {
            SimulationResult::F64 { statevector, .. } => statevector,
            _ => unreachable!(),
        };
        for i in 0..4 {
            mat[i][j] = sv.amplitudes()[i];
        }
    }
    mat
}

fn extract_1q_matrix(qasm_body: &str) -> [[C; 2]; 2] {
    let mut mat: [[C; 2]; 2] = [[c(0.0, 0.0); 2]; 2];
    for j in 0..2 {
        let mut prep = String::from("OPENQASM 2.0;\nqreg q[1];\n");
        if j == 1 {
            prep.push_str("x q[0];\n");
        }
        prep.push_str(qasm_body);
        let circuit = parse_qasm(&prep).expect("parse");
        let engine = ExecutionEngine::new().with_precision(Precision::F64);
        let result = engine.run(&circuit, 0);
        let sv = match result {
            SimulationResult::F64 { statevector, .. } => statevector,
            _ => unreachable!(),
        };
        for i in 0..2 {
            mat[i][j] = sv.amplitudes()[i];
        }
    }
    mat
}

fn assert_matrix_close_4(a: &[[C; 4]; 4], b: &[[C; 4]; 4], eps: f64) {
    for i in 0..4 {
        for j in 0..4 {
            let d = (a[i][j] - b[i][j]).norm();
            assert!(
                d < eps,
                "[{i}][{j}] mismatch: a={:?} b={:?} (|d|={d:e})",
                a[i][j],
                b[i][j]
            );
        }
    }
}

fn assert_matrix_close_2(a: &[[C; 2]; 2], b: &[[C; 2]; 2], eps: f64) {
    for i in 0..2 {
        for j in 0..2 {
            let d = (a[i][j] - b[i][j]).norm();
            assert!(d < eps, "[{i}][{j}] mismatch");
        }
    }
}

// ---------- 2.0 builtin: u1, u2, u3 ----------

#[test]
fn test_u1_matches_diag_phase() {
    let lambda = 1.234_f64;
    let m = extract_1q_matrix(&format!("u1({lambda}) q[0];\n"));
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(lambda.cos(), lambda.sin())],
    ];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_u2_matches_qiskit_def() {
    let phi = 0.4_f64;
    let lambda = -0.7_f64;
    let m = extract_1q_matrix(&format!("u2({phi}, {lambda}) q[0];\n"));
    let s = std::f64::consts::FRAC_1_SQRT_2;
    let expected = [
        [c(s, 0.0), c(-s * lambda.cos(), -s * lambda.sin())],
        [
            c(s * phi.cos(), s * phi.sin()),
            c(s * (phi + lambda).cos(), s * (phi + lambda).sin()),
        ],
    ];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_u3_matches_qiskit_def() {
    let theta = 0.7_f64;
    let phi = 1.1_f64;
    let lambda = -0.3_f64;
    let m = extract_1q_matrix(&format!("u3({theta}, {phi}, {lambda}) q[0];\n"));
    let cc = (theta / 2.0).cos();
    let ss = (theta / 2.0).sin();
    let expected = [
        [c(cc, 0.0), c(-ss * lambda.cos(), -ss * lambda.sin())],
        [
            c(ss * phi.cos(), ss * phi.sin()),
            c(cc * (phi + lambda).cos(), cc * (phi + lambda).sin()),
        ],
    ];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

// ---------- cy ----------

#[test]
fn test_cy_matches_qiskit() {
    // Qiskit cy q[0], q[1]: control q[0], target q[1]
    // cy = diag(1, ?, 1, ?) with Y action on target when control=1.
    // Little-endian basis |q1 q0⟩: |00⟩, |01⟩, |10⟩, |11⟩
    // c=q[0], t=q[1].
    // |00⟩: c=0 → unchanged
    // |01⟩: c=1, t=0 → apply Y to t: Y|0⟩=i|1⟩ → i|11⟩
    // |10⟩: c=0 → unchanged
    // |11⟩: c=1, t=1 → Y|1⟩=-i|0⟩ → -i|01⟩
    let m = extract_2q_matrix("cy q[0], q[1];\n");
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, -1.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(0.0, 1.0), c(0.0, 0.0), c(0.0, 0.0)],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

// ---------- ch ----------

#[test]
fn test_ch_matches_qiskit() {
    // ch q[0], q[1]: when c=1, apply H to t.
    // Basis |q1 q0⟩: |00⟩, |01⟩, |10⟩, |11⟩
    // c=q[0], t=q[1].
    // |00⟩: c=0, unchanged → |00⟩
    // |01⟩: c=1, t=0, apply H to t: H|0⟩ = (|0⟩+|1⟩)/√2 → (|01⟩+|11⟩)/√2
    // |10⟩: c=0, unchanged → |10⟩
    // |11⟩: c=1, t=1, apply H to t: H|1⟩ = (|0⟩-|1⟩)/√2 → (|01⟩-|11⟩)/√2
    let m = extract_2q_matrix("ch q[0], q[1];\n");
    let s = std::f64::consts::FRAC_1_SQRT_2;
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(s, 0.0), c(0.0, 0.0), c(s, 0.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(s, 0.0), c(0.0, 0.0), c(-s, 0.0)],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

// ---------- crz ----------

#[test]
fn test_crz_matches_qiskit() {
    let lambda = 0.7_f64;
    // crz = diag(1, e^(-iλ/2)·on |t=0,c=1⟩, 1, e^(iλ/2)·on |t=1,c=1⟩)
    // Wait actually: crz applies rz(λ) to t when c=1.
    // rz(λ) = diag(e^(-iλ/2), e^(iλ/2))
    // c=q[0], t=q[1]. Basis |q1 q0⟩.
    // |00⟩: unchanged
    // |01⟩: c=1, t=0. rz on t: phase e^(-iλ/2) on |t=0⟩ → e^(-iλ/2)|01⟩
    // |10⟩: unchanged
    // |11⟩: c=1, t=1. phase e^(iλ/2) → e^(iλ/2)|11⟩
    let m = extract_2q_matrix(&format!("crz({lambda}) q[0], q[1];\n"));
    let half = lambda / 2.0;
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [
            c(0.0, 0.0),
            c((-half).cos(), (-half).sin()),
            c(0.0, 0.0),
            c(0.0, 0.0),
        ],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(half.cos(), half.sin()),
        ],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

// ---------- cu1 / cp ----------

#[test]
fn test_cu1_matches_qiskit() {
    let lambda = 0.5_f64;
    // cu1 = diag(1, 1, 1, e^iλ) — phase only when both qubits are 1.
    let m = extract_2q_matrix(&format!("cu1({lambda}) q[0], q[1];\n"));
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(lambda.cos(), lambda.sin()),
        ],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

#[test]
fn test_cp_3p0_matches_cu1() {
    // 3.0 의 cp 는 2.0 의 cu1 와 동일.
    let lambda = 0.5_f64;
    let mut prep = String::from("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\n");
    prep.push_str(&format!("cp({lambda}) q[0], q[1];\n"));
    let mut mat: [[C; 4]; 4] = [[c(0.0, 0.0); 4]; 4];
    for j in 0..4 {
        let mut p = String::from("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\n");
        if j & 1 != 0 {
            p.push_str("x q[0];\n");
        }
        if j & 2 != 0 {
            p.push_str("x q[1];\n");
        }
        p.push_str(&format!("cp({lambda}) q[0], q[1];\n"));
        let circuit = parse_qasm(&p).unwrap();
        let engine = ExecutionEngine::new().with_precision(Precision::F64);
        let r = engine.run(&circuit, 0);
        let sv = match r {
            SimulationResult::F64 { statevector, .. } => statevector,
            _ => unreachable!(),
        };
        for i in 0..4 {
            mat[i][j] = sv.amplitudes()[i];
        }
    }
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(0.0, 0.0),
            c(lambda.cos(), lambda.sin()),
        ],
    ];
    assert_matrix_close_4(&mat, &expected, 1e-12);
}

// ---------- cu3 ----------

#[test]
fn test_cu3_matches_qiskit() {
    // controlled-u3: when c=1, apply U(θ,φ,λ) to t. Otherwise identity.
    let theta = 0.4_f64;
    let phi = 0.5_f64;
    let lambda = -0.3_f64;
    let m = extract_2q_matrix(&format!("cu3({theta}, {phi}, {lambda}) q[0], q[1];\n"));
    // Basis |q1 q0⟩:
    // |00⟩: unchanged
    // |01⟩ (c=1,t=0): apply U to t=|0⟩: result on t = U·|0⟩ = [U[0][0], U[1][0]]·|0..1⟩ = U00|0⟩+U10|1⟩
    //                 → in basis with c=1: U00·|01⟩ + U10·|11⟩
    // |10⟩: unchanged
    // |11⟩ (c=1,t=1): apply U to t=|1⟩ → U01|0⟩+U11|1⟩ → U01·|01⟩+U11·|11⟩
    let cc = (theta / 2.0).cos();
    let ss = (theta / 2.0).sin();
    let u00 = c(cc, 0.0);
    let u01 = c(-ss * lambda.cos(), -ss * lambda.sin());
    let u10 = c(ss * phi.cos(), ss * phi.sin());
    let u11 = c(cc * (phi + lambda).cos(), cc * (phi + lambda).sin());
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), u00, c(0.0, 0.0), u01],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), u10, c(0.0, 0.0), u11],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

// ---------- cry, crx ----------

#[test]
fn test_cry_matches_qiskit() {
    let lambda = 0.6_f64;
    let m = extract_2q_matrix(&format!("cry({lambda}) q[0], q[1];\n"));
    let cc = (lambda / 2.0).cos();
    let ss = (lambda / 2.0).sin();
    // Basis |q1 q0⟩, c=q[0], t=q[1]:
    // |00⟩ → |00⟩
    // |01⟩ (c=1,t=0): ry on t: cos·|0⟩ + sin·|1⟩ → cc·|01⟩ + ss·|11⟩
    // |10⟩ → |10⟩
    // |11⟩ (c=1,t=1): -sin·|0⟩ + cos·|1⟩ → -ss·|01⟩ + cc·|11⟩
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(cc, 0.0), c(0.0, 0.0), c(-ss, 0.0)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(ss, 0.0), c(0.0, 0.0), c(cc, 0.0)],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}

// ---------- v0.3.1: sx / sxdg / gphase (글로벌 phase 추적) ----------

/// `qubit[1] q;` 헤더 (3.0) 로 1큐비트 게이트 행렬을 추출. global_phase 도 적용됨.
fn extract_1q_matrix_v3(qasm_body: &str) -> [[C; 2]; 2] {
    let mut mat: [[C; 2]; 2] = [[c(0.0, 0.0); 2]; 2];
    for j in 0..2 {
        let mut prep = String::from("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[1] q;\n");
        if j == 1 {
            prep.push_str("x q[0];\n");
        }
        prep.push_str(qasm_body);
        let circuit = parse_qasm(&prep).expect("parse");
        let engine = ExecutionEngine::new().with_precision(Precision::F64);
        let result = engine.run(&circuit, 0);
        let sv = match result {
            SimulationResult::F64 { statevector, .. } => statevector,
            _ => unreachable!(),
        };
        for i in 0..2 {
            mat[i][j] = sv.amplitudes()[i];
        }
    }
    mat
}

#[test]
fn test_sx_matches_qiskit_def() {
    // Qiskit 정의: sx = (1/2)·[[1+i, 1−i], [1−i, 1+i]] = e^(iπ/4)·Rx(π/2)
    let m = extract_1q_matrix_v3("sx q[0];\n");
    let expected = [[c(0.5, 0.5), c(0.5, -0.5)], [c(0.5, -0.5), c(0.5, 0.5)]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_sxdg_matches_qiskit_def() {
    // sxdg = (sx)† = (1/2)·[[1−i, 1+i], [1+i, 1−i]]
    let m = extract_1q_matrix_v3("sxdg q[0];\n");
    let expected = [[c(0.5, -0.5), c(0.5, 0.5)], [c(0.5, 0.5), c(0.5, -0.5)]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_sx_then_sxdg_is_identity() {
    // sx 와 sxdg 의 phase 가 정확히 상쇄되어야 I 가 됨.
    let m = extract_1q_matrix_v3("sx q[0];\nsxdg q[0];\n");
    let expected = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_sx_squared_is_x() {
    // sx · sx = X (위상 포함).
    let m = extract_1q_matrix_v3("sx q[0];\nsx q[0];\n");
    let expected = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_gphase_only_is_phase_times_identity() {
    // gphase(λ) → e^(iλ)·I
    let lambda = 0.5_f64;
    let m = extract_1q_matrix_v3(&format!("gphase({lambda});\n"));
    let phase = Complex::from_polar(1.0, lambda);
    let expected = [[phase, c(0.0, 0.0)], [c(0.0, 0.0), phase]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_gphase_combined_with_x() {
    // X · gphase(π/3) = e^(iπ/3) · X
    let lambda = std::f64::consts::PI / 3.0;
    let m = extract_1q_matrix_v3(&format!("gphase({lambda});\nx q[0];\n"));
    let phase = Complex::from_polar(1.0, lambda);
    let expected = [[c(0.0, 0.0), phase], [phase, c(0.0, 0.0)]];
    assert_matrix_close_2(&m, &expected, 1e-12);
}

#[test]
fn test_crx_matches_qiskit() {
    let lambda = 0.4_f64;
    let m = extract_2q_matrix(&format!("crx({lambda}) q[0], q[1];\n"));
    let cc = (lambda / 2.0).cos();
    let ss = (lambda / 2.0).sin();
    // rx on t: [[cos, -i·sin], [-i·sin, cos]]
    // |00⟩ → |00⟩
    // |01⟩ (c=1,t=0): rx col 0 = (cos|0⟩, -i·sin|1⟩) → cc·|01⟩ + (-i·ss)·|11⟩
    // |10⟩ → |10⟩
    // |11⟩ (c=1,t=1): rx col 1 = (-i·sin|0⟩, cos|1⟩) → (-i·ss)·|01⟩ + cc·|11⟩
    let expected = [
        [c(1.0, 0.0), c(0.0, 0.0), c(0.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(cc, 0.0), c(0.0, 0.0), c(0.0, -ss)],
        [c(0.0, 0.0), c(0.0, 0.0), c(1.0, 0.0), c(0.0, 0.0)],
        [c(0.0, 0.0), c(0.0, -ss), c(0.0, 0.0), c(cc, 0.0)],
    ];
    assert_matrix_close_4(&m, &expected, 1e-12);
}
