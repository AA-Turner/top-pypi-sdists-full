use std::fmt;

/// QASM 파싱 / lowering 단계의 오류.
///
/// 모든 변형은 `line` / `column` (1-based) 정보를 포함해 사용자가 어떤 위치에서
/// 문제가 발생했는지 확인 가능. PyO3 경로에서는 `to_string()` 결과가
/// `ValueError` 메시지로 노출된다.
#[derive(Debug, Clone, PartialEq)]
pub enum QasmError {
    /// 토큰화 단계의 오류.
    Lex {
        line: usize,
        col: usize,
        message: String,
    },
    /// 문법 분석 오류 (예: `;` 누락, 잘못된 토큰).
    Parse {
        line: usize,
        col: usize,
        message: String,
    },
    /// AST → Circuit 변환 단계 오류.
    Lower { message: String },
    /// v0.3.0 범위 밖 기능 (classical control, dynamic 회로 등).
    UnsupportedFeature {
        message: String,
        planned_for: &'static str,
    },
    /// 정의되지 않은 게이트 호출.
    UnknownGate {
        line: usize,
        col: usize,
        name: String,
    },
    /// 잘못된 인자 개수.
    ArityMismatch {
        line: usize,
        col: usize,
        gate: String,
        expected: usize,
        got: usize,
    },
    /// 큐비트 인덱스 범위 벗어남.
    QubitOutOfRange { qubit: usize, n_qubits: usize },
    /// 클래식 비트 인덱스 범위 벗어남.
    CbitOutOfRange { cbit: usize, n_cbits: usize },
    /// user-defined gate 의 재귀 inline 깊이 초과.
    RecursionLimit { name: String, limit: usize },
    /// `if (c == N)` 의 `c` 가 정의된 creg 가 아님 (v0.4.5).
    IfCregUndefined {
        line: usize,
        col: usize,
        name: String,
    },
    /// `if (c == N)` 의 N 이 c 의 비트 폭으로 표현 불가 (v0.4.5).
    IfValueOutOfRange {
        line: usize,
        col: usize,
        value: i64,
        max: u64,
    },
    /// `if (c == N) ...` body 가 정확히 1 개의 ApplyGate 로 lowering 안 됨 (v0.4.5).
    /// (예: 빈 body / 여러 게이트 / measure / nested if / register-broadcast)
    IfBodyNotSingleGate {
        line: usize,
        col: usize,
        instructions: usize,
    },
    /// 같은 큐비트가 multi-qubit gate operands 안에서 중복 — 예: `cx q[0], q[0];`.
    /// release path 에서도 silent corruption 방지를 위해 거부 (v0.6.2).
    DuplicateQargs {
        line: usize,
        col: usize,
        gate: String,
        qubits: Vec<usize>,
    },
}

impl fmt::Display for QasmError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            QasmError::Lex { line, col, message } => {
                write!(f, "qasm lex error at line {line}:{col}: {message}")
            }
            QasmError::Parse { line, col, message } => {
                write!(f, "qasm parse error at line {line}:{col}: {message}")
            }
            QasmError::Lower { message } => write!(f, "qasm lower error: {message}"),
            QasmError::UnsupportedFeature {
                message,
                planned_for,
            } => write!(
                f,
                "qasm unsupported feature: {message} (planned for {planned_for})"
            ),
            QasmError::UnknownGate { line, col, name } => {
                write!(f, "qasm unknown gate '{name}' at line {line}:{col}")
            }
            QasmError::ArityMismatch {
                line,
                col,
                gate,
                expected,
                got,
            } => write!(
                f,
                "qasm gate '{gate}' at line {line}:{col} expected {expected} qubits, got {got}"
            ),
            QasmError::QubitOutOfRange { qubit, n_qubits } => write!(
                f,
                "qasm qubit index {qubit} out of range (n_qubits={n_qubits})"
            ),
            QasmError::CbitOutOfRange { cbit, n_cbits } => {
                write!(f, "qasm cbit index {cbit} out of range (n_cbits={n_cbits})")
            }
            QasmError::RecursionLimit { name, limit } => write!(
                f,
                "qasm gate '{name}' inline expansion exceeded recursion limit {limit}"
            ),
            QasmError::IfCregUndefined { line, col, name } => write!(
                f,
                "qasm 'if ({name} == ...)' at line {line}:{col}: classical register '{name}' is not defined"
            ),
            QasmError::IfValueOutOfRange { line, col, value, max } => write!(
                f,
                "qasm 'if (c == {value})' at line {line}:{col}: value out of range (creg max={max})"
            ),
            QasmError::IfBodyNotSingleGate { line, col, instructions } => write!(
                f,
                "qasm 'if (c == N) ...' at line {line}:{col}: body must lower to exactly one gate (got {instructions})"
            ),
            QasmError::DuplicateQargs { line, col, gate, qubits } => write!(
                f,
                "qasm gate '{gate}' at line {line}:{col}: duplicate qubit operand(s) {qubits:?} — multi-qubit gate operands must be distinct"
            ),
        }
    }
}

impl std::error::Error for QasmError {}

pub type QasmResult<T> = Result<T, QasmError>;
