//! Density matrix backend (v0.5.0).
//!
//! n큐비트 양자 상태의 density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` 를 row-major flat
//! `Vec<Complex<F>>` 로 표현한다. statevector 와 달리 **mixed state 를 자연스럽게
//! 표현** — noise 가 있는 회로에서 trajectory 의 통계 불확실성 없이 결정적
//! 진화를 얻을 수 있다 (Aer `method="density_matrix"` 와 동일 의미).
//!
//! 메모리: dim × dim = 4ⁿ complex.
//! - N=10:  4¹⁰ × 16B (f64) = 16 MB
//! - N=12:  4¹² × 16B = 256 MB
//! - N=14:  4¹⁴ × 16B = 4 GB (실용 한계)
//! - N≥15:  권장 안 함 (statevector + trajectory 조합 사용)
//!
//! 핵심 알고리즘 (qubit-wise block update):
//! - **Unitary `ρ → U_q ρ U_q†`**: row 인덱스의 q-th bit pair 결합 (left
//!   multiply U) 후 column 인덱스의 q-th bit pair 결합 (right multiply U†) —
//!   2 pass, in-place, O(4ⁿ) FLOPs.
//! - **Kraus `ρ → Σᵢ Kᵢ ρ Kᵢ†`**: 단일 큐비트 4-element block 순회,
//!   `ρ_blk' = Σᵢ Kᵢ ρ_blk Kᵢ†` 를 in-place 로 누적.  temp 버퍼 0,
//!   메모리 1×.
//!
//! 참고:
//! - refs.md #15 노이즈 수학적 모델링 (Kraus 형식).
//! - Aer `method="density_matrix"` (qubit-wise block update 패턴).

use num_complex::Complex;
use num_traits::NumCast;
use rand::Rng;

use crate::complex::{one, zero, Real};
use crate::gates::{Matrix2x2, Matrix4x4};
use crate::statevector::StateVector;

/// n큐비트 양자 상태의 density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)`.
///
/// row-major flat `Vec<Complex<F>>` (length = `dim²`, `dim = 2ⁿ`).  인덱스는
/// `data[r * dim + c]` 로 ρ[r][c] 에 대응.
///
/// 정밀도 `F` 는 [`Real`] (f32 / f64) — `StateVector<F>` 와 동일 generic 패턴.
#[derive(Debug, Clone)]
pub struct DensityMatrix<F: Real> {
    n_qubits: usize,
    dim: usize,
    data: Vec<Complex<F>>,
}

impl<F: Real> DensityMatrix<F> {
    /// `|0⟩⟨0|⊗ⁿ` 로 초기화된 density matrix 를 생성한다.
    ///
    /// `data[0]` 만 1, 나머지는 0.
    pub fn new(n_qubits: usize) -> Self {
        assert!(n_qubits > 0, "qubit 수는 1 이상이어야 합니다");
        let dim = 1usize << n_qubits;
        let mut data = vec![zero::<F>(); dim * dim];
        data[0] = one::<F>();
        Self {
            n_qubits,
            dim,
            data,
        }
    }

    /// 순수 상태 |ψ⟩ → ρ = |ψ⟩⟨ψ| 변환 (테스트 / 비교용).
    pub fn from_pure_state(state: &StateVector<F>) -> Self {
        let n = state.num_qubits();
        let dim = state.dim();
        let amps = state.amplitudes();
        let mut data = vec![zero::<F>(); dim * dim];
        for i in 0..dim {
            for j in 0..dim {
                data[i * dim + j] = amps[i] * amps[j].conj();
            }
        }
        Self {
            n_qubits: n,
            dim,
            data,
        }
    }

    pub fn num_qubits(&self) -> usize {
        self.n_qubits
    }

    pub fn dim(&self) -> usize {
        self.dim
    }

    pub fn data(&self) -> &[Complex<F>] {
        &self.data
    }

    pub fn data_mut(&mut self) -> &mut [Complex<F>] {
        &mut self.data
    }

    /// `Tr(ρ)` (대각선 합).  trace-preserving 채널이면 1 에 수렴 — drift 모니터링용.
    ///
    /// 누적은 항상 f64 (정밀도 안전, statevector::normalize 와 동일 패턴).
    pub fn trace(&self) -> Complex<F> {
        let mut re: f64 = 0.0;
        let mut im: f64 = 0.0;
        for i in 0..self.dim {
            let z = self.data[i * self.dim + i];
            re += <f64 as NumCast>::from(z.re).expect("F → f64 변환 실패");
            im += <f64 as NumCast>::from(z.im).expect("F → f64 변환 실패");
        }
        Complex::new(
            F::from(re).expect("f64 → F 변환 실패"),
            F::from(im).expect("f64 → F 변환 실패"),
        )
    }

