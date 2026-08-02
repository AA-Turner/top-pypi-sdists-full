//! Downsample a time-domain trace to
//! a fixed number of points, the easier to draw with
//! Get the min and max for each point.

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::params::channel_params::Unit;
use crate::{AccumulationStats, AnalysisId};
use futures::future::FutureExt;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::pipe::Pipe1;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::collections::VecDeque;
use std::mem;
use std::sync::Arc;
use tokio::task::JoinHandle;
use user_messages::UserMsgProvider;

#[derive(Default)]
enum DownsampleMode<T>
where
    T: PipeDataPrimitive + Copy + PartialOrd + Default,
{
    Rough {
        factor: usize,
        join: JoinHandle<DownsampleCache<T>>,
    },
    #[default]
    Full,
}

#[allow(dead_code)]
struct DownsampleAssessment {
    factor: usize,
    non_overlap_points: usize,
    force_reset: bool,
}

#[derive(Copy, Clone, Default)]
struct Stat<T: Copy + Clone + Default + PartialOrd> {
    min: T,
    max: T,
    n: usize,
    min_first: bool,
}

impl<T: Copy + Clone + Default + PartialOrd> Stat<T> {
    /// Update the stat bucket while going to the left on an array
    fn update_left(&mut self, v: T) {
        if self.n == 0 || v < self.min {
            self.min = v;
            self.min_first = true;
        }
        if self.n == 0 || v > self.max {
            self.max = v;
            self.min_first = false;
        }
        self.n += 1;
    }

    /// Update the stat bucket while going to the right on an array
    fn update_right(&mut self, v: T) {
        if self.n == 0 || v < self.min {
            self.min = v;
            self.min_first = false;
        }
        if self.n == 0 || v > self.max {
            self.max = v;
            self.min_first = true;
        }
        self.n += 1;
    }

    fn new(v: T) -> Self {
        Self {
            min: v,
            max: v,
            n: 1,
            min_first: true,
        }
    }
}

#[derive(Default)]
pub(crate) struct DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + PartialOrd + Default,
{
    stat: VecDeque<Stat<T>>,
    factor: usize,
    /// the decimator is given some flexibility.
    /// the cache is allowed to range to two times target_size
    /// and won't enlarge unless less than half target_size
    target_size: usize,
    start_pip: PipInstant,
    /// this captures the end point of the
    /// input arrays
    /// it can be different than the calculated
    /// end point of the downsampled array,
    /// which does not take into account the original sample period.
    end_pip: PipInstant,
    accumulation_stats: AccumulationStats,
    rate_hz: f64,
    mode: DownsampleMode<T>,
    total_gap_size: usize,
    id: AnalysisId,
    unit: Unit,
}

impl<T> DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + Default + PartialOrd,
{
    fn new(target_size: usize) -> Self {
        let start_pip = PipInstant::gpst_epoch();
        Self {
            stat: VecDeque::with_capacity(3 * target_size),
            factor: 0,
            target_size,
            start_pip,
            end_pip: start_pip,
            rate_hz: 0.0,
            accumulation_stats: AccumulationStats::default(),
            mode: DownsampleMode::Full,
            total_gap_size: 0,
            id: AnalysisId::default(),
            unit: Unit::default(),
        }
    }

    fn len(&self) -> usize {
        self.stat.len()
    }

