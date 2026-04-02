from django.test import TestCase

from taskmonitor.core.list_queryset import ListAsQuerySet
from taskmonitor.models import QueuedTask
from taskmonitor.tests.factories import QueuedTaskFactory


class TestOther(TestCase):
    def test_count(self):
        # given
        data = [QueuedTaskFactory.build(), QueuedTaskFactory.build()]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when/then
        self.assertEqual(qs.count(), 2)

    def test_none(self):
        # given
        data = [
            QueuedTaskFactory.build(),
            QueuedTaskFactory.build(),
            QueuedTaskFactory.build(),
        ]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.none()
        # then
        self.assertEqual(result, [])

    def test_get_should_return_obj(self):
        # given
        t1 = QueuedTaskFactory.build(id=1)
        t2 = QueuedTaskFactory.build(id=2)
        t3 = QueuedTaskFactory.build(id=3)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        obj = qs.get(id=3)
        # then
        self.assertEqual(obj, t3)

    def test_get_should_raise_error_when_obj_not_found(self):
        # given
        t1 = QueuedTaskFactory.build(id=1)
        t2 = QueuedTaskFactory.build(id=2)
        t3 = QueuedTaskFactory.build(id=3)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when/then
        with self.assertRaises(QueuedTask.DoesNotExist):
            qs.get(id=4)

    def test_first_should_return_obj_when_it_exists(self):
        # given
        t1 = QueuedTaskFactory.build(id=1)
        t2 = QueuedTaskFactory.build(id=2)
        t3 = QueuedTaskFactory.build(id=3)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        obj = qs.first()
        # then
        self.assertEqual(obj, t1)

    def test_first_should_return_none_when_obj_not_exists(self):
        # given
        data = []
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        obj = qs.first()
        # then
        self.assertIsNone(obj)

    def test_last_should_return_last_element_when_it_exists(self):
        # given
        t1 = QueuedTaskFactory.build(id=1)
        t2 = QueuedTaskFactory.build(id=2)
        t3 = QueuedTaskFactory.build(id=3)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        obj = qs.last()
        # then
        self.assertEqual(obj, t3)

    def test_last_should_return_none_when_obj_not_exists(self):
        # given
        data = []
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        obj = qs.last()
        # then
        self.assertIsNone(obj)

    def test_clone(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="one")
        t2 = QueuedTaskFactory.build(app_name="alpha", name="two")
        t3 = QueuedTaskFactory.build(app_name="alpha", name="three")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs._clone()

        # then
        self.assertEqual(result, data)
        self.assertIsNot(result, data)

    def test_should_raise_error_when_trying_to_create(self):
        # when/then
        with self.assertRaises(NotImplementedError):
            QueuedTaskFactory.create()


class TestAll(TestCase):
    def test_should_return_all_objs(self):
        # given
        t1 = QueuedTaskFactory.build()
        t2 = QueuedTaskFactory.build()
        data = [t1, t2]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.all()
        # then
        self.assertEqual(result, data)

    def test_should_return_all_objs_with_distinct(self):
        # given
        t1 = QueuedTaskFactory.build()
        data = [t1, t1]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.distinct().all()
        # then
        self.assertEqual(result, [t1])


class TestFilter(TestCase):
    def test_filter_no_params(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="one")
        t2 = QueuedTaskFactory.build(app_name="alpha", name="two")
        t3 = QueuedTaskFactory.build(app_name="alpha", name="three")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.filter()
        self.assertEqual(result, data)

    def test_filter_single_kwargs(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="one")
        t2 = QueuedTaskFactory.build(app_name="alpha", name="two")
        t3 = QueuedTaskFactory.build(app_name="alpha", name="three")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.filter(name="two")
        self.assertEqual(result, [t2])

    def test_filter_multiple_kwargs(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="1", priority=2)
        t2 = QueuedTaskFactory.build(app_name="alpha", name="2", priority=3)
        t3 = QueuedTaskFactory.build(app_name="alpha", name="3", priority=3)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.filter(app_name="alpha", priority=3)
        self.assertEqual(result, [t2, t3])

    def test_filter_kwargs_with_contains(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="joe_1")
        t2 = QueuedTaskFactory.build(app_name="alpha", name="joe_2")
        t3 = QueuedTaskFactory.build(app_name="alpha", name="Joe")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.filter(name__contains="joe")
        self.assertEqual(result, [t1, t2])

    def test_filter_kwargs_with_icontains(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="joe_1")
        t2 = QueuedTaskFactory.build(app_name="alpha", name="Joe_2")
        t3 = QueuedTaskFactory.build(app_name="alpha", name="bob")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when
        result = qs.filter(name__icontains="joe")
        self.assertEqual(result, [t1, t2])

    def test_should_raise_error_when_lookup_is_unknown(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="joe_1")
        data = [t1]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when/then
        with self.assertRaises(NotImplementedError):
            qs.filter(name__unknown="joe")

    def test_should_raise_error_when_filter_is_invalid(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="alpha", name="joe_1")
        data = [t1]
        qs = ListAsQuerySet(data, model=QueuedTask)
        # when/then
        with self.assertRaises(ValueError):
            qs.filter(name__exact__illegal="joe")

    def test_filter_should_allow_chaining(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="charlie")
        t2 = QueuedTaskFactory.build(app_name="alpha")
        t3 = QueuedTaskFactory.build(app_name="alpha")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.filter(app_name="alpha").count()

        # then
        self.assertEqual(result, 2)


