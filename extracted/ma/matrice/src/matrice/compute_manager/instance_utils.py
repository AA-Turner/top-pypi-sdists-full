"""Module providing instance utilities functionality."""

import os
import socket
import urllib.request
import subprocess
import logging
import base64
from datetime import datetime
import psutil
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes,
)
from cryptography.hazmat.backends import default_backend
from matrice.utils import log_errors


@log_errors(default_return=(None, None), raise_exception=False, log_error=False)
def get_instance_info():
    """
    Get instance provider and ID information.

    Returns:
        tuple: (service_provider, instance_id) strings
    """
    service_provider = os.environ.get("SERVICE_PROVIDER") or "LOCAL"
    instance_id = os.environ.get("INSTANCE_ID") or ""
    try:
        gcp_check = subprocess.run(
            "curl -s -m 1 -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/id'",
            shell=True,
            capture_output=True,
            check=True,
        )
        if gcp_check.returncode == 0:
            service_provider = "GCP"
            instance_id = gcp_check.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass
    try:
        azure_check = subprocess.run(
            "curl -s -m 1 -H Metadata:true 'http://169.254.169.254/metadata/instance?api-version=2020-09-01'",
            shell=True,
            capture_output=True,
            check=True,
        )
        if azure_check.returncode == 0:
            service_provider = "AZURE"
            azure_id = subprocess.run(
                "curl -s -H Metadata:true 'http://169.254.169.254/metadata/instance/compute/vmId?api-version=2017-08-01&format=text'",
                shell=True,
                capture_output=True,
                check=True,
            )
            instance_id = azure_id.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass
    try:
        oci_check = subprocess.run(
            "curl -s -m 1 -H 'Authorization: Bearer OracleCloud' 'http://169.254.169.254/opc/v1/instance/'",
            shell=True,
            capture_output=True,
            check=True,
        )
        if oci_check.returncode == 0:
            service_provider = "OCI"
            oci_id = subprocess.run(
                "curl -s http://169.254.169.254/opc/v1/instance/id",
                shell=True,
                capture_output=True,
                check=True,
            )
            instance_id = oci_id.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass
    try:
        aws_check = subprocess.run(
            "curl -s -m 1 http://169.254.169.254/latest/meta-data/",
            shell=True,
            capture_output=True,
            check=True,
        )
        if aws_check.returncode == 0:
            service_provider = "AWS"
            aws_id = subprocess.run(
                "curl -s http://169.254.169.254/latest/meta-data/instance-id",
                shell=True,
                capture_output=True,
                check=True,
            )
            instance_id = aws_id.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass
    return str(service_provider), str(instance_id)


@log_errors(default_return=0, raise_exception=False, log_error=False)
def calculate_time_difference(start_time_str, finish_time_str):
    """
    Calculate time difference between start and finish times.

    Args:
        start_time_str (str): Start time string
        finish_time_str (str): Finish time string

    Returns:
        int: Time difference in seconds
    """
    if os.environ["SERVICE_PROVIDER"] in [
        "AWS",
        "OCI",
        "LAMBDA",
    ]:
        start_time = datetime.fromisoformat(start_time_str.split(".")[0] + "+00:00")
        finish_time = datetime.fromisoformat(finish_time_str.split(".")[0] + "+00:00")
    else:
        start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
        finish_time = datetime.fromisoformat(finish_time_str.replace("Z", "+00:00"))
    return int((finish_time - start_time).total_seconds())


@log_errors(default_return=False, raise_exception=False, log_error=False)
def has_gpu() -> bool:
    """
    Check if the system has a GPU.

    Returns:
        bool: True if GPU is present, False otherwise
    """
    subprocess.run("nvidia-smi", check=True)
    return True


@log_errors(default_return=0, raise_exception=False)
def get_gpu_memory_usage():
    """
    Get GPU memory usage percentage.

    Returns:
        float: Memory usage between 0 and 1
    """
    command = "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,nounits,noheader"
    output = subprocess.check_output(command.split()).decode("ascii").strip().split("\n")
    memory_percentages = []
    for line in output:
        used, total = map(int, line.split(","))
        usage_percentage = used / total
        memory_percentages.append(usage_percentage)
    return min(memory_percentages)


@log_errors(default_return=0, raise_exception=False)
def get_cpu_memory_usage():
    """
    Get CPU memory usage.

    Returns:
        float: Memory usage between 0 and 1
    """
    memory = psutil.virtual_memory()
    return memory.percent / 100


@log_errors(default_return=0, raise_exception=False)
def get_mem_usage():
    """
    Get memory usage for either GPU or CPU.

    Returns:
        float: Memory usage between 0 and 1
    """
    if has_gpu():
        try:
            mem_usage = get_gpu_memory_usage()
        except Exception as err:
            logging.error(
                "Error getting GPU memory usage: %s",
                err,
            )
            mem_usage = get_cpu_memory_usage()
    else:
        mem_usage = get_cpu_memory_usage()
    if mem_usage is None:
        mem_usage = 0
    return mem_usage


