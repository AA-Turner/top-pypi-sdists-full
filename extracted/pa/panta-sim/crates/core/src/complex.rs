use num_complex::Complex;
use num_traits::{Float, FloatConst, FromPrimitive, NumCast};
use std::fmt::Debug;
use std::iter::Sum;

/// 양자 시뮬레이션이 사용할 수 있는 실수 타입 추상화.
///
/// `f32` / `f64` 양쪽에 구현되어 `StateVector<F>` 와 게이트 적용 함수가
/// 동일 코드 베이스로 두 정밀도를 모두 지원하게 한다.
///
/// 트레잇 바운드 의도:
/// - `Float` — sqrt, sin, cos 등 수치 연산 (회전 게이트, 정규화)
/// - `FloatConst` — π 같은 상수 (현재 직접 쓰이진 않지만 향후 회전 게이트 generic 화 시 유용)
/// - `FromPrimitive` / `NumCast` — `f64` 상수를 `F` 로 변환 (`F::from(0.5).unwrap()`)
/// - `Send` + `Sync` + `'static` — rayon 병렬 처리에 필요
/// - `Sum` — `iter().sum()` 패턴
pub trait Real:
    Float + FloatConst + FromPrimitive + NumCast + Send + Sync + Sum + Debug + 'static
{
}

impl Real for f32 {}
impl Real for f64 {}

/// 64비트 정밀도 복소수 타입 alias (기존 코드 호환용 default).
pub type C64 = Complex<f64>;

/// 32비트 정밀도 복소수 타입 alias.
pub type C32 = Complex<f32>;

/// `C64` 의 0 + 0i. 기존 코드 호환을 위해 유지.
pub const ZERO: C64 = C64::new(0.0, 0.0);
/// `C64` 의 1 + 0i. 기존 코드 호환을 위해 유지.
pub const ONE: C64 = C64::new(1.0, 0.0);
/// `C64` 의 0 + 1i. 기존 코드 호환을 위해 유지.
pub const I: C64 = C64::new(0.0, 1.0);

/// 임의 정밀도 `Complex<F>` 의 0.
#[inline]
pub fn zero<F: Real>() -> Complex<F> {
    Complex::new(F::zero(), F::zero())
}

/// 임의 정밀도 `Complex<F>` 의 1.
#[inline]
pub fn one<F: Real>() -> Complex<F> {
    Complex::new(F::one(), F::zero())
}

/// 임의 정밀도 `Complex<F>` 의 허수 단위 i.
#[inline]
pub fn imag_unit<F: Real>() -> Complex<F> {
    Complex::new(F::zero(), F::one())
}

/// `f64` 상수를 `Complex<F>` 의 실수부로 변환한다.
///
/// 회전 게이트의 cos/sin 결과 같은 `f64` 스칼라를 `F` 로 다운캐스트할 때 사용.
/// `F = f64` 면 무손실, `F = f32` 면 1-ULP 정도 절단.
#[inline]
pub fn real<F: Real>(x: f64) -> Complex<F> {
    Complex::new(F::from(x).expect("f64 → F 변환 실패"), F::zero())
}

/// `f64` (real, imag) 쌍을 `Complex<F>` 로 변환한다.
#[inline]
pub fn complex<F: Real>(re: f64, im: f64) -> Complex<F> {
    Complex::new(
        F::from(re).expect("f64 → F 변환 실패"),
        F::from(im).expect("f64 → F 변환 실패"),
    )
}

/// 두 복소수가 주어진 epsilon 안에서 같은지 비교한다.
pub fn approx_eq<F: Real>(a: Complex<F>, b: Complex<F>, eps: F) -> bool {
    (a - b).norm() < eps
}
