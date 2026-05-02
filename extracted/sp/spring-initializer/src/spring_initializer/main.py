import requests
import os
import time
import zipfile
import tarfile
import shutil
from requests.exceptions import Timeout, RequestException
from .file_tools import FileTools


class Main():
    def __init__(self):
        self.fileTools = FileTools()
    
    def download_with_retry(self, url, filename, max_retries=10, timeout=2):
        """下载文件并实现超时重试机制"""
        for attempt in range(max_retries):
            try:
                print(f"尝试下载 ({attempt + 1}/{max_retries})...")
                response = requests.get(url, timeout=timeout, stream=True)
                response.raise_for_status()

                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("下载成功!")
                return True

            except Timeout:
                print(f"连接超时（{timeout}s），正在重试...")
            except RequestException as e:
                print(f"网络错误: {str(e)}")
                time.sleep(1)  # 等待后重试

        print(f"下载失败，已达最大重试次数 {max_retries}")
        return False

    def extract_file(self, filename, extract_to):
        """解压文件到指定目录"""
        try:
            # 清理已存在的目录
            if os.path.exists(extract_to):
                shutil.rmtree(extract_to)
            os.makedirs(extract_to, exist_ok=True)

            # 根据文件类型选择解压方式
            if filename.endswith(".zip"):
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall(extract_to)
                print(f"ZIP文件已解压到: {extract_to}")

            elif filename.endswith(".tar.gz") or filename.endswith(".tgz"):
                with tarfile.open(filename, "r:gz") as tar_ref:
                    tar_ref.extractall(extract_to)
                print(f"TAR.GZ文件已解压到: {extract_to}")

            else:
                print("不支持的文件格式")
                return False

            return True

        except Exception as e:
            print(f"解压失败: {str(e)}")
            return False

    def generate_spring_project(
        self,
        dirName: str = "spring_demo",
        groupId: str = "com.example",
        javaVersion: str = "21",
        type: str = "maven-project",
        packging: str = "jar",
        dependencies: str = "web,lombok",
        removeZip: bool = True,
        packageName: str = "com.example.demo"
    ):
        """生成并下载Spring项目"""
        # Spring Initializr API参数
        base_url = "https://start.spring.io/starter.zip"
        params = {
            "type": type,
            "language": "java",
            "javaVersion": javaVersion,
            "groupId": groupId,
            "artifactId": "demo",
            "name": "demo",
            "description": "Spring Boot Demo",
            "packageName": packageName,
            "packaging": packging,
            "version": "0.0.1-SNAPSHOT",
            "dependencies": dependencies,
        }

        # 生成下载URL
        download_url = f"{base_url}?{requests.compat.urlencode(params)}"
        local_file = dirName + ".zip"
        extract_dir = os.path.join(os.getcwd(), dirName)
        
        # 检查目标目录是否已经存在
        if os.path.exists(extract_dir):
            print(f"目标目录：{extract_dir} 已经存在，无法创建 Spring 项目，请先删除该目录。")
            return False

        # 下载并解压
        if self.download_with_retry(download_url, local_file):
            if self.extract_file(local_file, extract_dir):
                print("\nSpring项目已成功创建！")
                print(f"目录位置: {os.path.abspath(extract_dir)}")
                print("包含依赖: " + dependencies)
                # 删除压缩包
                if removeZip:
                    os.remove(local_file)
                return True

        return False
    
    def printHelp(self):
        helpFilePath = os.path.join(self.fileTools.getProjectHomeDir(), "help.info")
        with open(file=helpFilePath, mode='r', encoding='UTF-8') as helpFileOpen:
            content = helpFileOpen.read()
            print(content)
            
    def printVersion(self):
        import pkg_resources
        version = pkg_resources.get_distribution(
            'spring-initializer').version
        # version = self.fileTools.get_version_from_setup_cfg()
        print(f"当前版本：{version}")
