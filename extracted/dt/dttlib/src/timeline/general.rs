//! These functions are used in calculation of more than one kind of timeline

use crate::c_math::{fr_exp, ld_exp};
use crate::errors::DTTError;
use crate::params::channel_params::{ActiveList, ChannelSettings};
use crate::params::test_params::TestParams;
use crate::run_context::RunContext;
use crate::timeline::init::TimelineInit;

/// All complex channels must have the same heterodyne frequency
/// This enum represents the state of the check as we iterate through
/// the channels
#[derive(PartialEq)]
pub enum HeterodyneFreqMatch {
    None,
    Freq(f64),
    Mismatch,
}

impl HeterodyneFreqMatch {
    fn match_heterodyne_freq(self, chan: &ChannelSettings) -> HeterodyneFreqMatch {
        let chan_h_freq = if chan.data_type().is_complex() {
            chan.channel.heterodyne_freq_hz.unwrap_or_else(|| 0.0)
        } else {
            0.0
        };
        match self {
            HeterodyneFreqMatch::None => HeterodyneFreqMatch::Freq(chan_h_freq),
            HeterodyneFreqMatch::Freq(f) => {
                if chan_h_freq == f {
                    HeterodyneFreqMatch::Freq(f)
                } else {
                    HeterodyneFreqMatch::Mismatch
                }
            }
            HeterodyneFreqMatch::Mismatch => HeterodyneFreqMatch::Mismatch,
        }
    }
}

/// find Zoom frequency from complex channels
/// If there are multiple complex channels with different channels, that's an error.
/// If there are no complex channels, zero is returned.
/// If the returned value is zero, the final heterodyne frequency may still be determined
/// to be non-zero by later functions, hence "initial" in this function's name
/// ### References
/// 1. DTT stdtest.cc heterodyneFrequency()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/stdtest.cc#L851
pub fn initial_heterodyne_freq_hz(
    rc: Box<RunContext>,
    params: &TestParams,
) -> Result<f64, DTTError> {
    let mut fz: HeterodyneFreqMatch = HeterodyneFreqMatch::None;

    for exc in params.excitations.active_iter() {
        if let Some(rb) = exc.excitation.clone().read_back_channel {
            fz = fz.match_heterodyne_freq(&rb);
            if fz == HeterodyneFreqMatch::Mismatch {
                break;
            }
        }
    }
    for chan in params.measurement_channels.active_iter() {
        fz = fz.match_heterodyne_freq(&chan.channel);
        if fz == HeterodyneFreqMatch::Mismatch {
            break;
        }
    }
    match fz {
        HeterodyneFreqMatch::Mismatch => {
            rc.user_messages.set_error(
                "heterodyne_mismatch",
                "All complex channels must have the same heterodyne frequency.",
            );
            Err(DTTError::UnsatisfiedConstraint)
        }
        HeterodyneFreqMatch::None => {
            rc.user_messages.clear_message("heterodyne_mismatch");
            Ok(0.0)
        }
        HeterodyneFreqMatch::Freq(f) => {
            rc.user_messages.clear_message("heterodyne_mismatch");
            Ok(f)
        }
    }
}

/// ### References
/// 1. DTT stdtest::samplingFrequencies
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/stdtest.cc#L823
///
/// all panics here should either be locally guaranteed, or should test initialization order
/// in which case they will fail in unit tests.
pub fn sample_frequency_hz(timeline: &TimelineInit) -> (f64, f64) {
    let exp = fr_exp(2.0 * timeline.max_meas_hz.get().unwrap() - 1e-8).1;
    let sample_max = ld_exp(1.0, exp);
    let mut sample_min = sample_max;
    sample_min = sample_min.min(
        timeline
            .measurement_channels
            .get()
            .unwrap()
            .iter()
            .map(|c| c.rate_hz())
            .reduce(f64::min)
            .or_else(|| Some(f64::INFINITY))
            .expect("Should be guaranteed not to be None"),
    );

    sample_min = sample_min.min(
        timeline
            .excitations
            .get()
            .unwrap()
            .iter()
            .filter(|e| e.read_back_channel.is_some())
            .map(|e| {
                e.read_back_channel
                    .clone()
                    .expect("all None values should have been filtered out")
                    .rate_hz()
            })
            .reduce(f64::min)
            .or_else(|| Some(f64::INFINITY))
            .expect("Should be guaranteed not to be None"),
    );
    (sample_min, sample_max)
}
