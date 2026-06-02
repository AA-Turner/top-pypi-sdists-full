"""2-큐비트 임의 unitary 분해 (KAK / Cartan) — v0.7.1.

임의의 4×4 unitary ``U`` 를 단일 큐비트 게이트와 네이티브 2-큐비트 회전
(``RXX`` / ``RYY`` / ``RZZ``) 의 곱으로 분해한다::

(v0.7.3) 하드웨어 basis 타깃의 **CNOT-개수 최적** 합성도 제공한다 —
``two_qubit_decompose_cx`` / ``QuantumCircuit.unitary(..., decompose="cx")`` 가
Weyl chamber 정준 좌표로 0/1/2/3-CNOT 을 판정해 ``CX`` + 단일 큐비트 게이트로
최소 CNOT 회로를 emit (Qiskit ``TwoQubitBasisDecomposer(CXGate)`` 와 CNOT 개수
+ 행렬 1e-9 일치).  아래는 native (``RXX/RYY/RZZ``) 기저 설명이다::

    U = e^{iφ} · (a_L ⊗ b_L) · exp(i(x·XX + y·YY + z·ZZ)) · (a_R ⊗ b_R)

여기서 ``XX``, ``YY``, ``ZZ`` 는 서로 교환하므로 비국소부는
``RXX(-2x)·RYY(-2y)·RZZ(-2z)`` 로 그대로 실현된다.  따라서 분해 결과는
panta 의 모든 백엔드 (statevector / density / MPS / GPU) 에서 동작하며 QASM
으로 export 하거나 하드웨어 basis 로 트랜스파일할 수 있다.

알고리즘 (Cartan KAK, magic basis):

1. 전역 위상을 빼 ``U`` 를 ``SU(4)`` 로 만든다.
2. magic (Bell) basis 로 변환 — 국소 ``SU(2)⊗SU(2)`` 가 실수 ``SO(4)`` 가
   된다.
3. ``M = Uₘᵀ Uₘ`` (복소 대칭 unitary) 를 실수 직교 ``P`` 로 동시 대각화한다
   (실/허수부가 교환하므로 비-degenerate 선형결합의 ``eigh``).
4. ``Uₘ = K₁ A K₂`` (``K₁, K₂ ∈ SO(4)``, ``A`` 대각 위상) 를 복원하고
   ``det(K₁) = +1`` 이 되도록 위상 부호를 맞춘다.
5. 국소부 ``B K B†`` 를 Kronecker 인수분해해 단일 큐비트 게이트를, 비국소부
   에서 ``x, y, z`` 를 Pauli 사영으로 추출한다.

수백~수천 개의 무작위 ``U(4)`` 및 CNOT / SWAP / iSWAP / DCX 등 특수 게이트
에서 재구성 오차 < 1e-12 (Qiskit ``Operator`` 교차검증).
"""

from __future__ import annotations

import numpy as np

# magic (Bell) basis: B† (a⊗b) B 가 실수 SO(4), B† exp(i(xXX+yYY+zZZ)) B 가 대각.
_MAGIC = (1.0 / np.sqrt(2.0)) * np.array(
    [[1, 0, 0, 1j], [0, 1j, 1, 0], [0, 1j, -1, 0], [1, 0, 0, -1j]], dtype=np.complex128
)
_MAGIC_DAG = _MAGIC.conj().T

_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
_XX = np.kron(_X, _X)
_YY = np.kron(_Y, _Y)
_ZZ = np.kron(_Z, _Z)


