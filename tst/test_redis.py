#!/usr/bin/env python

import unittest
import time

from tst.test_utility import *
from redis_process import RedisProcess
from redis_deserializer import *

class TestRedis(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    def test_PING(self):
        input = generate_input(['PING'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_simple_string("PONG"))

    def test_ECHO(self):
        input = generate_input(['echo', 'hello world'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_simple_string("hello world"))

