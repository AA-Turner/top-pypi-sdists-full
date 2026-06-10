//! 회로 레벨 basis-gate 타깃 transpile 패스 (v0.8.3).
//!
//! 임의의 (named-gate) 회로를 **CX + 임의 1-큐비트 게이트** basis 로 변환한다.
//! 실제 하드웨어의 2-큐비트 native gate 는 대부분 CX (또는 CX-동치) 이므로,
//! 모든 2/3-큐비트 게이트를 CX + 1q 회전으로 풀어내는 것이 transpile 의 핵심
//! 단계다.  1-큐비트 게이트는 그대로 통과시키며 (target 1q basis 가 임의 1q),
//! 필요하면 이후 [`crate::decompose`] 의 ZYZ 패스로 추가 rebase 할 수 있다.
//!
//! 각 분해는 표준 항등식 (Nielsen–Chuang §4.3 controlled-U ABC 분해, 표준
//! 2-큐비트 회전 분해) 이며, 단위 테스트에서 statevector 엔진으로 원본 게이트와
//! **상대 위상까지 (global phase 제외) 1e-9 일치** 를 검증한다.
//!
//! cuStateVec / 임의 unitary (KAK) 분해가 필요한 일부 게이트 (CU/CU3/ECR/
//! XXPlusYY/XXMinusYY) 는 Python `unitary(M, q, decompose="cx")` (KAK 합성) 으로
//! 안내하는 에러를 반환한다.

use std::f64::consts::FRAC_PI_2;

use qsim_core::Gate;
use qsim_simulator::{Circuit, Instruction};

/// transpile 실패 (CX basis 로 직접 풀 수 없는 게이트).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TranspileError(pub String);

impl std::fmt::Display for TranspileError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "CX-basis transpile 실패: {}", self.0)
    }
}

impl std::error::Error for TranspileError {}

/// 회로를 **CX + 1-큐비트** basis 로 변환한 새 회로를 반환한다.
///
/// 1-큐비트 게이트와 비-게이트 명령 (measure / reset / 제어흐름 / noise) 은
/// 그대로 보존하고, 모든 2/3-큐비트 게이트를 CX + 1q 로 분해한다.  분해 불가
/// 게이트를 만나면 [`TranspileError`].
pub fn transpile_to_cx_basis(circuit: &Circuit) -> Result<Circuit, TranspileError> {
    let mut out = Circuit::new(circuit.num_qubits());
    out.set_global_phase(circuit.global_phase());
    for inst in circuit.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                lower_gate(&mut out, gate, targets)?;
            }
            // 비-게이트 / 동적 / 1q-에 안 닿는 명령은 그대로 보존.
            other => out.instructions_mut().push(other.clone()),
        }
    }
    Ok(out)
}

