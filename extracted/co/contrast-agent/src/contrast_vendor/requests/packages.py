import sys

from .compat import chardet

# This code exists for backwards compatibility reasons.
# I don't like it either. Just look the other way. :)

for package in ("urllib3", "idna"):
### Contrast Modification Start ###
    contrast_package = f"contrast_vendor.{package}"
    locals()[package] = __import__(contrast_package, fromlist=[package])
    # This traversal is apparently necessary such that the identities are
    # preserved (requests.packages.urllib3.* is urllib3.*)
    for mod in list(sys.modules):
        if mod == contrast_package or mod.startswith(f"{contrast_package}."):
            suffix = mod[len(contrast_package):]
            sys.modules[f"contrast_vendor.requests.packages.{package}{suffix}"] = sys.modules[mod]
### Contrast Modification End ###

if chardet is not None:
    target = chardet.__name__
    for mod in list(sys.modules):
        if mod == target or mod.startswith(f"{target}."):
            imported_mod = sys.modules[mod]
            sys.modules[f"contrast_vendor.requests.packages.{mod}"] = imported_mod
            mod = mod.replace(target, "chardet")
            sys.modules[f"contrast_vendor.requests.packages.{mod}"] = imported_mod
