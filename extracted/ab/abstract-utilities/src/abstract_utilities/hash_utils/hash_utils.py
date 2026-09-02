from .imports import *
def full_hash(path):
    """Only called when quick hashes match"""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
def quick_hash(path, bytes_to_read=16384):
    """Fast fingerprint to avoid full hash on obvious non-dups"""
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read(bytes_to_read)).hexdigest()
def generate_data_hash(insertName,value):
    # Combine values to create a unique reference
    data_string = f"{insertName}_{value}"
    return hashlib.md5(data_string.encode()).hexdigest()
def get_size_to_paths(directory,exts):
    exts=make_list(exts or [])
    size_to_paths = defaultdict(list)
    dirs,file_paths = get_files_and_dirs(directory,allowed_exts=exts)
    for file_path in file_paths:
        if os.path.isfile(file_path):
            size_to_paths[os.path.getsize(file_path)].append(file_path)
    return size_to_paths
def dedupe_media(directory,exts):
    size_to_paths = get_size_to_paths(directory,exts)
    hash_to_paths = defaultdict(list)
    for size_group in size_to_paths.values():
        if len(size_group) < 2: continue
        quick_to_paths = defaultdict(list)
        for p in size_group:
            if os.path.isfile(p):
                quick_to_paths[quick_hash(p)].append(p)
        for quick_matches in quick_to_paths.values():
            if len(quick_matches) < 2: continue
            full_h = full_hash(quick_matches[0])
            hash_to_paths[full_h].extend(quick_matches)
    return hash_to_paths
def dedupe_hash_to_paths(directory,exts):
    hash_to_paths_js = {}
    hash_to_paths = dedupe_media(directory,exts)
    hash_to_paths_js["hash_to_paths"] = hash_to_paths
    hash_to_paths_js["dedups"] = {h: paths for h, paths in hash_to_paths.items() if len(paths) >= 2}
    hash_to_paths_js["singles"] = {h: paths for h, paths in hash_to_paths.items() if len(paths) < 2}
    return hash_to_paths_js
def dedupe_and_save_hash_to_paths(directory,exts,basename=None):
    basename = basename or 'hash_to_paths.json'
    hash_to_paths_js = dedupe_hash_to_paths(directory,exts)
    file_path = os.path.join(directory,basename)
    safe_dump_to_json(data=hash_to_paths_js,file_path=file_path)
    return file_path