@log_errors(default_return=[], raise_exception=False)
def get_gpu_info():
    """
    Get GPU information.

    Returns:
        list: GPU information strings
    """
    with subprocess.Popen(
        [
            "nvidia-smi",
            "--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu",
            "--format=csv,noheader,nounits",
        ],
        stdout=subprocess.PIPE,
    ) as proc:
        stdout, _ = proc.communicate()
        output = stdout.decode("UTF-8")
        return output.split("\n")[:-1]


@log_errors(default_return="", raise_exception=False)
def get_instance_id() -> str:
    """
    Get instance ID.

    Returns:
        str: Instance ID or empty string
    """
    return os.environ["INSTANCE_ID"]


@log_errors(default_return=False, raise_exception=False, log_error=False)
def is_docker_running():
    """
    Check if Docker is running.

    Returns:
        bool: True if Docker containers are running
    """
    command = "docker ps"
    docker_images = (
        subprocess.check_output(command.split()).decode("ascii").split("\n")[:-1][1:]
    )
    return bool(docker_images)


@log_errors(default_return=None, raise_exception=False)
def prune_docker_images():
    """Prune Docker images."""
    subprocess.run(
        [
            "docker",
            "image",
            "prune",
            "-a",
            "-f",
        ],
        check=True,
    )
    logging.info("Docker images pruned successfully.")


@log_errors(default_return=0.0, raise_exception=False)
def _normalize_disk_usage_to_gb(disk_space):
    """
    Normalize disk usage to GB.

    Args:
        disk_space (str): Disk space with unit

    Returns:
        float: Disk space in GB
    """
    if disk_space.endswith("G"):
        disk_space = float(disk_space[:-1])
    elif disk_space.endswith("T"):
        disk_space = float(disk_space[:-1]) * 1024
    elif disk_space.endswith("M"):
        disk_space = float(disk_space[:-1]) / 1024
    elif disk_space.endswith("K"):
        disk_space = float(disk_space[:-1]) / (1024 * 1024)
    else:
        disk_space = float(disk_space)
    logging.debug(
        "Normalized disk space value to %f GB",
        disk_space,
    )
    return disk_space


@log_errors(default_return=None, raise_exception=False)
def _parse_disk_usage_info(line):
    """
    Parse disk usage information.

    Args:
        line (str): Disk usage line from df command

    Returns:
        dict: Parsed disk usage information
    """
    parts = line.split()
    parsed_info = {
        "filesystem": parts[0],
        "size": float(_normalize_disk_usage_to_gb(parts[1])),
        "used": float(_normalize_disk_usage_to_gb(parts[2])),
        "available": float(_normalize_disk_usage_to_gb(parts[3])),
        "use_percentage": float(parts[4].rstrip("%")),
        "mounted_on": parts[5],
    }
    logging.debug(
        "Successfully parsed disk usage info: %s",
        parsed_info,
    )
    return parsed_info


