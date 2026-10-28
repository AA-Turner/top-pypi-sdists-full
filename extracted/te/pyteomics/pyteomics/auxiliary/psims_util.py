from functools import partial


def _needs_psims(name):
    raise ImportError("Loading %s requires the `psims` library. To access it, please install `psims`" % name)


def _needs_newer_psims(name):
    raise ImportError("Loading %s requires a newer version of the `psims` library. "
                      "To access it, please upgrade `psims`" % name)


try:
    from psims.controlled_vocabulary.controlled_vocabulary import (load_psimod, load_xlmod, load_gno, obo_cache, load_unimod, load_psims)
    from psims.controlled_vocabulary.relationship import HasValueTypeRelationship
    _has_psims = True
except ImportError:
    load_psimod = partial(_needs_psims, 'PSIMOD')
    load_xlmod = partial(_needs_psims, 'XLMOD')
    load_gno = partial(_needs_psims, 'GNO')
    load_unimod = partial(_needs_psims, 'UNIMOD')
    load_psims = partial(_needs_psims, 'PSI-MS')
    obo_cache = None
    HasValueTypeRelationship = None
    _has_psims = False

try:
    # Imported on its own rather than with the others, so that a psims
    # predating RESID support loses only RESID. Folding it into the tuple above
    # would turn one missing name into "psims is not installed" and disable
    # every controlled vocabulary.
    from psims.controlled_vocabulary.controlled_vocabulary import load_resid
except ImportError:
    load_resid = partial(_needs_newer_psims if _has_psims else _needs_psims, 'RESID')
