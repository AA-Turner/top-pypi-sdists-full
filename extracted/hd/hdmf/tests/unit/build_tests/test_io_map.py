from hdmf.utils import StrDataset, docval, getargs
from hdmf import Container, Data
from hdmf.backends.hdf5 import H5DataIO
from hdmf.build import (GroupBuilder, DatasetBuilder, ObjectMapper, BuildManager, TypeMap, LinkBuilder,
                        ReferenceBuilder, MissingRequiredBuildWarning, OrphanContainerBuildError,
                        ContainerConfigurationError)
from hdmf.spec import (GroupSpec, AttributeSpec, DatasetSpec, SpecCatalog, SpecNamespace, NamespaceCatalog, RefSpec,
                       LinkSpec)
from hdmf.testing import TestCase
import h5py
from abc import ABCMeta, abstractmethod
import unittest
import numpy as np

from tests.unit.helpers.utils import CORE_NAMESPACE, create_test_type_map

H5PY_3 = h5py.__version__.startswith('3')


class Bar(Container):

    @docval({'name': 'name', 'type': str, 'doc': 'the name of this Bar'},
            {'name': 'data', 'type': ('data', 'array_data'), 'doc': 'some data'},
            {'name': 'attr1', 'type': str, 'doc': 'an attribute'},
            {'name': 'attr2', 'type': int, 'doc': 'another attribute'},
            {'name': 'attr3', 'type': float, 'doc': 'a third attribute', 'default': 3.14},
            {'name': 'attr_array', 'type': 'array_data', 'doc': 'another attribute', 'default': (1, 2, 3)},
            {'name': 'foo', 'type': 'Foo', 'doc': 'a group', 'default': None})
    def __init__(self, **kwargs):
        name, data, attr1, attr2, attr3, attr_array, foo = getargs('name', 'data', 'attr1', 'attr2', 'attr3',
                                                                   'attr_array', 'foo', kwargs)
        super().__init__(name=name)
        self.__data = data
        self.__attr1 = attr1
        self.__attr2 = attr2
        self.__attr3 = attr3
        self.__attr_array = attr_array
        self.__foo = foo
        if self.__foo is not None and self.__foo.parent is None:
            self.__foo.parent = self

    def __eq__(self, other):
        attrs = ('name', 'data', 'attr1', 'attr2', 'attr3', 'attr_array', 'foo')
        return all(getattr(self, a) == getattr(other, a) for a in attrs)

    def __str__(self):
        attrs = ('name', 'data', 'attr1', 'attr2', 'attr3', 'attr_array', 'foo')
        return ','.join('%s=%s' % (a, getattr(self, a)) for a in attrs)

    @property
    def data_type(self):
        return 'Bar'

    @property
    def data(self):
        return self.__data

    @property
    def attr1(self):
        return self.__attr1

    @property
    def attr2(self):
        return self.__attr2

    @property
    def attr3(self):
        return self.__attr3

    @property
    def attr_array(self):
        return self.__attr_array

    @property
    def foo(self):
        return self.__foo

    def remove_foo(self):
        if self is self.__foo.parent:
            self._remove_child(self.__foo)


class SubBar(Bar):
    pass


class Foo(Container):

    @property
    def data_type(self):
        return 'Foo'


class FooData(Data):

    @property
    def data_type(self):
        return 'FooData'


