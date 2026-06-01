use num_complex::Complex;
use num_traits::NumCast;

use crate::complex::{one, zero, Real};

/// n큐비트 양자 상태를 나타내는 상태 벡터 (정밀도 `F` 에 대해 generic).
/// Little-endian 컨벤션: q[0]이 최하위 비트(LSB).
///
/// `F = f64` 가 default 정밀도. `F = f32` 는 메모리 50% 절감 + SIMD 친화성을
/// 위해 v0.2.1 에서 도입된 옵션.
#[derive(Debug, Clone)]
pub struct StateVector<F: Real> {
    n_qubits: usize,
    amplitudes: Vec<Complex<F>>,
}

impl<F: Real> StateVector<F> {
    /// |000...0⟩ 상태로 초기화된 n큐비트 상태 벡터를 생성한다.
    pub fn new(n_qubits: usize) -> Self {
        assert!(n_qubits > 0, "qubit 수는 1 이상이어야 합니다");
        let size = 1 << n_qubits;
        let mut amplitudes = vec![zero::<F>(); size];
        amplitudes[0] = one::<F>();
        Self {
            n_qubits,
            amplitudes,
        }
    }

    pub fn num_qubits(&self) -> usize {
        self.n_qubits
    }

    pub fn dim(&self) -> usize {
        self.amplitudes.len()
    }

    pub fn amplitudes(&self) -> &[Complex<F>] {
        &self.amplitudes
    }

    pub fn amplitudes_mut(&mut self) -> &mut [Complex<F>] {
        &mut self.amplitudes
    }

    /// 특정 basis state의 측정 확률 |amplitude|^2을 반환한다.
    pub fn probability(&self, index: usize) -> F {
        self.amplitudes[index].norm_sqr()
    }

    /// 모든 basis state의 측정 확률 벡터를 반환한다.
    pub fn probabilities(&self) -> Vec<F> {
        self.amplitudes.iter().map(|a| a.norm_sqr()).collect()
    }

    /// 상태 벡터를 정규화한다.
    ///
    /// **정밀도 안전장치**: `F = f32` 일 때 `2^n` 개의 작은 norm² 를 직접 누적하면
    /// 큰 N 에서 mantissa 손실로 norm 이 1.0 에 못 도달할 수 있다. 합산은 항상 f64 로,
    /// 마지막에만 `F` 로 다운캐스트.
    pub fn normalize(&mut self) {
        let norm_sq: f64 = self
            .amplitudes
            .iter()
            .map(|a| {
                let r = a.re;
                let i = a.im;
                let r64: f64 = NumCast::from(r).expect("F → f64 변환 실패");
                let i64: f64 = NumCast::from(i).expect("F → f64 변환 실패");
                r64 * r64 + i64 * i64
            })
            .sum();
        let norm = norm_sq.sqrt();
        if norm > 0.0 {
            let inv_f: F = F::from(1.0 / norm).expect("f64 → F 변환 실패");
            for a in &mut self.amplitudes {
                *a = *a * Complex::new(inv_f, F::zero());
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complex::{ONE, ZERO};

    #[test]
    fn test_new_single_qubit_f64() {
        let sv: StateVector<f64> = StateVector::new(1);
        assert_eq!(sv.num_qubits(), 1);
        assert_eq!(sv.dim(), 2);
        assert_eq!(sv.amplitudes()[0], ONE);
        assert_eq!(sv.amplitudes()[1], ZERO);
    }

    #[test]
    fn test_new_single_qubit_f32() {
        let sv: StateVector<f32> = StateVector::new(1);
        assert_eq!(sv.num_qubits(), 1);
        assert_eq!(sv.dim(), 2);
        assert_eq!(sv.amplitudes()[0].re, 1.0_f32);
        assert_eq!(sv.amplitudes()[1].re, 0.0_f32);
    }

    #[test]
    fn test_new_two_qubits() {
        let sv: StateVector<f64> = StateVector::new(2);
        assert_eq!(sv.dim(), 4);
        assert!((sv.probability(0) - 1.0).abs() < 1e-10);
        assert!(sv.probability(1).abs() < 1e-10);
    }

    #[test]
    fn test_probabilities_sum_to_one_f64() {
        let sv: StateVector<f64> = StateVector::new(3);
        let total: f64 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_probabilities_sum_to_one_f32() {
        let sv: StateVector<f32> = StateVector::new(3);
        let total: f32 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-6);
    }
}