def _kron_factor(w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """``w = a ⊗ b`` (4×4) 를 두 SU(2) 행렬 ``a, b`` 로 인수분해한다.

    스칼라 위상은 ``a``, ``b`` 를 ``det=1`` 로 정규화하며 흡수한다 (호출부가
    전역 위상을 수치적으로 보정).
    """
    r, c = np.unravel_index(int(np.argmax(np.abs(w))), w.shape)
    i0, k0 = divmod(r, 2)
    j0, l0 = divmod(c, 2)
    b = np.array(
        [[w[2 * i0, 2 * j0], w[2 * i0, 2 * j0 + 1]],
         [w[2 * i0 + 1, 2 * j0], w[2 * i0 + 1, 2 * j0 + 1]]],
        dtype=np.complex128,
    )
    a = np.array(
        [[w[k0, l0], w[k0, 2 + l0]], [w[2 + k0, l0], w[2 + k0, 2 + l0]]],
        dtype=np.complex128,
    )
    scale = w[r, c] / (a[i0, j0] * b[k0, l0])
    a = a * scale
    a = a / np.sqrt(np.linalg.det(a))
    b = b / np.sqrt(np.linalg.det(b))
    return a, b


def _simultaneous_so4(m2: np.ndarray) -> np.ndarray:
    """복소 대칭 unitary ``M`` 를 동시 대각화하는 실수 직교 ``P`` 를 찾는다.

    ``M`` 의 실수부/허수부는 교환하는 실대칭 행렬이므로, 충분히 비-degenerate
    한 선형결합 ``Re(M) + α·Im(M)`` 의 고유벡터가 둘 다 대각화한다.
    """
    best_p = None
    best_gap = -1.0
    for alpha in (0.5, 0.31, 0.717, 1.3, 2.1, 0.07, 3.7, 0.93, 5.1, 1.7, 11.3, 0.013):
        _, p = np.linalg.eigh(m2.real + alpha * m2.imag)
        gap = float(np.min(np.abs(np.diff(np.sort(np.linalg.eigvalsh(m2.real + alpha * m2.imag))))))
        if gap > best_gap:
            best_gap = gap
            best_p = p
        if gap > 1e-4:
            break
    return best_p


def two_qubit_kak(u: np.ndarray) -> dict:
    """4×4 unitary ``u`` 를 KAK 형식으로 분해한다.

    Args:
        u: ``2×2`` 가 아닌 ``4×4`` 복소 unitary (검증은 호출부 책임).

    Returns:
        다음 키를 가진 dict::

            {"a_l", "b_l", "a_r", "b_r": 2×2 SU(2) ndarray,
             "x", "y", "z": float (비국소 상호작용 계수),
             "phase": float (전역 위상 φ)}

        의미: ``u = e^{iφ}·(a_l⊗b_l)·exp(i(x·XX+y·YY+z·ZZ))·(a_r⊗b_r)``,
        여기서 첫 인자 (``a``) 가 상위 큐비트 (qubit 1), 둘째 (``b``) 가 하위
        큐비트 (qubit 0) 에 작용한다.
    """
    u = np.asarray(u, dtype=np.complex128)
    det = np.linalg.det(u)
    gphase = det ** 0.25
    u_su = u / gphase  # det(u_su) = 1

    um = _MAGIC_DAG @ u_su @ _MAGIC
    m2 = um.T @ um
    p = _simultaneous_so4(m2)
    if np.linalg.det(p) < 0:
        p = p.copy()
        p[:, 0] = -p[:, 0]

    um_p = um @ p
    a = np.empty(4, dtype=np.complex128)
    for k in range(4):
        cc = um_p[:, k] @ um_p[:, k]
        a[k] = np.sqrt(cc / abs(cc)) if abs(cc) > 1e-12 else 1.0
    k1 = um_p * (1.0 / a)
    if np.real(np.linalg.det(k1)) < 0:  # SO(4) 보장 (det +1).
        a[0] = -a[0]
        k1 = um_p * (1.0 / a)
    k1 = k1.real

    loc_l = _MAGIC @ k1 @ _MAGIC_DAG
    loc_r = _MAGIC @ p.T @ _MAGIC_DAG
    # 비국소 Hamiltonian H = B·diag(angle(a))·B† (logm 불필요, pure numpy).
    h = _MAGIC @ np.diag(np.angle(a)) @ _MAGIC_DAG
    x = float(np.real(np.trace(h @ _XX)) / 4.0)
    y = float(np.real(np.trace(h @ _YY)) / 4.0)
    z = float(np.real(np.trace(h @ _ZZ)) / 4.0)

    a_l, b_l = _kron_factor(loc_l)
    a_r, b_r = _kron_factor(loc_r)

    # 비국소부 N 을 닫힌 형식으로 재구성 (XX,YY,ZZ 가 모두 involution 이므로
    # exp(iθP) = cosθ·I + i·sinθ·P).  scipy 불필요.
    n_int = _interaction_matrix(x, y, z)
    u_rec0 = np.kron(a_l, b_l) @ n_int @ np.kron(a_r, b_r)
    idx = np.unravel_index(int(np.argmax(np.abs(u_rec0))), u_rec0.shape)
    phase = float(np.angle(u[idx] / u_rec0[idx]))

    return {"a_l": a_l, "b_l": b_l, "a_r": a_r, "b_r": b_r,
            "x": x, "y": y, "z": z, "phase": phase}


def _interaction_matrix(x: float, y: float, z: float) -> np.ndarray:
    """``exp(i(x·XX + y·YY + z·ZZ))`` 를 닫힌 형식으로 계산한다."""
    eye = np.eye(4, dtype=np.complex128)
    nx = np.cos(x) * eye + 1j * np.sin(x) * _XX
    ny = np.cos(y) * eye + 1j * np.sin(y) * _YY
    nz = np.cos(z) * eye + 1j * np.sin(z) * _ZZ
    return nx @ ny @ nz


# ----------------- CNOT-count 최적 2-큐비트 합성 (하드웨어 basis = CX) -----------------
#
# KAK 분해는 ``U = e^{iφ}(a_l⊗b_l)·exp(i(x·XX+y·YY+z·ZZ))·(a_r⊗b_r)`` 를 준다.
# 비국소 상호작용 ``N(x,y,z)`` 를 실현하는 데 필요한 CNOT 의 최소 개수는 국소
# 불변량 (Weyl chamber 정준 좌표) 으로 결정된다 (Vidal-Dawson 2004,
# Vatan-Williams 2004, Shende-Bullock-Markov 2004):
#
#   정준 좌표 (ca≥cb≥cc≥0, 모두 [0,π/4]):
#     (0,0,0)      → 0 CNOT (국소)
#     (π/4,0,0)    → 1 CNOT (CX 와 국소 동등)
#     cc = 0       → 2 CNOT
#     cc > 0       → 3 CNOT (일반)
#
# 각 케이스를 CX + 단일 큐비트 회전으로 정확히 실현하는 닫힌 형식 회로 (모두
# Qiskit ``TwoQubitBasisDecomposer(CXGate)`` 와 행렬 1e-9 + CNOT 개수 교차검증):
#
#   2-CNOT (한 좌표 0):  CX·CX 사이에 단일 큐비트 회전.  ``XX+ZZ`` 가 기본형
#       (``CX01·e^{ix X₀}·e^{iz Z₁}·CX01 = e^{i(x·XX+z·ZZ)}`` — control-X→XX,
#       target-Z→ZZ 의 CNOT 켤레), ``XX+YY`` / ``YY+ZZ`` 는 단일 큐비트 Clifford
#       (Rx/Rz ±π/2) 기저 변환으로 유도.
#   1-CNOT (정준 (π/4,0,0)):  ``CZ = (I⊗H)·CX01·(I⊗H)`` 와 ``e^{i(π/4)ZZ} =
#       e^{-iπ/4}·Rz₀(-π/2)Rz₁(-π/2)·CZ`` 에서 ``e^{i·v·ZZ}`` (v=±π/4) 를 얻고
#       ``XX``/``YY`` 는 Clifford 켤레로 유도.
#   3-CNOT (일반):  Vatan-Williams 정준 회로 (CX10·CX01·CX10 + Rz/Ry).

_HMAT = (1.0 / np.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)


def _rx_mat(t: float) -> np.ndarray:
    c, s = np.cos(t / 2.0), np.sin(t / 2.0)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=np.complex128)