class TestGetSubSpec(TestCase):

    def setUp(self):
        self.bar_spec = GroupSpec(doc='A test group specification with a data type', data_type_def='Bar')
        self.sub_bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='SubBar',
            data_type_inc='Bar'
        )
        self.type_map = create_test_type_map([self.bar_spec, self.sub_bar_spec], {'Bar': Bar, 'SubBar': SubBar})

    def test_bad_name(self):
        """Test get_subspec on a builder that doesn't map to the spec."""
        parent_spec = GroupSpec(doc='Empty group', name='bar_bucket')
        sub_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        GroupBuilder(name='bar_bucket', groups={'my_bar': sub_builder})  # add sub_builder as a child to bar_bucket
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIsNone(result)

    def test_bad_name_no_data_type(self):
        """Test get_subspec on a builder without a data type that doesn't map to the spec."""
        parent_spec = GroupSpec(doc='Empty group', name='bar_bucket')
        sub_builder = GroupBuilder(name='my_bar')
        GroupBuilder(name='bar_bucket', groups={'my_bar': sub_builder})  # add sub_builder as a child to bar_bucket
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIsNone(result)

    def test_unnamed_group_data_type_def(self):
        """Test get_subspec on a builder that maps to an unnamed subgroup of the given spec using data_type_def."""
        parent_spec = GroupSpec(
            doc='Something to hold a Bar',
            name='bar_bucket',
            groups=[self.bar_spec]  # using data_type_def, no name
        )
        sub_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        GroupBuilder(name='bar_bucket', groups={'my_bar': sub_builder})  # add sub_builder as a child to bar_bucket
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, self.bar_spec)

    def test_unnamed_group_data_type_inc(self):
        """Test get_subspec on a builder that maps to an unnamed subgroup of the given spec using data_type_inc."""
        inc_spec = GroupSpec(
            doc='This Bar',
            data_type_inc='Bar'
        )
        parent_spec = GroupSpec(
            doc='Something to hold a Bar',
            name='bar_bucket',
            groups=[inc_spec]  # using data_type_inc
        )
        sub_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        GroupBuilder(name='bar_bucket', groups={'my_bar': sub_builder})  # add sub_builder as a child to bar_bucket
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, inc_spec)

    def test_named_group(self):
        """Test get_subspec on a builder that maps to a named subgroup of the given spec."""
        # NOTE this works despite the fact that child_spec has no data type but the builder has a data type because
        # get_subspec acts on the name and not necessarily the data type
        child_spec = GroupSpec(doc='A test group specification', name='my_subgroup')
        parent_spec = GroupSpec(doc='Something to hold a Bar', name='my_group', groups=[child_spec])
        sub_builder = GroupBuilder(
            name='my_subgroup',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        GroupBuilder(name='my_group', groups={'my_bar': sub_builder})  # add sub_builder as a child to my_group
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, child_spec)

    def test_named_dataset(self):
        """Test get_subspec on a builder that maps to a named dataset of the given spec."""
        # NOTE this works despite the fact that child_spec has no data type but the builder has a data type because
        # get_subspec acts on the name and not necessarily the data type
        child_spec = DatasetSpec(doc='A test dataset specification', name='my_dataset')
        parent_spec = GroupSpec(doc='Something to hold a Bar', name='my_group', datasets=[child_spec])
        sub_builder = DatasetBuilder(
            name='my_dataset',
            data=[],
            attributes={
                'data_type': 'FooData',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        GroupBuilder(name='my_group', datasets={'my_dataset': sub_builder})  # add sub_builder as a child to my_group
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, child_spec)

    def test_unnamed_link_data_type_inc(self):
        """Test get_subspec on a builder that maps to an unnamed link."""
        link_spec = LinkSpec(doc='This Bar', target_type='Bar')
        parent_spec = GroupSpec(
            doc='Something to hold a Bar',
            name='bar_bucket',
            links=[link_spec]
        )
        bar_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        sub_builder = LinkBuilder(builder=bar_builder, name='my_link')
        GroupBuilder(name='bar_bucket', links={'my_bar': sub_builder})
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, link_spec)

    def test_named_link_data_type_inc(self):
        """Test get_subspec on a builder that maps to an named link."""
        link_spec = LinkSpec(doc='This Bar', target_type='Bar', name='bar_link')
        parent_spec = GroupSpec(
            doc='Something to hold a Bar',
            name='bar_bucket',
            links=[link_spec]
        )
        bar_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'Bar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        sub_builder = LinkBuilder(builder=bar_builder, name='bar_link')
        GroupBuilder(name='bar_bucket', links={'my_bar': sub_builder})
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, link_spec)

    def test_named_link_hierarchy_data_type_inc(self):
        """Test get_subspec on a builder that maps to an named link."""
        link_spec = LinkSpec(doc='This Bar', target_type='Bar', name='bar_link')
        parent_spec = GroupSpec(
            doc='Something to hold a Bar',
            name='bar_bucket',
            links=[link_spec]
        )
        bar_builder = GroupBuilder(
            name='my_bar',
            attributes={
                'data_type': 'SubBar',
                'namespace': CORE_NAMESPACE,
                'object_id': -1
            }
        )
        sub_builder = LinkBuilder(builder=bar_builder, name='bar_link')
        GroupBuilder(name='bar_bucket', links={'my_bar': sub_builder})
        result = self.type_map.get_subspec(parent_spec, sub_builder)
        self.assertIs(result, link_spec)


class TestTypeMap(TestCase):

    def setUp(self):
        self.bar_spec = GroupSpec('A test group specification with a data type', data_type_def='Bar')
        self.foo_spec = GroupSpec('A test group specification with data type Foo', data_type_def='Foo')
        self.spec_catalog = SpecCatalog()
        self.spec_catalog.register_spec(self.bar_spec, 'test.yaml')
        self.spec_catalog.register_spec(self.foo_spec, 'test.yaml')
        self.namespace = SpecNamespace('a test namespace', CORE_NAMESPACE, [{'source': 'test.yaml'}],
                                       version='0.1.0',
                                       catalog=self.spec_catalog)
        self.namespace_catalog = NamespaceCatalog()
        self.namespace_catalog.add_namespace(CORE_NAMESPACE, self.namespace)
        self.type_map = TypeMap(self.namespace_catalog)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Bar', Bar)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Foo', Foo)

    def test_get_map_unique_mappers(self):
        bar_inst = Bar('my_bar', list(range(10)), 'value1', 10)
        foo_inst = Foo(name='my_foo')
        bar_mapper = self.type_map.get_map(bar_inst)
        foo_mapper = self.type_map.get_map(foo_inst)
        self.assertIsNot(bar_mapper, foo_mapper)

    def test_get_map(self):
        container_inst = Bar('my_bar', list(range(10)), 'value1', 10)
        mapper = self.type_map.get_map(container_inst)
        self.assertIsInstance(mapper, ObjectMapper)
        self.assertIs(mapper.spec, self.bar_spec)
        mapper2 = self.type_map.get_map(container_inst)
        self.assertIs(mapper, mapper2)

    def test_get_map_register(self):
        class MyMap(ObjectMapper):
            pass
        self.type_map.register_map(Bar, MyMap)

        container_inst = Bar('my_bar', list(range(10)), 'value1', 10)
        mapper = self.type_map.get_map(container_inst)
        self.assertIs(mapper.spec, self.bar_spec)
        self.assertIsInstance(mapper, MyMap)


