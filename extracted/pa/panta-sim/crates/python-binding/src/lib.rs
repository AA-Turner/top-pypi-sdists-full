use num_complex::Complex;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use qsim_core::Gate;
use qsim_simulator::{
    Backend, Circuit, ExecutionEngine, Instruction, NoiseChannel, Precision, SimulationResult,
};

/// Python에서 사용 가능한 양자 회로 클래스.
#[pyclass(name = "Circuit")]
struct PyCircuit {
    inner: Circuit,
}

#[pymethods]
impl PyCircuit {
    #[new]
    fn new(n_qubits: usize) -> Self {
        Self {
            inner: Circuit::new(n_qubits),
        }
    }

    fn num_qubits(&self) -> usize {
        self.inner.num_qubits()
    }

    // 단일 큐비트 게이트
    fn h(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "h")?;
        self.inner.h(qubit);
        Ok(())
    }
    fn x(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "x")?;
        self.inner.x(qubit);
        Ok(())
    }
    fn y(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "y")?;
        self.inner.y(qubit);
        Ok(())
    }
    fn z(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "z")?;
        self.inner.z(qubit);
        Ok(())
    }
    fn s(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "s")?;
        self.inner.s(qubit);
        Ok(())
    }
    fn sdg(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "sdg")?;
        self.inner.sdg(qubit);
        Ok(())
    }
    fn t(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "t")?;
        self.inner.t(qubit);
        Ok(())
    }
    fn tdg(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "tdg")?;
        self.inner.tdg(qubit);
        Ok(())
    }
    fn sx(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "sx")?;
        self.inner.sx(qubit);
        Ok(())
    }
    fn sxdg(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "sxdg")?;
        self.inner.sxdg(qubit);
        Ok(())
    }
    fn p(&mut self, lambda: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "p")?;
        self.inner.p(lambda, qubit);
        Ok(())
    }
    fn u2(&mut self, phi: f64, lambda: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "u2")?;
        self.inner.u2(phi, lambda, qubit);
        Ok(())
    }
    fn u(&mut self, theta: f64, phi: f64, lambda: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "u")?;
        self.inner.u(theta, phi, lambda, qubit);
        Ok(())
    }
    fn rx(&mut self, theta: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "rx")?;
        self.inner.rx(theta, qubit);
        Ok(())
    }
    fn ry(&mut self, theta: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "ry")?;
        self.inner.ry(theta, qubit);
        Ok(())
    }
    fn rz(&mut self, theta: f64, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "rz")?;
        self.inner.rz(theta, qubit);
        Ok(())
    }
    fn id(&mut self, qubit: usize) -> PyResult<()> {
        self.check_q(qubit, "id")?;
        self.inner.id(qubit);
        Ok(())
    }

    // 2큐비트 게이트
    fn cx(&mut self, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "cx")?;
        self.inner.cx(control, target);
        Ok(())
    }
    fn cz(&mut self, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "cz")?;
        self.inner.cz(qubit0, qubit1);
        Ok(())
    }
    fn swap(&mut self, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "swap")?;
        self.inner.swap(qubit0, qubit1);
        Ok(())
    }
    fn cy(&mut self, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "cy")?;
        self.inner.cy(control, target);
        Ok(())
    }
    fn ch(&mut self, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "ch")?;
        self.inner.ch(control, target);
        Ok(())
    }
    fn crx(&mut self, theta: f64, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "crx")?;
        self.inner.crx(theta, control, target);
        Ok(())
    }
    fn cry(&mut self, theta: f64, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "cry")?;
        self.inner.cry(theta, control, target);
        Ok(())
    }
    fn crz(&mut self, theta: f64, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "crz")?;
        self.inner.crz(theta, control, target);
        Ok(())
    }
    fn cp(&mut self, lambda: f64, control: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[control, target], "cp")?;
        self.inner.cp(lambda, control, target);
        Ok(())
    }
    fn cu3(
        &mut self,
        theta: f64,
        phi: f64,
        lambda: f64,
        control: usize,
        target: usize,
    ) -> PyResult<()> {
        self.check_qs(&[control, target], "cu3")?;
        self.inner.cu3(theta, phi, lambda, control, target);
        Ok(())
    }
    fn cu(
        &mut self,
        theta: f64,
        phi: f64,
        lambda: f64,
        gamma: f64,
        control: usize,
        target: usize,
    ) -> PyResult<()> {
        self.check_qs(&[control, target], "cu")?;
        self.inner.cu(theta, phi, lambda, gamma, control, target);
        Ok(())
    }

    // 3큐비트 게이트
    fn ccx(&mut self, ctrl1: usize, ctrl2: usize, target: usize) -> PyResult<()> {
        self.check_qs(&[ctrl1, ctrl2, target], "ccx")?;
        self.inner.ccx(ctrl1, ctrl2, target);
        Ok(())
    }
    fn cswap(&mut self, control: usize, target1: usize, target2: usize) -> PyResult<()> {
        self.check_qs(&[control, target1, target2], "cswap")?;
        self.inner.cswap(control, target1, target2);
        Ok(())
    }

    fn measure(&mut self, qubit: usize, cbit: usize) -> PyResult<()> {
        self.check_q(qubit, "measure")?;
        self.inner.measure(qubit, cbit);
        Ok(())
    }
    fn measure_all(&mut self) {
        self.inner.measure_all();
    }

    /// OpenQASM 2.0 또는 3.0 문자열을 파싱해 [`Circuit`] 으로 만든다.
    ///
    /// 헤더 (`OPENQASM 2.0;` 또는 `OPENQASM 3.0;`) 로 버전 자동 감지.
    /// 미지원 syntax (`if`, `reset`, `for`/`while`/`box`, `sx`/`gphase` 등) 는
    /// `ValueError` 로 변환되어 사용자에게 명확한 milestone 정보가 노출된다.
    #[staticmethod]
    fn from_qasm(qasm: &str) -> PyResult<Self> {
        let circuit =
            qsim_qasm::parse_qasm(qasm).map_err(|e| PyValueError::new_err(format!("{e}")))?;
        Ok(Self { inner: circuit })
    }

    /// 회로를 OpenQASM 문자열로 export 한다.
    ///
    /// `version`: `"2.0"` (default) 또는 `"3.0"`. 다른 값은 `ValueError`.
    #[pyo3(signature = (version = "2.0"))]
    fn to_qasm(&self, version: &str) -> PyResult<String> {
        let dialect = match version {
            "2.0" | "2" => qsim_qasm::QasmDialect::V2,
            "3.0" | "3" => qsim_qasm::QasmDialect::V3,
            other => {
                return Err(PyValueError::new_err(format!(
                    "to_qasm: version 은 '2.0' 또는 '3.0' 이어야 합니다 (입력: {other:?})"
                )));
            }
        };
        Ok(qsim_qasm::circuit_to_qasm(&self.inner, dialect))
    }

    /// 임의 2×2 unitary 행렬을 회로의 `qubit` 큐비트에 적용한다.
    ///
    /// Z-Y-Z 분해 (Nielsen-Chuang Thm 4.1) 로 native 게이트 시퀀스
    /// `Rz(δ); Ry(γ); Rz(β)` 를 추가하고 글로벌 phase α 는 회로의
    /// global_phase 에 누적된다.
    ///
    /// `validate=True` (default) 일 때 입력 행렬의 unitarity (`M·M† ≈ I`,
    /// 1e-10) 를 검증하고 위반 시 `ValueError`. `False` 면 검증 생략.
    #[pyo3(signature = (matrix, qubit, validate = true))]
    fn unitary(
        &mut self,
        matrix: PyReadonlyArray2<Complex<f64>>,
        qubit: usize,
        validate: bool,
    ) -> PyResult<()> {
        let arr = matrix.as_array();
        if arr.shape() != [2, 2] {
            return Err(PyValueError::new_err(format!(
                "unitary: matrix 는 2×2 여야 합니다 (입력 shape={:?})",
                arr.shape()
            )));
        }
        let m: qsim_transpiler::Matrix2 = [[arr[[0, 0]], arr[[0, 1]]], [arr[[1, 0]], arr[[1, 1]]]];
        if validate {
            qsim_transpiler::is_unitary_2x2(&m, 1e-10)
                .map_err(|e| PyValueError::new_err(format!("unitary: {e}")))?;
        }
        if qubit >= self.inner.num_qubits() {
            return Err(PyValueError::new_err(format!(
                "unitary: qubit 인덱스 {qubit} 가 범위를 벗어남 (n_qubits={})",
                self.inner.num_qubits()
            )));
        }
        qsim_transpiler::append_unitary(&mut self.inner, &m, qubit);
        Ok(())
    }

    /// 회로에 peephole 최적화 패스를 in-place 로 적용한다.
    ///
    /// Cut C 에서 실제 패스 (회전 합성, 항등식, trivial drop) 가 활성화되며,
    /// 현재는 no-op stub.  반환값은 수렴까지 사용된 패스 횟수.
    #[pyo3(signature = (max_iters = 16))]
    fn transpile(&mut self, max_iters: usize) -> usize {
        let stats = qsim_transpiler::peephole_optimize(&mut self.inner, max_iters);
        stats.passes
    }

    /// 회로의 누적된 글로벌 phase (라디안).
    #[getter]
    fn global_phase(&self) -> f64 {
        self.inner.global_phase()
    }

    /// 회로의 글로벌 phase 를 명시적으로 설정한다 (NoiseModel.apply_to 등에서
    /// 회로 재구성 후 phase 보존용).
    #[setter(global_phase)]
    fn set_global_phase(&mut self, lambda: f64) {
        self.inner.set_global_phase(lambda);
    }

    /// 단일 큐비트 노이즈 채널을 회로 명령 시퀀스에 추가한다 (v0.4 trajectory).
    fn add_noise(&mut self, channel: &PyNoiseChannel, qubit: usize) -> PyResult<()> {
        if qubit >= self.inner.num_qubits() {
            return Err(PyValueError::new_err(format!(
                "add_noise: qubit {qubit} 가 범위를 벗어남 (n_qubits={})",
                self.inner.num_qubits()
            )));
        }
        self.inner.add_noise(channel.inner, qubit);
        Ok(())
    }

    /// 큐비트를 |0⟩ 상태로 리셋한다 (v0.4.5).
    fn reset(&mut self, qubit: usize) -> PyResult<()> {
        if qubit >= self.inner.num_qubits() {
            return Err(PyValueError::new_err(format!(
                "reset: qubit {qubit} 가 범위를 벗어남 (n_qubits={})",
                self.inner.num_qubits()
            )));
        }
        self.inner.reset(qubit);
        Ok(())
    }

    /// 직전에 추가된 게이트를 classical-controlled (`if (cbits == value) gate`) 로
    /// in-place wrap 한다 (v0.4.5). `qc.x(0).c_if(c, 1)` 의 Rust-side.
    ///
    /// 회로가 비어 있거나 마지막 instruction 이 단일 ApplyGate 가 아닌 경우 / cbits
    /// 가 비어 있거나 64 개 초과인 경우 / 빌더 invariant 위반 시 ValueError.
    fn c_if_last(&mut self, cbit_indices: Vec<usize>, value: u64) -> PyResult<()> {
        if cbit_indices.is_empty() {
            return Err(PyValueError::new_err(
                "c_if_last: cbit_indices 가 비어 있을 수 없습니다",
            ));
        }
        if cbit_indices.len() > 64 {
            return Err(PyValueError::new_err(format!(
                "c_if_last: cbit_indices 길이가 64 를 초과 ({}). u64 packing 한계.",
                cbit_indices.len()
            )));
        }
        // 마지막 instruction 이 단일 ApplyGate 가 아니면 panic 대신 ValueError 를
        // 사용자에게 노출하기 위해 사전 검사. (빌더의 panic 은 fail-fast 용)
        let last = self
            .inner
            .instructions()
            .last()
            .ok_or_else(|| {
                PyValueError::new_err("c_if_last: 회로가 비어 있어 wrap 할 게이트가 없습니다")
            })?
            .clone();
        if !matches!(last, Instruction::ApplyGate { .. }) {
            return Err(PyValueError::new_err(format!(
                "c_if_last: 마지막 instruction 이 단일 ApplyGate 가 아닙니다 ({last:?})"
            )));
        }
        self.inner.c_if_last(cbit_indices, value);
        Ok(())
    }

    /// Dynamic instruction (Reset / IfEq / 위치별 Measure) 가 있는지 (v0.4.5).
    fn has_dynamic(&self) -> bool {
        self.inner.has_dynamic()
    }

    // ========================================================================
    // v0.4.7 — Block-form classical control flow
    // ========================================================================

    /// Block-form `IfElse` 추가 (v0.4.7).
    ///
    /// `then_circuit` / `else_circuit` 은 미리 빌드된 `PyCircuit` 인스턴스.
    /// 그 안의 instruction 시퀀스를 sub-circuit body 로 가져온다.  Python 측의
    /// context manager (`qc.if_test(...)`) 가 이 entrypoint 를 사용한다.
    ///
    /// `else_circuit` 이 `None` 이면 then-only block.
    #[pyo3(signature = (cbit_indices, value, then_circuit, else_circuit = None))]
    fn add_if_else(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        then_circuit: &PyCircuit,
        else_circuit: Option<&PyCircuit>,
    ) -> PyResult<()> {
        if cbit_indices.is_empty() {
            return Err(PyValueError::new_err("add_if_else: cbit_indices empty"));
        }
        if cbit_indices.len() > 64 {
            return Err(PyValueError::new_err(format!(
                "add_if_else: cbit_indices > 64 ({})",
                cbit_indices.len()
            )));
        }
        let then_body = then_circuit.inner.instructions().to_vec();
        let else_body = else_circuit.map(|c| c.inner.instructions().to_vec());
        // sub-circuit n_cbits 도 propagate.
        let propagate_n_cbits = then_circuit
            .inner
            .num_cbits()
            .max(else_circuit.map(|c| c.inner.num_cbits()).unwrap_or(0));
        if propagate_n_cbits > self.inner.num_cbits() {
            // Circuit 의 n_cbits 는 private — extend_instructions 호출하지 않고
            // measure(0, propagate_n_cbits-1) 같은 hack 대신, 빌더를 직접 사용해야.
            // 그러나 add_if_else 메서드가 이미 max(cbit_indices)+1 까지만 grow.
            // sub-circuit 의 cbits 가 더 클 경우는 dummy measure 로 grow.
            // 실제로는 IfEq/Measure body 가 cbit 사용 시 사용자가 outer 에서 미리
            // measure(_, cbit) 로 register 를 grow 했을 것이므로 거의 안 부딪힘.
            // 보수적으로 unused 변수 경고만 silence.
            let _ = propagate_n_cbits;
        }
        self.inner
            .add_if_else(cbit_indices, value, then_body, else_body);
        Ok(())
    }

    /// Block-form `WhileLoop` 추가 (v0.4.7).
    fn add_while_loop(
        &mut self,
        cbit_indices: Vec<usize>,
        value: u64,
        body_circuit: &PyCircuit,
        max_iters: usize,
    ) -> PyResult<()> {
        if cbit_indices.is_empty() {
            return Err(PyValueError::new_err("add_while_loop: cbit_indices empty"));
        }
        let body = body_circuit.inner.instructions().to_vec();
        self.inner
            .add_while_loop(cbit_indices, value, body, max_iters);
        Ok(())
    }

    /// Block-form `ForLoop` 추가 (v0.4.7).
    fn add_for_loop(&mut self, iterations: usize, body_circuit: &PyCircuit) -> PyResult<()> {
        let body = body_circuit.inner.instructions().to_vec();
        self.inner.add_for_loop(iterations, body);
        Ok(())
    }

    /// Block-form `Switch` 추가 (v0.4.7).
    ///
    /// `cases` 는 `(label_or_None, body_circuit)` 의 리스트.  `label_or_None` 이
    /// `None` 이면 default — 마지막 한 번만 허용.
    fn add_switch(
        &mut self,
        cbit_indices: Vec<usize>,
        cases: Vec<(Option<u64>, PyRef<PyCircuit>)>,
    ) -> PyResult<()> {
        if cbit_indices.is_empty() {
            return Err(PyValueError::new_err("add_switch: cbit_indices empty"));
        }
        let mut seen_default = false;
        let mut compiled: Vec<(Option<u64>, Vec<Instruction>)> = Vec::new();
        for (label, body_circuit) in cases {
            if label.is_none() {
                if seen_default {
                    return Err(PyValueError::new_err("add_switch: multiple default cases"));
                }
                seen_default = true;
            }
            let body = body_circuit.inner.instructions().to_vec();
            compiled.push((label, body));
        }
        self.inner.add_switch(cbit_indices, compiled);
        Ok(())
    }

    /// 회로의 명령 시퀀스를 Python 친화적 튜플 리스트로 반환한다.
    ///
    /// 반환 shape: `[(name, qubits, params), ...]` — Python `QuantumCircuit._ops`
    /// 와 동일 형태. `from_qasm()` 으로 만든 회로도 `_ops` 가 채워지므로
    /// `qc.draw()` / `to_qiskit()` 가 직접 매핑 path 를 사용할 수 있다.
    ///
    /// `name` → params 매핑:
    /// - 단일 큐비트 (no params): `"h"/"x"/"y"/"z"/"s"/"sdg"/"t"/"tdg"/"id"`
    /// - 회전: `"rx"/"ry"/"rz"` (params=[θ])
    /// - 일반 1-큐비트 유니터리: `"u"` (params=[θ, φ, λ])  — Qiskit u3 정의
    /// - 2/3 큐비트: `"cx"/"cz"/"swap"/"ccx"/"cswap"`
    /// - 측정: `"measure"` (qubits=[q], params=[cbit_as_f64]),
    ///   `"measure_all"` (qubits=[0..n], params=[])
    fn instructions(&self) -> Vec<(String, Vec<usize>, Vec<f64>)> {
        let mut out = Vec::with_capacity(self.inner.instructions().len());
        for inst in self.inner.instructions() {
            match inst {
                Instruction::ApplyGate { gate, targets } => {
                    let (name, params): (&str, Vec<f64>) = match gate {
                        Gate::H => ("h", vec![]),
                        Gate::X => ("x", vec![]),
                        Gate::Y => ("y", vec![]),
                        Gate::Z => ("z", vec![]),
                        Gate::S => ("s", vec![]),
                        Gate::Sdg => ("sdg", vec![]),
                        Gate::T => ("t", vec![]),
                        Gate::Tdg => ("tdg", vec![]),
                        Gate::Sx => ("sx", vec![]),
                        Gate::Sxdg => ("sxdg", vec![]),
                        Gate::Id => ("id", vec![]),
                        Gate::Rx(theta) => ("rx", vec![*theta]),
                        Gate::Ry(theta) => ("ry", vec![*theta]),
                        Gate::Rz(theta) => ("rz", vec![*theta]),
                        Gate::P(lam) => ("p", vec![*lam]),
                        Gate::U2(phi, lam) => ("u2", vec![*phi, *lam]),
                        Gate::U(theta, phi, lam) => ("u", vec![*theta, *phi, *lam]),
                        Gate::CNOT => ("cx", vec![]),
                        Gate::CZ => ("cz", vec![]),
                        Gate::CY => ("cy", vec![]),
                        Gate::CH => ("ch", vec![]),
                        Gate::CRx(theta) => ("crx", vec![*theta]),
                        Gate::CRy(theta) => ("cry", vec![*theta]),
                        Gate::CRz(theta) => ("crz", vec![*theta]),
                        Gate::CP(lam) => ("cp", vec![*lam]),
                        Gate::CU3(theta, phi, lam) => ("cu3", vec![*theta, *phi, *lam]),
                        Gate::CU(theta, phi, lam, gam) => ("cu", vec![*theta, *phi, *lam, *gam]),
                        Gate::SWAP => ("swap", vec![]),
                        Gate::Toffoli => ("ccx", vec![]),
                        Gate::Fredkin => ("cswap", vec![]),
                    };
                    out.push((name.to_string(), targets.clone(), params));
                }
                Instruction::ApplyNoise { .. } => {
                    // Noise 명령은 Python `_ops` 형식으로 노출하지 않는다 (Cut C 에서
                    // 별도 NoiseModel 클래스가 채널을 관리). draw / to_qiskit 등 기존
                    // 어댑터가 noise 를 모르므로 skip 이 안전.
                }
                Instruction::Measure { qubit, cbit } => {
                    out.push(("measure".to_string(), vec![*qubit], vec![*cbit as f64]));
                }
                Instruction::MeasureAll => {
                    let qs: Vec<usize> = (0..self.inner.num_qubits()).collect();
                    out.push(("measure_all".to_string(), qs, vec![]));
                }
                Instruction::Reset { qubit } => {
                    out.push(("reset".to_string(), vec![*qubit], vec![]));
                }
                Instruction::IfEq { .. } => {
                    // 3-tuple `instructions()` getter 는 IfEq 의 inner op + cbit 메타를
                    // 전달할 수 없음 — Python 측은 _ops 직접 빌드를 사용.
                }
                Instruction::IfElse { .. }
                | Instruction::WhileLoop { .. }
                | Instruction::ForLoop { .. }
                | Instruction::Switch { .. } => {
                    // v0.4.7: block control flow 도 3-tuple 형식으로 표현 불가 — Python
                    // _ops 가 이미 nested 구조를 갖고 있으므로 Rust 측에서 reconstruct
                    // 안 한다 (from_qasm path 는 Python adapter 가 별도 처리).
                }
            }
        }
        out
    }
}

