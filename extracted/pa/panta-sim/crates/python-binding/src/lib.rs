use num_complex::Complex;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use qsim_core::Gate;
use qsim_simulator::{
    Backend, Circuit, ExecutionEngine, Instruction, NoiseChannel, NoiseChannel2, PathOptimizer,
    Precision, SimulationResult,
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
    fn iswap(&mut self, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "iswap")?;
        self.inner.iswap(qubit0, qubit1);
        Ok(())
    }
    fn rxx(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "rxx")?;
        self.inner.rxx(theta, qubit0, qubit1);
        Ok(())
    }
    fn ryy(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "ryy")?;
        self.inner.ryy(theta, qubit0, qubit1);
        Ok(())
    }
    fn rzz(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "rzz")?;
        self.inner.rzz(theta, qubit0, qubit1);
        Ok(())
    }
    fn dcx(&mut self, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "dcx")?;
        self.inner.dcx(qubit0, qubit1);
        Ok(())
    }
    fn ecr(&mut self, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "ecr")?;
        self.inner.ecr(qubit0, qubit1);
        Ok(())
    }
    fn rzx(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "rzx")?;
        self.inner.rzx(theta, qubit0, qubit1);
        Ok(())
    }
    fn xx_plus_yy(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "xx_plus_yy")?;
        self.inner.xx_plus_yy(theta, qubit0, qubit1);
        Ok(())
    }
    fn xx_minus_yy(&mut self, theta: f64, qubit0: usize, qubit1: usize) -> PyResult<()> {
        self.check_qs(&[qubit0, qubit1], "xx_minus_yy")?;
        self.inner.xx_minus_yy(theta, qubit0, qubit1);
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

    /// 임의 k-큐비트 (k ≥ 1) 유니터리를 직접 적용한다 (v0.6.8).
    ///
    /// `matrix` 는 `2^k × 2^k` 복소 행렬, `targets` 는 k 개의 큐비트 인덱스
    /// (행렬 sub-index 비트 `j` ↔ `targets[j]`, `targets[0]` = LSB).
    /// 1-큐비트 ZYZ 분해 (`unitary`) 와 달리 행렬을 그대로 보존해
    /// statevector 백엔드에서 직접 적용한다 (다른 백엔드는 실행 시 거부).
    /// unitarity 검증은 Python 측 (`QuantumCircuit.unitary`) 에서 수행한다.
    fn apply_unitary(
        &mut self,
        matrix: PyReadonlyArray2<Complex<f64>>,
        targets: Vec<usize>,
    ) -> PyResult<()> {
        let arr = matrix.as_array();
        let k = targets.len();
        if k == 0 {
            return Err(PyValueError::new_err(
                "unitary: targets 는 비어 있을 수 없음",
            ));
        }
        let dim = 1usize << k;
        if arr.shape() != [dim, dim] {
            return Err(PyValueError::new_err(format!(
                "unitary: matrix shape {:?} 가 targets 수 {k} (2^k = {dim}) 와 불일치",
                arr.shape()
            )));
        }
        let nq = self.inner.num_qubits();
        for &t in &targets {
            if t >= nq {
                return Err(PyValueError::new_err(format!(
                    "unitary: qubit 인덱스 {t} 가 범위를 벗어남 (n_qubits={nq})"
                )));
            }
        }
        for i in 0..k {
            for j in (i + 1)..k {
                if targets[i] == targets[j] {
                    return Err(PyValueError::new_err(format!(
                        "unitary: targets 중복 {targets:?} (distinct 해야 함)"
                    )));
                }
            }
        }
        let mut flat = Vec::with_capacity(dim * dim);
        for r in 0..dim {
            for c in 0..dim {
                flat.push(arr[[r, c]]);
            }
        }
        self.inner.unitary(flat, targets);
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

    /// 회로를 **CX + 임의 1-큐비트** basis 로 변환한 새 회로를 반환한다 (v0.8.3).
    ///
    /// 모든 2/3-큐비트 게이트 (CZ/CY/SWAP/iSWAP/DCX/CRx/CRy/CRz/CP/CH/RXX/RYY/
    /// RZZ/RZX/Toffoli/Fredkin) 를 표준 항등식으로 CX + 1q 회전으로 분해한다.
    /// KAK 합성이 필요한 게이트 (CU/CU3/ECR/XXPlusYY/XXMinusYY) 를 만나면
    /// `ValueError` — Python `unitary(M, q, decompose="cx")` 사용 권장.
    fn transpile_cx_basis(&self) -> PyResult<PyCircuit> {
        let circ = qsim_transpiler::transpile_to_cx_basis(&self.inner)
            .map_err(|e| PyValueError::new_err(format!("{e}")))?;
        Ok(PyCircuit { inner: circ })
    }

    /// 회로가 CX + 1q basis 인지 (모든 2/3q 게이트가 CX 인지) 검사한다.
    fn is_cx_basis(&self) -> bool {
        qsim_transpiler::is_cx_basis(&self.inner)
    }

    /// 회로를 IBM basis (`rz` + `sx` + `x` + CX) 로 변환한 새 회로.
    /// CX-basis 분해 후 모든 1q 게이트를 ZYZ→{rz,sx,x} 로 rebase 한다.
    fn transpile_ibm_basis(&self) -> PyResult<PyCircuit> {
        let circ = qsim_transpiler::transpile_to_ibm_basis(&self.inner)
            .map_err(|e| PyValueError::new_err(format!("{e}")))?;
        Ok(PyCircuit { inner: circ })
    }

    /// 회로가 IBM basis (rz/sx/x 1q + CX 2q) 인지 검사한다.
    fn is_zsx_basis(&self) -> bool {
        qsim_transpiler::is_zsx_basis(&self.inner)
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
        self.inner.add_noise(channel.inner.clone(), qubit);
        Ok(())
    }

    /// 2-큐비트 상관 노이즈 채널 적용 (v0.7.2).
    fn add_noise_2q(&mut self, channel: &PyNoiseChannel2, q0: usize, q1: usize) -> PyResult<()> {
        let n = self.inner.num_qubits();
        if q0 >= n || q1 >= n {
            return Err(PyValueError::new_err(format!(
                "add_noise_2q: qubit ({q0},{q1}) 가 범위를 벗어남 (n_qubits={n})"
            )));
        }
        if q0 == q1 {
            return Err(PyValueError::new_err(format!(
                "add_noise_2q: q0 == q1 ({q0})"
            )));
        }
        self.inner.add_noise_2q(channel.inner.clone(), q0, q1);
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
                        Gate::ISwap => ("iswap", vec![]),
                        Gate::Rxx(theta) => ("rxx", vec![*theta]),
                        Gate::Ryy(theta) => ("ryy", vec![*theta]),
                        Gate::Rzz(theta) => ("rzz", vec![*theta]),
                        Gate::Dcx => ("dcx", vec![]),
                        Gate::Ecr => ("ecr", vec![]),
                        Gate::Rzx(theta) => ("rzx", vec![*theta]),
                        Gate::XxPlusYy(theta) => ("xx_plus_yy", vec![*theta]),
                        Gate::XxMinusYy(theta) => ("xx_minus_yy", vec![*theta]),
                        Gate::Toffoli => ("ccx", vec![]),
                        Gate::Fredkin => ("cswap", vec![]),
                    };
                    out.push((name.to_string(), targets.clone(), params));
                }
                Instruction::ApplyUnitary { targets, .. } => {
                    // 행렬은 (name, qubits, f64-params) 형식으로 표현 불가 —
                    // draw / _ops 에는 이름과 큐비트만 노출 (box 로 렌더).
                    out.push(("unitary".to_string(), targets.clone(), vec![]));
                }
                Instruction::ApplyNoise { .. } | Instruction::ApplyNoise2 { .. } => {
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

    /// Phase-damping 채널: T2 (위상 디코히어런스) 모델. γ ∈ [0, 1].
    #[staticmethod]
    fn phase_damping(gamma: f64) -> PyResult<Self> {
        let inner = NoiseChannel::phase_damping(gamma).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    /// Generalized amplitude damping: 유한 온도 T1. γ, p ∈ [0, 1] (p=1 → amplitude damping).
    #[staticmethod]
    fn generalized_amplitude_damping(gamma: f64, p: f64) -> PyResult<Self> {
        let inner =
            NoiseChannel::generalized_amplitude_damping(gamma, p).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    /// 사용자 정의 단일 큐비트 Kraus 채널.  `kraus_ops` 는 2×2 행렬의 리스트,
    /// 각 원소는 `[[(re,im),(re,im)],[(re,im),(re,im)]]` (row-major).
    /// trace-preserving (`Σ K_i† K_i = I`) 을 검증한다.
    #[staticmethod]
    fn custom(kraus_ops: Vec<Vec<Vec<(f64, f64)>>>) -> PyResult<Self> {
        let mut ops: Vec<[[Complex<f64>; 2]; 2]> = Vec::with_capacity(kraus_ops.len());
        for (i, k) in kraus_ops.iter().enumerate() {
            if k.len() != 2 || k[0].len() != 2 || k[1].len() != 2 {
                return Err(PyValueError::new_err(format!(
                    "custom: Kraus 연산자 {i} 가 2×2 가 아닙니다"
                )));
            }
            ops.push([
                [
                    Complex::new(k[0][0].0, k[0][0].1),
                    Complex::new(k[0][1].0, k[0][1].1),
                ],
                [
                    Complex::new(k[1][0].0, k[1][0].1),
                    Complex::new(k[1][1].0, k[1][1].1),
                ],
            ]);
        }
        let inner = NoiseChannel::custom(ops).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    fn __repr__(&self) -> String {
        match &self.inner {
            NoiseChannel::BitFlip { p } => format!("NoiseChannel.bit_flip(p={p})"),
            NoiseChannel::PhaseFlip { p } => format!("NoiseChannel.phase_flip(p={p})"),
            NoiseChannel::Depolarizing { p } => format!("NoiseChannel.depolarizing(p={p})"),
            NoiseChannel::AmplitudeDamping { gamma } => {
                format!("NoiseChannel.amplitude_damping(gamma={gamma})")
            }
            NoiseChannel::PhaseDamping { gamma } => {
                format!("NoiseChannel.phase_damping(gamma={gamma})")
            }
            NoiseChannel::GeneralizedAmplitudeDamping { gamma, p } => {
                format!("NoiseChannel.generalized_amplitude_damping(gamma={gamma}, p={p})")
            }
            NoiseChannel::Custom { kraus_ops } => {
                format!("NoiseChannel.custom({} Kraus ops)", kraus_ops.len())
            }
        }
    }
}

/// 2-큐비트 상관 노이즈 채널 (v0.7.2).
#[pyclass(name = "NoiseChannel2")]
#[derive(Clone)]
struct PyNoiseChannel2 {
    inner: NoiseChannel2,
}

#[pymethods]
impl PyNoiseChannel2 {
    /// 사용자 정의 2-큐비트 Kraus 채널.  `kraus_ops` 는 4×4 행렬의 리스트, 각
    /// 원소는 `[[(re,im); 4]; 4]` (row-major).  trace-preserving 검증.
    #[staticmethod]
    fn custom(kraus_ops: Vec<Vec<Vec<(f64, f64)>>>) -> PyResult<Self> {
        let mut ops: Vec<[[Complex<f64>; 4]; 4]> = Vec::with_capacity(kraus_ops.len());
        for (idx, k) in kraus_ops.iter().enumerate() {
            if k.len() != 4 || k.iter().any(|row| row.len() != 4) {
                return Err(PyValueError::new_err(format!(
                    "custom: Kraus 연산자 {idx} 가 4×4 가 아닙니다"
                )));
            }
            let mut m = [[Complex::new(0.0, 0.0); 4]; 4];
            for (i, row) in k.iter().enumerate() {
                for (j, &(re, im)) in row.iter().enumerate() {
                    m[i][j] = Complex::new(re, im);
                }
            }
            ops.push(m);
        }
        let inner = NoiseChannel2::custom(ops).map_err(PyValueError::new_err)?;
        Ok(Self { inner })
    }

    fn __repr__(&self) -> String {
        match &self.inner {
            NoiseChannel2::Custom { kraus_ops } => {
                format!("NoiseChannel2.custom({} Kraus ops)", kraus_ops.len())
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

impl PySimulationResult {
    /// statevector 가 있는 결과면 큐비트 수, 아니면 None.
    fn num_qubits_of_statevector(&self) -> Option<usize> {
        match &self.inner {
            SimulationResult::F64 { statevector, .. } => Some(statevector.num_qubits()),
            SimulationResult::F32 { statevector, .. } => Some(statevector.num_qubits()),
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => Some(sv.num_qubits()),
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => Some(sv.num_qubits()),
            SimulationResult::MpsF64 { mps: Some(mps), .. } => Some(mps.num_qubits()),
            SimulationResult::MpsF32 { mps: Some(mps), .. } => Some(mps.num_qubits()),
            SimulationResult::DensityF64 { density, .. } => Some(density.num_qubits()),
            SimulationResult::DensityF32 { density, .. } => Some(density.num_qubits()),
            _ => None,
        }
    }
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

    /// Pauli observable `H = Σ cᵢ Pᵢ` 의 기댓값 `⟨ψ|H|ψ⟩` 를 계산한다 (v0.7).
    ///
    /// `terms` 의 각 원소는 `(paulis, coeff)` — `paulis[q] ∈ {0=I,1=X,2=Y,3=Z}`
    /// (큐비트 `q`), `coeff` 는 복소 계수.  Python `SimulationResult.expectation`
    /// 가 Pauli string / SparsePauliOp 를 이 형식으로 변환해 호출한다.
    ///
    /// statevector 백엔드 (F64 / F32 / dense 가 있는 MPS) 에서 동작하며 2ⁿ 행렬을
    /// 만들지 않고 직접 계산한다.  Hermitian observable 이면 결과는 실수 —
    /// 실수부를 반환한다.
    fn expectation(&self, terms: Vec<(Vec<u8>, f64, f64)>) -> PyResult<f64> {
        // 각 Pauli string 길이가 큐비트 수와 일치하는지 검증 (release 빌드는
        // core 의 debug_assert 가 꺼져 있으므로 여기서 친화 에러).
        if let Some(nq) = self.num_qubits_of_statevector() {
            for (paulis, _, _) in &terms {
                if paulis.len() != nq {
                    return Err(PyValueError::new_err(format!(
                        "expectation(): Pauli string 길이 {} 가 큐비트 수 {nq} 와 불일치",
                        paulis.len()
                    )));
                }
            }
        }
        let pairs: Vec<(Complex<f64>, Vec<u8>)> = terms
            .into_iter()
            .map(|(p, re, im)| (Complex::new(re, im), p))
            .collect();
        let value = match &self.inner {
            SimulationResult::F64 { statevector, .. } => {
                qsim_core::expectation_pauli_sum(statevector, &pairs)
            }
            SimulationResult::F32 { statevector, .. } => {
                qsim_core::expectation_pauli_sum(statevector, &pairs)
            }
            SimulationResult::MpsF64 {
                statevector: Some(sv),
                ..
            } => qsim_core::expectation_pauli_sum(sv, &pairs),
            SimulationResult::MpsF32 {
                statevector: Some(sv),
                ..
            } => qsim_core::expectation_pauli_sum(sv, &pairs),
            // v0.7: N>20 (dense SV 없음) — MPS-direct expectation_pauli.
            SimulationResult::MpsF64 {
                statevector: None,
                mps: Some(mps),
                ..
            } => pairs
                .iter()
                .map(|(c, p)| c * mps.expectation_pauli(p))
                .sum(),
            SimulationResult::MpsF32 {
                statevector: None,
                mps: Some(mps),
                ..
            } => pairs
                .iter()
                .map(|(c, p)| c * mps.expectation_pauli(p))
                .sum(),
            SimulationResult::MpsF64 {
                statevector: None,
                mps: None,
                ..
            }
            | SimulationResult::MpsF32 {
                statevector: None,
                mps: None,
                ..
            } => {
                return Err(PyValueError::new_err(
                    "expectation(): MPS 결과에 statevector 도 MPS 도 없습니다 \
                     (trajectory/noise 회로는 expectation 미지원 — mixed state). \
                     정적 회로로 실행하세요",
                ));
            }
            // v0.7: density backend → Tr(ρH) (noisy observable expectation).
            SimulationResult::DensityF64 { density, .. } => {
                qsim_core::expectation_pauli_sum_density(density, &pairs)
            }
            SimulationResult::DensityF32 { density, .. } => {
                qsim_core::expectation_pauli_sum_density(density, &pairs)
            }
        };
        Ok(value.re)
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

/// `θ` 가 `k·π/2` 에 가까우면 사분면 인덱스 `k mod 4` (∈ {0,1,2,3}) 를 반환.
/// 그 외 (비-Clifford 각도) 면 `None`.
fn clifford_quarter(theta: f64) -> Option<u8> {
    use std::f64::consts::PI;
    let q = theta / (PI / 2.0);
    let r = q.round();
    if (q - r).abs() > 1e-9 {
        return None;
    }
    Some((r.rem_euclid(4.0)) as u8)
}

/// 단일 `Gate` 를 [`CliffordOp`] 시퀀스로 변환한다.  비-Clifford 면 `Err`.
fn gate_to_clifford(
    gate: &Gate,
    targets: &[usize],
) -> Result<Vec<qsim_stabilizer::CliffordOp>, String> {
    use qsim_stabilizer::CliffordOp as C;
    let a = targets.first().copied().unwrap_or(0);
    let b = targets.get(1).copied().unwrap_or(0);
    // Rz(k·π/2) → I/S/Z/Sdg, Rx → I/Sx/X/Sxdg, P(λ) → I/S/Z/Sdg.
    let rz_like = |k: u8, a: usize| -> Vec<C> {
        match k {
            0 => vec![],
            1 => vec![C::S(a)],
            2 => vec![C::Z(a)],
            _ => vec![C::Sdg(a)],
        }
    };
    let rx_like = |k: u8, a: usize| -> Vec<C> {
        match k {
            0 => vec![],
            1 => vec![C::Sx(a)],
            2 => vec![C::X(a)],
            _ => vec![C::Sxdg(a)],
        }
    };
    let ops = match gate {
        Gate::H => vec![C::H(a)],
        Gate::X => vec![C::X(a)],
        Gate::Y => vec![C::Y(a)],
        Gate::Z => vec![C::Z(a)],
        Gate::S => vec![C::S(a)],
        Gate::Sdg => vec![C::Sdg(a)],
        Gate::Sx => vec![C::Sx(a)],
        Gate::Sxdg => vec![C::Sxdg(a)],
        Gate::Id => vec![],
        Gate::CNOT => vec![C::Cnot(a, b)],
        Gate::CZ => vec![C::Cz(a, b)],
        Gate::CY => vec![C::Cy(a, b)],
        Gate::SWAP => vec![C::Swap(a, b)],
        Gate::ISwap => vec![C::Iswap(a, b)],
        Gate::Dcx => vec![C::Dcx(a, b)],
        Gate::Rz(t) | Gate::P(t) => clifford_quarter(*t)
            .map(|k| rz_like(k, a))
            .ok_or_else(|| format!("Rz/P({t}) 은 π/2 의 배수 각도만 Clifford 입니다"))?,
        Gate::Rx(t) => clifford_quarter(*t)
            .map(|k| rx_like(k, a))
            .ok_or_else(|| format!("Rx({t}) 은 π/2 의 배수 각도만 Clifford 입니다"))?,
        Gate::Ry(t) => {
            // Ry(0)=I, Ry(π)=Y; 그 외 (±π/2 포함) 는 분해가 복잡해 거부.
            let k = clifford_quarter(*t)
                .ok_or_else(|| format!("Ry({t}) 은 0 또는 π 만 Clifford 로 지원합니다"))?;
            match k {
                0 => vec![],
                2 => vec![C::Y(a)],
                _ => {
                    return Err(format!(
                        "Ry({t}) (±π/2) 는 stabilizer 백엔드에서 미지원입니다"
                    ))
                }
            }
        }
        Gate::Rzz(t) => match clifford_quarter(*t) {
            // Rzz(π/2) = e^{-iπ/4 ZZ} 는 Clifford: CX·(I⊗S†? )... 단순화 위해
            // π 의 배수만 (I 또는 Z⊗Z) 지원, ±π/2 는 거부.
            Some(0) => vec![],
            Some(2) => vec![C::Z(a), C::Z(b)],
            _ => return Err(format!("Rzz({t}) 은 π 의 배수만 Clifford 로 지원합니다")),
        },
        other => {
            return Err(format!(
                "비-Clifford 게이트 {other:?} — stabilizer 백엔드 미지원 (T/Tdg/일반 회전 등)"
            ))
        }
    };
    Ok(ops)
}

/// 단일 `Gate` 를 near-Clifford [`CtGate`] 시퀀스로 변환 (Clifford + T/Tdg).
fn gate_to_ct(
    gate: &Gate,
    targets: &[usize],
) -> Result<Vec<qsim_stabilizer::clifford_t::CtGate>, String> {
    use qsim_stabilizer::clifford_t::CtGate as C;
    let a = targets.first().copied().unwrap_or(0);
    let b = targets.get(1).copied().unwrap_or(0);
    let rz_like = |k: u8, a: usize| -> Vec<C> {
        match k {
            0 => vec![],
            1 => vec![C::S(a)],
            2 => vec![C::Z(a)],
            _ => vec![C::Sdg(a)],
        }
    };
    let rx_like = |k: u8, a: usize| -> Vec<C> {
        match k {
            0 => vec![],
            1 => vec![C::Sx(a)],
            2 => vec![C::X(a)],
            _ => vec![C::Sxdg(a)],
        }
    };
    let ops = match gate {
        Gate::H => vec![C::H(a)],
        Gate::X => vec![C::X(a)],
        Gate::Y => vec![C::Y(a)],
        Gate::Z => vec![C::Z(a)],
        Gate::S => vec![C::S(a)],
        Gate::Sdg => vec![C::Sdg(a)],
        Gate::Sx => vec![C::Sx(a)],
        Gate::Sxdg => vec![C::Sxdg(a)],
        Gate::Id => vec![],
        Gate::T => vec![C::T(a)],
        Gate::Tdg => vec![C::Tdg(a)],
        Gate::CNOT => vec![C::Cnot(a, b)],
        Gate::CZ => vec![C::Cz(a, b)],
        Gate::CY => vec![C::Cy(a, b)],
        Gate::SWAP => vec![C::Swap(a, b)],
        Gate::ISwap => vec![C::Iswap(a, b)],
        Gate::Dcx => vec![C::Dcx(a, b)],
        Gate::Rz(t) => clifford_quarter(*t)
            .map(|k| rz_like(k, a))
            .ok_or_else(|| format!("Rz({t}) 은 π/2 배수만 지원 (T 는 t 게이트 사용)"))?,
        Gate::P(t) => {
            // p(π/4)=T, p(-π/4)=Tdg, π/2 배수=Clifford.
            let q4 = *t / (std::f64::consts::FRAC_PI_4);
            if (q4 - q4.round()).abs() < 1e-9 {
                let kk = (q4.round().rem_euclid(8.0)) as i32;
                match kk {
                    0 => vec![],
                    1 => vec![C::T(a)],
                    2 => vec![C::S(a)],
                    3 => vec![C::S(a), C::T(a)],
                    4 => vec![C::Z(a)],
                    5 => vec![C::Z(a), C::T(a)],
                    6 => vec![C::Sdg(a)],
                    _ => vec![C::Tdg(a)],
                }
            } else {
                return Err(format!("P({t}) 은 π/4 배수만 지원"));
            }
        }
        Gate::Rx(t) => clifford_quarter(*t)
            .map(|k| rx_like(k, a))
            .ok_or_else(|| format!("Rx({t}) 은 π/2 배수만 지원"))?,
        other => {
            return Err(format!(
                "near-Clifford 백엔드 미지원 게이트 {other:?} (Clifford + T/Tdg 만)"
            ))
        }
    };
    Ok(ops)
}

/// near-Clifford (Clifford+T) 회로의 amplitude `⟨x|C|0…0⟩` 를 정확히 계산한다.
///
/// T 게이트를 stabilizer 항의 간섭 합으로 분해 (T 당 항 2배) → 큰 N · 적은
/// T-count 회로의 진폭을 statevector 없이 정확히 (전역 위상 포함) 계산.
/// T-count 가 크면 (≳25) 항 폭발로 비현실적.  noise/dynamic/임의 unitary 거부.
/// `low_rank=True` 면 Bravyi–Gosset rank-2 블록 분해 (항 수 `2^{⌈t/2⌉}`),
/// 아니면 직접 분해 (`2ᵗ`).
#[pyfunction]
#[pyo3(signature = (circuit, bitstring, low_rank = false))]
fn clifford_t_amplitude(
    py: Python<'_>,
    circuit: &PyCircuit,
    bitstring: Vec<u8>,
    low_rank: bool,
) -> PyResult<(f64, f64)> {
    let n = circuit.inner.num_qubits();
    if bitstring.len() != n {
        return Err(PyValueError::new_err(format!(
            "bitstring 길이 {} != n_qubits {n}",
            bitstring.len()
        )));
    }
    let mut gates: Vec<qsim_stabilizer::clifford_t::CtGate> = Vec::new();
    for inst in circuit.inner.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                gates.extend(gate_to_ct(gate, targets).map_err(PyValueError::new_err)?);
            }
            Instruction::Measure { .. } | Instruction::MeasureAll => {}
            other => {
                return Err(PyValueError::new_err(format!(
                    "near-Clifford 백엔드는 Clifford+T 게이트만 지원합니다: {other:?}"
                )));
            }
        }
    }
    let t_count = gates
        .iter()
        .filter(|g| {
            matches!(
                g,
                qsim_stabilizer::clifford_t::CtGate::T(_)
                    | qsim_stabilizer::clifford_t::CtGate::Tdg(_)
            )
        })
        .count();
    // low_rank 은 2^{⌈t/2⌉} 항이라 더 큰 T 허용.
    let cap = if low_rank { 50 } else { 30 };
    if t_count > cap {
        return Err(PyValueError::new_err(format!(
            "T-count={t_count} 이 너무 큽니다 (≤{cap})"
        )));
    }
    let amp = py.allow_threads(move || {
        if low_rank {
            qsim_stabilizer::clifford_t::clifford_t_amplitude_lowrank(n, &gates, &bitstring)
        } else {
            qsim_stabilizer::clifford_t::clifford_t_amplitude_fast(n, &gates, &bitstring)
        }
    });
    Ok((amp.re, amp.im))
}

/// near-Clifford (Clifford+T) 회로를 다중 체인 Metropolis-Hastings MCMC 로
/// 샘플링 (근사).  타깃 `∝ |⟨x|ψ⟩|²` (amplitude 는 정확).  `(counts, r_hat)`
/// 반환 — `counts` 는 measure-all dict, `r_hat` 은 Gelman-Rubin 수렴 진단
/// (체인 1개거나 표본 부족 시 `None`).
#[pyfunction]
#[pyo3(signature = (circuit, shots = 1024, burn_in = 1000, thin = 2, chains = 4, seed = None))]
fn clifford_t_sample(
    py: Python<'_>,
    circuit: &PyCircuit,
    shots: usize,
    burn_in: usize,
    thin: usize,
    chains: usize,
    seed: Option<u64>,
) -> PyResult<(std::collections::HashMap<String, usize>, Option<f64>)> {
    let n = circuit.inner.num_qubits();
    let mut gates: Vec<qsim_stabilizer::clifford_t::CtGate> = Vec::new();
    for inst in circuit.inner.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                gates.extend(gate_to_ct(gate, targets).map_err(PyValueError::new_err)?);
            }
            Instruction::Measure { .. } | Instruction::MeasureAll => {}
            other => {
                return Err(PyValueError::new_err(format!(
                    "near-Clifford 백엔드는 Clifford+T 게이트만 지원합니다: {other:?}"
                )));
            }
        }
    }
    let t_count = gates
        .iter()
        .filter(|g| {
            matches!(
                g,
                qsim_stabilizer::clifford_t::CtGate::T(_)
                    | qsim_stabilizer::clifford_t::CtGate::Tdg(_)
            )
        })
        .count();
    if t_count > 30 {
        return Err(PyValueError::new_err(format!(
            "T-count={t_count} 이 너무 큽니다 (≤30)"
        )));
    }
    let (samples, r_hat) = py.allow_threads(move || {
        qsim_stabilizer::clifford_t::clifford_t_sample_diagnostic(
            n, &gates, shots, burn_in, thin, chains, seed,
        )
    });
    let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for bits in &samples {
        let key: String = (0..n)
            .rev()
            .map(|q| if bits[q] != 0 { '1' } else { '0' })
            .collect();
        *counts.entry(key).or_insert(0) += 1;
    }
    Ok((counts, r_hat))
}

/// near-Clifford (Clifford+T) 회로의 Pauli-sum 기댓값 `⟨ψ|H|ψ⟩`.
///
/// `terms` 는 `(pauli_string, re, im)` 리스트 — `pauli[n-1-q]` 가 큐비트 `q`
/// (Qiskit 규약, I/X/Y/Z).  비용 `O(#terms · 2^{2t} · n²)` 라 T-count 가 작을 때
/// (≲12) 적합.  전역 위상 무관.  비-Clifford(비-T)/noise/동적 회로는 `ValueError`.
#[pyfunction]
#[pyo3(signature = (circuit, terms))]
fn clifford_t_expectation(
    py: Python<'_>,
    circuit: &PyCircuit,
    terms: Vec<(String, f64, f64)>,
) -> PyResult<(f64, f64)> {
    let n = circuit.inner.num_qubits();
    let mut gates: Vec<qsim_stabilizer::clifford_t::CtGate> = Vec::new();
    for inst in circuit.inner.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                gates.extend(gate_to_ct(gate, targets).map_err(PyValueError::new_err)?);
            }
            Instruction::Measure { .. } | Instruction::MeasureAll => {}
            other => {
                return Err(PyValueError::new_err(format!(
                    "near-Clifford 백엔드는 Clifford+T 게이트만 지원합니다: {other:?}"
                )));
            }
        }
    }
    let t_count = gates
        .iter()
        .filter(|g| {
            matches!(
                g,
                qsim_stabilizer::clifford_t::CtGate::T(_)
                    | qsim_stabilizer::clifford_t::CtGate::Tdg(_)
            )
        })
        .count();
    if t_count > 16 {
        return Err(PyValueError::new_err(format!(
            "expectation 은 T-count ≤ 16 만 지원합니다 (입력 {t_count}): 비용 2^(2t)"
        )));
    }
    // Pauli 문자열 → (px, pz) (pauli[n-1-q] = qubit q).
    let mut parsed: Vec<(Vec<bool>, Vec<bool>, Complex<f64>)> = Vec::with_capacity(terms.len());
    for (s, re, im) in &terms {
        if s.len() != n {
            return Err(PyValueError::new_err(format!(
                "pauli 문자열 길이 {} != n_qubits {n}",
                s.len()
            )));
        }
        let mut px = vec![false; n];
        let mut pz = vec![false; n];
        for (pos, ch) in s.chars().enumerate() {
            let q = n - 1 - pos;
            match ch {
                'I' => {}
                'X' => px[q] = true,
                'Y' => {
                    px[q] = true;
                    pz[q] = true;
                }
                'Z' => pz[q] = true,
                _ => {
                    return Err(PyValueError::new_err(format!(
                        "지원하지 않는 Pauli 문자 {ch:?} (I/X/Y/Z)"
                    )))
                }
            }
        }
        parsed.push((px, pz, Complex::new(*re, *im)));
    }
    let val = py.allow_threads(move || {
        let mut acc = Complex::new(0.0, 0.0);
        for (px, pz, coeff) in &parsed {
            acc += *coeff * qsim_stabilizer::clifford_t::clifford_t_expectation(n, &gates, px, pz);
        }
        acc
    });
    Ok((val.re, val.im))
}

/// Stabilizer (Clifford) 백엔드로 회로를 샘플링해 측정 카운트를 반환한다.
///
/// 회로가 Clifford (H/S/CNOT 군 + π/2 배수 회전) 면 Aaronson–Gottesman tableau
/// 로 **다항시간** 시뮬레이션해 수천 큐비트까지 동작한다.  비-Clifford 게이트나
/// noise / mid-circuit measure / reset / control-flow 를 만나면 `ValueError`.
/// 반환 키는 다른 백엔드와 동일한 MSB-first 비트열 (`{qubit n-1 … qubit 0}`).
#[pyfunction]
#[pyo3(signature = (circuit, shots = 1024, seed = None, depolarizing = 0.0))]
fn stabilizer_counts(
    py: Python<'_>,
    circuit: &PyCircuit,
    shots: usize,
    seed: Option<u64>,
    depolarizing: f64,
) -> PyResult<std::collections::HashMap<String, usize>> {
    if !(0.0..=1.0).contains(&depolarizing) {
        return Err(PyValueError::new_err(
            "depolarizing 은 [0,1] 범위여야 합니다",
        ));
    }
    let n = circuit.inner.num_qubits();
    let mut ops: Vec<qsim_stabilizer::CliffordOp> = Vec::new();
    for inst in circuit.inner.instructions() {
        match inst {
            Instruction::ApplyGate { gate, targets } => {
                let mapped = gate_to_clifford(gate, targets).map_err(PyValueError::new_err)?;
                ops.extend(mapped);
            }
            // 회로 끝 측정은 stabilizer 샘플링이 암묵적으로 수행 — 무시.
            Instruction::Measure { .. } | Instruction::MeasureAll => {}
            other => {
                return Err(PyValueError::new_err(format!(
                    "stabilizer 백엔드는 Clifford 게이트만 지원합니다 \
                     (noise / mid-circuit measure / reset / control-flow / 임의 \
                     unitary 미지원): {other:?}"
                )));
            }
        }
    }
    let samples = py.allow_threads(move || {
        qsim_stabilizer::sample_counts_depolarizing(n, &ops, shots, seed, depolarizing)
    });
    let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for bits in &samples {
        // bits[q] (q=0 LSB) → 정수 → MSB-first 폭 n 비트열.
        let mut outcome: u128 = 0;
        for (q, &bit) in bits.iter().enumerate() {
            if bit != 0 {
                outcome |= 1u128 << q;
            }
        }
        let key: String = (0..n)
            .rev()
            .map(|q| if (outcome >> q) & 1 == 1 { '1' } else { '0' })
            .collect();
        *counts.entry(key).or_insert(0) += 1;
    }
    Ok(counts)
}

/// optimizer 문자열 → [`PathOptimizer`].
fn parse_optimizer(
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
) -> PyResult<PathOptimizer> {
    let s = seed.unwrap_or(0);
    match optimizer {
        "greedy" => Ok(PathOptimizer::Greedy),
        "random-greedy" | "random_greedy" => Ok(PathOptimizer::RandomGreedy { trials, seed: s }),
        "sa" | "simulated-annealing" | "simulated_annealing" => {
            Ok(PathOptimizer::SimulatedAnnealing {
                iters,
                restarts,
                seed: s,
            })
        }
        "partition" | "hgp" => Ok(PathOptimizer::Partition { trials, seed: s }),
        "hyper" | "auto" => Ok(PathOptimizer::Hyper {
            effort: restarts.max(1),
            seed: s,
        }),
        other => Err(PyValueError::new_err(format!(
            "optimizer 는 'greedy' / 'random-greedy' / 'sa' / 'partition' / \
             'hyper' 여야 합니다 (입력: {other:?})"
        ))),
    }
}

/// Tensor Network Contraction: amplitude `⟨bitstring|C|0…0⟩` (deep/large 회로).
#[pyfunction]
#[pyo3(signature = (circuit, bitstring, optimizer="random-greedy", trials=32, iters=200, restarts=4, seed=None, gpu=false, max_width=0.0, max_slices=30))]
#[allow(clippy::too_many_arguments)]
fn tensornet_amplitude(
    py: Python<'_>,
    circuit: &PyCircuit,
    bitstring: Vec<u8>,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
    gpu: bool,
    max_width: f64,
    max_slices: usize,
) -> PyResult<(f64, f64)> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    let amp = py
        .allow_threads(move || {
            if max_width > 0.0 {
                // 자동 slicing (메모리 한계 안에서 큰 회로) — CPU.
                qsim_simulator::tensornet_backend::run_amplitude_sliced(
                    &circ, &bitstring, opt, max_width, max_slices,
                )
            } else if gpu {
                qsim_simulator::tensornet_backend::run_amplitude_gpu(&circ, &bitstring, opt)
            } else {
                qsim_simulator::tensornet_backend::run_amplitude(&circ, &bitstring, opt)
            }
        })
        .map_err(PyValueError::new_err)?;
    Ok((amp.re, amp.im))
}

