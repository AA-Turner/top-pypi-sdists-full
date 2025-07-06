from appian_locust._ui_reconciler import UiReconciler
import unittest


class TestUiReconciler(unittest.TestCase):

    def setUp(self) -> None:
        self.reconciler: UiReconciler = UiReconciler()

    def test_reconcile_new_state_replace(self) -> None:
        # Given
        old_state = {"ui": {'#t': 'abc'}}
        new_state = {"ui": {'#t': '123'}}

        # When
        reconciled_state = self.reconciler.reconcile_ui(old_state, new_state)

        # Then
        self.assertEqual(reconciled_state, new_state)

    def test_reconcile_reconcile_one_level_deep_replace(self) -> None:
        # Given
        old_component = {'_cId': '12345', 'value': "This is what it used to be"}
        new_component = {'_cId': '12345', 'value': "This is what it is now"}
        old_state = {'context': 'abc', "ui": {'#t': 'abc', 'contents': [old_component]}, "timers": {"#t": "Dictionary"}}
        new_state = {'context': '123', "ui": {'#t': UiReconciler.COMPONENT_DELTA_TYPE, 'modifiedComponents': [new_component]}}

        # When
        reconciled_state = self.reconciler.reconcile_ui(old_state, new_state)

        # Then
        self.assertNotEqual(reconciled_state, new_state)
        self.assertEqual('123', reconciled_state['context'])
        self.assertEqual(new_component, reconciled_state['ui']['contents'][0])

    def test_reconcile_reconcile_two_levels_deep_replace(self) -> None:
        # Given
        old_component = {'_cId': '12345', 'value': "This is what it used to be"}
        old_unchanged_component = {'_cId': '55555', 'value': "This is what it used to be"}
        new_component = {'_cId': '12345', 'value': "This is what it is now"}
        old_state = {'context': 'abc', "ui": {'#t': 'abc', 'contents': [{'contents': [old_component, old_unchanged_component]}]}, "timers": {"#t": "Dictionary"}}
        new_state = {'context': '123', "ui": {'#t': UiReconciler.COMPONENT_DELTA_TYPE, 'modifiedComponents': [new_component]}}

        # When
        reconciled_state = self.reconciler.reconcile_ui(old_state, new_state)

        # Then
        self.assertNotEqual(reconciled_state, new_state)
        self.assertEqual('123', reconciled_state['context'])
        self.assertEqual(new_component, reconciled_state['ui']['contents'][0]['contents'][0])
        self.assertEqual(old_unchanged_component, reconciled_state['ui']['contents'][0]['contents'][1])


if __name__ == '__main__':
    unittest.main()
