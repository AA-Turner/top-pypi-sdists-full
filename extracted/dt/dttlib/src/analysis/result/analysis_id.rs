use std::collections::HashSet;
use std::fmt::{Display, Formatter};

use crate::analysis::result::EdgeDataType;
use crate::params::channel_params::ChannelName;
use crate::{
    errors::DTTError,
    params::channel_params::{Channel, ChannelHeader, ChannelId, ChannelSettings, TrendType},
};

#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::{new, staticmethod};
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass_complex_enum, gen_stub_pymethods};

/// create a tree of Analysis functions with channel identifiers
/// of some type as the leaves of the tree
///
/// $trend_target is the .into() target when converting
/// from (TrendType, $name)
macro_rules! create_id {
    ($name: ident, $leaf: ident, $iterator: ident, $trend_target: ident) => {
        /// This is the name of a result
        /// Can be of the simple form "SomeChannelName"
        /// Or the compound form "Name(OtherID1, OtherID2, ...)"
        ///
        /// Structured to avoid unnecessary string parsing
        #[derive(Clone, Hash, Debug, PartialEq, Eq, Ord, PartialOrd)]
        #[cfg_attr(feature = "all", gen_stub_pyclass_complex_enum)]
        #[cfg_attr(
            any(feature = "python", feature = "python-pipe"),
            pyclass(frozen, str, eq, hash)
        )]
        pub enum $name {
            Simple { channel: $leaf },
            Compound { name: String, args: Vec<$name> },
        }

        impl Display for $name {
            fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
                match self {
                    Self::Compound { name, args } => {
                        f.write_str(name)?;
                        if !args.is_empty() {
                            let mut first = true;
                            f.write_str("(")?;
                            for sub_id in args {
                                if first {
                                    first = false;
                                } else {
                                    f.write_str(", ")?;
                                }
                                f.write_str(&sub_id.to_string())?;
                            }
                            f.write_str(")")?;
                        }
                    }
                    Self::Simple { channel } => {
                        f.write_str(&channel.name)?;
                    }
                }
                Ok(())
            }
        }

        #[cfg_attr(feature = "all", gen_stub_pymethods)]
        #[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
        impl $name {
            #[staticmethod]
            pub fn from_channel(channel: $leaf) -> Self {
                $name::Simple { channel }
            }

            #[new]
            pub fn new(name: String, args: Vec<$name>) -> Self {
                $name::Compound { name, args }
            }

            /// get the first channel
            pub fn first_channel(&self) -> Result<$leaf, DTTError> {
                //there's always one channel
                self.channels().next().ok_or(DTTError::CalcError(
                    "A result ID has no associated channel".to_string(),
                ))
            }

            /// The set is pass-through ownership so that the function is usable from python
            ///
            /// This function is needed to "flesh out" the collection of analyses request
            /// by the user to include all intermediate analyses
            pub fn add_to_set_recursive(&self, mut set: HashSet<Self>) -> HashSet<Self> {
                set.insert(self.clone());

                if let $name::Compound { name: _name, args } = self {
                    for arg in args {
                        set = arg.add_to_set_recursive(set);
                    }
                }

                set
            }

            pub fn add_trend(&self, trend: &TrendType) -> $trend_target {
                match &self {
                    $name::Simple { channel } => {
                        $trend_target::from_channel((channel, trend.clone()).into())
                    }
                    $name::Compound { name, args } => {
                        let new_args = args.iter().map(|a| a.add_trend(trend)).collect();
                        $trend_target::new(name.clone(), new_args)
                    }
                }
            }

            pub fn to_analysis_name_id(&self) -> AnalysisNameId {
                match &self {
                    $name::Simple { channel } => {
                        let c: ChannelName = channel.clone().into();
                        AnalysisNameId::from_channel(c)
                    }
                    $name::Compound { name, args } => {
                        let new_args = args.iter().map(|a| a.to_analysis_name_id()).collect();
                        AnalysisNameId::new(name.clone(), new_args)
                    }
                }
            }

            pub fn get_channels(&self) -> HashSet<$leaf> {
                self.channels().map(|c| c.clone()).collect()
            }
        }

        impl $name {
            pub fn channels(&'_ self) -> $iterator<'_> {
                $iterator::new(self)
            }
        }

        impl<T> From<T> for $name
        where
            $leaf: From<T>,
        {
            fn from(value: T) -> Self {
                let c: $leaf = value.into();
                Self::from_channel(c)
            }
        }

        impl Default for $name {
            fn default() -> Self {
                return $leaf::default().into();
            }
        }

        pub struct $iterator<'a> {
            id: &'a $name,
            count: usize,
            sub_iterator: Option<Box<$iterator<'a>>>,
            done: bool,
        }

        impl<'a> Iterator for $iterator<'a> {
            type Item = $leaf;

            /// depth-first iteration of all channels in the id
            fn next(&mut self) -> Option<Self::Item> {
                match self.id {
                    $name::Simple { channel } => {
                        if self.done {
                            None
                        } else {
                            self.done = true;
                            Some(channel.clone())
                        }
                    }
                    $name::Compound { name: _, args } => {
                        if self.count < args.len() {
                            match &mut self.sub_iterator {
                                None => {
                                    self.sub_iterator =
                                        Some(Box::new($iterator::new(&args[self.count])));
                                    self.next()
                                }
                                Some(sub) => match sub.next() {
                                    Some(x) => Some(x),
                                    None => {
                                        self.count += 1;
                                        self.sub_iterator = None;
                                        self.next()
                                    }
                                },
                            }
                        } else {
                            None
                        }
                    }
                }
            }
        }

        impl<'a> $iterator<'a> {
            fn new(id: &'a $name) -> Self {
                Self {
                    id,
                    count: 0,
                    sub_iterator: None,
                    done: false,
                }
            }
        }
    };
}

