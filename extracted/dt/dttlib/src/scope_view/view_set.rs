use crate::AnalysisId;
use crate::analysis::result::analysis_id::{AnalysisHeaderId, AnalysisRequestId};
use crate::data_source::DataBlock;
use crate::params::channel_params::channel_id::ChannelHeader;
use crate::params::channel_params::{Channel, ChannelId, TrendStat, TrendType};
#[cfg(not(feature = "python"))]
use dtt_macros::staticmethod;
use log::debug;
#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::collections::{HashMap, HashSet};

pub type SetMember = AnalysisId;

#[derive(Clone, Debug)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass)]
pub struct ViewSet {
    pub(crate) members: HashSet<SetMember>,

    /// Index map by of expected channel name to source channel name that's not resolved.
    unresolved_chans: HashSet<ChannelHeader>,

    /// look up table from analysisheaderid (from requests) to AnalysisId (to results)
    /// When all channels are resolved, the is table will be complete, and
    /// incoming channel data can be connected to the analysis pipelines
    lookup_analysis_id: HashMap<AnalysisHeaderId, AnalysisId>,

    /// these include any pipeline analysis requests
    //analysis_requests: HashSet<AnalysisRequestId>,
    full_requests: HashSet<AnalysisHeaderId>,
}

impl From<ViewSet> for Vec<Channel> {
    fn from(value: ViewSet) -> Self {
        let mut cvec = Vec::new();
        for c in value.members {
            cvec.push(c.first_channel().expect("cannot have zero channels"));
        }
        cvec
    }
}

impl From<Vec<Channel>> for ViewSet {
    fn from(value: Vec<Channel>) -> Self {
        Self {
            members: value
                .into_iter()
                .map(|channel| AnalysisId::Simple { channel })
                .collect(),
            unresolved_chans: HashSet::new(),
            //analysis_requests: HashSet::new(),
            full_requests: HashSet::new(),
            lookup_analysis_id: HashMap::new(),
        }
    }
}

impl From<Vec<ChannelId>> for ViewSet {
    fn from(value: Vec<ChannelId>) -> Self {
        let mut unresolved_chans = HashSet::new();

        value
            .into_iter()
            .for_each(|c| unresolved_chans.extend(c.to_channel_headers()));

        Self {
            members: HashSet::new(),
            unresolved_chans,
            full_requests: HashSet::new(),
            lookup_analysis_id: HashMap::new(),
        }
    }
}