    /// `ρ → U_q ρ U_q†` (단일 큐비트 unitary).
    ///
    /// in-place 2 pass: 먼저 row 인덱스의 q-th bit pair 결합 (left multiply U),
    /// 그 다음 column 인덱스의 q-th bit pair 결합 (right multiply U†).
    /// statevector 의 [`apply_single_qubit_gate`](crate::operations::apply_single_qubit_gate)
    /// 와 동일 qubit-wise 패턴.
    pub fn apply_unitary_1q(&mut self, u: &Matrix2x2<F>, q: usize) {
        assert!(
            q < self.n_qubits,
            "apply_unitary_1q: target {q} 가 범위 벗어남 (n_qubits={})",
            self.n_qubits
        );
        let dim = self.dim;
        let stride = 1usize << q;
        let m00 = u[0][0];
        let m01 = u[0][1];
        let m10 = u[1][0];
        let m11 = u[1][1];

        // Pass 1: ρ' = U_q ρ — row 인덱스의 q-th bit pair 결합.
        // For each column j: pair (r0, r0 + stride) → [U @ (ρ[r0][j], ρ[r1][j])ᵀ].
        for j in 0..dim {
            let mut r = 0;
            while r < dim {
                for k in r..r + stride {
                    let i0 = k * dim + j;
                    let i1 = (k + stride) * dim + j;
                    let a = self.data[i0];
                    let b = self.data[i1];
                    self.data[i0] = m00 * a + m01 * b;
                    self.data[i1] = m10 * a + m11 * b;
                }
                r += stride << 1;
            }
        }

        // Pass 2: ρ' = ρ U_q† — column 인덱스의 q-th bit pair 결합.
        // U† = [[conj(m00), conj(m10)], [conj(m01), conj(m11)]]
        // [a, b] @ U† = [a · conj(m00) + b · conj(m01),  a · conj(m10) + b · conj(m11)]
        let n00 = m00.conj();
        let n01 = m01.conj();
        let n10 = m10.conj();
        let n11 = m11.conj();
        for i in 0..dim {
            let mut c = 0;
            while c < dim {
                for k in c..c + stride {
                    let i0 = i * dim + k;
                    let i1 = i * dim + (k + stride);
                    let a = self.data[i0];
                    let b = self.data[i1];
                    self.data[i0] = a * n00 + b * n01;
                    self.data[i1] = a * n10 + b * n11;
                }
                c += stride << 1;
            }
        }
    }

    /// `ρ → U ρ U†` (2-큐비트 unitary).  4×4 행렬 인덱스는 `|q1 q0⟩` 순서
    /// (statevector 의 [`apply_two_qubit_gate`](crate::operations::apply_two_qubit_gate)
    /// 와 동일 컨벤션).
    ///
    /// in-place 2 pass: row 인덱스의 `(q1, q0)` 비트 4-pair 결합 (left multiply U)
    /// → column 인덱스의 `(q1, q0)` 비트 4-pair 결합 (right multiply U†).
    pub fn apply_unitary_2q(&mut self, u: &Matrix4x4<F>, q0: usize, q1: usize) {
        assert!(q0 < self.n_qubits && q1 < self.n_qubits && q0 != q1);
        let dim = self.dim;
        let bit0 = 1usize << q0;
        let bit1 = 1usize << q1;
        // 4 인덱스: 00 / 01 / 10 / 11 (q1 q0 순).
        let idx_offsets = [0usize, bit0, bit1, bit0 | bit1];

        // U† 미리 계산.
        let mut udag = [[zero::<F>(); 4]; 4];
        for i in 0..4 {
            for j in 0..4 {
                udag[i][j] = u[j][i].conj();
            }
        }

        let (q_lo, q_hi) = if q0 < q1 { (q0, q1) } else { (q1, q0) };
        let mask_lo = (1usize << q_lo) - 1;
        let mask_mid = ((1usize << (q_hi - 1)) - 1) ^ mask_lo;
        let mask_hi = !((1usize << (q_hi - 1)) - 1);
        let groups = dim >> 2;

        // Pass 1: ρ' = U ρ — row 인덱스의 q0/q1 4-pair 결합.
        for j in 0..dim {
            for k in 0..groups {
                let low = k & mask_lo;
                let mid = (k & mask_mid) << 1;
                let high = (k & mask_hi) << 2;
                let base = high | mid | low;
                let v0 = self.data[(base | idx_offsets[0]) * dim + j];
                let v1 = self.data[(base | idx_offsets[1]) * dim + j];
                let v2 = self.data[(base | idx_offsets[2]) * dim + j];
                let v3 = self.data[(base | idx_offsets[3]) * dim + j];
                self.data[(base | idx_offsets[0]) * dim + j] =
                    u[0][0] * v0 + u[0][1] * v1 + u[0][2] * v2 + u[0][3] * v3;
                self.data[(base | idx_offsets[1]) * dim + j] =
                    u[1][0] * v0 + u[1][1] * v1 + u[1][2] * v2 + u[1][3] * v3;
                self.data[(base | idx_offsets[2]) * dim + j] =
                    u[2][0] * v0 + u[2][1] * v1 + u[2][2] * v2 + u[2][3] * v3;
                self.data[(base | idx_offsets[3]) * dim + j] =
                    u[3][0] * v0 + u[3][1] * v1 + u[3][2] * v2 + u[3][3] * v3;
            }
        }

        // Pass 2: ρ' = ρ U† — column 인덱스의 q0/q1 4-pair 결합.
        for i in 0..dim {
            for k in 0..groups {
                let low = k & mask_lo;
                let mid = (k & mask_mid) << 1;
                let high = (k & mask_hi) << 2;
                let base = high | mid | low;
                let v0 = self.data[i * dim + (base | idx_offsets[0])];
                let v1 = self.data[i * dim + (base | idx_offsets[1])];
                let v2 = self.data[i * dim + (base | idx_offsets[2])];
                let v3 = self.data[i * dim + (base | idx_offsets[3])];
                // [v0 v1 v2 v3] @ U† row by row.
                self.data[i * dim + (base | idx_offsets[0])] =
                    v0 * udag[0][0] + v1 * udag[1][0] + v2 * udag[2][0] + v3 * udag[3][0];
                self.data[i * dim + (base | idx_offsets[1])] =
                    v0 * udag[0][1] + v1 * udag[1][1] + v2 * udag[2][1] + v3 * udag[3][1];
                self.data[i * dim + (base | idx_offsets[2])] =
                    v0 * udag[0][2] + v1 * udag[1][2] + v2 * udag[2][2] + v3 * udag[3][2];
                self.data[i * dim + (base | idx_offsets[3])] =
                    v0 * udag[0][3] + v1 * udag[1][3] + v2 * udag[2][3] + v3 * udag[3][3];
            }
        }
    }

