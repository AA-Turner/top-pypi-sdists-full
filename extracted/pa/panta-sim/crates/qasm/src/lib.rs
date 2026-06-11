//! OpenQASM 2.0 / 3.0 파서 + lowering.
//!
//! 공개 진입점:
//! - [`parse_qasm`] — QASM 문자열 → simulator [`Circuit`].
//! - [`try_circuit_to_qasm`] (+ `try_circuit_to_qasm2/3`) — [`Circuit`] →
//!   QASM 문자열 (fallible, v1.4).  [`circuit_to_qasm`] 계열은 panic 하는
//!   하위 호환 wrapper.
//!
//! 지원 범위:
//! - OpenQASM 2.0 / 3.0 syntactic subset (헤더 자동 감지).
//! - qelib1.inc / stdgates.inc 표준 게이트 (CX/CY/CZ/CH/SWAP/CCX/CSWAP/U/u1-3/p/
//!   Rx/Ry/Rz/CRx/CRy/CRz/CU1/CU3/CP/CU/sx/sxdg/gphase 등 — v0.7.1 에서
//!   iswap/dcx/ecr/rxx/ryy/rzz/rzx/xx_plus_yy/xx_minus_yy 추가).
//! - user-defined `gate name(params) qubits { body }` (재귀 깊이 16 까지 inline).
//! - `barrier` (no-op), `measure q[i] -> c[j];`, `reset` (v0.4.5).
//! - classical control: `if (c == N) gate;` (v0.4.5) + block-form
//!   `if/else` / `while` / `for` (v1.4: `[low:step:high]` step 포함) /
//!   `switch` (v0.4.7).
//! - 3.0 `box` (v0.6.8), `def` 서브루틴 (v0.6.9~v1.3.2: classical / qubit /
//!   qubit[N] / bit / bit[N] 파라미터, body measure·reset·control-flow).
//!
//! 명시적 unsupported:
//! - `opaque` 선언.
//! - `def` 의 반환값 (`-> bit` 등).
//!
//! [`Circuit`]: qsim_simulator::Circuit

pub mod ast;
pub mod error;
pub mod exporter;
pub mod gates_lib;
pub mod lexer;
pub mod lowering;
pub mod parser;

pub use error::{QasmError, QasmResult};
pub use exporter::{
    circuit_to_qasm, circuit_to_qasm2, circuit_to_qasm3, try_circuit_to_qasm, try_circuit_to_qasm2,
    try_circuit_to_qasm3, QasmDialect,
};

/// QASM 소스를 파싱해 [`Circuit`] 으로 lowering 한다.
///
/// OpenQASM 2.0 (`OPENQASM 2.0;`) 와 3.0 (`OPENQASM 3.0;` / `OPENQASM 3;`) 모두
/// 자동으로 감지한다. 지원 범위 밖의 syntax 는 [`QasmError::UnsupportedFeature`] 로
/// 명확한 에러 + planned milestone 정보를 반환.
///
/// # 예
/// ```
/// use qsim_qasm::parse_qasm;
/// let qasm = r#"OPENQASM 2.0;
/// include "qelib1.inc";
/// qreg q[2];
/// h q[0];
/// cx q[0], q[1];"#;
/// let circuit = parse_qasm(qasm).unwrap();
/// assert_eq!(circuit.num_qubits(), 2);
/// ```
///
/// [`Circuit`]: qsim_simulator::Circuit
pub fn parse_qasm(source: &str) -> QasmResult<qsim_simulator::Circuit> {
    let tokens = lexer::Lexer::new(source).tokenize()?;
    let program = parser::Parser::new(tokens).parse_program()?;
    lowering::lower_program(program)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bell_end_to_end() {
        let circuit = parse_qasm(
            "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\nh q[0];\ncx q[0], q[1];",
        )
        .unwrap();
        assert_eq!(circuit.num_qubits(), 2);
        assert_eq!(circuit.instructions().len(), 2);
    }

    #[test]
    fn test_v3_end_to_end() {
        let circuit = parse_qasm(
            "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nh q[0];\ncx q[0], q[1];",
        )
        .unwrap();
        assert_eq!(circuit.num_qubits(), 2);
    }
}