def _two_qubit_weyl_coords(x: float, y: float, z: float) -> list:
    """비국소 좌표 ``(x,y,z)`` 를 Weyl chamber 정준 좌표로 환원한다 (CNOT 개수
    판정용).  각 좌표를 ``mod π/2`` 로 ``[0,π/2)`` 에 넣고 ``π/4`` 초과는 반사,
    내림차순 정렬."""
    red = []
    for v in (x, y, z):
        v = v % (np.pi / 2.0)
        if v > np.pi / 4.0 + 1e-12:
            v = np.pi / 2.0 - v
        red.append(v)
    return sorted(red, reverse=True)


def cnot_count_2q(x: float, y: float, z: float, tol: float = 1e-6) -> int:
    """비국소 좌표 ``(x,y,z)`` 의 2-큐비트 게이트를 실현하는 데 필요한 최소 CNOT
    개수 (0/1/2/3) 를 정준 좌표로부터 판정한다."""
    ca, cb, cc = _two_qubit_weyl_coords(x, y, z)
    if ca < tol:
        return 0
    if cb < tol and abs(ca - np.pi / 4.0) < tol:
        return 1
    if cc < tol:
        return 2
    return 3


def _interaction_cx_ops(x: float, y: float, z: float, ncx: int, q0: int, q1: int) -> list:
    """``N(x,y,z)`` 를 ``ncx`` 개의 CX 와 단일 큐비트 회전으로 실현하는 op 시퀀스
    (적용 순서, 전역 큐비트 인덱스).  ``q0`` = 하위 (LSB), ``q1`` = 상위."""
    if ncx == 0:
        return []
    if ncx == 3:
        # Vatan-Williams 정준 3-CNOT 회로.
        return [
            ("rz", np.pi / 2.0, q1),
            ("cx", q1, q0),
            ("rz", np.pi / 2.0 - 2.0 * z, q0),
            ("ry", -2.0 * x + np.pi / 2.0, q1),
            ("cx", q0, q1),
            ("ry", 2.0 * y - np.pi / 2.0, q1),
            ("cx", q1, q0),
            ("rz", -np.pi / 2.0, q0),
        ]
    coords = (x, y, z)
    if ncx == 1:
        # 정준 (π/4,0,0): 한 축만 ±π/4.  1-CNOT 블록은 v=±π/4 에서만 정확하므로
        # 부호를 보존해 정확히 ±π/4 로 스냅한다 (진짜 1-CNOT 게이트는 정확히
        # ±π/4; 경계 근처 오분류는 호출부의 재구성 검증이 3-CNOT 으로 폴백).
        i = int(np.argmax([abs(v) for v in coords]))
        v = float(np.copysign(np.pi / 4.0, coords[i]))
        return _one_cnot_axis_ops(i, v, q0, q1)
    # ncx == 2: 한 좌표가 0 → 나머지 두 축의 2-CNOT 블록.
    i = int(np.argmin([abs(v) for v in coords]))
    if i == 1:  # y≈0 → XX+ZZ
        return _xz_block_ops(x, z, q0, q1)
    if i == 2:  # z≈0 → XX+YY
        return _xy_block_ops(x, y, q0, q1)
    return _yz_block_ops(y, z, q0, q1)  # x≈0 → YY+ZZ