/// 단일 named gate 를 CX + 1q 로 분해해 `out` 에 emit 한다.
fn lower_gate(out: &mut Circuit, gate: &Gate, targets: &[usize]) -> Result<(), TranspileError> {
    let q0 = targets.first().copied().unwrap_or(0);
    let q1 = targets.get(1).copied().unwrap_or(0);
    match gate {
        // ---- 1-큐비트 게이트: 그대로 통과 ----
        Gate::H => out.h(q0),
        Gate::X => out.x(q0),
        Gate::Y => out.y(q0),
        Gate::Z => out.z(q0),
        Gate::S => out.s(q0),
        Gate::Sdg => out.sdg(q0),
        Gate::T => out.t(q0),
        Gate::Tdg => out.tdg(q0),
        Gate::Sx => out.sx(q0),
        Gate::Sxdg => out.sxdg(q0),
        Gate::Id => out.id(q0),
        Gate::Rx(t) => out.rx(*t, q0),
        Gate::Ry(t) => out.ry(*t, q0),
        Gate::Rz(t) => out.rz(*t, q0),
        Gate::P(l) => out.p(*l, q0),
        Gate::U2(phi, lam) => out.u2(*phi, *lam, q0),
        Gate::U(th, phi, lam) => out.u(*th, *phi, *lam, q0),

        // ---- 2-큐비트: 이미 CX ----
        Gate::CNOT => out.cx(q0, q1),

        // CZ = H_t · CX · H_t
        Gate::CZ => {
            out.h(q1);
            out.cx(q0, q1);
            out.h(q1);
        }
        // CY = Sdg_t · CX · S_t
        Gate::CY => {
            out.sdg(q1);
            out.cx(q0, q1);
            out.s(q1);
        }
        // SWAP = 3 CX
        Gate::SWAP => {
            out.cx(q0, q1);
            out.cx(q1, q0);
            out.cx(q0, q1);
        }
        // DCX = CX(a,b)·CX(b,a)
        Gate::Dcx => {
            out.cx(q0, q1);
            out.cx(q1, q0);
        }
        // iSWAP = S_a S_b H_a CX(a,b) CX(b,a) H_b
        Gate::ISwap => {
            out.s(q0);
            out.s(q1);
            out.h(q0);
            out.cx(q0, q1);
            out.cx(q1, q0);
            out.h(q1);
        }
        // CRz(θ): Rz(θ/2)_t CX Rz(-θ/2)_t CX
        Gate::CRz(t) => crz(out, *t, q0, q1),
        // CRx(θ) = H_t · CRz(θ) · H_t
        Gate::CRx(t) => {
            out.h(q1);
            crz(out, *t, q0, q1);
            out.h(q1);
        }
        // CRy(θ): Ry(θ/2)_t CX Ry(-θ/2)_t CX
        Gate::CRy(t) => {
            out.ry(*t / 2.0, q1);
            out.cx(q0, q1);
            out.ry(-*t / 2.0, q1);
            out.cx(q0, q1);
        }
        // CP(λ): p(λ/2)_c CX p(-λ/2)_t CX p(λ/2)_t
        Gate::CP(l) => {
            out.p(*l / 2.0, q0);
            out.cx(q0, q1);
            out.p(-*l / 2.0, q1);
            out.cx(q0, q1);
            out.p(*l / 2.0, q1);
        }
        // CH = Sdg_t H_t Tdg_t CX T_t H_t S_t  (Qiskit 표준)
        Gate::CH => {
            out.s(q1);
            out.h(q1);
            out.t(q1);
            out.cx(q0, q1);
            out.tdg(q1);
            out.h(q1);
            out.sdg(q1);
        }
        // RZZ(θ): CX Rz(θ)_b CX
        Gate::Rzz(t) => rzz(out, *t, q0, q1),
        // RXX(θ): H⊗H · RZZ · H⊗H
        Gate::Rxx(t) => {
            out.h(q0);
            out.h(q1);
            rzz(out, *t, q0, q1);
            out.h(q0);
            out.h(q1);
        }
        // RYY(θ): Rx(π/2)⊗Rx(π/2) · RZZ · Rx(-π/2)⊗Rx(-π/2)
        Gate::Ryy(t) => {
            out.rx(FRAC_PI_2, q0);
            out.rx(FRAC_PI_2, q1);
            rzz(out, *t, q0, q1);
            out.rx(-FRAC_PI_2, q0);
            out.rx(-FRAC_PI_2, q1);
        }
        // RZX(θ): H_b · RZZ · H_b
        Gate::Rzx(t) => {
            out.h(q1);
            rzz(out, *t, q0, q1);
            out.h(q1);
        }

        // ---- 3-큐비트 ----
        Gate::Toffoli => toffoli(out, targets[0], targets[1], targets[2]),
        Gate::Fredkin => {
            // Fredkin(c,a,b) = CX(b,a) · Toffoli(c,a,b) · CX(b,a)
            let (c, a, b) = (targets[0], targets[1], targets[2]);
            out.cx(b, a);
            toffoli(out, c, a, b);
            out.cx(b, a);
        }

        // ---- KAK / ABC 합성이 필요한 게이트: Python 합성으로 안내 ----
        other => {
            return Err(TranspileError(format!(
                "{other:?} 는 CX-basis 직접 분해가 미구현입니다. Python \
                 `circuit.unitary(gate.to_matrix(), qubits, decompose=\"cx\")` \
                 (KAK 합성) 을 사용하세요."
            )));
        }
    }
    Ok(())
}

