from unittest.mock import MagicMock

class RulesApiMock:

    def __init__(self):
        self.mock_cleanup_standalone_rules = MagicMock()
        self.mock_create_ruleset_label = MagicMock()
        self.mock_create_standalone_rule = MagicMock()
        self.mock_create_standalone_rule_policy = MagicMock()
        self.mock_create_standalone_rule_tree = MagicMock()
        self.mock_create_standalone_ruleset = MagicMock()
        self.mock_create_standalone_ruleset_bundle = MagicMock()
        self.mock_delete_ruleset_label = MagicMock()
        self.mock_delete_standalone_rule = MagicMock()
        self.mock_delete_standalone_rule_policy = MagicMock()
        self.mock_delete_standalone_rule_tree = MagicMock()
        self.mock_delete_standalone_ruleset = MagicMock()
        self.mock_delete_standalone_ruleset_bundle = MagicMock()
        self.mock_get_ruleset_label = MagicMock()
        self.mock_get_standalone_rule = MagicMock()
        self.mock_get_standalone_rule_policy = MagicMock()
        self.mock_get_standalone_rule_tree = MagicMock()
        self.mock_get_standalone_ruleset = MagicMock()
        self.mock_get_standalone_ruleset_bundle = MagicMock()
        self.mock_list_ruleset_labels = MagicMock()
        self.mock_list_standalone_rule_policies = MagicMock()
        self.mock_list_standalone_rule_trees = MagicMock()
        self.mock_list_standalone_rules = MagicMock()
        self.mock_list_standalone_ruleset_bundles = MagicMock()
        self.mock_list_standalone_rulesets = MagicMock()
        self.mock_replace_standalone_rule = MagicMock()
        self.mock_replace_standalone_rule_policy = MagicMock()
        self.mock_replace_standalone_rule_tree = MagicMock()
        self.mock_replace_standalone_ruleset = MagicMock()
        self.mock_replace_standalone_ruleset_bundle = MagicMock()

    def cleanup_standalone_rules(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.cleanup_standalone_rules with MagicMock.
        """
        return self.mock_cleanup_standalone_rules(self, *args, **kwargs)

    def create_ruleset_label(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_ruleset_label with MagicMock.
        """
        return self.mock_create_ruleset_label(self, *args, **kwargs)

    def create_standalone_rule(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_standalone_rule with MagicMock.
        """
        return self.mock_create_standalone_rule(self, *args, **kwargs)

    def create_standalone_rule_policy(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_standalone_rule_policy with MagicMock.
        """
        return self.mock_create_standalone_rule_policy(self, *args, **kwargs)

    def create_standalone_rule_tree(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_standalone_rule_tree with MagicMock.
        """
        return self.mock_create_standalone_rule_tree(self, *args, **kwargs)

    def create_standalone_ruleset(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_standalone_ruleset with MagicMock.
        """
        return self.mock_create_standalone_ruleset(self, *args, **kwargs)

    def create_standalone_ruleset_bundle(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.create_standalone_ruleset_bundle with MagicMock.
        """
        return self.mock_create_standalone_ruleset_bundle(self, *args, **kwargs)

    def delete_ruleset_label(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_ruleset_label with MagicMock.
        """
        return self.mock_delete_ruleset_label(self, *args, **kwargs)

    def delete_standalone_rule(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_standalone_rule with MagicMock.
        """
        return self.mock_delete_standalone_rule(self, *args, **kwargs)

    def delete_standalone_rule_policy(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_standalone_rule_policy with MagicMock.
        """
        return self.mock_delete_standalone_rule_policy(self, *args, **kwargs)

    def delete_standalone_rule_tree(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_standalone_rule_tree with MagicMock.
        """
        return self.mock_delete_standalone_rule_tree(self, *args, **kwargs)

    def delete_standalone_ruleset(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_standalone_ruleset with MagicMock.
        """
        return self.mock_delete_standalone_ruleset(self, *args, **kwargs)

    def delete_standalone_ruleset_bundle(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.delete_standalone_ruleset_bundle with MagicMock.
        """
        return self.mock_delete_standalone_ruleset_bundle(self, *args, **kwargs)

    def get_ruleset_label(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_ruleset_label with MagicMock.
        """
        return self.mock_get_ruleset_label(self, *args, **kwargs)

    def get_standalone_rule(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_standalone_rule with MagicMock.
        """
        return self.mock_get_standalone_rule(self, *args, **kwargs)

    def get_standalone_rule_policy(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_standalone_rule_policy with MagicMock.
        """
        return self.mock_get_standalone_rule_policy(self, *args, **kwargs)

    def get_standalone_rule_tree(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_standalone_rule_tree with MagicMock.
        """
        return self.mock_get_standalone_rule_tree(self, *args, **kwargs)

    def get_standalone_ruleset(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_standalone_ruleset with MagicMock.
        """
        return self.mock_get_standalone_ruleset(self, *args, **kwargs)

    def get_standalone_ruleset_bundle(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.get_standalone_ruleset_bundle with MagicMock.
        """
        return self.mock_get_standalone_ruleset_bundle(self, *args, **kwargs)

    def list_ruleset_labels(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_ruleset_labels with MagicMock.
        """
        return self.mock_list_ruleset_labels(self, *args, **kwargs)

    def list_standalone_rule_policies(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_standalone_rule_policies with MagicMock.
        """
        return self.mock_list_standalone_rule_policies(self, *args, **kwargs)

    def list_standalone_rule_trees(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_standalone_rule_trees with MagicMock.
        """
        return self.mock_list_standalone_rule_trees(self, *args, **kwargs)

    def list_standalone_rules(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_standalone_rules with MagicMock.
        """
        return self.mock_list_standalone_rules(self, *args, **kwargs)

    def list_standalone_ruleset_bundles(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_standalone_ruleset_bundles with MagicMock.
        """
        return self.mock_list_standalone_ruleset_bundles(self, *args, **kwargs)

    def list_standalone_rulesets(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.list_standalone_rulesets with MagicMock.
        """
        return self.mock_list_standalone_rulesets(self, *args, **kwargs)

    def replace_standalone_rule(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.replace_standalone_rule with MagicMock.
        """
        return self.mock_replace_standalone_rule(self, *args, **kwargs)

    def replace_standalone_rule_policy(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.replace_standalone_rule_policy with MagicMock.
        """
        return self.mock_replace_standalone_rule_policy(self, *args, **kwargs)

    def replace_standalone_rule_tree(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.replace_standalone_rule_tree with MagicMock.
        """
        return self.mock_replace_standalone_rule_tree(self, *args, **kwargs)

    def replace_standalone_ruleset(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.replace_standalone_ruleset with MagicMock.
        """
        return self.mock_replace_standalone_ruleset(self, *args, **kwargs)

    def replace_standalone_ruleset_bundle(self, *args, **kwargs):
        """
        This method mocks the original api RulesApi.replace_standalone_ruleset_bundle with MagicMock.
        """
        return self.mock_replace_standalone_ruleset_bundle(self, *args, **kwargs)