def _xz_block_ops(x: float, z: float, q0: int, q1: int) -> list:
    """``CX01·e^{ix X₀}·e^{iz Z₁}·CX01 = e^{i(x·XX+z·ZZ)}`` (2 CNOT)."""
    return [
        ("cx", q0, q1),
        ("rz", -2.0 * z, q1),
        ("rx", -2.0 * x, q0),
        ("cx", q0, q1),
    ]


def _xy_block_ops(x: float, y: float, q0: int, q1: int) -> list:
    """``e^{i(x·XX+y·YY)}`` — ZZ→YY (Rx±π/2 켤레) 로 ``_xz_block`` 변형 (2 CNOT)."""
    return (
        [("rx", -np.pi / 2.0, q0), ("rx", -np.pi / 2.0, q1)]
        + _xz_block_ops(x, y, q0, q1)
        + [("rx", np.pi / 2.0, q0), ("rx", np.pi / 2.0, q1)]
    )


def _yz_block_ops(y: float, z: float, q0: int, q1: int) -> list:
    """``e^{i(y·YY+z·ZZ)}`` — XX→YY (Rz±π/2 켤레) 로 ``_xz_block`` 변형 (2 CNOT)."""
    return (
        [("rz", -np.pi / 2.0, q0), ("rz", -np.pi / 2.0, q1)]
        + _xz_block_ops(y, z, q0, q1)
        + [("rz", np.pi / 2.0, q0), ("rz", np.pi / 2.0, q1)]
    )


