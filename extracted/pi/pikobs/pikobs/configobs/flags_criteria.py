def flag_criteria(flags):
    """
    Flag Criteria for Filtering Elements
    ====================================

    In data processing and analysis, flag criteria are essential for selecting and managing elements based on specific conditions or quality assessments. Pikobs uses a **bitmask system** to filter data effectively, focusing on elements that meet predefined standards or have undergone particular processing stages.

    Standard Flag Criteria
    ----------------------

    When using the ``--flags_criteria`` parameter in Pikobs, the system checks specific bits to determine if an observation should be included.

    ``all``
        **No restrictions:** Selects all available elements. No bitmask filters are applied.

    ``assimilee``
        **Assimilated elements:** * **Required Active Bits:** **BIT12** (4096) must be active (1).
        * Indicates that the observation has actively influenced the analysis. By default, this includes both clear and cloudy sky conditions.

    ``assimilee_full``
        **Assimilated with its full weight:** * **Required Active Bits:** **BIT12** (4096).
        * **Required Inactive Bits:** every rejection bit -- **BIT7** (128), **BIT9** (512), **BIT16** (65536), **BIT17** (131072), **BIT18** (262144) and **BIT19** (524288).
        * What the analysis used with its full weight. ``assimilee`` is this one plus ``assimilee_rejet``.

    ``assimilee_rejet``
        **Assimilated with a reduced weight:** * **Required Active Bits:** **BIT12** (4096) and at least one rejection bit of the list above (in practice BIT9 and BIT17).
        * Observations the variational QC kept with a reduced weight. They are few, but their sigma is several times that of the others, and on humidity their O-A can be absurd: enough to widen the sigma of a whole comparison.

    ``bgckalt``
        **Approved by Background Check:** * **Required Inactive Bits:** **BIT9** (512), **BIT11** (2048), and **BIT8** (256) must be inactive (0).
        * Removes observations rejected due to AO quality control, thinning/canal selection processes, and those on the blacklist.

    ``bgckalt_qc``
        **Approved by Background Check and QC-Var:** * **Required Inactive Bits:** **BIT9** (512) and **BIT11** (2048) must be inactive (0).

    ``monitoring``
        **Monitoring filter:** * **Required Inactive Bits:** **BIT9** (512) and **BIT7** (128) must be inactive (0).
        * Filters out observations rejected by AO quality control or satellite QC.

    ``postalt``
        **Post-Analysis filter:** * **Required Inactive Bits:** **BIT17** (131072), **BIT9** (512), **BIT11** (2048), and **BIT8** (256) must be inactive (0).
        * Removes data rejected by QC-Var, AO quality control, thinning/canal processes, and blacklisted observations.

    Splitting ``assimilee``
    -----------------------

    ``assimilee`` is every observation with BIT12. A few of them also carry a rejection bit, in practice BIT9 and BIT17: the variational QC did not throw them out, it kept them with a reduced weight. They are few, and they are not like the others. Over a summer of radiosondes, June to September 2025, in two suites that give the same picture:

    .. list-table:: Radiosondes with BIT12, June to September 2025
       :widths: 26 12 14 14 14 14
       :header-rows: 1

       * - Variable
         - Share with a rejection bit
         - Sigma O-P, full
         - Sigma O-P, rejet
         - Sigma O-A, full
         - Sigma O-A, rejet
       * - Wind, u component
         - 0.02 %
         - 2.47
         - 11.8
         - 1.79
         - 11.9
       * - Temperature
         - 0.1 %
         - 1.08
         - 4.67
         - 0.89
         - 4.61
       * - Dew point depression
         - 0.8 %
         - 4.0
         - 15.5
         - 2.5
         - 96 and 187

    Their O-P was already four to five times wider than the others: the QC had its reasons. Their O-A is as wide as their O-P, while for the others the analysis narrows it, which is what a reduced weight looks like -- the analysis hardly moves towards them. Humidity has one thing more. A few hundred of these observations, in very dry layers, come out with an O-A of hundreds or thousands of kelvins, which is not physical; the two numbers in the last cell are the two suites, and those few values alone make the difference.

    So ``assimilee_full`` gives the statistics of what the analysis used with its full weight, and ``assimilee_rejet`` isolates the rest. Asking for both, ``FLAGS_CRITERIA=(assimilee_full assimilee_rejet)``, shows them side by side in any module; in timeserie the panel of the sigma also draws the mean OBS_ERROR each group was given.

    Sky Condition Filters (Radiance Data)
    -------------------------------------

    For satellite radiances, specific flags can be used to filter assimilated observations based on cloud conditions using **BIT23** (Cloud-affected radiance).

    ``assimilee_clear_sky``
        **Clear Sky Only:**
        
        * **Required Active Bits:** **BIT12** (4096) must be active.
        * **Required Inactive Bits:** **BIT23** (8388608) must be strictly inactive (0).
        * Filters assimilated radiances that are completely free of cloud contamination.

    ``assimilee_cloudy_sky``
        **Cloudy Sky Only:**
        
        * **Required Active Bits:** Both **BIT12** (4096) and **BIT23** (8388608) must be active (1).
        * Filters radiances specifically flagged as being affected by clouds that successfully passed assimilation checks.

    ``assimilee_clear_cloudy_sky``
        **All-Sky (Clear + Cloudy):**
        
        * **Required Active Bits:** **BIT12** (4096) must be active.
        * This is the standard behavior for all-sky assimilation, accepting elements regardless of whether BIT23 is active or inactive.

    Radiances
    ---------

    Named filters matching each of :func:`flag_reason`'s bit-pattern
    diagnoses one-for-one (``ASSIMILATED`` is not repeated here -- use
    ``assimilee`` above, which is the same BIT12-only check; the
    cloud-affected-but-assimilated case is ``assimilee_cloudy_sky``
    above, not repeated here either since the two were identical).

    ``cloudy_rejected_qc``
        **Cloud-affected, rejected by quality control, not blacklisted:**

        * **Required Active Bits:** **BIT9** (512) and **BIT23** (8388608) must both be active.
        * **Required Inactive Bits:** **BIT8** (256) must be inactive.
        * The observation is cloud-affected and was rejected by the AO quality control (background check or QC-Var), and is not on the blacklist.

    ``cloudy_blacklisted``
        **Cloud-affected, rejected by quality control, and blacklisted:**

        * **Required Active Bits:** **BIT9** (512), **BIT23** (8388608), and **BIT8** (256) must all be active.
        * The observation is cloud-affected, was rejected by the AO quality control, and is also on the blacklist.

    ``cloudy_thinning``
        **Cloud-affected, rejected by thinning/canal selection, not blacklisted:**

        * **Required Active Bits:** **BIT11** (2048) and **BIT23** (8388608) must both be active.
        * **Required Inactive Bits:** **BIT8** (256) must be inactive.
        * The observation is cloud-affected and was rejected by the thinning/canal selection process, and is not on the blacklist.

    ``cloudy_thinning_blacklisted``
        **Cloud-affected, rejected by thinning/canal selection, and blacklisted:**

        * **Required Active Bits:** **BIT11** (2048), **BIT23** (8388608), and **BIT8** (256) must all be active.
        * The observation is cloud-affected, was rejected by thinning/canal selection, and is also on the blacklist.

    ``erroneous_data``
        **Required Active Bits:** at least one of **BIT0** (1), **BIT2** (4), or **BIT7** (128).
        The observation was modified/generated by ADE, flagged as an erroneous element, or rejected by satellite QC.

    ``blacklisted``
        **Required Active Bits:** **BIT8** (256).
        The observation (or channel) is on the blacklist.

    ``background_check_rogue``
        **Required Active Bits:** **BIT9** (512) and **BIT16** (65536).
        The observation was rejected by AO quality control specifically via the O-P innovation comparison against the test field (background check).

    ``not_assimilated_daytime``
        **Required Active Bits:** **BIT11** (2048) and **BIT7** (128).
        The observation was rejected by both thinning/canal selection and satellite QC -- typically daytime observations excluded from assimilation.

    ``land_sea_ice_sensitivity``
        **Required Active Bits:** **BIT19** (524288).
        The observation was not used because of its position relative to the land-sea mask.

    ``model_top_sensitivity``
        **Required Active Bits:** **BIT11** (2048) and **BIT21** (2097152).
        The observation was rejected by thinning/canal selection and flagged by a CQ-process inconsistency check, typically near the model top.

    ``rejected_overall_qc``
        **Required Active Bits:** at least one of **BIT9** (512) or **BIT11** (2048).
        The observation was rejected either by AO quality control or by the thinning/canal selection process.

    ``topography_sensitivity``
        **Required Active Bits:** **BIT9** (512) and **BIT18** (262144).
        The observation was rejected by AO quality control and not used due to orography (terrain) sensitivity.

    ``rejected_thinning``
        **Required Active Bits:** **BIT11** (2048).
        The observation was rejected specifically by the thinning/canal selection process.

    ``rejected_background_check``
        **Required Active Bits:** **BIT9** (512).
        **Required Inactive Bits:** **BIT11** (2048).
        The observation was rejected by AO quality control (background check), not via thinning/canal selection.

    .. note::
       Each of these checks exactly the bits named -- it does not
       replicate :func:`flag_reason`'s full priority chain, so a flag
       matching one of these filters is not guaranteed to be the one
       :func:`flag_reason` would label it with if OTHER, unrelated
       bits are also set (the same caveat documented under
       :func:`flag_reason`'s "Matching order" section).

    Active Bits Description Reference
    ---------------------------------

    The following table defines all active bits, their decimal values, and their meaning within the quality control (QC) and assimilation processes:

    .. list-table:: Bitmask Definitions and Values
       :widths: 15 15 70
       :header-rows: 1
       :align: center

       * - Bit Index
         - Decimal Value
         - Description / Rejection Reason
       * - **BIT0**
         - 1
         - Modified or generated by ADE.
       * - **BIT1**
         - 2
         - Element that exceeds a climatological extreme or fails consistency test.
       * - **BIT2**
         - 4
         - Erroneous element.
       * - **BIT3**
         - 8
         - Potentially erroneous element.
       * - **BIT4**
         - 16
         - Dubious element.
       * - **BIT5**
         - 32
         - Interpolated element, generated by DERIVATE.
       * - **BIT6**
         - 64
         - Corrected by DERIVATE sequence or bias correction.
       * - **BIT7**
         - 128
         - Rejected by satellite QC.
       * - **BIT8**
         - 256
         - Element rejected because it is on a blacklist.
       * - **BIT9**
         - 512
         - Element rejected by AO quality control (Background Check or QC-Var).
       * - **BIT10**
         - 1024
         - Generated by AO.
       * - **BIT11**
         - 2048
         - Rejected by a selection process (thinning or canal).
       * - **BIT12**
         - 4096
         - Assimilated (successfully used in analysis).
       * - **BIT13**
         - 8192
         - Comparison against test field, level 1.
       * - **BIT14**
         - 16384
         - Comparison against test field, level 2.
       * - **BIT15**
         - 32768
         - Comparison against test field, level 3.
       * - **BIT16**
         - 65536
         - Rejected by comparison against test field (Background Check).
       * - **BIT17**
         - 131072
         - Rejected by QC-Var.
       * - **BIT18**
         - 262144
         - Not used due to orography.
       * - **BIT19**
         - 524288
         - Not used due to land-sea mask.
       * - **BIT20**
         - 1048576
         - Aircraft position error detected by TrackQC.
       * - **BIT21**
         - 2097152
         - Inconsistency detected by a CQ process.
       * - **BIT22**
         - 4194304
         - Rejected due to transmittance above model top.
       * - **BIT23**
         - 8388608
         - Cloud-affected radiance.
    """ 

    # Define bit masks for flag criteria
    BIT0_ADE = 1            # Modified/generated by ADE
    BIT2_ERR = 4            # Erroneous element
    BIT6_BIASCORR = 64  
    BIT7_REJ = 128  
    BIT8_BLACKLIST = 256
    BIT9_REJ = 512
    BIT11_SELCOR = 2048  
    BIT12_VUE = 4096 
    BIT16_REJBGCK = 65536
    BIT17_QCVAR = 131072
    BIT18_OROG = 262144     # Not used due to orography
    BIT19_LANDSEA = 524288  # Not used due to land-sea mask
    BIT21_CQ = 2097152      # Inconsistency detected by a CQ process
    BIT23_CLOUD = 8388608  # Added BIT23 for sky conditions
    # the rejection bits both bit tables of Pikobs agree on: 7 9 16 17 18 19
    REJECT_BITS = BIT7_REJ | BIT9_REJ | BIT16_REJBGCK | BIT17_QCVAR | BIT18_OROG | BIT19_LANDSEA

    # Generate filtering criteria based on the selected flag
    if flags == "all":
        FLAG = "and flag >= 0"
    elif flags == "assimilee":
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE}"
    elif flags == "assimilee_full":
        # assimilated with its full weight: BIT12 and no rejection bit
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE} and (flag & {REJECT_BITS}) = 0"
    elif flags == "assimilee_rejet":
        # kept by the variational QC with a reduced weight: BIT12 and a rejection bit
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE} and (flag & {REJECT_BITS}) != 0"
    elif flags == "bgckalt":
        FLAG = f"and (flag & {BIT9_REJ}) = 0 and (flag & {BIT11_SELCOR}) = 0 and (flag & {BIT8_BLACKLIST}) = 0"
    elif flags == "bgckalt_qc":
        FLAG = f"and (flag & {BIT9_REJ}) = 0 and (flag & {BIT11_SELCOR}) = 0"
    elif flags == "monitoring":
        FLAG = f"and (flag & {BIT9_REJ}) = 0 and (flag & {BIT7_REJ}) = 0"
    elif flags == "postalt":
        FLAG = f"and (flag & {BIT17_QCVAR}) = 0 and (flag & {BIT9_REJ}) = 0 and (flag & {BIT11_SELCOR}) = 0 and (flag & {BIT8_BLACKLIST}) = 0"
    elif flags == "rejets_qc":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ}"
    elif flags == "rejets_bgck":
        FLAG = f"and (flag & {BIT16_REJBGCK}) = {BIT16_REJBGCK}"
    elif flags == "bias_corr":
        FLAG = f"and (flag & {BIT6_BIASCORR}) = {BIT6_BIASCORR}"
    elif flags == "qc":
        FLAG = f"and (flag & {BIT9_REJ}) = 0"
        
    # --- New Sky Condition Filters ---
    # NOTE: renamed from clear_sky/cloudy_sky/clear_cloudy_sky to the
    # assimilee_-prefixed names below (on request) so the name itself
    # makes clear these three all imply assimilation (BIT12 required).
    # The old, unprefixed names are gone -- update any callers still
    # using them.
    elif flags == "assimilee_clear_sky":
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE} and (flag & {BIT23_CLOUD}) = 0"
    elif flags == "assimilee_cloudy_sky":
        # CORRECTION: Added BIT12 requirement to ensure it was assimilated
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE} and (flag & {BIT23_CLOUD}) = {BIT23_CLOUD}"
    elif flags == "assimilee_clear_cloudy_sky":
        FLAG = f"and (flag & {BIT12_VUE}) = {BIT12_VUE}" # Same logical operation as 'assimilee'

    # --- Granular cloud-related filters, matching flag_reason()'s
    # cloud-related diagnoses one-for-one ---
    # NOTE: "cloudy_assimilated" removed -- it was identical to
    # assimilee_cloudy_sky (both require BIT12+BIT23 active); use that
    # name instead.
    elif flags == "cloudy_rejected_qc":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ} and (flag & {BIT23_CLOUD}) = {BIT23_CLOUD} and (flag & {BIT8_BLACKLIST}) = 0"
    elif flags == "cloudy_blacklisted":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ} and (flag & {BIT23_CLOUD}) = {BIT23_CLOUD} and (flag & {BIT8_BLACKLIST}) = {BIT8_BLACKLIST}"
    elif flags == "cloudy_thinning":
        FLAG = f"and (flag & {BIT11_SELCOR}) = {BIT11_SELCOR} and (flag & {BIT23_CLOUD}) = {BIT23_CLOUD} and (flag & {BIT8_BLACKLIST}) = 0"
    elif flags == "cloudy_thinning_blacklisted":
        FLAG = f"and (flag & {BIT11_SELCOR}) = {BIT11_SELCOR} and (flag & {BIT23_CLOUD}) = {BIT23_CLOUD} and (flag & {BIT8_BLACKLIST}) = {BIT8_BLACKLIST}"

    # --- Remaining filters matching flag_reason()'s non-cloud diagnoses ---
    elif flags == "erroneous_data":
        FLAG = f"and ((flag & {BIT0_ADE}) = {BIT0_ADE} or (flag & {BIT2_ERR}) = {BIT2_ERR} or (flag & {BIT7_REJ}) = {BIT7_REJ})"
    elif flags == "blacklisted":
        FLAG = f"and (flag & {BIT8_BLACKLIST}) = {BIT8_BLACKLIST}"
    elif flags == "background_check_rogue":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ} and (flag & {BIT16_REJBGCK}) = {BIT16_REJBGCK}"
    elif flags == "not_assimilated_daytime":
        FLAG = f"and (flag & {BIT11_SELCOR}) = {BIT11_SELCOR} and (flag & {BIT7_REJ}) = {BIT7_REJ}"
    elif flags == "land_sea_ice_sensitivity":
        FLAG = f"and (flag & {BIT19_LANDSEA}) = {BIT19_LANDSEA}"
    elif flags == "model_top_sensitivity":
        FLAG = f"and (flag & {BIT11_SELCOR}) = {BIT11_SELCOR} and (flag & {BIT21_CQ}) = {BIT21_CQ}"
    elif flags == "rejected_overall_qc":
        FLAG = f"and ((flag & {BIT9_REJ}) = {BIT9_REJ} or (flag & {BIT11_SELCOR}) = {BIT11_SELCOR})"
    elif flags == "topography_sensitivity":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ} and (flag & {BIT18_OROG}) = {BIT18_OROG}"
    elif flags == "rejected_thinning":
        FLAG = f"and (flag & {BIT11_SELCOR}) = {BIT11_SELCOR}"
    elif flags == "rejected_background_check":
        FLAG = f"and (flag & {BIT9_REJ}) = {BIT9_REJ} and (flag & {BIT11_SELCOR}) = 0"

    else:
        raise ValueError(f'Invalid flag option: {flags}')

    return FLAG