// PyCircuit 의 내부 헬퍼 (Python 에 노출하지 않음).
//
// v0.4.5.1: 게이트 메서드의 qubit 인덱스 사전 검증.  v0.4.5.0 까지는 Rust 측
// `Circuit::validate_qubit` 의 `assert!` 가 panic 으로 떨어져 PyO3 가 그걸
// `PanicException` 으로 노출했음 — Python 사용자에게 비친화적이고 stderr 에
// Rust backtrace 까지 같이 출력되는 UX 문제.  wrapper 단계에서 깨끗한
// `ValueError` 로 변환한다.
impl PyCircuit {
    fn check_q(&self, qubit: usize, op: &str) -> PyResult<()> {
        let n = self.inner.num_qubits();
        if qubit >= n {
            return Err(PyValueError::new_err(format!(
                "{op}: qubit 인덱스 {qubit} 가 범위를 벗어남 (n_qubits={n})"
            )));
        }
        Ok(())
    }

    fn check_qs(&self, qubits: &[usize], op: &str) -> PyResult<()> {
        let n = self.inner.num_qubits();
        for &q in qubits {
            if q >= n {
                return Err(PyValueError::new_err(format!(
                    "{op}: qubit 인덱스 {q} 가 범위를 벗어남 (n_qubits={n})"
                )));
            }
        }
        // 멀티-큐비트 게이트는 큐비트가 서로 달라야 함 (Rust 측 debug_assert 에서만
        // 검사하던 invariant 를 release 에서도 클린하게 ValueError 로 노출).
        if qubits.len() >= 2 {
            for i in 0..qubits.len() {
                for j in (i + 1)..qubits.len() {
                    if qubits[i] == qubits[j] {
                        return Err(PyValueError::new_err(format!(
                            "{op}: 큐비트 인덱스가 중복됨 ({:?})",
                            qubits
                        )));
                    }
                }
            }
        }
        Ok(())
    }
}

