"""시뮬레이션 결과 클래스."""

from __future__ import annotations

from typing import Dict

import numpy as np
import numpy.typing as npt

_PAULI_CODE = {"I": 0, "X": 1, "Y": 2, "Z": 3}


def _apply_1q_np(psi: np.ndarray, u: np.ndarray, qubit: int, n: int) -> np.ndarray:
    """단일 큐비트 행렬 ``u`` 를 statevector ``psi`` 의 ``qubit`` 에 적용 (numpy).

    little-endian: index bit ``qubit`` (값 ``1<<qubit``) 이 해당 큐비트.
    """
    t = psi.reshape([2] * n)  # axis a ↔ qubit (n-1-a)
    axis = n - 1 - qubit
    t = np.tensordot(u, t, axes=([1], [axis]))  # 새 축 0 = 출력 물리 index
    t = np.moveaxis(t, 0, axis)
    return t.reshape(-1)


def _apply_1q_density(rho: np.ndarray, u: np.ndarray, qubit: int, n: int) -> np.ndarray:
    """density matrix ``rho`` 에 ``U ρ U†`` (단일 큐비트 ``qubit``) 를 적용 (numpy)."""
    t = rho.reshape([2] * n + [2] * n)
    rax = n - 1 - qubit  # row 축
    t = np.moveaxis(np.tensordot(u, t, axes=([1], [rax])), 0, rax)
    cax = 2 * n - 1 - qubit  # col 축: ρ U† → conj(U) 로 수축
    t = np.moveaxis(np.tensordot(u.conj(), t, axes=([1], [cax])), 0, cax)
    return t.reshape(1 << n, 1 << n)


def _bit_parity(x: np.ndarray) -> np.ndarray:
    """정수 배열의 비트 패리티 (popcount mod 2) — 벡터화."""
    x = x.astype(np.uint64).copy()
    x ^= x >> np.uint64(32)
    x ^= x >> np.uint64(16)
    x ^= x >> np.uint64(8)
    x ^= x >> np.uint64(4)
    x ^= x >> np.uint64(2)
    x ^= x >> np.uint64(1)
    return (x & np.uint64(1)).astype(np.int64)


def _label_to_codes(label: str) -> list[int]:
    """Pauli string 라벨 → per-qubit 코드 (오른쪽 끝 = 큐비트 0)."""
    n = len(label)
    codes = [0] * n
    for pos, ch in enumerate(label):
        codes[n - 1 - pos] = _PAULI_CODE[ch]
    return codes


def _parse_observable(observable) -> list[tuple[list[int], float, float]]:
    """Pauli observable 을 Rust 의 ``(paulis, coeff_re, coeff_im)`` 형식으로 변환.

    각 Pauli string (Qiskit label 컨벤션, 오른쪽 끝 = 큐비트 0) 을 per-qubit
    코드 리스트 ``paulis[q] ∈ {0=I,1=X,2=Y,3=Z}`` 로 변환한다.  ``dict`` /
    ``list[(str, coeff)]`` / Qiskit ``SparsePauliOp`` 를 받는다.
    """
    # Qiskit SparsePauliOp → list[(label, coeff)].
    if hasattr(observable, "to_list") and not isinstance(observable, (list, tuple, dict)):
        items = list(observable.to_list())
    elif isinstance(observable, dict):
        items = list(observable.items())
    elif isinstance(observable, (list, tuple)):
        items = list(observable)
    else:
        raise TypeError(
            f"observable 은 dict / list[(str, coeff)] / SparsePauliOp 여야 합니다 "
            f"(입력: {type(observable).__name__})"
        )

    terms: list[tuple[list[int], float, float]] = []
    n_qubits = None
    for label, coeff in items:
        label = str(label).upper()
        if n_qubits is None:
            n_qubits = len(label)
        elif len(label) != n_qubits:
            raise ValueError(
                f"observable 의 Pauli string 길이가 일관되지 않습니다 "
                f"({len(label)} vs {n_qubits})"
            )
        n = len(label)
        paulis = [0] * n
        for pos, ch in enumerate(label):
            if ch not in _PAULI_CODE:
                raise ValueError(f"잘못된 Pauli 문자 {ch!r} (I/X/Y/Z 만 허용)")
            # 라벨 오른쪽 끝(pos = n-1)이 큐비트 0.
            paulis[n - 1 - pos] = _PAULI_CODE[ch]
        c = complex(coeff)
        terms.append((paulis, float(c.real), float(c.imag)))
    return terms