    /// `ρ → C-U_(ctrl,tgt) ρ C-U_(ctrl,tgt)†` (controlled 1-큐비트 unitary).
    ///
    /// 의미: row/col 인덱스의 ctrl bit 가 1 인 element 에만 U 의 row/col pass 적용.
    /// statevector [`apply_controlled_gate`](crate::operations::apply_controlled_gate) 와
    /// 동일 의미. CNOT / CY / CH / CRx / CRy / CRz / CP / CU3 / CU 모두 이 path.
    pub fn apply_controlled_1q(&mut self, u: &Matrix2x2<F>, ctrl: usize, tgt: usize) {
        assert!(ctrl != tgt && ctrl < self.n_qubits && tgt < self.n_qubits);
        let dim = self.dim;
        let ctrl_bit = 1usize << ctrl;
        let tgt_stride = 1usize << tgt;
        let m00 = u[0][0];
        let m01 = u[0][1];
        let m10 = u[1][0];
        let m11 = u[1][1];
        let n00 = m00.conj();
        let n01 = m01.conj();
        let n10 = m10.conj();
        let n11 = m11.conj();

        // Pass 1: row 인덱스의 ctrl bit=1, tgt bit=0 (그리고 짝 +tgt_stride) pair 만 결합.
        for j in 0..dim {
            for i in 0..dim {
                if (i & ctrl_bit) != 0 && (i & tgt_stride) == 0 {
                    let i0 = i * dim + j;
                    let i1 = (i | tgt_stride) * dim + j;
                    let a = self.data[i0];
                    let b = self.data[i1];
                    self.data[i0] = m00 * a + m01 * b;
                    self.data[i1] = m10 * a + m11 * b;
                }
            }
        }
        // Pass 2: column 인덱스의 ctrl bit=1, tgt bit=0 pair 결합 (right multiply U†).
        for i in 0..dim {
            for j in 0..dim {
                if (j & ctrl_bit) != 0 && (j & tgt_stride) == 0 {
                    let j0 = i * dim + j;
                    let j1 = i * dim + (j | tgt_stride);
                    let a = self.data[j0];
                    let b = self.data[j1];
                    self.data[j0] = a * n00 + b * n01;
                    self.data[j1] = a * n10 + b * n11;
                }
            }
        }
    }

    /// `ρ → CC-U ρ CC-U†` (이중 제어 1-큐비트 unitary, Toffoli 일반화).
    ///
    /// 의미: row/col 인덱스의 c1, c2 둘 다 1 인 element 에만 U 적용.
    pub fn apply_doubly_controlled_1q(
        &mut self,
        u: &Matrix2x2<F>,
        c1: usize,
        c2: usize,
        tgt: usize,
    ) {
        assert!(c1 != c2 && c1 != tgt && c2 != tgt);
        assert!(c1 < self.n_qubits && c2 < self.n_qubits && tgt < self.n_qubits);
        let dim = self.dim;
        let c1_bit = 1usize << c1;
        let c2_bit = 1usize << c2;
        let tgt_stride = 1usize << tgt;
        let m00 = u[0][0];
        let m01 = u[0][1];
        let m10 = u[1][0];
        let m11 = u[1][1];
        let n00 = m00.conj();
        let n01 = m01.conj();
        let n10 = m10.conj();
        let n11 = m11.conj();

        for j in 0..dim {
            for i in 0..dim {
                if (i & c1_bit) != 0 && (i & c2_bit) != 0 && (i & tgt_stride) == 0 {
                    let i0 = i * dim + j;
                    let i1 = (i | tgt_stride) * dim + j;
                    let a = self.data[i0];
                    let b = self.data[i1];
                    self.data[i0] = m00 * a + m01 * b;
                    self.data[i1] = m10 * a + m11 * b;
                }
            }
        }
        for i in 0..dim {
            for j in 0..dim {
                if (j & c1_bit) != 0 && (j & c2_bit) != 0 && (j & tgt_stride) == 0 {
                    let j0 = i * dim + j;
                    let j1 = i * dim + (j | tgt_stride);
                    let a = self.data[j0];
                    let b = self.data[j1];
                    self.data[j0] = a * n00 + b * n01;
                    self.data[j1] = a * n10 + b * n11;
                }
            }
        }
    }

    /// `ρ → CSWAP ρ CSWAP†` (Fredkin 게이트).
    ///
    /// ctrl 이 1 인 element 만 t1 ↔ t2 amplitude swap.  CSWAP 은 unitary 이고
    /// 자기 self-adjoint 이므로 row pass + col pass 모두 같은 swap.
    pub fn apply_controlled_swap(&mut self, ctrl: usize, t1: usize, t2: usize) {
        assert!(ctrl != t1 && ctrl != t2 && t1 != t2);
        assert!(ctrl < self.n_qubits && t1 < self.n_qubits && t2 < self.n_qubits);
        let dim = self.dim;
        let ctrl_bit = 1usize << ctrl;
        let t1_bit = 1usize << t1;
        let t2_bit = 1usize << t2;

        // Pass 1: row swap.  ctrl=1 + (t1=0, t2=1) ↔ (t1=1, t2=0).
        for j in 0..dim {
            for i in 0..dim {
                if (i & ctrl_bit) != 0 && (i & t1_bit) == 0 && (i & t2_bit) != 0 {
                    let i_other = (i | t1_bit) & !t2_bit;
                    self.data.swap(i * dim + j, i_other * dim + j);
                }
            }
        }
        // Pass 2: column swap.
        for i in 0..dim {
            for j in 0..dim {
                if (j & ctrl_bit) != 0 && (j & t1_bit) == 0 && (j & t2_bit) != 0 {
                    let j_other = (j | t1_bit) & !t2_bit;
                    self.data.swap(i * dim + j, i * dim + j_other);
                }
            }
        }
    }

