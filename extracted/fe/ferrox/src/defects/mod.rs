//! Point defect generation for crystal structures.
//!
//! This module provides functionality for creating and analyzing point defects
//! in crystal structures, including vacancies, substitutions, interstitials,
//! and antisite pairs.

mod creation;
mod generator;
mod interstitial_site;
mod supercell;
mod types;
mod voronoi;

pub use creation::{
    create_antisite_pair, create_interstitial, create_substitution, create_vacancy,
};
pub use generator::{
    DefectEntry, DefectsGeneratorConfig, DefectsGeneratorResult, generate_all_defects,
};
pub use interstitial_site::{InterstitialSiteType, classify_interstitial_site};
pub use supercell::{DefectSupercellConfig, find_defect_supercell};
pub use types::{DefectStructure, DefectType, PointDefect, generate_defect_name};
pub use voronoi::{VoronoiInterstitial, find_voronoi_interstitials};

#[cfg(test)]
mod tests;