def _one_cnot_axis_ops(axis: int, v: float, q0: int, q1: int) -> list:
    """``e^{i·v·PP}`` (P = X/Y/Z, ``axis`` 0/1/2, v=±π/4) 를 1 CNOT 으로 실현한다."""
    zz = [
        ("u1", _HMAT, q1),
        ("cx", q0, q1),
        ("u1", _HMAT, q1),
        ("rz", -2.0 * v, q1),
        ("rz", -2.0 * v, q0),
        ("u1", np.exp(-1j * v) * np.eye(2, dtype=np.complex128), q0),
    ]
    if axis == 2:  # ZZ
        return zz
    # XX: Z→X (H 켤레);  YY: Z→Y (Rx(π/2) 켤레).
    c = _HMAT if axis == 0 else _rx_mat(np.pi / 2.0)
    cd = c.conj().T
    return (
        [("u1", cd, q0), ("u1", cd, q1)] + zz + [("u1", c, q0), ("u1", c, q1)]
    )


def two_qubit_decompose_cx(u: np.ndarray, qubits: list) -> list:
    """4×4 unitary ``u`` 를 **CNOT-개수 최적** 회로로 분해한다 (하드웨어 basis = CX).

    KAK 정준 좌표로 0/1/2/3-CNOT 을 판정하고, 각 케이스를 CX + 단일 큐비트
    게이트로 정확히 실현한다.  Qiskit ``TwoQubitBasisDecomposer(CXGate)`` 와
    동일한 CNOT 개수 + 행렬 1e-9 일치 (전역 위상 포함).

    Args:
        u: ``4×4`` 복소 unitary.
        qubits: 전역 큐비트 인덱스 ``[q0, q1]`` (``q0`` = LSB, ``u`` 의 sub-index
            비트 0 에 대응).

    Returns:
        op 리스트.  각 op 은 ``("u1", mat2x2, q)`` / ``("cx", control, target)``
        / ``("rx"|"ry"|"rz", angle, q)`` 중 하나 (전역 큐비트 인덱스).  곱이 ``u``
        와 정확히 일치한다 (전역 위상 포함).
    """
    u = np.asarray(u, dtype=np.complex128)
    q0, q1 = int(qubits[0]), int(qubits[1])
    k = two_qubit_kak(u)
    x, y, z = k["x"], k["y"], k["z"]

    def _build(ncx: int) -> list:
        inter = _interaction_cx_ops(x, y, z, ncx, q0, q1)
        ops = (
            [("u1", k["b_r"], q0), ("u1", k["a_r"], q1)]
            + inter
            + [("u1", k["b_l"], q0), ("u1", k["a_l"], q1)]
        )
        # 전역 위상 보정: 전체 곱을 계산해 잔여 위상을 마지막 u1 행렬에 흡수.
        rec = _replay_ops(ops, q0, q1)
        idx = np.unravel_index(int(np.argmax(np.abs(u))), u.shape)
        if abs(rec[idx]) > 1e-12:
            phase = np.angle(u[idx] / rec[idx])
            last = ops[-1]
            ops[-1] = ("u1", np.exp(1j * phase) * last[1], last[2])
            rec = rec * np.exp(1j * phase)
        # rtol=0 (절대 오차만) — 경계 근처 게이트의 부정확 블록을 확실히 검출.
        return ops, bool(np.allclose(rec, u, rtol=0.0, atol=1e-9))

    ncx = cnot_count_2q(x, y, z)
    ops, ok = _build(ncx)
    # 경계 근처 (정준 좌표가 0/π/4 에 매우 가깝지만 정확하지 않은) 게이트는
    # 특수 (0/1/2-CNOT) 블록이 부정확할 수 있다.  3-CNOT Vatan-Williams 회로는
    # 임의 좌표에서 정확하므로 검증 실패 시 폴백 (정확성 보장; 최적 CNOT 개수는
    # 명확한 경우에만).
    if not ok and ncx != 3:
        ops, ok = _build(3)
    return ops


