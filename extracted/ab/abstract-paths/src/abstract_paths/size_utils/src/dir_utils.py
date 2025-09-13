import os
from .cmd_utils import *
from abstract_utilities.cmd_utils import get_sudo_password,get_env_value
def get_password(password=None,key=None):
    if password:
        return password
    if key:
        return get_env_value(key)
    return get_sudo_password()
class directoryHist:
    def __init__(self):
        self.history = {}
        self.abs_dir = os.path.dirname(os.path.abspath(__name__))
    def get_filepath(self,directory,local=True,outfile=False):
        if outfile == False:
            return None
        file_path = outfile
        if not isinstance(outfile,str):
            basename = os.path.basename(directory)
            basepath = os.path.join(self.abs_dir,basename)
            file_path = f"{basepath}.txt"
            key = f"{directory}_local"
            if not local:
                key = f"{directory}_ssh"
                
            if os.path.exists(file_path):
                if self.history.get(key) != file_path:
                    i=0
                    while True:
                        nubasepath=f"{basepath}_{i}"
                        file_path = f"{nubasepath}.txt"
                        if not os.path.exists(file_path):
                            break
                        i+=1
        self.history[key] = file_path
        return file_path
dir_mgr = directoryHist()
def get_outfile(directory):
    return dir_mgr.get_filepath(directory)
def get_is_ssh_dir(directory,host,outfile=False):
    outfile = dir_mgr.get_filepath(directory,local=False,outfile=outfile)
    resp = run_remote_cmd(user_at_host=host, cmd=f"ls {directory}", workdir=directory, outfile=outfile,shell=True, text=True, capture_output=True)
    return not resp.endswith('No such file or directory')
def is_src_dir(directory):
    return directory and os.path.isdir(str(directory))

def get_directory_vars(directory,local=True,host=None,outfile=False,password=None,key=None):
    if isinstance(directory,dict):
        host = directory.get('host')
        dir_ = directory.get('directory')
        outfile = directory.get('outfile',outfile)
        password = directory.get('password',password)
        key = directory.get('key',key)
        local = directory.get('local', False if host else os.path.exists(dir_))
        directory = dir_
    src_dir = is_src_dir(directory)
    ssh_dir= get_is_ssh_dir(directory,host)
    outfile = dir_mgr.get_filepath(directory,local=local,outfile=outfile)
    if (local and src_dir) or (not local and ssh_dir):
        return directory,local,host,outfile,get_password(password=password,key=key)
    return None,None,None,None
