use super::buffer::Buffer;
use crate::data_source::{
    ChannelQuery, DataBlock, DataBlockReceiver, DataBlockSender, DataSource, DataSourceFeatures,
    DataSourceRef,
};
use crate::errors::DTTError;
use crate::params::channel_params::channel::Channel;
use crate::params::channel_params::nds_data_type::NDSDataType;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use nds_cache_rs::buffer::TimeSeries;
use pipelines::complex::c64;
use std::collections::HashSet;
use tokio::sync::mpsc;
use user_messages::UserMessageProviderBase;

/// The Dummy data source gives made up data for any channel requested of it.
#[derive(Default, Clone, Copy)]
pub struct Dummy {}

impl DataSource for Dummy {
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

        let chans: Vec<_> = view.set.clone().into();
        view.block_tx = Some(db_tx.clone());
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
        Dummy {}.into()
    }

    fn find_channels(&self, _rc: Box<RunContext>, _query: &ChannelQuery) -> Result<(), DTTError> {
        Err(DTTError::NoCapabaility(
            "Dummy data source".into(),
            "find channels".into(),
        ))
    }
}

impl Dummy {
    async fn stream_loop(
        rc: Box<RunContext>,
        channels: Vec<Channel>,
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
        datablock_tx: DataBlockSender,
    ) {
        let mut next_time_pip = start_pip;
        let stride_pip: PipDuration = PipDuration::from_seconds(1.0); // 2**30 pips per second

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
            if let Err(_) = datablock_tx.send(db).await {
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
        Ok(match channel.data_type {
            NDSDataType::Int16 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, i16::default());
                nds_cache_rs::buffer::Buffer::Int16(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Int32 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, i32::default());
                nds_cache_rs::buffer::Buffer::Int32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Int64 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, i64::default());
                nds_cache_rs::buffer::Buffer::Int64(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Float32 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, f32::default());
                nds_cache_rs::buffer::Buffer::Float32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Float64 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, f64::default());
                nds_cache_rs::buffer::Buffer::Float64(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::Complex64 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, c64::default());
                nds_cache_rs::buffer::Buffer::Complex32(TimeSeries::new(
                    channel.clone().into(),
                    start,
                    channel.period,
                    v,
                )?)
                .into()
            }
            NDSDataType::UInt32 => {
                let mut v = Vec::with_capacity(count);
                v.resize(count, u32::default());
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