class BarMapper(ObjectMapper):
    def __init__(self, spec):
        super().__init__(spec)
        data_spec = spec.get_dataset('data')
        self.map_spec('attr2', data_spec.get_attribute('attr2'))


class TestMapStrings(TestCase):

    def customSetUp(self, bar_spec):
        spec_catalog = SpecCatalog()
        spec_catalog.register_spec(bar_spec, 'test.yaml')
        namespace = SpecNamespace('a test namespace', CORE_NAMESPACE, [{'source': 'test.yaml'}], version='0.1.0',
                                  catalog=spec_catalog)
        namespace_catalog = NamespaceCatalog()
        namespace_catalog.add_namespace(CORE_NAMESPACE, namespace)
        type_map = TypeMap(namespace_catalog)
        type_map.register_container_type(CORE_NAMESPACE, 'Bar', Bar)
        return type_map

    def test_build_1d(self):
        bar_spec = GroupSpec('A test group specification with a data type',
                             data_type_def='Bar',
                             datasets=[DatasetSpec('an example dataset', 'text', name='data', shape=(None,),
                                                   attributes=[AttributeSpec(
                                                       'attr2', 'an example integer attribute', 'int')])],
                             attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                                         AttributeSpec('attr_array', 'an example array attribute', 'text',
                                            shape=(None,))])
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        bar_inst = Bar('my_bar', ['a', 'b', 'c', 'd'], 'value1', 10, attr_array=['a', 'b', 'c', 'd'])
        builder = type_map.build(bar_inst)
        np.testing.assert_array_equal(builder.get('data').data, np.array(['a', 'b', 'c', 'd']))
        np.testing.assert_array_equal(builder.get('attr_array'), np.array(['a', 'b', 'c', 'd']))

    def test_build_scalar(self):
        bar_spec = GroupSpec('A test group specification with a data type',
                             data_type_def='Bar',
                             datasets=[DatasetSpec('an example dataset', 'text', name='data',
                                                   attributes=[AttributeSpec(
                                                       'attr2', 'an example integer attribute', 'int')])],
                             attributes=[AttributeSpec('attr1', 'an example string attribute', 'text')])
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        bar_inst = Bar('my_bar', ['a', 'b', 'c', 'd'], 'value1', 10)
        builder = type_map.build(bar_inst)
        self.assertEqual(builder.get('data').data, "['a', 'b', 'c', 'd']")

    def test_build_2d_lol(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        str_lol_2d = [['aa', 'bb'], ['cc', 'dd']]
        bar_inst = Bar('my_bar', str_lol_2d, 'value1', 10, attr_array=str_lol_2d)
        builder = type_map.build(bar_inst)
        self.assertEqual(builder.get('data').data, str_lol_2d)
        self.assertEqual(builder.get('attr_array'), str_lol_2d)

    def test_build_2d_ndarray(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        str_array_2d = np.array([['aa', 'bb'], ['cc', 'dd']])
        bar_inst = Bar('my_bar', str_array_2d, 'value1', 10, attr_array=str_array_2d)
        builder = type_map.build(bar_inst)
        np.testing.assert_array_equal(builder.get('data').data, str_array_2d)
        np.testing.assert_array_equal(builder.get('attr_array'), str_array_2d)

    def test_build_3d_lol(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        str_lol_3d = [[['aa', 'bb'], ['cc', 'dd']], [['ee', 'ff'], ['gg', 'hh']]]
        bar_inst = Bar('my_bar', str_lol_3d, 'value1', 10, attr_array=str_lol_3d)
        builder = type_map.build(bar_inst)
        self.assertEqual(builder.get('data').data, str_lol_3d)
        self.assertEqual(builder.get('attr_array'), str_lol_3d)

    def test_build_3d_ndarray(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        str_array_3d = np.array([[['aa', 'bb'], ['cc', 'dd']], [['ee', 'ff'], ['gg', 'hh']]])
        bar_inst = Bar('my_bar', str_array_3d, 'value1', 10, attr_array=str_array_3d)
        builder = type_map.build(bar_inst)
        np.testing.assert_array_equal(builder.get('data').data, str_array_3d)
        np.testing.assert_array_equal(builder.get('attr_array'), str_array_3d)

    @unittest.skipIf(not H5PY_3, "Use StrDataset only for h5py 3+")
    def test_build_1d_h5py_3_dataset(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, ),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, ))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        # create in-memory hdf5 file that is discarded after closing
        with h5py.File("test.h5", "w", driver="core", backing_store=False) as f:
            str_array_1d = np.array(
                ['aa', 'bb', 'cc', 'dd'],
                dtype=h5py.special_dtype(vlen=str)
            )
            # wrap the dataset in a StrDataset to mimic how HDF5IO would read this dataset with h5py 3+
            dataset = StrDataset(f.create_dataset('data', data=str_array_1d), None)
            bar_inst = Bar('my_bar', dataset, 'value1', 10, attr_array=dataset)
            builder = type_map.build(bar_inst)
            np.testing.assert_array_equal(builder.get('data').data, dataset[:])
            np.testing.assert_array_equal(builder.get('attr_array'), dataset[:])

    @unittest.skipIf(not H5PY_3, "Use StrDataset only for h5py 3+")
    def test_build_3d_h5py_3_dataset(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        # create in-memory hdf5 file that is discarded after closing
        with h5py.File("test.h5", "w", driver="core", backing_store=False) as f:
            str_array_3d = np.array(
                [[['aa', 'bb'], ['cc', 'dd']], [['ee', 'ff'], ['gg', 'hh']]],
                dtype=h5py.special_dtype(vlen=str)
            )
            # wrap the dataset in a StrDataset to mimic how HDF5IO would read this dataset with h5py 3+
            dataset = StrDataset(f.create_dataset('data', data=str_array_3d), None)
            bar_inst = Bar('my_bar', dataset, 'value1', 10, attr_array=dataset)
            builder = type_map.build(bar_inst)
            np.testing.assert_array_equal(builder.get('data').data, dataset[:])
            np.testing.assert_array_equal(builder.get('attr_array'), dataset[:])

    @unittest.skipIf(H5PY_3, "Create dataset differently for h5py < 3")
    def test_build_1d_h5py_2_dataset(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, ),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, ))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        # create in-memory hdf5 file that is discarded after closing
        with h5py.File("test.h5", "w", driver="core", backing_store=False) as f:
            str_array_1d = np.array(
                ['aa', 'bb', 'cc', 'dd'],
                dtype=h5py.special_dtype(vlen=str)
            )
            dataset = f.create_dataset('data', data=str_array_1d)
            bar_inst = Bar('my_bar', dataset, 'value1', 10, attr_array=dataset)
            builder = type_map.build(bar_inst)
            np.testing.assert_array_equal(builder.get('data').data, dataset[:])
            np.testing.assert_array_equal(builder.get('attr_array'), dataset[:])

    @unittest.skipIf(H5PY_3, "Create dataset differently for h5py < 3")
    def test_build_3d_h5py_2_dataset(self):
        bar_spec = GroupSpec(
            doc='A test group specification with a data type',
            data_type_def='Bar',
            datasets=[
                DatasetSpec(
                    doc='an example dataset',
                    dtype='text',
                    name='data',
                    shape=(None, None, None),
                    attributes=[AttributeSpec(name='attr2', doc='an example integer attribute', dtype='int')],
                )
            ],
            attributes=[AttributeSpec(name='attr_array', doc='an example array attribute', dtype='text',
                                      shape=(None, None, None))],
        )
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        # create in-memory hdf5 file that is discarded after closing
        with h5py.File("test.h5", "w", driver="core", backing_store=False) as f:
            str_array_3d = np.array(
                [[['aa', 'bb'], ['cc', 'dd']], [['ee', 'ff'], ['gg', 'hh']]],
                dtype=h5py.special_dtype(vlen=str)
            )
            dataset = f.create_dataset('data', data=str_array_3d)
            bar_inst = Bar('my_bar', dataset, 'value1', 10, attr_array=dataset)
            builder = type_map.build(bar_inst)
            np.testing.assert_array_equal(builder.get('data').data, dataset[:])
            np.testing.assert_array_equal(builder.get('attr_array'), dataset[:])

    def test_build_dataio(self):
        bar_spec = GroupSpec('A test group specification with a data type',
                             data_type_def='Bar',
                             datasets=[DatasetSpec('an example dataset', 'text', name='data', shape=(None,),
                                                   attributes=[AttributeSpec(
                                                       'attr2', 'an example integer attribute', 'int')])],
                             attributes=[AttributeSpec('attr1', 'an example string attribute', 'text')])
        type_map = self.customSetUp(bar_spec)
        type_map.register_map(Bar, BarMapper)
        bar_inst = Bar('my_bar', H5DataIO(['a', 'b', 'c', 'd'], chunks=True), 'value1', 10)
        builder = type_map.build(bar_inst)
        self.assertIsInstance(builder.get('data').data, H5DataIO)


class ObjectMapperMixin(metaclass=ABCMeta):

    def setUp(self):
        self.setUpBarSpec()
        self.spec_catalog = SpecCatalog()
        self.spec_catalog.register_spec(self.bar_spec, 'test.yaml')
        self.namespace = SpecNamespace('a test namespace', CORE_NAMESPACE,
                                       [{'source': 'test.yaml'}],
                                       version='0.1.0',
                                       catalog=self.spec_catalog)
        self.namespace_catalog = NamespaceCatalog()
        self.namespace_catalog.add_namespace(CORE_NAMESPACE, self.namespace)
        self.type_map = TypeMap(self.namespace_catalog)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Bar', Bar)
        self.manager = BuildManager(self.type_map)
        self.mapper = ObjectMapper(self.bar_spec)

    @abstractmethod
    def setUpBarSpec(self):
        raise NotImplementedError('Cannot run test unless setUpBarSpec is implemented')

    def test_default_mapping(self):
        attr_map = self.mapper.get_attr_names(self.bar_spec)
        keys = set(attr_map.keys())
        for key in keys:
            with self.subTest(key=key):
                self.assertIs(attr_map[key], self.mapper.get_attr_spec(key))
                self.assertIs(attr_map[key], self.mapper.get_carg_spec(key))


class TestObjectMapperNested(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec('A test group specification with a data type',
                                  data_type_def='Bar',
                                  datasets=[DatasetSpec('an example dataset', 'int', name='data',
                                                        attributes=[AttributeSpec(
                                                            'attr2', 'an example integer attribute', 'int')])],
                                  attributes=[AttributeSpec('attr1', 'an example string attribute', 'text')])

    def test_build(self):
        ''' Test default mapping functionality when object attributes map to an  attribute deeper
        than top-level Builder '''
        container_inst = Bar('my_bar', list(range(10)), 'value1', 10)
        expected = GroupBuilder(
            name='my_bar',
            datasets={'data': DatasetBuilder(
                name='data',
                data=list(range(10)),
                attributes={'attr2': 10}
            )},
            attributes={'attr1': 'value1'}
        )
        self._remap_nested_attr()
        builder = self.mapper.build(container_inst, self.manager)
        self.assertBuilderEqual(builder, expected)

    def test_construct(self):
        ''' Test default mapping functionality when object attributes map to an attribute
        deeper than top-level Builder '''
        expected = Bar('my_bar', list(range(10)), 'value1', 10)
        builder = GroupBuilder(
            name='my_bar',
            datasets={'data': DatasetBuilder(
                name='data',
                data=list(range(10)),
                attributes={'attr2': 10}
            )},
            attributes={'attr1': 'value1',
                        'data_type': 'Bar',
                        'namespace': CORE_NAMESPACE,
                        'object_id': expected.object_id}
        )
        self._remap_nested_attr()
        container = self.mapper.construct(builder, self.manager)
        self.assertEqual(container, expected)

    def test_default_mapping_keys(self):
        attr_map = self.mapper.get_attr_names(self.bar_spec)
        keys = set(attr_map.keys())
        expected = {'attr1', 'data', 'data__attr2'}
        self.assertSetEqual(keys, expected)

    def test_remap_keys(self):
        self._remap_nested_attr()
        self.assertEqual(self.mapper.get_attr_spec('attr2'),
                         self.mapper.spec.get_dataset('data').get_attribute('attr2'))
        self.assertEqual(self.mapper.get_attr_spec('attr1'), self.mapper.spec.get_attribute('attr1'))
        self.assertEqual(self.mapper.get_attr_spec('data'), self.mapper.spec.get_dataset('data'))

    def _remap_nested_attr(self):
        data_spec = self.mapper.spec.get_dataset('data')
        self.mapper.map_spec('attr2', data_spec.get_attribute('attr2'))


class TestObjectMapperNoNesting(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec('A test group specification with a data type',
                                  data_type_def='Bar',
                                  datasets=[DatasetSpec('an example dataset', 'int', name='data')],
                                  attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                                              AttributeSpec('attr2', 'an example integer attribute', 'int')])

    def test_build(self):
        ''' Test default mapping functionality when no attributes are nested '''
        container = Bar('my_bar', list(range(10)), 'value1', 10)
        builder = self.mapper.build(container, self.manager)
        expected = GroupBuilder('my_bar', datasets={'data': DatasetBuilder('data', list(range(10)))},
                                attributes={'attr1': 'value1', 'attr2': 10})
        self.assertBuilderEqual(builder, expected)

    def test_build_empty(self):
        ''' Test default mapping functionality when no attributes are nested '''
        container = Bar('my_bar', [], 'value1', 10)
        builder = self.mapper.build(container, self.manager)
        expected = GroupBuilder('my_bar', datasets={'data': DatasetBuilder('data', [])},
                                attributes={'attr1': 'value1', 'attr2': 10})
        self.assertBuilderEqual(builder, expected)

    def test_construct(self):
        expected = Bar('my_bar', list(range(10)), 'value1', 10)
        builder = GroupBuilder('my_bar', datasets={'data': DatasetBuilder('data', list(range(10)))},
                               attributes={'attr1': 'value1', 'attr2': 10, 'data_type': 'Bar',
                                           'namespace': CORE_NAMESPACE, 'object_id': expected.object_id})
        container = self.mapper.construct(builder, self.manager)
        self.assertEqual(container, expected)

    def test_default_mapping_keys(self):
        attr_map = self.mapper.get_attr_names(self.bar_spec)
        keys = set(attr_map.keys())
        expected = {'attr1', 'data', 'attr2'}
        self.assertSetEqual(keys, expected)


class TestObjectMapperContainer(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec('A test group specification with a data type',
                                  data_type_def='Bar',
                                  groups=[GroupSpec('an example group', data_type_def='Foo')],
                                  attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                                              AttributeSpec('attr2', 'an example integer attribute', 'int')])

    def test_default_mapping_keys(self):
        attr_map = self.mapper.get_attr_names(self.bar_spec)
        keys = set(attr_map.keys())
        expected = {'attr1', 'foo', 'attr2'}
        self.assertSetEqual(keys, expected)


class TestLinkedContainer(TestCase):

    def setUp(self):
        self.foo_spec = GroupSpec('A test group specification with data type Foo', data_type_def='Foo')
        self.bar_spec = GroupSpec('A test group specification with a data type Bar',
                                  data_type_def='Bar',
                                  groups=[self.foo_spec],
                                  datasets=[DatasetSpec('an example dataset', 'int', name='data')],
                                  attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                                              AttributeSpec('attr2', 'an example integer attribute', 'int')])

        self.spec_catalog = SpecCatalog()
        self.spec_catalog.register_spec(self.foo_spec, 'test.yaml')
        self.spec_catalog.register_spec(self.bar_spec, 'test.yaml')
        self.namespace = SpecNamespace('a test namespace', CORE_NAMESPACE,
                                       [{'source': 'test.yaml'}],
                                       version='0.1.0',
                                       catalog=self.spec_catalog)
        self.namespace_catalog = NamespaceCatalog()
        self.namespace_catalog.add_namespace(CORE_NAMESPACE, self.namespace)
        self.type_map = TypeMap(self.namespace_catalog)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Foo', Foo)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Bar', Bar)
        self.manager = BuildManager(self.type_map)
        self.foo_mapper = ObjectMapper(self.foo_spec)
        self.bar_mapper = ObjectMapper(self.bar_spec)

    def test_build_child_link(self):
        ''' Test default mapping functionality when one container contains a child link to another container '''
        foo_inst = Foo('my_foo')
        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10, foo=foo_inst)
        # bar_inst2.foo should link to bar_inst1.foo
        bar_inst2 = Bar('my_bar2', list(range(10)), 'value1', 10, foo=foo_inst)

        foo_builder = self.foo_mapper.build(foo_inst, self.manager)
        bar1_builder = self.bar_mapper.build(bar_inst1, self.manager)
        bar2_builder = self.bar_mapper.build(bar_inst2, self.manager)

        foo_expected = GroupBuilder('my_foo')

        inner_foo_builder = GroupBuilder('my_foo',
                                         attributes={'data_type': 'Foo',
                                                     'namespace': CORE_NAMESPACE,
                                                     'object_id': foo_inst.object_id})
        bar1_expected = GroupBuilder('my_bar1',
                                     datasets={'data': DatasetBuilder('data', list(range(10)))},
                                     groups={'foo': inner_foo_builder},
                                     attributes={'attr1': 'value1', 'attr2': 10})
        link_foo_builder = LinkBuilder(builder=inner_foo_builder)
        bar2_expected = GroupBuilder('my_bar2',
                                     datasets={'data': DatasetBuilder('data', list(range(10)))},
                                     links={'foo': link_foo_builder},
                                     attributes={'attr1': 'value1', 'attr2': 10})
        self.assertBuilderEqual(foo_builder, foo_expected)
        self.assertBuilderEqual(bar1_builder, bar1_expected)
        self.assertBuilderEqual(bar2_builder, bar2_expected)

    @unittest.expectedFailure
    def test_build_broken_link_parent(self):
        ''' Test that building a container with a broken link that has a parent raises an error. '''
        foo_inst = Foo('my_foo')
        Bar('my_bar1', list(range(10)), 'value1', 10, foo=foo_inst)  # foo_inst.parent is this bar
        # bar_inst2.foo should link to bar_inst1.foo
        bar_inst2 = Bar('my_bar2', list(range(10)), 'value1', 10, foo=foo_inst)

        # TODO bar_inst.foo.parent exists but is never built - this is a tricky edge case that should raise an error
        with self.assertRaises(OrphanContainerBuildError):
            self.bar_mapper.build(bar_inst2, self.manager)

    def test_build_broken_link_no_parent(self):
        ''' Test that building a container with a broken link that has no parent raises an error. '''
        foo_inst = Foo('my_foo')
        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10, foo=foo_inst)  # foo_inst.parent is this bar
        # bar_inst2.foo should link to bar_inst1.foo
        bar_inst2 = Bar('my_bar2', list(range(10)), 'value1', 10, foo=foo_inst)
        bar_inst1.remove_foo()

        msg = ("my_bar2 (my_bar2): Linked Foo 'my_foo' has no parent. Remove the link or ensure the linked container "
               "is added properly.")
        with self.assertRaisesWith(OrphanContainerBuildError, msg):
            self.bar_mapper.build(bar_inst2, self.manager)