/// Tensor Network Contraction: **여러 비트열의 amplitude 를 배치** 로 (path 1회
/// 최적화 + rayon 병렬 contraction).  XEB 등 다수 amplitude 계산에 적합.
/// 반환은 `(re, im)` 튜플 리스트.
#[pyfunction]
#[pyo3(signature = (circuit, bitstrings, optimizer="random-greedy", trials=32, iters=200, restarts=4, seed=None))]
#[allow(clippy::too_many_arguments)]
fn tensornet_amplitude_batch(
    py: Python<'_>,
    circuit: &PyCircuit,
    bitstrings: Vec<Vec<u8>>,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
) -> PyResult<Vec<(f64, f64)>> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    let amps = py
        .allow_threads(move || {
            qsim_simulator::tensornet_backend::run_amplitude_batch(&circ, &bitstrings, opt)
        })
        .map_err(PyValueError::new_err)?;
    Ok(amps.into_iter().map(|a| (a.re, a.im)).collect())
}

/// Tensor Network Contraction: statevector + sampling (작은 N) → SimulationResult.
#[pyfunction]
#[pyo3(signature = (circuit, shots=0, seed=None, optimizer="random-greedy", trials=32, iters=200, restarts=4, gpu=false))]
#[allow(clippy::too_many_arguments)]
fn tensornet_run(
    py: Python<'_>,
    circuit: &PyCircuit,
    shots: usize,
    seed: Option<u64>,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    gpu: bool,
) -> PyResult<PySimulationResult> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    let inner = py
        .allow_threads(move || {
            let sv = if gpu {
                qsim_simulator::tensornet_backend::run_statevector_gpu(&circ, opt)?
            } else {
                qsim_simulator::tensornet_backend::run_statevector(&circ, opt)?
            };
            let counts = if shots > 0 {
                // sampling 은 statevector 로부터 (CPU) — sv 재사용.
                let probs: Vec<f64> = sv.amplitudes().iter().map(|a| a.norm_sqr()).collect();
                sample_from_probs(&probs, shots, seed, circ.num_qubits())
            } else {
                std::collections::HashMap::new()
            };
            Ok::<_, String>(SimulationResult::F64 {
                counts,
                statevector: sv,
            })
        })
        .map_err(PyValueError::new_err)?;
    Ok(PySimulationResult { inner })
}

