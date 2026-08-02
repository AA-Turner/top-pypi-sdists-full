use std::ffi::{c_double, c_int};

unsafe extern "C" {
    fn frexp(x: c_double, exp: *mut c_int) -> c_double;
    fn ldexp(x: c_double, exp: c_int) -> c_double;
}

pub(crate) fn fr_exp(f: f64) -> (f64, i32) {
    let mut exp: c_int = 0;
    let res = unsafe { frexp(f, &mut exp) };
    (res, exp)
}

pub(crate) fn ld_exp(f: f64, exp: i32) -> f64 {
    unsafe { ldexp(f, exp) }
}

/// round up to the nearest power of two
pub(crate) fn round_up_p2(v: f64) -> f64 {
    let exp = fr_exp(v).1;
    ld_exp(1.0, exp)
}

/// round to the nearest power of two
pub(crate) fn round_p2(v: f64) -> f64 {
    let (m, x) = fr_exp(v);
    if m >= 0.5 {
        ld_exp(1.0, x)
    } else {
        ld_exp(1.0, x - 1)
    }
}
