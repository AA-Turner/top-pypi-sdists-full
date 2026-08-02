//! Pipelines for doing fourier tools style analysis
//! starting from this point:
//! https://git.ligo.org/cds/software/dtt/-/blob/4.1.2/src/dtt/diag/ffttools.cc

//! # PSD calc
//! 1. Take the FFT - windowing is built into the C fft func
//! 2. Rotate data if zoom: presumably we're centering on the zoom frequency in some sense, ffttools line 1029
//! 3. OR if not zoom, chop off freqs below starting freq.
//! 4. Get PSD from FFT fftttools.cc line 1059
//! 5. Do averaging of PSDs fftttools.cc line 1077  (Welch's method)
//!
//! # Cross calcs
//! run for each A channel ffttools.cc line 1100
//! Every other channel is a B channel, apparently
//!
//! 1. Calculate cross-correlation ffttools.cc line 1194
//! 2. Average cross-correlation (Welch's method) fftttools.cc line 1226
//! 3. Calculate Coherence ffttools.cc line 1255
//!    This is from cumulative PSD for A,B channels, and cumulative cross-correlation
//! 4. Calculate transfer function -- CITATION NEEDED.  I think this is actually calculated in the Graph class of DTT.

pub(crate) mod asd;
pub(crate) mod csd;
pub(crate) mod fft;
