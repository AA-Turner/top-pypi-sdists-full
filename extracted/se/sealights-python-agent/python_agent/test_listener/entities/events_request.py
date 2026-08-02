class EventsRequest(object):
    def __init__(
        self,
        customer_id,
        app_name,
        branch_name,
        build_name,
        environment_data,
        events,
        test_selection_status,
    ):
        self.customerId = customer_id
        self.appName = app_name
        self.branch = branch_name
        self.build = build_name
        self.environment = environment_data
        self.events = events
        self.testSelectionStatus = test_selection_status
