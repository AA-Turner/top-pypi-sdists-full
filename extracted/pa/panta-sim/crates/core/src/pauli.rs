//! Pauli observable 기댓값 (v0.7 Cut 1).
//!
//! 변분 알고리즘 (VQE / QAOA) 의 토대.  Hamiltonian `H = Σ cᵢ Pᵢ` (각 `Pᵢ` 는
//! Pauli string) 에 대한 `⟨ψ|H|ψ⟩` 를 **2ⁿ × 2ⁿ 행렬을 만들지 않고** statevector
//! 에 직접 작용시켜 O(2ⁿ) per term 으로 계산한다 — 20~25큐비트 확장, Qiskit
//! 의존성 0.
//!
//! Pauli string 컨벤션은 `paulis[q]` 가 큐비트 `q` 의 연산자
//! (`0=I, 1=X, 2=Y, 3=Z`).  Qiskit `SparsePauliOp` 의 label (오른쪽 끝 = 큐비트 0)
//! 과의 변환은 호출 측 (Python binding) 책임.

use num_complex::Complex;
use rayon::prelude::*;

use crate::complex::Real;
use crate::density::DensityMatrix;
use crate::statevector::StateVector;

const PARALLEL_THRESHOLD: usize = 1 << 13;

/// 단일 Pauli string `P` 에 대한 `⟨ψ|P|ψ⟩` 를 계산한다.
///
/// `paulis[q] ∈ {0=I, 1=X, 2=Y, 3=Z}` 이고 `paulis.len() == n_qubits`.
///
/// Pauli 의 작용: `P|k⟩ = phase(k) · |k ⊕ flip⟩` 이고
/// - `flip` = X 또는 Y 가 있는 큐비트 비트마스크,
/// - `phase(k) = iⁿ_Y · (-1)^{popcount(k & zy_mask)}` (`zy_mask` = Z 또는 Y 비트).
///
/// 따라서 `⟨ψ|P|ψ⟩ = Σ_i conj(ψ_i) · phase(i ⊕ flip) · ψ_{i ⊕ flip}`.
/// Hermitian Pauli 라 결과는 실수지만, 일반성을 위해 `Complex<f64>` 반환.
pub fn expectation_pauli_term<F: Real>(state: &StateVector<F>, paulis: &[u8]) -> Complex<f64> {
    let n = state.num_qubits();
    debug_assert_eq!(paulis.len(), n, "paulis 길이는 n_qubits 와 같아야 함");
    let amps = state.amplitudes();

    let mut flip = 0usize;
    let mut zy_mask = 0usize;
    let mut num_y = 0u32;
    for (q, &p) in paulis.iter().enumerate() {
        match p {
            1 => flip |= 1 << q, // X
            2 => {
                flip |= 1 << q;
                zy_mask |= 1 << q;
                num_y += 1;
            } // Y
            3 => zy_mask |= 1 << q, // Z
            0 => {}              // I
            other => panic!("invalid Pauli code {other} (0=I,1=X,2=Y,3=Z)"),
        }
    }
    // i^num_y.
    let y_phase = match num_y & 3 {
        0 => Complex::new(1.0, 0.0),
        1 => Complex::new(0.0, 1.0),
        2 => Complex::new(-1.0, 0.0),
        _ => Complex::new(0.0, -1.0),
    };

    let dim = amps.len();
    let term = |i: usize| -> Complex<f64> {
        let ip = i ^ flip;
        let sign = if (ip & zy_mask).count_ones() & 1 == 1 {
            -1.0
        } else {
            1.0
        };
        let psi_i = to_c64(amps[i]);
        let psi_ip = to_c64(amps[ip]);
        psi_i.conj() * (y_phase * sign) * psi_ip
    };

    if dim < PARALLEL_THRESHOLD {
        let mut acc = Complex::new(0.0, 0.0);
        for i in 0..dim {
            acc += term(i);
        }
        acc
    } else {
        (0..dim)
            .into_par_iter()
            .map(term)
            .reduce(|| Complex::new(0.0, 0.0), |a, b| a + b)
    }
}