# 단일 큐비트 Pauli 곱 표 σ_a·σ_b = phase·σ_c.  코드 0=I,1=X,2=Y,3=Z.
_PAULI_PRODUCT = {
    (0, 0): (0, 1 + 0j), (0, 1): (1, 1 + 0j), (0, 2): (2, 1 + 0j), (0, 3): (3, 1 + 0j),
    (1, 0): (1, 1 + 0j), (1, 1): (0, 1 + 0j), (1, 2): (3, 1j), (1, 3): (2, -1j),
    (2, 0): (2, 1 + 0j), (2, 1): (3, -1j), (2, 2): (0, 1 + 0j), (2, 3): (1, 1j),
    (3, 0): (3, 1 + 0j), (3, 1): (2, 1j), (3, 2): (1, -1j), (3, 3): (0, 1 + 0j),
}


def _pauli_sum_square(terms: list) -> list:
    """Pauli sum ``H = Σ cᵢ Pᵢ`` 의 제곱 ``H²`` 를 Pauli sum 으로 전개한다.

    ``Pᵢ Pⱼ`` 를 단일 Pauli + 위상으로 곱해 같은 string 끼리 합친다.  결과는
    ``(codes, re, im)`` 리스트.
    """
    acc: dict = {}
    for paulis_a, ra, ia in terms:
        ca = complex(ra, ia)
        for paulis_b, rb, ib in terms:
            cb = complex(rb, ib)
            phase = 1 + 0j
            res_codes = []
            for a, b in zip(paulis_a, paulis_b):
                code, ph = _PAULI_PRODUCT[(a, b)]
                res_codes.append(code)
                phase *= ph
            coeff = ca * cb * phase
            key = tuple(res_codes)
            acc[key] = acc.get(key, 0j) + coeff
    return [(list(codes), c.real, c.imag) for codes, c in acc.items() if abs(c) > 1e-15]


class _StabilizerRaw:
    """``method="stabilizer"`` 결과의 경량 raw 어댑터.

    Stabilizer (Clifford) 백엔드는 수천 큐비트를 대상으로 하므로 전체 2ⁿ
    statevector / probabilities / density matrix 를 생성하지 않는다.  측정
    ``counts`` 만 보유하고, 나머지 접근은 명확한 에러로 막는다.  [`SimulationResult`]
    가 이 객체를 다른 백엔드의 raw 결과와 동일하게 래핑한다.
    """

    def __init__(self, counts: Dict[str, int]) -> None:
        self._counts = dict(counts)

    @property
    def precision(self) -> str:
        return "n/a"

    @property
    def backend(self) -> str:
        return "stabilizer"

    @property
    def mps_max_bond_dim(self):
        return None

    @property
    def mps_final_norm_sq(self):
        return None

    @property
    def mps_truncation_error_sum(self):
        return None

    @property
    def mps_trunc_threshold(self):
        return None

    @property
    def mps_observed_max_bond_dim(self):
        return None

    def counts(self) -> Dict[str, int]:
        return dict(self._counts)

    def statevector(self):
        raise NotImplementedError(
            "stabilizer 백엔드는 전체 statevector 를 생성하지 않습니다 "
            "(수천 큐비트 Clifford 회로 대상). counts() 만 사용하세요."
        )

    def density_matrix(self):
        raise NotImplementedError("stabilizer 백엔드는 density_matrix 를 지원하지 않습니다.")

    def probabilities(self):
        raise NotImplementedError(
            "stabilizer 백엔드는 전체 probabilities 를 지원하지 않습니다 (counts() 사용)."
        )

    def expectation(self, terms):
        raise NotImplementedError(
            "stabilizer 백엔드는 statevector 기반 expectation 을 지원하지 않습니다."
        )


