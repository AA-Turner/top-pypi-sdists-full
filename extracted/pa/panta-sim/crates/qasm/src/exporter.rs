//! [`Circuit`] → OpenQASM 2.0 / 3.0 문자열 변환 (export).
//!
//! 두 버전 모두 동일 게이트셋 + 거의 동일 syntax — 헤더 / 선언부만 다름.
//!
//! 부동소수 포맷: Rust `f64::to_string()` (= shortest round-trip representation).
//! `0.5_f64.to_string()` → `"0.5"`, `π.to_string()` → `"3.141592653589793"`. Qiskit 의
//! `qasm2.loads()` 가 그대로 reparse 가능 — qelib1.inc 에 없는 게이트
//! (iswap / dcx / ecr / ryy / rzx / xx_plus_yy / xx_minus_yy) 는 회로가 실제로
//! 사용할 때만 V2 헤더에 qelib1 스타일 `gate` 정의를 함께 emit 한다 (v1.4).
//!
//! v1.4: export 불가 케이스 (V2 target 의 block control flow, non-contiguous
//! cbit 조건) 는 panic 대신 [`QasmError::Export`] — fallible 진입점은
//! [`try_circuit_to_qasm`] 계열.  기존 [`circuit_to_qasm`] 계열은 하위 호환
//! wrapper 로 유지되며 Err 시 panic 한다 (python-binding 이 try 계열로 이전할
//! 때까지).
//!
//! [`Circuit`]: qsim_simulator::Circuit

use qsim_core::Gate;
use qsim_simulator::{Circuit, Instruction};

use crate::error::{QasmError, QasmResult};

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
/// export 불가 회로 (non-contiguous cbit 조건, V2 에 없는 block control flow)
/// 는 panic — fallible 처리가 필요하면 [`try_circuit_to_qasm2`] 사용.
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn circuit_to_qasm2(circuit: &Circuit) -> String {
    circuit_to_qasm(circuit, QasmDialect::V2)
}

/// [`Circuit`] 을 OpenQASM 3.0 문자열로 export 한다.
///
/// export 불가 회로는 panic — fallible 처리가 필요하면
/// [`try_circuit_to_qasm3`] 사용.
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn circuit_to_qasm3(circuit: &Circuit) -> String {
    circuit_to_qasm(circuit, QasmDialect::V3)
}

/// 버전 분기 없는 export 진입점 (하위 호환 wrapper).
///
/// [`try_circuit_to_qasm`] 의 panic 변형 — Err 를 그대로 panic 메시지로 올린다.
/// 새 코드는 [`try_circuit_to_qasm`] 사용 권장.
pub fn circuit_to_qasm(circuit: &Circuit, dialect: QasmDialect) -> String {
    match try_circuit_to_qasm(circuit, dialect) {
        Ok(s) => s,
        Err(e) => panic!("{e}"),
    }
}

/// [`Circuit`] 을 OpenQASM 2.0 문자열로 export 한다 (fallible, v1.4).
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn try_circuit_to_qasm2(circuit: &Circuit) -> QasmResult<String> {
    try_circuit_to_qasm(circuit, QasmDialect::V2)
}

/// [`Circuit`] 을 OpenQASM 3.0 문자열로 export 한다 (fallible, v1.4).
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn try_circuit_to_qasm3(circuit: &Circuit) -> QasmResult<String> {
    try_circuit_to_qasm(circuit, QasmDialect::V3)
}

