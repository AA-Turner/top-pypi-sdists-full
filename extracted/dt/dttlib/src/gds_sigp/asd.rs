//! the underlying C function is called fftToPSD,
//! but the square root is taken, making it an ASD with units
//! of counts/sqrt(Hz)

use pipelines::complex::c128;

/// Calculate asd from an fft result
/// If input time domain is in units Y, then output ASD is
/// in Y/sqrt(Hz).
///
/// when has_dc is true, then the first element in the fft input is the DC component
/// this element is normalized differently than AC components
///
/// ### References
/// 1. fftToPs in gds-sigp
///    https://git.ligo.org/cds/software/gds-sigp/-/blob/1.0.0/src/SignalProcessing/algo/fftmodule.c#L580
pub fn asd(fft: &[c128], has_dc: bool) -> Vec<f64> {
    // fftToPs assumes complex input data does not have a DC element.
    // This is good assumption considering that all complex channels are heterodyned
    // so DC isn't in the FFT window.
    let data_complex = !has_dc;

    let mut output = Vec::with_capacity(fft.len());
    output.resize(fft.len(), f64::default());

    unsafe {
        crate::fftToPs(
            fft.len() as i32,
            data_complex as i32,
            fft.as_ptr() as *const f64,
            output.as_ptr() as *mut f64,
        );
    }
    output
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::f64::consts::SQRT_2;

    #[test]
    fn test_asd_dc() {
        let fft = [c128::new(2.0, 0.0), c128::new(4.0, 3.0)];
        let a = asd(&fft, true);
        assert_eq!(a, [2.0, 5.0 * SQRT_2]);
    }

    #[test]
    fn test_asd_no_dc() {
        let fft = [c128::new(2.0, 0.0), c128::new(4.0, 3.0)];
        let a = asd(&fft, false);
        assert_eq!(a, [2.0 * SQRT_2, 5.0 * SQRT_2]);
    }
}