def _replay_ops(ops: list, q0: int, q1: int) -> np.ndarray:
    """op 시퀀스를 4×4 행렬로 재생 (내부 위상 보정용, 큐비트 ``q0`` < ``q1``)."""
    eye = np.eye(2, dtype=np.complex128)

    def emb(m2: np.ndarray, q: int) -> np.ndarray:
        # q1 = 상위 비트, q0 = 하위 비트.
        return np.kron(m2, eye) if q == q1 else np.kron(eye, m2)

    # 기저 |q1 q0> (인덱스 = q1·2+q0).  cx01: control q0(하위)→target q1(상위)
    # 가 |01>↔|11> (인덱스 1↔3) 교환.  cx10: control q1→target q0 가 |10>↔|11>
    # (인덱스 2↔3) 교환.
    cx01 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]],
                    dtype=np.complex128)
    cx10 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
                    dtype=np.complex128)
    g = np.eye(4, dtype=np.complex128)
    for op in ops:
        if op[0] == "cx":
            g = (cx01 if op[1] == q0 else cx10) @ g
        elif op[0] == "u1":
            g = emb(op[1], op[2]) @ g
        else:
            ang = op[1]
            if op[0] == "rx":
                m2 = _rx_mat(ang)
            elif op[0] == "ry":
                cc, ss = np.cos(ang / 2.0), np.sin(ang / 2.0)
                m2 = np.array([[cc, -ss], [ss, cc]], dtype=np.complex128)
            else:  # rz
                m2 = np.array([[np.exp(-1j * ang / 2.0), 0], [0, np.exp(1j * ang / 2.0)]],
                              dtype=np.complex128)
            g = emb(m2, op[2]) @ g
    return g


# ----------------------- n-큐비트 상태 준비 (Möttönen) -----------------------


def _ucr_alphas(theta: np.ndarray) -> np.ndarray:
    """uniformly-controlled rotation 의 분해 각도 ``α = M·θ / 2ᵐ``.

    ``M[i][j] = (-1)^{gray(i)·j}`` (Möttönen et al. 2004).
    """
    na = len(theta)
    if na == 1:
        return theta.copy()
    m = np.empty((na, na))
    for i in range(na):
        gi = i ^ (i >> 1)
        for j in range(na):
            m[i, j] = (-1.0) ** bin(gi & j).count("1")
    return m @ theta / na


def _ucr_native(theta: np.ndarray, controls: list[int], target: int, axis: str) -> list:
    """uniformly-controlled ``R_axis(θ)`` 를 native (``ry``/``rz`` + ``cx``)
    게이트 시퀀스로 분해한다 (gray-code CNOT 배치)."""
    m = len(controls)
    na = 1 << m
    alpha = _ucr_alphas(theta)
    seq: list = []
    for i in range(na):
        seq.append((axis, float(alpha[i]), target))
        if m > 0:
            if i < na - 1:
                cpos = (((i ^ (i >> 1)) ^ ((i + 1) ^ ((i + 1) >> 1)))).bit_length() - 1
            else:
                cpos = m - 1
            seq.append(("cx", controls[cpos], target))
    return seq