create_id!(AnalysisId, Channel, ChannelIterator, AnalysisId);
create_id!(
    AnalysisRequestId,
    ChannelId,
    ChannelIdIterator,
    AnalysisRequestId
);
create_id!(
    AnalysisNameId,
    ChannelName,
    ChannelNameIterator,
    AnalysisRequestId
);

create_id!(
    AnalysisHeaderId,
    ChannelHeader,
    ChannelHeaderIterator,
    AnalysisHeaderId
);

create_id!(
    AnalysisSettingsId,
    ChannelSettings,
    ChannelSettingsIterator,
    AnalysisSettingsId
);

#[macro_export]
macro_rules! analysis_id {
    ($name:expr, $($args:expr), +) => {
        AnalysisId::Compound {
            name: $name.to_string(),
            args: vec!($($args.into()),+),
        }
    };
    ($channel:expr) => {
        AnalysisId::Simple{channel: Channel::from($channel)}
    }
}

impl TryFrom<&AnalysisId> for EdgeDataType {
    type Error = DTTError;

    fn try_from(value: &AnalysisId) -> Result<Self, Self::Error> {
        Ok(match value {
            AnalysisId::Simple { channel } => channel.data_type.clone().into(),
            AnalysisId::Compound { name, args } => {
                // first argument type is often all that's needed
                let arg0 = &args[0];
                let arg0_type: EdgeDataType = arg0.try_into()?;
                if name == "complex" {
                    match arg0_type {
                        EdgeDataType::FreqDomainValueReal => EdgeDataType::FreqDomainValueComplex,
                        EdgeDataType::TimeDomainValueReal => EdgeDataType::TimeDomainValueComplex,
                        _ => {
                            return Err(DTTError::AnalysisPipelineError(format!(
                                "'{}' is not a valid input for a 'complex' operator.  Must be a 64-bit floating point real.",
                                arg0_type
                            )));
                        }
                    }
                } else if name == "phase" {
                    match arg0_type {
                        EdgeDataType::FreqDomainValueComplex => EdgeDataType::FreqDomainValueReal,
                        EdgeDataType::TimeDomainValueComplex => EdgeDataType::TimeDomainValueReal,
                        _ => {
                            return Err(DTTError::AnalysisPipelineError(format!(
                                "'{}' is not a valid input for a 'phase' operator.  Must be a complex value.",
                                arg0_type
                            )));
                        }
                    }
                } else {
                    return Err(DTTError::AnalysisPipelineError(format!(
                        "Could not determine output edge type for '{}'",
                        name
                    )));
                }
            }
        })
    }
}

/// Useful or ndscope views which do not set any channel settings
impl From<AnalysisId> for AnalysisSettingsId {
    fn from(value: AnalysisId) -> Self {
        match value {
            AnalysisId::Simple { channel } => Self::Simple {
                channel: channel.into(),
            },
            AnalysisId::Compound { name, args } => {
                let new_args = args.into_iter().map(|a| a.into()).collect();
                Self::Compound {
                    name,
                    args: new_args,
                }
            }
        }
    }
}