/// 버전 분기 없는 fallible export 진입점 (v1.4).
///
/// export 불가 케이스는 [`QasmError::Export`]:
/// - V2 target 의 block control flow (`if/else` / `while` / `for` / `switch`)
///   — OpenQASM 2.0 에 표현이 없음.  `to_qasm("3.0")` 사용.
/// - control-flow 조건의 cbit_indices 가 `[0, 1, ..., k-1]` (contiguous from
///   zero) 가 아닌 경우 — OpenQASM 의 `if (c == N)` 은 creg 단위 비교만 표현
///   가능.
pub fn try_circuit_to_qasm(circuit: &Circuit, dialect: QasmDialect) -> QasmResult<String> {
    let mut out = String::new();
    write_header(&mut out, dialect);
    if matches!(dialect, QasmDialect::V2) {
        write_v2_ext_gate_defs(&mut out, circuit);
    }
    write_declarations(&mut out, circuit, dialect);
    write_global_phase(&mut out, circuit, dialect);
    write_body(&mut out, circuit, dialect)?;
    Ok(out)
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

// =====================================================================
// v1.4: qelib1.inc 에 없는 native 게이트의 V2 로컬 `gate` 정의.
// =====================================================================

/// qelib1.inc 에 없는 panta-sim native 게이트 (V2 export 시 정의 필요).
/// 배열 인덱스 = 의존성 순서 (ecr 은 rzx 를, xx_±yy 는 ryy 를 호출).
const EXT_RYY: usize = 0;
const EXT_RZX: usize = 1;
const EXT_ISWAP: usize = 2;
const EXT_DCX: usize = 3;
const EXT_ECR: usize = 4;
const EXT_XX_PLUS_YY: usize = 5;
const EXT_XX_MINUS_YY: usize = 6;
const N_EXT_GATES: usize = 7;

/// 각 extension 게이트의 qelib1 스타일 정의.  본문은 qelib1.inc 게이트
/// (h/s/x/cx/rx/rz/rxx) 만 사용 — Qiskit `qasm2.loads()` 가 그대로 reparse
/// 가능하고, panta 자체 parser 의 라운드트립 + statevector 검증으로 분해
/// 정확성을 보증한다 (exporter tests).
///
/// 분해 출처 (Qiskit standard gate `_define` 과 동일 컨벤션, targets[0] = LSB):
/// - ryy(θ) = (Rx(π/2)⊗Rx(π/2)) · CX · Rz(θ) · CX · (Rx(-π/2)⊗Rx(-π/2))
/// - rzx(θ) = H_b · CX · Rz(θ)_b · CX · H_b  (= exp(-iθ/2 Z⊗X))
/// - iswap = (S⊗S) · (H⊗I) · CX_ab · CX_ba · (I⊗H)
/// - dcx = CX_ab · CX_ba
/// - ecr = rzx(π/4) · X_a · rzx(-π/4)
/// - xx_plus_yy(θ) = rxx(θ/2) · ryy(θ/2)   (XX, YY 가환 → exp(-iθ/4(XX+YY)))
/// - xx_minus_yy(θ) = rxx(θ/2) · ryy(-θ/2) (exp(-iθ/4(XX−YY)))
const EXT_GATE_DEFS: [&str; N_EXT_GATES] = [
    "gate ryy(theta) a,b { rx(pi/2) a; rx(pi/2) b; cx a,b; rz(theta) b; cx a,b; rx(-pi/2) a; rx(-pi/2) b; }\n",
    "gate rzx(theta) a,b { h b; cx a,b; rz(theta) b; cx a,b; h b; }\n",
    "gate iswap a,b { s a; s b; h a; cx a,b; cx b,a; h b; }\n",
    "gate dcx a,b { cx a,b; cx b,a; }\n",
    "gate ecr a,b { rzx(pi/4) a,b; x a; rzx(-pi/4) a,b; }\n",
    "gate xx_plus_yy(theta) a,b { rxx(theta/2) a,b; ryy(theta/2) a,b; }\n",
    "gate xx_minus_yy(theta) a,b { rxx(theta/2) a,b; ryy(-theta/2) a,b; }\n",
];

/// 회로가 실제 사용하는 extension 게이트의 `gate` 정의를 V2 헤더에 emit.
/// 사용하지 않으면 아무것도 emit 하지 않는다 (의존성 정의 포함).
fn write_v2_ext_gate_defs(out: &mut String, circuit: &Circuit) {
    let mut used = [false; N_EXT_GATES];
    collect_ext_gates(circuit.instructions(), &mut used);
    // 의존성: ecr 본문이 rzx 를, xx_plus_yy / xx_minus_yy 본문이 ryy 를 호출.
    if used[EXT_ECR] {
        used[EXT_RZX] = true;
    }
    if used[EXT_XX_PLUS_YY] || used[EXT_XX_MINUS_YY] {
        used[EXT_RYY] = true;
    }
    for (i, def) in EXT_GATE_DEFS.iter().enumerate() {
        if used[i] {
            out.push_str(def);
        }
    }
}

/// instruction 시퀀스 (control-flow body 포함, 재귀) 에서 extension 게이트
/// 사용 여부를 수집.
fn collect_ext_gates(instructions: &[Instruction], used: &mut [bool; N_EXT_GATES]) {
    for inst in instructions {
        match inst {
            Instruction::ApplyGate { gate, .. } => match gate {
                Gate::Ryy(_) => used[EXT_RYY] = true,
                Gate::Rzx(_) => used[EXT_RZX] = true,
                Gate::ISwap => used[EXT_ISWAP] = true,
                Gate::Dcx => used[EXT_DCX] = true,
                Gate::Ecr => used[EXT_ECR] = true,
                Gate::XxPlusYy(_) => used[EXT_XX_PLUS_YY] = true,
                Gate::XxMinusYy(_) => used[EXT_XX_MINUS_YY] = true,
                _ => {}
            },
            Instruction::IfEq { body, .. } => {
                collect_ext_gates(std::slice::from_ref(body), used);
            }
            Instruction::IfElse {
                then_body,
                else_body,
                ..
            } => {
                collect_ext_gates(then_body, used);
                if let Some(eb) = else_body {
                    collect_ext_gates(eb, used);
                }
            }
            Instruction::WhileLoop { body, .. } | Instruction::ForLoop { body, .. } => {
                collect_ext_gates(body, used);
            }
            Instruction::Switch { cases, .. } => {
                for (_, body) in cases {
                    collect_ext_gates(body, used);
                }
            }
            _ => {}
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

fn write_body(out: &mut String, circuit: &Circuit, dialect: QasmDialect) -> QasmResult<()> {
    write_body_slice(out, circuit.instructions(), circuit.num_qubits(), dialect)
}

fn write_body_slice(
    out: &mut String,
    instructions: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) -> QasmResult<()> {
    for inst in instructions {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                write_gate_call(out, gate, targets, dialect);
            }
            Instruction::ApplyUnitary { targets, .. } => {
                // OpenQASM 2.0/3.0 표준에 임의 unitary 행렬 표기가 없으므로 주석으로
                // 보존 (round-trip 불가).  사용자에게 분해 후 export 를 권장.
                out.push_str(&format!(
                    "// panta-sim arbitrary unitary on q{targets:?} (omitted: no QASM representation)\n"
                ));
            }
            Instruction::ApplyNoise { channel, target } => {
                // OpenQASM 2.0/3.0 표준에 노이즈 채널 표기가 없으므로 주석으로 보존.
                // 다른 시뮬레이터는 이 라인을 무시; panta-sim 의 from_qasm 도 무시 (재구성하지 않음).
                out.push_str(&format!("// panta-sim noise: {channel:?} on q[{target}]\n"));
            }
            Instruction::ApplyNoise2 { channel, q0, q1 } => {
                out.push_str(&format!(
                    "// panta-sim noise2: {channel:?} on q[{q0}],q[{q1}]\n"
                ));
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
                write_if_eq(out, cbit_indices, *value, body, dialect)?;
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
                )?;
            }
            Instruction::WhileLoop {
                cbit_indices,
                value,
                body,
                max_iters: _,
            } => {
                write_while_loop(out, cbit_indices, *value, body, n_qubits, dialect)?;
            }
            Instruction::ForLoop { iterations, body } => {
                write_for_loop(out, *iterations, body, n_qubits, dialect)?;
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                write_switch(out, cbit_indices, cases, n_qubits, dialect)?;
            }
        }
    }
    Ok(())
}

/// `if (c == N) gate q[i];` (V2/V3 공통, body 는 단일 게이트만).
///
/// cbit_indices 가 `[0, 1, ..., k-1]` (contiguous from zero) 일 때만
/// `if (c == value) ...` 로 emit 가능 — 그 외엔 명시적 multi-bit 표현이
/// OpenQASM 2.0/3.0 의 creg 단위 비교에 없어 [`QasmError::Export`] (v1.4,
/// 이전에는 panic).  Python 의 `qc.measure(0, 1); qc.x(0).c_if(1, 1)` 처럼
/// 사용자 입력으로 도달 가능.
fn write_if_eq(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    body: &Instruction,
    dialect: QasmDialect,
) -> QasmResult<()> {
    require_contiguous(cbit_indices, "IfEq")?;
    // body 는 단일 ApplyGate (빌더/lowering invariant).
    let Instruction::ApplyGate { gate, targets } = body else {
        return Err(QasmError::Export {
            message: format!("IfEq body must be a single gate (got {body:?})"),
        });
    };
    out.push_str(&format!("if (c == {value}) "));
    // write_gate_call 이 마지막에 \n 을 push 하므로 그대로 사용 가능.
    // "if (c == 1) x q[0];\n" 형태가 됨.
    write_gate_call(out, gate, targets, dialect);
    Ok(())
}

/// V3 block-form `if (c == N) { ... } else { ... }` (v0.4.7).  V2 는 Export error.
#[allow(clippy::too_many_arguments)]
fn write_if_else(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    then_body: &[Instruction],
    else_body: Option<&[Instruction]>,
    n_qubits: usize,
    dialect: QasmDialect,
) -> QasmResult<()> {
    require_v3(dialect, "block-form if/else")?;
    require_contiguous(cbit_indices, "IfElse")?;
    out.push_str(&format!("if (c == {value}) {{\n"));
    write_body_slice(out, then_body, n_qubits, dialect)?;
    out.push_str("}\n");
    if let Some(eb) = else_body {
        out.push_str("else {\n");
        write_body_slice(out, eb, n_qubits, dialect)?;
        out.push_str("}\n");
    }
    Ok(())
}

/// V3 block-form `while (c == N) { ... }` (v0.4.7).
fn write_while_loop(
    out: &mut String,
    cbit_indices: &[usize],
    value: u64,
    body: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) -> QasmResult<()> {
    require_v3(dialect, "while loop")?;
    require_contiguous(cbit_indices, "WhileLoop")?;
    out.push_str(&format!("while (c == {value}) {{\n"));
    write_body_slice(out, body, n_qubits, dialect)?;
    out.push_str("}\n");
    Ok(())
}

/// V3 block-form `for i in [0:N-1] { ... }` (v0.4.7).
/// loop variable 은 panta-sim body 에서 미사용 — placeholder `_` 로 emit.
fn write_for_loop(
    out: &mut String,
    iterations: usize,
    body: &[Instruction],
    n_qubits: usize,
    dialect: QasmDialect,
) -> QasmResult<()> {
    require_v3(dialect, "for loop")?;
    if iterations == 0 {
        return Ok(());
    }
    out.push_str(&format!("for int _ in [0:{}] {{\n", iterations - 1));
    write_body_slice(out, body, n_qubits, dialect)?;
    out.push_str("}\n");
    Ok(())
}

/// V3 block-form `switch (c) { case N { ... } ... default { ... } }` (v0.4.7).
fn write_switch(
    out: &mut String,
    cbit_indices: &[usize],
    cases: &[(Option<u64>, Vec<Instruction>)],
    n_qubits: usize,
    dialect: QasmDialect,
) -> QasmResult<()> {
    require_v3(dialect, "switch")?;
    require_contiguous(cbit_indices, "Switch")?;
    out.push_str("switch (c) {\n");
    for (label, body) in cases {
        match label {
            Some(v) => out.push_str(&format!("case {v} {{\n")),
            None => out.push_str("default {\n"),
        }
        write_body_slice(out, body, n_qubits, dialect)?;
        out.push_str("}\n");
    }
    out.push_str("}\n");
    Ok(())
}

/// V3 전용 구조가 V2 target 으로 export 되면 [`QasmError::Export`] (v1.4,
/// 이전에는 panic).
fn require_v3(dialect: QasmDialect, feature: &str) -> QasmResult<()> {
    if matches!(dialect, QasmDialect::V2) {
        return Err(QasmError::Export {
            message: format!("OpenQASM 2.0 doesn't support {feature}; use to_qasm(\"3.0\")"),
        });
    }
    Ok(())
}

/// control-flow 조건의 cbit_indices 가 contiguous-from-zero 인지 검증 (v1.4,
/// 이전에는 panic).
fn require_contiguous(cbit_indices: &[usize], op: &str) -> QasmResult<()> {
    let contiguous_from_zero = cbit_indices.iter().enumerate().all(|(i, &c)| c == i);
    if !contiguous_from_zero {
        return Err(QasmError::Export {
            message: format!(
                "{op} condition on cbits {cbit_indices:?} cannot be expressed in OpenQASM — \
                 `if (c == N)` compares the whole creg, so the condition cbits must be \
                 [0, 1, ..., k-1] (contiguous from zero)"
            ),
        });
    }
    Ok(())
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
        Gate::ISwap => two(out, "iswap", targets),
        Gate::Rxx(theta) => two_param1(out, "rxx", *theta, targets),
        Gate::Ryy(theta) => two_param1(out, "ryy", *theta, targets),
        Gate::Rzz(theta) => two_param1(out, "rzz", *theta, targets),
        Gate::Dcx => two(out, "dcx", targets),
        Gate::Ecr => two(out, "ecr", targets),
        Gate::Rzx(theta) => two_param1(out, "rzx", *theta, targets),
        Gate::XxPlusYy(theta) => two_param1(out, "xx_plus_yy", *theta, targets),
        Gate::XxMinusYy(theta) => two_param1(out, "xx_minus_yy", *theta, targets),
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
    use num_complex::Complex;
    use qsim_simulator::ExecutionEngine;

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

    // =====================================================================
    // v1.4: panic → Err 전환 (try_circuit_to_qasm 계열).
    // =====================================================================

    #[test]
    fn test_non_contiguous_c_if_exports_as_error_not_panic() {
        // Python 재현 경로: qc.measure(0, 1); qc.x(0).c_if(1, 1); qc.to_qasm().
        // 조건 cbit 이 [1] (contiguous-from-zero 아님) → Export error.
        let mut c = Circuit::new(2);
        c.measure(0, 1);
        c.x(0);
        c.c_if_last(vec![1], 1);
        for dialect in [QasmDialect::V2, QasmDialect::V3] {
            let r = try_circuit_to_qasm(&c, dialect);
            match r {
                Err(QasmError::Export { message }) => {
                    assert!(message.contains("contiguous"), "{message}");
                }
                other => panic!("expected Export error, got {other:?}"),
            }
        }
    }

    #[test]
    fn test_v3_construct_with_v2_target_errors_cleanly() {
        // block-form for-loop 는 OpenQASM 2.0 에 표현 없음 → Export error.
        let mut c = Circuit::new(1);
        c.add_for_loop(
            3,
            vec![Instruction::ApplyGate {
                gate: Gate::X,
                targets: vec![0],
            }],
        );
        match try_circuit_to_qasm2(&c) {
            Err(QasmError::Export { message }) => {
                assert!(message.contains("3.0"), "{message}");
            }
            other => panic!("expected Export error, got {other:?}"),
        }
        // 같은 회로의 V3 export 는 성공해야.
        let v3 = try_circuit_to_qasm3(&c).unwrap();
        assert!(v3.contains("for int _ in [0:2]"));
    }

    #[test]
    fn test_v3_if_else_with_v2_target_errors_cleanly() {
        let mut c = Circuit::new(1);
        c.measure(0, 0);
        c.add_if_else(
            vec![0],
            1,
            vec![Instruction::ApplyGate {
                gate: Gate::X,
                targets: vec![0],
            }],
            None,
        );
        match try_circuit_to_qasm2(&c) {
            Err(QasmError::Export { message }) => {
                assert!(message.contains("3.0"), "{message}");
            }
            other => panic!("expected Export error, got {other:?}"),
        }
        assert!(try_circuit_to_qasm3(&c).is_ok());
    }

    // =====================================================================
    // v1.4: qelib1.inc 에 없는 게이트의 V2 로컬 `gate` 정의.
    // =====================================================================

    /// shots=0 statevector 실행.
    fn run_statevector(c: &Circuit) -> Vec<Complex<f64>> {
        ExecutionEngine::new()
            .run(c, 0)
            .statevector()
            .amplitudes()
            .to_vec()
    }

    fn assert_states_close(a: &[Complex<f64>], b: &[Complex<f64>], context: &str) {
        assert_eq!(a.len(), b.len(), "{context}: dim mismatch");
        for (i, (x, y)) in a.iter().zip(b.iter()).enumerate() {
            assert!(
                (x - y).norm() < 1e-9,
                "{context}: amplitude {i} differs: {x} vs {y}"
            );
        }
    }

    /// extension 게이트 1 개를 쓰는 회로를 V2 export 한 뒤:
    /// 1. emit 된 `gate` 정의가 존재하는지,
    /// 2. 자체 parser 라운드트립 statevector 가 native 와 일치하는지,
    /// 3. 게이트 이름들을 rename 해 native fast-path 를 우회 — emit 된 정의
    ///    본문이 실제로 inline 전개될 때도 statevector 가 일치하는지 (분해
    ///    정확성 검증) 를 확인한다.
    fn assert_ext_gate_def_round_trip(build: impl Fn(&mut Circuit), names: &[&str]) {
        let mut c = Circuit::new(2);
        // 비자명 (얽힘 + 복소 진폭) 입력 상태 준비.
        c.h(0);
        c.rx(0.3, 1);
        c.t(0);
        c.cx(0, 1);
        build(&mut c);
        let expected = run_statevector(&c);

        let qasm = try_circuit_to_qasm2(&c).unwrap();
        for name in names {
            assert!(
                qasm.contains(&format!("gate {name}")),
                "missing `gate {name}` definition in:\n{qasm}"
            );
        }
        // (2) 라운드트립 (native fast-path).
        let reparsed = crate::parse_qasm(&qasm).unwrap();
        assert_states_close(&run_statevector(&reparsed), &expected, "native round-trip");

        // (3) rename → 정의 본문 inline 전개 경로.
        let mut renamed = qasm.clone();
        for name in names {
            renamed = renamed.replace(name, &format!("{name}__udef"));
        }
        let reparsed2 = crate::parse_qasm(&renamed).unwrap();
        assert_states_close(
            &run_statevector(&reparsed2),
            &expected,
            "renamed-def round-trip",
        );
    }

    #[test]
    fn test_v2_iswap_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.iswap(0, 1), &["iswap"]);
    }

    #[test]
    fn test_v2_dcx_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.dcx(0, 1), &["dcx"]);
    }

    #[test]
    fn test_v2_ryy_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.ryy(0.7, 0, 1), &["ryy"]);
    }

    #[test]
    fn test_v2_rzx_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.rzx(0.7, 0, 1), &["rzx"]);
        // 비대칭 게이트 — qubit 순서 반전도 검증.
        assert_ext_gate_def_round_trip(|c| c.rzx(-1.1, 1, 0), &["rzx"]);
    }

    #[test]
    fn test_v2_ecr_def_round_trip() {
        // ecr 정의 본문이 rzx 를 호출 → 둘 다 rename 해 전체 체인 검증.
        assert_ext_gate_def_round_trip(|c| c.ecr(0, 1), &["ecr", "rzx"]);
        assert_ext_gate_def_round_trip(|c| c.ecr(1, 0), &["ecr", "rzx"]);
    }

    #[test]
    fn test_v2_xx_plus_yy_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.xx_plus_yy(0.9, 0, 1), &["xx_plus_yy", "ryy"]);
    }

    #[test]
    fn test_v2_xx_minus_yy_def_round_trip() {
        assert_ext_gate_def_round_trip(|c| c.xx_minus_yy(-0.4, 0, 1), &["xx_minus_yy", "ryy"]);
    }

    #[test]
    fn test_v2_ext_gate_defs_only_when_used() {
        // extension 게이트 미사용 회로 헤더에 `gate` 정의가 없어야.
        let s = circuit_to_qasm2(&make_bell());
        assert!(!s.contains("gate "), "unexpected gate defs in:\n{s}");
        // iswap 사용 시 iswap 정의만 (의존성 없는 게이트라 1 개).
        let mut c = Circuit::new(2);
        c.iswap(0, 1);
        let s = circuit_to_qasm2(&c);
        assert!(s.contains("gate iswap"));
        for name in ["ryy", "rzx", "dcx", "ecr", "xx_plus_yy", "xx_minus_yy"] {
            assert!(!s.contains(&format!("gate {name}")), "{s}");
        }
    }

    #[test]
    fn test_v2_ext_gate_defs_collected_from_control_flow_bodies() {
        // for-loop body 안에서만 쓰여도 정의가 emit 돼야 (V3 는 def 없이 그대로
        // 라 V2 전용 — 여기선 수집 로직만 확인).
        let mut c = Circuit::new(2);
        c.add_for_loop(
            2,
            vec![Instruction::ApplyGate {
                gate: Gate::ISwap,
                targets: vec![0, 1],
            }],
        );
        let mut used = [false; super::N_EXT_GATES];
        super::collect_ext_gates(c.instructions(), &mut used);
        assert!(used[super::EXT_ISWAP]);
    }
}