    /// 큐비트 `q` 를 trace out 한 (n-1)-qubit reduced density matrix `ρ' = Tr_q(ρ)`.
    ///
    /// `ρ'[a][b] = Σ_{m∈{0,1}} ρ[a_with_q=m][b_with_q=m]` (q 큐비트 자리 marginal).
    /// 결과 큐비트 인덱스: 원래 `q' < q` 는 그대로, `q' > q` 는 `q' - 1`.
    pub fn partial_trace(&self, q: usize) -> DensityMatrix<F> {
        assert!(q < self.n_qubits);
        let new_n = self.n_qubits - 1;
        assert!(
            new_n > 0,
            "partial_trace: 1-큐비트 ρ 의 trace_out 은 스칼라"
        );
        let new_dim = 1usize << new_n;
        let mut out = vec![zero::<F>(); new_dim * new_dim];
        let dim = self.dim;
        let stride = 1usize << q;
        let mask_lo = stride - 1;

        for a in 0..new_dim {
            // a 의 비트들을 원래 인덱스의 q 자리를 비워둔 상태로 확장.
            let a_lo = a & mask_lo;
            let a_hi = (a & !mask_lo) << 1;
            for b in 0..new_dim {
                let b_lo = b & mask_lo;
                let b_hi = (b & !mask_lo) << 1;
                let mut s = zero::<F>();
                for m in 0..2 {
                    let qa = a_lo | a_hi | (m << q);
                    let qb = b_lo | b_hi | (m << q);
                    s = s + self.data[qa * dim + qb];
                }
                out[a * new_dim + b] = s;
            }
        }
        DensityMatrix {
            n_qubits: new_n,
            dim: new_dim,
            data: out,
        }
    }

    /// `ρ → Σᵢ Kᵢ ρ Kᵢ†` (단일 큐비트 Kraus 채널).
    ///
    /// in-place block update.  단일 큐비트 위치 `q` 의 (row q-bit, col q-bit)
    /// 4-element block ρ_blk = [[ρ[r0][c0], ρ[r0][c1]], [ρ[r1][c0], ρ[r1][c1]]]
    /// 마다:
    ///
    /// ```text
    ///   ρ_blk' = Σᵢ Kᵢ ρ_blk Kᵢ†
    /// ```
    ///
    /// 4 element 단위 block 만 결합되므로 다른 block 과 독립 → 메모리 1× (temp 0).
    pub fn apply_kraus_1q(&mut self, kraus: &[Matrix2x2<F>], q: usize) {
        assert!(
            q < self.n_qubits,
            "apply_kraus_1q: target {q} 가 범위 벗어남 (n_qubits={})",
            self.n_qubits
        );
        assert!(!kraus.is_empty(), "apply_kraus_1q: kraus 가 비었음");
        let dim = self.dim;
        let stride = 1usize << q;

        // (r_base, c_base) 4-element block 순회.  block 안의 4 인덱스:
        //   (r0, c0) = (r_base, c_base)
        //   (r0, c1) = (r_base, c_base + stride)
        //   (r1, c0) = (r_base + stride, c_base)
        //   (r1, c1) = (r_base + stride, c_base + stride)
        let mut r = 0;
        while r < dim {
            for r_inner in r..r + stride {
                let mut c = 0;
                while c < dim {
                    for c_inner in c..c + stride {
                        let i00 = r_inner * dim + c_inner;
                        let i01 = r_inner * dim + (c_inner + stride);
                        let i10 = (r_inner + stride) * dim + c_inner;
                        let i11 = (r_inner + stride) * dim + (c_inner + stride);
                        let rho_00 = self.data[i00];
                        let rho_01 = self.data[i01];
                        let rho_10 = self.data[i10];
                        let rho_11 = self.data[i11];

                        let mut new_00 = zero::<F>();
                        let mut new_01 = zero::<F>();
                        let mut new_10 = zero::<F>();
                        let mut new_11 = zero::<F>();

                        for k in kraus {
                            let k00 = k[0][0];
                            let k01 = k[0][1];
                            let k10 = k[1][0];
                            let k11 = k[1][1];
                            // K ρ_blk
                            let kp_00 = k00 * rho_00 + k01 * rho_10;
                            let kp_01 = k00 * rho_01 + k01 * rho_11;
                            let kp_10 = k10 * rho_00 + k11 * rho_10;
                            let kp_11 = k10 * rho_01 + k11 * rho_11;
                            // (K ρ_blk) K† 의 행렬곱.  K† = [[conj(k00), conj(k10)],
                            //                              [conj(k01), conj(k11)]]
                            let dk00 = k00.conj();
                            let dk01 = k10.conj();
                            let dk10 = k01.conj();
                            let dk11 = k11.conj();
                            new_00 = new_00 + kp_00 * dk00 + kp_01 * dk10;
                            new_01 = new_01 + kp_00 * dk01 + kp_01 * dk11;
                            new_10 = new_10 + kp_10 * dk00 + kp_11 * dk10;
                            new_11 = new_11 + kp_10 * dk01 + kp_11 * dk11;
                        }

                        self.data[i00] = new_00;
                        self.data[i01] = new_01;
                        self.data[i10] = new_10;
                        self.data[i11] = new_11;
                    }
                    c += stride << 1;
                }
            }
            r += stride << 1;
        }
    }

    /// 단일 큐비트 측정 결과 0 의 확률 `P(q=0) = Tr(P_0 ρ)`.
    ///
    /// `P_0 = |0⟩⟨0|_q ⊗ I` projector — q-th bit 가 0 인 대각선 원소만 합산.
    /// 누적은 f64 (큰 N 안전).
    pub fn measure_probability_zero(&self, q: usize) -> f64 {
        assert!(q < self.n_qubits);
        let dim = self.dim;
        let stride = 1usize << q;
        let mut p: f64 = 0.0;
        let mut r = 0;
        while r < dim {
            for k in r..r + stride {
                let z = self.data[k * dim + k];
                p += <f64 as NumCast>::from(z.re).expect("F → f64");
            }
            r += stride << 1;
        }
        p.clamp(0.0, 1.0)
    }

