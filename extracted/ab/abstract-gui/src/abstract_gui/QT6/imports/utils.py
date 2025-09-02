from .imports import *
def read_from_dot_file(path):
    graphs, = pydot.graph_from_dot_file(path)
    return graphs

def sh_quote(s: str) -> str:
    return "'" + (s or "").replace("'", "'\\''") + "'"

def strip_ansi(text: str) -> str:
    return ANSI_RE.sub('', text or "")

def get_trailing_number(file_path):
    return_js = {"chars":'',"file_path":file_path}
    for i in range(1,len(file_path)+1):
        char = file_path[-i]
        if is_number(char) or char == ':':
            return_js["chars"] = str(char)+ str(chars)
        else:
            file_path = file_path[:-i]
    return return_js

def resolve_alt_ext(path: str, project_root: str) -> str:
    """
    If 'path' doesn't exist, try sibling files with alternate extensions
    (ts<->tsx, js<->jsx). Also tries case-insensitive match and glob
    for same basename with any extension in the same folder.
    Returns the best existing path, or the original if none found.
    """
    if not path:
        return path
    if os.path.exists(path):
        return path

    folder, base = os.path.dirname(path), os.path.basename(path)
    stem, ext = os.path.splitext(base)

    # 1) explicit swap candidates
    for alt in EXT_SWAP.get(ext, []):
        cand = os.path.join(folder, stem + alt)
        if os.path.exists(cand):
            return cand

    # 2) case-insensitive lookup (useful on case-sensitive FS when log had case mismatch)
    try:
        for name in os.listdir(folder or "."):
            if name.lower() == (stem + ext).lower():
                cand = os.path.join(folder, name)
                if os.path.exists(cand):
                    return cand
    except Exception:
        pass

    # 3) any sibling with same stem (e.g., foo.*)
    try:
        for name in os.listdir(folder or "."):
            nstem, next_ = os.path.splitext(name)
            if nstem == stem and os.path.isfile(os.path.join(folder, name)):
                # prefer our known alternates order
                if next_ in sum(EXT_SWAP.values(), []):
                    return os.path.join(folder, name)
        # fallback: first file with same stem
        for name in os.listdir(folder or "."):
            nstem, _ = os.path.splitext(name)
            if nstem == stem:
                return os.path.join(folder, name)
    except Exception:
        pass

    return path



#split funcs
def split_sections(raw: str):
    """Return (tsc_text, build_text) from the full captured output."""
    raw = strip_ansi(raw)
    tsc = ""
    build = ""
    try:
        tsc = raw.split("__TSC_BEGIN__", 1)[1].split("__TSC_END__", 1)[0]
    except Exception:
        pass
    try:
        build = raw.split("__BUILD_BEGIN__", 1)[1].split("__BUILD_END__", 1)[0]
    except Exception:
        pass
    return tsc.strip(), build.strip()

def split_by_severity(text: str):
    """Return (errors_text, warnings_text) based on simple, robust heuristics."""
    errs, warns = [], []
    for ln in (text or "").splitlines():
        # webpack/CRA often prints 'WARNING in ...' / 'ERROR in ...'
        if ln.startswith('WARNING in '):
            warns.append(ln)
            continue
        if ln.startswith('ERROR in '):
            errs.append(ln)
            continue

        lnl = ln.lower()
        if 'error' in lnl:
            errs.append(ln)
        elif 'warning' in lnl:
            warns.append(ln)
    return "\n".join(errs), "\n".join(warns)

#entries
def get_error_entries(log_text: str, project_path: str):
    """Find file(line,col) triplets."""
    entries = []
    if not log_text:
        return entries
    for match in FILE_REGEX.finditer(log_text):
        rel, line, col = match.groups()
        full = rel if os.path.isabs(rel) else os.path.normpath(os.path.join(project_path, rel))
        try:
            entries.append((full, int(line), int(col)))
        except Exception:
            continue
    return entries

def get_file_error_entries(log_text: str, project_path: str):
    entries = []
    if not log_text:
        return entries
    for m in FILE_FILE_REGEX.finditer(log_text):
        rel = m.group('file')
        line = m.group('l1') or m.group('l2')
        col  = m.group('c1') or m.group('c2')
        full = rel if os.path.isabs(rel) else os.path.normpath(os.path.join(project_path, rel))
        try:
            entries.append((full, int(line), int(col)))
        except Exception:
            continue
    return entries

def get_entries_for(text: str, project_path: str):
    """Use file(line,col) extractor on a subset."""
    return get_error_entries(text, project_path)

#imports
def grep_use_imports(project_path: str):
    """Fallback: grep for suspect 'use' imports in src. Returns list[(path,line,1)]."""
    results = []
    try:
        proc = subprocess.run(
            ["grep", "-RnE", GREP_REGEX, "src"],
            cwd=project_path,
            capture_output=True, text=True
        )
        for ln in proc.stdout.splitlines():
            try:
                file, lineno, _ = ln.split(':', 2)
                results.append((os.path.join(project_path, file), int(lineno), 1))
            except Exception:
                continue
    except Exception:
        pass
    return results

#cmd utils
def run_ssh_cmd(user_at_host: str, cmd: str, path: str) -> str:
    """Run on remote via SSH and return stdout+stderr."""
    try:
        full = f"ssh {user_at_host} 'cd {path} && bash -lc {sh_quote(cmd)}'"
        proc = subprocess.run(full, shell=True, capture_output=True, text=True)
        return (proc.stdout or "") + (proc.stderr or "")
    except Exception as e:
        return f"❌ run_ssh_cmd error: {e}\n"


def run_local_cmd(cmd: str, path: str) -> str:
    """Run locally in cwd=path and return stdout+stderr."""
    try:
        proc = subprocess.run(["bash", "-lc", cmd], cwd=path, capture_output=True, text=True)
        return (proc.stdout or "") + (proc.stderr or "")
    except Exception as e:
        return f"❌ run_local_cmd error: {e}\n"