def state_preparation_gates(amplitudes) -> tuple[list, float]:
    """``|0…0⟩ → |ψ⟩`` 를 native 게이트로 준비하는 시퀀스를 반환한다.

    Möttönen et al. (2004) 의 uniformly-controlled rotation 방식 — 진폭을
    큐비트별로 disentangle 하는 회로를 역순/역게이트로 뒤집어 준비 회로를
    만든다.  ``RY/RZ + CNOT`` 만 사용하므로 모든 백엔드에서 동작하고 전체 행렬
    (``O(4ⁿ)``) 을 만들지 않는다 (게이트 수 ``O(2ⁿ)``).

    Args:
        amplitudes: 정규화된 길이 ``2ⁿ`` 복소 진폭.  ``amplitudes[i]`` 의 비트
            ``j`` 가 (로컬) 큐비트 ``j`` 에 대응 (little-endian).

    Returns:
        ``(gates, global_phase)``.  ``gates`` 는 ``("ry"|"rz", angle, qubit)``
        또는 ``("cx", control, target)`` 튜플 리스트 (적용 순서).  로컬 큐비트
        인덱스 ``0..n-1``.  최종 상태의 전역 위상은 ``global_phase``.
    """
    a = np.asarray(amplitudes, dtype=np.complex128).ravel()
    n = int(round(np.log2(len(a))))
    cur = a.copy()
    disentangle: list = []
    for t in range(n):  # target 큐비트 t (LSB 부터)
        m = n - 1 - t
        controls = list(range(t + 1, n))
        thy = np.zeros(1 << m)
        thz = np.zeros(1 << m)
        for hi in range(1 << m):
            base = sum(((hi >> b) & 1) << (t + 1 + b) for b in range(m))
            x0 = cur[base]
            x1 = cur[base | (1 << t)]
            r = float(np.hypot(abs(x0), abs(x1)))
            if r > 1e-300 and (abs(x0) > 1e-300 or abs(x1) > 1e-300):
                thz[hi] = float(np.angle(x1) - np.angle(x0))
                thy[hi] = 2.0 * float(np.arctan2(abs(x1), abs(x0)))
        level = _ucr_native(-thz, controls, t, "rz") + _ucr_native(-thy, controls, t, "ry")
        cur = _apply_gates(cur, level, n)
        disentangle += level
    global_phase = float(np.angle(cur[0]))
    # 준비 = disentangle 의 역게이트를 역순으로.
    prep: list = []
    for g in reversed(disentangle):
        if g[0] == "cx":
            prep.append(g)
        else:
            prep.append((g[0], -g[1], g[2]))
    return prep, global_phase


def _zyz_phase(u: np.ndarray) -> float:
    """2×2 unitary 의 전역 위상 (det 의 절반)."""
    return float(np.angle(np.linalg.det(u)) / 2.0)