    /// 단일 큐비트 측정 + collapse + 재정규화.  outcome (0 또는 1) 반환.
    ///
    /// outcome m 을 P(m) 에 따라 RNG 샘플링한 뒤 `ρ' = P_m ρ P_m / Tr(P_m ρ)`
    /// 적용.  `q` 외 큐비트의 marginal 분포는 보존됨.
    pub fn measure_collapse<R: Rng>(&mut self, q: usize, rng: &mut R) -> u8 {
        assert!(q < self.n_qubits);
        let p0 = self.measure_probability_zero(q);
        let r: f64 = rng.gen();
        let outcome: u8 = if r < p0 { 0 } else { 1 };
        let p_chosen = if outcome == 0 { p0 } else { 1.0 - p0 };
        self.project(q, outcome);
        // 재정규화: ρ /= P(outcome).
        if p_chosen > 0.0 {
            let inv: F = F::from(1.0 / p_chosen).expect("f64 → F");
            for z in &mut self.data {
                *z = *z * Complex::new(inv, F::zero());
            }
        }
        outcome
    }

    /// `ρ → P_m ρ P_m` (정규화 없음 — `measure_collapse` / `reset` 내부용).
    ///
    /// q 큐비트의 bit 가 outcome 과 다른 row/col 의 모든 원소를 0 으로.
    pub fn project(&mut self, q: usize, outcome: u8) {
        assert!(q < self.n_qubits);
        assert!(outcome <= 1);
        let dim = self.dim;
        let bit = 1usize << q;
        for i in 0..dim {
            let row_bit = ((i >> q) & 1) as u8;
            for j in 0..dim {
                let col_bit = ((j >> q) & 1) as u8;
                if row_bit != outcome || col_bit != outcome {
                    self.data[i * dim + j] = zero::<F>();
                }
            }
        }
        let _ = bit; // (마스크 직접 안 써도 가독성 위해 보존)
    }

    /// 큐비트 q 를 |0⟩ 으로 강제 reset: `ρ' = P_0 ρ P_0 + X_q P_1 ρ P_1 X_q`.
    ///
    /// trace-preserving — outcome 통계 없이 결정적.  cbit 미소비.
    pub fn reset_qubit(&mut self, q: usize) {
        assert!(q < self.n_qubits);
        let dim = self.dim;
        let stride = 1usize << q;
        // |0⟩⟨0| ρ |0⟩⟨0| + |0⟩⟨1| ρ |1⟩⟨0|
        // = (q-bit=0 row, q-bit=0 col) + (q-bit=0 row, q-bit=1 col) flipped to (0,0)
        // 실제론 단순: (i,j) 에서 row_bit, col_bit 둘 다 반영.
        // ρ' 은 q-th bit 가 모두 0 인 부분만 나머지에서 합치고 나머지 0.
        //
        // 깔끔히: q-bit-major 4 block 각각의 origin (0,0) 에 (0,0)+(1,1) 합치고
        // 나머지 3 block 0 으로.
        let mut r = 0;
        while r < dim {
            for r_inner in r..r + stride {
                let mut c = 0;
                while c < dim {
                    for c_inner in c..c + stride {
                        let i00 = r_inner * dim + c_inner;
                        let i01 = r_inner * dim + (c_inner + stride);
                        let i10 = (r_inner + stride) * dim + c_inner;
                        let i11 = (r_inner + stride) * dim + (c_inner + stride);
                        // new_00 = old_00 + old_11 (X P_1 X 가 (0,0) block 으로 회수)
                        self.data[i00] = self.data[i00] + self.data[i11];
                        self.data[i01] = zero::<F>();
                        self.data[i10] = zero::<F>();
                        self.data[i11] = zero::<F>();
                    }
                    c += stride << 1;
                }
            }
            r += stride << 1;
        }
    }

