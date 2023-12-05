#!/usr/bin/env python

import unittest

from redis_process import RedisProcess
from redis_deserializer import *
from tst.test_utility import *

class TestRedisBenchmark(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    def test_redis_benchmark_set_get(self):
        input = generate_input(['SET', 'key:__rand_int__', 'xxx'])
        self.rp.set_command(input)

        input = generate_input(['get', 'key:__rand_int__'])
        self.rp.set_command(input)
        self.rp.set_command(input)
        self.rp.set_command(input)
        out = self.rp.set_command(input)

        self.assertEqual(out, b'+xxx\r\n')
 