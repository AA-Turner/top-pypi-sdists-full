use crate::OUTPUT_GDSFORMAT;
use crate::errors::DTTError;
use crate::params::test_params::FFTWindow;
use pipelines::complex::c128;
use std::sync::Mutex;

#[derive(Debug)]
#[allow(dead_code)]
pub struct FFTParam {
    c_param: *const crate::fftparam,
    length: usize,
    type_code: i32,
    window: FFTWindow,
}

unsafe impl Sync for FFTParam {}
unsafe impl Send for FFTParam {}

static create_mut: Mutex<i32> = Mutex::new(0);

impl FFTParam {
    fn get(&self) -> *const crate::fftparam {
        self.c_param
    }

    /// An fft plan of type FFTParam has to be created here before calling fft
    /// Typically one test needs only one plan for real valued channels and another plan
    /// for complex valued channels.
    ///
    /// plans so created should be destroyed later with param.destroy()
    pub(crate) fn create<T>(length: usize, window: FFTWindow) -> Result<Self, DTTError>
    where
        T: FFTTypeInfo + Default + Clone,
    {
        let _l = create_mut
            .lock()
            .expect("couldn't lock mutex because another user panicked while using the mutex");
        let type_code = T::type_code();
        let c_param = unsafe { crate::create_fft_plan(length, type_code, window.clone().into()) };
        if c_param.is_null() {
            return Err(DTTError::OutOfMemory("allocating fft parameter"));
        }
        Ok(Self {
            c_param,
            length,
            type_code,
            window,
        })
    }

    /// When an fft plan is finished (when a test is done), destroy the plan
    /// with this function to free memory.
    fn destroy(&self) {
        let _l = create_mut
            .lock()
            .expect("couldn't lock mutex because another user panicked while using the mutex");
        unsafe { crate::destroy_fft_plan(self.c_param as *mut crate::fftparam) };
    }

    pub(crate) fn get_window_coeffs(&self) -> &[f64] {
        let wc = unsafe { crate::get_window_coeffs(self.c_param) };
        unsafe { std::slice::from_raw_parts(wc, self.length) }
    }
}

impl Drop for FFTParam {
    fn drop(&mut self) {
        self.destroy();
    }
}

/// Descriptors needed to take ffts of data of specific types
pub trait FFTTypeInfo {
    /// Return the code used to identify the type in gds-sigp functions
    fn type_code() -> i32;

    /// Return the size of the c128 output array for the given sized input array
    fn output_size(input_size: usize) -> usize;
}

impl FFTTypeInfo for f64 {
    fn type_code() -> i32 {
        0
    }

    fn output_size(input_size: usize) -> usize {
        input_size / 2 + 1
    }
}

impl FFTTypeInfo for c128 {
    fn type_code() -> i32 {
        1
    }

    fn output_size(input_size: usize) -> usize {
        input_size
    }
}

/// Generate an FFT of a time domain array
/// If the input array is real (f64), then DC, the positive frequencies, and finally the nyquist frequencies
/// are returned.
///
/// If the input array is complex (c128), then the result is positive DC, positive frequencies, nyquist, negative
/// from the most negative down to the least
///
/// This function requires a frequency plan created with create_fft_param()
pub fn fft<T: FFTTypeInfo>(
    td_data: &[T],
    param: &FFTParam,
    sample_length_sec: f64,
    remove_dc: bool,
) -> Result<Vec<c128>, DTTError> {
    let cap = T::output_size(td_data.len());
    let mut result: Vec<c128> = Vec::with_capacity(cap);
    result.resize(cap, c128::default());

    let is_error = unsafe {
        crate::psGen(
            param.get(),
            td_data.len() as i32,
            T::type_code(),
            td_data.as_ptr() as *const f64,
            sample_length_sec,
            OUTPUT_GDSFORMAT as i32,
            result.as_mut_ptr() as *mut f64,
            remove_dc as i32,
        )
    };

    match is_error {
        0 => Ok(result),
        e => Err(fft_error_to_dtt_error(e)),
    }
}

fn fft_error_to_dtt_error(fe: i32) -> DTTError {
    match fe {
        -3 => DTTError::BadArgument("psGen", "output_format", "unrecognized value"),
        -2 => DTTError::BadArgument("psGen", "data_type", "unrecognized value"),
        -1 => DTTError::BadArgument("psGen", "timeseries_length", "must be a power of two"),
        _ => {
            let msg = format!("psGen returned unrecognized value {}", fe);
            DTTError::UnrecognizedError(msg)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use tokio::task::JoinSet;

    #[test]
    fn test_fft_sin() {
        let param = FFTParam::create::<f64>(8, FFTWindow::Uniform).unwrap();

        let input_data = [0.0, 0.71, 1.0, 0.71, 0.0, -0.71, -1.0, -0.71];
        let out = match fft(&input_data, &param, 1.0, false) {
            Ok(f) => f,
            Err(e) => panic!("fft failure: {}", e.to_string()),
        };
        let target = [
            c128::new(0.0, 0.0),
            c128::new(0.0, -1.4171067811865479),
            c128::new(0.0, 0.0),
            c128::new(0.0, -0.0028932188134525509),
            c128::new(0.0, 0.0),
        ];
        assert_eq!(out, target);
    }

    #[test]
    fn test_fft_cos() {
        let param = FFTParam::create::<f64>(8, FFTWindow::Uniform).unwrap();

        let input_data = [1.0, 0.71, 0.0, -0.71, -1.0, -0.71, 0.0, 0.71];
        let out = match fft(&input_data, &param, 1.0, false) {
            Ok(f) => f,
            Err(e) => panic!("fft failure: {}", e.to_string()),
        };
        let target = [
            c128::new(0.0, 0.0),
            c128::new(1.4171067811865479, 0.0),
            c128::new(0.0, 0.0),
            c128::new(-0.0028932188134525509, 0.0),
            c128::new(0.0, 0.0),
        ];
        assert_eq!(out, target);
    }

    #[test]
    fn test_fft_1024() {
        let param = Arc::new(FFTParam::create::<f64>(8, FFTWindow::Uniform).unwrap());

        let rt = tokio::runtime::Runtime::new().unwrap();
        let input_data = [0.0, 0.71, 1.0, 0.71, 0.0, -0.71, -1.0, -0.71];
        const n: usize = 1024;

        let mut count: usize = 0;
        let target = [
            c128::new(0.0, 0.0),
            c128::new(0.0, -1.4171067811865479),
            c128::new(0.0, 0.0),
            c128::new(0.0, -0.0028932188134525509),
            c128::new(0.0, 0.0),
        ];

        rt.block_on({
            async {
                let mut join_handles = JoinSet::new();
                for _i in 0..n {
                    let inpdata = input_data.clone();
                    let p = param.clone();
                    join_handles.spawn_blocking(move || fft(&inpdata, &p, 1.0, false));
                }

                while let Some(res) = join_handles.join_next().await {
                    let out = match res {
                        Ok(Ok(f)) => f,
                        Ok(Err(e)) => panic!("fft failure: {}", e.to_string()),
                        Err(e) => panic!("fft failure: {}", e.to_string()),
                    };
                    assert_eq!(out, target);
                    count += 1;
                }
            }
        });

        assert_eq!(count, n);
    }
}