    /// 모든 basis state 의 측정 확률 `P(b) = ρ[b][b]` (대각선) 벡터 반환.
    ///
    /// `Σ P(b) = Tr(ρ) = 1` (trace-preserving 채널이면).
    pub fn diagonal_probabilities(&self) -> Vec<f64> {
        let dim = self.dim;
        let mut p = Vec::with_capacity(dim);
        for i in 0..dim {
            let z = self.data[i * dim + i];
            let r: f64 = <f64 as NumCast>::from(z.re).expect("F → f64");
            p.push(r.max(0.0));
        }
        p
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complex::approx_eq;
    use crate::gates::Gate;
    use crate::noise::NoiseChannel;
    use crate::operations::apply_single_qubit_gate;
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    fn assert_hermitian<F: Real>(rho: &DensityMatrix<F>, eps: F) {
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let a = rho.data()[i * dim + j];
                let b = rho.data()[j * dim + i].conj();
                assert!(
                    approx_eq(a, b, eps),
                    "non-hermitian at ({i},{j}): {a:?} vs conj({b:?})"
                );
            }
        }
    }

    #[test]
    fn new_initializes_to_zero_zero() {
        let rho = DensityMatrix::<f64>::new(2);
        assert_eq!(rho.dim(), 4);
        assert_eq!(rho.num_qubits(), 2);
        assert!(approx_eq(rho.data()[0], one::<f64>(), 1e-12));
        for i in 1..16 {
            assert!(approx_eq(rho.data()[i], zero::<f64>(), 1e-12));
        }
        let tr = rho.trace();
        assert!(approx_eq(tr, one::<f64>(), 1e-12));
    }

    #[test]
    fn from_pure_state_plus() {
        let mut sv = StateVector::<f64>::new(1);
        let h = Gate::H.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &h, 0);
        // |+⟩⟨+| = [[0.5, 0.5], [0.5, 0.5]]
        let rho = DensityMatrix::from_pure_state(&sv);
        let half = Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(rho.data()[0], half, 1e-12));
        assert!(approx_eq(rho.data()[1], half, 1e-12));
        assert!(approx_eq(rho.data()[2], half, 1e-12));
        assert!(approx_eq(rho.data()[3], half, 1e-12));
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn apply_x_to_zero_zero_gives_one_one() {
        // |0⟩⟨0| → X → |1⟩⟨1| = [[0,0],[0,1]]
        let mut rho = DensityMatrix::<f64>::new(1);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        assert!(approx_eq(rho.data()[0], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[1], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[2], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[3], one::<f64>(), 1e-12));
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
    }

    #[test]
    fn apply_h_to_zero_gives_plus_plus() {
        let mut rho = DensityMatrix::<f64>::new(1);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let half = Complex::new(0.5_f64, 0.0);
        for i in 0..4 {
            assert!(approx_eq(rho.data()[i], half, 1e-12), "i={i}");
        }
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn h_h_returns_to_identity() {
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 0);
        // ρ should be back to |00⟩⟨00| + tiny drift
        assert!(approx_eq(rho.data()[0], one::<f64>(), 1e-12));
        for i in 1..16 {
            assert!(approx_eq(rho.data()[i], zero::<f64>(), 1e-12));
        }
    }

    #[test]
    fn unitary_matches_pure_state_evolution() {
        // ρ_init = |00⟩⟨00|, apply H on q0 then CNOT-like X conditioned not done here;
        // 단순 test: H on q1 of 2-qubit ρ vs from_pure_state(H_{q1} |00⟩).
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 1);

        let mut sv = StateVector::<f64>::new(2);
        apply_single_qubit_gate(&mut sv, &h, 1);
        let rho_ref = DensityMatrix::from_pure_state(&sv);

        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let a = rho.data()[i * dim + j];
                let b = rho_ref.data()[i * dim + j];
                assert!(approx_eq(a, b, 1e-12), "diff at ({i},{j})");
            }
        }
    }

    #[test]
    fn unitary_preserves_trace() {
        let mut rho = DensityMatrix::<f64>::new(3);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 1);
        rho.apply_unitary_1q(&h, 2);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 1);
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-10));
        assert_hermitian(&rho, 1e-10);
    }

    #[test]
    fn kraus_bit_flip_p_half_on_zero() {
        // BitFlip(p=0.5) on |0⟩⟨0|: ρ' = 0.5 |0⟩⟨0| + 0.5 |1⟩⟨1| = diag(0.5, 0.5)
        let mut rho = DensityMatrix::<f64>::new(1);
        let kraus = NoiseChannel::BitFlip { p: 0.5 }.kraus_operators::<f64>();
        rho.apply_kraus_1q(&kraus, 0);
        let half = Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(rho.data()[0], half, 1e-12));
        assert!(approx_eq(rho.data()[1], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[2], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[3], half, 1e-12));
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn kraus_bit_flip_p_zero_is_identity() {
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let before = rho.data().to_vec();
        let kraus = NoiseChannel::BitFlip { p: 0.0 }.kraus_operators::<f64>();
        rho.apply_kraus_1q(&kraus, 0);
        for (a, b) in rho.data().iter().zip(before.iter()) {
            assert!(approx_eq(*a, *b, 1e-12));
        }
    }

    #[test]
    fn kraus_phase_flip_decoheres_off_diagonal() {
        // PhaseFlip(p=0.5) on |+⟩⟨+|:
        // (1-p) |+⟩⟨+| + p Z|+⟩⟨+|Z = 0.5 |+⟩⟨+| + 0.5 |−⟩⟨−|
        // = 0.5 (|+⟩⟨+| + |−⟩⟨−|) = 0.5 I = diag(0.5, 0.5)
        let mut rho = DensityMatrix::<f64>::new(1);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let kraus = NoiseChannel::PhaseFlip { p: 0.5 }.kraus_operators::<f64>();
        rho.apply_kraus_1q(&kraus, 0);
        let half = Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(rho.data()[0], half, 1e-12));
        assert!(approx_eq(rho.data()[1], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[2], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[3], half, 1e-12));
    }

    #[test]
    fn kraus_amp_damp_gamma_one_on_one_decays() {
        // |1⟩⟨1| → AmpDamp(γ=1) → |0⟩⟨0|
        let mut rho = DensityMatrix::<f64>::new(1);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        let kraus = NoiseChannel::AmplitudeDamping { gamma: 1.0 }.kraus_operators::<f64>();
        rho.apply_kraus_1q(&kraus, 0);
        assert!(approx_eq(rho.data()[0], one::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[3], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
    }

    #[test]
    fn kraus_depolarizing_to_max_mixed() {
        // Depolarizing(p=1) on |0⟩⟨0|: ρ' = (1/4)(I + X X† + Y Y† + Z Z†) ρ /...
        // 정확히는 (1-3p/4) ρ + (p/4)(X ρ X + Y ρ Y + Z ρ Z).  p=1 → (1/4)(ρ + X ρ X + Y ρ Y + Z ρ Z) = I/2.
        let mut rho = DensityMatrix::<f64>::new(1);
        let kraus = NoiseChannel::Depolarizing { p: 1.0 }.kraus_operators::<f64>();
        rho.apply_kraus_1q(&kraus, 0);
        let half = Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(rho.data()[0], half, 1e-12));
        assert!(approx_eq(rho.data()[1], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[2], zero::<f64>(), 1e-12));
        assert!(approx_eq(rho.data()[3], half, 1e-12));
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn kraus_preserves_trace_for_all_channels() {
        for channel in [
            NoiseChannel::BitFlip { p: 0.3 },
            NoiseChannel::PhaseFlip { p: 0.3 },
            NoiseChannel::Depolarizing { p: 0.3 },
            NoiseChannel::AmplitudeDamping { gamma: 0.4 },
        ] {
            let mut rho = DensityMatrix::<f64>::new(2);
            let h = Gate::H.matrix_2x2::<f64>();
            rho.apply_unitary_1q(&h, 0);
            rho.apply_unitary_1q(&h, 1);
            let kraus = channel.kraus_operators::<f64>();
            rho.apply_kraus_1q(&kraus, 0);
            rho.apply_kraus_1q(&kraus, 1);
            assert!(
                approx_eq(rho.trace(), one::<f64>(), 1e-10),
                "trace not preserved for {channel:?}: {:?}",
                rho.trace()
            );
            assert_hermitian(&rho, 1e-10);
        }
    }

    #[test]
    fn measure_probability_on_plus_is_half() {
        let mut rho = DensityMatrix::<f64>::new(1);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let p0 = rho.measure_probability_zero(0);
        assert!((p0 - 0.5).abs() < 1e-12);
    }

    #[test]
    fn measure_collapse_keeps_trace_one() {
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 1);
        let mut rng = StdRng::seed_from_u64(42);
        let _ = rho.measure_collapse(0, &mut rng);
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-10));
        assert_hermitian(&rho, 1e-10);
    }

    #[test]
    fn measure_collapse_statistical() {
        let trials = 5_000;
        let mut count_one = 0;
        let mut rng = StdRng::seed_from_u64(99);
        for _ in 0..trials {
            let mut rho = DensityMatrix::<f64>::new(1);
            let h = Gate::H.matrix_2x2::<f64>();
            rho.apply_unitary_1q(&h, 0);
            let outcome = rho.measure_collapse(0, &mut rng);
            if outcome == 1 {
                count_one += 1;
            }
        }
        let observed = count_one as f64 / trials as f64;
        assert!(
            (observed - 0.5).abs() < 0.03,
            "measure_collapse on |+⟩ got {observed}, expected ~0.5"
        );
    }

    #[test]
    fn reset_brings_qubit_to_zero() {
        // Bell-like ρ then reset q=0 → q=0 marginal is |0⟩.
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 1);
        rho.reset_qubit(0);
        // 모든 basis with q0=1 인 entry 는 0.  data[i*4+j] 에서 i,j 의 q0 bit=1 인 곳.
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let bit_i = i & 1;
                let bit_j = j & 1;
                if bit_i == 1 || bit_j == 1 {
                    assert!(
                        approx_eq(rho.data()[i * dim + j], zero::<f64>(), 1e-12),
                        "reset failed at ({i},{j})"
                    );
                }
            }
        }
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
    }

    #[test]
    fn diagonal_probabilities_sum_to_one() {
        let mut rho = DensityMatrix::<f64>::new(3);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 1);
        rho.apply_unitary_1q(&h, 2);
        let probs = rho.diagonal_probabilities();
        assert_eq!(probs.len(), 8);
        let total: f64 = probs.iter().sum();
        assert!((total - 1.0).abs() < 1e-12);
        for p in probs {
            assert!((p - 0.125).abs() < 1e-12);
        }
    }

    /// CNOT 행렬 (control=q0, target=q1) basis |q1 q0⟩:
    /// |00⟩=0 → |00⟩=0, |01⟩=1 → |11⟩=3, |10⟩=2 → |10⟩=2, |11⟩=3 → |01⟩=1.
    fn cnot_matrix_q0_ctrl() -> Matrix4x4<f64> {
        let z = zero::<f64>();
        let o = one::<f64>();
        [[o, z, z, z], [z, z, z, o], [z, z, o, z], [z, o, z, z]]
    }

    #[test]
    fn cnot_creates_bell_state_in_density() {
        // |00⟩ → H q0 → CNOT (ctrl=q0, target=q1) → Bell |Φ+⟩.
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let cnot = cnot_matrix_q0_ctrl();
        rho.apply_unitary_2q(&cnot, 0, 1);

        // Reference: pure state evolution + density 변환.
        let mut sv = StateVector::<f64>::new(2);
        apply_single_qubit_gate(&mut sv, &h, 0);
        crate::operations::apply_controlled_gate(&mut sv, &Gate::X.matrix_2x2::<f64>(), 0, 1);
        let rho_ref = DensityMatrix::from_pure_state(&sv);
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let a = rho.data()[i * dim + j];
                let b = rho_ref.data()[i * dim + j];
                assert!(approx_eq(a, b, 1e-12), "Bell density diff at ({i},{j})");
            }
        }
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn swap_two_qubit_in_density() {
        // |01⟩⟨01| → SWAP → |10⟩⟨10|
        let mut rho = DensityMatrix::<f64>::new(2);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0); // |01⟩⟨01|
        let swap = Gate::swap_matrix::<f64>();
        rho.apply_unitary_2q(&swap, 0, 1);
        // |10⟩ = index 2.  ρ[2][2] = 1.
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let expected = if i == 2 && j == 2 {
                    one::<f64>()
                } else {
                    zero::<f64>()
                };
                assert!(approx_eq(rho.data()[i * dim + j], expected, 1e-12));
            }
        }
    }

    #[test]
    fn partial_trace_on_bell_gives_max_mixed() {
        // Bell state |Φ+⟩ = (|00⟩+|11⟩)/√2 → density Bell ⟨Bell|.
        // Tr_q1(ρ) = I/2 (q0 marginal is maximally mixed).
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let cnot = cnot_matrix_q0_ctrl();
        rho.apply_unitary_2q(&cnot, 0, 1);

        let reduced = rho.partial_trace(1);
        assert_eq!(reduced.num_qubits(), 1);
        let half = Complex::new(0.5_f64, 0.0);
        assert!(approx_eq(reduced.data()[0], half, 1e-12));
        assert!(approx_eq(reduced.data()[1], zero::<f64>(), 1e-12));
        assert!(approx_eq(reduced.data()[2], zero::<f64>(), 1e-12));
        assert!(approx_eq(reduced.data()[3], half, 1e-12));
    }

    #[test]
    fn partial_trace_preserves_trace() {
        let mut rho = DensityMatrix::<f64>::new(3);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 2);
        let reduced = rho.partial_trace(1);
        assert!(approx_eq(reduced.trace(), one::<f64>(), 1e-12));
    }

    #[test]
    fn controlled_x_creates_bell() {
        // |00⟩ → H q0 → CX(ctrl=q0, tgt=q1) → Bell |Φ+⟩.
        let mut rho = DensityMatrix::<f64>::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&h, 0);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_controlled_1q(&x, 0, 1);

        let half = Complex::new(0.5_f64, 0.0);
        // Bell density: (|00⟩+|11⟩)/√2 ⟨...| = 0.5 (|00⟩⟨00| + |00⟩⟨11| + |11⟩⟨00| + |11⟩⟨11|)
        let dim = rho.dim();
        let expect_pairs: [(usize, usize); 4] = [(0, 0), (0, 3), (3, 0), (3, 3)];
        for i in 0..dim {
            for j in 0..dim {
                let val = rho.data()[i * dim + j];
                if expect_pairs.contains(&(i, j)) {
                    assert!(approx_eq(val, half, 1e-12), "Bell ({i},{j}) = {val:?}");
                } else {
                    assert!(approx_eq(val, zero::<f64>(), 1e-12), "non-zero ({i},{j})");
                }
            }
        }
        assert!(approx_eq(rho.trace(), one::<f64>(), 1e-12));
        assert_hermitian(&rho, 1e-12);
    }

    #[test]
    fn controlled_x_reverse_order() {
        // ctrl=q1, tgt=q0 — apply_controlled_1q 가 control/target 순서 무관히 동작.
        // |10⟩⟨10| → CX(ctrl=q1, tgt=q0) → |11⟩⟨11|.  index 2 → 3.
        let mut rho = DensityMatrix::<f64>::new(2);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 1); // |10⟩⟨10| = ρ[2][2] = 1
        rho.apply_controlled_1q(&x, 1, 0);
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let v = rho.data()[i * dim + j];
                let expect = if i == 3 && j == 3 {
                    one::<f64>()
                } else {
                    zero::<f64>()
                };
                assert!(approx_eq(v, expect, 1e-12));
            }
        }
    }

    #[test]
    fn doubly_controlled_x_is_toffoli() {
        // |110⟩⟨110| → Toffoli (c1=q0, c2=q1, tgt=q2) → |111⟩⟨111|.
        // |110⟩ = q0=0, q1=1, q2=1 → index 6.  After: q2 flips → q2=0 → |010⟩? 잠깐.
        // 컨벤션 little-endian.  |q2 q1 q0⟩ basis where index = q0 + 2*q1 + 4*q2.
        // c1=q0, c2=q1.  When q0=q1=1, flip q2.
        // Build state |011⟩ = q0=1, q1=1, q2=0 → index 3.  After Toffoli → q2 flips → q2=1 → index 3+4=7.
        let mut rho = DensityMatrix::<f64>::new(3);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        rho.apply_unitary_1q(&x, 1);
        // 현재 ρ = |011⟩⟨011| = ρ[3][3]=1.
        rho.apply_doubly_controlled_1q(&x, 0, 1, 2);
        // After: ρ = |111⟩⟨111| = ρ[7][7]=1.
        let dim = rho.dim();
        for i in 0..dim {
            for j in 0..dim {
                let v = rho.data()[i * dim + j];
                let expect = if i == 7 && j == 7 {
                    one::<f64>()
                } else {
                    zero::<f64>()
                };
                assert!(approx_eq(v, expect, 1e-12), "({i},{j}) = {v:?}");
            }
        }
    }

    #[test]
    fn doubly_controlled_no_action_when_one_control_zero() {
        // |001⟩⟨001| → Toffoli(c1=q0, c2=q1, tgt=q2) → unchanged (q1=0).
        let mut rho = DensityMatrix::<f64>::new(3);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        rho.apply_doubly_controlled_1q(&x, 0, 1, 2);
        // ρ = |001⟩⟨001| = ρ[1][1]=1.
        assert!(approx_eq(rho.data()[8 + 1], one::<f64>(), 1e-12));
    }

    #[test]
    fn fredkin_swap_when_control_one() {
        // |101⟩ = q0=1, q1=0, q2=1 → index 5.  Fredkin(ctrl=q2, t1=q0, t2=q1):
        // ctrl=q2=1 → swap q0 ↔ q1.  q0=1, q1=0 → q0=0, q1=1 → |110⟩ = index 6.
        let mut rho = DensityMatrix::<f64>::new(3);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        rho.apply_unitary_1q(&x, 2);
        rho.apply_controlled_swap(2, 0, 1);
        // After: ρ = |110⟩⟨110| = ρ[6][6]=1.
        assert!(approx_eq(rho.data()[6 * 8 + 6], one::<f64>(), 1e-12));
    }

    #[test]
    fn fredkin_no_action_when_control_zero() {
        // |001⟩⟨001| → Fredkin(ctrl=q2, t1=q0, t2=q1) → unchanged (ctrl=0).
        let mut rho = DensityMatrix::<f64>::new(3);
        let x = Gate::X.matrix_2x2::<f64>();
        rho.apply_unitary_1q(&x, 0);
        rho.apply_controlled_swap(2, 0, 1);
        assert!(approx_eq(rho.data()[8 + 1], one::<f64>(), 1e-12));
    }

    #[test]
    fn f32_path_works() {
        let mut rho = DensityMatrix::<f32>::new(2);
        let h = Gate::H.matrix_2x2::<f32>();
        rho.apply_unitary_1q(&h, 0);
        rho.apply_unitary_1q(&h, 1);
        let tr = rho.trace();
        assert!((tr.re - 1.0).abs() < 1e-5);
        assert_hermitian(&rho, 1e-5_f32);
    }
}
