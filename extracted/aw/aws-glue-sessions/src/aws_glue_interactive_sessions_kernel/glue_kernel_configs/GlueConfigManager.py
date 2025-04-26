class GlueConfigManager:
    def __init__(self, config_retriever_ordered_dict):
        self.config_retriever_ordered_dict = config_retriever_ordered_dict

    def get_config_by_priority(self, config_name):
        for config_retriever in self.config_retriever_ordered_dict.values():
            value = config_retriever.get_config_variable(config_name)
            if value is not None:
                return value
        return None

    # This method works only for configs which support dict type as return type.
    # The values are iterated in reverse as the values with same keys can be replaced according to config priority.
    def get_config_from_all_retrievers(self, config_name):
        values = dict()
        for config_retriever in reversed(self.config_retriever_ordered_dict.values()):
            value = config_retriever.get_config_variable(config_name)
            if value is not None:
                values = {**values, **value}
        return values
