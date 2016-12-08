# __author__ = 'zhengandy'

# from Config import config
import redis


class RedisOperation(object):
    def __init__(self, host, port, db):
        self.r = redis.Redis(host=host, port=port, db=db)

    def redis_flush_all(self):
        self.r.flushall()

    def redis_keys(self):
        keys = self.r.keys()
        return keys

    def redis_size(self):
        size = self.r.dbsize()
        return size

    def redis_set(self, name, value):
        self.r.set(name, value)

    def redis_get(self, name):
        return self.r.get(name)

    def redis_del(self, name):
        self.r.delete(name)

# if "__main__" == __name__:
#     f = RedisOperation(config.redis_host, config.redis_port, config.redis_db)
#     f.redis_set("key1", "test_value")
#     f.redis_set("key2", "test_value")
#     f.redis_set("key3", "test_value")
#     print(f.redis_keys())
#     print f.redis_size()
#     print f.redis_get("ad")
#     f.redis_flush_all()
#     print f.redis_size()