    fn assess_update(&self, input: &TimeDomainArray<T>) -> DownsampleAssessment {
        // if the gap handler has changed things, there might be a gap that was not filled
        // but now is filled.
        log::debug!(
            "[DOWNSAMPLE] old gap size = {} new gap size = {}",
            self.total_gap_size,
            input.total_gap_size
        );
        let force_reset = input.total_gap_size != self.total_gap_size;

        let suggested_factor = if input.len() < self.target_size {
            return DownsampleAssessment {
                factor: 1,
                non_overlap_points: 0,
                force_reset,
            };
        } else if input.len() % self.target_size == 0 {
            input.len() / self.target_size
        } else {
            input.len() / self.target_size + 1
        };

        let input_period = input.period_pip;
        let orig_dec_period = self.factor * input_period;

        log::debug!(
            "[DOWNSAMPLE] input_len = {}, target_size = {}, suggested_factor = {}",
            input.len(),
            self.target_size,
            suggested_factor
        );

        // if the factor is changed by at least 2x, or if the new data doesn't intersect the cache
        // or if th factor is low
        // clear the cache
        if (self.factor == 0)
            || (!(self.factor / 2 + 1..self.factor * 2).contains(&suggested_factor))
            || (self.start_pip > input.end_gps_pip())
            || (self.start_pip + self.len() * orig_dec_period < input.start_gps_pip)
        {
            return DownsampleAssessment {
                factor: suggested_factor,
                non_overlap_points: input.len(),
                force_reset: true,
            };
        }

        let mut non_overlap_points = 0;

        let dec_end = self.start_pip + self.len() * orig_dec_period;

        if input.end_gps_pip() > dec_end {
            non_overlap_points += ((input.end_gps_pip() - dec_end) / input_period) as usize;
        }

        if input.start_gps_pip < self.start_pip {
            non_overlap_points += ((self.start_pip - input.start_gps_pip) / input_period) as usize;
        }

        DownsampleAssessment {
            factor: self.factor,
            non_overlap_points,
            force_reset,
        }
    }

