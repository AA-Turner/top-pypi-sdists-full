"""Amazon Braket ↔ panta-sim 회로 변환 어댑터 (v0.7.3).

``to_braket`` 은 panta-sim ``QuantumCircuit`` 을 Braket ``Circuit`` 으로 변환한다
(``from_braket`` 은 역방향).  Braket ``LocalSimulator`` 로 로컬에서 statevector
교차검증할 수 있고 (실 디바이스는 AWS 자격증명 필요), v0.8 하드웨어 백엔드
(AWS Braket QPU) 의 첫 단계가 된다.

Wire convention:
    Braket 의 statevector index 는 qubit 0 = MSB (big-endian) 인 반면 panta-sim
    은 qubit 0 = LSB (little-endian).  일관성 유지를 위해 panta-sim 의 qubit
    ``k`` (0..n-1) 를 Braket 의 qubit ``n-1-k`` 로 매핑한다.  그 결과 Braket 의
    statevector 가 panta-sim 의 statevector 와 **동일 인덱스로** 일치한다 (전역
    위상 제외 — Braket 회로는 전역 위상을 표현하지 않으므로 비교는 전역 위상까지).

게이트 매핑:
    - 직접 매핑 (Braket native 동명): h/x/y/z/s/t/rx/ry/rz, cx(→cnot)/cy/cz/
      swap/iswap, ccx(→ccnot)/cswap.  Braket 메서드는 ``method(*qubits, *params)``
      시그니처 (qubit 먼저, 각도 나중) — panta 의 ``(params, qubits)`` 순서와
      반대이므로 변환한다.
    - 그 외 게이트 (sdg/tdg/sx/sxdg/p/u1/u2/u/crx/cry/crz/cp/cu1/cu3/cu/ch/rxx/
      ryy/rzz/rzx/dcx/ecr/xx_plus_yy/xx_minus_yy 및 임의 ``unitary``) 는 게이트의
      유니터리 행렬을 Braket ``unitary`` (임의 행렬 게이트) 로 emit 한다.  행렬은
      panta 의 little-endian 컨벤션 그대로이고, target 순서를 역순 매핑
      (``[map(q) for q in reversed(qubits)]``) 하면 Braket 의 big-endian
      ``unitary`` 와 정확히 일치한다 (LocalSimulator 교차검증).

지원 안 함 (``NotImplementedError`` 로 명시 거부):
    - mid-circuit measurement / classical control / 블록 제어흐름 (Braket
      LocalSimulator 기본 미지원) — v0.8+.
    - 노이즈 모델 (Braket density-matrix 시뮬레이터는 별도) — v0.8+.
    측정 (``measure`` / ``measure_all``) op 은 무시한다 (Braket 은 실행 시
    전체 큐비트를 샘플링; statevector 비교에는 영향 없음).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from ..circuit import QuantumCircuit as PantaCircuit

if TYPE_CHECKING:  # pragma: no cover
    from braket.circuits import Circuit as BraketCircuit


# panta 게이트명 → Braket 메서드명 (직접 매핑, 컨벤션 1e-10 검증됨).
_DIRECT_0PARAM = {
    "h": "h",
    "x": "x",
    "y": "y",
    "z": "z",
    "s": "s",
    "t": "t",
    "cx": "cnot",
    "cy": "cy",
    "cz": "cz",
    "swap": "swap",
    "iswap": "iswap",
    "ccx": "ccnot",
    "cswap": "cswap",
}
_DIRECT_1PARAM = {"rx": "rx", "ry": "ry", "rz": "rz"}

# 제어흐름 / 동적 op — 명시 거부.
_UNSUPPORTED = {"if_eq", "if_else", "while_loop", "for_loop", "switch", "reset"}


def _gate_matrix(name: str, params: tuple, k: int) -> np.ndarray:
    """이름붙은 게이트의 유니터리 행렬을 panta 서브회로 ``to_matrix`` 로 얻는다
    (little-endian, local qubit ``i`` = ``qubits[i]``).  panta 게이트 정의를 그대로
    재사용해 중복/불일치를 피한다."""
    sub = PantaCircuit(k)
    getattr(sub, name)(*[float(p) for p in params], *range(k))
    return sub.to_matrix()


def to_braket(panta_circuit: PantaCircuit) -> "BraketCircuit":
    """panta-sim ``QuantumCircuit`` 을 Braket ``Circuit`` 으로 변환한다.

    Args:
        panta_circuit: 변환할 panta-sim 회로 (측정/제어흐름/노이즈 없는 유니터리
            회로).  측정 op 은 무시되고, 제어흐름/리셋은 ``NotImplementedError``.

    Returns:
        ``braket.circuits.Circuit``.  ``LocalSimulator`` 의 statevector 가
        panta-sim 의 statevector 와 동일 인덱스로 일치한다 (전역 위상 제외).
    """
    from braket.circuits import Circuit

    n = panta_circuit.num_qubits
    bc = Circuit()

    def mapq(q: int) -> int:
        return n - 1 - int(q)

    def emit_unitary(matrix: np.ndarray, qubits: tuple) -> None:
        # 역순 target + little-endian 행렬 그대로 → Braket big-endian unitary 일치.
        targets = [mapq(q) for q in reversed(qubits)]
        bc.unitary(targets=targets, matrix=np.asarray(matrix, dtype=np.complex128))

    used = set()
    for name, qubits, params in panta_circuit._ops:
        if name in _UNSUPPORTED:
            raise NotImplementedError(
                f"to_braket: '{name}' (제어흐름/리셋) 은 미지원 — 유니터리 회로만 "
                f"변환 가능 (v0.8 하드웨어 백엔드에서 확장)."
            )
        if name in ("measure", "measure_all"):
            continue  # Braket 은 실행 시 전체 샘플링.
        used.update(int(q) for q in qubits)
        if name in _DIRECT_0PARAM:
            getattr(bc, _DIRECT_0PARAM[name])(*[mapq(q) for q in qubits])
        elif name in _DIRECT_1PARAM:
            getattr(bc, _DIRECT_1PARAM[name])(mapq(qubits[0]), float(params[0]))
        elif name == "unitary":
            if not params:  # 빈 unitary = identity → no-op.
                continue
            emit_unitary(params[0], qubits)
        else:
            # 그 외 모든 게이트: panta 행렬 → Braket unitary.
            emit_unitary(_gate_matrix(name, params, len(qubits)), qubits)

    # Braket 회로는 instruction 이 있는 qubit 만 인식 — 미사용 qubit 에 I 보강해
    # statevector 차원을 n 으로 유지 (Braket 인덱스로 매핑).
    for q in range(n):
        if q not in used:
            bc.i(mapq(q))
    return bc


def from_braket(braket_circuit: "BraketCircuit") -> PantaCircuit:
    """Braket ``Circuit`` 을 panta-sim ``QuantumCircuit`` 으로 변환한다.

    각 Braket instruction 의 유니터리 행렬 (``gate.to_matrix()``) 을 추출해
    panta-sim 의 ``unitary`` (1-큐비트 ZYZ / k-큐비트 직접 적용) 로 emit 한다.
    Wire convention 은 ``to_braket`` 의 역 (Braket qubit ``b`` → panta qubit
    ``n-1-b``).  측정/노이즈/결과타입은 무시한다.

    Args:
        braket_circuit: 변환할 Braket 회로.

    Returns:
        panta-sim ``QuantumCircuit`` (statevector 가 Braket 과 동일 인덱스 일치).
    """
    n = braket_circuit.qubit_count
    # Braket qubit 라벨은 정수가 아닐 수 있어 정렬 인덱스로 정규화.
    labels = sorted(int(q) for q in braket_circuit.qubits)
    relabel = {lab: i for i, lab in enumerate(labels)}
    qc = PantaCircuit(n)

    def mapq(b: int) -> int:
        return n - 1 - relabel[int(b)]

    for instr in braket_circuit.instructions:
        gate = instr.operator
        targets = [int(q) for q in instr.target]
        try:
            mat = np.asarray(gate.to_matrix(), dtype=np.complex128)
        except Exception as exc:  # noqa: BLE001 - 노이즈/결과타입 등 비-게이트.
            raise NotImplementedError(
                f"from_braket: '{type(gate).__name__}' 은 유니터리 게이트가 아닙니다 "
                f"(측정/노이즈/결과타입 미지원)."
            ) from exc
        # Braket big-endian (targets[0]=MSB) → panta little-endian: 역순 매핑.
        panta_qubits = [mapq(b) for b in reversed(targets)]
        qc.unitary(mat, panta_qubits, validate=False)
    return qc