class TestReference(TestCase):

    def setUp(self):
        self.foo_spec = GroupSpec('A test group specification with data type Foo', data_type_def='Foo')
        self.bar_spec = GroupSpec('A test group specification with a data type Bar',
                                  data_type_def='Bar',
                                  datasets=[DatasetSpec('an example dataset', 'int', name='data')],
                                  attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                                              AttributeSpec('attr2', 'an example integer attribute', 'int'),
                                              AttributeSpec('foo', 'a referenced foo', RefSpec('Foo', 'object'),
                                                            required=False)])

        self.spec_catalog = SpecCatalog()
        self.spec_catalog.register_spec(self.foo_spec, 'test.yaml')
        self.spec_catalog.register_spec(self.bar_spec, 'test.yaml')
        self.namespace = SpecNamespace('a test namespace', CORE_NAMESPACE,
                                       [{'source': 'test.yaml'}],
                                       version='0.1.0',
                                       catalog=self.spec_catalog)
        self.namespace_catalog = NamespaceCatalog()
        self.namespace_catalog.add_namespace(CORE_NAMESPACE, self.namespace)
        self.type_map = TypeMap(self.namespace_catalog)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Foo', Foo)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Bar', Bar)
        self.manager = BuildManager(self.type_map)
        self.foo_mapper = ObjectMapper(self.foo_spec)
        self.bar_mapper = ObjectMapper(self.bar_spec)

    def test_build_attr_ref(self):
        ''' Test default mapping functionality when one container contains an attribute reference to another container.
        '''
        foo_inst = Foo('my_foo')
        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10, foo=foo_inst)
        bar_inst2 = Bar('my_bar2', list(range(10)), 'value1', 10)

        foo_builder = self.manager.build(foo_inst, root=True)
        bar1_builder = self.manager.build(bar_inst1, root=True)  # adds refs
        bar2_builder = self.manager.build(bar_inst2, root=True)

        foo_expected = GroupBuilder('my_foo',
                                    attributes={'data_type': 'Foo',
                                                'namespace': CORE_NAMESPACE,
                                                'object_id': foo_inst.object_id})
        bar1_expected = GroupBuilder('n/a',  # name doesn't matter
                                     datasets={'data': DatasetBuilder('data', list(range(10)))},
                                     attributes={'attr1': 'value1',
                                                 'attr2': 10,
                                                 'foo': ReferenceBuilder(foo_expected),
                                                 'data_type': 'Bar',
                                                 'namespace': CORE_NAMESPACE,
                                                 'object_id': bar_inst1.object_id})
        bar2_expected = GroupBuilder('n/a',  # name doesn't matter
                                     datasets={'data': DatasetBuilder('data', list(range(10)))},
                                     attributes={'attr1': 'value1',
                                                 'attr2': 10,
                                                 'data_type': 'Bar',
                                                 'namespace': CORE_NAMESPACE,
                                                 'object_id': bar_inst2.object_id})
        self.assertDictEqual(foo_builder, foo_expected)
        self.assertDictEqual(bar1_builder, bar1_expected)
        self.assertDictEqual(bar2_builder, bar2_expected)

    def test_build_attr_ref_invalid(self):
        ''' Test default mapping functionality when one container contains an attribute reference to another container.
        '''
        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        bar_inst1._Bar__foo = object()  # make foo object a non-container type

        msg = "invalid type for reference 'foo' (<class 'object'>) - must be AbstractContainer"
        with self.assertRaisesWith(ValueError, msg):
            self.bar_mapper.build(bar_inst1, self.manager)


