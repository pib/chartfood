class DummyCache(dict):
    def get(self, key):
        return self[key]

    def put(self, key, val):
        self[key] = val