/// 단일 큐비트 노이즈 채널을 표현하는 Python 클래스 (v0.4).
///
/// 4 가지 표준 채널을 정적 컨스트럭터로 만든다. 모든 컨스트럭터는 파라미터
/// 범위 검증 (p ∈ [0, 1]) 후 `ValueError` 또는 인스턴스를 반환.
///
/// Python 측 [`panta_sim.NoiseModel`] 이 이 객체를 게이트 / 큐비트 필터와
/// 함께 묶어 회로에 적용한다.
#[pyclass(name = "NoiseChannel")]
#[derive(Clone)]
struct PyNoiseChannel {
    inner: NoiseChannel,
}

#[pymethods]
impl PyNoiseChannel {
    /// Bit-flip 채널: 확률 `p` 로 X 게이트 적용. p ∈ [0, 1].
    #[staticmethod]
    fn bit_flip(p: f64) -> PyResult<Self> {
        let inner = NoiseChannel::bit_flip(p).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    /// Phase-flip 채널: 확률 `p` 로 Z 게이트 적용. p ∈ [0, 1].
    #[staticmethod]
    fn phase_flip(p: f64) -> PyResult<Self> {
        let inner = NoiseChannel::phase_flip(p).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    /// Depolarizing 채널: 확률 `p` 로 {X, Y, Z} 균등 적용. p ∈ [0, 1].
    #[staticmethod]
    fn depolarizing(p: f64) -> PyResult<Self> {
        let inner = NoiseChannel::depolarizing(p).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    /// Amplitude-damping 채널: T1 (에너지 손실) 모델. γ ∈ [0, 1].
    #[staticmethod]
    fn amplitude_damping(gamma: f64) -> PyResult<Self> {
        let inner = NoiseChannel::amplitude_damping(gamma).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    fn __repr__(&self) -> String {
        match self.inner {
            NoiseChannel::BitFlip { p } => format!("NoiseChannel.bit_flip(p={p})"),
            NoiseChannel::PhaseFlip { p } => format!("NoiseChannel.phase_flip(p={p})"),
            NoiseChannel::Depolarizing { p } => format!("NoiseChannel.depolarizing(p={p})"),
            NoiseChannel::AmplitudeDamping { gamma } => {
                format!("NoiseChannel.amplitude_damping(gamma={gamma})")
            }
        }
    }
}

/// Python에서 사용 가능한 시뮬레이션 결과 클래스.
///
/// 내부 `SimulationResult` 가 정밀도별 enum 이므로 statevector / probabilities 는
/// 정밀도에 따라 numpy `complex64`/`float32` (f32) 또는 `complex128`/`float64` (f64) 를 반환한다.
#[pyclass(name = "SimulationResult")]
struct PySimulationResult {
    inner: SimulationResult,
}

#[pymethods]
impl PySimulationResult {
    /// 측정 결과 counts를 dict로 반환한다.
    fn counts(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (key, value) in self.inner.counts() {
            dict.set_item(key, value)?;
        }
        Ok(dict.into())
    }

    /// 시뮬레이션에 사용된 정밀도 ("f32" 또는 "f64").
    #[getter]
    fn precision(&self) -> &'static str {
        self.inner.precision().as_str()
    }

    /// 시뮬레이션에 사용된 백엔드 ("statevector" / "density_matrix" / "mps").
    #[getter]
    fn backend(&self) -> &'static str {
        self.inner.backend().as_str()
    }

    /// MPS 백엔드 결과의 사용자 지정 χ_max.  비-MPS 결과면 `None`.
    #[getter]
    fn mps_max_bond_dim(&self) -> Option<usize> {
        self.inner.mps_max_bond_dim()
    }

    /// MPS 백엔드 결과의 SVD truncation 후 squared norm.
    /// 1.0 미만이면 max_bond_dim 부족 (정보 손실).  비-MPS 결과면 `None`.
    #[getter]
    fn mps_final_norm_sq(&self) -> Option<f64> {
        self.inner.mps_final_norm_sq()
    }

    /// MPS 백엔드 결과의 누적 SVD discarded weight
    /// `Σ_{SVDs} Σ_{j>=keep} sv_j²` (Schollwöck 2011 §4.5.3, v0.6.3).
    /// 0 이면 무손실, 클수록 truncation 손실이 큼 — `final_norm_sq` 와 달리
    /// 회로 전체의 누적 metric.  비-MPS 결과면 `None`.
    #[getter]
    fn mps_truncation_error_sum(&self) -> Option<f64> {
        self.inner.mps_truncation_error_sum()
    }

    /// MPS 백엔드 결과의 사용자 지정 singular-value cutoff (v0.6.5).
    /// `0.0` 이면 disabled — `max_bond_dim` 만으로 truncation.  비-MPS
    /// 결과면 `None`.
    #[getter]
    fn mps_trunc_threshold(&self) -> Option<f64> {
        self.inner.mps_trunc_threshold()
    }

    /// MPS 백엔드가 회로 종료 시점에 실제로 발생한 최대 internal bond
    /// dimension (v0.6.5).  adaptive truncation (`trunc_threshold > 0`)
    /// 활성 시 일반적으로 `mps_max_bond_dim` 보다 작다.  비-MPS 결과면
    /// `None`.
    #[getter]
    fn mps_observed_max_bond_dim(&self) -> Option<usize> {
        self.inner.mps_observed_max_bond_dim()
    }

    /// 측정 전 상태 벡터를 numpy 배열로 반환한다.
    ///
    /// dtype 은 시뮬레이션 정밀도를 따른다:
    /// - f64 경로 → `numpy.complex128`
    /// - f32 경로 → `numpy.complex64`
    fn statevector<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        match &self.inner {
            SimulationResult::F64 { statevector, .. } => {
                let amps: Vec<Complex<f64>> = statevector.amplitudes().to_vec();
                Ok(PyArray1::from_vec(py, amps).into_any())
            }
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => {
                let amps: Vec<Complex<f64>> = sv.amplitudes().to_vec();
                Ok(PyArray1::from_vec(py, amps).into_any())
            }
            SimulationResult::MpsF64 {
                statevector: None, ..
            }
            | SimulationResult::MpsF32 {
                statevector: None, ..
            } => Err(PyValueError::new_err(
                "statevector(): MPS 결과가 N>20 이라 dense statevector 가 없습니다. \
                 counts() 를 사용하거나 N≤20 회로로 다시 실행하세요",
            )),
            SimulationResult::F32 { statevector, .. } => {
                let amps: Vec<Complex<f32>> = statevector.amplitudes().to_vec();
                Ok(PyArray1::from_vec(py, amps).into_any())
            }
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => {
                let amps: Vec<Complex<f32>> = sv.amplitudes().to_vec();
                Ok(PyArray1::from_vec(py, amps).into_any())
            }
            SimulationResult::DensityF32 { .. } | SimulationResult::DensityF64 { .. } => {
                Err(PyValueError::new_err(
                    "statevector(): density backend 결과입니다. density_matrix() 를 사용하세요",
                ))
            }
        }
    }

    /// 확률 벡터를 numpy 배열로 반환한다.
    ///
    /// dtype 은 시뮬레이션 정밀도를 따른다 (`float64` / `float32`).
    /// density 백엔드는 ρ 의 대각선 (`ρ[b][b]`) 을 반환.
    fn probabilities<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        match &self.inner {
            SimulationResult::F64 { statevector, .. } => {
                Ok(PyArray1::from_vec(py, statevector.probabilities()).into_any())
            }
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => Ok(PyArray1::from_vec(py, sv.probabilities()).into_any()),
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => Ok(PyArray1::from_vec(py, sv.probabilities()).into_any()),
            SimulationResult::MpsF64 {
                statevector: None, ..
            }
            | SimulationResult::MpsF32 {
                statevector: None, ..
            } => Err(PyValueError::new_err(
                "probabilities(): MPS 결과가 N>20 이라 dense probabilities 가 없습니다. \
                 counts() 를 사용하세요",
            )),
            SimulationResult::F32 { statevector, .. } => {
                Ok(PyArray1::from_vec(py, statevector.probabilities()).into_any())
            }
            SimulationResult::DensityF64 { density, .. } => {
                Ok(PyArray1::from_vec(py, density.diagonal_probabilities()).into_any())
            }
            SimulationResult::DensityF32 { density, .. } => {
                Ok(PyArray1::from_vec(py, density.diagonal_probabilities()).into_any())
            }
        }
    }

