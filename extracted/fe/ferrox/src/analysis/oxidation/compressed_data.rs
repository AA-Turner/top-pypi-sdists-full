// === Compressed Data Files (embedded at compile time) ===

// ICSD oxidation state occurrence counts
pub(super) const ICSD_OXI_PROB_GZ: &[u8] = include_bytes!("../../data/icsd_oxi_prob.json.gz");

// BVS statistics (mean, std, n) per species
pub(super) const ICSD_BV_STATS_GZ: &[u8] = include_bytes!("../../data/icsd_bv_stats.json.gz");

// O'Keeffe & Brese BV parameters (r, c per element)
pub(super) const BV_PARAMS_GZ: &[u8] = include_bytes!("../../data/bv_params.json.gz");
