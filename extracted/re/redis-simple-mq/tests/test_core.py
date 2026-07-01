import unittest

from redis import Redis

from simple_mq import SimpleMQ


class TestPQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.conn = Redis()
        cls.q = SimpleMQ(cls.conn)

    def setUp(self):
        self.q.clear()

    def test_create_queue_with_custom_name(self):
        q = SimpleMQ(self.conn, "my_own_name")
        self.assertEqual(q.name, "my_own_name")

    def test_init_with_wrong_conn_type(self):
        with self.assertRaises(TypeError):
            SimpleMQ("xxx", "yyy")  # type: ignore

    def test_empty_queue_returns_none(self):
        self.assertIsNone(self.q.dequeue())

    def test_empty_queue_has_length_0(self):
        self.assertEqual(self.q.size(), 0)

    def test_queue_dequeue_one_empty(self):
        x = "precious"
        self.assertEqual(self.q.enqueue(x), 1)
        self.assertEqual(self.q.size(), 1)
        y = self.q.dequeue()
        self.assertEqual(x, y)

    def test_enqueue_many(self):
        self.assertEqual(self.q.enqueue("dummy_100"), 1)
        self.assertEqual(self.q.enqueue("dummy_101"), 2)
        self.assertEqual(self.q.enqueue("dummy_102"), 3)
        self.assertEqual(self.q.size(), 3)

    def test_queue_dequeue_many(self):
        x_list = ["apple", "kiwi", "lemon"]
        for x in x_list:
            self.q.enqueue(x)
        self.assertEqual(self.q.size(), len(x_list))

        y_list = list()
        while True:
            y = self.q.dequeue()
            if y is not None:
                y_list.append(y)
            else:
                break

        self.assertListEqual(x_list, y_list)

    def test_enqueue_bulk(self):
        x_list = ["apple", "kiwi", "lemon"]
        self.q.enqueue_bulk(x_list)

        y_list = list()
        while True:
            y = self.q.dequeue()
            if y is not None:
                y_list.append(y)
            else:
                break

        self.assertListEqual(x_list, y_list)

    def test_dequeue_bulk_normal(self):
        x_list = ["apple", "kiwi", "lemon"]
        self.q.enqueue_bulk(x_list)
        y_list = self.q.dequeue_bulk()
        self.assertListEqual(x_list, y_list)

    def test_dequeue_bulk_empty_queue(self):
        self.assertListEqual(self.q.dequeue_bulk(), [])

    def test_dequeue_bulk_limited(self):
        x_list = ["apple", "kiwi", "lemon"]
        self.q.enqueue_bulk(x_list)
        y_list = self.q.dequeue_bulk(2)
        self.assertListEqual(x_list[:2], y_list)

    def test_dequeue_bulk_error(self):
        x_list = ["apple", "kiwi", "lemon"]
        self.q.enqueue_bulk(x_list)
        with self.assertRaises(ValueError):
            self.q.dequeue_bulk(-1)

    def test_clear_full_queue(self):
        self.q.enqueue("dummy_100")
        self.q.enqueue("dummy_100")
        self.assertEqual(self.q.size(), 2)

        result = self.q.clear()

        self.assertEqual(result, 2)
        self.assertEqual(self.q.size(), 0)

    def test_clear_empty_queue(self):
        self.assertEqual(self.q.size(), 0)

        result = self.q.clear()

        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
