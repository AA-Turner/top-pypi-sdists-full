//! `qelib1.inc` (OpenQASM 2.0) + `stdgates.inc` (3.0) 표준 게이트셋 → panta-sim native
//! gate 분해 표.
//!
//! [`apply_named_gate`] 가 단일 진입점. 게이트 이름과 평가된 파라미터 / 큐비트
//! 인덱스를 받아 [`Circuit`] 에 native 명령을 추가한다.
//!
//! 모든 분해는 Qiskit 의 표준 정의와 unitary matrix level 에서 정확히 일치 (글로벌
//! phase 포함). 1e-10 statevector cross-check 가 이 분해 정확도에 의존한다.
//!
//! [`Circuit`]: qsim_simulator::Circuit

use qsim_simulator::Circuit;
use std::f64::consts::{FRAC_PI_2, FRAC_PI_4};

use crate::error::{QasmError, QasmResult};

/// 게이트 이름과 인자를 받아 [`Circuit`] 에 명령을 추가한다.
///
/// 이름이 qelib1 / stdgates 표준 게이트면 분해해서 native 명령을 추가하고 `Ok(true)`
/// 를 반환한다. 알려진 unsupported 게이트(`sx`/`sxdg`/`gphase` 등) 는 명확한
/// `UnsupportedFeature` 에러. 알 수 없는 이름은 `Ok(false)` (호출 측이 user-defined
/// gate 룩업으로 fallback).
pub fn apply_named_gate(
    circuit: &mut Circuit,
    name: &str,
    params: &[f64],
    qubits: &[usize],
    line: usize,
    col: usize,
) -> QasmResult<bool> {
    let arity_err = |gate: &str, expected: usize, got: usize| QasmError::ArityMismatch {
        line,
        col,
        gate: gate.into(),
        expected,
        got,
    };
    let param_err = |gate: &str, expected: usize, got: usize| QasmError::Lower {
        message: format!(
            "qasm gate '{gate}' at line {line}:{col} expected {expected} parameters, got {got}"
        ),
    };

    // v0.6.2: multi-qubit gate operands 가 distinct 한지 검사.  `cx q[0], q[0];`
    // 같은 입력은 core operations 의 controlled-update 가 silent 하게 잘못된
    // 결과를 만들어내는 path 라 명시 reject.  단일 qubit 게이트와 measure/barrier
    // 는 영향 없음.
    if qubits.len() >= 2 {
        for i in 0..qubits.len() {
            for j in (i + 1)..qubits.len() {
                if qubits[i] == qubits[j] {
                    return Err(QasmError::DuplicateQargs {
                        line,
                        col,
                        gate: name.to_string(),
                        qubits: qubits.to_vec(),
                    });
                }
            }
        }
    }

    // 단일 큐비트, 파라미터 없음
    let mono = |c: &mut Circuit, op: fn(&mut Circuit, usize), q: &[usize]| -> QasmResult<()> {
        if q.len() != 1 {
            return Err(arity_err(name, 1, q.len()));
        }
        op(c, q[0]);
        Ok(())
    };

    match name {
        // ---------- 1-큐비트, 파라미터 없음 ----------
        "id" => mono(circuit, Circuit::id, qubits)?,
        "x" => mono(circuit, Circuit::x, qubits)?,
        "y" => mono(circuit, Circuit::y, qubits)?,
        "z" => mono(circuit, Circuit::z, qubits)?,
        "h" => mono(circuit, Circuit::h, qubits)?,
        "s" => mono(circuit, Circuit::s, qubits)?,
        "sdg" => mono(circuit, Circuit::sdg, qubits)?,
        "t" => mono(circuit, Circuit::t, qubits)?,
        "tdg" => mono(circuit, Circuit::tdg, qubits)?,

        // ---------- 1-큐비트, 회전 ----------
        "rx" => {
            if params.len() != 1 {
                return Err(param_err("rx", 1, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("rx", 1, qubits.len()));
            }
            circuit.rx(params[0], qubits[0]);
        }
        "ry" => {
            if params.len() != 1 {
                return Err(param_err("ry", 1, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("ry", 1, qubits.len()));
            }
            circuit.ry(params[0], qubits[0]);
        }
        "rz" => {
            if params.len() != 1 {
                return Err(param_err("rz", 1, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("rz", 1, qubits.len()));
            }
            circuit.rz(params[0], qubits[0]);
        }

        // ---------- 1-큐비트, 일반 unitary (u1/u2/u3/u/p) ----------
        // u1(λ) = U(0, 0, λ) = diag(1, e^iλ). Qiskit u1 정확 일치.
        // p(λ) (3.0) = u1(λ).
        "u1" | "p" | "phase" => {
            if params.len() != 1 {
                return Err(param_err(name, 1, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err(name, 1, qubits.len()));
            }
            circuit.u(0.0, 0.0, params[0], qubits[0]);
        }
        // u2(φ,λ) = U(π/2, φ, λ).
        "u2" => {
            if params.len() != 2 {
                return Err(param_err("u2", 2, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("u2", 1, qubits.len()));
            }
            circuit.u(FRAC_PI_2, params[0], params[1], qubits[0]);
        }
        // u3(θ,φ,λ) = U(θ,φ,λ). u(θ,φ,λ) (3.0 stdgates) 동일.
        "u3" | "u" | "U" => {
            if params.len() != 3 {
                return Err(param_err(name, 3, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err(name, 1, qubits.len()));
            }
            circuit.u(params[0], params[1], params[2], qubits[0]);
        }

        // ---------- 2-큐비트 ----------
        // CX (OpenQASM 2.0 builtin) = cx
        "cx" | "CX" => {
            if !params.is_empty() {
                return Err(param_err("cx", 0, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cx", 2, qubits.len()));
            }
            circuit.cx(qubits[0], qubits[1]);
        }
        "cz" => {
            if !params.is_empty() {
                return Err(param_err("cz", 0, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cz", 2, qubits.len()));
            }
            circuit.cz(qubits[0], qubits[1]);
        }
        "swap" => {
            if !params.is_empty() {
                return Err(param_err("swap", 0, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("swap", 2, qubits.len()));
            }
            circuit.swap(qubits[0], qubits[1]);
        }
        // cy q,t = sdg t; cx q,t; s t  (Qiskit 표준)
        "cy" => {
            if !params.is_empty() {
                return Err(param_err("cy", 0, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cy", 2, qubits.len()));
            }
            let (c, t) = (qubits[0], qubits[1]);
            circuit.sdg(t);
            circuit.cx(c, t);
            circuit.s(t);
        }
        // ch q,t — Qiskit 표준 분해.
        // CH = (I⊗S)(I⊗H)(I⊗T)(CX)(I⊗Tdg)(I⊗H)(I⊗Sdg)
        "ch" => {
            if !params.is_empty() {
                return Err(param_err("ch", 0, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("ch", 2, qubits.len()));
            }
            let (c, t) = (qubits[0], qubits[1]);
            circuit.s(t);
            circuit.h(t);
            circuit.t(t);
            circuit.cx(c, t);
            circuit.tdg(t);
            circuit.h(t);
            circuit.sdg(t);
        }
        // crz(λ) q,t = rz(λ/2) t; cx q,t; rz(-λ/2) t; cx q,t  (Qiskit 표준)
        "crz" => {
            if params.len() != 1 {
                return Err(param_err("crz", 1, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("crz", 2, qubits.len()));
            }
            let lambda = params[0];
            let (c, t) = (qubits[0], qubits[1]);
            circuit.rz(lambda / 2.0, t);
            circuit.cx(c, t);
            circuit.rz(-lambda / 2.0, t);
            circuit.cx(c, t);
        }
        // crx(λ) q,t = h t; crz(λ) q,t; h t  (Qiskit 표준 — 단순화 가능)
        // 정확히 Qiskit 정의: crx(λ) c,t = u3(0,0,π/2) t; cx c,t; u3(-λ/2, 0, 0) t; cx c,t; u3(λ/2, -π/2, 0) t
        "crx" => {
            if params.len() != 1 {
                return Err(param_err("crx", 1, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("crx", 2, qubits.len()));
            }
            let lambda = params[0];
            let (c, t) = (qubits[0], qubits[1]);
            circuit.u(0.0, 0.0, FRAC_PI_2, t);
            circuit.cx(c, t);
            circuit.u(-lambda / 2.0, 0.0, 0.0, t);
            circuit.cx(c, t);
            circuit.u(lambda / 2.0, -FRAC_PI_2, 0.0, t);
        }
        // cry(λ) q,t = ry(λ/2) t; cx q,t; ry(-λ/2) t; cx q,t  (Qiskit 표준)
        "cry" => {
            if params.len() != 1 {
                return Err(param_err("cry", 1, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cry", 2, qubits.len()));
            }
            let lambda = params[0];
            let (c, t) = (qubits[0], qubits[1]);
            circuit.ry(lambda / 2.0, t);
            circuit.cx(c, t);
            circuit.ry(-lambda / 2.0, t);
            circuit.cx(c, t);
        }
        // cu1(λ) c,t = u1(λ/2) c; cx c,t; u1(-λ/2) t; cx c,t; u1(λ/2) t  (Qiskit 표준)
        // cp(λ) (3.0) = cu1(λ).
        "cu1" | "cp" => {
            if params.len() != 1 {
                return Err(param_err(name, 1, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err(name, 2, qubits.len()));
            }
            let lambda = params[0];
            let (c, t) = (qubits[0], qubits[1]);
            circuit.u(0.0, 0.0, lambda / 2.0, c);
            circuit.cx(c, t);
            circuit.u(0.0, 0.0, -lambda / 2.0, t);
            circuit.cx(c, t);
            circuit.u(0.0, 0.0, lambda / 2.0, t);
        }
        // cu3(θ,φ,λ) c,t — Qiskit 표준 분해.
        "cu3" => {
            if params.len() != 3 {
                return Err(param_err("cu3", 3, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cu3", 2, qubits.len()));
            }
            apply_cu3(
                circuit, params[0], params[1], params[2], qubits[0], qubits[1],
            );
        }
        // cu(θ,φ,λ,γ) c,t (3.0) — Qiskit 의 4-param controlled U + global phase γ on control.
        // γ는 control 에 phase(γ) 적용. cu3 와 다른 점: extra phase param.
        "cu" => {
            if params.len() != 4 {
                return Err(param_err("cu", 4, params.len()));
            }
            if qubits.len() != 2 {
                return Err(arity_err("cu", 2, qubits.len()));
            }
            let (theta, phi, lambda, gamma) = (params[0], params[1], params[2], params[3]);
            let (c, t) = (qubits[0], qubits[1]);
            // p(γ) on control = u1(γ) on c
            circuit.u(0.0, 0.0, gamma, c);
            apply_cu3(circuit, theta, phi, lambda, c, t);
        }

        // ---------- 3-큐비트 ----------
        "ccx" | "toffoli" => {
            if !params.is_empty() {
                return Err(param_err("ccx", 0, params.len()));
            }
            if qubits.len() != 3 {
                return Err(arity_err("ccx", 3, qubits.len()));
            }
            circuit.ccx(qubits[0], qubits[1], qubits[2]);
        }
        "cswap" | "fredkin" => {
            if !params.is_empty() {
                return Err(param_err("cswap", 0, params.len()));
            }
            if qubits.len() != 3 {
                return Err(arity_err("cswap", 3, qubits.len()));
            }
            circuit.cswap(qubits[0], qubits[1], qubits[2]);
        }

        // ---------- v0.3.1: global phase 추적이 필요한 게이트 ----------
        "sx" => {
            // Qiskit 정의: sx = e^(iπ/4) · Rx(π/2)
            // = (1/2)·[[1+i, 1−i], [1−i, 1+i]]
            if !params.is_empty() {
                return Err(param_err("sx", 0, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("sx", 1, qubits.len()));
            }
            circuit.rx(FRAC_PI_2, qubits[0]);
            circuit.add_global_phase(FRAC_PI_4);
        }
        "sxdg" => {
            // sxdg = e^(−iπ/4) · Rx(−π/2)
            if !params.is_empty() {
                return Err(param_err("sxdg", 0, params.len()));
            }
            if qubits.len() != 1 {
                return Err(arity_err("sxdg", 1, qubits.len()));
            }
            circuit.rx(-FRAC_PI_2, qubits[0]);
            circuit.add_global_phase(-FRAC_PI_4);
        }
        "gphase" => {
            // OpenQASM 3 의 gphase(λ) — 큐비트 인자가 없는 순수 글로벌 phase.
            // 본 함수는 broadcast 단위로 호출되므로 같은 회로에 여러 번 누적되지
            // 않도록 lowering 측이 broadcast=1 로 한 번만 호출해야 한다.
            if params.len() != 1 {
                return Err(param_err("gphase", 1, params.len()));
            }
            if !qubits.is_empty() {
                return Err(arity_err("gphase", 0, qubits.len()));
            }
            circuit.add_global_phase(params[0]);
        }
        "u0" => {
            // OpenQASM 2.0 의 u0(γ) — γ만큼 idle. 시뮬레이션상 no-op 으로 처리 가능.
            // 정확한 시간 모델 없으므로 그냥 id 적용.
            if qubits.len() != 1 {
                return Err(arity_err("u0", 1, qubits.len()));
            }
            circuit.id(qubits[0]);
        }

        // 알 수 없는 이름 → user-defined gate 룩업 fallback
        _ => return Ok(false),
    }
    Ok(true)
}

/// `cu3(θ,φ,λ)` Qiskit 표준 분해.
///
/// ```text
/// cu3(θ,φ,λ) c,t:
///     u1((λ+φ)/2) c
///     u1((λ-φ)/2) t
///     cx c,t
///     u3(-θ/2, 0, -(φ+λ)/2) t
///     cx c,t
///     u3(θ/2, φ, 0) t
/// ```
fn apply_cu3(circuit: &mut Circuit, theta: f64, phi: f64, lambda: f64, c: usize, t: usize) {
    circuit.u(0.0, 0.0, (lambda + phi) / 2.0, c);
    circuit.u(0.0, 0.0, (lambda - phi) / 2.0, t);
    circuit.cx(c, t);
    circuit.u(-theta / 2.0, 0.0, -(phi + lambda) / 2.0, t);
    circuit.cx(c, t);
    circuit.u(theta / 2.0, phi, 0.0, t);
}
