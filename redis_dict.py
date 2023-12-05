
import time

class RedisDict():

    def __init__(self):
        self.data = {}
        self.expiry_times = {}

    def set(self, key, value, ttl_seconds=None, unix_timestamp=None):
        self.data[key] = value

        if ttl_seconds:
            expiry_time = time.time() + ttl_seconds
            self.expiry_times[key] = expiry_time
        elif unix_timestamp:
            self.expiry_times[key] = unix_timestamp
        else:
            self.expiry_times.pop(key, None)
    
    def get(self, key):
        now = time.time()

        if key in self.expiry_times and now > self.expiry_times[key]:
            self.data.pop(key, None)
            self.expiry_times.pop(key, None)
            return ''
        else:
            return self.data.get(key)
    
    def delete(self, key):
        value = self.data.pop(key, None)
        self.expiry_times.pop(key, None)
        return value
    
    def keys(self):
        return list(self.data.keys())
    