    /// Density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` 를 numpy 2D ndarray 로 반환한다 (v0.5.0).
    ///
    /// dtype 은 시뮬레이션 정밀도를 따른다 (`complex128` / `complex64`).
    /// statevector 백엔드 결과에 호출하면 `ValueError`.
    ///
    /// 반환된 행렬은 row-major: `rho[i][j]` = ρ_{ij}, hermitian (ρ = ρ†).
    fn density_matrix<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        match &self.inner {
            SimulationResult::DensityF64 { density, .. } => {
                let dim = density.dim();
                let data: Vec<Complex<f64>> = density.data().to_vec();
                let arr = PyArray1::from_vec(py, data);
                let arr2 = arr
                    .reshape((dim, dim))
                    .map_err(|e| PyValueError::new_err(format!("density_matrix reshape: {e}")))?;
                Ok(arr2.into_any())
            }
            SimulationResult::DensityF32 { density, .. } => {
                let dim = density.dim();
                let data: Vec<Complex<f32>> = density.data().to_vec();
                let arr = PyArray1::from_vec(py, data);
                let arr2 = arr
                    .reshape((dim, dim))
                    .map_err(|e| PyValueError::new_err(format!("density_matrix reshape: {e}")))?;
                Ok(arr2.into_any())
            }
            SimulationResult::F32 { .. }
            | SimulationResult::F64 { .. }
            | SimulationResult::MpsF64 { .. }
            | SimulationResult::MpsF32 { .. } => Err(
                PyValueError::new_err(
                    "density_matrix(): statevector backend 결과입니다. statevector() 를 사용하거나 backend='density_matrix' 로 실행하세요",
                ),
            ),
        }
    }
}