# =============================================================================
#  FLAG_REASONS — human-readable diagnosis for a specific flag value
# =============================================================================
#
# Unlike flag_criteria() above (which builds a SQL WHERE-fragment to
# INCLUDE/EXCLUDE rows by a named criterion), FLAG_REASONS answers a
# different question for a single already-fetched flag INTEGER: "in
# plain English, why does this particular bit combination look the way
# it does?" It's a priority-ordered chain of bit-pattern -> reason-text
# rules, evaluated top to bottom; the FIRST rule whose condition holds
# for the given flag value wins.
#
# Condition tuple mini-language
# ------------------------------
# Each dict key is a tuple of tokens describing when that rule applies:
#
#   * a plain int N            -> BIT N must be ACTIVE (set to 1)
#   * a string "nN"             -> BIT N must be INACTIVE (set to 0)
#   * the string "or"           -> splits the tuple into OR-groups
#
# Tokens between 'or' separators form a GROUP; within a group every
# condition must hold (AND). The whole tuple matches if AT LEAST ONE
# group matches (OR). A qualifier like 'n16' appearing only in the
# LAST group of an 'or'-chain applies ONLY to that group, not to the
# whole tuple -- e.g. (0, 'or', 2, 'or', 9, 'n16') means
# (bit0 set) OR (bit2 set) OR (bit9 set AND bit16 unset), not
# "(... ) AND bit16 unset" applied to all three branches.
#
# A tuple with no 'or' at all, like (9, 16, 'n8'), is a single group:
# bit9 AND bit16 must be set, AND bit8 must be unset.
#
# Order matters -- rules are checked top to bottom and the first match
# wins. This dict was supplied pre-ordered (most specific / qualified
# patterns generally first) and is kept in that exact order. One
# consequence worth knowing: the very first rule,
# (0, 'or', 2, 'or', 9, 'n16'), matches ANY flag with bit9 set as long
# as bit16 is unset -- since it's checked first, it will catch most
# bit9-only combinations before later, more specific bit9 rules (like
# (9, 16, 'n8') or (9, 'n11')) are ever reached. That's confirmed
# intentional, not a bug -- documented here so it isn't mistaken for
# one later.
FLAG_REASONS = {
    (0, 'or', 2, 'or', 9, 'n16'): "ERRONEOUS DATA",
    (8,): "CHANNELS ON THE BLACKLIST",
    (9, 16, 'n8'): "BACKGROUND CHECK (O-P INNOVATION ROGUE CHECK)",
    (9, 16): "BACKGROUND CHECK (O-P INNOVATION ROGUE CHECK)",
    (11, 7, 'n8'): "NOT ASSIMILATED DURING THE DAY",
    (11, 7): "NOT ASSIMILATED DURING THE DAY",
    (11, 19, 'n8'): "LAND / SEA-ICE SENSITIVITY",
    (11, 19): "LAND / SEA-ICE SENSITIVITY",
    (11, 21, 'n8'): "SENSITIVITY OVER MODEL TOP",
    (11, 21): "SENSITIVITY OVER MODEL TOP",
    (11, 23, 'n8'): "AFFECTED BY CLOUDS",
    (11, 23): "AFFECTED BY CLOUDS AND BIT 11",
    (9, 'n8', 'or', 11, 'n8'): "REJECTED BY OVERALL QUALITY CONTROL",
    (9, 'or', 11): "REJECTED BY OVERALL QUALITY CONTROL",
    (23, 12): "AFFECTED BY CLOUDS BUT ASSIMILATED",
    (12,): "ASSIMILATED",
    (0, 'n8', 'or', 7, 'n8'): "ERRONEOUS DATA",
    (0, 'or', 7): "ERRONEOUS DATA",
    (0, 'or', 7, 'n8'): "ERRONEOUS DATA",
    (9, 18, 'n8'): "TOPOGRAPHY SENSITIVITY",
    (9, 18): "TOPOGRAPHY SENSITIVITY",
    (9, 23, 'n8'): "AFFECTED BY CLOUDS NOT ASSIMILATED",
    (9, 23): "AFFECTED BY CLOUDS AND BIT 9",
    (23,): "AFFECTED BY CLOUDS",
    (9, 'n8'): "REJECTED BY OVERALL QUALITY CONTROL",
    (9,): "REJECTED BY OVERALL QUALITY CONTROL",
    (11,): "REJECTED BY THINNING",
    (9, 'n11'): "REJECTED BY BACKGROUND CHECK",
    (19,): "LAND / SEA-ICE SENSITIVITY",
}


