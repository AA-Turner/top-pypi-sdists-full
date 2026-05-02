import os
from configparser import ConfigParser
from pathlib import Path
class FileTools():
    def getCurrentDirPath(self):
        """获取当前文件所在目录"""
        part = __file__.rpartition(self.getPathSplit())
        return part[0]
    
    def getProjectHomeDir(self):
        """获取项目代码的根目录"""
        return self.getCurrentDirPath()
    
    def getProjectRootDir(self):
        """获取项目根目录"""
        return os.path.join(self.getProjectHomeDir(),"..","..")
    
    def getPathSplit(self):
        """获取路径分割符"""
        return os.path.sep
    
    def get_version_from_setup_cfg(self):
        # cfg_path = Path(__file__).parent / "setup.cfg"  # 假设与当前脚本同目录
        cfg_path = os.path.join(self.getProjectRootDir(), "setup.cfg")
        config = ConfigParser()
        config.read(cfg_path, encoding="utf-8")
        if (not os.path.exists(cfg_path)):
            raise RuntimeError(f"配置文件 {cfg_path} 不存在")
        if not config.has_section('metadata'):
            raise ValueError(f"缺失 [metadata] 节，请检查配置文件")
        try:
            return config.get("metadata", "version")
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"读取版本失败: {e}")