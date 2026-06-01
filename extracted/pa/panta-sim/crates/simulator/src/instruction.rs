use qsim_core::{Gate, NoiseChannel};

/// 회로에 추가되는 개별 명령.
#[derive(Debug, Clone)]
pub enum Instruction {
    /// 게이트 적용 명령.
    ApplyGate { gate: Gate, targets: Vec<usize> },
    /// 단일 큐비트 노이즈 채널 적용 (v0.4 stochastic trajectory).
    /// 실행 시 [`crate::engine::ExecutionEngine`] 의 RNG 로 Kraus 연산자 하나를
    /// 샘플링·적용·재정규화 한다.
    ApplyNoise {
        channel: NoiseChannel,
        target: usize,
    },
    /// 특정 큐비트 측정 명령.
    ///
    /// v0.4.5 부터 위치 의미가 확장: 회로 끝이 아닌 mid-circuit 위치에 있어도
    /// 즉시 collapse + cbit 갱신이 수행된다 (dynamic 모드). 회로에 dynamic
    /// instruction (`Reset`/`IfEq`/위치별 `Measure`) 이 하나라도 있으면 engine
    /// 이 trajectory 모드로 전환된다.
    Measure { qubit: usize, cbit: usize },
    /// 모든 큐비트 측정 (회로 끝 한 번만).
    MeasureAll,
    /// 큐비트를 |0⟩ 상태로 리셋 (v0.4.5).
    ///
    /// 측정 + outcome 따른 X 적용과 의미 동등하지만 cbit 을 소비하지 않는다.
    /// engine 에서 P_0 projector 적용 + 재정규화 (norm=0 이면 |1⟩→|0⟩ swap)
    /// 으로 직접 구현.
    Reset { qubit: usize },
    /// Classical-controlled 게이트 적용 (v0.4.5).
    ///
    /// `cbit_indices` 의 cbit 들을 LSB-first packed 정수로 만들고 `value` 와
    /// 같으면 `body` 를 실행. `body` 는 단일 [`Instruction::ApplyGate`] 만
    /// 허용 (Qiskit `instr.condition` / OpenQASM `if (c==N) gate;` 의미).
    /// 빌더 (`Circuit::c_if_last`) 와 lowering 모두 이 invariant 를 enforce.
    ///
    /// v0.4.7 에서 [`Instruction::IfElse`] (sub-circuit body) 가 도입됐지만
    /// `IfEq` 는 가벼운 single-gate 케이스 + 기존 v0.4.5 코드 호환성을 위해
    /// 그대로 유지된다.  새 코드는 `IfElse` 사용 권장.
    IfEq {
        cbit_indices: Vec<usize>,
        value: u64,
        body: Box<Instruction>,
    },
    /// Block-form classical control flow (v0.4.7) — Qiskit `IfElseOp` 동치.
    ///
    /// `cbit_indices` (LSB-first packed) 가 `value` 와 같으면 `then_body` 를,
    /// 다르면 `else_body` (있으면) 를 실행.  body 는 임의 sub-circuit
    /// (`Vec<Instruction>`) — nested IfElse / 게이트 시퀀스 / Reset / Measure
    /// 모두 가능.
    IfElse {
        cbit_indices: Vec<usize>,
        value: u64,
        then_body: Vec<Instruction>,
        else_body: Option<Vec<Instruction>>,
    },
    /// While loop (v0.4.7) — Qiskit `WhileLoopOp` 동치.
    ///
    /// `cbit_indices == value` 인 동안 `body` 반복.  `max_iters` 로 안전
    /// bound (디폴트 256, 안전망).  cbit 이 body 안에서 갱신되지 않으면 1 회
    /// 실행 후 종료 또는 max_iters 회까지 도달.
    WhileLoop {
        cbit_indices: Vec<usize>,
        value: u64,
        body: Vec<Instruction>,
        max_iters: usize,
    },
    /// For loop (v0.4.7) — Qiskit `ForLoopOp` 동치.
    ///
    /// `body` 를 정확히 `iterations` 회 반복.  loop variable 은 panta-sim
    /// 에서 직접 사용 불가 — body 안에서 i 가 게이트 인자로 쓰이는 회로는
    /// 빌더 측에서 unroll 후 [`Instruction::ApplyGate`] 시퀀스로 push 해야 함
    /// (또는 from_qiskit adapter 가 unroll 처리).
    ForLoop {
        iterations: usize,
        body: Vec<Instruction>,
    },
    /// Switch-case (v0.4.7) — Qiskit `SwitchCaseOp` 동치.
    ///
    /// `cbit_indices` 의 packed 정수가 case 의 label 과 일치하는 첫 case 의
    /// body 를 실행.  label 이 `None` 이면 default (어느 case 에도 매칭 안
    /// 됐을 때).  default 는 cases 리스트의 마지막 위치에 한 번만 등장.
    Switch {
        cbit_indices: Vec<usize>,
        cases: Vec<(Option<u64>, Vec<Instruction>)>,
    },
}