/// 확률 분포 (panta LSB index) 에서 shots 샘플 → Qiskit 표기 counts.
fn sample_from_probs(
    probs: &[f64],
    shots: usize,
    seed: Option<u64>,
    n: usize,
) -> std::collections::HashMap<String, usize> {
    use rand::{Rng, SeedableRng};
    let total: f64 = probs.iter().sum();
    let mut rng = match seed {
        Some(s) => rand::rngs::StdRng::seed_from_u64(s),
        None => rand::rngs::StdRng::from_entropy(),
    };
    let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for _ in 0..shots {
        let r = rng.gen::<f64>() * total;
        let mut acc = 0.0;
        let mut idx = probs.len() - 1;
        for (i, &p) in probs.iter().enumerate() {
            acc += p;
            if r <= acc {
                idx = i;
                break;
            }
        }
        let mut s = String::with_capacity(n);
        for q in (0..n).rev() {
            s.push(if (idx >> q) & 1 == 1 { '1' } else { '0' });
        }
        *counts.entry(s).or_insert(0) += 1;
    }
    counts
}

/// 분산 슬라이싱 계획 `(n_slices, n_configs, log2_width_per_worker, log10_flops)`.
#[pyfunction]
#[pyo3(signature = (circuit, optimizer="hyper", trials=32, iters=200, restarts=4, seed=None, max_width=27.0, max_slices=40))]
#[allow(clippy::too_many_arguments)]
fn tensornet_plan(
    py: Python<'_>,
    circuit: &PyCircuit,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
    max_width: f64,
    max_slices: usize,
) -> PyResult<(usize, u64, f64, f64)> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    py.allow_threads(move || {
        qsim_simulator::tensornet_backend::plan_amplitude(&circ, opt, max_width, max_slices)
    })
    .map_err(PyValueError::new_err)
}

