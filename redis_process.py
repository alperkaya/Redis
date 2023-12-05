#!/usr/bin/env python

from redis_array_parser import RedisArrayParser 
from redis_deserializer import *

class RedisProcess:

    def __init__(self):
        self.rap = RedisArrayParser()

    def set_command(self, data):
        if data == b'':
            return deserialize_error_message("Null input")

        decoded_data   = data.decode('utf-8')
        
        return self.response_ping(decoded_data) or \
                self.rap.parse(decoded_data) or \
                deserialize_error_message("Undefined command")
    
    def response_ping(self, decoded_data):
        data_list = decoded_data.split(redis_constants.LINE_BREAK)
        if data_list[0].upper() == redis_constants.PING_STR:
            return deserialize_simple_string("PONG")
