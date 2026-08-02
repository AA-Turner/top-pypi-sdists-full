class BuildMappingRequest(object):
    def __init__(self, meta, configuration_data, files, dependencies=None):
        self.meta = meta
        self.configurationData = configuration_data
        self.files = files
        self.dependencies = dependencies or []