class TestMissingRequiredAttribute(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            attributes=[AttributeSpec('attr1', 'an example string attribute', 'text'),
                        AttributeSpec('attr2', 'an example integer attribute', 'int')]
        )

    def test_required_attr_missing(self):
        """Test mapping when one container is missing a required attribute."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        bar_inst1._Bar__attr1 = None  # make attr1 attribute None

        msg = "Bar 'my_bar1' is missing required value for attribute 'attr1'."
        with self.assertWarnsWith(MissingRequiredBuildWarning, msg):
            builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
            attributes={'attr2': 10}
        )
        self.assertBuilderEqual(expected, builder)


class TestMissingRequiredAttributeRef(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            attributes=[AttributeSpec('foo', 'a referenced foo', RefSpec('Foo', 'object'))]
        )

    def test_required_attr_ref_missing(self):
        """Test mapping when one container is missing a required attribute reference."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)

        msg = "Bar 'my_bar1' is missing required value for attribute 'foo'."
        with self.assertWarnsWith(MissingRequiredBuildWarning, msg):
            builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
        )
        self.assertBuilderEqual(expected, builder)


class TestMissingRequiredDataset(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            datasets=[DatasetSpec('an example dataset', 'int', name='data')]
        )

    def test_required_dataset_missing(self):
        """Test mapping when one container is missing a required dataset."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        bar_inst1._Bar__data = None  # make data dataset None

        msg = "Bar 'my_bar1' is missing required value for attribute 'data'."
        with self.assertWarnsWith(MissingRequiredBuildWarning, msg):
            builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
        )
        self.assertBuilderEqual(expected, builder)


class TestMissingRequiredGroup(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            groups=[GroupSpec('foo', data_type_inc='Foo')]
        )

    def test_required_group_missing(self):
        """Test mapping when one container is missing a required group."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        msg = "Bar 'my_bar1' is missing required value for attribute 'foo'."
        with self.assertWarnsWith(MissingRequiredBuildWarning, msg):
            builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
        )
        self.assertBuilderEqual(expected, builder)