@log_errors(default_return=None, raise_exception=False)
def get_disk_space_usage():
    """
    Get disk space usage for all filesystems.

    Returns:
        list: List of disk usage information dictionaries
    """
    logging.info("Getting disk space usage information")
    result = subprocess.run(
        ["df", "-h"],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().split("\n")[1:]
    disk_usage = []
    for line in lines:
        disk = _parse_disk_usage_info(line)
        if disk:
            disk_usage.append(disk)
    logging.info(
        "Found disk usage info for %d filesystems",
        len(disk_usage),
    )
    return disk_usage


@log_errors(default_return=None, raise_exception=False)
def get_max_file_system():
    """
    Get filesystem with maximum available space.

    Returns:
        str: Path to filesystem with most space or None
    """
    logging.info("Finding filesystem with maximum available space")
    disk_usage = get_disk_space_usage()
    if not disk_usage:
        logging.warning("No disk usage information available")
        return None
    filtered_disks = [
        disk
        for disk in disk_usage
        if disk["mounted_on"] != "/boot/efi"
        and "overlay" not in disk["filesystem"]
        and disk["available"] > 0
    ]
    if not filtered_disks:
        logging.warning("No suitable filesystems found after filtering")
        max_available_filesystem = ""
    else:
        max_disk = max(
            filtered_disks,
            key=lambda x: x["available"],
        )
        max_available_filesystem = max_disk["mounted_on"]
        logging.info(
            "Found filesystem with maximum space: %s (%f GB available)",
            max_available_filesystem,
            max_disk["available"],
        )
    if max_available_filesystem in ["/", ""]:
        home_dir = os.path.expanduser("~")
        if not os.environ.get("WORKSPACE_DIR"):
            logging.error("WORKSPACE_DIR environment variable not set")
            return None
        workspace_dir = os.path.join(
            home_dir,
            os.environ["WORKSPACE_DIR"],
        )
        os.makedirs(workspace_dir, exist_ok=True)
        logging.info(
            "Created workspace directory at: %s",
            workspace_dir,
        )
        return workspace_dir
    return max_available_filesystem


@log_errors(default_return=None, raise_exception=False)
def get_docker_disk_space_usage():
    """
    Get disk space usage for Docker storage.

    Returns:
        dict: Docker disk usage information
    """
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        text=True,
        check=True,
    )
    docker_info = result.stdout
    docker_root_dir = None
    for line in docker_info.split("\n"):
        if line.strip().startswith("Docker Root Dir"):
            docker_root_dir = line.split(":")[1].strip()
            break
    if docker_root_dir is None:
        logging.error("Unable to find Docker root directory")
        raise ValueError("Unable to find Docker root directory")
    logging.debug(
        "Found Docker root directory: %s",
        docker_root_dir,
    )
    result = subprocess.run(
        ["df", "-h", docker_root_dir],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().split("\n")[1:]
    if not lines:
        logging.error("No disk usage information found for Docker root directory")
        raise ValueError("No disk usage information found for Docker root directory")
    docker_disk_usage = _parse_disk_usage_info(lines[0])
    if docker_disk_usage is None:
        logging.error("Failed to parse Docker disk usage information")
        raise ValueError("Failed to parse Docker disk usage information")
    logging.info(
        "Successfully retrieved Docker disk usage: %s",
        docker_disk_usage,
    )
    return docker_disk_usage


@log_errors(raise_exception=False)
def cleanup_docker_storage():
    """Clean up Docker storage if space is low."""
    docker_disk_usage = get_docker_disk_space_usage()
    if docker_disk_usage is None:
        logging.error("Failed to get Docker disk space usage, skipping cleanup")
        return
    if docker_disk_usage["use_percentage"] >= 90 or docker_disk_usage["available"] <= 30:
        logging.info(
            "Pruning Docker images. Disk space is low: %s",
            docker_disk_usage,
        )
        prune_docker_images()


@log_errors(default_return=0, raise_exception=False)
def get_required_gpu_memory(action_details):
    """
    Get required GPU memory from action details.

    Args:
        action_details (dict): Action details

    Returns:
        int: Required GPU memory
    """
    try:
        return action_details["actionDetails"]["expectedResources"]["gpuMemory"]
    except KeyError:
        return 0


@log_errors(default_return=True, raise_exception=False)
def is_allowed_gpu_device(gpu_index):
    """
    Check if GPU device is allowed.

    Args:
        gpu_index (int): GPU device index

    Returns:
        bool: True if GPU is allowed
    """
    gpus = os.environ.get("GPUS")
    if not gpus:
        return True
    allowed_gpus = [int(x) for x in gpus.split(",") if x.strip()]
    return int(gpu_index) in allowed_gpus


@log_errors(raise_exception=True)
def get_gpu_with_sufficient_memory_for_action(
    action_details,
):
    """
    Get GPUs with sufficient memory for action.

    Args:
        action_details (dict): Action details

    Returns:
        list: List of GPU indices

    Raises:
        ValueError: If insufficient GPU memory
    """
    required_gpu_memory = get_required_gpu_memory(action_details)
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = subprocess.check_output(command.split()).decode("ascii").split("\n")
    if len(memory_free_info) < 2:
        raise ValueError("No GPU information available from nvidia-smi")
    memory_free_values = [int(x.split()[0]) for x in memory_free_info[1:-1]]
    if required_gpu_memory < 80000:
        try:
            return get_single_gpu_with_sufficient_memory_for_action(action_details)
        except ValueError:
            pass
    selected_gpus = []
    total_memory = 0
    for i, mem in enumerate(memory_free_values):
        if not is_allowed_gpu_device(i):
            continue
        if total_memory >= required_gpu_memory:
            break
        selected_gpus.append(i)
        total_memory += mem
    if total_memory >= required_gpu_memory:
        return selected_gpus
    raise ValueError(
        f"Insufficient GPU memory available. Required: {required_gpu_memory}, Available: {total_memory}"
    )


@log_errors(raise_exception=True)
def get_single_gpu_with_sufficient_memory_for_action(
    action_details,
):
    """
    Get single GPU with sufficient memory.

    Args:
        action_details (dict): Action details

    Returns:
        list: List with single GPU index

    Raises:
        ValueError: If no GPU has sufficient memory
    """
    required_gpu_memory = get_required_gpu_memory(action_details)
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = subprocess.check_output(command.split()).decode("ascii").split("\n")
    if len(memory_free_info) < 2:
        raise ValueError("No GPU information available from nvidia-smi")
    memory_free_values = [int(x.split()[0]) for x in memory_free_info[1:-1]]
    best_fit_gpu = None
    best_fit_memory = float("inf")
    for i, mem in enumerate(memory_free_values):
        if not is_allowed_gpu_device(i):
            continue
        if mem >= required_gpu_memory and mem < best_fit_memory:
            best_fit_gpu = i
            best_fit_memory = mem
    if best_fit_gpu is not None:
        return [best_fit_gpu]
    raise ValueError(
        f"No single GPU with sufficient memory ({required_gpu_memory}MB) available"
    )


@log_errors(default_return=(None, None), raise_exception=False)
def get_decrypted_access_key_pair(
    enc_access_key,
    enc_secret_key,
    encryption_key="",
):
    """
    Get decrypted access key pair.

    Args:
        enc_access_key (str): Encrypted access key
        enc_secret_key (str): Encrypted secret key
        encryption_key (str): Encryption key

    Returns:
        tuple: (access_key, secret_key) strings
    """
    encryption_key = encryption_key or os.environ.get("MATRICE_ENCRYPTION_KEY")
    if not encryption_key:
        logging.warning("Encryption key is not set, Will assume that the keys are not encrypted")
        return enc_access_key, enc_secret_key
    encrypted_access_key = base64.b64decode(enc_access_key)
    encrypted_secret_key = base64.b64decode(enc_secret_key)
    nonce = encrypted_access_key[:12]
    tag = encrypted_access_key[-16:]
    ciphertext = encrypted_access_key[12:-16]
    cipher = Cipher(
        algorithms.AES(encryption_key.encode()),
        modes.GCM(nonce, tag),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    decrypted_access_key = decryptor.update(ciphertext) + decryptor.finalize()
    nonce = encrypted_secret_key[:12]
    tag = encrypted_secret_key[-16:]
    ciphertext = encrypted_secret_key[12:-16]
    cipher = Cipher(
        algorithms.AES(encryption_key.encode()),
        modes.GCM(nonce, tag),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    decrypted_secret_key = decryptor.update(ciphertext) + decryptor.finalize()
    access_key = decrypted_access_key.decode("utf-8", errors="replace")
    secret_key = decrypted_secret_key.decode("utf-8", errors="replace")
    return access_key, secret_key

@log_errors(default_return=(None, None), raise_exception=False)
def get_encrypted_access_key_pair(
    access_key,
    secret_key,
    encryption_key="",
):
    """
    Get encrypted access key pair.

    Args:
        access_key (str):  access key
        secret_key (str):  secret key
        encryption_key (str): Encryption key

    Returns:
        tuple: (encrypted_access_key, encrypted_secret_key) strings
    """
    encryption_key = encryption_key or os.environ.get("MATRICE_ENCRYPTION_KEY")
    if not encryption_key:
        logging.warning("Encryption key is not set, returning unencrypted keys")
        return access_key, secret_key
    
    # Convert encryption key to bytes
    key = encryption_key.encode()
    
    # Encrypt access key
    nonce = os.urandom(12)
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_access_key = encryptor.update(access_key.encode()) + encryptor.finalize()
    encrypted_access_key_with_nonce = nonce + encrypted_access_key + encryptor.tag
    
    # Encrypt secret key
    nonce = os.urandom(12)
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_secret_key = encryptor.update(secret_key.encode()) + encryptor.finalize()
    encrypted_secret_key_with_nonce = nonce + encrypted_secret_key + encryptor.tag
    
    # Encode to base64 for storage
    encoded_access_key = base64.b64encode(encrypted_access_key_with_nonce).decode()
    encoded_secret_key = base64.b64encode(encrypted_secret_key_with_nonce).decode()
    
    return encoded_access_key, encoded_secret_key

@log_errors(default_return=False, raise_exception=False)
def check_public_port_exposure(port):
    """
    Check if port is publicly accessible.

    Args:
        port (int): Port number to check

    Returns:
        bool: True if port is publicly accessible
    """
    is_public_exposed = False
    is_locally_available = False
    # Check if port is publicly accessible
    public_ip = urllib.request.urlopen("https://ident.me", timeout=10).read().decode("utf8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_sock:
        conn_sock.settimeout(3)
        result = conn_sock.connect_ex((public_ip, port))
        is_public_exposed = result == 0
    
    # Check if port is locally available
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bind_sock:
        bind_sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        bind_sock.bind(("", port))
        bind_sock.listen(1)
        is_locally_available = True

    if not is_public_exposed:
        logging.debug(
            "Port %d is not publicly exposed",
            port,
        )
        return False
    if not is_locally_available:
        logging.debug(
            "Port %d is not locally available",
            port,
        )
        return False
    return True
