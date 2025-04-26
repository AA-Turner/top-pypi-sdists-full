import time
import unittest

from django.conf import settings
from django.core.files.base import ContentFile
from django.test.utils import override_settings

from inmemorystorage import InMemoryStorage
from inmemorystorage.storage import InMemoryDir, InMemoryFile, PathDoesNotExist


class MemoryStorageTests(unittest.TestCase):
    def setUp(self):
        if not settings.configured:
            settings.configure(MEDIA_URL='')
        self.storage = InMemoryStorage()
        self.filesystem = self.storage.filesystem

    def test_listdir(self):
        self.assertEqual(self.storage.listdir(''), [[], []])

        self.filesystem.add_child('dir0', InMemoryDir())
        self.filesystem.add_child('file0', InMemoryFile())

        self.assertEqual(self.storage.listdir(''), [['dir0'], ['file0']])
        self.assertEqual(self.storage.listdir('dir0'), [[], []])

        self.filesystem.resolve('dir0').add_child('subdir', InMemoryDir())
        self.assertEqual(self.storage.listdir('dir0'), [['subdir'], []])
        self.assertEqual(self.storage.listdir('dir0/subdir'), [[], []])

    def test_delete(self):
        self.filesystem.add_child('dir0', InMemoryDir())
        self.filesystem.resolve('dir0').add_child('nested_file', InMemoryFile())
        self.filesystem.add_child('file0', InMemoryFile())
        self.assertEqual(self.filesystem.resolve('dir0').ls(), ['nested_file'])

        self.storage.delete('dir0/nested_file')
        self.assertEqual(self.filesystem.resolve('dir0').ls(), [])
        self.assertEqual(set(self.filesystem.ls()), set(['dir0', 'file0']))

        self.storage.delete('dir0')
        self.assertEqual(set(self.filesystem.ls()), set(['file0']))

    def test_exists(self):
        self.filesystem.add_child('file0', InMemoryFile())
        self.assertTrue(self.storage.exists('file0'))
        self.assertFalse(self.storage.exists('file1'))
        self.storage.delete('file0')
        self.assertFalse(self.storage.exists('file0'))

    def test_size(self):
        self.filesystem.add_child('file0', InMemoryFile('test'))
        self.assertEqual(self.storage.size('file0'), 4)

    def test_save(self):
        self.storage.save('file', ContentFile('test'))
        self.assertEqual(self.storage.size('file'), 4)
        self.storage.save('subdir/file', ContentFile('test'))
        self.assertEqual(self.storage.size('subdir/file'), 4)
        self.storage.save('bytes_file', ContentFile(b'test'))
        self.assertEqual(self.storage.size('bytes_file'), 4)

    def test_write(self):
        with self.storage.open("file", "w") as f:
            f.write("hello")
        with self.storage.open("file", "r") as f:
            self.assertEqual(f.read(), "hello")

    def test_missing(self):
        missing_file_name = "missing-file"
        with self.assertRaises(PathDoesNotExist) as context_manager:
            self.storage.open(missing_file_name, "r")
            self.assertEqual(context_manager.exception.args, (missing_file_name,))

    def test_all(self):
        self.assertEqual(self.storage.listdir('/'), [[], []])
        self.assertEqual(self.storage.save('dir/subdir/file', ContentFile('testing')), 'dir/subdir/file')
        self.assertEqual(self.storage.listdir('/'), [['dir'], []])
        self.assertEqual(self.storage.listdir('dir/'), [['subdir'], []])
        self.assertEqual(self.storage.save('dir/subdir/file2', ContentFile('testing2')), 'dir/subdir/file2')
        self.assertEqual(self.storage.save('file', ContentFile('testing3')), 'file')
        self.assertEqual(self.storage.listdir('/'), [['dir'], ['file']])
        self.assertEqual(self.storage.listdir('dir/'), [['subdir'], []])
        self.assertEqual(self.storage.open('dir/subdir/file').read(), 'testing')
        self.assertEqual(self.storage.size('dir/subdir/file'), 7)
        self.assertEqual(self.storage.size('dir/subdir/file2'), 8)
        self.assertEqual(self.storage.size('file'), 8)
        self.assertEqual(self.storage.delete('file'), None)
        self.assertEqual(self.storage.listdir('/'), [['dir'], []])
        self.assertEqual(self.storage.delete('dir/subdir/file'), None)
        self.assertEqual(self.storage.listdir('dir/subdir'), [[], ['file2']])
        self.assertEqual(self.storage.exists('dir/subdir/file2'), True)
        self.assertEqual(self.storage.delete('dir/subdir/file2'), None)
        self.assertEqual(self.storage.exists('dir/subdir/file2'), False)
        self.assertEqual(self.storage.listdir('dir/subdir'), [[], []])

    @override_settings(MEDIA_URL=None)
    def test_url(self):
        # main storage not instantiated with a base url so should raise not
        # implemented.
        storage = InMemoryStorage()

        self.assertRaises(ValueError, storage.url, ('file0',))

        storage = InMemoryStorage(base_url='http://www.example.com')

        self.assertEqual(storage.url('file0'), 'http://www.example.com/file0')

    def test_modified_time(self):
        self.storage.save('file', ContentFile('test'))
        modified_time = self.storage.modified_time('file')

        self.storage.delete('file')

        time.sleep(0.1)

        self.storage.save('file', ContentFile('test-again'))
        new_modified_time = self.storage.modified_time('file')
        self.assertTrue(new_modified_time > modified_time)

    def test_accessed_time(self):
        self.storage.save('file', ContentFile('test'))

        self.storage.open('file', 'r')
        accessed_time = self.storage.accessed_time('file')

        time.sleep(0.1)

        self.storage.open('file', 'r')
        new_accessed_time = self.storage.accessed_time('file')
        self.assertTrue(new_accessed_time > accessed_time)

    def test_created_time(self):
        self.storage.save('file', ContentFile('test'))
        created_time = self.storage.created_time('file')

        time.sleep(0.1)

        # make sure opening it doesn't change creation time.
        file = self.storage.open('file', 'r')

        after_open_created_time = self.storage.created_time('file')
        self.assertEqual(after_open_created_time, created_time)

        # make sure writing to it doesn't change creation time.
        file.write('test-test-test')
        self.storage.save('file', file)

        after_write_created_time = self.storage.created_time('file')
        self.assertEqual(after_write_created_time, created_time)

    @override_settings(INMEMORYSTORAGE_PERSIST=True)
    def test_persistance(self):
        storage_a = InMemoryStorage()
        storage_b = InMemoryStorage()

        # Can't use self.assertIs because it isn't available in Python 2.6
        self.assertTrue(storage_a.filesystem is storage_b.filesystem)

    def test_no_persistance_without_setting(self):
        storage_a = InMemoryStorage()
        storage_b = InMemoryStorage()

        # Can't use self.assertIs because it isn't available in Python 2.6
        self.assertTrue(storage_a.filesystem is not storage_b.filesystem)


if __name__ == '__main__':
    unittest.main()
