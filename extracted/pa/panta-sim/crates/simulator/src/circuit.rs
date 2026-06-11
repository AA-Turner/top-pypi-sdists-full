use qsim_core::{Gate, NoiseChannel, NoiseChannel2};

use crate::instruction::Instruction;

/// closure-based block control flow body builder (v0.4.7).
/// `Box<dyn FnOnce(&mut Circuit)>` 의 type alias — clippy type_complexity 회피.
pub type SubCircuitBuilder = Box<dyn FnOnce(&mut Circuit)>;

/// 양자 회로. 게이트와 측정 명령을 순서대로 저장한다.
///
/// `global_phase` 는 회로 전체에 곱해지는 e^(iλ) 인자를 라디안으로 추적한다
/// (Qiskit 의 `QuantumCircuit.global_phase` 와 동일 개념). 측정 결과 분포에는
/// 영향이 없지만 statevector 수준 비교/내보내기에서는 보존되어야 한다.
/// 누적은 [`Circuit::add_global_phase`] 로만 한다 — Decomposition 함수는 자기
/// 몫만 더하고 호출자가 책임진다.
#[derive(Debug, Clone)]
pub struct Circuit {
    n_qubits: usize,
    n_cbits: usize,
    instructions: Vec<Instruction>,
    global_phase: f64,
}

impl Circuit {
    /// n큐비트 빈 회로를 생성한다.
    pub fn new(n_qubits: usize) -> Self {
        Self {
            n_qubits,
            n_cbits: 0,
            instructions: Vec::new(),
            global_phase: 0.0,
        }
    }

    pub fn num_qubits(&self) -> usize {
        self.n_qubits
    }

    pub fn num_cbits(&self) -> usize {
        self.n_cbits
    }

    pub fn instructions(&self) -> &[Instruction] {
        &self.instructions
    }

    /// 명령 리스트에 대한 가변 참조 (트랜스파일러용).
    pub fn instructions_mut(&mut self) -> &mut Vec<Instruction> {
        &mut self.instructions
    }

    /// 누적된 글로벌 phase λ (라디안).
    pub fn global_phase(&self) -> f64 {
        self.global_phase
    }

    /// 글로벌 phase 에 λ 를 더한다.
    pub fn add_global_phase(&mut self, lambda: f64) {
        self.global_phase += lambda;
    }

    /// 글로벌 phase 를 λ 로 설정한다.
    pub fn set_global_phase(&mut self, lambda: f64) {
        self.global_phase = lambda;
    }

    fn validate_qubit(&self, q: usize) {
        assert!(
            q < self.n_qubits,
            "큐비트 인덱스 {q}가 범위를 벗어남 (n_qubits={})",
            self.n_qubits
        );
    }

    fn add_gate(&mut self, gate: Gate, targets: Vec<usize>) {
        for &t in &targets {
            self.validate_qubit(t);
        }
        // v0.6.2: multi-qubit gate operands distinct check.  release path 도 막아
        // core operations 의 controlled-update 가 silent corruption 을 일으키는
        // 입력 (예: cx(0,0)) 을 거부.  Python API 의 check_qs 가 이미 막지만,
        // QASM lowering / Rust crate 직접 사용에도 동일 보장이 필요.
        if targets.len() > 1 {
            for i in 0..targets.len() {
                for j in (i + 1)..targets.len() {
                    assert!(
                        targets[i] != targets[j],
                        "multi-qubit gate operands 중복: {:?} (gate operands 는 distinct 해야 함)",
                        targets
                    );
                }
            }
        }
        self.instructions
            .push(Instruction::ApplyGate { gate, targets });
    }

