#!/usr/bin/env python

import redis_constants

def deserialize_error_message(error_msg):
    byte_response = redis_constants.MINUS_SIGN + error_msg + redis_constants.LINE_BREAK
    return byte_response.encode('utf-8')

def deserialize_simple_string(str_data):
    byte_response = redis_constants.PLUS_SIGN + str_data + redis_constants.LINE_BREAK
    return byte_response.encode('utf-8')

def deserialize_integer(int_data):
    byte_response = redis_constants.COLON_SIGN + str(int_data) + redis_constants.LINE_BREAK
    return byte_response.encode('utf-8')