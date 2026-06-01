//! [`Circuit`] → OpenQASM 2.0 / 3.0 문자열 변환 (export).
//!
//! 두 버전 모두 동일 게이트셋 + 거의 동일 syntax — 헤더 / 선언부만 다름.
//!
//! 부동소수 포맷: Rust `f64::to_string()` (= shortest round-trip representation).
//! `0.5_f64.to_string()` → `"0.5"`, `π.to_string()` → `"3.141592653589793"`. Qiskit 의
//! `qasm2.loads()` 가 그대로 reparse 가능.
//!
//! [`Circuit`]: qsim_simulator::Circuit

use qsim_core::Gate;
use qsim_simulator::{Circuit, Instruction};

/// 출력할 QASM 버전.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum QasmDialect {
    /// `OPENQASM 2.0;` + `include "qelib1.inc";` + `qreg q[N];` / `creg c[N];`.
    V2,
    /// `OPENQASM 3.0;` + `include "stdgates.inc";` + `qubit[N] q;` / `bit[N] c;`.
    V3,
}

/// [`Circuit`] 을 OpenQASM 2.0 문자열로 export 한다.
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn circuit_to_qasm2(circuit: &Circuit) -> String {
    circuit_to_qasm(circuit, QasmDialect::V2)
}

/// [`Circuit`] 을 OpenQASM 3.0 문자열로 export 한다.
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn circuit_to_qasm3(circuit: &Circuit) -> String {
    circuit_to_qasm(circuit, QasmDialect::V3)
}

/// 버전 분기 없는 export 진입점.
pub fn circuit_to_qasm(circuit: &Circuit, dialect: QasmDialect) -> String {
    let mut out = String::new();
    write_header(&mut out, dialect);
    write_declarations(&mut out, circuit, dialect);
    write_global_phase(&mut out, circuit, dialect);
    write_body(&mut out, circuit, dialect);
    out
}

/// 글로벌 phase 를 emit 한다.
///
/// V3 에서는 `gphase(λ);` 로 정상 emit. V2 spec 에는 gphase 가 없으므로 주석으로만
/// 표기 (Qiskit `qasm2.dumps` 와 동일한 lossy 동작).
fn write_global_phase(out: &mut String, circuit: &Circuit, dialect: QasmDialect) {
    let lambda = circuit.global_phase();
    if lambda == 0.0 {
        return;
    }
    match dialect {
        QasmDialect::V2 => {
            out.push_str(&format!("// global_phase: {}\n", fmt_param(lambda)));
        }
        QasmDialect::V3 => {
            out.push_str(&format!("gphase({});\n", fmt_param(lambda)));
        }
    }
}

fn write_header(out: &mut String, dialect: QasmDialect) {
    match dialect {
        QasmDialect::V2 => {
            out.push_str("OPENQASM 2.0;\n");
            out.push_str("include \"qelib1.inc\";\n");
        }
        QasmDialect::V3 => {
            out.push_str("OPENQASM 3.0;\n");
            out.push_str("include \"stdgates.inc\";\n");
        }
    }
}

fn write_declarations(out: &mut String, circuit: &Circuit, dialect: QasmDialect) {
    let nq = circuit.num_qubits();
    let nc = circuit.num_cbits();
    match dialect {
        QasmDialect::V2 => {
            out.push_str(&format!("qreg q[{nq}];\n"));
            if nc > 0 {
                out.push_str(&format!("creg c[{nc}];\n"));
            }
        }
        QasmDialect::V3 => {
            out.push_str(&format!("qubit[{nq}] q;\n"));
            if nc > 0 {
                out.push_str(&format!("bit[{nc}] c;\n"));
            }
        }
    }
}

fn write_body(out: &mut String, circuit: &Circuit, dialect: QasmDialect) {
    write_body_slice(out, circuit.instructions(), circuit.num_qubits(), dialect);
}

