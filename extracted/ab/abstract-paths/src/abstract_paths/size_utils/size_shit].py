from src import *


def replicate_directory_structure(src_directory, dst_directory,local=True, host=None):
    src_directory,src_local,src_host,src_outfile = get_directory_vars(src_directory,local=local,host=host)
    dst_directory,dst_local,dst_host,dst_outfile = get_directory_vars(src_directory,local=local,host=host)
src_directory = {"directory":"/home","password":"1"}
dst_directory = {"directory":'/mnt/24T/consolidated/backups/phones/ubuntu_backups/ubuntu_main/home',"local":False, "host":'solcatcher',"password":"ANy1Kan@!23"}
src_size_output = run_size_cmd(**dst_directory)
sizes = get_sizes(src_directory,dst_directory)