    fn update(&mut self, input: &TimeDomainArray<T>) -> TimeDomainArray<T> {
        self.accumulation_stats = input.accumulation_stats;
        self.id = input.id.clone();
        self.unit = input.unit.clone();

        let input_period = input.period_pip;

        let dec_period = self.factor * input_period;

        self.rate_hz = input.rate_hz() / self.factor as f64;

        {
            // Find out of there is any leading component of the input
            // that's not in the cache, and how much
            let (lead_end, mut block_start_pip) = if self.len() == 0 {
                // if the cache is empty, we have to do the whole thing
                (Some(input.len() - 1), None)
            } else if input.start_gps_pip.snap_down_to_step(&dec_period) < self.start_pip {
                let max_time = self.start_pip + (self.factor - 1) * input_period;
                let block_start_pip = max_time.snap_down_to_step(&dec_period);
                (
                    Some(
                        input
                            .ligo_hires_gps_time_to_index(max_time)
                            .min(input.len() - 1),
                    ),
                    Some(block_start_pip),
                )
            } else {
                (None, None)
            };

            // if there is any leading component, then decimate it.
            if let Some(e) = lead_end {
                let mut new_stat = if let Some(start_pip) = block_start_pip {
                    let block_start_index = (start_pip - self.start_pip) / dec_period;
                    if block_start_index >= 0 {
                        Some(self.stat[block_start_index as usize])
                    } else {
                        None
                    }
                } else {
                    None
                };

                for inp_index in (0..=e).rev() {
                    let inp_pip = input.index_to_gps_instant(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);

                    if let Some(t) = &block_start_pip {
                        if &new_block_start_pip != t {
                            let block_start_index = ((t - self.start_pip) / dec_period) as usize;
                            self.stat[block_start_index] =
                                new_stat.unwrap_or(self.stat[block_start_index]);

                            // fill in any zero-size blocks that might have been pushed earlier
                            for i in block_start_index..self.stat.len() {
                                if self.stat[i].n == 0 {
                                    self.stat[i].min = self.stat[block_start_index].min;
                                    self.stat[i].max = self.stat[block_start_index].max;
                                } else {
                                    break;
                                }
                            }

                            let new_block_start_index =
                                (new_block_start_pip - self.start_pip) / dec_period;
                            if new_block_start_index >= 0 {
                                let nbsi = new_block_start_index as usize;
                                new_stat = Some(self.stat[nbsi]);
                            } else {
                                new_stat = None;
                            }
                        }
                    } else {
                        self.stat.push_front(Stat::default());
                        self.start_pip = new_block_start_pip;
                    }

                    while new_block_start_pip < self.start_pip {
                        self.stat.push_front(Stat::default());
                        self.start_pip -= dec_period;
                    }

                    block_start_pip = Some(new_block_start_pip);

                    match new_stat {
                        None => new_stat = Some(Stat::new(input.data[inp_index])),
                        Some(_) => new_stat
                            .as_mut()
                            .expect("should have been checked for None just prior")
                            .update_left(input.data[inp_index]),
                    };
                }

                // fill in the last block
                if let Some(s) = new_stat {
                    if s.n > 0 {
                        let block_start_index = ((block_start_pip
                            .expect("should be guaranteed prior not to be None")
                            - self.start_pip)
                            / dec_period) as usize;
                        self.stat[block_start_index] =
                            new_stat.expect("should be guaranteed prior not to be None");
                    }
                }
            }
        }

        {
            // handle any extension of the input past the cache end
            let inp_last = input.len() - 1;
            let inp_last_pip = input.index_to_gps_instant(inp_last);

            let mut block_start_pip = self.start_pip + (self.len() - 1) * dec_period;
            let _last_block_start_index = self.len() - 1;

            if inp_last_pip.snap_down_to_step(&dec_period) > block_start_pip {
                let mut new_stat = if self.len() > 0 {
                    Some(self.stat[self.len() - 1])
                } else {
                    None
                };

                let inp_start_index = input.ligo_hires_gps_time_to_index(block_start_pip).max(0);

                for inp_index in inp_start_index..=inp_last {
                    let inp_pip = input.index_to_gps_instant(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);

                    if new_block_start_pip != block_start_pip {
                        let block_start_index =
                            ((block_start_pip - self.start_pip) / dec_period) as usize;
                        self.stat[block_start_index] = if let Some(stat) = new_stat {
                            stat
                        } else if block_start_index > 0 {
                            self.stat[block_start_index - 1]
                        } else {
                            Stat::default()
                        };

                        let nbsi = ((new_block_start_pip - self.start_pip) / dec_period) as usize;
                        if nbsi < self.len() {
                            new_stat = Some(self.stat[nbsi]);
                        } else {
                            new_stat = None;
                        }
                    }

                    while new_block_start_pip >= self.start_pip + self.len() * dec_period {
                        self.stat.push_back(Stat::default());
                    }

                    block_start_pip = new_block_start_pip;

                    match new_stat {
                        None => new_stat = Some(Stat::new(input.data[inp_index])),
                        Some(_) => new_stat
                            .as_mut()
                            .expect("should be guaranteed prior not to be None")
                            .update_right(input.data[inp_index]),
                    };
                }

                if let Some(s) = new_stat {
                    if s.n > 0 {
                        let block_start_index =
                            ((block_start_pip - self.start_pip) / dec_period) as usize;
                        //println!("[DOWNSAMPLE] fill in last block {}", block_start_index);
                        self.stat[block_start_index] =
                            new_stat.expect("Should be guaranteed prior not to be None");
                    }
                }
                //print!("[DOWNSAMPLE] min == max blocks out of {} ", self.len());

                // for i in 0..self.len() {
                //     if self.max[i] == self.min[i] {
                //         print!("[{}]={} ", i, self.n[i]);
                //     }
                // }
                // println!();
            }
        }

        // trim the cache to minimize its size

        let end_time = (input.end_gps_pip() - input_period).snap_down_to_step(&dec_period);
        let start_time = input.start_gps_pip.snap_down_to_step(&dec_period);

        let start_index = ((start_time - self.start_pip) / dec_period) as usize;
        let end_index = ((end_time - self.start_pip) / dec_period) as usize;

        if start_index > 0 {
            self.stat.drain(..start_index);
            self.start_pip += (start_index) * dec_period;
        }

        if end_index + 1 < self.stat.len() {
            self.stat.truncate(end_index + 1);
        }

        let real_end = input.get_real_end_gps_pip();
        if self.end_pip < real_end {
            self.end_pip = real_end;
        }

        //println!("downsampled from {} to {} points", input.len(), self.len());

        self.get_blended_min_max()
    }