    // 단일 큐비트 게이트
    pub fn h(&mut self, qubit: usize) {
        self.add_gate(Gate::H, vec![qubit]);
    }
    pub fn x(&mut self, qubit: usize) {
        self.add_gate(Gate::X, vec![qubit]);
    }
    pub fn y(&mut self, qubit: usize) {
        self.add_gate(Gate::Y, vec![qubit]);
    }
    pub fn z(&mut self, qubit: usize) {
        self.add_gate(Gate::Z, vec![qubit]);
    }
    pub fn s(&mut self, qubit: usize) {
        self.add_gate(Gate::S, vec![qubit]);
    }
    pub fn sdg(&mut self, qubit: usize) {
        self.add_gate(Gate::Sdg, vec![qubit]);
    }
    pub fn t(&mut self, qubit: usize) {
        self.add_gate(Gate::T, vec![qubit]);
    }
    pub fn tdg(&mut self, qubit: usize) {
        self.add_gate(Gate::Tdg, vec![qubit]);
    }
    /// √X — Sx 게이트 (v0.4.6).  IBM Falcon/Eagle hardware-native.
    pub fn sx(&mut self, qubit: usize) {
        self.add_gate(Gate::Sx, vec![qubit]);
    }
    /// √X† — Sxdg 게이트 (v0.4.6).
    pub fn sxdg(&mut self, qubit: usize) {
        self.add_gate(Gate::Sxdg, vec![qubit]);
    }
    /// Phase 게이트 `P(λ) = diag(1, e^iλ)` (v0.4.6).  Qiskit `p(λ)` / `u1(λ)`.
    pub fn p(&mut self, lambda: f64, qubit: usize) {
        self.add_gate(Gate::P(lambda), vec![qubit]);
    }
    /// `U2(φ, λ) = U(π/2, φ, λ)` (v0.4.6).
    pub fn u2(&mut self, phi: f64, lambda: f64, qubit: usize) {
        self.add_gate(Gate::U2(phi, lambda), vec![qubit]);
    }
    /// OpenQASM `U(θ,φ,λ)` (= Qiskit `u3`) 일반 1-큐비트 유니터리.
    pub fn u(&mut self, theta: f64, phi: f64, lambda: f64, qubit: usize) {
        self.add_gate(Gate::U(theta, phi, lambda), vec![qubit]);
    }
    pub fn rx(&mut self, theta: f64, qubit: usize) {
        self.add_gate(Gate::Rx(theta), vec![qubit]);
    }
    pub fn ry(&mut self, theta: f64, qubit: usize) {
        self.add_gate(Gate::Ry(theta), vec![qubit]);
    }
    pub fn rz(&mut self, theta: f64, qubit: usize) {
        self.add_gate(Gate::Rz(theta), vec![qubit]);
    }
    pub fn id(&mut self, qubit: usize) {
        self.add_gate(Gate::Id, vec![qubit]);
    }

