use crate::analysis::result::record::ResultsRecord;
use crate::data_source::DataSourceRef;
use crate::run_context::RunContext;
use crate::timeline::Timeline;
use std::fmt;
use tokio::sync::{mpsc, watch};

/// target number of total time-histories to save
/// We can't save them all, or we run out of memory
/// This could be dynamic based on size
/// if the time histories are small, we should save more
const TOTAL_TIME_HISTORIES: usize = 100;

/// encapsulates a running test process
struct RunTest {
    rc: Box<RunContext>,
    #[allow(dead_code)]
    interrupt_receiver: RunInterruptReceiver,
    status_sender: RunStatusSender,
    timeline: Timeline,
    data_source: DataSourceRef,
}

impl RunTest {
    pub(crate) async fn run_loop(self) {
        self.set_status(RunStatusMsg::Initializing);

        // fix start time
        let bound_tl = self.timeline.bind_start_time(&self.data_source);

        // build up analysis
        let results_rx = match bound_tl
            .setup_analysis(&self.rc, self.data_source.clone())
            .await
        {
            Ok(r) => r,
            Err(e) => {
                let msg = format!("Failed to setup analysis: {}", e);
                self.set_status(RunStatusMsg::Aborted(msg));
                return;
            }
        };

        // create run record
        let per_channel_history = 1.max(TOTAL_TIME_HISTORIES / bound_tl.all_channels().len());
        let rr_join =
            ResultsRecord::start(self.rc.clone(), bound_tl, per_channel_history, results_rx).await;

        // start test (it should already be started)

        // wait until finished
        if let Err(e) = rr_join.await {
            let msg = format!("Join of recording task failed at end of test: {}", e);
            self.rc.user_messages.warning(msg);
        }

        self.set_status(RunStatusMsg::Finished);
    }

    fn set_status(&self, status: RunStatusMsg) {
        // send to processes
        match self.status_sender.send(status.clone()) {
            Ok(_) => (),
            // maybe we should stop running in the error case?
            // there are no more receivers.
            Err(e) => {
                let msg = format!(
                    "A running test tried to update its status, but the run was already abandoned: {}",
                    e
                );
                self.rc.user_messages.warning(msg);
            }
        }

        // send to user
        let status_string = status.to_string();
        self.rc.user_messages.set_notice("RunStatus", status_string)
    }
}

#[allow(dead_code)]
#[derive(Clone, Debug)]
enum RunInterruptMsg {
    AbortTest,
    PauseTest,
}

type RunInterruptSender = mpsc::UnboundedSender<RunInterruptMsg>;
type RunInterruptReceiver = mpsc::UnboundedReceiver<RunInterruptMsg>;

/// these messages give general updates about run state to other processes
/// So they can decide, for example, whether to start another test.
/// They aren't meant for the user or to provide run details
#[derive(Clone, Debug)]
#[allow(dead_code)]
pub(crate) enum RunStatusMsg {
    NeverStarted,
    Initializing,
    Running,
    Analyzing,
    Finished,
    Aborted(String),
}

unsafe impl Sync for RunStatusMsg {}
unsafe impl Send for RunStatusMsg {}

/// Allows to_string() to be called on the enum
impl fmt::Display for RunStatusMsg {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

pub(crate) type RunStatusSender = watch::Sender<RunStatusMsg>;
pub(crate) type _RunStatusReceiver = watch::Receiver<RunStatusMsg>;

/// Cloneable handle that can be passed around to
pub(crate) struct RunHandle {
    interrupt_sender: RunInterruptSender,
}

impl RunHandle {
    pub(crate) async fn run_test(
        rc: Box<RunContext>,
        timeline: &Timeline,
        status_sender: RunStatusSender,
        data_source: DataSourceRef,
    ) -> Self {
        let (interrupt_sender, interrupt_receiver) = mpsc::unbounded_channel();
        let rt = RunTest {
            rc,
            interrupt_receiver,
            status_sender,
            data_source,
            timeline: timeline.clone(),
        };
        tokio::spawn(rt.run_loop());
        Self { interrupt_sender }
    }

