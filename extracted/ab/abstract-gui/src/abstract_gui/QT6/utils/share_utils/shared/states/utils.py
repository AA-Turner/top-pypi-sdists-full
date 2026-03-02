# --- helpers ---------------------------------------------------------------
def make_string(x):
    try:
        x = json.loads(x)
    except:
        pass
    if isinstance(x,tuple):
        nulist=[]
        for each in x:

            if isinstance(each, (list, tuple, set)):
               nulist+=list(each)
                   
            else:
                nulist.append(each)
        x = nulist
    if isinstance(x, (list, tuple, set)):
        return ",".join(str(i) for i in x)
        
    return "" if x is None else str(x)

def norm_csv(val, *, lower=True, split_chars=(",","|")):
    """Normalize a CSV/pipe string or iterable to a sorted tuple for stable compare."""
    if not val or val is False:
        return tuple()
    if isinstance(val, (list, tuple, set)):
        items = [str(v) for v in val]
    else:
        s = str(val)
        for ch in split_chars[1:]:
            s = s.replace(ch, split_chars[0])
        items = [p.strip() for p in s.split(split_chars[0]) if p.strip()]
    if lower:
        items = [i.lower() for i in items]
    return tuple(sorted(items))

def filters_subset(state: dict) -> dict:
    """Just the filter fields (the ones you care about for auto-unlink)."""
    return {
        "allowed_exts":    norm_csv(state.get("allowed_exts", "")),
        "unallowed_exts":  norm_csv(state.get("unallowed_exts", "")),
        
        "allowed_types":   norm_csv(state.get("allowed_types", ""), lower=False),
        "exclude_types":   norm_csv(state.get("exclude_types", ""), lower=False),
    
        "allowed_dirs":    norm_csv(state.get("allowed_dirs", ""),  lower=False),
        "exclude_dirs":    norm_csv(state.get("exclude_dirs", ""),  lower=False),

        "allowed_dirs":    norm_csv(state.get("allowed_dirs", ""),  lower=False),
        "exclude_patterns":norm_csv(state.get("exclude_patterns",""),lower=False),
    }

