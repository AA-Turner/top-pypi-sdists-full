class FootprintsRequest(object):
    def __init__(self, customer_id, environment_data, configuration_data, tests, apps):
        self.customerId = customer_id
        self.environment = environment_data
        self.configurationData = configuration_data
        self.tests = tests
        self.apps = apps