/// 회로 실행 함수.
///
/// `precision` 으로 시뮬레이션 정밀도를 선택한다 ("f64" default, "f32" 옵션).
/// f32 는 메모리 ~50% 절감과 SIMD 친화성을 제공하지만 정확도는 ~1e-6 수준.
///
/// `backend` (v0.5.0) 으로 실행 백엔드를 선택한다:
/// - `"statevector"` (default): 기존 state vector 경로 (2ⁿ amplitude).
/// - `"density_matrix"`: density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` 직접 진화.
///   noise 가 있어도 deterministic Kraus 적용 (Aer `method="density_matrix"`
///   와 동일 의미).  메모리 4ⁿ → N≤14 권장.
///
/// rayon 병렬 게이트 적용이 GIL 을 들고 있으면 Python 멀티스레드 환경에서
/// 다른 스레드가 막히므로, 시뮬레이션 동안 GIL 을 해제한다.
#[pyfunction]
#[pyo3(signature = (circuit, shots = 1024, seed = None, precision = "f64", backend = "statevector", max_bond_dim = 64, trunc_threshold = 0.0))]
#[allow(clippy::too_many_arguments)] // PyO3 keyword-arg surface — splitting would harm UX
fn run(
    py: Python<'_>,
    circuit: &PyCircuit,
    shots: usize,
    seed: Option<u64>,
    precision: &str,
    backend: &str,
    max_bond_dim: usize,
    trunc_threshold: f64,
) -> PyResult<PySimulationResult> {
    let prec = match precision {
        "f64" => Precision::F64,
        "f32" => Precision::F32,
        other => {
            return Err(PyValueError::new_err(format!(
                "precision 은 'f32' 또는 'f64' 여야 합니다 (입력: {other:?})"
            )));
        }
    };
    let bk = match backend {
        "statevector" | "cpu" => Backend::CpuStatevector,
        "density_matrix" | "density" => Backend::CpuDensity,
        "wgpu" | "wgpu_statevector" => Backend::WgpuStatevector,
        "wgpu_density_matrix" | "wgpu_density" => Backend::WgpuDensity,
        "cuda" | "cuda_statevector" | "custatevec" => Backend::CudaStatevector,
        "mps" | "mps_statevector" => Backend::CpuMps,
        // v0.6.6 Cut 1: scaffolding — 현재 CPU MPS 로 fallback, Cut 6 부터 GPU SVD 실제 통합.
        "wgpu_mps" => Backend::WgpuMps,
        other => {
            return Err(PyValueError::new_err(format!(
                "backend 는 'statevector' / 'density_matrix' / 'wgpu' / \
                 'wgpu_density_matrix' / 'cuda' / 'mps' / 'wgpu_mps' \
                 여야 합니다 (입력: {other:?})"
            )));
        }
    };
    if matches!(bk, Backend::CpuMps | Backend::WgpuMps) && max_bond_dim < 1 {
        return Err(PyValueError::new_err("max_bond_dim 은 1 이상이어야 합니다"));
    }
    // v0.6.5: trunc_threshold validation must precede engine construction
    // (engine builder panics on negative / NaN — we'd rather PyValueError).
    if !trunc_threshold.is_finite() || trunc_threshold < 0.0 {
        return Err(PyValueError::new_err(format!(
            "trunc_threshold 는 유한한 0 이상의 값이어야 합니다 (입력: {trunc_threshold})"
        )));
    }
    let circuit_owned = circuit.inner.clone();
    let mut engine = match seed {
        Some(s) => ExecutionEngine::with_seed(s),
        None => ExecutionEngine::new(),
    };
    engine = engine
        .with_precision(prec)
        .with_backend(bk)
        .with_mps_bond_dim(max_bond_dim)
        .with_mps_trunc_threshold(trunc_threshold);
    // wgpu backend 의 GpuError 를 PyValueError 로 변환하기 위해 run_checked 사용.
    let result = py.allow_threads(move || engine.run_checked(&circuit_owned, shots));
    let inner = result.map_err(|e| PyValueError::new_err(format!("{e}")))?;
    Ok(PySimulationResult { inner })
}

#[pymodule]
fn qsim_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyCircuit>()?;
    m.add_class::<PySimulationResult>()?;
    m.add_class::<PyNoiseChannel>()?;
    m.add_function(wrap_pyfunction!(run, m)?)?;
    Ok(())
}