#[inline]
fn crz(out: &mut Circuit, theta: f64, c: usize, t: usize) {
    out.rz(theta / 2.0, t);
    out.cx(c, t);
    out.rz(-theta / 2.0, t);
    out.cx(c, t);
}

#[inline]
fn rzz(out: &mut Circuit, theta: f64, a: usize, b: usize) {
    out.cx(a, b);
    out.rz(theta, b);
    out.cx(a, b);
}

/// Toffoli (CCX) 표준 6-CNOT 분해 (Nielsen–Chuang Fig 4.9).
fn toffoli(out: &mut Circuit, c1: usize, c2: usize, t: usize) {
    out.h(t);
    out.cx(c2, t);
    out.tdg(t);
    out.cx(c1, t);
    out.t(t);
    out.cx(c2, t);
    out.tdg(t);
    out.cx(c1, t);
    out.t(c2);
    out.t(t);
    out.h(t);
    out.cx(c1, c2);
    out.t(c1);
    out.tdg(c2);
    out.cx(c1, c2);
}

/// 회로가 CX + 1q basis 인지 검사한다 (모든 2/3-큐비트 게이트가 CX 인지).
pub fn is_cx_basis(circuit: &Circuit) -> bool {
    for inst in circuit.instructions() {
        if let Instruction::ApplyGate { gate, targets } = inst {
            if targets.len() >= 2 && !matches!(gate, Gate::CNOT) {
                return false;
            }
        }
    }
    true
}

/// 회로를 **IBM basis (`rz` + `sx` + `x` + CX)** 로 변환한 새 회로를 반환한다.
///
/// 두 단계: (1) [`transpile_to_cx_basis`] 로 모든 2/3q 게이트를 CX + 임의 1q 로
/// 풀고, (2) 모든 1-큐비트 게이트를 `{rz, sx, x}` 로 rebase 한다.  IBM Eagle/
/// Heron (`rz`/`sx`/`x`/`cx`(or `ecr`)) 등 실제 초전도 하드웨어의 표준 basis.
///
/// 1q rebase 는 ZYZ 분해 `U = e^{iα} Rz(β) Ry(γ) Rz(δ)` 후 항등식
/// `Ry(γ) = SX† Rz(γ) SX = X·SX·Rz(γ)·SX` (∵ `SX³ = SX†`, `X`·`SX` 가환) 로
/// `Ry` 를 제거한다 → `Rz(β)·X·SX·Rz(γ)·SX·Rz(δ)` (전역 위상 `α` 보존).  대각
/// (γ≈0) 게이트는 `Rz(β+δ)` 하나로 접는다.
pub fn transpile_to_ibm_basis(circuit: &Circuit) -> Result<Circuit, TranspileError> {
    let cx = transpile_to_cx_basis(circuit)?;
    Ok(rebase_1q_to_zsx(&cx))
}

/// 모든 1-큐비트 게이트를 `{rz, sx, x}` 로 rebase 한 새 회로 (2q+ / 비게이트
/// 명령은 그대로 보존).
fn rebase_1q_to_zsx(circuit: &Circuit) -> Circuit {
    let mut out = Circuit::new(circuit.num_qubits());
    out.set_global_phase(circuit.global_phase());
    for inst in circuit.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } if targets.len() == 1 => {
                rebase_1q_zsx(&mut out, &gate_matrix2(gate), targets[0]);
            }
            Instruction::ApplyUnitary { matrix, targets } if targets.len() == 1 => {
                let u = [[matrix[0], matrix[1]], [matrix[2], matrix[3]]];
                rebase_1q_zsx(&mut out, &u, targets[0]);
            }
            other => out.instructions_mut().push(other.clone()),
        }
    }
    out
}

/// 게이트의 2×2 행렬 (ZYZ 분해 입력용).
fn gate_matrix2(gate: &Gate) -> crate::decompose::Matrix2 {
    let m = gate.matrix_2x2::<f64>();
    [[m[0][0], m[0][1]], [m[1][0], m[1][1]]]
}

