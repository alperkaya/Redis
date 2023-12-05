#!/usr/bin/env python

import unittest

from tst.test_utility import *
from redis_process import RedisProcess
from redis_deserializer import *

class TestRedisINCR(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    # def test_INCR_1(self):
    #     input = generate_input(['set', 'mykey', '10'])
    #     self.rp.set_command(input)

    #     input = generate_input(['INCR', 'mykey'])
    #     out = self.rp.set_command(input)

    #     self.assertEqual(out, deserialize_integer('11'))

    