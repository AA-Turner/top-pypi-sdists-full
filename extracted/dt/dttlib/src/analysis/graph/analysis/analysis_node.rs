use std::cmp::Ordering;
use std::hash::{Hash, Hasher};

use crate::AnalysisSettingsId;
use crate::analysis::graph::scheme::{SchemeNode, SchemePipelineType};

#[derive(Debug, Clone)]
pub(crate) struct AnalysisNode<'a> {
    pub pipeline_type: SchemePipelineType<'a>,
    pub name: String,
    pub id: Option<AnalysisSettingsId>,
}

impl<'a> PartialEq for AnalysisNode<'a> {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name && self.id == other.id
    }
}

impl<'a> Eq for AnalysisNode<'a> {}

impl<'a> Hash for AnalysisNode<'a> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.name.hash(state);
        self.id.hash(state);
    }
}

impl<'a> PartialOrd for AnalysisNode<'a> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<'a> Ord for AnalysisNode<'a> {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.id < other.id {
            Ordering::Less
        } else if self.id > other.id {
            Ordering::Greater
        } else if self.name < other.name {
            Ordering::Less
        } else if self.name > other.name {
            Ordering::Greater
        } else {
            Ordering::Equal
        }
    }
}

impl<'a> AnalysisNode<'a> {
    pub(crate) fn from_scheme_node(other: &SchemeNode<'a>) -> Self {
        Self {
            pipeline_type: other.pipeline_type.clone(),
            name: other.name.clone(),
            id: None,
        }
    }
}
