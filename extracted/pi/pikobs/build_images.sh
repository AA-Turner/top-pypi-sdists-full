#!/usr/bin/env bash
# ============================================================================
# pikobs_doc_images.sh
# ----------------------------------------------------------------------------
# Copy one representative figure of each module into docs/source/_static,
# with the fixed names the docstrings reference. Run it after the modules
# have produced their output, then rebuild the documentation:
#
#     ./pikobs_doc_images.sh
#     cd docs && make html
#
# Only the modules whose PATHWORK exists are touched, so it is fine to run
# it when just one of them has been re-run.
# ============================================================================
set -uo pipefail

# ---- where each module wrote its output ------------------------------------
# Two kinds of directory. The ones named pikobs_doc_* are written by
# run_doc_examples.sh: the operational suite against the parallel one,
# every module over the same days, which is where every comparison figure
# should come from. The plain ones are ordinary runs of each wrapper, and
# they are where a single-run figure has to come from -- taking one from a
# comparison directory is how the page came to show a difference map as
# its example of a run on its own.
DOC="/home/${USER}/sites8/pikobs_doc"

SCATTER_EXP="${DOC}_scatter_exp"
SCATTER_CMP="${DOC}_scatter"
OBSCOUNTDB="${DOC}_obscountdb"
VDEDR="${DOC}_vdedr"
CARDIO="${DOC}_cardio"
FLAGS="${DOC}_flags"
MAPOBS="${DOC}_mapobs"
ZONE="${DOC}_zone"
VERIFPROFILE="${DOC}_verifprofile"
HISTOGRAM="${DOC}_histogram_exp"
HISTOGRAM_CMP="${DOC}_histogram"
PROFILE="${DOC}_profile_radar"
PROFILE_CMP="${DOC}_profile"
TIMESERIE="${DOC}_timeserie"
TIMESERIE_RUN="${DOC}_timeserie_exp"
REGIONS="/home/${USER}/sites8/pikobs_regions"

# ---- where the documentation looks for them --------------------------------
STATIC="docs/source/_static"

# Family preferred for each module; the first one found is used, and if
# none matches, the first family directory of the run is taken.
SCATTER_FAMILY="${SCATTER_FAMILY:-cris iasi to_amsua_allsky sw ai ua}"
OBSCOUNTDB_FAMILY="${OBSCOUNTDB_FAMILY:-sw ai ua to_amsua_allsky}"
VDEDR_FAMILY="${VDEDR_FAMILY:-to_amsua_allsky atms_allsky cris iasi}"
CARDIO_FAMILY="${CARDIO_FAMILY:-sw ai ua to_amsua_allsky}"
FLAGS_FAMILY="${FLAGS_FAMILY:-to_amsua_allsky atms_allsky iasi cris}"
MAPOBS_FAMILY="${MAPOBS_FAMILY:-sw to_amsua_allsky atms_allsky iasi}"
ZONE_FAMILY="${ZONE_FAMILY:-sw ua ai to_amsua_allsky}"
VERIFPROFILE_FAMILY="${VERIFPROFILE_FAMILY:-ch ro sw ua}"
HISTOGRAM_FAMILY="${HISTOGRAM_FAMILY:-sw ua ai iasi}"
PROFILE_FAMILY="${PROFILE_FAMILY:-ra radar ua ai sw}"
TIMESERIE_FAMILY="${TIMESERIE_FAMILY:-sw ua ai}"

# Longest side of the copied image; larger ones are resized to keep the
# documentation light. Set to 0 to copy as is.
MAX_WIDTH="${MAX_WIDTH:-1800}"

# The figure of the statistics page is not copied from a run: it is drawn
# from the functions of pikobs.stats, so the percentages printed on it are
# the ones Pikobs reports. Point this at the script, or leave it empty to
# keep whatever is already in _static.
STATS_FIGURE="${STATS_FIGURE:-pikobs/build_doc/build_stats_figure.py}"
PROFILE_RUN="${DOC}_profile_exp"
CARDIO_EXP="${DOC}_cardio_exp"

# ============================================================================
if [ ! -d "${STATIC}" ]; then
    echo "ERROR: ${STATIC} not found: run this from the root of the repository." >&2
    exit 1