def _parse_condition_groups(spec):
    """Split one FLAG_REASONS key into OR-groups of (bit, must_be_set) pairs.

    ``spec`` is a tuple like ``(9, 'n8', 'or', 11, 'n8')``. Tokens are
    consumed left to right; ``'or'`` starts a new group, a plain int
    N adds ``(N, True)`` ("bit N must be set") to the current group,
    and a string ``"nN"`` adds ``(N, False)`` ("bit N must be unset").
    """
    groups = []
    current = []
    for tok in spec:
        if tok == 'or':
            groups.append(current)
            current = []
        elif isinstance(tok, int):
            current.append((tok, True))
        elif isinstance(tok, str) and tok.startswith('n') and tok[1:].isdigit():
            current.append((int(tok[1:]), False))
        else:
            raise ValueError(f"Unrecognized token in flag condition: {tok!r}")
    groups.append(current)
    return groups


# Cache the parsed groups once per condition tuple instead of
# re-parsing on every flag_reason() call -- FLAG_REASONS is static for
# the lifetime of the process, so this is safe and avoids redoing the
# same tuple-splitting work for every row when this is registered as a
# SQLite scalar function and called once per row of a large result set.
_PARSED_FLAG_REASONS = [
    (_parse_condition_groups(spec), reason)
    for spec, reason in FLAG_REASONS.items()
]


