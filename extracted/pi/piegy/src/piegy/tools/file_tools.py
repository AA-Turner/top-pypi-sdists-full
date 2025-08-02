'''
File-processing tools.

Functions:
- del_dirs:     Delete everything in a directory, as well as the directory itself.
'''

import os


def del_dirs(dirs):
    # Delete everything in a directory.
    
    subdirs_list = []
    
    for subdirs, dirs_, files in os.walk(dirs):
        if subdirs not in subdirs_list:
            subdirs_list.append(subdirs)
            
        for file in files:
            path = os.path.join(subdirs, file)
            if os.path.isfile(path):
                os.remove(path)
    
    len_s = len(subdirs_list)
    
    for i in range(len_s):
        os.rmdir(subdirs_list[len_s - i - 1])

