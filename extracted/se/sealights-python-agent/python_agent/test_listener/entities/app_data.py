class AppData(object):
    def __init__(self, app_name, branch_name, build_name, files):
        self.appName = app_name
        self.branchName = branch_name
        self.buildName = build_name
        self.files = files