fn write_body_slice(
    out: &mut String,
    instructions: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) {
    for inst in instructions {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                write_gate_call(out, gate, targets, dialect);
            }
            Instruction::ApplyNoise { channel, target } => {
                // OpenQASM 2.0/3.0 표준에 노이즈 채널 표기가 없으므로 주석으로 보존.
                // 다른 시뮬레이터는 이 라인을 무시; panta-sim 의 from_qasm 도 무시 (재구성하지 않음).
                out.push_str(&format!("// panta-sim noise: {channel:?} on q[{target}]\n"));
            }
            Instruction::Measure { qubit, cbit } => {
                write_measure(out, *qubit, *cbit, dialect);
            }
            Instruction::MeasureAll => {
                for i in 0..n_qubits {
                    write_measure(out, i, i, dialect);
                }
            }
            Instruction::Reset { qubit } => {
                out.push_str(&format!("reset q[{qubit}];\n"));
            }
            Instruction::IfEq {
                cbit_indices,
                value,
                body,
            } => {
                write_if_eq(out, cbit_indices, *value, body, dialect);
            }
            Instruction::IfElse {
                cbit_indices,
                value,
                then_body,
                else_body,
            } => {
                write_if_else(
                    out,
                    cbit_indices,
                    *value,
                    then_body,
                    else_body.as_deref(),
                    n_qubits,
                    dialect,
                );
            }
            Instruction::WhileLoop {
                cbit_indices,
                value,
                body,
                max_iters: _,
            } => {
                write_while_loop(out, cbit_indices, *value, body, n_qubits, dialect);
            }
            Instruction::ForLoop { iterations, body } => {
                write_for_loop(out, *iterations, body, n_qubits, dialect);
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                write_switch(out, cbit_indices, cases, n_qubits, dialect);
            }
        }
    }
}

/// `if (c == N) gate q[i];` (V2/V3 공통, body 는 단일 게이트만).
///
/// 현재 구현은 cbit_indices 가 (a) `[0, 1, ..., k-1]` contiguous from 0 일 때만
/// `if (c == value) ...` 로 emit. 그 외엔 명시적 multi-bit 표현이 OpenQASM 2.0
/// 에 없어 panic — panta-sim 자체 회로는 항상 contiguous 라 도달하지 않음.
fn write_if_eq(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    body: &Instruction,
    dialect: QasmDialect,
) {
    let contiguous_from_zero = cbit_indices.iter().enumerate().all(|(i, &c)| c == i);
    if !contiguous_from_zero {
        panic!(
            "QASM export: IfEq cbit_indices {cbit_indices:?} 가 contiguous-from-zero 가 아님 (V2/V3 표현 한계)"
        );
    }
    out.push_str(&format!("if (c == {value}) "));
    // body 는 단일 ApplyGate (빌더/lowering invariant).
    match body {
        Instruction::ApplyGate { gate, targets } => {
            // write_gate_call 이 마지막에 \n 을 push 하므로 그대로 사용 가능.
            // "if (c == 1) x q[0];\n" 형태가 됨.
            write_gate_call(out, gate, targets, dialect);
        }
        other => panic!("QASM export: IfEq.body 는 단일 ApplyGate 이어야 합니다 (got {other:?})"),
    }
}

/// V3 block-form `if (c == N) { ... } else { ... }` (v0.4.7).  V2 는 deferred.
fn write_if_else(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    then_body: &[Instruction],
    else_body: Option<&[Instruction]>,
    n_qubits: usize,
    dialect: QasmDialect,
) {
    require_v3(dialect, "block-form if/else");
    require_contiguous(cbit_indices, "IfElse");
    out.push_str(&format!("if (c == {value}) {{\n"));
    write_body_slice(out, then_body, n_qubits, dialect);
    out.push_str("}\n");
    if let Some(eb) = else_body {
        out.push_str("else {\n");
        write_body_slice(out, eb, n_qubits, dialect);
        out.push_str("}\n");
    }
}

/// V3 block-form `while (c == N) { ... }` (v0.4.7).
fn write_while_loop(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    body: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) {
    require_v3(dialect, "while loop");
    require_contiguous(cbit_indices, "WhileLoop");
    out.push_str(&format!("while (c == {value}) {{\n"));
    write_body_slice(out, body, n_qubits, dialect);
    out.push_str("}\n");
}