class TestOrderBy(TestCase):
    def test_should_order_by_field_ascending(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie")
        t2 = QueuedTaskFactory.build(name="alpha")
        t3 = QueuedTaskFactory.build(name="bravo")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.order_by("name")

        # then
        self.assertIsInstance(result, ListAsQuerySet)
        self.assertEqual(result, [t2, t3, t1])

    def test_should_order_by_field_descending(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie")
        t2 = QueuedTaskFactory.build(name="alpha")
        t3 = QueuedTaskFactory.build(name="bravo")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.order_by("-name")

        # then
        self.assertIsInstance(result, ListAsQuerySet)
        self.assertEqual(result, [t1, t3, t2])

    def test_order_should_return_self_unchanged_when_no_params_given(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie")
        t2 = QueuedTaskFactory.build(name="alpha")
        t3 = QueuedTaskFactory.build(name="bravo")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.order_by()

        # then
        self.assertIsInstance(result, ListAsQuerySet)
        self.assertEqual(result, qs)

    def test_should_order_by_multiple_fields_ascending(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        t3 = QueuedTaskFactory.build(name="alpha", priority=1)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.order_by("name", "priority")

        # then
        self.assertIsInstance(result, ListAsQuerySet)
        self.assertEqual(result, [t3, t2, t1])

    def test_should_order_by_multiple_fields_mixed(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        t3 = QueuedTaskFactory.build(name="alpha", priority=1)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.order_by("-name", "priority")

        # then
        self.assertIsInstance(result, ListAsQuerySet)
        self.assertEqual(result, [t1, t3, t2])

    def test_should_keep_distinct(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        t3 = QueuedTaskFactory.build(name="alpha", priority=1)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.distinct().order_by("name").values_list("name", flat=True)

        # then
        self.assertEqual(result, ["alpha", "charlie"])


class TestValues(TestCase):
    def test_should_return_data(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        data = [t1, t2]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.values("name", "priority")

        # then
        self.assertEqual(
            result,
            [{"name": "charlie", "priority": 1}, {"name": "alpha", "priority": 2}],
        )

    def test_should_return_data_with_distinct(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie")
        t2 = QueuedTaskFactory.build(name="alpha")
        t3 = QueuedTaskFactory.build(name="alpha")
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.distinct().values("name")

        # then
        self.assertEqual(result, [{"name": "charlie"}, {"name": "alpha"}])


class TestValuesList(TestCase):
    def test_should_return_as_tuples(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        data = [t1, t2]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.values_list("name", "priority")

        # then
        self.assertEqual(result, [("charlie", 1), ("alpha", 2)])

    def test_should_return_flat(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(app_name="alpha", priority=2)
        t3 = QueuedTaskFactory.build(app_name="charlie", priority=1)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.values_list("app_name", flat=True)

        # then
        self.assertListEqual(result, ["charlie", "alpha", "charlie"])

    def test_should_return_flat_and_distinct(self):
        # given
        t1 = QueuedTaskFactory.build(app_name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(app_name="alpha", priority=2)
        t3 = QueuedTaskFactory.build(app_name="charlie", priority=1)
        data = [t1, t2, t3]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when
        result = qs.distinct().values_list("app_name", flat=True)

        # then
        self.assertListEqual(result, ["charlie", "alpha"])

    def test_should_raise_error_when_trying_flat_with_multiple_fields(self):
        # given
        t1 = QueuedTaskFactory.build(name="charlie", priority=1)
        t2 = QueuedTaskFactory.build(name="alpha", priority=2)
        data = [t1, t2]
        qs = ListAsQuerySet(data, model=QueuedTask)

        # when/then
        with self.assertRaises(TypeError):
            qs.values_list("name", "priority", flat=True)