fi

pick_family() {   # pick_family <pathwork> <preferred families>
    local work="$1"; shift
    local fam
    for fam in $@; do
        [ -d "${work}/${fam}" ] && { echo "${fam}"; return; }
    done
    for fam in "${work}"/*/; do
        fam="$(basename "${fam}")"
        case "${fam}" in figures|tables) continue ;; esac
        echo "${fam}"; return
    done
}

copy_one() {      # copy_one <source png> <target name>
    local src="$1" dst="${STATIC}/$2"
    if [ -z "${src}" ] || [ ! -f "${src}" ]; then
        echo "  skip  $2  (no source found)"
        return
    fi
    cp "${src}" "${dst}"
    if [ "${MAX_WIDTH}" -gt 0 ] && command -v python > /dev/null; then
        python - "${dst}" "${MAX_WIDTH}" <<'EOF' 2> /dev/null
import sys
from PIL import Image
path, limit = sys.argv[1], int(sys.argv[2])
im = Image.open(path)
if im.width > limit:
    im = im.resize((limit, round(im.height * limit / im.width)))
    im.save(path, optimize=True)
EOF
    fi
    echo "  ok    $2  <- $(basename "${src}")"
}

first() {         # first <glob...>: the first existing file of the patterns
    local pattern match
    for pattern in "$@"; do
        match="$(ls -1 ${pattern} 2> /dev/null | head -1)"
        [ -n "${match}" ] && { echo "${match}"; return; }
    done
}

first_plain() {   # first_plain <glob...>: the first file, not a panel, of the patterns
    local pattern match
    for pattern in "$@"; do
        match="$(ls -1 ${pattern} 2> /dev/null | grep -v '_signif\.png$\|_sigonly\.png$' | head -1)"
        [ -n "${match}" ] && { echo "${match}"; return; }
    done
}

# ---- scatter: single run ---------------------------------------------------
if [ -d "${SCATTER_EXP}" ]; then
    fam="$(pick_family "${SCATTER_EXP}" ${SCATTER_FAMILY})"
    echo "scatter (single run), family ${fam}:"
    dir="${SCATTER_EXP}/${fam}"
    for fn in omp oma stdomp stdoma bcorr obs nobs dens; do
        copy_one "$(first "${dir}/${fn}_npolar_*flag_assimilee_*_Monde_vcoord_32_*.png" "${dir}/${fn}_npolar_*_Monde_vcoord_32_*.png" "${dir}/${fn}_*flag_assimilee_*vcoord_join_*.png" "${dir}/${fn}_*flag_assimilee_*.png" \
                          "${dir}/${fn}_*.png")" "scatter_exp_${fn}.png"
    done
fi

# ---- scatter: control vs experience ----------------------------------------
if [ -d "${SCATTER_CMP}" ]; then
    fam="$(pick_family "${SCATTER_CMP}" ${SCATTER_FAMILY})"
    echo "scatter (comparison), family ${fam}:"
    dir="${SCATTER_CMP}/${fam}"
    # O-A is what the page shows: between two passes of one cycle (G0,
    # G2) O-B is identical, see "Two passes of the same cycle"
    for fn in omp oma stdomp stdoma; do
        copy_one "$(first_plain "${dir}/${fn}_npolar_*flag_assimilee_*_Monde_vcoord_32_*_vs_*.png" "${dir}/${fn}_npolar_*_Monde_vcoord_32_*_vs_*.png" "${dir}/${fn}_*flag_assimilee_*vcoord_join_*_vs_*.png" \
                                "${dir}/${fn}_*flag_assimilee_*_vs_*.png" "${dir}/${fn}_*_vs_*.png")" \
                 "scatter_cmp_${fn}_difference.png"
        copy_one "$(first "${dir}/${fn}_npolar_*flag_assimilee_*_Monde_vcoord_32_*_signif.png" "${dir}/${fn}_npolar_*_Monde_vcoord_32_*_signif.png" "${dir}/${fn}_*flag_assimilee_*vcoord_join_*_signif.png" "${dir}/${fn}_*flag_assimilee_*_signif.png" \
                          "${dir}/${fn}_*_signif.png")"  "scatter_cmp_${fn}_significance.png"
        copy_one "$(first "${dir}/${fn}_npolar_*flag_assimilee_*_Monde_vcoord_32_*_sigonly.png" "${dir}/${fn}_npolar_*_Monde_vcoord_32_*_sigonly.png" "${dir}/${fn}_*flag_assimilee_*vcoord_join_*_sigonly.png" "${dir}/${fn}_*flag_assimilee_*_sigonly.png" \
                          "${dir}/${fn}_*_sigonly.png")" "scatter_cmp_${fn}_sigonly.png"
    done
    copy_one "$(first_plain "${dir}/nobs_npolar_*flag_assimilee_*_Monde_vcoord_32_*_vs_*.png" "${dir}/nobs_npolar_*_Monde_vcoord_32_*_vs_*.png" "${dir}/nobs_*flag_assimilee_*vcoord_join_*_vs_*.png" "${dir}/nobs_*flag_assimilee_*_vs_*.png" \
                            "${dir}/nobs_*_vs_*.png")" \
             "scatter_cmp_nobs_difference.png"
fi

# ---- obscountdb ------------------------------------------------------------
if [ -d "${OBSCOUNTDB}/figures" ]; then
    echo "obscountdb:"
    copy_one "$(first "${OBSCOUNTDB}/figures/*.png")" "obscountdb_station.png"
fi

# ---- vdedr -----------------------------------------------------------------
if [ -d "${VDEDR}" ]; then
    fam="$(pick_family "${VDEDR}" ${VDEDR_FAMILY})"
    echo "vdedr, family ${fam}:"
    dir="${VDEDR}/${fam}"
    copy_one "$(first "${dir}/omp_rel_*.png")"  "vdedr_omp_rel.png"
    copy_one "$(first "${dir}/omp_bias_*.png")" "vdedr_omp_bias.png"
fi

# ---- cardio ----------------------------------------------------------------
if [ -d "${CARDIO}" ]; then
    fam="$(pick_family "${CARDIO}" ${CARDIO_FAMILY})"
    echo "cardio, family ${fam}:"
    copy_one "$(first "${CARDIO}/${fam}/serie_*.png")" "cardio_panels.png"
fi

# ---- flags -----------------------------------------------------------------
if [ -d "${FLAGS}" ]; then
    fam="$(pick_family "${FLAGS}" ${FLAGS_FAMILY})"
    echo "flags, family ${fam}:"
    copy_one "$(first "${FLAGS}/${fam}/flags_*.png")" "flags_plot.png"
fi

# ---- mapobs ----------------------------------------------------------------
# mapobs writes one figure per panel, in <family>_6h; the documentation
# shows the vertical distribution and a polar map, so a polar region is
# preferred when the run has one.
if [ -d "${MAPOBS}" ]; then
    fam=""
    for cand in ${MAPOBS_FAMILY}; do
        [ -d "${MAPOBS}/${cand}_6h" ] && { fam="${cand}"; break; }
    done
    if [ -z "${fam}" ]; then
        for dir in "${MAPOBS}"/*_6h/; do
            fam="$(basename "${dir}")"; fam="${fam%_6h}"; break
        done
    fi
    if [ -n "${fam}" ]; then
        echo "mapobs, family ${fam}:"
        dir="${MAPOBS}/${fam}_6h"
        copy_one "$(first "${dir}/vertical_*.png")" "mapobs_dashboard.png"
        # a polar map if the run has one, otherwise any map
        copy_one "$(first "${dir}/map_*npolar*.png" "${dir}/map_*spolar*.png" \
                          "${dir}/map_*canada*.png" "${dir}/map_*.png")" \
                 "mapobs_polar.png"
    fi
fi

# ---- zone ------------------------------------------------------------------
# A comparison if the run had a control (the file name holds "_vs_"),
# otherwise any section; "join" first, since it is the one worth showing.
if [ -d "${ZONE}" ]; then
    fam="$(pick_family "${ZONE}" ${ZONE_FAMILY})"
    echo "zone, family ${fam}:"
    dir="${ZONE}/${fam}"
    copy_one "$(first "${dir}/zone_*_vs_*_oma_*_join_Monde_*.png" "${dir}/zone_*_vs_*_oma_*_join_*.png" "${dir}/zone_*_vs_*_join_*.png" "${dir}/zone_*_vs_*.png" \
                      "${dir}/zone_*_join_*.png" "${dir}/zone_*.png")" \
             "zone_comparison.png"
fi

# ---- verifprofile ------------------------------------------------------------
if [ -d "${VERIFPROFILE}" ]; then
    fam="$(pick_family "${VERIFPROFILE}" ${VERIFPROFILE_FAMILY})"
    echo "verifprofile, family ${fam}:"
    dir="${VERIFPROFILE}/${fam}"
    copy_one "$(first "${dir}/verifprofile_*_vs_*_join_*.png" \
                      "${dir}/verifprofile_*_vs_*.png" "${dir}/verifprofile_*.png")" \
             "verifprofile_comparison.png"
fi

# ---- histogram ----------------------------------------------------------------
# three runs, one folder each, same settings otherwise:
#   pikobs_histogram       a run of the wrapper       -> the single run
#   pikobs_doc_histogram   run_doc_examples.sh, which has a control and
#                          runs with QC_SPLIT="on" and both flag criteria
#                          -> the comparison and the QC split
# each folder is looked at for its own image, and the plain one as a fallback
if [ -d "${HISTOGRAM}" ] || [ -d "${HISTOGRAM_CMP}" ] || [ -d "${HISTOGRAM_CMP}" ]; then
    echo "histogram:"
    for d in "${HISTOGRAM}" "${HISTOGRAM_CMP}" "${HISTOGRAM_CMP}"; do
        [ -d "${d}" ] || echo "  note  ${d} not found"
    done
    fam="$(pick_family "${HISTOGRAM}" ${HISTOGRAM_FAMILY})"
    fam_c="$(pick_family "${HISTOGRAM_CMP}" ${HISTOGRAM_FAMILY})"
    fam_q="$(pick_family "${HISTOGRAM_CMP}" ${HISTOGRAM_FAMILY})"
    # "join" figures first: all levels and all stations read best on a page
    copy_one "$(first "${HISTOGRAM}/${fam}/histogram_*_omp_*levjoin_join_*.png" \
                      "${HISTOGRAM}/${fam}/histogram_*_omp_*.png" \
                      "${HISTOGRAM}/${fam}/histogram_*.png")" \
             "histogram_single.png"
    copy_one "$(first "${HISTOGRAM_CMP}/${fam_c}"/histogram_*_vs_*levjoin_join_*_assimilee.png \
                      "${HISTOGRAM_CMP}/${fam_c}"/histogram_*_vs_*levjoin_join_*_assimilee_*.png \
                      "${HISTOGRAM_CMP}/${fam_c}"/histogram_*_vs_*_assimilee_*.png \
                      "${HISTOGRAM_CMP}/${fam_c}"/histogram_*_vs_*levjoin_join_*.png \
                      "${HISTOGRAM_CMP}/${fam_c}"/histogram_*_vs_*.png)" \
             "histogram_comparison.png"
    # The QC split reads best with every observation in it, so take the
    # "all" criteria figure; the comparison above takes "assimilee".
    # Without this both patterns match the same file and the page shows
    # one figure twice under two captions.
    copy_one "$(first "${HISTOGRAM_CMP}/${fam_q}"/histogram_*levjoin_join_*_all.png \
                      "${HISTOGRAM_CMP}/${fam_q}"/histogram_*levjoin_join_*_all_all.png \
                      "${HISTOGRAM_CMP}/${fam_q}"/histogram_*_all_all.png \
                      "${HISTOGRAM_CMP}/${fam_q}"/histogram_*levjoin_join_*.png \
                      "${HISTOGRAM_CMP}/${fam_q}"/histogram_*.png)" \
             "histogram_qc_split.png"
fi

# ---- verifprofile, the scorecard ---------------------------------------------
# the O-P scorecard of a summer experiment against its control: between G0 and
# G2 O-P is the same, and their scorecard would be grey
SC_DIR="${DOC}_verifprofile_scorecard/scorecard"
if [ -d "${SC_DIR}" ]; then
    echo "verifprofile, scorecard:"
    copy_one "$(first "${SC_DIR}"/scorecard_*_omp_*.png)" "verifprofile_scorecard.png"
fi

# ---- profile ------------------------------------------------------------------
# The comparison and the plain run come from the reference run, which has
# conventional families; the radar view can only come from a run over
# radar data, which the operational suites do not carry.
if [ -d "${PROFILE}" ] || [ -d "${PROFILE_CMP}" ]; then
    fam="$(pick_family "${PROFILE_CMP}" ${PROFILE_FAMILY})"
    echo "profile, family ${fam}:"
    dir="${PROFILE_CMP}/${fam}"
    copy_one "$(first "${dir}"/profile_*_vs_*join*.png "${dir}"/profile_*_vs_*.png)" \
             "profile_change.png"
    # the radar view: one elevation of one network against the height, where
    # the OBS_ERROR of the files, the model and the fit are drawn
    radar_fam="$(pick_family "${PROFILE}" radar ra)"
    rdir="${PROFILE}/${radar_fam}"
    copy_one "$(first "${rdir}"/profile_*_omp_*upct_*assimilee_elev1.5_height.png \
                      "${rdir}"/profile_*_omp_*upct_*assimilee_elev1.0_height.png \
                      "${rdir}"/profile_*_omp_*upct_*assimilee_elev0.8_height.png \
                      "${rdir}"/profile_*_omp_*pct_*_elev*_height.png)" \
             "profile_radar.png"
    # the plain run comes from a conventional family, never from radar:
    # otherwise both patterns fall back to the same file and the page
    # shows one figure twice under two captions
    run_fam="$(pick_family "${PROFILE_RUN}" ua ai sw ro)"
    if [ -n "${run_fam}" ] && [ "${run_fam}" != "radar" ]; then
        copy_one "$(first "${PROFILE_RUN}/${run_fam}"/profile_*_omp_*join*.png \
                          "${PROFILE_RUN}/${run_fam}"/profile_*.png)" \
                 "profile_run.png"
    else
        echo "  skip  profile_run.png  (the run has only radar; add ua or"
        echo "        sw to FAMILY in run_profile_exp.sh / run_profile_cont_exp.sh)"
    fi
fi

# ---- timeserie ----------------------------------------------------------------
if [ -d "${TIMESERIE}" ]; then
    fam="$(pick_family "${TIMESERIE}" ${TIMESERIE_FAMILY})"
    echo "timeserie, family ${fam}:"
    dir="${TIMESERIE}/${fam}"
    copy_one "$(first "${dir}"/timeserie_all_vs_*_levjoin_*.png "${dir}"/timeserie_all_vs_*.png)" \
             "timeserie_comparison.png"
    copy_one "$(first "${dir}"/timeserie_[!a]*_levjoin_*.png "${dir}"/timeserie_*.png)" \
             "timeserie_run.png"
fi

# ---- regions ------------------------------------------------------------------
# one box and one polygon are enough on the page; regions.html has them all
if [ -d "${REGIONS}" ]; then
    echo "regions:"
    copy_one "$(first "${REGIONS}/region_canada.png" \
                      "${REGIONS}/region_monde.png" \
                      "${REGIONS}/region_*.png")" "region_box.png"
    copy_one "$(first "${REGIONS}/region_hrdps.png" \
                      "${REGIONS}/region_*_clim.png")" "region_polygon.png"
fi

# ---- statistics page -------------------------------------------------------
# Drawn, not copied: it explains what the t-test and the F-test each see,
# with the numbers computed by the module itself.
if [ -n "${STATS_FIGURE}" ] && [ -f "${STATS_FIGURE}" ]; then
    echo "stats:"
    if python "${STATS_FIGURE}" "${STATIC}/stats_tests.png" > /dev/null 2>&1; then
        echo "  ok    stats_tests.png  <- drawn by $(basename "${STATS_FIGURE}")"
    else
        echo "  skip  stats_tests.png  (the script failed; is pikobs importable?)"
    fi
fi

echo
echo "Now rebuild the documentation:  cd docs && make html"
