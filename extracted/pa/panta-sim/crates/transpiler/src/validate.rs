//! 입력 행렬의 unitarity 검증.

use num_complex::Complex;

use crate::decompose::Matrix2;

/// `M·M† ≈ I` 위배 시 반환되는 에러.
#[derive(Debug, Clone, PartialEq)]
pub struct UnitarityError {
    /// 가장 큰 편차가 발생한 (row, col) 위치.
    pub row: usize,
    pub col: usize,
    /// `M·M†` 의 해당 원소 값.
    pub got: Complex<f64>,
    /// 기대값 (대각이면 1+0i, 비대각이면 0+0i).
    pub expected: Complex<f64>,
    /// 측정된 절대 오차 `|got - expected|`.
    pub max_abs_error: f64,
    /// 사용된 허용 오차.
    pub tol: f64,
}

impl std::fmt::Display for UnitarityError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "matrix is not unitary: (M·M†)[{},{}] = {}+{}i (expected {}+{}i, |error|={:.3e}, tol={:.3e})",
            self.row,
            self.col,
            self.got.re,
            self.got.im,
            self.expected.re,
            self.expected.im,
            self.max_abs_error,
            self.tol
        )
    }
}

impl std::error::Error for UnitarityError {}

/// 2×2 행렬이 unitary 인지 검사한다.
///
/// `M·M† = I` 를 element-wise 로 비교한다. 가장 큰 편차가 `tol` 보다 크면
/// [`UnitarityError`] 를 반환한다.
///
/// 입력 원소가 NaN/Inf 이면 즉시 reject — 이전엔 `err > tol` 비교가 NaN
/// 일 때 false 라서 silent pass 후 statevector 까지 NaN 전파됐다 (v0.6.2 fix).
pub fn is_unitary_2x2(m: &Matrix2, tol: f64) -> Result<(), UnitarityError> {
    // v0.6.2: 입력 원소 finite 검사.  NaN 이 들어오면 prod 도 NaN 이 되고
    // diff.norm() = NaN → `err > tol` = false 로 silent pass 했음.
    for (r, row) in m.iter().enumerate() {
        for (c, entry) in row.iter().enumerate() {
            if !entry.re.is_finite() || !entry.im.is_finite() {
                return Err(UnitarityError {
                    row: r,
                    col: c,
                    got: *entry,
                    expected: Complex::new(0.0, 0.0),
                    max_abs_error: f64::NAN,
                    tol,
                });
            }
        }
    }

    // M·M† 계산: 행렬 곱 [[m00,m01],[m10,m11]] * [[m00*, m10*],[m01*, m11*]]
    let prod = [
        [
            m[0][0] * m[0][0].conj() + m[0][1] * m[0][1].conj(),
            m[0][0] * m[1][0].conj() + m[0][1] * m[1][1].conj(),
        ],
        [
            m[1][0] * m[0][0].conj() + m[1][1] * m[0][1].conj(),
            m[1][0] * m[1][0].conj() + m[1][1] * m[1][1].conj(),
        ],
    ];

    let identity = [
        [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
        [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
    ];

    let mut worst: Option<UnitarityError> = None;
    for r in 0..2 {
        for c in 0..2 {
            let diff = prod[r][c] - identity[r][c];
            let err = diff.norm();
            // err 가 NaN 이면 `err > tol` 가 false 라 worst 가 안 잡힘.  finite
            // 가드를 명시적으로 추가 — 입력 finite 검사로 이미 도달 안 하지만
            // 이중 안전망.
            if !err.is_finite() || err > tol {
                let candidate = UnitarityError {
                    row: r,
                    col: c,
                    got: prod[r][c],
                    expected: identity[r][c],
                    max_abs_error: err,
                    tol,
                };
                worst = Some(match worst {
                    Some(prev) if prev.max_abs_error >= err => prev,
                    _ => candidate,
                });
            }
        }
    }

    match worst {
        Some(e) => Err(e),
        None => Ok(()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn c(re: f64, im: f64) -> Complex<f64> {
        Complex::new(re, im)
    }

    #[test]
    fn test_identity_is_unitary() {
        let m = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_ok());
    }

    #[test]
    fn test_pauli_x_is_unitary() {
        let m = [[c(0.0, 0.0), c(1.0, 0.0)], [c(1.0, 0.0), c(0.0, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_ok());
    }

    #[test]
    fn test_hadamard_is_unitary() {
        let s = std::f64::consts::FRAC_1_SQRT_2;
        let m = [[c(s, 0.0), c(s, 0.0)], [c(s, 0.0), c(-s, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_ok());
    }

    #[test]
    fn test_diagonal_phase_is_unitary() {
        let theta: f64 = 0.7;
        let m = [
            [c(1.0, 0.0), c(0.0, 0.0)],
            [c(0.0, 0.0), c(theta.cos(), theta.sin())],
        ];
        assert!(is_unitary_2x2(&m, 1e-10).is_ok());
    }

    #[test]
    fn test_non_unitary_diagonal_rejected() {
        let m = [[c(1.0, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(2.0, 0.0)]];
        let err = is_unitary_2x2(&m, 1e-10).unwrap_err();
        assert_eq!(err.row, 1);
        assert_eq!(err.col, 1);
    }

    #[test]
    fn test_non_unitary_off_diagonal_rejected() {
        let m = [[c(1.0, 0.0), c(0.5, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_err());
    }

    #[test]
    fn test_nan_entry_rejected() {
        // v0.6.2 fix: NaN 원소가 들어오면 silent pass 했었음.
        let m = [[c(f64::NAN, 0.0), c(0.0, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_err());
    }

    #[test]
    fn test_nan_imag_entry_rejected() {
        let m = [[c(1.0, f64::NAN), c(0.0, 0.0)], [c(0.0, 0.0), c(1.0, 0.0)]];
        assert!(is_unitary_2x2(&m, 1e-10).is_err());
    }

    #[test]
    fn test_inf_entry_rejected() {
        let m = [
            [c(f64::INFINITY, 0.0), c(0.0, 0.0)],
            [c(0.0, 0.0), c(0.0, 0.0)],
        ];
        assert!(is_unitary_2x2(&m, 1e-10).is_err());
    }
}