/// V3 block-form `for i in [0:N-1] { ... }` (v0.4.7).
/// loop variable 은 panta-sim body 에서 미사용 — placeholder `_` 로 emit.
fn write_for_loop(
    out: &mut String,
    iterations: usize,
    body: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) {
    require_v3(dialect, "for loop");
    if iterations == 0 {
        return;
    }
    out.push_str(&format!("for int _ in [0:{}] {{\n", iterations - 1));
    write_body_slice(out, body, n_qubits, dialect);
    out.push_str("}\n");
}

/// V3 block-form `switch (c) { case N { ... } ... default { ... } }` (v0.4.7).
fn write_switch(
    out: &mut String,
    cbit_indices: &[usize],
    cases: &[(Option<u64>, Vec<Instruction>)],
    n_qubits: usize,
    dialect: QasmDialect,
) {
    require_v3(dialect, "switch");
    require_contiguous(cbit_indices, "Switch");
    out.push_str("switch (c) {\n");
    for (label, body) in cases {
        match label {
            Some(v) => out.push_str(&format!("case {v} {{\n")),
            None => out.push_str("default {\n"),
        }
        write_body_slice(out, body, n_qubits, dialect);
        out.push_str("}\n");
    }
    out.push_str("}\n");
}

fn require_v3(dialect: QasmDialect, feature: &str) {
    if matches!(dialect, QasmDialect::V2) {
        panic!("QASM 2.0 doesn't support {feature}; use to_qasm(\"3.0\")");
    }
}

fn require_contiguous(cbit_indices: &[usize], op: &str) {
    let contiguous_from_zero = cbit_indices.iter().enumerate().all(|(i, &c)| c == i);
    if !contiguous_from_zero {
        panic!("QASM export: {op} cbit_indices {cbit_indices:?} not contiguous-from-zero");
    }
}

fn write_measure(out: &mut String, qubit: usize, cbit: usize, dialect: QasmDialect) {
    match dialect {
        // 2.0 canonical form
        QasmDialect::V2 => out.push_str(&format!("measure q[{qubit}] -> c[{cbit}];\n")),
        // 3.0 canonical assignment form (Qiskit qasm3.dumps 와 일치)
        QasmDialect::V3 => out.push_str(&format!("c[{cbit}] = measure q[{qubit}];\n")),
    }
}

