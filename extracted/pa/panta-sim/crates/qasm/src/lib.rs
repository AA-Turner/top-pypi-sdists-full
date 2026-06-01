//! OpenQASM 2.0 / 3.0 파서 + lowering.
//!
//! 공개 진입점:
//! - [`parse_qasm`] — QASM 문자열 → simulator [`Circuit`].
//!
//! 지원 범위 (v0.3.0 Cut 1):
//! - OpenQASM 2.0 / 3.0 syntactic subset (헤더 자동 감지).
//! - qelib1.inc / stdgates.inc 표준 게이트 (CX/CY/CZ/CH/SWAP/CCX/CSWAP/U/u1-3/p/Rx/Ry/Rz/CRx/CRy/CRz/CU1/CU3/CP/CU 등).
//! - user-defined `gate name(params) qubits { body }` (재귀 깊이 16 까지 inline).
//! - `barrier` (no-op).
//! - `measure q[i] -> c[j];`.
//!
//! 명시적 unsupported (v0.5+ 로 deferred):
//! - `if (c == N) ...;` classical control.
//! - `reset`, `opaque`.
//! - `sx`/`sxdg`/`gphase` (글로벌 phase tracking 필요 — v0.3.1).
//! - 3.0 `for`/`while`/`box`/`def` 등 동적 회로.
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
pub use exporter::{circuit_to_qasm, circuit_to_qasm2, circuit_to_qasm3, QasmDialect};

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
