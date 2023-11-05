import json


def get(db, key):
    key = json.dumps(key).encode("utf-8")
    value = db.Get(key)
    if value is None:
        return None
    return json.loads(value.decode("utf-8"))

def put(db, key, value):
    key = json.dumps(key).encode("utf-8")
    value = json.dumps(value).encode("utf-8")
    db.Put(key, value)

def isin(db, key):
    try:
        get(db, key)
        return True
    except KeyError:
        return False