fn write_gate_call(out: &mut String, gate: &Gate, targets: &[usize], dialect: QasmDialect) {
    match gate {
        Gate::H => mono(out, "h", targets),
        Gate::X => mono(out, "x", targets),
        Gate::Y => mono(out, "y", targets),
        Gate::Z => mono(out, "z", targets),
        Gate::S => mono(out, "s", targets),
        Gate::Sdg => mono(out, "sdg", targets),
        Gate::T => mono(out, "t", targets),
        Gate::Tdg => mono(out, "tdg", targets),
        Gate::Sx => mono(out, "sx", targets),
        Gate::Sxdg => mono(out, "sxdg", targets),
        Gate::Id => mono(out, "id", targets),
        Gate::Rx(theta) => param1(out, "rx", *theta, targets),
        Gate::Ry(theta) => param1(out, "ry", *theta, targets),
        Gate::Rz(theta) => param1(out, "rz", *theta, targets),
        Gate::P(lambda) => {
            // 2.0: u1(λ), 3.0: p(λ).  의미 동일 — qelib1 의 u1 = stdgates 의 p.
            let name = match dialect {
                QasmDialect::V2 => "u1",
                QasmDialect::V3 => "p",
            };
            param1(out, name, *lambda, targets);
        }
        Gate::U2(phi, lambda) => {
            // qelib1 / stdgates 모두 u2(φ,λ) 가 standard.
            param2(out, "u2", *phi, *lambda, targets);
        }
        Gate::U(theta, phi, lambda) => {
            // qelib1 의 u3 는 stdgates 의 u 와 동일 정의. 양 dialect 공통으로 u3 emit.
            out.push_str(&format!(
                "u3({},{},{}) q[{}];\n",
                fmt_param(*theta),
                fmt_param(*phi),
                fmt_param(*lambda),
                targets[0]
            ));
        }
        Gate::CNOT => two(out, "cx", targets),
        Gate::CZ => two(out, "cz", targets),
        Gate::CY => two(out, "cy", targets),
        Gate::CH => two(out, "ch", targets),
        Gate::CRx(theta) => two_param1(out, "crx", *theta, targets),
        Gate::CRy(theta) => two_param1(out, "cry", *theta, targets),
        Gate::CRz(theta) => two_param1(out, "crz", *theta, targets),
        Gate::CP(lambda) => {
            // 2.0: cu1(λ), 3.0: cp(λ).
            let name = match dialect {
                QasmDialect::V2 => "cu1",
                QasmDialect::V3 => "cp",
            };
            two_param1(out, name, *lambda, targets);
        }
        Gate::CU3(theta, phi, lambda) => {
            // qelib1 cu3 (2.0).  3.0 stdgates 에는 cu3 없고 cu(θ,φ,λ,γ=0) 으로 emit
            // 하는 것이 표준. 의미 동일.
            match dialect {
                QasmDialect::V2 => out.push_str(&format!(
                    "cu3({},{},{}) q[{}],q[{}];\n",
                    fmt_param(*theta),
                    fmt_param(*phi),
                    fmt_param(*lambda),
                    targets[0],
                    targets[1]
                )),
                QasmDialect::V3 => out.push_str(&format!(
                    "cu({},{},{},0) q[{}],q[{}];\n",
                    fmt_param(*theta),
                    fmt_param(*phi),
                    fmt_param(*lambda),
                    targets[0],
                    targets[1]
                )),
            }
        }
        Gate::CU(theta, phi, lambda, gamma) => {
            // 2.0/3.0 모두 cu(θ,φ,λ,γ).  qelib1 의 4-param cu = stdgates cu.
            out.push_str(&format!(
                "cu({},{},{},{}) q[{}],q[{}];\n",
                fmt_param(*theta),
                fmt_param(*phi),
                fmt_param(*lambda),
                fmt_param(*gamma),
                targets[0],
                targets[1]
            ));
        }
        Gate::SWAP => two(out, "swap", targets),
        Gate::Toffoli => three(out, "ccx", targets),
        Gate::Fredkin => three(out, "cswap", targets),
    }
}

fn mono(out: &mut String, name: &str, targets: &[usize]) {
    out.push_str(&format!("{name} q[{}];\n", targets[0]));
}

fn param1(out: &mut String, name: &str, theta: f64, targets: &[usize]) {
    out.push_str(&format!(
        "{name}({}) q[{}];\n",
        fmt_param(theta),
        targets[0]
    ));
}

fn param2(out: &mut String, name: &str, p0: f64, p1: f64, targets: &[usize]) {
    out.push_str(&format!(
        "{name}({},{}) q[{}];\n",
        fmt_param(p0),
        fmt_param(p1),
        targets[0]
    ));
}

fn two(out: &mut String, name: &str, targets: &[usize]) {
    out.push_str(&format!("{name} q[{}],q[{}];\n", targets[0], targets[1]));
}

fn two_param1(out: &mut String, name: &str, theta: f64, targets: &[usize]) {
    out.push_str(&format!(
        "{name}({}) q[{}],q[{}];\n",
        fmt_param(theta),
        targets[0],
        targets[1]
    ));
}

fn three(out: &mut String, name: &str, targets: &[usize]) {
    out.push_str(&format!(
        "{name} q[{}],q[{}],q[{}];\n",
        targets[0], targets[1], targets[2]
    ));
}

