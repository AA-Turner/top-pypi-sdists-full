"""회로 / 결과 / 상태 시각화 모듈 (v0.3.2).

이 모듈은 panta-sim 회로와 시뮬레이션 결과를 시각화하는 헬퍼를 제공한다.
텍스트 출력 (`_draw_circuit_text`, `histogram_text`) 은 표준 라이브러리만
사용하고, matplotlib 기반 함수 (`plot_histogram`, `plot_bloch`) 는
`panta-sim[viz]` extras 가 설치되어 있을 때만 동작한다.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import numpy.typing as npt

OpRecord = Tuple[str, Tuple[int, ...], Tuple[Any, ...]]

_VIZ_INSTALL_HINT = (
    "matplotlib is required for this function — install with: "
    "pip install panta-sim[viz]"
)

_GLYPHS_UNICODE: Dict[str, str] = {
    "wire": "─",   # ─
    "vert": "│",   # │
    "cross": "┼",  # ┼
    "lbox": "┤",   # ┤
    "rbox": "├",   # ├
    "ctrl": "●",   # ●
}

_GLYPHS_ASCII: Dict[str, str] = {
    "wire": "-",
    "vert": "|",
    "cross": "+",
    "lbox": "[",
    "rbox": "]",
    "ctrl": "*",
}

def _label_for(name: str, params: Sequence[float]) -> str:
    """단일 박스 라벨 (게이트 종류별)."""
    base = {
        "h": "H",
        "x": "X",
        "y": "Y",
        "z": "Z",
        "s": "S",
        "sdg": "Sdg",
        "t": "T",
        "tdg": "Tdg",
        "id": "I",
        "unitary": "U",
        "measure": "M",
        "measure_all": "M",
    }
    if name in base:
        return base[name]
    if name in ("rx", "ry", "rz", "crx", "cry", "crz"):
        # CRx/CRy/CRz 의 target box 라벨도 동일.
        head = "R" + name[-1]
        return f"{head}({params[0]:.4f})"
    if name in ("p", "u1", "cp", "cu1"):
        return f"P({params[0]:.4f})"
    if name == "u2":
        return f"U2({params[0]:.4f},{params[1]:.4f})"
    if name in ("u", "cu3"):
        return f"U({params[0]:.4f},{params[1]:.4f},{params[2]:.4f})"
    if name == "cu":
        return f"U({params[0]:.4f},{params[1]:.4f},{params[2]:.4f},γ={params[3]:.4f})"
    if name == "sx":
        return "√X"
    if name == "sxdg":
        return "√X†"
    return name.upper()


def _markers_for_op(
    op: OpRecord,
) -> Tuple[Dict[int, Tuple[str, str]], Tuple[int, int]]:
    """op → ({qubit: (kind, label)}, (qmin, qmax)) 변환.

    kind 는 "box" (단일 게이트 / target / SWAP / measure) 또는 "ctrl" (제어 점).
    """
    name, qubits, params = op
    if not qubits:
        raise ValueError(f"op {name!r} has no qubits")
    qmin, qmax = min(qubits), max(qubits)
    if name in (
        "h", "x", "y", "z", "s", "sdg", "t", "tdg", "sx", "sxdg", "id",
        "rx", "ry", "rz", "p", "u1", "u2", "u", "unitary", "measure", "reset",
    ):
        return {qubits[0]: ("box", _label_for(name, params))}, (qmin, qmax)
    if name == "measure_all":
        return {q: ("box", "M") for q in qubits}, (qmin, qmax)
    if name == "cx":
        ctrl, tgt = qubits
        return {ctrl: ("ctrl", "●"), tgt: ("box", "X")}, (qmin, qmax)
    if name == "cz":
        a, b = qubits
        return {a: ("ctrl", "●"), b: ("ctrl", "●")}, (qmin, qmax)
    if name == "swap":
        a, b = qubits
        return {a: ("box", "X"), b: ("box", "X")}, (qmin, qmax)
    if name == "iswap":
        a, b = qubits
        return {a: ("box", "iSWAP"), b: ("box", "iSWAP")}, (qmin, qmax)
    if name in ("rxx", "ryy", "rzz", "rzx", "xx_plus_yy", "xx_minus_yy"):
        # 두 큐비트 모두 라벨 box.
        a, b = qubits
        lbl = name.upper().replace("_", "") + (f"({params[0]:.2f})" if params else "")
        return {a: ("box", lbl), b: ("box", lbl)}, (qmin, qmax)
    if name in ("dcx", "ecr"):
        a, b = qubits
        return {a: ("box", name.upper()), b: ("box", name.upper())}, (qmin, qmax)
    # v0.4.6 controlled-1q gates: control 은 점, target 은 게이트 라벨 box.
    if name == "cy":
        ctrl, tgt = qubits
        return {ctrl: ("ctrl", "●"), tgt: ("box", "Y")}, (qmin, qmax)
    if name == "ch":
        ctrl, tgt = qubits
        return {ctrl: ("ctrl", "●"), tgt: ("box", "H")}, (qmin, qmax)
    if name in ("crx", "cry", "crz"):
        ctrl, tgt = qubits
        return (
            {ctrl: ("ctrl", "●"), tgt: ("box", _label_for(name, params))},
            (qmin, qmax),
        )
    if name in ("cp", "cu1", "cu3", "cu"):
        ctrl, tgt = qubits
        return (
            {ctrl: ("ctrl", "●"), tgt: ("box", _label_for(name, params))},
            (qmin, qmax),
        )
    if name == "ccx":
        c1, c2, tgt = qubits
        return (
            {c1: ("ctrl", "●"), c2: ("ctrl", "●"), tgt: ("box", "X")},
            (qmin, qmax),
        )
    if name == "cswap":
        c, t1, t2 = qubits
        return (
            {c: ("ctrl", "●"), t1: ("box", "X"), t2: ("box", "X")},
            (qmin, qmax),
        )
    if name == "if_eq":
        # v0.4.5 IfEq op: inner 게이트의 markers + classical control 표시.
        # params = (cbits_tuple, value, inner_name, inner_params).
        _, _, inner_name, inner_params = params
        inner_op = (inner_name, qubits, tuple(inner_params))
        return _markers_for_op(inner_op)
    raise ValueError(f"unsupported op for draw(): {name!r}")


def _pack_columns(
    ops: Sequence[OpRecord],
) -> List[List[Tuple[OpRecord, Dict[int, Tuple[str, str]], Tuple[int, int]]]]:
    """op 들을 column 으로 packing.

    실행 순서를 보존하기 위해 *마지막* column 에만 합치기를 시도한다 — 비
    인접 op 가 같은 column 으로 흘러들어가 의미상 inversion 이 일어나는
    것을 방지. 동일 column 은 순수하게 병렬 실행 가능한 op (서로의 span
    이 겹치지 않음) 만 포함한다.
    """
    columns: List[Dict[str, object]] = []
    for op in ops:
        markers, (qmin, qmax) = _markers_for_op(op)
        span = set(range(qmin, qmax + 1))
        if columns:
            last_used: set = columns[-1]["used"]  # type: ignore[assignment]
            if not (span & last_used):
                columns[-1]["ops"].append(  # type: ignore[union-attr]
                    (op, markers, (qmin, qmax))
                )
                last_used.update(span)
                continue
        columns.append({
            "ops": [(op, markers, (qmin, qmax))],
            "used": set(span),
        })
    return [col["ops"] for col in columns]  # type: ignore[misc]


def _draw_circuit_text(
    ops: Sequence[OpRecord],
    num_qubits: int,
    style: str = "unicode",
) -> str:
    """회로의 텍스트 다이어그램을 반환한다.

    Args:
        ops: ``(name, qubits, params)`` 튜플 리스트. 게이트 추가 순서.
        num_qubits: 큐비트 수.
        style: ``"unicode"`` (default) — box-drawing 문자, 또는 ``"ascii"``.

    Returns:
        줄 바꿈으로 join 된 회로 다이어그램 문자열.
    """
    if style not in ("unicode", "ascii"):
        raise ValueError(
            f"style must be 'unicode' or 'ascii', got {style!r}"
        )
    g = _GLYPHS_UNICODE if style == "unicode" else _GLYPHS_ASCII

    qprefix_w = len(f"q{num_qubits - 1}: ") if num_qubits > 0 else 4

    def _prefix(q: int) -> str:
        return f"q{q}: ".ljust(qprefix_w)

    if num_qubits == 0:
        return ""

    if not ops:
        rows = [_prefix(q) + g["wire"] * 4 for q in range(num_qubits)]
        return "\n".join(rows)

    columns = _pack_columns(ops)

    rows = [_prefix(q) for q in range(num_qubits)]

    for col in columns:
        col_w = 1
        for _op, markers, _span in col:
            for _q, (kind, label) in markers.items():
                if kind == "box":
                    col_w = max(col_w, len(label))
        cell_w = col_w + 2

        cell_per_q: Dict[int, str] = {}
        for _op, markers, (qmin, qmax) in col:
            for q in range(qmin, qmax + 1):
                if q in markers:
                    kind, label = markers[q]
                    if kind == "box":
                        cell_per_q[q] = (
                            g["lbox"] + label.center(col_w) + g["rbox"]
                        )
                    elif kind == "ctrl":
                        left = (cell_w - 1) // 2
                        right = cell_w - 1 - left
                        cell_per_q[q] = (
                            g["wire"] * left + g["ctrl"] + g["wire"] * right
                        )
                else:
                    left = (cell_w - 1) // 2
                    right = cell_w - 1 - left
                    cell_per_q[q] = (
                        g["wire"] * left + g["cross"] + g["wire"] * right
                    )

        for q in range(num_qubits):
            if q not in cell_per_q:
                cell_per_q[q] = g["wire"] * cell_w

        for q in range(num_qubits):
            rows[q] += g["wire"] + cell_per_q[q]

    for q in range(num_qubits):
        rows[q] += g["wire"]

    return "\n".join(rows)


def _lazy_import_pyplot() -> Any:
    """matplotlib.pyplot 을 lazy import 한다 (없으면 ImportError 친절 메시지)."""
    try:
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
        raise ImportError(_VIZ_INSTALL_HINT) from exc
    return plt


def histogram_text(
    counts: Mapping[str, int],
    width: int = 40,
    style: str = "unicode",
) -> str:
    """측정 counts 분포의 텍스트 막대 그래프.

    Args:
        counts: ``{bitstring: count}`` 딕셔너리.
        width: 막대의 최대 폭 (가장 큰 카운트가 이 폭으로 정규화됨).
        style: ``"unicode"`` (default) 면 ``█``, ``"ascii"`` 면 ``#``.

    Returns:
        한 줄에 ``"<key> | <bar> <count>"`` 형식의 정렬된 문자열.
    """
    if style not in ("unicode", "ascii"):
        raise ValueError(
            f"style must be 'unicode' or 'ascii', got {style!r}"
        )
    if width <= 0:
        raise ValueError(f"width must be positive, got {width}")
    if not counts:
        return ""
    bar_char = "█" if style == "unicode" else "#"
    items = sorted(counts.items())
    max_count = max(counts.values())
    key_w = max(len(k) for k in counts.keys())
    lines = []
    for key, cnt in items:
        filled = round(cnt / max_count * width) if max_count > 0 else 0
        bar = bar_char * filled
        lines.append(f"{key:>{key_w}} | {bar} {cnt}")
    return "\n".join(lines)


def plot_histogram(
    counts: Mapping[str, int],
    *,
    figsize: Optional[Tuple[float, float]] = None,
    ax: Optional[Any] = None,
    title: Optional[str] = None,
    color: Optional[str] = None,
    bar_labels: bool = True,
) -> Any:
    """측정 counts 의 막대 히스토그램을 matplotlib Figure 로 반환한다.

    matplotlib 미설치 시 ``ImportError`` 친절 메시지.

    Args:
        counts: ``{bitstring: count}``.
        figsize: ``(width, height)`` (인치). ``ax`` 가 None 이고 새 figure
            를 생성할 때만 사용.
        ax: 기존 ``Axes`` 에 그리려면 전달. None 이면 새 Figure / Axes 생성.
        title: 차트 제목.
        color: 막대 색깔. None 이면 matplotlib default.
        bar_labels: True 면 막대 위에 카운트 숫자를 annotate.

    Returns:
        ``matplotlib.figure.Figure`` 객체.
    """
    plt = _lazy_import_pyplot()
    items = sorted(counts.items())
    keys = [k for k, _ in items]
    values = [v for _, v in items]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    bars = ax.bar(keys, values, color=color)
    ax.set_xlabel("bitstring")
    ax.set_ylabel("counts")
    if title is not None:
        ax.set_title(title)
    if keys and max(len(k) for k in keys) > 4:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment("right")
    if bar_labels:
        for bar, v in zip(bars, values):
            ax.annotate(
                str(v),
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    fig.tight_layout()
    return fig


def _reduced_density_matrix(
    state: npt.ArrayLike, qubit: int
) -> npt.NDArray[np.complex128]:
    """statevector → 지정 큐비트의 2×2 reduced density matrix.

    panta-sim 컨벤션: state index ``i`` 의 qubit ``k`` bit = ``(i >> k) & 1``.
    numpy ``reshape([2]*n)`` 의 axis 0 = MSB = qubit ``n-1``, axis ``n-1`` =
    LSB = qubit 0. 따라서 keep axis = ``n - 1 - qubit``.

    Args:
        state: 길이 ``2^n`` complex array.
        qubit: ``0 <= qubit < n``.

    Returns:
        2×2 ``np.complex128`` density matrix ρ. ``Tr(ρ) ≈ 1``.
    """
    psi = np.asarray(state, dtype=np.complex128).ravel()
    if psi.size == 0:
        raise ValueError("empty state vector")
    n = int(round(math.log2(psi.size)))
    if 2 ** n != psi.size:
        raise ValueError(
            f"state vector length {psi.size} is not a power of 2"
        )
    if not 0 <= qubit < n:
        raise ValueError(
            f"qubit must satisfy 0 <= qubit < {n}, got {qubit}"
        )
    if n == 1:
        return np.outer(psi, psi.conj())
    psi_t = psi.reshape([2] * n)
    keep_axis = n - 1 - qubit
    psi_moved = np.moveaxis(psi_t, keep_axis, 0)
    psi_flat = psi_moved.reshape(2, -1)
    return psi_flat @ psi_flat.conj().T


def _bloch_vector(rho: npt.NDArray[np.complex128]) -> Tuple[float, float, float]:
    """2×2 density matrix → Bloch 좌표 (r_x, r_y, r_z)."""
    r_x = float(2 * rho[0, 1].real)
    r_y = float(2 * rho[1, 0].imag)
    r_z = float((rho[0, 0] - rho[1, 1]).real)
    return r_x, r_y, r_z


def plot_bloch(
    state: npt.ArrayLike,
    qubit: int = 0,
    *,
    figsize: Optional[Tuple[float, float]] = None,
    ax: Optional[Any] = None,
    title: Optional[str] = None,
) -> Any:
    """statevector 의 Bloch sphere 시각화.

    다큐빗 입력 시 자동으로 partial trace 를 수행해서 ``qubit`` 번 큐비트의
    reduced density matrix 를 추출. mixed state 는 구 내부 점으로 표시.

    Args:
        state: 길이 ``2^n`` complex array (panta-sim ``run().statevector()``).
        qubit: 시각화할 큐비트 인덱스. 1큐빗일 땐 0 (default).
        figsize: 새 figure 의 ``(width, height)`` (인치).
        ax: 기존 3D Axes 에 그리려면 전달.
        title: 차트 제목.

    Returns:
        ``matplotlib.figure.Figure``.

    Raises:
        ValueError: 비트 길이가 2^n 아님 / qubit 범위 벗어남 / |r| > 1.
        ImportError: matplotlib 미설치 시.
    """
    plt = _lazy_import_pyplot()
    rho = _reduced_density_matrix(state, qubit)
    r_x, r_y, r_z = _bloch_vector(rho)
    r_norm = math.sqrt(r_x * r_x + r_y * r_y + r_z * r_z)
    if r_norm > 1.0 + 1e-9:
        raise ValueError(
            f"Bloch vector norm {r_norm:.6f} > 1 — invalid quantum state"
        )

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    u = np.linspace(0.0, 2.0 * np.pi, 30)
    v = np.linspace(0.0, np.pi, 20)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(sx, sy, sz, color="lightgray", linewidth=0.4, alpha=0.6)

    axis_len = 1.2
    ax.plot([-axis_len, axis_len], [0, 0], [0, 0], color="gray", linewidth=0.5)
    ax.plot([0, 0], [-axis_len, axis_len], [0, 0], color="gray", linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-axis_len, axis_len], color="gray", linewidth=0.5)

    ax.text(axis_len, 0, 0, "|+⟩", fontsize=10)
    ax.text(-axis_len, 0, 0, "|−⟩", fontsize=10)
    ax.text(0, axis_len, 0, "|+i⟩", fontsize=10)
    ax.text(0, -axis_len, 0, "|−i⟩", fontsize=10)
    ax.text(0, 0, axis_len, "|0⟩", fontsize=10)
    ax.text(0, 0, -axis_len, "|1⟩", fontsize=10)

    ax.quiver(0, 0, 0, r_x, r_y, r_z, color="red", linewidth=2.0, arrow_length_ratio=0.1)
    ax.scatter([r_x], [r_y], [r_z], color="red", s=40)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if title is not None:
        ax.set_title(title)
    try:
        ax.set_box_aspect((1, 1, 1))
    except (AttributeError, NotImplementedError):
        pass
    return fig