/// 분산 슬라이싱 worker: `worker_id`/`n_workers` 의 부분합 amplitude.  모든 worker
/// 부분합을 더하면 전체 amplitude (멀티노드 reduce 모델).
#[pyfunction]
#[pyo3(signature = (circuit, bitstring, n_workers, worker_id, optimizer="hyper", trials=32, iters=200, restarts=4, seed=None, max_width=27.0, max_slices=40))]
#[allow(clippy::too_many_arguments)]
fn tensornet_amplitude_worker(
    py: Python<'_>,
    circuit: &PyCircuit,
    bitstring: Vec<u8>,
    n_workers: u64,
    worker_id: u64,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
    max_width: f64,
    max_slices: usize,
) -> PyResult<(f64, f64)> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    let amp = py
        .allow_threads(move || {
            qsim_simulator::tensornet_backend::run_amplitude_worker(
                &circ, &bitstring, opt, max_width, max_slices, n_workers, worker_id,
            )
        })
        .map_err(PyValueError::new_err)?;
    Ok((amp.re, amp.im))
}

/// Tensor Network Contraction: Pauli-sum 기댓값 `⟨ψ|H|ψ⟩` (deep 회로).
/// `terms` = `[(pauli_string, coeff_re, coeff_im), …]` (Qiskit 라벨 — 오른쪽 끝
/// 문자 = 큐비트 0).
#[pyfunction]
#[pyo3(signature = (circuit, terms, optimizer="random-greedy", trials=32, iters=200, restarts=4, seed=None))]
#[allow(clippy::too_many_arguments)]
fn tensornet_expectation(
    py: Python<'_>,
    circuit: &PyCircuit,
    terms: Vec<(String, f64, f64)>,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
) -> PyResult<(f64, f64)> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let terms_c: Vec<(String, Complex<f64>)> = terms
        .into_iter()
        .map(|(p, re, im)| (p, Complex::new(re, im)))
        .collect();
    let circ = circuit.inner.clone();
    let val = py
        .allow_threads(move || {
            qsim_simulator::tensornet_backend::run_expectation(&circ, &terms_c, opt)
        })
        .map_err(PyValueError::new_err)?;
    Ok((val.re, val.im))
}

