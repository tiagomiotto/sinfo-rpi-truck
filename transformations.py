import time

def default(data):
    data[-1]['timestamp'] = time.time()
    return data[-1]

def median(data):
    pass