impl From<HashSet<AnalysisRequestId>> for ViewSet {
    fn from(analysis_requests: HashSet<AnalysisRequestId>) -> Self {
        let mut full_requests = HashSet::new();
        for id in &analysis_requests {
            fill_out_recursive(&mut full_requests, id);
        }

        let mut unresolved_chans = HashSet::new();
        for r in &full_requests {
            let headers: HashSet<ChannelHeader> = r.channels().collect();
            unresolved_chans.extend(headers);
        }

        Self {
            members: HashSet::new(),
            unresolved_chans,
            full_requests,
            lookup_analysis_id: HashMap::new(),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl ViewSet {
    /// convenience function
    /// for turning a simple list of channels into a ViewSet
    #[staticmethod]
    pub fn from_channels(channels: Vec<Channel>) -> Self {
        channels.into()
    }

    /// convenience function
    /// for turning a simple list of channel names into a ViewSet with
    /// unresolved channel names
    #[staticmethod]
    pub fn from_channel_names(channel_names: Vec<String>, trend: TrendType) -> Self {
        let ids: Vec<_> = channel_names
            .into_iter()
            .map(|n| ChannelId::new(n, trend.clone()))
            .collect();
        ids.into()
    }

    #[staticmethod]
    pub fn from_analysis_request_ids(request_ids: HashSet<AnalysisRequestId>) -> Self {
        request_ids.into()
    }

    pub fn has_unresolved_channels(&self) -> bool {
        !self.unresolved_chans.is_empty()
    }

    /// Return the resolved names of any channels in the set
    /// Including expected resolved names of unresolved channels.
    pub fn to_resolved_channel_names(&self) -> Vec<String> {
        let mut headers_set: HashSet<ChannelHeader> =
            HashSet::with_capacity(self.unresolved_chans.len() + self.members.len());

        for member in &self.members {
            if let AnalysisId::Simple { channel } = member {
                headers_set.insert(channel.into());
            }
        }

        headers_set.extend(self.unresolved_chans.iter().map(|c| c.clone()));

        headers_set.iter().map(|c| c.nds_name()).collect()
    }
}

impl ViewSet {
    /// Change any unresolved channel names to resolved channels.
    pub(super) async fn resolve_channels(&mut self, block: DataBlock) -> Option<DataBlock> {
        debug!("resolve channels on a block");
        for channel in block.keys() {
            debug!(
                "looking for channel {}:{}",
                channel.name, channel.trend_stat
            );
            let header = channel.into();
            if self.unresolved_chans.contains(&header) {
                self.unresolved_chans.remove(&header);
                let real_id = AnalysisId::Simple {
                    channel: channel.clone(),
                };
                let header_id = AnalysisHeaderId::Simple {
                    channel: header.clone(),
                };
                self.lookup_analysis_id.insert(header_id, real_id.clone());
                self.members.insert(real_id);
            }
        }

        if self.has_unresolved_channels() {
            None
        } else {
            self.populate_compound_members();
            Some(block)
        }
    }

    fn populate_compound_members(&mut self) {
        for id in &self.full_requests {
            self.members
                .insert(populate_compound_member(id, &mut self.lookup_analysis_id));
        }
    }

    // /// fill out the sets to contain every element of the analysis request.
    // pub (super) async fn fill_out_analysis_requests(&mut self) {
    //     //let mut new_channels: HashSet<ChannelHeader> = HashSet::new();
    //     let fr = &mut self.full_requests;
    //     for r in &self.analysis_requests {
    //         for c in r.channels() {
    //             self.unresolved_chans.extend(c.to_channel_headers());
    //         }
    //         fill_out_recursive(fr, r);
    //     }
    // }
}

fn fill_out_recursive(
    full_requests: &mut HashSet<AnalysisHeaderId>,
    request_id: &AnalysisRequestId,
) -> AnalysisHeaderId {
    match request_id {
        AnalysisRequestId::Simple { channel } => {
            let mut saved = None;
            for header in channel.to_channel_headers() {
                let id = AnalysisHeaderId::Simple { channel: header };
                let fc = id.first_channel().expect("always at least 1 channel");
                if fc.trend_stat == TrendStat::Mean || fc.trend_stat == TrendStat::Raw {
                    saved = Some(id.clone());
                }
                full_requests.insert(id);
            }

            saved.expect("There's always either a mean or a raw")
        }
        AnalysisRequestId::Compound { name, args } => {
            let new_args = args
                .iter()
                .map(|a| fill_out_recursive(full_requests, a))
                .collect();
            let id = AnalysisHeaderId::Compound {
                name: name.clone(),
                args: new_args,
            };
            full_requests.insert(id.clone());
            id
        }
    }
}

fn populate_compound_member(
    header_id: &AnalysisHeaderId,
    lookup: &mut HashMap<AnalysisHeaderId, AnalysisId>,
) -> AnalysisId {
    if lookup.contains_key(header_id) {
        return lookup
            .get(header_id)
            .expect("checked for key immediately prior")
            .clone();
    }

    let new_id = match header_id {
        AnalysisHeaderId::Simple { channel } => panic!("found unbound channel {:?}", channel),
        AnalysisHeaderId::Compound { name, args } => {
            let new_args = args
                .iter()
                .map(|a| populate_compound_member(a, lookup))
                .collect();
            AnalysisId::Compound {
                name: name.clone(),
                args: new_args,
            }
        }
    };
    lookup.insert(header_id.clone(), new_id.clone());
    new_id
}