    fn update_rough(&mut self, input: &TimeDomainArray<T>) -> TimeDomainArray<T> {
        let factor = self.factor;

        let rate_hz = input.rate_hz() / factor as f64;
        let period_pip = PipDuration::freq_hz_to_period(rate_hz);

        let new_size = input.len() / factor;
        let mut data = Vec::with_capacity(new_size);

        for out_index in 0..new_size {
            let in_index = out_index * factor;
            data.push(input.data[in_index]);
        }

        TimeDomainArray {
            start_gps_pip: input.start_gps_pip,
            period_pip,
            data,
            accumulation_stats: input.accumulation_stats,
            total_gap_size: input.total_gap_size,
            id: input.id.clone(),
            unit: input.unit.clone(),
            real_end_gps_pip: input.real_end_gps_pip,
        }
    }

    // fn get_min_max(&self) -> (TimeDomainArray<T>, TimeDomainArray<T>) {
    //
    //     let min_data = self.stat.iter().map(|x| x.min).collect();
    //     let max_data = self.stat.iter().map(|x| x.max).collect();
    //     (
    //         TimeDomainArray {
    //             start_gps_pip: self.start_pip,
    //             rate_hz: self.rate_hz,
    //             data: min_data,
    //             accumulation_stats: self.accumulation_stats,
    //         }
    //         ,
    //         TimeDomainArray {
    //             start_gps_pip: self.start_pip,
    //             rate_hz: self.rate_hz,
    //             data: max_data,
    //             accumulation_stats: self.accumulation_stats,
    //         }
    //     )
    //
    // }

    /// Get a single array where each min/max time point is subdivided into two separate
    /// points so that min-max can be drawn as near veritcal line in the same bucket
    /// using a single curve. (Might be drawn faster than min-max separate plus fill in.)
    fn get_blended_min_max(&self) -> TimeDomainArray<T> {
        // offset min by 1 quarter steps, and max by 3 quarter steps
        let quarter_period = PipDuration::freq_hz_to_period(self.rate_hz) / 4.0;

        let mut data = Vec::with_capacity(self.len() * 2);
        let rate_hz = self.rate_hz * 2.0;
        let start_gps_pip = self.start_pip + quarter_period;

        for i in 0..self.stat.len() {
            let s = &self.stat[i];
            if s.min_first {
                data.push(s.min);
                data.push(s.max);
            } else {
                data.push(s.max);
                data.push(s.min);
            }
        }

        let period_pip = PipDuration::freq_hz_to_period(rate_hz);

        TimeDomainArray {
            start_gps_pip,
            real_end_gps_pip: Some(self.end_pip),
            period_pip,
            data,
            accumulation_stats: self.accumulation_stats,
            total_gap_size: 0,
            id: self.id.clone(),
            unit: self.unit.clone(),
        }
    }

    fn almost_clone(&self) -> Self {
        Self {
            stat: self.stat.clone(),
            factor: self.factor,
            start_pip: self.start_pip,
            end_pip: self.end_pip,
            rate_hz: self.rate_hz,
            accumulation_stats: self.accumulation_stats,
            mode: DownsampleMode::Full,
            target_size: self.target_size,
            total_gap_size: self.total_gap_size,
            id: self.id.clone(),
            unit: self.unit.clone(),
        }
    }

    fn copy_from(&mut self, other: Self) {
        self.stat = other.stat;
        self.factor = other.factor;
        self.start_pip = other.start_pip;
        self.end_pip = other.end_pip;
        self.rate_hz = other.rate_hz;
        self.accumulation_stats = other.accumulation_stats;
        self.target_size = other.target_size;
        self.mode = DownsampleMode::Full;
    }

    fn clear(&mut self) {
        self.stat.clear();
        // set end_pip to 0 so it's always updated at the next add
        self.end_pip = PipInstant::gpst_epoch();
    }

