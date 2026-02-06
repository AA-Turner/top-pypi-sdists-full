from concurrent.futures import as_completed
import threading
import time
import unittest

from adam.config import Config
from adam.utils import clear_wait_log_flag, parallelize, ing, log2, log_timing, offload, wait_log

class TestUtils(unittest.TestCase):
    Config()

    # def test_ing(self):
    #     inner_body_called = [False]

    #     def set_inner_body_called():
    #         inner_body_called[0] = True

    #     with ing('outer'):
    #         ing('inner', set_inner_body_called)

    #     self.assertTrue(inner_body_called[0])

    # def test_log2(self):
    #     with ing('outer'):
    #         self.assertFalse(log2('hello'))

    # def test_log_timing(self):
    #     Config().set('debugs.timings', 'true')

    #     with log_timing('outer-most'):
    #         with log_timing('outer'):
    #             with log_timing('inner1'):
    #                 print('inside1')
    #             with log_timing('inner2'):
    #                 print('inside2')
    #             time.sleep(1)

    # def test_log_timing2(self):
    #     Config().set('debugs.timings', 'true')

    #     with log_timing('outer-most'):
    #         with log_timing('outer'):
    #             log_timing('inner1', lambda: print('inside1'))
    #             log_timing('inner2', lambda: print('inside2'))
    #             time.sleep(1)

    # def test_log_timing3(self):
    #     Config().set('debugs.timings', 'true')

    #     log_timing('inner1-s0', s0=time.time())

    # def test_wait_log(self):
    #     wait_log('wait1')
    #     wait_log('wait1-1')
    #     clear_wait_log_flag()
    #     wait_log('wait2')

    # def test_parallel0(self):
    #     words = []

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'a:{a}, b:{b}')

    #             return b

    #         with parallel(len(words), 8) as (submit, collect):
    #             return collect([submit(fn, '1', word) for word in words])

    #     self.assertEqual(words, xyz())

    # def test_parallel1(self):
    #     words = ['hello']

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'a:{a}, b:{b}')

    #             return b

    #         with parallel(len(words), 8) as (submit, collect):
    #             return collect([submit(fn, '1', word) for word in words])

    #     self.assertEqual(words, xyz())

    # def test_parallel(self):
    #     words = ['hello', 'world']

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'a:{a}, b:{b}')
    #             return b

    #         with parallel_collect(words, 8, msg='Exporting|Exported {size} Cassandra tables') as (submit, collect):
    #             return collect([submit(fn, '1', word) for word in words])

    #     self.assertEqual(set(words), set(xyz()))

    # def test_parallel_sampling(self):
    #     words = ['hello', 'world', 'or', 'hi', 'universe']

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'a:{a}, b:{b}')
    #             return b

    #         with parallel_collect(words, 8, samples=3, msg='Exporting|Exported {size} Cassandra tables') as (submit, collect):
    #             return collect([submit(fn, '1', word) for word in words])

    #     self.assertEqual(set(words[:3]), set(xyz()))

    def test_offloaded(self):
        def xyz():
            def fn(a: str, b: str):
                print(f'a:{a}, b:{b}')
                return b

            with offload(3, msg='Begin|End') as exec:
                return [exec.submit(lambda: fn('1', 'offloaded'))]

        self.assertEqual(['offloaded'], [f.result() for f in as_completed(xyz())])

    # def test_parallel_map(self):
    #     words = ['hello', 'world', 'or', 'hi', 'universe']

    #     def xyz():
    #         def fn(b: str):
    #             print(f'b:{b}')
    #             return b

    #         with parallel_map(words, 3, msg='Exporting|Exported {size} Cassandra tables') as map:
    #             return map(fn, words)

    #     self.assertEqual(set(words), set(xyz()))

    # def test_concurrent_map_serially(self):
    #     words = ['hello', 'world', 'or', 'hi', 'universe']

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'{threading.get_ident()}: a:{a}, b:{b}')
    #             time.sleep(1)
    #             return b

    #         with concurrent_map(words, 1, msg='Exporting|Exported {size} Cassandra tables') as map:
    #             return map(lambda b: fn('constant', b))

    #     self.assertEqual(set(words), set(xyz()))

    # def test_concurrent_map_serially(self):
    #     words = ['hello', 'world', 'or', 'hi', 'universe']

    #     def xyz():
    #         def fn(a: str, b: str):
    #             print(f'{threading.get_ident()}: a:{a}, b:{b}')
    #             time.sleep(1)
    #             return b

    #         with concurrent_map(words, 1, msg='Exporting|Exported {size} Cassandra tables') as map:
    #             return map(lambda b: fn('constant', b))

    #     self.assertEqual(set(words), set(xyz()))

if __name__ == '__main__':
    unittest.main()