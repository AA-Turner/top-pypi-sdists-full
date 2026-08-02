//! random data on all channels between 0-1.

use super::buffer::Buffer;
use crate::data_source::{
    ChannelQuery, DataBlock, DataBlockReceiver, DataBlockSender, DataSource, DataSourceFeatures,
    DataSourceRef,
};
use crate::errors::DTTError;
use crate::params::channel_params::{channel::Channel, nds_data_type::NDSDataType};
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use nds_cache_rs::buffer::TimeSeries;
use pipelines::complex::c64;
use rand::Rng;
use std::collections::HashSet;
use tokio::sync::mpsc;
use user_messages::UserMessageProviderBase;

/// The Dummy data source gives made up data for any channel requested of it.
pub struct RandomSource {}

impl DataSource for RandomSource {
    fn stream_data(
        &self,
        rc: Box<RunContext>,
        channels: &[Channel],
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError> {
        // create blocks 1 second in size.
        let (db_tx, db_rx) = mpsc::channel(4);

        let chans = Vec::from(channels);
        tokio::spawn(Self::stream_loop(rc, chans, start_pip, end_pip, db_tx));

        Ok(db_rx)
    }

    fn start_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError> {
        // create blocks 1 second in size.
        let (db_tx, db_rx) = mpsc::channel(4);

        let chans = view.set.clone().into();

        tokio::spawn(Self::stream_loop(
            rc,
            chans,
            view.span.start_pip,
            view.span.optional_end_pip(),
            db_tx,
        ));

        Ok(db_rx)
    }

    fn update_scope_data(&self, rc: Box<RunContext>, view: &mut ScopeView) -> Result<(), DTTError> {
        let db_tx = match &view.block_tx {
            Some(s) => s.clone(),
            None => {
                return Err(DTTError::MissingDataStreamError(
                    "Data stream missing from scope view.  Cannot update.".into(),
                ));
            }
        };

        tokio::spawn(Self::stream_loop(
            rc,
            view.set.clone().into(),
            view.span.start_pip,
            view.span.optional_end_pip(),
            db_tx,
        ));

        Ok(())
    }

    fn capabilities(&self) -> HashSet<DataSourceFeatures> {
        HashSet::from([DataSourceFeatures::LiveStream, DataSourceFeatures::Stream])
    }

    fn as_ref(&self) -> DataSourceRef {
        RandomSource {}.into()
    }

    fn find_channels(&self, _rc: Box<RunContext>, _query: &ChannelQuery) -> Result<(), DTTError> {
        Err(DTTError::NoCapabaility(
            "Random data source".into(),
            "find channels".into(),
        ))
    }
}

impl RandomSource {
    pub fn new() -> Self {
        Self {}
    }

    async fn stream_loop(
        rc: Box<RunContext>,
        channels: Vec<Channel>,
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
        datablock_tx: DataBlockSender,
    ) {
        let mut next_time_pip = start_pip;
        let stride_pip = PipDuration::from_seconds(1.0); // 2**30 pips per second

        'main: loop {
            let mut db = DataBlock::new();
            let span = match end_pip {
                Some(e) => stride_pip.min(e - start_pip),
                None => stride_pip,
            };
            for channel in channels.as_slice() {
                let buffer = match Self::gen_data_for_channel(channel, next_time_pip, span) {
                    Ok(b) => b,
                    Err(e) => {
                        rc.user_message_handle()
                            .error(format!("Error when generating channel data: {}", e));
                        break 'main;
                    }
                };

                db.insert(channel.clone(), vec![buffer]);
            }
            if datablock_tx.send(db).await.is_err() {
                break 'main;
            }

            next_time_pip += stride_pip;
            if let Some(e) = end_pip {
                if next_time_pip >= e {
                    break 'main;
                }
            }
        }
    }

    fn gen_data_for_channel(
        channel: &Channel,
        start: PipInstant,
        span: PipDuration,
    ) -> Result<Buffer, DTTError> {
        let count = (span / channel.period) as usize;

        let mut rng = rand::rng();
        Ok(match channel.data_type {
            NDSDataType::Int16 => {
                let v = (0..count).map(|_x| rng.random::<i16>()).collect();
                nds_cache_rs::buffer::Buffer::Int16(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Int32 => {
                let v = (0..count).map(|_x| rng.random::<i32>()).collect();
                nds_cache_rs::buffer::Buffer::Int32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Int64 => {
                let v = (0..count).map(|_x| rng.random::<i64>()).collect();
                nds_cache_rs::buffer::Buffer::Int64(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Float32 => {
                let v = (0..count).map(|_x| rng.random::<f32>()).collect();
                nds_cache_rs::buffer::Buffer::Float32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Float64 => {
                let v = (0..count).map(|_x| rng.random::<f64>()).collect();
                nds_cache_rs::buffer::Buffer::Float64(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Complex64 => {
                let v = (0..count)
                    .map(|_x| c64::new(rng.random::<f32>(), rng.random::<f32>()))
                    .collect();
                nds_cache_rs::buffer::Buffer::Complex32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::UInt32 => {
                let v = (0..count).map(|_x| rng.random::<u32>()).collect();
                nds_cache_rs::buffer::Buffer::UInt32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Complex128 => panic!("Complex 128 not supported by NDS."),
            NDSDataType::Int8 => panic!("Int 8 not supported by NDS."),
            NDSDataType::UInt16 => panic!("UInt 16 not supported by NDS."),
            NDSDataType::UInt8 => panic!("UInt 8 not supported by NDS."),
            NDSDataType::UInt64 => panic!("UInt 64 not supported by NDS."),
            //NDSDataType::String => panic!("String not supported by NDS."),
        })
    }
}