/// f64 의 shortest round-trip representation.
///
/// `f64::to_string()` 이 이미 그 contract: 같은 비트 패턴으로 다시 parse 됨.
/// 정수형 (`"1"`) 도 OpenQASM expression atom 으로 통하므로 추가 후처리 없음.
fn fmt_param(x: f64) -> String {
    x.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_bell() -> Circuit {
        let mut c = Circuit::new(2);
        c.h(0);
        c.cx(0, 1);
        c
    }

    #[test]
    fn test_v2_header_and_decl() {
        let c = Circuit::new(3);
        let s = circuit_to_qasm2(&c);
        assert!(s.starts_with("OPENQASM 2.0;\n"));
        assert!(s.contains("include \"qelib1.inc\";\n"));
        assert!(s.contains("qreg q[3];\n"));
        // creg 없는 회로는 emit 안 함
        assert!(!s.contains("creg"));
    }

    #[test]
    fn test_v3_header_and_decl() {
        let c = Circuit::new(2);
        let s = circuit_to_qasm3(&c);
        assert!(s.starts_with("OPENQASM 3.0;\n"));
        assert!(s.contains("include \"stdgates.inc\";\n"));
        assert!(s.contains("qubit[2] q;\n"));
    }

    #[test]
    fn test_bell_round_trips_through_parser() {
        let original = make_bell();
        let qasm = circuit_to_qasm2(&original);
        let reparsed = crate::parse_qasm(&qasm).unwrap();
        assert_eq!(reparsed.num_qubits(), original.num_qubits());
        assert_eq!(reparsed.instructions().len(), original.instructions().len());
    }

    #[test]
    fn test_measure_emits_creg_and_measure_stmt() {
        let mut c = Circuit::new(2);
        c.h(0);
        c.measure(0, 0);
        c.measure(1, 1);
        let s = circuit_to_qasm2(&c);
        assert!(s.contains("creg c[2];\n"));
        assert!(s.contains("measure q[0] -> c[0];\n"));
        assert!(s.contains("measure q[1] -> c[1];\n"));
    }

    #[test]
    fn test_measure_all_expands() {
        let mut c = Circuit::new(2);
        c.h(0);
        c.measure_all();
        let s = circuit_to_qasm2(&c);
        assert!(s.contains("measure q[0] -> c[0];\n"));
        assert!(s.contains("measure q[1] -> c[1];\n"));
    }

    #[test]
    fn test_all_native_gates_emit() {
        let mut c = Circuit::new(3);
        c.h(0);
        c.x(0);
        c.y(0);
        c.z(0);
        c.s(0);
        c.sdg(0);
        c.t(0);
        c.tdg(0);
        c.id(0);
        c.rx(0.5, 0);
        c.ry(0.6, 0);
        c.rz(0.7, 0);
        c.u(1.0, 2.0, 3.0, 0);
        c.cx(0, 1);
        c.cz(0, 1);
        c.swap(0, 1);
        c.ccx(0, 1, 2);
        c.cswap(0, 1, 2);
        let s = circuit_to_qasm2(&c);
        for keyword in [
            "h q[0];",
            "x q[0];",
            "y q[0];",
            "z q[0];",
            "s q[0];",
            "sdg q[0];",
            "t q[0];",
            "tdg q[0];",
            "id q[0];",
            "rx(0.5) q[0];",
            "ry(0.6) q[0];",
            "rz(0.7) q[0];",
            "u3(1,2,3) q[0];",
            "cx q[0],q[1];",
            "cz q[0],q[1];",
            "swap q[0],q[1];",
            "ccx q[0],q[1],q[2];",
            "cswap q[0],q[1],q[2];",
        ] {
            assert!(s.contains(keyword), "missing {keyword:?} in:\n{s}");
        }
    }

    #[test]
    fn test_round_trip_preserves_instruction_count() {
        // import-export-import 라운드 트립이 instruction 개수를 보존.
        let qasm_in = "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[3];\nh q[0];\nrx(0.5) q[1];\ncx q[0], q[1];\nccx q[0], q[1], q[2];\n";
        let c1 = crate::parse_qasm(qasm_in).unwrap();
        let qasm_out = circuit_to_qasm2(&c1);
        let c2 = crate::parse_qasm(&qasm_out).unwrap();
        assert_eq!(c1.instructions().len(), c2.instructions().len());
    }

    #[test]
    fn test_export_v3_round_trips() {
        let c = make_bell();
        let qasm = circuit_to_qasm3(&c);
        let reparsed = crate::parse_qasm(&qasm).unwrap();
        assert_eq!(reparsed.num_qubits(), c.num_qubits());
    }
}
