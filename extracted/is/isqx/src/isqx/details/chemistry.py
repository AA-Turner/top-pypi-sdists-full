from .. import chemistry
from . import SELF, Details, Equation

PHYSICAL_CHEMISTRY: Details = {
    chemistry.KA: Equation(
        r"K_a = \frac{a_{\mathrm{H}^+} a_{\mathrm{A}^-}}{a_{\mathrm{HA}}}",
        {
            "K_a": SELF,
            r"a_{\mathrm{H}^+}": chemistry.ACTIVITY_HPLUS,
            r"a_{\mathrm{A}^-}": chemistry.ACTIVITY_AMINUS,
            r"a_{\mathrm{HA}}": chemistry.ACTIVITY_HA,
        },
        assumptions={"aqueous solution"},
    ),
}
