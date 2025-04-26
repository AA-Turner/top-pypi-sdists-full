import hashlib
import os
import platform
import shutil
import string
import tarfile
import zipfile
from pathlib import Path

from mag_tools.enums.digest_alg import DigestAlg


class FileUtils:
    @staticmethod
    def is_system_path(path: str) -> bool:
        """
        判断一个目录是否为系统目录
        :param path: 目录路径
        :return: 如果是系统目录返回 True，否则返回 False
        """
        system_directories = []

        if platform.system() == "Windows":
            user_profile = os.environ.get("USERPROFILE", "C:\\Users\\Default").lower()

            # 获取所有驱动器的根目录
            drives = [f"{d}:" for d in string.ascii_lowercase if os.path.exists(f"{d}:")]

            system_directories = drives + [
                os.path.normpath(os.environ.get("SystemDrive", "C:")).lower(),
                os.path.normpath(os.environ.get("HOMEDRIVE", "C:")).lower(),
                os.path.normpath(os.environ.get("SystemRoot", "C:\\Windows")).lower(),
                os.path.normpath(os.environ.get("ProgramFiles", "C:\\Program Files")).lower(),
                os.path.normpath(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")).lower(),
                os.path.normpath(os.environ.get("Public", "C:\\Users\\Public")).lower(),
                os.path.normpath(os.environ.get("USERPROFILE", "C:\\Users\\Default")).lower(),
                os.path.normpath(os.environ.get("HOMEPATH", "C:\\Users\\Default")).lower(),
                os.path.join(user_profile, "Desktop").lower(),
                os.path.join(user_profile, "Documents").lower(),
                os.path.join(user_profile, "Downloads").lower(),
                os.path.join(user_profile, "Pictures").lower(),
                os.path.normpath("C:\\Windows\\System32").lower(),
                os.path.normpath("C:\\Windows\\SysWOW64").lower(),
                os.path.normpath("C:\\Users\\Default").lower(),
                os.path.normpath("C:\\ProgramData").lower(),
                os.path.normpath("C:\\Users").lower()
            ]
        elif platform.system() == "Linux":
            system_directories = [
                "/",
                "/bin", "/sbin", "/usr", "/lib", "/etc",
                "/boot", "/dev", "/home", "/opt", "/root", "/srv", "/var"
            ]

        # 标准化输入路径并去掉末尾的反斜杠
        normalized_path = os.path.normpath(path).lower().rstrip("\\")

        # 检查目录路径是否在系统目录列表中
        if normalized_path in system_directories:
            return True

        return False

    @staticmethod
    def copy_and_overwrite(src: str, dst: str):
        """
        将源文件覆盖目标文件
        :param src: 源文件路径
        :param dst: 目标文件路径
        """
        src_path = Path(src)
        dst_path = Path(dst)

        # 确保目标文件所在目录存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # 复制并覆盖文件
        shutil.copy2(src_path, dst_path)

    @staticmethod
    def clear_dir(dir_name):
        if os.path.exists(dir_name):
            if FileUtils.is_system_path(dir_name):
                raise ValueError(f"不能清除系统目录[{dir_name}]下的文件")

            for filename in os.listdir(dir_name):
                file_path = os.path.join(dir_name, filename)  # 构建文件的完整路径
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    else:
                        shutil.rmtree(file_path)
                except Exception as e:
                    raise ValueError(f"Error removing {file_path}: {e}")

    @staticmethod
    def delete_dir(dir_name):
        if os.path.exists(dir_name):
            if FileUtils.is_system_path(dir_name):
                raise ValueError(f"不能清除系统目录[{dir_name}]下的文件")

            shutil.rmtree(dir_name)

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            file_dir = os.path.dirname(file_path)
            if FileUtils.is_system_path(file_dir):
                raise ValueError(f"不能清除系统目录[{file_dir}]下的文件")

            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def file_size(file_path):
        if os.path.isfile(file_path):
            return os.path.getsize(file_path)
        else:
            return None

    @staticmethod
    def file_hash(file_path, algorithm=DigestAlg.MD5):
        """
        计算文件内容的哈希值

        :param file_path: 文件路径
        :param algorithm: 哈希算法（默认使用 'sha256'）
        :return: 文件哈希值的十六进制字符串表示
        """
        hash_func = hashlib.new(algorithm.code)
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def extract_zip(zip_path: str, extract_path: str):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    @staticmethod
    def extract_tar(tar_path: str, extract_path: str):
        with tarfile.open(tar_path, 'r') as tar_ref:
            tar_ref.extractall(extract_path)

if __name__ == '__main__':
    # 示例调用
    _file = "D:\\HiSimPack\\data\\Comp\\spe9\\SPE9.dat"
    hash_ = FileUtils.file_hash(_file)
    print(hash_)