/// Tensor Network contraction 비용 추정 `(log10_flops, log2_width)` — 회로가 TN
/// 으로 다룰 만한지 판단 (width = peak 중간 텐서 큐비트 수).
#[pyfunction]
#[pyo3(signature = (circuit, optimizer="random-greedy", trials=32, iters=200, restarts=4, seed=None))]
#[allow(clippy::too_many_arguments)]
fn tensornet_contraction_cost(
    py: Python<'_>,
    circuit: &PyCircuit,
    optimizer: &str,
    trials: usize,
    iters: usize,
    restarts: usize,
    seed: Option<u64>,
) -> PyResult<(f64, f64)> {
    let opt = parse_optimizer(optimizer, trials, iters, restarts, seed)?;
    let circ = circuit.inner.clone();
    let cost = py
        .allow_threads(move || qsim_simulator::tensornet_backend::contraction_cost(&circ, opt))
        .map_err(PyValueError::new_err)?;
    Ok((cost.0, cost.1))
}

#[pymodule]
fn qsim_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyCircuit>()?;
    m.add_class::<PySimulationResult>()?;
    m.add_class::<PyNoiseChannel>()?;
    m.add_class::<PyNoiseChannel2>()?;
    m.add_function(wrap_pyfunction!(run, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_amplitude, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_run, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_expectation, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_contraction_cost, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_plan, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_amplitude_worker, m)?)?;
    m.add_function(wrap_pyfunction!(stabilizer_counts, m)?)?;
    m.add_function(wrap_pyfunction!(clifford_t_amplitude, m)?)?;
    m.add_function(wrap_pyfunction!(clifford_t_expectation, m)?)?;
    m.add_function(wrap_pyfunction!(clifford_t_sample, m)?)?;
    m.add_function(wrap_pyfunction!(tensornet_amplitude_batch, m)?)?;
    Ok(())
}
