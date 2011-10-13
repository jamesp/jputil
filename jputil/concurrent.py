# helper functions for writing multi-threaded and concurrent programs.
import threading
from contextlib import contextmanager

# from http://dabeaz.blogspot.com/2009/11/python-thread-deadlock-avoidance_20.html
local = threading.local()
@contextmanager
def acquire(*locks):
    """A context manager for aquiring several locks in one go.
    
    Throws an RuntimeError in a deadlock situation by tracking which locks
    have already been claimed by another nested acquire call.
    """
    locks = sorted(locks, key=lambda x: id(x))   
    acquired = getattr(local,"acquired",[])
    # Check to make sure we're not violating the order of locks already acquired   
    if acquired:
        if max(id(lock) for lock in acquired) >= id(locks[0]):
            raise RuntimeError("Lock Order Violation")
    acquired.extend(locks)
    local.acquired = acquired
    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]