def quantum_shannon_decompose(u: np.ndarray, qubits: list[int], basis: str = "native") -> list:
    """임의 k-큐비트 unitary 를 native 게이트 op 리스트로 분해한다 (QSD).

    Quantum Shannon Decomposition (Shende-Bullock-Markov 2006): cosine-sine
    분해로 최상위 큐비트를 분리해 두 멀티플렉서 + uniformly-controlled Ry 로
    나누고, 멀티플렉서를 고유분해로 demux (두 (k-1)-큐비트 unitary + UCRz) 한다.
    1-큐비트는 그대로, 2-큐비트는 KAK 로 종료.

    Args:
        u: ``2^k × 2^k`` unitary.
        qubits: 전역 큐비트 인덱스 (``qubits[-1]`` = 최상위 = select).
        basis: 2-큐비트 종료 기저.  ``"native"`` (기본) 은 ``RXX/RYY/RZZ`` 곱,
            ``"cx"`` 는 CNOT-개수 최적 (하드웨어 basis = CX + 단일 큐비트).

    Returns:
        op 리스트.  각 op 은 다음 중 하나 (전역 큐비트 인덱스)::

            ("u1", mat2x2, q)            # 1-큐비트 unitary (위상 포함)
            ("cx", control, target)
            ("rx"|"ry"|"rz", angle, q)
            ("rxx"|"ryy"|"rzz", angle, q0, q1)

        모든 op 의 곱이 ``u`` 와 정확히 일치 (전역 위상 포함).
    """
    n = len(qubits)
    u = np.asarray(u, dtype=np.complex128)
    if n == 1:
        return [("u1", u, qubits[0])]
    if n == 2:
        if basis == "cx":
            return two_qubit_decompose_cx(u, [qubits[0], qubits[1]])
        k = two_qubit_kak(u)
        q0, q1 = qubits[0], qubits[1]
        # 전역 위상은 a_l 에 흡수 (u1 op 의 행렬에 보존 → replay-safe).
        return [
            ("u1", k["a_r"], q1),
            ("u1", k["b_r"], q0),
            ("rxx", -2.0 * k["x"], q0, q1),
            ("ryy", -2.0 * k["y"], q0, q1),
            ("rzz", -2.0 * k["z"], q0, q1),
            ("u1", np.exp(1j * k["phase"]) * k["a_l"], q1),
            ("u1", k["b_l"], q0),
        ]
    from scipy.linalg import cossin

    half = 1 << (n - 1)
    uu, cs, vdh = cossin(u, p=half, q=half)
    u1, u2 = uu[:half, :half], uu[half:, half:]
    v1, v2 = vdh[:half, :half], vdh[half:, half:]
    c = np.diag(cs[:half, :half]).real
    s = np.diag(cs[half:, :half]).real
    theta_y = 2.0 * np.arctan2(s, c)
    sel = qubits[-1]
    lower = qubits[:-1]

    def _demux(g1, g2):
        x = g1 @ g2.conj().T
        lam, vmat = np.linalg.eig(x)
        d = np.sqrt(lam)
        w = (np.diag(d) @ vmat.conj().T) @ g2
        return vmat, w, -2.0 * np.angle(d)

    ops: list = []
    # u = uu · cs · vdh  → 회로 적용 순서 (state 에 우→좌): vdh, cs, uu.
    vmat, wmat, az = _demux(v1, v2)
    ops += quantum_shannon_decompose(wmat, lower, basis)
    ops += _relabel_ucr(_ucr_native(az, list(range(n - 1)), n - 1, "rz"), qubits)
    ops += quantum_shannon_decompose(vmat, lower, basis)
    ops += _relabel_ucr(_ucr_native(theta_y, list(range(n - 1)), n - 1, "ry"), qubits)
    vmat, wmat, az = _demux(u1, u2)
    ops += quantum_shannon_decompose(wmat, lower, basis)
    ops += _relabel_ucr(_ucr_native(az, list(range(n - 1)), n - 1, "rz"), qubits)
    ops += quantum_shannon_decompose(vmat, lower, basis)
    return ops


def _relabel_ucr(seq: list, qubits: list[int]) -> list:
    """_ucr_native 의 로컬 인덱스 (controls=0..n-2, target=n-1) 를 전역으로 매핑."""
    out = []
    for g in seq:
        if g[0] == "cx":
            out.append(("cx", qubits[g[1]], qubits[g[2]]))
        else:
            out.append((g[0], g[1], qubits[g[2]]))
    return out


def _apply_gates(psi: np.ndarray, gates: list, n: int) -> np.ndarray:
    """native 게이트 시퀀스를 statevector 에 적용 (내부 검증/disentangle 용)."""
    t = psi.reshape([2] * n)
    for g in gates:
        if g[0] == "cx":
            c, tgt = g[1], g[2]
            sl = [slice(None)] * n
            sl[n - 1 - c] = 1
            idx = tuple(sl)
            block = t[idx]
            t[idx] = np.flip(block, axis=(n - 1 - tgt) if (n - 1 - tgt) < (n - 1 - c) else (n - 1 - tgt) - 1)
        else:
            angle = g[1]
            if g[0] == "ry":
                cc, ss = np.cos(angle / 2), np.sin(angle / 2)
                u = np.array([[cc, -ss], [ss, cc]], dtype=np.complex128)
            else:  # rz
                u = np.array([[np.exp(-1j * angle / 2), 0], [0, np.exp(1j * angle / 2)]], dtype=np.complex128)
            ax = n - 1 - g[2]
            t = np.moveaxis(np.tensordot(u, t, axes=([1], [ax])), 0, ax)
    return t.reshape(-1)
