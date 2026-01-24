import pytest
from django.conf import settings
from django.db import models

from wbcore import serializers, viewsets
from wbcore.contrib.pandas.views import PandasAPIViewSet

from .mixins import (
    TestChartViewSet,
    TestModel,
    TestPandasView,
    TestRepresentationViewSet,
    TestSerializer,
    TestViewSet,
)
from .utils import get_all_subclasses, is_intermediate_table_m2m

""""
If CELERY_TASK_ALWAYS_EAGER is True, all tasks will be executed locally by blocking until the task returns.
apply_async() and Task.delay() will return an EagerResult instance, that emulates the API and behavior of AsyncResult, except the result is already evaluated.
That is, tasks will be executed locally instead of being sent to the queue.
This is useful mainly when running tests, or running locally without Celery workers.
"""
settings.CELERY_TASK_ALWAYS_EAGER = True


def modules_condition(module):
    return not module.startswith(("wbcore", "django", "rest_framework", "dynamic_preferences", "eventtools")) or (
        module.startswith("wbcore") and module.startswith("wbcore.contrib")
    )


default_config = {
    "models": list(
        filter(
            lambda x: modules_condition(x.__module__) and not x._meta.abstract and not is_intermediate_table_m2m(x),
            get_all_subclasses(models.Model),
        )
    ),
    "serializers": list(
        filter(lambda x: modules_condition(x.__module__), get_all_subclasses(serializers.ModelSerializer))
    ),
    "representations": list(
        filter(lambda x: modules_condition(x.__module__), get_all_subclasses(viewsets.RepresentationViewSet))
    ),
    "viewsets": list(
        filter(
            lambda x: modules_condition(x.__module__) and x not in get_all_subclasses(viewsets.InfiniteDataModelView),
            get_all_subclasses(viewsets.ModelViewSet),
        )
    ),
    "pandasviews": list(
        filter(
            lambda x: modules_condition(x.__module__),
            get_all_subclasses(PandasAPIViewSet),
        )
    ),
    "chartviewsets": list(
        filter(
            lambda x: modules_condition(x.__module__),
            get_all_subclasses(viewsets.ChartViewSet),
        )
    ),
}


class GenerateTest:
    def __init__(self, config):
        self.config = config

    def test_models(self, _model):
        my_test = TestModel(_model)
        my_test.execute_test()

    def test_serializers(self, _serializer):
        my_test = TestSerializer(_serializer)
        my_test.execute_test()

    def test_representationviewsets(self, rvs):
        my_test = TestRepresentationViewSet(rvs)
        my_test.execute_test()

    def test_modelviewsets(self, mvs, client):
        my_test = TestViewSet(mvs)
        my_test.execute_test_list_endpoint(client)
        my_test.execute_test_detail_endpoint()

    def test_pandasviews(self, pvs):
        my_test = TestPandasView(pvs)
        if my_test.model:
            my_test.execute_test()

    def test_chartviewsets(self, cvs):
        my_test = TestChartViewSet(cvs)
        my_test.execute_test()

    def __call__(self, test_class):
        @pytest.mark.parametrize("_model", self.config.get("models", []))
        def _test_models(_self, _model):
            self.test_models(_model)

        @pytest.mark.parametrize("_serializer", self.config.get("serializers", []))
        def _test_serializers(_self, _serializer):
            self.test_serializers(_serializer)

        @pytest.mark.parametrize("rvs", self.config.get("representations", []))
        def _test_representationviewsets(_self, rvs):
            self.test_representationviewsets(rvs)

        @pytest.mark.parametrize("mvs", self.config.get("viewsets", []))
        def _test_modelviewsets(_self, mvs, client):
            self.test_modelviewsets(mvs, client)

        @pytest.mark.parametrize("pvs", self.config.get("pandasviews", []))
        def _test_pandasviews(_self, pvs):
            self.test_pandasviews(pvs)

        @pytest.mark.parametrize("cvs", self.config.get("chartviewsets", []))
        def _test_chartviewsets(_self, cvs):
            self.test_chartviewsets(cvs)

        test_class.test_models = _test_models
        test_class.test_serializers = _test_serializers
        test_class.test_representationviewsets = _test_representationviewsets
        test_class.test_modelviewsets = _test_modelviewsets
        test_class.test_pandasviews = _test_pandasviews
        test_class.test_chartviewsets = _test_chartviewsets

        return test_class
