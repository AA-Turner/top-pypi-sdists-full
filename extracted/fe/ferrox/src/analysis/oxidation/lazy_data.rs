// === Lazy Data Loading ===

use super::compressed_data::{BV_PARAMS_GZ, ICSD_BV_STATS_GZ, ICSD_OXI_PROB_GZ};
use super::data_structs::{BvParams, BvStats};
use flate2::read::GzDecoder;
use std::collections::HashMap;
use std::io::Read;
use std::sync::OnceLock;

// Type aliases for data maps
type OxiProbMap = HashMap<String, u32>;
type BvStatsMap = HashMap<String, BvStats>;
type BvParamsMap = HashMap<String, BvParams>;

static ICSD_OXI_PROB: OnceLock<OxiProbMap> = OnceLock::new();
static ICSD_BV_STATS: OnceLock<BvStatsMap> = OnceLock::new();
static BV_PARAMS: OnceLock<BvParamsMap> = OnceLock::new();

fn decompress_json<T: serde::de::DeserializeOwned>(gz_data: &[u8]) -> T {
    let mut decoder = GzDecoder::new(gz_data);
    let mut json = String::new();
    decoder
        .read_to_string(&mut json)
        .expect("Failed to decompress gzipped JSON");
    serde_json::from_str(&json).expect("Failed to parse JSON data")
}

/// Get ICSD oxidation state occurrence probabilities.
///
/// Keys are "Element:oxidation_state" (e.g., "Fe:3", "O:-2").
pub fn get_icsd_oxi_prob() -> &'static OxiProbMap {
    ICSD_OXI_PROB.get_or_init(|| decompress_json(ICSD_OXI_PROB_GZ))
}

/// Get ICSD BVS statistics (mean, std, n).
///
/// Keys are "Element:oxidation_state" (e.g., "Fe:3", "O:-2").
pub fn get_icsd_bv_stats() -> &'static BvStatsMap {
    ICSD_BV_STATS.get_or_init(|| decompress_json(ICSD_BV_STATS_GZ))
}

/// Get O'Keeffe & Brese bond valence parameters.
///
/// Keys are element symbols (e.g., "Fe", "O").
pub fn get_bv_params() -> &'static BvParamsMap {
    BV_PARAMS.get_or_init(|| decompress_json(BV_PARAMS_GZ))
}