class TestRequiredEmptyGroup(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            groups=[GroupSpec(name='empty', doc='empty group')],
        )

    def test_required_group_empty(self):
        """Test mapping when one container has a required empty group."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
            groups={'empty': GroupBuilder('empty')},
        )
        self.assertBuilderEqual(expected, builder)


class TestOptionalEmptyGroup(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            groups=[GroupSpec(
                name='empty',
                doc='empty group',
                quantity='?',
                attributes=[AttributeSpec('attr3', 'an optional float attribute', 'float', required=False)]
            )]
        )

    def test_optional_group_empty(self):
        """Test mapping when one container has an optional empty group."""

        self.mapper.map_spec('attr3', self.mapper.spec.get_group('empty').get_attribute('attr3'))

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)
        bar_inst1._Bar__attr3 = None  # force attr3 to be None
        builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
        )
        self.assertBuilderEqual(expected, builder)

    def test_optional_group_not_empty(self):
        """Test mapping when one container has an optional not empty group."""

        self.mapper.map_spec('attr3', self.mapper.spec.get_group('empty').get_attribute('attr3'))

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10, attr3=1.23)
        builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
            groups={'empty': GroupBuilder(
                name='empty',
                attributes={'attr3': 1.23},
            )},
        )
        self.assertBuilderEqual(expected, builder)


class TestFixedAttributeValue(ObjectMapperMixin, TestCase):

    def setUpBarSpec(self):
        self.bar_spec = GroupSpec(
            doc='A test group specification with a data type Bar',
            data_type_def='Bar',
            attributes=[AttributeSpec('attr1', 'an example string attribute', 'text', value='hi'),
                        AttributeSpec('attr2', 'an example integer attribute', 'int')]
        )

    def test_required_attr_missing(self):
        """Test mapping when one container has a required attribute with a fixed value."""

        bar_inst1 = Bar('my_bar1', list(range(10)), 'value1', 10)  # attr1=value1 is not processed
        builder = self.mapper.build(bar_inst1, self.manager)

        expected = GroupBuilder(
            name='my_bar1',
            attributes={'attr1': 'hi', 'attr2': 10}
        )
        self.assertBuilderEqual(builder, expected)


class TestObjectMapperBadValue(TestCase):

    def test_bad_value(self):
        """Test that an error is raised if the container attribute value for a spec with a data type is not a container
        or collection of containers.
        """
        class Qux(Container):
            @docval({'name': 'name', 'type': str, 'doc': 'the name of this Qux'},
                    {'name': 'foo', 'type': int, 'doc': 'a group'})
            def __init__(self, **kwargs):
                name, foo = getargs('name', 'foo', kwargs)
                super().__init__(name=name)
                self.__foo = foo
                if isinstance(foo, Foo):
                    self.__foo.parent = self

            @property
            def foo(self):
                return self.__foo

        self.qux_spec = GroupSpec(
            doc='A test group specification with data type Qux',
            data_type_def='Qux',
            groups=[GroupSpec('an example dataset', data_type_inc='Foo')]
        )
        self.foo_spec = GroupSpec('A test group specification with data type Foo', data_type_def='Foo')
        self.spec_catalog = SpecCatalog()
        self.spec_catalog.register_spec(self.qux_spec, 'test.yaml')
        self.spec_catalog.register_spec(self.foo_spec, 'test.yaml')
        self.namespace = SpecNamespace('a test namespace', CORE_NAMESPACE, [{'source': 'test.yaml'}],
                                       version='0.1.0',
                                       catalog=self.spec_catalog)
        self.namespace_catalog = NamespaceCatalog()
        self.namespace_catalog.add_namespace(CORE_NAMESPACE, self.namespace)
        self.type_map = TypeMap(self.namespace_catalog)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Qux', Qux)
        self.type_map.register_container_type(CORE_NAMESPACE, 'Foo', Foo)
        self.manager = BuildManager(self.type_map)
        self.mapper = ObjectMapper(self.qux_spec)

        container = Qux('my_qux', foo=1)
        msg = "Qux 'my_qux' attribute 'foo' has unexpected type."
        with self.assertRaisesWith(ContainerConfigurationError, msg):
            self.mapper.build(container, self.manager)

    # TODO test passing a Container/Data/other object for a non-container/data array spec