def flag_reason(flag):
    """
    Human-Readable Diagnosis for a Flag Value
    ==========================================

    Given a single observation's flag bitmask, :func:`flag_reason` returns
    a short, human-readable label explaining why the observation's flag
    looks the way it does. It complements :func:`flag_criteria`: that
    function builds a SQL fragment to INCLUDE/EXCLUDE rows by a named
    criterion; this function explains, for an already-fetched flag value,
    what happened to it in plain English.

    Radiance / Sky-Condition Reasons (BIT23)
    -----------------------------------------

    Several reasons specifically describe how a radiance observation's
    cloud state (**BIT23**, 8388608) interacted with assimilation and
    other quality-control bits. These are the ones to look for first
    when diagnosing satellite radiance coverage:

    ``AFFECTED BY CLOUDS BUT ASSIMILATED``
        BIT23 and BIT12 are both active: a cloud-affected radiance that
        was still assimilated (the normal outcome for all-sky
        assimilation of a cloudy observation).

    ``AFFECTED BY CLOUDS NOT ASSIMILATED``
        BIT9 and BIT23 are active, BIT8 is inactive: a cloud-affected
        radiance rejected by overall quality control (not blacklisted).

    ``AFFECTED BY CLOUDS AND BIT 9``
        BIT9 and BIT23 are active (BIT8 also active): same as above,
        but the observation was additionally blacklisted.

    ``AFFECTED BY CLOUDS``
        Either BIT11+BIT23 active with BIT8 inactive (rejected by
        thinning/canal selection while cloud-affected), or BIT23 active
        alone with none of the more specific combinations above.

    ``AFFECTED BY CLOUDS AND BIT 11``
        BIT11 and BIT23 are both active (BIT8 also active): rejected by
        thinning/canal selection, cloud-affected, and blacklisted.

    Other Reasons
    --------------

    Every remaining reason text that :func:`flag_reason` can return,
    each named the same way :func:`flag_criteria`'s criteria are:

    ``ASSIMILATED``
        BIT12 active alone (no cloud flag on top -- see the radiance
        section above for the cloud-affected-but-assimilated case):
        the observation was successfully used in the analysis.

    ``ERRONEOUS DATA``
        BIT0 (modified/generated by ADE) or BIT2 (erroneous element)
        or BIT7 (rejected by satellite QC) active, or BIT9 active with
        BIT16 inactive.

    ``CHANNELS ON THE BLACKLIST``
        BIT8 active: the observation (or channel) is on the blacklist.

    ``BACKGROUND CHECK (O-P INNOVATION ROGUE CHECK)``
        BIT9 and BIT16 both active: rejected by AO quality control
        AND by comparison against the test field (background check).

    ``REJECTED BY OVERALL QUALITY CONTROL``
        BIT9 (rejected by AO quality control) or BIT11 (rejected by
        thinning/canal selection) active, without a more specific
        combination above taking priority.

    ``REJECTED BY THINNING``
        BIT11 active alone: rejected by the thinning/canal selection
        process, with none of the more specific BIT11 combinations
        above (day/night, land-sea, model-top, clouds) applying.

    ``REJECTED BY BACKGROUND CHECK``
        BIT9 active, BIT11 inactive: rejected by AO quality control,
        not via the thinning/canal selection path.

    ``NOT ASSIMILATED DURING THE DAY``
        BIT11 and BIT7 both active: rejected by thinning/canal
        selection AND by satellite QC.

    ``TOPOGRAPHY SENSITIVITY``
        BIT9 and BIT18 both active: rejected by AO quality control,
        not used due to orography.

    ``LAND / SEA-ICE SENSITIVITY``
        BIT19 active (not used due to the land-sea mask), alone or
        combined with BIT11 (also rejected by thinning/canal
        selection).

    ``SENSITIVITY OVER MODEL TOP``
        BIT11 and BIT21 both active: rejected by thinning/canal
        selection AND flagged by a CQ-process inconsistency check.

    Matching order
    ---------------

    :data:`FLAG_REASONS` is a priority-ordered chain: rules are checked
    top to bottom and the first one whose condition holds for ``flag``
    wins. Some entries are deliberately-kept safety-net duplicates that
    a broader, earlier rule will always reach first for any flag value
    actually seen in practice -- this is intentional (confirmed) and not
    a bug; they document this same reason under an alternate bit
    combination in case an earlier rule's condition is ever narrowed.

    :param flag: the observation's flag bitmask, as an int (or
        anything ``int()``-convertible, e.g. a value fetched from
        SQLite). ``None`` is accepted and returns ``None``.
    :returns: the reason string for the first matching rule, or
        ``None`` if no rule matches (e.g. ``flag`` is 0 or ``None``) --
        callers that want a fallback string should do so explicitly,
        e.g. ``flag_reason(flag) or "UNKNOWN"``.
    """
    if flag is None:
        return None
    flag = int(flag)
    for groups, reason in _PARSED_FLAG_REASONS:
        for group in groups:
            if all((bool(flag & (1 << bit)) == must_be_set)
                   for bit, must_be_set in group):
                return reason
    return None


def register_flag_reason(conn) -> None:
    """Register :func:`flag_reason` as a scalar SQLite function.

    After calling this once on a connection, SQL against that
    connection can call ``flag_reason(flag)`` directly, e.g.::

        register_flag_reason(conn)
        cursor.execute(
            "SELECT flag, flag_reason(flag) AS reason "
            "FROM data WHERE flag_reason(flag) IS NOT NULL"
        )

    :param conn: an open ``sqlite3.Connection``.
    """
    conn.create_function("flag_reason", 1, flag_reason, deterministic=True)
