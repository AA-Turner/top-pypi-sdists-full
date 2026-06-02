//! OpenQASM 2.0 / 3.0 AST.
//!
//! 파서 산출물. lowering 단계가 이 AST 를 simulator [`Circuit`] 로 변환한다.
//!
//! [`Circuit`]: qsim_simulator::Circuit

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum QasmVersion {
    V2,
    V3,
}

#[derive(Debug, Clone)]
pub struct Program {
    pub version: QasmVersion,
    pub stmts: Vec<Stmt>,
}

#[derive(Debug, Clone)]
pub enum Stmt {
    /// `include "qelib1.inc";` — 파일 이름만 보존 (qelib1/stdgates 외에는 lowering 에서 error).
    Include {
        file: String,
        line: usize,
        col: usize,
    },
    /// `qreg q[N];` (2.0) 또는 `qubit[N] q;` / `qubit q;` (3.0).
    QregDecl { name: String, size: usize },
    /// `creg c[N];` (2.0) 또는 `bit[N] c;` / `bit c;` (3.0).
    CregDecl { name: String, size: usize },
    /// `gate name(params) qubits { body }` user-defined gate 정의.
    GateDecl(GateDecl),
    /// `opaque ...;` — lowering 단계에서 unsupported error.
    OpaqueDecl {
        name: String,
        line: usize,
        col: usize,
    },
    /// 게이트 호출 (`h q[0];`, `cx q[0], q[1];`, `u3(0.1, 0.2, 0.3) q[0];`).
    GateCall(GateCall),
    /// `barrier q[i], ...;` 또는 `barrier q;` — no-op (lowering 에서 무시).
    Barrier { qargs: Vec<QArg> },
    /// `measure q[i] -> c[j];`.
    Measure {
        qubit: QArg,
        cbit: CArg,
        line: usize,
        col: usize,
    },
    /// `reset q[i];` — UnsupportedFeature (mid-circuit).
    Reset { qarg: QArg, line: usize, col: usize },
    /// `if (c == N) gate_call;` — single-statement body, v0.4.5 lowering.
    If {
        creg: String,
        value: i64,
        body: Box<Stmt>,
        line: usize,
        col: usize,
    },
    /// `if (c == N) { stmts } else { stmts }` — block-form, v0.4.7 추가.
    /// then_body / else_body 는 임의 길이의 sub-statement 리스트.
    IfElse {
        creg: String,
        value: i64,
        then_body: Vec<Stmt>,
        else_body: Option<Vec<Stmt>>,
        line: usize,
        col: usize,
    },
    /// `while (c == N) { stmts }` — v0.4.7.
    WhileLoop {
        creg: String,
        value: i64,
        body: Vec<Stmt>,
        line: usize,
        col: usize,
    },
    /// `for type var in [low:high] { stmts }` — v0.4.7.
    /// loop variable 은 panta-sim 에서 사용 불가 — body 안에서 i 가 게이트 인자
    /// 로 쓰이는 회로는 from_qiskit 에서 unroll 후 들어와야 함.
    ForLoop {
        var: String,
        low: i64,
        high: i64,
        body: Vec<Stmt>,
        line: usize,
        col: usize,
    },
    /// `switch (c) { case N { stmts } ... default { stmts } }` — v0.4.7.
    Switch {
        creg: String,
        cases: Vec<(SwitchLabel, Vec<Stmt>)>,
        line: usize,
        col: usize,
    },
    /// `box [designator]? { stmts }` — v0.6.8.  OpenQASM 3.0 의 box scope.
    /// panta-sim 은 timing/scheduling 을 모델링하지 않으므로 designator 는
    /// 무시하고 body 를 투명하게 (scope wrapper 없이) 직접 lowering 한다.
    Box {
        body: Vec<Stmt>,
        line: usize,
        col: usize,
    },
    /// `def name(typed-params) { gate-body }` 서브루틴 정의 (v0.6.9, v0.7.3
    /// qubit 배열 추가).  OpenQASM 3.0 §4.  classical (int/float/angle/uint),
    /// qubit (단일), qubit[N] (배열) 파라미터를 섞을 수 있으며, 호출 시 body 가
    /// 인라인 확장된다.  반환값 / bit 파라미터 / body 내 measure·control-flow 는
    /// 미지원 (lowering 에서 거부).
    DefDecl(DefDecl),
    /// def 서브루틴 호출 `name(arg, arg, ...)` (v0.6.9).  classical 인자는
    /// 표현식, qubit 인자는 qubit 참조 — 순서대로 def 파라미터에 바인딩된다.
    DefCall {
        name: String,
        args: Vec<DefArg>,
        line: usize,
        col: usize,
    },
    /// 3.0 의 `def` 등 아직 미지원 키워드 — UnsupportedFeature.
    UnsupportedV3 {
        keyword: &'static str,
        line: usize,
        col: usize,
    },
}

