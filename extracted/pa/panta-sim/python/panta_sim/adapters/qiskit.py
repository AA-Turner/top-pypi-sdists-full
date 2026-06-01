"""Qiskit ↔ panta-sim 회로 변환 어댑터 (v0.3.5 Cut 1).

``from_qiskit`` 은 Qiskit ``QuantumCircuit`` 을 panta-sim ``QuantumCircuit`` 으로,
``to_qiskit`` 은 그 반대 방향 변환을 수행한다. statevector convention 은
양쪽 모두 little-endian (qubit 0 = LSB, ``little`` ordering) 이므로 매핑은
1:1 이며, statevector 비교 시 1e-10 (f64) 일치한다.

게이트 매핑:
    panta-sim 의 native Rust 게이트 (H, X, Y, Z, S, Sdg, T, Tdg, Id, Rx,
    Ry, Rz, CNOT, CZ, SWAP, Toffoli, Fredkin) 와 단일 큐비트 ``unitary`` 는
    직접 매핑. 그 외 Qiskit 게이트 (sx, sxdg, p, u, u1, u2, u3, ch, cy,
    cu, cu1, cu3, cp, crx, cry, crz, …) 는 ``qiskit.qasm2.dumps()`` 로
    OpenQASM 2.0 직렬화 후 panta-sim 의 ``from_qasm()`` 가 standard
    qelib1.inc decomposition 으로 import 한다.

미지원:
    - parameterized circuit (unbound ``Parameter``) — 먼저
      ``qc.assign_parameters({...})`` 로 bind 후 호출.
    - block 기반 control flow (``IfElseOp`` / ``WhileLoopOp`` /
      ``ForLoopOp`` / ``SwitchCaseOp``) — v0.4.6+.

v0.4.5 부터 지원:
    - mid-circuit measurement (회로 중간 위치에 measure 가 있어도 정상 동작).
    - ``reset`` instruction → panta-sim ``qc.reset(q)``.
    - 레거시 ``c_if`` (instruction ``condition`` 속성 — ``(ClassicalRegister, int)``
      또는 ``(Clbit, int)``) → panta-sim ``qc.<gate>().c_if(cbits, value)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from ..circuit import QuantumCircuit as PantaCircuit

if TYPE_CHECKING:  # pragma: no cover
    from qiskit import QuantumCircuit as QiskitCircuit


_QISKIT_INSTALL_HINT = (
    "qiskit is required for this function — install with: "
    "pip install panta-sim[qiskit]"
)


def _lazy_import_qiskit() -> Any:
    """qiskit 패키지를 lazy import 한다 (미설치 시 친절한 ImportError)."""
    try:
        import qiskit  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_QISKIT_INSTALL_HINT) from exc
    return qiskit


# panta-sim 의 native fluent 메서드와 1:1 매핑되는 Qiskit gate 이름 표.
#
# v0.4.6 부터: sx/sxdg/p/u1/u2/u/cy/ch/crx/cry/crz/cp/cu1/cu3/cu 도 native 매핑.
# 매핑 표 외 게이트만 QASM2 우회 path 로 분해된다 (예: dcx, ecr, iswap, …).
_DIRECT_GATE_MAP: dict[str, str] = {
    "h": "h",
    "x": "x",
    "y": "y",
    "z": "z",
    "s": "s",
    "sdg": "sdg",
    "t": "t",
    "tdg": "tdg",
    "sx": "sx",
    "sxdg": "sxdg",
    "id": "id",
    "iden": "id",  # Qiskit alias
    "rx": "rx",
    "ry": "ry",
    "rz": "rz",
    # v0.4.6: phase / U1 / U2 / U3 native 매핑.
    "p": "p",
    "u1": "u1",
    "u2": "u2",
    "u": "u",
    "u3": "u",
    "cx": "cx",
    "cnot": "cx",
    "cz": "cz",
    "swap": "swap",
    # v0.4.6: controlled 게이트 native 매핑.
    "cy": "cy",
    "ch": "ch",
    "crx": "crx",
    "cry": "cry",
    "crz": "crz",
    "cp": "cp",
    "cu1": "cu1",
    "cu3": "cu3",
    "cu": "cu",
    "ccx": "ccx",
    "toffoli": "ccx",
    "cswap": "cswap",
    "fredkin": "cswap",
}

# 매핑 표에 없지만 special-case 처리되는 op name.
_SPECIAL_OPS = {"measure", "barrier", "unitary", "reset"}

# v0.4.7: Qiskit block-form control flow ops 도 direct-mapping path 에서 처리.
_BLOCK_CONTROL_FLOW = {"if_else", "while_loop", "for_loop", "switch_case"}


def _condition_to_cbit_indices(qiskit_circuit: Any, cond_target: Any) -> list[int]:
    """Qiskit ``instr.condition[0]`` (``ClassicalRegister`` 또는 ``Clbit``) 을
    flat cbit 인덱스 리스트로 변환한다 (LSB-first).
    """
    # ClassicalRegister 는 iterable, Clbit 은 아님.
    if hasattr(cond_target, "__iter__"):
        return [qiskit_circuit.find_bit(b).index for b in cond_target]
    return [qiskit_circuit.find_bit(cond_target).index]


def from_qiskit(qiskit_circuit: "QiskitCircuit") -> PantaCircuit:
    """Qiskit ``QuantumCircuit`` 을 panta-sim ``QuantumCircuit`` 으로 변환한다.

    ``qiskit.QuantumCircuit.data`` 의 instruction list 를 순회하며 panta-sim 의
    fluent 메서드로 매핑한다. 매핑 표 외 게이트가 발견되면 회로 전체를
    ``qiskit.qasm2.dumps()`` → ``panta_sim.QuantumCircuit.from_qasm()`` 경로로
    fallback 한다 (v0.3.0 의 16종 qelib1 게이트 decomposition 재활용).

    Args:
        qiskit_circuit: Qiskit ``QuantumCircuit``. unbound ``Parameter`` 가 있으면
            ``ValueError`` (먼저 ``assign_parameters`` 로 bind 필요).

    Returns:
        panta-sim ``QuantumCircuit``. ``run()`` 결과의 statevector 가 Qiskit
        ``Statevector(qiskit_circuit)`` 와 1e-10 (f64) 일치한다.

    Raises:
        ImportError: ``qiskit`` 미설치.
        ValueError: 매개변수 bind 안 됐거나, 변환 불가 op (reset / if_else 등).

    Example:
        >>> from qiskit import QuantumCircuit as QC
        >>> from panta_sim import from_qiskit
        >>> qc = QC(2); qc.h(0); qc.cx(0, 1)
        >>> panta = from_qiskit(qc)
        >>> result = panta.run(shots=0)  # statevector mode
    """
    _lazy_import_qiskit()  # ImportError early

    if list(qiskit_circuit.parameters):
        raise ValueError(
            "qiskit circuit has unbound Parameters: "
            f"{list(qiskit_circuit.parameters)}. "
            "Call qc.assign_parameters({...}) before from_qiskit()."
        )

    n_qubits = qiskit_circuit.num_qubits

    # 1차: 모든 op 이 직접 매핑 가능한지 확인. 하나라도 매핑 표 외면
    # QASM2 fallback 으로 일괄 변환 (mixed walk 보다 단순 + 안정).
    # v0.4.7: block control flow (IfElseOp / WhileLoopOp / ForLoopOp /
    # SwitchCaseOp) 도 native 매핑 — _convert_instructions_into 가 재귀로 처리.
    needs_qasm_fallback = False
    for instr in qiskit_circuit.data:
        name = instr.operation.name
        if (
            name in _DIRECT_GATE_MAP
            or name in _SPECIAL_OPS
            or name in _BLOCK_CONTROL_FLOW
        ):
            continue
        needs_qasm_fallback = True
        break

    if needs_qasm_fallback:
        return _from_qiskit_via_qasm(qiskit_circuit)

    # 직접 매핑 path
    n_qubits_full = qiskit_circuit.num_qubits
    n_clbits_full = qiskit_circuit.num_clbits
    panta = PantaCircuit(n_qubits_full)
    # 사용자 cbit register 폭을 보존 — measure 가 한 번도 안 나와도 outer cbit 폭은
    # block control flow 의 cond_indices 가 참조 가능해야 함.  dummy 로 grow.
    if n_clbits_full > 0:
        # n_cbits 는 measure / c_if / block control flow 의 cbit_indices 로 자동 grow.
        # 여기서 미리 grow 시킬 직접 API 가 없으므로 instructions 진행 시 처리.
        pass

    q_map = list(range(n_qubits_full))
    c_map = list(range(n_clbits_full))
    needs_fallback = _convert_instructions_into(panta, qiskit_circuit, q_map, c_map)
    if needs_fallback:
        return _from_qiskit_via_qasm(qiskit_circuit)
    return panta


def _convert_instructions_into(
    panta: PantaCircuit,
    qiskit_subcircuit: Any,
    q_map: list[int],
    c_map: list[int],
) -> bool:
    """Qiskit sub-circuit 의 instructions 를 panta 에 push (재귀 가능).

    `q_map` / `c_map` 은 sub-circuit 의 qubit/cbit 인덱스를 outer panta 의 인덱스로
    변환하는 lookup.  최상위 호출에서는 identity, block control flow 의 nested
    body 에서는 outer instruction 의 qubits / clbits 위치로 매핑된다.

    반환값: `True` 면 multi-qubit unitary 등 fallback 필요 — 호출자가 QASM 우회.
    """
    for instr in qiskit_subcircuit.data:
        op = instr.operation
        name = op.name

        if name == "barrier":
            continue

        # qubits / cbits 매핑 (sub-circuit 인덱스 → outer)
        sub_q_idxs = [qiskit_subcircuit.find_bit(q).index for q in instr.qubits]
        sub_c_idxs = [qiskit_subcircuit.find_bit(c).index for c in instr.clbits]
        outer_q_idxs = [q_map[i] for i in sub_q_idxs]
        outer_c_idxs = [c_map[i] for i in sub_c_idxs]

        if name == "measure":
            panta.measure(outer_q_idxs[0], outer_c_idxs[0])
            continue
        if name == "reset":
            for q in outer_q_idxs:
                panta.reset(q)
            continue
        if name == "unitary":
            matrix = op.params[0]
            if matrix.shape != (2, 2):
                return True
            panta.unitary(
                np.asarray(matrix, dtype=np.complex128), outer_q_idxs[0]
            )
            continue

        # v0.4.7 block control flow.
        if name == "if_else":
            _convert_if_else(panta, instr, qiskit_subcircuit, q_map, c_map)
            continue
        if name == "while_loop":
            _convert_while_loop(panta, instr, qiskit_subcircuit, q_map, c_map)
            continue
        if name == "for_loop":
            _convert_for_loop(panta, instr, qiskit_subcircuit, q_map, c_map)
            continue
        if name == "switch_case":
            _convert_switch(panta, instr, qiskit_subcircuit, q_map, c_map)
            continue

        if name not in _DIRECT_GATE_MAP:
            # 매핑 표 외 게이트 — 우회 시그널.
            return True

        target = _DIRECT_GATE_MAP[name]
        params = list(op.params)
        method = getattr(panta, target)
        if target in ("rx", "ry", "rz", "p", "u1"):
            method(float(params[0]), outer_q_idxs[0])
        elif target == "u2":
            method(float(params[0]), float(params[1]), outer_q_idxs[0])
        elif target == "u":
            method(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                outer_q_idxs[0],
            )
        elif target in ("crx", "cry", "crz", "cp", "cu1"):
            method(float(params[0]), outer_q_idxs[0], outer_q_idxs[1])
        elif target == "cu3":
            method(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                outer_q_idxs[0],
                outer_q_idxs[1],
            )
        elif target == "cu":
            method(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                float(params[3]),
                outer_q_idxs[0],
                outer_q_idxs[1],
            )
        else:
            method(*outer_q_idxs)

        # 레거시 c_if (instr.condition).
        condition = getattr(instr, "condition", None)
        if condition is None:
            condition = getattr(op, "condition", None)
        if condition is not None:
            cond_target, cond_value = condition
            cbits = _condition_to_cbit_indices(qiskit_subcircuit, cond_target)
            outer_cbits = [c_map[i] for i in cbits]
            panta.c_if(outer_cbits, int(cond_value))

    return False


def _resolve_condition_indices(
    qiskit_subcircuit: Any, condition: Any, c_map: list[int]
) -> tuple[list[int], int]:
    """`(ClassicalRegister | Clbit, value)` → outer cbit 인덱스 리스트 + value."""
    cond_target, cond_value = condition
    sub_cbits = _condition_to_cbit_indices(qiskit_subcircuit, cond_target)
    outer_cbits = [c_map[i] for i in sub_cbits]
    return outer_cbits, int(cond_value)


def _build_block_subpanta(
    outer_panta: PantaCircuit,
    qiskit_block: Any,
    instr_qubits: list[int],
    instr_clbits: list[int],
) -> PantaCircuit:
    """Qiskit block (sub-circuit) 을 panta sub-circuit 으로 변환.

    sub-block 의 qubit/cbit i → instr_qubits[i] / instr_clbits[i] 로 매핑 후
    `_convert_instructions_into` 재귀.
    """
    sub_panta = PantaCircuit(outer_panta.num_qubits)
    needs = _convert_instructions_into(
        sub_panta, qiskit_block, instr_qubits, instr_clbits
    )
    if needs:
        raise ValueError(
            "block control flow body 에 매핑 불가 op (multi-qubit unitary 등). "
            "sub-circuit 을 단순 게이트로 decompose 후 다시 시도."
        )
    return sub_panta


def _convert_if_else(
    panta: PantaCircuit,
    instr: Any,
    qiskit_subcircuit: Any,
    q_map: list[int],
    c_map: list[int],
) -> None:
    op = instr.operation
    blocks = op.blocks  # (then_block, else_block?)
    instr_q = [q_map[qiskit_subcircuit.find_bit(q).index] for q in instr.qubits]
    instr_c = [c_map[qiskit_subcircuit.find_bit(c).index] for c in instr.clbits]
    cond = op.condition  # (Clbit | ClassicalRegister, value) — Qiskit 1.0+ 도 동일.
    cbits, value = _resolve_condition_indices(qiskit_subcircuit, cond, c_map)

    then_sub = _build_block_subpanta(panta, blocks[0], instr_q, instr_c)
    else_sub = (
        _build_block_subpanta(panta, blocks[1], instr_q, instr_c)
        if len(blocks) >= 2 and blocks[1] is not None
        else None
    )
    # PyO3 add_if_else: 사용 시 inner Rust circuit 만 필요 — sub-circuit 의 _circuit 과 _ops 둘 다 필요.
    panta._circuit.add_if_else(
        cbits,
        value,
        then_sub._circuit,
        else_sub._circuit if else_sub is not None else None,
    )
    panta._ops.append(
        (
            "if_else",
            (),
            (
                tuple(cbits),
                value,
                tuple(then_sub._ops),
                tuple(else_sub._ops) if else_sub is not None else None,
            ),
        )
    )


def _convert_while_loop(
    panta: PantaCircuit,
    instr: Any,
    qiskit_subcircuit: Any,
    q_map: list[int],
    c_map: list[int],
) -> None:
    op = instr.operation
    body_block = op.blocks[0]
    instr_q = [q_map[qiskit_subcircuit.find_bit(q).index] for q in instr.qubits]
    instr_c = [c_map[qiskit_subcircuit.find_bit(c).index] for c in instr.clbits]
    cond = op.condition
    cbits, value = _resolve_condition_indices(qiskit_subcircuit, cond, c_map)
    body_sub = _build_block_subpanta(panta, body_block, instr_q, instr_c)

    # max_iters: panta default 256 — Qiskit WhileLoopOp 자체는 unbounded 라
    # 보수적으로 256.  필요 시 사용자 주의.
    panta._circuit.add_while_loop(cbits, value, body_sub._circuit, 256)
    panta._ops.append(
        (
            "while_loop",
            (),
            (tuple(cbits), value, tuple(body_sub._ops), 256),
        )
    )


def _convert_for_loop(
    panta: PantaCircuit,
    instr: Any,
    qiskit_subcircuit: Any,
    q_map: list[int],
    c_map: list[int],
) -> None:
    op = instr.operation
    # ForLoopOp.params = (indexset, loop_param, body).
    # iterations = len(indexset).  loop_param 가 body 안에서 게이트 인자로
    # 사용되는 경우 (parameterized) — assign_parameters 로 unroll 해야 panta-sim
    # 의 fixed-body ForLoop 와 호환.
    indexset, loop_param, body_block = op.params
    iterations = len(list(indexset))
    instr_q = [q_map[qiskit_subcircuit.find_bit(q).index] for q in instr.qubits]
    instr_c = [c_map[qiskit_subcircuit.find_bit(c).index] for c in instr.clbits]

    if loop_param is not None and loop_param in body_block.parameters:
        # Unroll: 각 i 값으로 body 를 assign_parameters 후 iteration 시퀀스 push.
        # outer panta 에 직접 instructions 추가 (ForLoop op 안 만들고 unroll).
        for i_value in indexset:
            unrolled = body_block.assign_parameters({loop_param: i_value})
            unrolled_sub = _build_block_subpanta(
                panta, unrolled, instr_q, instr_c
            )
            # body 를 그대로 push (블록 op 아님).
            for op_record in unrolled_sub._ops:
                panta._ops.append(op_record)
            # Rust side 는 unrolled_sub._circuit.instructions() 를 outer 에 extend.
            # _RustCircuit 은 extend 메서드 없음 — for_loop(1, body) 로 처리.
            panta._circuit.add_for_loop(1, unrolled_sub._circuit)
        return

    # loop variable 없는 경우 — 1 회 변환 후 ForLoop op 로 N 회 반복.
    body_sub = _build_block_subpanta(panta, body_block, instr_q, instr_c)
    panta._circuit.add_for_loop(iterations, body_sub._circuit)
    panta._ops.append(
        (
            "for_loop",
            (),
            (iterations, tuple(body_sub._ops)),
        )
    )


def _convert_switch(
    panta: PantaCircuit,
    instr: Any,
    qiskit_subcircuit: Any,
    q_map: list[int],
    c_map: list[int],
) -> None:
    op = instr.operation
    instr_q = [q_map[qiskit_subcircuit.find_bit(q).index] for q in instr.qubits]
    instr_c = [c_map[qiskit_subcircuit.find_bit(c).index] for c in instr.clbits]
    target = op.target  # ClassicalRegister | Clbit | Expr
    sub_cbits = _condition_to_cbit_indices(qiskit_subcircuit, target)
    outer_cbits = [c_map[i] for i in sub_cbits]

    # cases() returns iterator of (label_or_default, body).
    rust_cases: list = []
    op_cases: list = []
    try:
        from qiskit.circuit.controlflow import CASE_DEFAULT  # type: ignore
    except Exception:
        CASE_DEFAULT = None  # type: ignore

    for label, body_block in op.cases_specifier():
        body_sub = _build_block_subpanta(panta, body_block, instr_q, instr_c)
        if CASE_DEFAULT is not None and label is CASE_DEFAULT:
            label_or_none = None
        elif isinstance(label, (list, tuple)) and len(label) > 0:
            # Multiple labels per case: panta 의 `Switch` 는 case 당 단일 label —
            # 각 label 에 대해 같은 body 를 case 로 복제.
            for sub_label in label:
                if sub_label is None or (
                    CASE_DEFAULT is not None and sub_label is CASE_DEFAULT
                ):
                    label_or_none = None
                else:
                    label_or_none = int(sub_label)
                rust_cases.append((label_or_none, body_sub._circuit))
                op_cases.append((label_or_none, tuple(body_sub._ops)))
            continue
        else:
            label_or_none = int(label)
        rust_cases.append((label_or_none, body_sub._circuit))
        op_cases.append((label_or_none, tuple(body_sub._ops)))

    panta._circuit.add_switch(outer_cbits, rust_cases)
    panta._ops.append(
        (
            "switch",
            (),
            (tuple(outer_cbits), tuple(op_cases)),
        )
    )


def _from_qiskit_via_qasm(qiskit_circuit: "QiskitCircuit") -> PantaCircuit:
    """OpenQASM 2.0 우회로로 변환. v0.3.0 의 from_qasm 인프라를 재활용한다."""
    _lazy_import_qiskit()
    import qiskit.qasm2 as qasm2  # submodule lazy import

    try:
        qasm_str = qasm2.dumps(qiskit_circuit)
    except Exception as exc:  # qasm2.dumps 실패 (예: QASM3-only feature)
        raise ValueError(
            f"failed to serialize qiskit circuit to OpenQASM 2.0: {exc}. "
            "Try qc.decompose() before from_qiskit() or use a circuit "
            "with only standard gates."
        ) from exc
    return PantaCircuit.from_qasm(qasm_str)


def to_qiskit(panta_circuit: PantaCircuit) -> "QiskitCircuit":
    """panta-sim ``QuantumCircuit`` 을 Qiskit ``QuantumCircuit`` 으로 변환한다.

    panta-sim 의 ``_ops`` (fluent 메서드 호출 기록) 를 순회하며 동명의 Qiskit
    메서드를 호출한다. v0.4 부터 ``from_qasm()`` 으로 만든 회로도 ``_ops`` 가
    Rust ``Circuit::instructions()`` 에서 복원되므로, QASM 우회 없이 직접
    매핑 path 가 사용된다.

    측정 / global phase 도 보존:
        - ``measure(qubit, cbit)`` → Qiskit ``measure(qubit, cbit)`` (cbit 인덱스
          1:1 보존).
        - ``measure_all()`` → Qiskit ``measure_all()``.
        - panta-sim 의 ``global_phase`` (radian) 가 Qiskit ``global_phase`` 로
          복사된다.

    Args:
        panta_circuit: panta-sim ``QuantumCircuit``.

    Returns:
        Qiskit ``QuantumCircuit``. ``Statevector()`` 와 panta-sim ``run().
        statevector()`` 가 1e-10 (f64) 일치한다.

    Raises:
        ImportError: ``qiskit`` 미설치.
    """
    qiskit = _lazy_import_qiskit()

    QiskitQC = qiskit.QuantumCircuit

    n = panta_circuit.num_qubits
    # cbit 개수 + unitary op 의 누적 phase 를 한 번에 산출.
    # unitary op 은 Qiskit 측에서 ``qc.unitary(m,...)`` 호출 시 phase 가
    # 자체 내장되므로, panta 의 ``global_phase`` 에서 그만큼 차감해야 double
    # counting 을 막을 수 있다. ``alpha = arg(det(m))/2`` 식은 panta-sim 의
    # ``crates/transpiler/src/decompose.rs`` 의 Z-Y-Z 분해와 동일.
    # if_eq op 은 cbit_indices 의 max + 1 까지 cbit 폭 확장 필요.
    max_cbit = -1
    has_measure_all = False
    unitary_phase_sum = 0.0

    def _scan_ops(ops_iter):
        nonlocal max_cbit, has_measure_all, unitary_phase_sum
        for name, _q, params in ops_iter:
            if name == "measure":
                max_cbit = max(max_cbit, int(params[0]) if params else 0)
            elif name == "measure_all":
                has_measure_all = True
            elif name == "unitary" and params:
                m = np.asarray(params[0], dtype=np.complex128)
                unitary_phase_sum += float(np.angle(np.linalg.det(m)) / 2.0)
            elif name == "if_eq" and params:
                cbits_tuple = params[0]
                if cbits_tuple:
                    max_cbit = max(max_cbit, max(cbits_tuple))
            elif name == "if_else" and params:
                cbits_tuple, _value, then_ops, else_ops = params
                if cbits_tuple:
                    max_cbit = max(max_cbit, max(cbits_tuple))
                _scan_ops(then_ops or ())
                if else_ops:
                    _scan_ops(else_ops)
            elif name == "while_loop" and params:
                cbits_tuple, _value, body_ops, _max_iters = params
                if cbits_tuple:
                    max_cbit = max(max_cbit, max(cbits_tuple))
                _scan_ops(body_ops or ())
            elif name == "for_loop" and params:
                _iter, body_ops = params
                _scan_ops(body_ops or ())
            elif name == "switch" and params:
                cbits_tuple, op_cases = params
                if cbits_tuple:
                    max_cbit = max(max_cbit, max(cbits_tuple))
                for _label, body_ops in op_cases or ():
                    _scan_ops(body_ops)

    _scan_ops(panta_circuit._ops)
    n_cbits = (max_cbit + 1) if max_cbit >= 0 else 0

    if has_measure_all and n_cbits == 0:
        # measure_all 은 cbit N 개를 자동 할당. 그 외 measure 가 없으므로
        # measure_all() Qiskit 메서드가 register 를 만든다 → 별도 cbit 인자 X.
        qc = QiskitQC(n)
    else:
        qc = QiskitQC(n, max(n_cbits, 0))

    def _emit_gate(name: str, qubits: tuple, params: tuple) -> Any:
        """단일 게이트 op 을 Qiskit 회로에 추가하고 InstructionSet 반환.

        v0.4.6 native 매핑 추가 — Qiskit 메서드 시그니처에 맞춰 dispatch.
        """
        if name in ("rx", "ry", "rz", "p", "u1"):
            return getattr(qc, name)(float(params[0]), qubits[0])
        if name == "u2":
            return qc.u2(float(params[0]), float(params[1]), qubits[0])
        if name == "u":
            return qc.u(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                qubits[0],
            )
        if name in ("crx", "cry", "crz", "cp", "cu1"):
            return getattr(qc, name)(float(params[0]), qubits[0], qubits[1])
        if name == "cu3":
            return qc.cu3(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                qubits[0],
                qubits[1],
            )
        if name == "cu":
            return qc.cu(
                float(params[0]),
                float(params[1]),
                float(params[2]),
                float(params[3]),
                qubits[0],
                qubits[1],
            )
        # parameter 없는 게이트 (h, x, ..., sx, sxdg, cx, cy, ch, swap, ccx, cswap)
        method = getattr(qc, name)
        return method(*qubits)

    for name, qubits, params in panta_circuit._ops:
        if name == "unitary":
            if not params:
                qc.id(qubits[0])
            else:
                qc.unitary(params[0], [qubits[0]])
            continue

        if name == "measure":
            cbit = int(params[0]) if params else qubits[0]
            qc.measure(qubits[0], cbit)
            continue

        if name == "measure_all":
            qc.measure_all()
            continue

        if name == "reset":
            qc.reset(qubits[0])
            continue

        if name == "if_eq":
            # params = (cbits_tuple, value, inner_name, inner_params)
            cbits_tuple, value, inner_name, inner_params = params
            instr_set = _emit_gate(inner_name, qubits, tuple(inner_params))
            # c_if target: 단일 cbit 이면 Clbit, contiguous-from-zero 매칭이면 creg.
            if len(cbits_tuple) == 1:
                cond_target = qc.clbits[cbits_tuple[0]]
            elif (
                qc.cregs
                and len(qc.cregs) == 1
                and tuple(cbits_tuple) == tuple(range(qc.cregs[0].size))
            ):
                cond_target = qc.cregs[0]
            else:
                raise NotImplementedError(
                    f"to_qiskit: c_if cbits {cbits_tuple} 가 단일 cbit 도, "
                    f"contiguous-from-zero ClassicalRegister 도 아닙니다 — "
                    f"Qiskit c_if API 한계."
                )
            instr_set.c_if(cond_target, int(value))
            continue

        # v0.4.7 block control flow.
        if name == "if_else":
            _emit_if_else(qc, params, panta_circuit)
            continue
        if name == "while_loop":
            _emit_while_loop(qc, params, panta_circuit)
            continue
        if name == "for_loop":
            _emit_for_loop(qc, params, panta_circuit)
            continue
        if name == "switch":
            _emit_switch(qc, params, panta_circuit)
            continue

        _emit_gate(name, qubits, params)

    # global phase 보존 (Qiskit Statevector 가 phase 포함 비교).
    # unitary op 의 phase 는 Qiskit 의 ``qc.unitary()`` 가 자체 내장하므로
    # ``unitary_phase_sum`` 만큼 빼서 double counting 방지.
    qc.global_phase = float(panta_circuit.global_phase - unitary_phase_sum)

    return qc


# ============================================================================
# v0.4.7 — to_qiskit block control flow helpers
# ============================================================================


def _build_subpanta_from_ops(num_qubits: int, ops_iter) -> PantaCircuit:
    """ops 시퀀스로부터 Qiskit-bound sub-panta circuit 을 새로 빌드.

    `to_qiskit` 가 nested body 를 별개의 Qiskit subcircuit 으로 만들 때 사용 —
    panta-side ops 만 갖고 새 PantaCircuit 만들어 to_qiskit 재귀.
    """
    sub = PantaCircuit(num_qubits)
    sub._ops = list(ops_iter)
    # _circuit 은 빈 상태로 둠 — to_qiskit 은 _ops 만 사용.
    return sub


def _emit_if_else(qc: Any, params: tuple, panta_circuit: PantaCircuit) -> None:
    cbits_tuple, value, then_ops, else_ops = params
    n = panta_circuit.num_qubits
    then_panta = _build_subpanta_from_ops(n, then_ops)
    then_qc = to_qiskit(then_panta)
    else_qc = None
    if else_ops is not None:
        else_panta = _build_subpanta_from_ops(n, else_ops)
        else_qc = to_qiskit(else_panta)

    cond_target = _resolve_qiskit_condition_target(qc, cbits_tuple)
    # IfElseOp 은 body num_qubits / num_clbits 와 정확히 일치하는 qubits / clbits
    # 인자를 받음.  단순화: outer 의 모든 큐비트 (panta n_qubits) + 사용된 cbit 들.
    body_n_qubits = then_qc.num_qubits
    body_n_clbits = max(
        then_qc.num_clbits, else_qc.num_clbits if else_qc is not None else 0
    )
    qubits = list(range(body_n_qubits))
    clbits = list(range(body_n_clbits))
    from qiskit.circuit.controlflow import IfElseOp  # type: ignore

    op = IfElseOp((cond_target, value), then_qc, else_qc)
    qc.append(op, qubits, clbits)


def _emit_while_loop(qc: Any, params: tuple, panta_circuit: PantaCircuit) -> None:
    cbits_tuple, value, body_ops, _max_iters = params
    n = panta_circuit.num_qubits
    body_panta = _build_subpanta_from_ops(n, body_ops)
    body_qc = to_qiskit(body_panta)
    cond_target = _resolve_qiskit_condition_target(qc, cbits_tuple)
    qubits = list(range(body_qc.num_qubits))
    clbits = list(range(body_qc.num_clbits))
    from qiskit.circuit.controlflow import WhileLoopOp  # type: ignore

    op = WhileLoopOp((cond_target, value), body_qc)
    qc.append(op, qubits, clbits)


def _emit_for_loop(qc: Any, params: tuple, panta_circuit: PantaCircuit) -> None:
    iterations, body_ops = params
    n = panta_circuit.num_qubits
    body_panta = _build_subpanta_from_ops(n, body_ops)
    body_qc = to_qiskit(body_panta)
    qubits = list(range(body_qc.num_qubits))
    clbits = list(range(body_qc.num_clbits))
    indexset = list(range(iterations))
    from qiskit.circuit.controlflow import ForLoopOp  # type: ignore

    op = ForLoopOp(indexset, None, body_qc)
    qc.append(op, qubits, clbits)


def _emit_switch(qc: Any, params: tuple, panta_circuit: PantaCircuit) -> None:
    cbits_tuple, op_cases = params
    n = panta_circuit.num_qubits
    cond_target = _resolve_qiskit_condition_target(qc, cbits_tuple)

    qiskit_cases: list = []
    try:
        from qiskit.circuit.controlflow import CASE_DEFAULT  # type: ignore
    except Exception:
        CASE_DEFAULT = None  # type: ignore

    body_n_qubits_max = 0
    body_n_clbits_max = 0
    for label, body_ops in op_cases:
        body_panta = _build_subpanta_from_ops(n, body_ops)
        body_qc = to_qiskit(body_panta)
        body_n_qubits_max = max(body_n_qubits_max, body_qc.num_qubits)
        body_n_clbits_max = max(body_n_clbits_max, body_qc.num_clbits)
        qiskit_label = (
            CASE_DEFAULT if (label is None and CASE_DEFAULT is not None) else label
        )
        qiskit_cases.append((qiskit_label, body_qc))

    qubits = list(range(body_n_qubits_max))
    clbits = list(range(body_n_clbits_max))
    from qiskit.circuit.controlflow import SwitchCaseOp  # type: ignore

    op = SwitchCaseOp(cond_target, qiskit_cases)
    qc.append(op, qubits, clbits)


def _resolve_qiskit_condition_target(qc: Any, cbits_tuple: tuple) -> Any:
    """panta cbits 인덱스 → Qiskit Clbit / ClassicalRegister.  v0.4.5 if_eq 와 동일 로직."""
    if len(cbits_tuple) == 1:
        return qc.clbits[cbits_tuple[0]]
    if (
        qc.cregs
        and len(qc.cregs) == 1
        and tuple(cbits_tuple) == tuple(range(qc.cregs[0].size))
    ):
        return qc.cregs[0]
    raise NotImplementedError(
        f"to_qiskit: cbits {cbits_tuple} 가 단일 cbit 도, contiguous-from-zero "
        f"ClassicalRegister 도 아닙니다."
    )
