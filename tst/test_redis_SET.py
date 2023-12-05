#!/usr/bin/env python

import unittest
import time

from tst.test_utility import *
from redis_process import RedisProcess
from redis_deserializer import *

class TestRedisSET(unittest.TestCase):

    def setUp(self) -> None:
        self.rp = RedisProcess()

    def test_set_KEY_VALUE(self):
        input = generate_input(['set', 'Name', 'John'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_simple_string('OK'))

    def test_get_KEY_VALUE(self):
        input = generate_input(['set', 'Name', 'John'])
        self.rp.set_command(input)

        input = generate_input(['get', 'Name'])
        out = self.rp.set_command(input)

        self.assertEqual(out, deserialize_simple_string('John'))
    
    def test_redis_benchmark_set_get(self):
        input = generate_input(['SET', 'key:__rand_int__', 'xxx'])
        self.rp.set_command(input)

        input = generate_input(['get', 'key:__rand_int__'])
        out = self.rp.set_command(input)
        out = self.rp.set_command(input)
        out = self.rp.set_command(input)

        self.assertEqual(out, b'+xxx\r\n')
    
    def test_not_expired(self):
        input = generate_input(['SET', 'key', 'xxx', 'EX', '11'])
        self.rp.set_command(input)

        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string('xxx'))

    def test_expire_sec(self):
        input = generate_input(['SET', 'key', 'xxx', 'EX', '1'])
        self.rp.set_command(input)

        time.sleep(2)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string(''))

    def test_expire_msec(self):
        input = generate_input(['SET', 'key', 'xxx', 'PX', '1'])
        self.rp.set_command(input)

        time.sleep(1)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string(''))

    def test_not_expired_unixtimestamp_sec(self):
        now_plus_5_sec = time.time() + 5
        input = generate_input(['SET', 'key', 'xxx', 'EAXT', str(now_plus_5_sec)])
        self.rp.set_command(input)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string('xxx'))
    
    def test_expired_unixtimestamp_sec(self):
        now_minus_1_sec = time.time() - 1
        input = generate_input(['SET', 'key', 'xxx', 'EAXT', str(now_minus_1_sec)])
        self.rp.set_command(input)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string(''))

    def test_not_expired_unixtimestamp_msec(self):
        now_plus_5_sec = time.time()*1000 + 5
        input = generate_input(['SET', 'key', 'xxx', 'PXAT', str(now_plus_5_sec)])
        self.rp.set_command(input)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string('xxx'))
    
    def test_expired_unixtimestamp_msec(self):
        now_in_msec = time.time()*1000 
        input = generate_input(['SET', 'key', 'xxx', 'PXAT', str(now_in_msec)])
        self.rp.set_command(input)
        
        out = self.rp.set_command(generate_input(['GET', 'key']))
        self.assertEqual(out, deserialize_simple_string(''))
