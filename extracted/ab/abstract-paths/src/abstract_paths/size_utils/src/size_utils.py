from .cmd_utils import *
from .dir_utils import *
SIZE_DIFFS = {
    "K": {"K": 1, "M": 1/1000, "G": 1/1000**2, "T": 1/1000**3},
    "M": {"K": 1000, "M": 1, "G": 1/1000, "T": 1/1000**2},
    "G": {"K": 1000**2, "M": 1000, "G": 1, "T": 1/1000},
    "T": {"K": 1000**3, "M": 1000**2, "G": 1000, "T": 1}
}
def break_size_lines(size_output):
    size_lines = size_output.replace('\t',' ').split('\n')
    return [size_line for size_line in size_lines if size_line]
def convert_size(value: float, from_unit: str, to_unit: str, binary: bool = False) -> float:
    """
    Convert file size between K, M, G, T.
    :param value: numeric size
    :param from_unit: 'K', 'M', 'G', 'T'
    :param to_unit: 'K', 'M', 'G', 'T'
    :param binary: if True, use 1024 instead of 1000
    """
    step = 1024 if binary else 1000
    units = ["K", "M", "G", "T"]
    if from_unit not in units or to_unit not in units:
        raise ValueError(f"Units must be one of {units}")
    power = units.index(from_unit) - units.index(to_unit)
    return value * (step ** power)
def get_file_sizes(directory, local=True, host=None, password="1") -> dict:
    """
    Return dict {filepath: size_in_bytes}, safe against weird filenames.
    """
    cmd = f"find {directory} -type f -print0 | xargs -0 du -b 2>/dev/null"
    if local:
        output = run_local_sudo(cmd, workdir=directory, password=password)
    else:
        output = run_remote_sudo(user_at_host=host, cmd=cmd, workdir=directory, password=password)

    file_sizes = {}
    for line in output.splitlines():
        if not line.strip() or not line[0].isdigit():
            continue
        try:
            size, path = line.split("\t", 1)
            file_sizes[path] = int(size)
        except ValueError:
            continue
    return file_sizes
def parse_size(size_str: str) -> int:
    """Convert human-readable du output into bytes."""
    size_str = size_str.strip().upper()
    multipliers = {"K": 1000, "M": 1000**2, "G": 1000**3, "T": 1000**4}
    if not size_str or not size_str[0].isdigit():
        # ignore lines that aren't proper size tokens (like 'DU')
        return 0
    if size_str[-1].isdigit():  # plain number, assume bytes
        return int(size_str)
    unit = size_str[-1]
    try:
        num = float(size_str[:-1])
    except ValueError:
        return 0
    return int(num * multipliers.get(unit, 1))

def get_size_cmd(directory):
    return f"du -h --max-depth=1  {directory}"
def run_size_cmd(directory,local=True,host=None,outfile=False,password=None):
    if local:
        is_exists = os.path.exists(directory)
        is_dir = os.path.isdir(directory)
    else:
        is_exists = is_dir = get_is_ssh_dir(directory,host=host)
    if is_exists and local and is_dir:
        outfile = dir_mgr.get_filepath(directory,local=local,outfile=outfile)
        cmd = get_size_cmd(directory)
        resp = run_local_sudo(cmd=cmd, workdir=directory, outfile=outfile,shell=True, text=True, capture_output=True,password=password)
        return resp 
    if not local and is_exists and is_dir:
        outfile = dir_mgr.get_filepath(directory,local=local,outfile=outfile)
        cmd = get_size_cmd(directory)
        resp = run_remote_sudo(user_at_host=host, cmd=cmd, workdir=directory, outfile=outfile,shell=True, text=True, capture_output=True,password=password)
        return resp     
def get_sizes(src_directory, dst_directory, local=True, host=None):
    src_directory,src_local,src_host,src_outfile,src_password = get_directory_vars(src_directory,local=local,host=host)
    dst_directory,dst_local,dst_host,dst_outfile,dst_password = get_directory_vars(dst_directory,local=local,host=host)

    src_size_output = run_size_cmd(src_directory, local=src_local, host=src_host,password=src_password)
    if src_directory and dst_directory:
        dst_size_output = run_size_cmd(directory=dst_directory, local=dst_local, host=dst_host,password=dst_password)

        srcs = break_size_lines(src_size_output)
        dsts = break_size_lines(dst_size_output)

        sizes = {"src": {}, "dst": {}, "needs": {}}

        for src in srcs:
            size, name = src.split()[0], src.split('/')[-1]
            sizes["src"][name] = parse_size(size)

        for dst in dsts:
            size, name = dst.split()[0], dst.split('/')[-1]
            sizes["dst"][name] = parse_size(size)

        # Compare src vs dst
        for src_dir, src_size in sizes["src"].items():
            dst_size = sizes["dst"].get(src_dir)
            if dst_size is None or dst_size != src_size:
                diff_entry = {"src": src_size, "dst": dst_size}
                diff_entry["files"] = {
                    "src": get_file_sizes(os.path.join(src_directory, src_dir), local=src_local, host=src_host),
                    "dst": get_file_sizes(os.path.join(dst_directory, src_dir), local=dst_local, host=dst_host),
                }
                sizes["needs"][src_dir] = diff_entry

        return sizes
    return False
