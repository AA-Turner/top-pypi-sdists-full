"""시뮬레이션 결과 클래스."""

from __future__ import annotations

from typing import Dict

import numpy as np
import numpy.typing as npt


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
