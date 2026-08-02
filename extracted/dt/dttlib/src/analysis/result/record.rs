//! Hold results for a test
//! Also hold a copy of the timeline and test parameters used to take a test.
//! Also passes through results to the app.

use std::collections::{HashMap, HashSet, VecDeque};
use tokio::task::JoinHandle;

#[cfg(feature = "python")]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;

use crate::analysis::result::{AnalysisId, AnalysisResult, ResultsReceiver};
use crate::params::channel_params::channel::Channel;
use crate::run_context::RunContext;
use crate::timeline::Timeline;
use crate::user::ResponseToUser;

/// Store analysis results for a given test.
#[derive(Clone, Debug)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(frozen))]
pub struct ResultsRecord {
    #[allow(dead_code)]
    timeline: Timeline,
    results: HashSet<AnalysisResult>,

    // time histories store separately because they are limited in size
    // and also are stored individually per segment
    time_histories: HashMap<Channel, VecDeque<AnalysisResult>>,

    // maximum number of histories to store per channel
    per_channel_history_limit: usize,
}

impl ResultsRecord {
    pub async fn start(
        rc: Box<RunContext>,
        timeline: Timeline,
        per_channel_history_limit: usize,
        mut results_rx: ResultsReceiver,
    ) -> JoinHandle<()> {
        let mut record = Self {
            timeline,
            results: HashSet::new(),
            time_histories: HashMap::new(),
            per_channel_history_limit,
        };

        tokio::spawn(async move {
            'main: loop {
                let result = match results_rx.recv().await {
                    None => break 'main,
                    Some(r) => r,
                };

                // store in cache
                record.store(result.clone());

                // send a response to the app
                let _ = rc
                    .output_handle
                    .send(rc.clone(), ResponseToUser::NewResult(result));
            }

            // when done, send self
            let _ = rc
                .output_handle
                .send(rc.clone(), ResponseToUser::FinalResults(record));
        })
    }

    /// store any result, whether time history or otherwise
    fn store(&mut self, result: AnalysisResult) {
        match &result {
            AnalysisResult::TimeDomainValueComplex(_) => self.store_time_history(result),
            AnalysisResult::TimeDomainValueReal(_) => self.store_time_history(result),
            _ => self.store_result(result),
        }
    }

    /// store non-time history i.e., frequency domain results
    fn store_result(&mut self, result: AnalysisResult) {
        self.results.replace(result);
    }

    /// store time histories, limiting them to a certain number
    /// of histories per channel
    fn store_time_history(&mut self, result: AnalysisResult) {
        let channel = match &result.id() {
            // Time History results use only the channel name
            // They are the only results with a Simple ID.
            AnalysisId::Simple { channel } => channel.clone(),
            // this panic is ok because it's contained in an analysis task
            _ => panic!("Received a non-time-history result to store with the time histories"),
        };

        if self.time_histories.contains_key(&channel) {
            let v = self
                .time_histories
                .get_mut(&channel)
                .expect("Should have been checked to be not None");
            v.push_front(result);
            v.truncate(self.per_channel_history_limit);
        } else {
            let mut v = VecDeque::with_capacity(self.per_channel_history_limit + 1);
            v.push_front(result);
            self.time_histories.insert(channel, v);
        }
    }
}
