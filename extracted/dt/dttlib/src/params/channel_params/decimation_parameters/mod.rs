use crate::errors::DTTError;
use crate::gds_sigp::decimate::{DecimationFilter, firphase};
use ligo_hires_gps_time::PipDuration;
use num_traits::FromPrimitive;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;
/// collects the delays associated with the total decimation on the channel
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass)]
#[derive(Default, Clone, Debug)]
pub struct DecimationDelays {
    /// seconds of delay for the decimation
    pub decimation_delay_s: f64,

    /// the number of points to shift data up for alignment
    pub delay_taps: i32,

    /// the time to shift down the start of a segment
    pub delayshift_pip: PipDuration,

    /// Time shift for start of heterodyne calculation
    pub heterodyne_delay_pip: PipDuration,
}

impl DecimationDelays {
    pub(super) fn new(
        remove_delay: bool,
        input_rate_hz: f64,
        num_decs: i32,
        filter: DecimationFilter,
    ) -> Self {
        let dec_factor = 1 << num_decs;
        let y = firphase(filter, dec_factor);
        let decimation_delay_s = y / input_rate_hz;

        if remove_delay {
            // this is the number of shift steps needed to correct the input
            let sDelay = i32::from_f64(y.round()).unwrap_or(0);
            let dec_factor = 1 << num_decs;

            // get sDelay rounded up to the nearest multiple of the decimation factor
            // this is number of shift steps on the output, but in units of input steps
            let tDelay = dec_factor * ((sDelay + dec_factor - 1) / dec_factor);

            // difference between output and input steps
            // data will be shifted later by this many points on input to get the timestamp
            // right on output
            let delay_taps = tDelay - sDelay;

            let dt = 1.0 / input_rate_hz;

            let delayshift_pip = PipDuration::from_seconds(f64::from(tDelay) * dt);

            let heterodyne_delay_pip = PipDuration::from_seconds((y + f64::from(delay_taps)) * dt);

            Self {
                decimation_delay_s,
                delay_taps,
                delayshift_pip,
                heterodyne_delay_pip,
            }
        } else {
            Self {
                decimation_delay_s,
                delay_taps: 0,
                delayshift_pip: PipDuration::default(),
                heterodyne_delay_pip: PipDuration::default(),
            }
        }
    }
}

/// Values used to generate a decimation pipeline for a single stage of decimation
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(get_all))]
#[derive(Default, Clone, Debug)]
pub struct DecimationParameters {
    /// anti-aliasing filter
    pub filter: DecimationFilter,

    /// number of x2 decimations
    pub num_decs: i32,
}

impl DecimationParameters {
    /// Calculation of delay correction values
    ///
    /// remove delay is false, the number of decimations and the real delay is calculated
    /// but all the correction factors are set to zero.
    ///
    /// ### References
    ///
    /// 1. cds/software/dtt dataChannel::preprocessing::preprocessing
    ///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L303
    pub(super) fn new(
        filter: DecimationFilter,
        input_rate_hz: f64,
        output_rate_hz: f64,
    ) -> Result<Self, DTTError> {
        let dec_factor = if let Some(df) = i32::from_f64(input_rate_hz / output_rate_hz) {
            df
        } else {
            return Err(DTTError::BadArgument(
                "DecimationParameters::new",
                "input_rate_hz",
                "should be output_rate_hz xN, where N is a multiple of two.",
            ));
        };

        let num_decs = num_decs_from_dec_factor(dec_factor)?;

        Ok(DecimationParameters { filter, num_decs })
    }
}

/// calculate the number of x2 decimations that are needed to reach the
/// given decimation factor.
/// Only exact values are permitted, i.e. powers of two.  Everything else
/// returns an Err(BadArgument)
fn num_decs_from_dec_factor(dec_factor: i32) -> Result<i32, DTTError> {
    let num_decs = match i32::from_f64(f64::from(dec_factor).log2().ceil()) {
        Some(x) => x,
        None => {
            return Err(DTTError::BadArgument(
                "num_decs_from_dec_factor",
                "dec_factor",
                "could not take log2() of the value",
            ));
        }
    };
    if (1 << num_decs) != dec_factor {
        return Err(DTTError::BadArgument(
            "num_decS_from_dec_factor",
            "dec_factor",
            "was not an exact power of two",
        ));
    }
    Ok(num_decs)
}