    #[box_async]
    pub(crate) fn generate(
        rc: Box<dyn UserMsgProvider>,
        state: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<TimeDomainArray<T>> {
        log::debug!("[DOWNSAMPLE] Start downsample");
        let dm = mem::take(&mut state.mode);
        // check join if in rough
        if let DownsampleMode::Rough { factor, join } = dm {
            if join.is_finished() {
                match join.await {
                    Ok(dc) => {
                        log::debug!("[DOWNSAMPLE] joined background downsample");
                        rc.user_message_handle()
                            .clear_message("BadBackgroundDownsample");
                        state.copy_from(dc)
                    }
                    Err(e) => {
                        let msg = format!(
                            "Error while calculating downsample in the background: {}",
                            e
                        );
                        rc.user_message_handle()
                            .set_error("BadBackgroundDownsample", msg);
                        state.factor = 0;
                        state.mode = DownsampleMode::Full;
                    }
                };
            } else {
                state.mode = DownsampleMode::Rough { factor, join };
            }
        }

        let assessment = state.assess_update(input.as_ref());

        // check direct

        if assessment.factor == 1 {
            log::debug!("[DOWNSAMPLE] direct");
            state.factor = 1;
            state.mode = DownsampleMode::Full;
            return input.as_ref().clone().into();
        }

        if assessment.force_reset || assessment.factor != state.factor {
            log::debug!("[DOWNSAMPLE] new factor: {}", assessment.factor);
            state.factor = assessment.factor;
            state.total_gap_size = input.total_gap_size;
            state.clear();
        }

        // if let DownsampleMode::Full = state.mode {
        //     if assessment.non_overlap_points > 100000 {
        //         //println!("[DOWNSAMPLE] large non overlap.  Running in background.");
        //         // do it in the background
        //         let mut dc = state.almost_clone();
        //         let inpclone = input.clone();
        //         let join = tokio::task::spawn_blocking(move || {
        //             dc.update(inpclone.as_ref());
        //             dc
        //         });
        //         state.mode = DownsampleMode::Rough{factor: state.factor, join};
        //     }
        // }

        match &state.mode {
            DownsampleMode::Rough { factor, join: _ } => {
                if *factor != state.factor {
                    //println!("[DOWNSAMPLE] background update stale.  Creating a new one.");
                    // if factor has changed, start a new background udpate
                    let mut dc = state.almost_clone();
                    let inpclone = input.clone();
                    let join = tokio::task::spawn_blocking(move || {
                        dc.update(inpclone.as_ref());
                        dc
                    });
                    state.mode = DownsampleMode::Rough {
                        factor: state.factor,
                        join,
                    };
                }
                //println!("[DOWNSAMPLE] rough update");
                let result = state.update_rough(input.as_ref());
                result.into()
            }
            DownsampleMode::Full => {
                // let result = state.update_rough(input.as_ref());
                // println!("[DOWNSAMPLE] rough update: {}", result.len());
                // (result.clone(), result).into()
                log::debug!("[DOWNSAMPLE] full update");
                tokio::task::block_in_place(|| state.update(input.as_ref())).into()
            }
        }
    }

    pub(crate) async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
        let state = Self::new(4096);

        Ok(Pipe1::create(rc, name.into(), Self::generate, state, None, None, input).await?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::types::time_domain_array::TimeDomainArray;

    #[test]
    fn test_add_lead() {
        let mut dc = DownsampleCache::<f64>::new(4);
        let rate_hz = 100.0;
        let step_pip = PipDuration::freq_hz_to_period(rate_hz);
        let offset = 10;

        let period_pip = PipDuration::freq_hz_to_period(rate_hz);

        let t1 = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset + 5),
            real_end_gps_pip: None,
            period_pip,
            data: vec![1.0; 20],
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: 0,
            id: AnalysisId::default(),
            unit: Unit::default(),
        };

        let t2 = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset),
            real_end_gps_pip: None,
            period_pip,
            data: vec![2.0; 27],
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: 0,
            id: AnalysisId::default(),
            unit: Unit::default(),
        };

        let assess = dc.assess_update(&t1);
        dc.factor = assess.factor;

        dc.update(&t1);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.stat.len(), 4);

        let assess2 = dc.assess_update(&t2);
        dc.factor = assess2.factor;
        dc.update(&t2);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.stat.len(), 6);
        assert_eq!(dc.stat[0].n, 5);
        assert_eq!(dc.stat[0].min, 2.0);
        assert_eq!(dc.stat[1].max, 2.0);
        assert_eq!(dc.stat[1].min, 1.0);
        assert_eq!(dc.end_pip, t2.get_real_end_gps_pip());
    }
}
