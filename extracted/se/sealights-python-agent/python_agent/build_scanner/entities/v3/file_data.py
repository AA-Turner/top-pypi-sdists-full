import os


class FileData(object):
    def __init__(self, logical_path):
        logical_path = logical_path.replace("\\", "/")
        self.logicalPath = logical_path
        self.physicalPath = logical_path
        self.filename = self.get_filename(logical_path)
        self.hash = ""
        self.methods = []
        self.commitIndexes = []
        self.lines = []
        self.error = None

    def __str__(self):
        return (
            "FileData(logicalPath=%s, physicalPath=%s, hash=%s, commitIndexes=%s )"
            % (self.logicalPath, self.physicalPath, self.hash, self.commitIndexes)
        )

    def get_filename(self, path):
        return os.path.basename(path.rstrip("/"))