/// 1-큐비트 unitary `u` 를 `{rz, sx, x}` 로 분해해 `out` 의 qubit `q` 에 emit.
fn rebase_1q_zsx(out: &mut Circuit, u: &crate::decompose::Matrix2, q: usize) {
    let zyz = crate::decompose::decompose_unitary_zyz(u);
    out.add_global_phase(zyz.alpha);
    let push_rz = |out: &mut Circuit, ang: f64, q: usize| {
        if ang.abs() > 1e-12 {
            out.rz(ang, q);
        }
    };
    if zyz.gamma.abs() < 1e-12 {
        // Ry(0) = I → 대각, Rz(β+δ) 하나로 접는다.
        push_rz(out, zyz.beta + zyz.delta, q);
    } else {
        // Rz(β)·X·SX·Rz(γ)·SX·Rz(δ) — 적용 순서 (역순): δ, SX, γ, SX, X, β.
        push_rz(out, zyz.delta, q);
        out.sx(q);
        out.rz(zyz.gamma, q);
        out.sx(q);
        out.x(q);
        push_rz(out, zyz.beta, q);
    }
}

/// 회로가 IBM basis (`rz`/`sx`/`x`/`id` 1q + CX 2q) 인지 검사한다.
pub fn is_zsx_basis(circuit: &Circuit) -> bool {
    for inst in circuit.instructions() {
        if let Instruction::ApplyGate { gate, targets } = inst {
            let ok = match targets.len() {
                1 => matches!(gate, Gate::Rz(_) | Gate::Sx | Gate::X | Gate::Id),
                _ => matches!(gate, Gate::CNOT),
            };
            if !ok {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_complex::Complex;
    use qsim_simulator::{Backend, ExecutionEngine, SimulationResult};

    /// 회로를 statevector 로 실행해 amplitude 벡터를 얻는다.
    fn statevector(circ: &Circuit) -> Vec<Complex<f64>> {
        let engine = ExecutionEngine::new().with_backend(Backend::CpuStatevector);
        match engine.run(circ, 0) {
            SimulationResult::F64 { statevector, .. } => statevector.amplitudes().to_vec(),
            _ => panic!("expected F64 statevector"),
        }
    }

    /// 두 statevector 가 global phase 제외 1e-9 일치하는지.
    fn equiv_up_to_phase(a: &[Complex<f64>], b: &[Complex<f64>]) -> bool {
        assert_eq!(a.len(), b.len());
        // 첫 유의 amplitude 로 global phase 추정.
        let mut phase = Complex::new(1.0, 0.0);
        for (x, y) in a.iter().zip(b.iter()) {
            if x.norm() > 1e-6 {
                phase = y / x;
                break;
            }
        }
        a.iter()
            .zip(b.iter())
            .all(|(x, y)| (x * phase - y).norm() < 1e-9)
    }

    /// 주어진 게이트를 `n`-큐비트 회로의 지정 qubit 에 올리고, 비자명한 입력
    /// 상태 (앞단 게이트) 에서 원본 vs transpiled statevector 를 비교한다.
    fn check_gate(n: usize, build: impl Fn(&mut Circuit)) {
        let mut orig = Circuit::new(n);
        // 비자명 입력 상태 (상대 위상 오류 검출용).
        for q in 0..n {
            orig.h(q);
            orig.t(q);
        }
        build(&mut orig);
        let trans = transpile_to_cx_basis(&orig).expect("transpile");
        assert!(is_cx_basis(&trans), "결과가 CX basis 가 아님");
        assert!(
            equiv_up_to_phase(&statevector(&orig), &statevector(&trans)),
            "statevector 불일치"
        );
    }

    #[test]
    fn cz_cy_swap_dcx() {
        check_gate(2, |c| c.cz(0, 1));
        check_gate(2, |c| c.cy(0, 1));
        check_gate(2, |c| c.swap(0, 1));
        check_gate(2, |c| c.dcx(0, 1));
        check_gate(2, |c| c.iswap(0, 1));
    }

    #[test]
    fn controlled_rotations() {
        check_gate(2, |c| c.crz(0.7, 0, 1));
        check_gate(2, |c| c.crx(1.3, 0, 1));
        check_gate(2, |c| c.cry(-0.9, 0, 1));
        check_gate(2, |c| c.cp(2.1, 0, 1));
        check_gate(2, |c| c.ch(0, 1));
    }

    #[test]
    fn two_qubit_rotations() {
        check_gate(2, |c| c.rzz(0.55, 0, 1));
        check_gate(2, |c| c.rxx(1.1, 0, 1));
        check_gate(2, |c| c.ryy(-0.4, 0, 1));
        check_gate(2, |c| c.rzx(0.8, 0, 1));
    }

    #[test]
    fn three_qubit() {
        check_gate(3, |c| c.ccx(0, 1, 2));
        check_gate(3, |c| c.cswap(0, 1, 2));
    }

    #[test]
    fn full_circuit_mixed() {
        // 여러 게이트 섞인 회로 전체.
        check_gate(3, |c| {
            c.cz(0, 1);
            c.cry(0.5, 1, 2);
            c.rzz(0.3, 0, 2);
            c.swap(0, 2);
            c.ccx(0, 1, 2);
        });
    }

    #[test]
    fn unsupported_gate_errors() {
        let mut c = Circuit::new(2);
        c.ecr(0, 1);
        assert!(transpile_to_cx_basis(&c).is_err());
    }

    // ---- IBM basis (rz/sx/x + CX) ----

    /// 원본 게이트를 비자명 입력 상태에서 IBM basis transpile 과 비교한다.
    fn check_ibm(n: usize, build: impl Fn(&mut Circuit)) {
        let mut orig = Circuit::new(n);
        for q in 0..n {
            orig.h(q);
            orig.t(q);
        }
        build(&mut orig);
        let trans = transpile_to_ibm_basis(&orig).expect("ibm transpile");
        assert!(is_zsx_basis(&trans), "결과가 rz/sx/x + CX basis 가 아님");
        assert!(
            equiv_up_to_phase(&statevector(&orig), &statevector(&trans)),
            "statevector 불일치"
        );
    }

    #[test]
    fn ibm_single_qubit_gates() {
        // 모든 1q 게이트가 rz/sx/x 로 정확히 rebase 되는지.
        for g in [
            |c: &mut Circuit| c.h(0),
            |c: &mut Circuit| c.x(0),
            |c: &mut Circuit| c.y(0),
            |c: &mut Circuit| c.z(0),
            |c: &mut Circuit| c.s(0),
            |c: &mut Circuit| c.sdg(0),
            |c: &mut Circuit| c.t(0),
            |c: &mut Circuit| c.tdg(0),
            |c: &mut Circuit| c.sx(0),
            |c: &mut Circuit| c.sxdg(0),
            |c: &mut Circuit| c.rx(0.7, 0),
            |c: &mut Circuit| c.ry(-1.3, 0),
            |c: &mut Circuit| c.rz(2.1, 0),
        ] {
            check_ibm(1, g);
        }
    }

    #[test]
    fn ibm_two_and_three_qubit() {
        check_ibm(2, |c| c.cz(0, 1));
        check_ibm(2, |c| c.crx(0.9, 0, 1));
        check_ibm(2, |c| c.rxx(0.6, 0, 1));
        check_ibm(2, |c| c.iswap(0, 1));
        check_ibm(3, |c| c.ccx(0, 1, 2));
    }

    #[test]
    fn ibm_full_circuit_mixed() {
        check_ibm(3, |c| {
            c.h(0);
            c.cz(0, 1);
            c.ry(0.5, 2);
            c.cry(0.3, 1, 2);
            c.rzz(0.4, 0, 2);
            c.swap(0, 2);
            c.ccx(0, 1, 2);
            c.t(0);
        });
    }

    #[test]
    fn ibm_diagonal_folds_to_single_rz() {
        // Z (대각) → rz 하나 (sx/x 없음).
        let mut c = Circuit::new(1);
        c.z(0);
        let t = transpile_to_ibm_basis(&c).unwrap();
        let n_sx = t
            .instructions()
            .iter()
            .filter(|i| matches!(i, Instruction::ApplyGate { gate: Gate::Sx, .. }))
            .count();
        assert_eq!(n_sx, 0, "대각 게이트는 SX 를 emit 하면 안 됨");
        assert!(is_zsx_basis(&t));
    }
}
