#!/usr/bin/env python

import unittest

from tst.test_utility import *
from redis_process import RedisProcess
from redis_deserializer import *

class TestRedisEXISTS(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    def test_EXISTS_1(self):
        input = generate_input(['set', 'Name', 'John'])
        self.rp.set_command(input)

        input = generate_input(['EXISTS', 'Name'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('1'))

    def test_EXISTS_2(self):
        input = generate_input(['set', 'Name', 'John'])
        self.rp.set_command(input)

        input = generate_input(['EXISTS', 'Name', 'Name'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('2'))

    def test_EXISTS_no_result(self):
        input = generate_input(['EXISTS', 'Name'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_integer('0'))
   