"""Display one unassigned central GGUF repository with its quant selector."""
import os


def grouped_inventory(keys, central, protected=()):
    protected = set(protected)
    groups = {}
    for key in sorted(keys):
        row = central.get(key) or {}
        path, directory = row.get('path') or '', row.get('dir') or ''
        weights = row.get('weights') or []
        files = {w.get('file') for w in weights if isinstance(w, dict) and not w.get('mmproj')}
        # Require the wrapper's file list to prove these IDs share a quant set.
        group = (directory, tuple(sorted(f for f in files if f))) if (
            key not in protected and directory and path.lower().endswith('.gguf')
            and os.path.basename(path) in files and len(files) > 1) else ('key', key)
        groups.setdefault(group, []).append(key)
    return [members[0] for members in groups.values()]
