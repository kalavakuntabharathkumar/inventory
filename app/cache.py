import json

class InventoryCache:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory = {}

    def get(self, key):
        if self.redis:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        return self.memory.get(key)

    def set(self, key, value, ttl=60):
        if self.redis:
            self.redis.setex(key, ttl, json.dumps(value))
        else:
            self.memory[key] = value

    def delete(self, key):
        if self.redis:
            self.redis.delete(key)
        else:
            self.memory.pop(key, None)