/// Hamiltonian `H = Σ cᵢ Pᵢ` 의 `⟨ψ|H|ψ⟩`.
///
/// `terms` 의 각 원소는 `(coeff, paulis)` — `paulis` 는 [`expectation_pauli_term`]
/// 컨벤션.  결과는 `Σ cᵢ ⟨Pᵢ⟩`.
pub fn expectation_pauli_sum<F: Real>(
    state: &StateVector<F>,
    terms: &[(Complex<f64>, Vec<u8>)],
) -> Complex<f64> {
    terms
        .iter()
        .map(|(coeff, paulis)| coeff * expectation_pauli_term(state, paulis))
        .sum()
}

/// Pauli string `P` 에 대한 density matrix 기댓값 `Tr(ρP)` (v0.7).
///
/// `P|i⟩ = phase(i)·|i⊕flip⟩` 이므로 `Tr(ρP) = Σ_i ρ_{i, i⊕flip} · phase(i)`,
/// `phase(i) = iⁿ_Y · (-1)^{popcount(i & zy_mask)}`.  noisy 회로 (density
/// backend) 의 observable 기댓값 — 순수 상태면 `⟨ψ|P|ψ⟩` 와 일치.
pub fn expectation_pauli_term_density<F: Real>(
    rho: &DensityMatrix<F>,
    paulis: &[u8],
) -> Complex<f64> {
    let n = rho.num_qubits();
    debug_assert_eq!(paulis.len(), n);
    let dim = rho.dim();
    let data = rho.data();

    let mut flip = 0usize;
    let mut zy_mask = 0usize;
    let mut num_y = 0u32;
    for (q, &p) in paulis.iter().enumerate() {
        match p {
            1 => flip |= 1 << q,
            2 => {
                flip |= 1 << q;
                zy_mask |= 1 << q;
                num_y += 1;
            }
            3 => zy_mask |= 1 << q,
            0 => {}
            other => panic!("invalid Pauli code {other} (0=I,1=X,2=Y,3=Z)"),
        }
    }
    let y_phase = match num_y & 3 {
        0 => Complex::new(1.0, 0.0),
        1 => Complex::new(0.0, 1.0),
        2 => Complex::new(-1.0, 0.0),
        _ => Complex::new(0.0, -1.0),
    };

    let mut acc = Complex::new(0.0, 0.0);
    for i in 0..dim {
        let j = i ^ flip;
        let sign = if (i & zy_mask).count_ones() & 1 == 1 {
            -1.0
        } else {
            1.0
        };
        // ρ[i][j] = data[i*dim + j].
        acc += to_c64(data[i * dim + j]) * (y_phase * sign);
    }
    acc
}

/// Hamiltonian `H = Σ cᵢ Pᵢ` 의 density 기댓값 `Tr(ρH) = Σ cᵢ Tr(ρPᵢ)`.
pub fn expectation_pauli_sum_density<F: Real>(
    rho: &DensityMatrix<F>,
    terms: &[(Complex<f64>, Vec<u8>)],
) -> Complex<f64> {
    terms
        .iter()
        .map(|(coeff, paulis)| coeff * expectation_pauli_term_density(rho, paulis))
        .sum()
}

