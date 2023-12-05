#!/usr/bin/env python

import unittest

from tst.test_utility import *
from redis_process import RedisProcess
from redis_deserializer import *

class TestRedisDEL(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    def test_DEL_1(self):
        input = generate_input(['set', 'key1', 'John'])
        self.rp.set_command(input)

        input = generate_input(['DEL', 'key1'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('1'))

    def test_EXISTS_2(self):
        input = generate_input(['set', 'key1', 'John'])
        self.rp.set_command(input)
        input = generate_input(['set', 'key2', 'John'])
        self.rp.set_command(input)

        input = generate_input(['DEL', 'key1', 'key2'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('2'))

    def test_EXISTS_no_result(self):
        input = generate_input(['DEL', 'Name'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('0'))
   