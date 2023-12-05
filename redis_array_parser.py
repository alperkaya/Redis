#!/usr/bin/env python

import redis_constants
from redis_dict import RedisDict
from redis_deserializer import *

class RedisArrayParser():

    def __init__(self):
        self.num_elems = 0
        self.elems = []
        self.redis_dict = RedisDict()
    
    def validate_data(self, decoded_data):
        self.data_list = decoded_data.split(redis_constants.LINE_BREAK)

        if self.data_list is None or self.data_list[0][0] != '*':
            return deserialize_error_message("Undefined input data structure")
        
        if not self.data_list[0][1].isdigit():
            return deserialize_error_message("Num of elements is not defined in input data")

        self.num_elems = int(self.data_list[0][1])
        self.elems =  self.data_list[2::2]

    def parse(self, data):
        self.validate_data(data)
        return self.response_ping_array() or \
            self.response_echo() or \
            self.response_exists() or \
            self.response_del() or \
            self.response_set() or \
            self.response_get() or \
            None

    def response_ping_array(self):
        if self.num_elems == 1 and self.elems[0] == redis_constants.PING_STR:
            return deserialize_simple_string(redis_constants.PONG_STR)
        
    def response_set(self):
        if self.elems[0] in redis_constants.SET_STR_LIST:
            if len(self.elems) == 3:
                self.redis_dict.set(self.elems[1], self.elems[2])
                return deserialize_simple_string('OK')
            elif len(self.elems) == 5:
                if self.elems[3] == 'EX': # seconds
                    self.redis_dict.set(self.elems[1], self.elems[2], float(self.elems[4]))
                    return deserialize_simple_string('OK')
                elif self.elems[3] == 'PX': # msec
                    self.redis_dict.set(self.elems[1], self.elems[2], float(self.elems[4])/1000)
                    return deserialize_simple_string('OK')
                elif self.elems[3] == 'EAXT': # unix time in sec
                    self.redis_dict.set(self.elems[1], self.elems[2], unix_timestamp=float(self.elems[4]))
                    return deserialize_simple_string('OK')
                elif self.elems[3] == 'PXAT': # unix time in msec
                    self.redis_dict.set(self.elems[1], self.elems[2], unix_timestamp=float(self.elems[4])/1000)
                    return deserialize_simple_string('OK')
            
    def response_get(self):
        if self.num_elems == 2 and self.elems[0] in redis_constants.GET_STR_LIST:
            redis_dict_value = self.redis_dict.get(self.elems[1])
            return deserialize_simple_string(redis_dict_value)        

    def response_echo(self):
        if self.elems[0] in redis_constants.ECHO_STR_LIST:
            return deserialize_simple_string(self.elems[1])
        
    def response_del(self):
        if self.elems[0] in redis_constants.DEL_STR_LIST:
            num_hit = 0
            for elem in self.elems[1:]:
                if self.redis_dict.delete(elem) != None:
                    num_hit += 1
            return deserialize_integer(num_hit)
    
    def response_exists(self):
        if self.elems[0] in redis_constants.EXISTS_STR_LIST:
            num_hit = 0
            keys = self.redis_dict.keys()
            for elem in self.elems[1:]:
                if elem in keys:
                    num_hit += 1
            return deserialize_integer(num_hit)