#[inline]
fn to_c64<F: Real>(c: Complex<F>) -> Complex<f64> {
    Complex::new(
        num_traits::NumCast::from(c.re).unwrap_or(0.0),
        num_traits::NumCast::from(c.im).unwrap_or(0.0),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::gates::{Gate, Matrix2x2};
    use crate::operations::{apply_controlled_gate, apply_single_qubit_gate};

    fn close(a: Complex<f64>, b: Complex<f64>) -> bool {
        (a - b).norm() < 1e-12
    }

    #[test]
    fn z_expectation_on_zero_state() {
        // |0⟩: ⟨Z⟩ = +1.
        let sv: StateVector<f64> = StateVector::new(1);
        assert!(close(
            expectation_pauli_term(&sv, &[3]),
            Complex::new(1.0, 0.0)
        ));
        // ⟨X⟩ = 0, ⟨Y⟩ = 0.
        assert!(close(
            expectation_pauli_term(&sv, &[1]),
            Complex::new(0.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term(&sv, &[2]),
            Complex::new(0.0, 0.0)
        ));
        // ⟨I⟩ = 1.
        assert!(close(
            expectation_pauli_term(&sv, &[0]),
            Complex::new(1.0, 0.0)
        ));
    }

    #[test]
    fn z_expectation_on_one_state() {
        // X|0⟩ = |1⟩: ⟨Z⟩ = -1.
        let mut sv: StateVector<f64> = StateVector::new(1);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        assert!(close(
            expectation_pauli_term(&sv, &[3]),
            Complex::new(-1.0, 0.0)
        ));
    }

    #[test]
    fn x_expectation_on_plus_state() {
        // H|0⟩ = |+⟩: ⟨X⟩ = +1, ⟨Z⟩ = 0.
        let mut sv: StateVector<f64> = StateVector::new(1);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        assert!(close(
            expectation_pauli_term(&sv, &[1]),
            Complex::new(1.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term(&sv, &[3]),
            Complex::new(0.0, 0.0)
        ));
    }

    #[test]
    fn y_expectation_on_plus_i_state() {
        // S·H|0⟩ = |+i⟩: ⟨Y⟩ = +1.
        let mut sv: StateVector<f64> = StateVector::new(1);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        let s: Matrix2x2<f64> = Gate::S.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        apply_single_qubit_gate(&mut sv, &s, 0);
        assert!(close(
            expectation_pauli_term(&sv, &[2]),
            Complex::new(1.0, 0.0)
        ));
    }

    #[test]
    fn zz_expectation_on_bell_state() {
        // Bell (|00⟩+|11⟩)/√2: ⟨ZZ⟩ = +1, ⟨XX⟩ = +1, ⟨YY⟩ = -1, ⟨Z_0⟩ = 0.
        let mut sv: StateVector<f64> = StateVector::new(2);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        apply_controlled_gate(&mut sv, &x, 0, 1);
        assert!(close(
            expectation_pauli_term(&sv, &[3, 3]),
            Complex::new(1.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term(&sv, &[1, 1]),
            Complex::new(1.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term(&sv, &[2, 2]),
            Complex::new(-1.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term(&sv, &[3, 0]),
            Complex::new(0.0, 0.0)
        ));
    }

    #[test]
    fn density_expectation_matches_pure_state() {
        // 순수 상태 ρ = |ψ⟩⟨ψ| 에서 Tr(ρP) = ⟨ψ|P|ψ⟩.
        let mut sv: StateVector<f64> = StateVector::new(2);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        apply_controlled_gate(&mut sv, &x, 0, 1);
        let rho = DensityMatrix::from_pure_state(&sv);
        for paulis in [[3u8, 3], [1, 1], [2, 2], [3, 0], [0, 1]] {
            let sv_val = expectation_pauli_term(&sv, &paulis);
            let rho_val = expectation_pauli_term_density(&rho, &paulis);
            assert!(
                close(sv_val, rho_val),
                "paulis {paulis:?}: {sv_val} vs {rho_val}"
            );
        }
    }

    #[test]
    fn density_expectation_maximally_mixed() {
        // 최대 혼합 상태 ρ = I/2ⁿ: Tr(ρP) = 0 for any non-identity Pauli, 1 for I⊗I.
        let dim = 4;
        let mut rho: DensityMatrix<f64> = DensityMatrix::new(2);
        let n = 1.0 / dim as f64;
        for i in 0..dim {
            rho.data_mut()[i * dim + i] = Complex::new(n, 0.0);
        }
        assert!(close(
            expectation_pauli_term_density(&rho, &[3, 3]),
            Complex::new(0.0, 0.0)
        ));
        assert!(close(
            expectation_pauli_term_density(&rho, &[0, 0]),
            Complex::new(1.0, 0.0)
        ));
    }

    #[test]
    fn pauli_sum_linear_combination() {
        // |+⟩ 에서 H = 0.5·X + 2.0·Z → 0.5·1 + 2.0·0 = 0.5.
        let mut sv: StateVector<f64> = StateVector::new(1);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        let terms = vec![
            (Complex::new(0.5, 0.0), vec![1u8]),
            (Complex::new(2.0, 0.0), vec![3u8]),
        ];
        assert!(close(
            expectation_pauli_sum(&sv, &terms),
            Complex::new(0.5, 0.0)
        ));
    }
}