/// Switch-case label.  `Some(N)` 또는 `None` (default).
#[derive(Debug, Clone)]
pub enum SwitchLabel {
    Value(i64),
    Default,
}

/// def 파라미터 종류 (v0.6.9, v0.7.3 QubitArray 추가).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DefParamKind {
    /// int / float / angle / uint — gate angle 표현식에 쓰이는 스칼라 (f64).
    Classical,
    /// qubit (단일).
    Qubit,
    /// qubit[N] — qubit 배열 (레지스터).  호출 시 레지스터/슬라이스 전달,
    /// body 에서 `name[i]` 인덱싱 (v0.7.3).
    QubitArray,
}

/// def 파라미터 (`int[32] a`, `qubit q`, `qubit[2] q` 등).
#[derive(Debug, Clone)]
pub struct DefParam {
    pub kind: DefParamKind,
    pub name: String,
    /// QubitArray 의 선언 크기 (`qubit[N]`).  None 이면 크기 미명시 (호출
    /// 레지스터 크기에 맞춤).  Classical/Qubit 에선 무시.
    pub size: Option<usize>,
}

/// def 호출 인자 — classical 표현식 또는 qubit 참조.
#[derive(Debug, Clone)]
pub enum DefArg {
    Classical(Expr),
    Qubit(QArg),
}

/// `def name(params) { body }` 서브루틴 정의 (v0.6.9, v0.7.3 body = Vec<Stmt>).
#[derive(Debug, Clone)]
pub struct DefDecl {
    pub name: String,
    pub params: Vec<DefParam>,
    /// body 문장들 (v0.7.3): gate-call / measure / reset / control-flow 허용.
    /// include/decl/nested-def 는 parser 가 거부.
    pub body: Vec<Stmt>,
    pub line: usize,
    pub col: usize,
}

#[derive(Debug, Clone)]
pub struct GateDecl {
    pub name: String,
    pub params: Vec<String>,
    pub qubits: Vec<String>,
    pub body: Vec<GateCall>,
    pub line: usize,
    pub col: usize,
}

#[derive(Debug, Clone)]
pub struct GateCall {
    pub name: String,
    pub params: Vec<Expr>,
    pub qargs: Vec<QArg>,
    pub line: usize,
    pub col: usize,
}

/// 양자 비트 인자.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum QArg {
    /// `q[i]` — 특정 인덱스.
    Indexed { reg: String, idx: usize },
    /// `q` — 레지스터 전체 (barrier / 사용자 정의 gate body 내 매개변수 참조).
    Whole { reg: String },
}

/// 클래식 비트 인자.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CArg {
    Indexed { reg: String, idx: usize },
    Whole { reg: String },
}

/// 게이트 파라미터 표현식. 컴파일 시점에 `f64` 로 평가된다.
#[derive(Debug, Clone)]
pub enum Expr {
    Int(i64),
    Real(f64),
    Pi,
    /// gate-decl 내부에서 파라미터 식별자.
    Var(String),
    Neg(Box<Expr>),
    Bin {
        op: BinOp,
        lhs: Box<Expr>,
        rhs: Box<Expr>,
    },
    Call {
        fn_: BuiltinFn,
        arg: Box<Expr>,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BinOp {
    Add,
    Sub,
    Mul,
    Div,
    Pow,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BuiltinFn {
    Sin,
    Cos,
    Tan,
    Exp,
    Ln,
    Sqrt,
}
