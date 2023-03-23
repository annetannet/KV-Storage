import unittest
import kv_stor
import os
from unittest.mock import MagicMock
import builtins


class TestKVS(unittest.TestCase):
    db_sample = 'sample_db.txt'
    db_copies = 'sample2.txt'
    kvs = kv_stor.KVS()

    def setUp(self) -> None:
        self.kvs.create_file(self.db_sample)
        self.kvs.create_file(self.db_copies)

    def tearDown(self) -> None:
        os.remove(f"{os.getcwd()}/{self.db_sample}")
        os.remove(f"{os.getcwd()}/{self.db_copies}")

    def test_create_file(self):
        data = self.kvs.read_database(db=self.db_sample)

        self.assertEqual(data, '')

    def test_no_data(self):
        data = self.kvs.read_database(db=self.db_sample)

        self.assertEqual(data, '')

    def test_key_not_in_data(self):
        self.kvs.write_database(key='key', value='value', db=[self.db_sample])
        value = self.kvs.read_database(key='k', db=self.db_sample)

        self.assertEqual(value, None)

    def test_key_in_data(self):
        self.kvs.write_database(key='key', value='value', db=[self.db_sample])
        value = self.kvs.read_database(key='key', db=self.db_sample)

        self.assertEqual(value, "value")

    def test_write_values_in_data(self):
        self.kvs.write_database(key='key1', value='val1', db=[self.db_sample])
        self.kvs.write_database(key='key2', value='val2', db=[self.db_sample])
        value1 = self.kvs.read_database(key='key1', db=self.db_sample)
        value2 = self.kvs.read_database(key='key2', db=self.db_sample)

        self.assertEqual(value1, "val1")
        self.assertEqual(value2, "val2")

    def test_new_value(self):
        self.kvs.write_database(key='key1', value='val1', db=[self.db_sample])
        self.kvs.write_database(key='key1', value='new', db=[self.db_sample])
        new = self.kvs.read_database(key='key1', db=self.db_sample)

        self.assertNotEqual(new, "val1")
        self.assertEqual(new, "new")

    def test_new_values(self):
        self.kvs.write_database(key='key1', value='val1', db=[self.db_sample])
        self.kvs.write_database(key='key2', value='val2', db=[self.db_sample])
        self.kvs.write_database(key='key1', value='new1', db=[self.db_sample])
        self.kvs.write_database(key='key2', value='new2', db=[self.db_sample])
        new1 = self.kvs.read_database(key='key1', db=self.db_sample)
        new2 = self.kvs.read_database(key='key2', db=self.db_sample)

        self.assertEqual(new1, "new1")
        self.assertEqual(new2, "new2")

    def test_write_pairs_in_data(self):
        attrs = self.kvs.parser.parse_args(['-k', 'key1', 'key2', 'key3',
                                            '-v', 'val1', 'val2', 'val3',
                                            '-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        data = self.kvs.read_database(db=self.db_sample)
        self.assertEqual('{"key1": "val1", "key2": "val2",'
                         ' "key3": "val3"}', data)

    def test_not_equal_keys_values_lengths(self):
        builtins.print = MagicMock()
        attrs = self.kvs.parser.parse_args(['-k', 'key1', 'key2', 'key3',
                                            '-v', 'val1',
                                            '-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        builtins.print.assert_called_with(
            'Invalid input. For one key, one value')

    def test_read_empty_db(self):
        builtins.print = MagicMock()
        attrs = self.kvs.parser.parse_args(['-k', 'key1', 'key2', 'key3',
                                            '-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        builtins.print.assert_called_with(None)

    def test_try_read_key_not_in_db(self):
        self.kvs.write_database(key='key', value='value', db=[self.db_sample])
        builtins.print = MagicMock()
        attrs = self.kvs.parser.parse_args(['-k', 'key1',
                                            '-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        db = self.kvs.read_database(db=self.db_sample)
        builtins.print.assert_called_with(None)
        self.assertEqual('{"key": "value"}', db)

    def test_try_read_key_in_db(self):
        self.kvs.write_database(key='key', value='value', db=[self.db_sample])
        builtins.print = MagicMock()
        attrs = self.kvs.parser.parse_args(['-k', 'key',
                                            '-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        builtins.print.assert_called_with('value')

    def test_invalid_input(self):
        builtins.print = MagicMock()
        attrs = self.kvs.parser.parse_args(['-f', 'sample_db.txt'])
        self.kvs.run(attrs)
        builtins.print.assert_called_with('Invalid input')

    def test_copies_db(self):
        attrs = self.kvs.parser.parse_args(['-k', 'key1', 'key2', 'key3',
                                            '-v', 'val1', 'val2', 'val3',
                                            '-f', 'sample_db.txt',
                                            'sample2.txt'])
        self.kvs.run(attrs)
        data = self.kvs.read_database(db='sample_db.txt')

        with open('sample2.txt', 'r') as f2:
            self.assertEqual(data, f2.read())


if __name__ == '__main__':
    unittest.main()