    // 2큐비트 게이트
    pub fn cx(&mut self, control: usize, target: usize) {
        self.add_gate(Gate::CNOT, vec![control, target]);
    }
    pub fn cz(&mut self, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::CZ, vec![qubit0, qubit1]);
    }
    pub fn swap(&mut self, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::SWAP, vec![qubit0, qubit1]);
    }
    /// iSWAP (v0.7).
    pub fn iswap(&mut self, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::ISwap, vec![qubit0, qubit1]);
    }
    /// `RXX(θ) = exp(-iθ/2 X⊗X)` (v0.7).
    pub fn rxx(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Rxx(theta), vec![qubit0, qubit1]);
    }
    /// `RYY(θ) = exp(-iθ/2 Y⊗Y)` (v0.7).
    pub fn ryy(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Ryy(theta), vec![qubit0, qubit1]);
    }
    /// `RZZ(θ) = exp(-iθ/2 Z⊗Z)` (v0.7).
    pub fn rzz(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Rzz(theta), vec![qubit0, qubit1]);
    }
    /// DCX — double-CNOT (v0.7.1).
    pub fn dcx(&mut self, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Dcx, vec![qubit0, qubit1]);
    }
    /// ECR — echoed cross-resonance (v0.7.1).
    pub fn ecr(&mut self, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Ecr, vec![qubit0, qubit1]);
    }
    /// `RZX(θ) = exp(-iθ/2 Z⊗X)` (v0.7.1).
    pub fn rzx(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::Rzx(theta), vec![qubit0, qubit1]);
    }
    /// `XXPlusYY(θ)` excitation-preserving (v0.7.1).
    pub fn xx_plus_yy(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::XxPlusYy(theta), vec![qubit0, qubit1]);
    }
    /// `XXMinusYY(θ)` (v0.7.1).
    pub fn xx_minus_yy(&mut self, theta: f64, qubit0: usize, qubit1: usize) {
        self.add_gate(Gate::XxMinusYy(theta), vec![qubit0, qubit1]);
    }
    /// Controlled-Y (v0.4.6).
    pub fn cy(&mut self, control: usize, target: usize) {
        self.add_gate(Gate::CY, vec![control, target]);
    }
    /// Controlled-H (v0.4.6).
    pub fn ch(&mut self, control: usize, target: usize) {
        self.add_gate(Gate::CH, vec![control, target]);
    }
    /// Controlled-Rx(θ) (v0.4.6).
    pub fn crx(&mut self, theta: f64, control: usize, target: usize) {
        self.add_gate(Gate::CRx(theta), vec![control, target]);
    }
    /// Controlled-Ry(θ) (v0.4.6).
    pub fn cry(&mut self, theta: f64, control: usize, target: usize) {
        self.add_gate(Gate::CRy(theta), vec![control, target]);
    }
    /// Controlled-Rz(θ) (v0.4.6).
    pub fn crz(&mut self, theta: f64, control: usize, target: usize) {
        self.add_gate(Gate::CRz(theta), vec![control, target]);
    }
    /// Controlled-Phase(λ) (v0.4.6).  Qiskit `cp(λ)` / `cu1(λ)` 와 동일.
    pub fn cp(&mut self, lambda: f64, control: usize, target: usize) {
        self.add_gate(Gate::CP(lambda), vec![control, target]);
    }
    /// Controlled-U3(θ,φ,λ) (v0.4.6).  Qiskit `cu3(θ,φ,λ)`.
    pub fn cu3(&mut self, theta: f64, phi: f64, lambda: f64, control: usize, target: usize) {
        self.add_gate(Gate::CU3(theta, phi, lambda), vec![control, target]);
    }
    /// Controlled-U(θ,φ,λ,γ) (v0.4.6).  Qiskit `cu(θ,φ,λ,γ)`.
    pub fn cu(
        &mut self,
        theta: f64,
        phi: f64,
        lambda: f64,
        gamma: f64,
        control: usize,
        target: usize,
    ) {
        self.add_gate(Gate::CU(theta, phi, lambda, gamma), vec![control, target]);
    }

    // 3큐비트 게이트
    pub fn ccx(&mut self, ctrl1: usize, ctrl2: usize, target: usize) {
        self.add_gate(Gate::Toffoli, vec![ctrl1, ctrl2, target]);
    }
    pub fn cswap(&mut self, control: usize, target1: usize, target2: usize) {
        self.add_gate(Gate::Fredkin, vec![control, target1, target2]);
    }

    /// 임의 k-큐비트 유니터리를 직접 적용한다 (v0.6.8).
    ///
    /// `matrix` 는 `2^k × 2^k` row-major (`matrix[row * 2^k + col]`),
    /// `targets` 는 k 개의 큐비트.  행렬 sub-index 비트 `j` 가 `targets[j]`
    /// 에 대응 (`targets[0]` = LSB).  unitarity 검증은 호출 측 (Python
    /// binding) 책임.  statevector 백엔드에서만 지원되며 다른 백엔드는
    /// 실행 시 에러를 반환한다.
    ///
    /// # Panics
    /// `targets` 가 비었거나 중복이거나, 큐비트 인덱스가 범위를 벗어나거나,
    /// `matrix.len() != 4^k` 이면 panic.
    pub fn unitary(&mut self, matrix: Vec<num_complex::Complex<f64>>, targets: Vec<usize>) {
        assert!(!targets.is_empty(), "unitary: targets 는 비어 있을 수 없음");
        for &t in &targets {
            self.validate_qubit(t);
        }
        for i in 0..targets.len() {
            for j in (i + 1)..targets.len() {
                assert!(
                    targets[i] != targets[j],
                    "unitary: targets 중복: {targets:?} (distinct 해야 함)"
                );
            }
        }
        let dim = 1usize << targets.len();
        assert_eq!(
            matrix.len(),
            dim * dim,
            "unitary: matrix 는 2^k × 2^k 여야 함 (k={}, expected {}, got {})",
            targets.len(),
            dim * dim,
            matrix.len()
        );
        self.instructions
            .push(Instruction::ApplyUnitary { matrix, targets });
    }

    /// 특정 큐비트를 측정하여 클래식 비트에 저장한다.
    pub fn measure(&mut self, qubit: usize, cbit: usize) {
        self.validate_qubit(qubit);
        if cbit >= self.n_cbits {
            self.n_cbits = cbit + 1;
        }
        self.instructions.push(Instruction::Measure { qubit, cbit });
    }

    /// 모든 큐비트를 측정한다.
    pub fn measure_all(&mut self) {
        // 빌더 불변식: n_cbits 는 단조 증가만 한다.  이전의 `= n_qubits` 는
        // 앞선 measure(q, c) 가 c >= n_qubits 로 넓혀 둔 레지스터를 줄여,
        // release 빌드에서 해당 cbit 기록이 조용히 사라지는 버그였다.
        self.n_cbits = self.n_cbits.max(self.n_qubits);
        self.instructions.push(Instruction::MeasureAll);
    }

    /// 단일 큐비트 노이즈 채널을 회로 명령 시퀀스에 추가한다 (v0.4 trajectory).
    ///
    /// 실행 시점 (`ExecutionEngine::run`) 에 RNG 로 Kraus 연산자 하나가 샘플링되어
    /// 적용된다. 회로 자체는 deterministic — 동일 seed 로 같은 결과가 재현된다.
    pub fn add_noise(&mut self, channel: NoiseChannel, qubit: usize) {
        self.validate_qubit(qubit);
        self.instructions.push(Instruction::ApplyNoise {
            channel,
            target: qubit,
        });
    }

    /// 2-큐비트 상관 노이즈 채널을 회로 명령 시퀀스에 추가한다 (v0.7.2 trajectory).
    pub fn add_noise_2q(&mut self, channel: NoiseChannel2, q0: usize, q1: usize) {
        self.validate_qubit(q0);
        self.validate_qubit(q1);
        assert!(q0 != q1, "add_noise_2q: q0 == q1 ({q0})");
        self.instructions
            .push(Instruction::ApplyNoise2 { channel, q0, q1 });
    }

    /// 큐비트를 |0⟩ 상태로 리셋한다 (v0.4.5).
    ///
    /// 측정 + 조건부 X 의 합성과 의미 동등하지만 cbit 을 소비하지 않는다.
    /// trajectory 실행 시 P_0 projector + 재정규화 (norm=0 이면 |1⟩→|0⟩ swap)
    /// 으로 즉시 적용된다.
    pub fn reset(&mut self, qubit: usize) {
        self.validate_qubit(qubit);
        self.instructions.push(Instruction::Reset { qubit });
    }

    /// 직전에 추가된 게이트를 classical-controlled 로 wrap 한다 (v0.4.5).
    ///
    /// Qiskit `qc.x(0).c_if(c, 1)` 와 동등 — 마지막 [`Instruction::ApplyGate`]
    /// 를 [`Instruction::IfEq`] 로 in-place swap 한다.
    /// `cbit_indices` 는 LSB-first 로 packed 정수로 만들어져 `value` 와 비교된다.
    ///
    /// `n_cbits` 는 `max(cbit_indices) + 1` 까지 자동 grow.
    ///
    /// # Panics
    /// - 회로가 비어 있거나 마지막 instruction 이 `ApplyGate` 가 아니면 panic.
    /// - `cbit_indices` 가 비어 있으면 panic.
    /// - `cbit_indices.len() > 64` 면 panic (u64 packing 한계).
    pub fn c_if_last(&mut self, cbit_indices: Vec<usize>, value: u64) {
        assert!(
            !cbit_indices.is_empty(),
            "c_if_last: cbit_indices 가 비어 있을 수 없습니다"
        );
        assert!(
            cbit_indices.len() <= 64,
            "c_if_last: cbit_indices 길이가 64 를 초과 ({}). u64 packing 한계.",
            cbit_indices.len()
        );
        let last = self
            .instructions
            .pop()
            .expect("c_if_last: 회로가 비어 있어 wrap 할 게이트가 없습니다");
        match &last {
            Instruction::ApplyGate { .. } => {}
            other => panic!("c_if_last: 마지막 instruction 이 ApplyGate 가 아닙니다: {other:?}"),
        }
        let max_cbit = *cbit_indices.iter().max().unwrap();
        if max_cbit >= self.n_cbits {
            self.n_cbits = max_cbit + 1;
        }
        self.instructions.push(Instruction::IfEq {
            cbit_indices,
            value,
            body: Box::new(last),
        });
    }

    // ========================================================================
    // v0.4.7 — Block-form classical control flow
    // ========================================================================

    /// Block-form `if (cbits == value) then_body [else else_body]` 추가 (v0.4.7).
    ///
    /// `then_body` / `else_body` 는 사용자 closure 가 nested [`Circuit`] 에
    /// instruction 들을 push 하면 그 instruction 시퀀스가 sub-circuit 으로
    /// 보존된다.  nested IfElse / WhileLoop / ForLoop / Switch / 게이트 /
    /// Reset / Measure 모두 가능.
    ///
    /// `n_cbits` 는 max(cbit_indices) + 1 까지 자동 grow + sub-circuit 의
    /// n_cbits 도 propagate.
    ///
    /// # Panics
    /// - `cbit_indices` 가 비어 있거나 길이 64 초과.
    pub fn if_else(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        then_fn: impl FnOnce(&mut Circuit),
        else_fn: Option<SubCircuitBuilder>,
    ) {
        assert!(!cbit_indices.is_empty(), "if_else: cbit_indices empty");
        assert!(
            cbit_indices.len() <= 64,
            "if_else: cbit_indices > 64 (u64 packing)"
        );
        let max_cbit = *cbit_indices.iter().max().unwrap();
        if max_cbit >= self.n_cbits {
            self.n_cbits = max_cbit + 1;
        }

        let then_body = self.build_subcircuit(then_fn);
        let else_body = else_fn.map(|f| self.build_subcircuit_dyn(f));

        self.instructions.push(Instruction::IfElse {
            cbit_indices,
            value,
            then_body,
            else_body,
        });
    }

    /// `while (cbits == value)` loop (v0.4.7).
    ///
    /// `max_iters` 안전 bound (디폴트 권장 256).
    pub fn while_loop(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        max_iters: usize,
        body_fn: impl FnOnce(&mut Circuit),
    ) {
        assert!(!cbit_indices.is_empty(), "while_loop: cbit_indices empty");
        assert!(
            cbit_indices.len() <= 64,
            "while_loop: cbit_indices > 64 (u64 packing)"
        );
        let max_cbit = *cbit_indices.iter().max().unwrap();
        if max_cbit >= self.n_cbits {
            self.n_cbits = max_cbit + 1;
        }

        let body = self.build_subcircuit(body_fn);
        self.instructions.push(Instruction::WhileLoop {
            cbit_indices,
            value,
            body,
            max_iters,
        });
    }

    /// `for _ in 0..iterations` loop (v0.4.7) — body 를 정확히 N 번 반복.
    pub fn for_loop(&mut self, iterations: usize, body_fn: impl FnOnce(&mut Circuit)) {
        let body = self.build_subcircuit(body_fn);
        self.instructions
            .push(Instruction::ForLoop { iterations, body });
    }

    /// Switch-case (v0.4.7) — `cases` 의 각 (label, body_fn) 빌드.
    ///
    /// `label` 이 `None` 이면 default — 마지막 case 한 번만 허용.
    pub fn switch(
        &mut self,
        cbit_indices: Vec<usize>,
        cases: Vec<(Option<u64>, SubCircuitBuilder)>,
    ) {
        assert!(!cbit_indices.is_empty(), "switch: cbit_indices empty");
        assert!(
            cbit_indices.len() <= 64,
            "switch: cbit_indices > 64 (u64 packing)"
        );
        let max_cbit = *cbit_indices.iter().max().unwrap();
        if max_cbit >= self.n_cbits {
            self.n_cbits = max_cbit + 1;
        }

        let mut compiled_cases: Vec<(Option<u64>, Vec<Instruction>)> = Vec::new();
        for (label, body_fn) in cases {
            let body = self.build_subcircuit_dyn(body_fn);
            compiled_cases.push((label, body));
        }
        self.instructions.push(Instruction::Switch {
            cbit_indices,
            cases: compiled_cases,
        });
    }

    /// closure 에 nested Circuit 을 빌드시켜 instruction 시퀀스를 추출.
    /// nested 가 사용한 cbit 폭은 호출자에게 propagate.
    fn build_subcircuit(&mut self, f: impl FnOnce(&mut Circuit)) -> Vec<Instruction> {
        let mut sub = Circuit::new(self.n_qubits);
        sub.n_cbits = self.n_cbits;
        f(&mut sub);
        if sub.n_cbits > self.n_cbits {
            self.n_cbits = sub.n_cbits;
        }
        sub.instructions
    }

    /// Box<dyn FnOnce> 변종 — Vec 안에 들고 다닐 수 있는 closure 용.
    fn build_subcircuit_dyn(&mut self, f: SubCircuitBuilder) -> Vec<Instruction> {
        let mut sub = Circuit::new(self.n_qubits);
        sub.n_cbits = self.n_cbits;
        f(&mut sub);
        if sub.n_cbits > self.n_cbits {
            self.n_cbits = sub.n_cbits;
        }
        sub.instructions
    }

    /// Block-form IfElse 를 명시적 Vec<Instruction> body 로 추가 (PyO3 / adapter
    /// 용 — closure 빌더로 안 풀리는 경우).
    pub fn add_if_else(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        then_body: Vec<Instruction>,
        else_body: Option<Vec<Instruction>>,
    ) {
        self.grow_n_cbits_for_indices(&cbit_indices);
        // v0.6.2: body 안의 Measure { cbit } 를 재귀 스캔해 outer n_cbits 도 함께
        // grow.  이전엔 body cbit > outer n_cbits 면 dispatch 의 silent guard
        // (engine.rs `if *cbit < cbits.len()`) 가 측정 결과를 조용히 버렸음.
        self.grow_n_cbits_for_body(&then_body);
        if let Some(eb) = else_body.as_deref() {
            self.grow_n_cbits_for_body(eb);
        }
        self.instructions.push(Instruction::IfElse {
            cbit_indices,
            value,
            then_body,
            else_body,
        });
    }

    /// Block-form WhileLoop 명시적 body 변종.
    pub fn add_while_loop(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        body: Vec<Instruction>,
        max_iters: usize,
    ) {
        self.grow_n_cbits_for_indices(&cbit_indices);
        self.grow_n_cbits_for_body(&body);
        self.instructions.push(Instruction::WhileLoop {
            cbit_indices,
            value,
            body,
            max_iters,
        });
    }

    /// Block-form ForLoop 명시적 body 변종.
    pub fn add_for_loop(&mut self, iterations: usize, body: Vec<Instruction>) {
        self.grow_n_cbits_for_body(&body);
        self.instructions
            .push(Instruction::ForLoop { iterations, body });
    }

    /// Block-form Switch 명시적 cases 변종.
    pub fn add_switch(
        &mut self,
        cbit_indices: Vec<usize>,
        cases: Vec<(Option<u64>, Vec<Instruction>)>,
    ) {
        self.grow_n_cbits_for_indices(&cbit_indices);
        for (_, body) in &cases {
            self.grow_n_cbits_for_body(body);
        }
        self.instructions.push(Instruction::Switch {
            cbit_indices,
            cases,
        });
    }

    fn grow_n_cbits_for_indices(&mut self, cbit_indices: &[usize]) {
        // pack_cbits 가 u64 로 패킹하므로 조건 비트는 64개 이하여야 한다.
        // (release 빌드에서 `1u64 << 64` 는 shift 마스킹으로 cbit 64 가
        // cbit 0 으로 aliasing 되는 silent bug 가 됨.)
        assert!(
            cbit_indices.len() <= 64,
            "control-flow condition: cbit_indices > 64 (u64 packing)"
        );
        if let Some(max_cbit) = cbit_indices.iter().max() {
            if *max_cbit >= self.n_cbits {
                self.n_cbits = *max_cbit + 1;
            }
        }
    }

    fn grow_n_cbits_for_body(&mut self, body: &[Instruction]) {
        if let Some(max_cbit) = scan_body_max_cbit(body) {
            if max_cbit >= self.n_cbits {
                self.n_cbits = max_cbit + 1;
            }
        }
    }

    /// Dynamic instruction (Reset / IfEq / 위치별 Measure) 가 회로 안에 하나라도
    /// 있는지 검사한다.
    ///
    /// `true` 면 engine 이 trajectory 모드로 전환되어 cbit register + 위치별
    /// 즉시 처리를 수행한다. `false` 면 기존 fast path (1 evolution + N shot
    /// 샘플) 을 유지한다.
    ///
    /// `MeasureAll` 만 회로 끝에 있고 그 외는 게이트뿐인 회로는 dynamic 이 아니다.
    pub fn has_dynamic(&self) -> bool {
        let last_idx = self.instructions.len().saturating_sub(1);
        for (i, inst) in self.instructions.iter().enumerate() {
            match inst {
                Instruction::Reset { .. }
                | Instruction::IfEq { .. }
                | Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => return true,
                Instruction::Measure { .. } => {
                    // 회로 끝에만 있는 trailing Measure 묶음은 fast path (sampling)
                    // 가능. 중간이거나 뒤에 게이트/Reset/IfEq 가 더 있으면 dynamic.
                    for later in &self.instructions[i + 1..] {
                        match later {
                            Instruction::Measure { .. } => {} // trailing measure 그룹 OK
                            _ => return true,
                        }
                    }
                }
                Instruction::MeasureAll => {
                    // MeasureAll 뒤에 더 있으면 dynamic. 보통은 마지막.
                    if i != last_idx {
                        return true;
                    }
                }
                Instruction::ApplyGate { .. }
                | Instruction::ApplyUnitary { .. }
                | Instruction::ApplyNoise { .. }
                | Instruction::ApplyNoise2 { .. } => {}
            }
        }
        false
    }
}