class SimulationResult:
    """시뮬레이션 실행 결과를 래핑하는 클래스.

    Rust SimulationResult를 감싸서 Python에서 편리하게 사용할 수 있게 한다.

    정밀도(``f32`` / ``f64``)에 따라 ``statevector()`` / ``probabilities()`` 가
    반환하는 numpy dtype 이 달라진다 — Rust 가 native dtype 을 직접 노출하므로
    Python wrapper 가 추가 cast 를 하지 않는다 (메모리 절약).
    """

    def __init__(self, raw_result: object) -> None:
        self._raw = raw_result

    @property
    def precision(self) -> str:
        """시뮬레이션에 사용된 정밀도 (``"f32"`` 또는 ``"f64"``)."""
        return self._raw.precision

    @property
    def backend(self) -> str:
        """시뮬레이션에 사용된 백엔드.

        - ``"statevector"`` (default): state vector 경로.
        - ``"density_matrix"``: density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` 직접 진화.
          noise 가 있어도 deterministic Kraus 적용.
        - ``"mps"`` (v0.6.0 / v0.6.1): Matrix Product State.  N > 20 의 경우
          ``statevector()`` 는 ``ValueError`` (dense SV 가 메모리상 불가능),
          ``counts()`` 만 사용 가능.  결과의 ``mps_max_bond_dim`` /
          ``mps_final_norm_sq`` 로 truncation 메타 확인.
        """
        return self._raw.backend

    @property
    def mps_max_bond_dim(self) -> int | None:
        """MPS 백엔드의 사용자 지정 χ_max (v0.6.0).  비-MPS 결과면 ``None``."""
        return self._raw.mps_max_bond_dim

    @property
    def mps_final_norm_sq(self) -> float | None:
        """MPS 백엔드의 SVD truncation 후 squared norm (v0.6.0).

        1.0 보다 작으면 ``max_bond_dim`` 부족 (정보 손실 발생).  사용자는 χ 를
        늘리거나 회로의 entanglement 를 줄여야 한다.  비-MPS 결과면 ``None``.
        """
        return self._raw.mps_final_norm_sq

    @property
    def mps_truncation_error_sum(self) -> float | None:
        """MPS 백엔드의 누적 SVD discarded weight (v0.6.3).

        Schollwöck 2011 §4.5.3 의 표준 절대 metric:
        ``Σ_{SVDs} Σ_{j>=keep} sv_j²`` — 회로 실행 중 모든 truncating SVD
        에서 잘려나간 singular value² 의 누적합.  ``mps_final_norm_sq`` 와
        달리 *최종 norm* 이 아닌 *누적 손실* 을 측정하므로 회로 전체의
        정확도 metric 으로 사용한다.

        - ``0.0`` — 무손실 (max_bond_dim ≥ 실제 Schmidt rank).
        - 작은 양수 — 약간의 정보 손실.  대부분의 VQE/QAOA 응용에서
          ``< 1e-6`` 정도면 결과 신뢰 가능.
        - 큰 양수 — 정보 손실 큼, χ 를 늘려야 함.

        v0.6.5 부터 ``trunc_threshold > 0`` 인 경우엔 ``right_canonicalize``
        의 thin SVD 에서 잘려나간 mode 도 함께 누적된다 (eps cutoff).
        ``trunc_threshold = 0`` (default) 일 땐 v0.6.3 동일 — 오직
        ``apply_two_qubit_adjacent`` 의 rank-capping SVD 만 누적.  비-MPS
        결과면 ``None``.
        """
        return self._raw.mps_truncation_error_sum

    @property
    def mps_trunc_threshold(self) -> float | None:
        """MPS 백엔드의 사용자 지정 singular-value cutoff (v0.6.5).

        ``0.0`` 이면 disabled — ``mps_max_bond_dim`` 만으로 truncation.
        양수면 adaptive truncation 활성 (Schollwöck 2011 §4.5.3 ε-rank).
        비-MPS 결과면 ``None``.
        """
        return self._raw.mps_trunc_threshold

    @property
    def mps_observed_max_bond_dim(self) -> int | None:
        """MPS 백엔드가 회로 종료 시점에 실제로 발생한 최대 internal bond
        dimension (v0.6.5).

        adaptive truncation (``trunc_threshold > 0``) 활성 시 일반적으로
        ``mps_max_bond_dim`` 보다 작다 — 회로의 실제 entanglement 양에
        자동 맞춤.  큰 값이면 회로가 가용 χ_max 를 다 쓰고 있다는 신호 →
        χ_max 를 늘리거나 cutoff 를 완화하면 정확도 향상 가능.  비-MPS
        결과면 ``None``.
        """
        return self._raw.mps_observed_max_bond_dim

    def counts(self) -> Dict[str, int]:
        """측정 결과 카운트를 딕셔너리로 반환한다.

        Returns:
            비트 문자열을 키로, 측정 횟수를 값으로 하는 딕셔너리.
        """
        return dict(self._raw.counts())

    def statevector(self) -> npt.NDArray[np.complexfloating]:
        """측정 전 최종 상태 벡터를 numpy 배열로 반환한다.

        dtype 은 시뮬레이션 정밀도를 따른다:

        - f64 정밀도 → ``numpy.complex128``
        - f32 정밀도 → ``numpy.complex64``

        density backend 결과에 호출하면 ``ValueError`` — ``density_matrix()``
        를 사용하라.

        Returns:
            1D numpy 배열 (정밀도별 native dtype).
        """
        return self._raw.statevector()

    def expectation(self, observable, shots: int | None = None, seed: int | None = None) -> float:
        """Pauli observable `H = Σ cᵢ Pᵢ` 의 기댓값 `⟨ψ|H|ψ⟩` 를 반환한다 (v0.7).

        2ⁿ × 2ⁿ 행렬을 만들지 않고 statevector 에 직접 작용시켜 계산하므로
        20~25큐비트까지 확장된다 (Qiskit 의존성 없음).  Hermitian observable
        이면 실수값을 반환한다.

        Args:
            observable: 다음 중 하나 —

                - ``dict``: ``{"ZZ": 1.0, "XX": 0.5}`` (Qiskit Pauli label
                  컨벤션 — 라벨의 오른쪽 끝 문자가 큐비트 0).
                - ``list``: ``[("ZZ", 1.0), ("IX", 0.5j), ...]``.
                - Qiskit ``SparsePauliOp`` (설치돼 있으면 자동 변환).

        Returns:
            기댓값 (``float``, 실수부).

        Args (추가):
            shots: ``None`` (기본) 이면 정확한 해석적 기댓값.  양의 정수면
                **shot-based 추정** — 각 Pauli 측정 기저로 statevector 를 회전해
                ``shots`` 회 샘플링하고 `⟨P⟩` 를 추정한다 (NISQ 현실성, shot
                noise 포함).  ``shots → ∞`` 에서 정확값으로 수렴.  같은 측정
                기저를 공유하는 항은 동일 샘플에서 추정 (qubit-wise commuting
                grouping).
            seed: shot-based 추정의 RNG seed (재현성).

        Raises:
            ValueError: density 백엔드 결과이거나 dense statevector 가 없는
                (N>20) MPS 결과일 때, 또는 Pauli string 길이가 큐비트 수와
                불일치할 때.
        """
        terms = _parse_observable(observable)
        if shots is None:
            return self._raw.expectation(terms)
        return self._sampled_expectation(terms, int(shots), seed)

    def _sampled_expectation(self, terms, shots: int, seed) -> float:
        """shot-based Pauli 기댓값 추정 (qubit-wise grouping).

        statevector 백엔드는 ``|ψ⟩`` 를 측정 기저로 회전 후 Born-rule 샘플링,
        density 백엔드는 ``U ρ U†`` 의 대각 (측정 확률) 에서 샘플링한다 (noisy
        observable 의 finite-shot 추정).  MPS (N>20, dense SV 없음) 는 미지원.
        """
        backend = self.backend
        H = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
        # Y 측정: S† 후 H → Z 측정.  HS† 를 한 행렬로.
        Sdg = np.array([[1, 0], [0, -1j]], dtype=np.complex128)
        HSdg = H @ Sdg

        if backend == "density_matrix":
            rho = np.asarray(self.density_matrix(), dtype=np.complex128)
            dim = rho.shape[0]
            n = int(round(np.log2(dim)))
            state = rho
            is_density = True
        else:
            psi = np.asarray(self.statevector(), dtype=np.complex128)
            dim = psi.shape[0]
            n = int(round(np.log2(dim)))
            state = psi
            is_density = False
        rng = np.random.default_rng(seed)

        # 측정 기저별로 항 grouping (qubit-wise commuting).
        groups: dict = {}
        for paulis, re, im in terms:
            # 측정 기저는 X/Y 위치만 중요 (I/Z 는 Z 측정).
            key = tuple(0 if p in (0, 3) else p for p in paulis)
            groups.setdefault(key, []).append((paulis, complex(re, im)))
        total = 0.0
        for key, group in groups.items():
            rotated = state
            for q in range(n):
                u = H if key[q] == 1 else HSdg if key[q] == 2 else None
                if u is None:
                    continue
                rotated = (
                    _apply_1q_density(rotated, u, q, n)
                    if is_density
                    else _apply_1q_np(rotated, u, q, n)
                )
            if is_density:
                probs = np.clip(np.real(np.diagonal(rotated)), 0.0, None)
            else:
                probs = np.abs(rotated) ** 2
            probs = probs / probs.sum()
            samples = rng.choice(dim, size=shots, p=probs)
            for paulis, coeff in group:
                mask = 0
                for q in range(n):
                    if paulis[q] != 0:
                        mask |= 1 << q
                parity = _bit_parity(samples & mask)
                ev = np.where(parity == 0, 1.0, -1.0)
                total += (coeff * ev.mean()).real
        return total

    def variance(self, observable) -> float:
        """Pauli observable `H` 의 분산 `⟨H²⟩ - ⟨H⟩²` 를 반환한다 (v0.7.1).

        `H` (Hermitian) 의 제곱을 Pauli sum 으로 전개해 (`Pᵢ Pⱼ` 곱) `⟨H²⟩`
        를 구하고 `⟨H⟩²` 를 뺀다.  VQE 에너지 오차 막대 / 물리량 요동 측정용.
        statevector / density / MPS 백엔드 모두에서 동작 (`expectation` 과 동일).

        Args:
            observable: Pauli observable (dict / list / SparsePauliOp).

        Returns:
            분산 (``float``, ≥ 0; 수치 오차로 인한 미세 음수는 0 으로 clamp).
        """
        terms = _parse_observable(observable)
        exp_h = float(self._raw.expectation(terms))
        h2_terms = _pauli_sum_square(terms)
        exp_h2 = float(self._raw.expectation(h2_terms))
        return max(exp_h2 - exp_h * exp_h, 0.0)

    def local_expectations(self, pauli: str = "Z") -> npt.NDArray[np.floating]:
        """각 큐비트의 단일 Pauli 기댓값 ``[⟨Pᵢ⟩ for i in 0..n-1]`` 를 반환한다 (v0.7.1).

        스핀 모델의 자기화 프로파일 ``⟨Zᵢ⟩`` / ``⟨Xᵢ⟩`` 등에 사용.  큐비트 0 부터
        오름차순.  전 백엔드 (statevector / density / MPS).

        Args:
            pauli: ``"X"`` / ``"Y"`` / ``"Z"`` 중 하나.

        Returns:
            길이 ``n`` 의 ``float`` 배열.
        """
        pauli = pauli.upper()
        if pauli not in ("X", "Y", "Z"):
            raise ValueError(f"pauli 는 X/Y/Z 중 하나여야 합니다 (입력 {pauli!r})")
        n = self._observable_n()
        out = np.empty(n, dtype=float)
        for i in range(n):
            label = ["I"] * n
            label[n - 1 - i] = pauli
            out[i] = self._raw.expectation([(_label_to_codes("".join(label)), 1.0, 0.0)])
        return out

    def correlation_matrix(self, pauli: str = "Z", *, connected: bool = False) -> npt.NDArray[np.floating]:
        """2점 상관 행렬 ``Cᵢⱼ = ⟨Pᵢ Pⱼ⟩`` 를 반환한다 (v0.7.1).

        스핀 모델 상관함수 / 구조 인자에 사용.  ``connected=True`` 면
        ``⟨PᵢPⱼ⟩ - ⟨Pᵢ⟩⟨Pⱼ⟩`` (연결 상관).  대각 ``Cᵢᵢ = ⟨Pᵢ²⟩ = 1``
        (connected 면 ``1 - ⟨Pᵢ⟩²``).

        Args:
            pauli: ``"X"`` / ``"Y"`` / ``"Z"``.
            connected: 연결 상관 여부.

        Returns:
            ``n × n`` 대칭 ``float`` 배열.
        """
        pauli = pauli.upper()
        if pauli not in ("X", "Y", "Z"):
            raise ValueError(f"pauli 는 X/Y/Z 중 하나여야 합니다 (입력 {pauli!r})")
        n = self._observable_n()
        c = np.empty((n, n), dtype=float)
        for i in range(n):
            for j in range(i, n):
                label = ["I"] * n
                if i == j:
                    val = 1.0  # Pᵢ² = I
                else:
                    label[n - 1 - i] = pauli
                    label[n - 1 - j] = pauli
                    val = float(self._raw.expectation([(_label_to_codes("".join(label)), 1.0, 0.0)]))
                c[i, j] = c[j, i] = val
        if connected:
            loc = self.local_expectations(pauli)
            c = c - np.outer(loc, loc)
        return c

    def _observable_n(self) -> int:
        """관측량 헬퍼용 큐비트 수 (dense 상태를 만들지 않고도 결정).

        MPS ``N > 20`` 결과는 ``statevector()`` / ``density_matrix()`` 가 모두
        실패하지만 ``raw.expectation`` (MPS-direct) 은 동작한다 — 그 경우에도
        ``local_expectations()`` / ``correlation_matrix()`` 가 쓰일 수 있도록
        counts 비트열 폭, 마지막으로 항등 Pauli string 프로브로 폴백한다.
        """
        try:
            return int(round(np.log2(len(self.statevector()))))
        except (ValueError, NotImplementedError):
            pass
        try:
            return int(round(np.log2(self.density_matrix().shape[0])))
        except (ValueError, NotImplementedError):
            pass
        # shots > 0 결과: counts 비트열 폭 = 큐비트 수.
        counts = self.counts()
        if counts:
            return len(next(iter(counts)))
        # MPS shots=0 N>20: dense 접근 없이 raw.expectation 의 길이 검증을
        # 프로브 — 항등 Pauli string 길이가 큐비트 수와 일치할 때만 성공한다.
        for n in range(1, 8193):
            try:
                self._raw.expectation([([0] * n, 1.0, 0.0)])
                return n
            except ValueError:
                continue
        raise ValueError(
            "큐비트 수를 결정할 수 없습니다 — statevector/density_matrix/counts "
            "가 모두 없는 결과입니다."
        )

    def density_matrix(self) -> npt.NDArray[np.complexfloating]:
        """Density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` 를 numpy 2D ndarray 로 반환한다 (v0.5.0).

        dtype 은 시뮬레이션 정밀도를 따른다 (``complex128`` / ``complex64``).
        statevector backend 결과에 호출하면 ``ValueError``.

        반환된 행렬은 row-major: ``rho[i][j]`` = ρ_{ij}, hermitian (ρ = ρ†),
        positive semi-definite, ``Tr(ρ) = 1`` (trace-preserving 채널이면).

        Returns:
            2D numpy 배열 (shape `(2ⁿ, 2ⁿ)`).
        """
        return self._raw.density_matrix()

    def probabilities(self) -> npt.NDArray[np.floating]:
        """각 basis state의 확률을 numpy 배열로 반환한다.

        dtype 은 시뮬레이션 정밀도를 따른다 (``float64`` / ``float32``).
        statevector 백엔드: ``|ψ_b|²``.  density 백엔드: ``ρ[b][b]`` (대각선).

        Returns:
            1D numpy 배열.
        """
        return self._raw.probabilities()

    def plot_histogram(self, **kwargs):  # type: ignore[no-untyped-def]
        """측정 카운트의 matplotlib 히스토그램 Figure 를 반환한다.

        ``panta_sim.plot_histogram(self.counts(), **kwargs)`` 의 alias.
        matplotlib 이 설치되어 있어야 한다 (``pip install panta-sim[viz]``).

        Args:
            **kwargs: ``figsize``, ``ax``, ``title``, ``color``, ``bar_labels``.

        Returns:
            ``matplotlib.figure.Figure``.
        """
        from .visualize import plot_histogram

        return plot_histogram(self.counts(), **kwargs)

    def histogram_text(self, width: int = 40, style: str = "unicode") -> str:
        """측정 카운트의 텍스트 막대 그래프를 반환한다 (matplotlib 불필요).

        Args:
            width: 막대의 최대 폭.
            style: ``"unicode"`` (default) 또는 ``"ascii"``.

        Returns:
            줄 바꿈된 문자열.
        """
        from .visualize import histogram_text

        return histogram_text(self.counts(), width=width, style=style)