    /// If Err is returned, the run has already finished.
    pub(crate) fn _abort(&self) -> Result<(), ()> {
        self.interrupt_sender
            .send(RunInterruptMsg::AbortTest)
            .or(Err(()))
    }
}

impl Clone for RunHandle {
    fn clone(&self) -> Self {
        Self {
            interrupt_sender: self.interrupt_sender.clone(),
            //status_receiver: self.status_receiver.resubscribe(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::data_source::dummy::Dummy;
    use crate::errors::DTTError;
    use crate::params::channel_params::channel::Channel;
    use crate::params::channel_params::{ChannelParams, nds_data_type::NDSDataType};
    use crate::params::test_params::{AverageType, FFTWindow, StartTime, TestParams};
    use crate::tokio_setup::tokio_init;
    use crate::user::{DTT, UserOutputReceiver};
    use lazy_static::lazy_static;
    use ligo_hires_gps_time::{PipDuration, PipInstant};
    use tokio::time::Duration;

    fn test_parameters(num_chans: usize, averages: u64) -> TestParams {
        let measurement_param_list = (0..num_chans)
            .map(|i| {
                let channel_name = format!("X1:NOT-ACHAN_{}", i);

                ChannelParams {
                    active: true,
                    channel: Channel::new(
                        channel_name,
                        NDSDataType::Float64,
                        PipDuration::freq_hz_to_period(2048.0),
                    ),
                }
            })
            .collect();

        TestParams {
            start_time_pip: StartTime::Bound {
                start_pip: PipInstant::from(1000),
            },
            average_type: AverageType::Fixed,
            average_size: averages,
            overlap: 0.0,
            start_hz: 0.0,
            stop_hz: 900.0,
            ramp_down_pip: 1.into(),
            settling_time_frac: 0.0,
            fft_window: FFTWindow::Hann,
            band_width_hz: 1.0,
            ..TestParams::default_fft_params()
        }
        .with_measurement_channels(measurement_param_list)
    }

    lazy_static! {
        static ref TEST_RUNTIME: tokio::runtime::Runtime = tokio::runtime::Runtime::new().unwrap();
    }

    fn get_user_context() -> Result<(DTT, UserOutputReceiver), DTTError> {
        tokio_init(TEST_RUNTIME.handle())
    }

    /// Run 96 channels on 10 minutes worth of zero data.  Get the total pipeline time.
    /// On my laptop, an 8 core i7 2.8 GHz, running on zero'd input,
    /// This takes 4 to 10 seconds in debug and 700ms to 1200 ms in release.
    ///
    /// With randomized input in release, 900  - 1500 ms.
    /// this calculation maxes out all 8 cores.
    #[test]
    fn big_test() {
        let (uc, or) = get_user_context().unwrap();

        //let data_source = Box::new (RandomSource::new());
        let data_source = Dummy::default().into();

        let test_params = test_parameters(96, 600);

        let (pipe_time,) = uc.runtime.clone().block_on(uc.exec_test(
            or,
            test_params,
            data_source,
            Duration::from_secs(32),
        ));

        dbg!(pipe_time);
    }

    /// test a single channel on 960 minutes of data.
    /// this is the same amount of data as big_test
    /// this takes ~14 seconds in debug on my laptop
    /// an 8 core i7 2.8 GHz
    /// with zeroed input, stateful fft pipeline
    /// releases, 800 - 1300 ms.  It doesn't max out the cores, maybe 75%.
    #[test]
    fn long_test() {
        let (uc, or) = get_user_context().unwrap();

        //let data_source = Box::new (RandomSource::new());
        let data_source = Dummy::default().into();

        let test_params = test_parameters(1, 96 * 600);

        let (pipe_time,) = uc.runtime.clone().block_on(uc.exec_test(
            or,
            test_params,
            data_source,
            Duration::from_secs(1024),
        ));

        dbg!(pipe_time);
    }
}
