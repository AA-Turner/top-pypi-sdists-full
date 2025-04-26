import os
import sys
import platform

class Tree:
    def __init__(self):
        self.dirCount = 0
        self.fileCount = 0
        # Set box drawing characters based on OS
        if platform.system() == 'Windows':
            self.PIPE = '|'
            self.ELBOW = '\\'
            self.TEE = '+'
            self.PIPE_PREFIX = '|   '
            self.SPACE_PREFIX = '    '
        else:
            self.PIPE = '│'
            self.ELBOW = '└'
            self.TEE = '├'
            self.PIPE_PREFIX = '│   '
            self.SPACE_PREFIX = '    '

    def register(self, absolute):
        if os.path.isdir(absolute):
            self.dirCount += 1
        else:
            self.fileCount += 1

    def summary(self):
        return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

    def walk(self, directory, prefix = "", exclude = [], stdout = sys.stdout):
        try:
            filepaths = sorted([filepath for filepath in os.listdir(directory)])
        except PermissionError:
            return
        except OSError:
            return

        for index in range(len(filepaths)):
            exclude = set(exclude)
            if filepaths[index] in exclude:
                continue
            if filepaths[index][0] == ".":
                continue

            absolute = os.path.join(directory, filepaths[index])
            self.register(absolute)

            if index == len(filepaths) - 1:
                print(prefix + self.ELBOW + "── " + os.path.basename(absolute), file = stdout, flush=True)
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + self.SPACE_PREFIX, exclude, stdout)
            else:
                print(prefix + self.TEE + "── " + os.path.basename(absolute), file = stdout, flush=True) 
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + self.PIPE_PREFIX, exclude, stdout)