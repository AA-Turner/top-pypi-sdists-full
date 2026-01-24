from unittest.mock import patch

import pytest
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.workflow.models import Condition


@pytest.mark.django_db
class TestCondition:
    def test_errors_satisfied_not_called(self, condition_factory):
        condition = condition_factory()
        with pytest.raises(ValueError):
            assert condition.errors == []

    def test_errors(self, condition_factory):
        condition = condition_factory()
        with patch.object(condition, "_errors", create=True):
            assert condition.errors

    def test_satisfied_attribute_error(self, condition_factory):
        instance = PersonFactory()
        condition = condition_factory(attribute_name="Test")
        assert not condition.satisfied(instance)
        assert len(condition.errors) == 1

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_value_error(self, mock_cast, condition_factory):
        instance = PersonFactory()
        condition = condition_factory()
        mock_cast.side_effect = ValueError
        assert not condition.satisfied(instance)
        assert len(condition.errors) == 1

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_eq(self, mock_cast, condition_factory):
        instance = PersonFactory()
        condition1 = condition_factory(operator=Condition.Operator.EQ, negate_operator=False)
        condition2 = condition_factory(operator=Condition.Operator.EQ, negate_operator=True)
        mock_cast.return_value = instance.first_name
        assert condition1.satisfied(instance)
        assert not condition1.errors
        assert not condition2.satisfied(instance)
        assert not condition2.errors

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_gt(self, mock_cast, condition_factory):
        instance = PersonFactory(personality_profile_red=5)
        condition1 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.GT, negate_operator=False
        )
        condition2 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.GT, negate_operator=True
        )
        mock_cast.return_value = 3
        assert condition1.satisfied(instance)
        assert not condition1.errors
        assert not condition2.satisfied(instance)
        assert not condition2.errors

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_gte(self, mock_cast, condition_factory):
        instance = PersonFactory(personality_profile_red=5)
        condition1 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.GTE, negate_operator=False
        )
        condition2 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.GTE, negate_operator=True
        )
        mock_cast.return_value = 5
        assert condition1.satisfied(instance)
        assert not condition1.errors
        assert not condition2.satisfied(instance)
        assert not condition2.errors

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_lt(self, mock_cast, condition_factory):
        instance = PersonFactory(personality_profile_red=2)
        condition1 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.LT, negate_operator=False
        )
        condition2 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.LT, negate_operator=True
        )
        mock_cast.return_value = 5
        assert condition1.satisfied(instance)
        assert not condition1.errors
        assert not condition2.satisfied(instance)
        assert not condition2.errors

    @patch("wbcore.contrib.workflow.models.data.Data.cast_value_from_target_object")
    def test_satisfied_lte(self, mock_cast, condition_factory):
        instance = PersonFactory(personality_profile_red=2)
        condition1 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.LTE, negate_operator=False
        )
        condition2 = condition_factory(
            attribute_name="personality_profile_red", operator=Condition.Operator.LTE, negate_operator=True
        )
        mock_cast.return_value = 2
        assert condition1.satisfied(instance)
        assert not condition1.errors
        assert not condition2.satisfied(instance)
        assert not condition2.errors
