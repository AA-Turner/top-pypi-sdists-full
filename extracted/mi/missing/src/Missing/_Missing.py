from zope.deferredimport import deprecated  # pragma: no cover


deprecated(
    "The functionality of Missing._Missing has moved to"
    " Missing.__init__. Please import from there."
    " This backward compatibility shim will be removed in Missing version 6.",
    MV="Missing.MV",
    Missing="Missing.Missing",
    V="Missing.V",
    Value="Missing.Value",
    notMissing="Missing.notMissing",
)  # pragma: no cover