/// 재귀로 instruction 시퀀스 안의 `Measure { cbit }` 와 control-flow body
/// 들이 사용하는 cbit 인덱스 최댓값을 찾는다.  body 안에 측정이 없으면 `None`.
///
/// `add_if_else` / `add_while_loop` / `add_for_loop` / `add_switch` 가 outer
/// circuit 의 `n_cbits` 를 충분히 확장하기 위해 사용.
pub fn scan_body_max_cbit(body: &[Instruction]) -> Option<usize> {
    let mut max_cbit: Option<usize> = None;
    let mut update = |c: Option<usize>| {
        if let Some(v) = c {
            max_cbit = Some(max_cbit.map_or(v, |m| m.max(v)));
        }
    };
    for inst in body {
        match inst {
            Instruction::Measure { cbit, .. } => update(Some(*cbit)),
            Instruction::IfEq {
                cbit_indices, body, ..
            } => {
                update(cbit_indices.iter().copied().max());
                update(scan_body_max_cbit(std::slice::from_ref(body)));
            }
            Instruction::IfElse {
                cbit_indices,
                then_body,
                else_body,
                ..
            } => {
                update(cbit_indices.iter().copied().max());
                update(scan_body_max_cbit(then_body));
                if let Some(eb) = else_body.as_deref() {
                    update(scan_body_max_cbit(eb));
                }
            }
            Instruction::WhileLoop {
                cbit_indices, body, ..
            } => {
                update(cbit_indices.iter().copied().max());
                update(scan_body_max_cbit(body));
            }
            Instruction::ForLoop { body, .. } => {
                update(scan_body_max_cbit(body));
            }
            Instruction::Switch {
                cbit_indices,
                cases,
            } => {
                update(cbit_indices.iter().copied().max());
                for (_, b) in cases {
                    update(scan_body_max_cbit(b));
                }
            }
            _ => {}
        }
    }
    max_cbit
}

/// 재귀로 instruction 시퀀스 안에 `Measure` 가 하나라도 있는지 검사.
/// trajectory loop 의 `has_explicit_measure` 계산에 사용 (control-flow body
/// 안의 측정도 final counts 에 반영하기 위해).
pub fn body_has_measure(body: &[Instruction]) -> bool {
    body.iter().any(|inst| match inst {
        Instruction::Measure { .. } => true,
        Instruction::IfEq { body, .. } => body_has_measure(std::slice::from_ref(body)),
        Instruction::IfElse {
            then_body,
            else_body,
            ..
        } => body_has_measure(then_body) || else_body.as_deref().is_some_and(body_has_measure),
        Instruction::WhileLoop { body, .. } | Instruction::ForLoop { body, .. } => {
            body_has_measure(body)
        }
        Instruction::Switch { cases, .. } => cases.iter().any(|(_, b)| body_has_measure(b)),
        _ => false,
    })
}
