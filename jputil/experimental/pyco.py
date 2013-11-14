"""Non-blocking concurrent processing using Python coroutines."""

# Where you  have a  CPU bound  or I/O  bound function,  instead of
# using a  thread and a  callback function to  run at a  later time
# when  the  result  has  been  processed,  you  simply  yield  the
# function  to the  coroutine runner.  Execution of  your coroutine
# will be suspended until the result is available.
#
#
# The Runner  will handle  the scheduling  of running  the blocking
# function in a  different thread (or on a  different processor for
# a CPU  bound task). Once  the result  has been computed,  this is
# sent back  into your coroutine  which then resumes from  the next
# line.

from functools import partial
from multiprocessing import Pool
from threading import Thread
import time

def io_bound(fn, *args, **kwargs):
    """Execute an I/O bound task and send back the return value to the coroutine."""
    return ('io', partial(fn, *args, **kwargs))

def cpu_bound(fn, *args, **kwargs):
    """Execute a CPU bound task and send back the return value"""
    return ('cpu', partial(fn, *args, **kwargs))


class AsyncThread(object):
    """A simple copy of the multiprocessing AsyncResult API.

    This runs a function in a background thread.  The return value of the
    function is stored and the flag `ready` is set.
    """
    def __init__(self, fn):
        self._ready = False
        self._result = None
        self._target = fn
        self.thread = Thread(target=self.runner)

    def runner(self):
        self._result = self._target()
        self._ready = True

    def run(self):
        self.thread.start()

    def ready(self):
        return self._ready

    def get(self):
        # if called before the result has been generated, block until ready
        while not self._ready:
            time.sleep(0.01)
        return self._result

class Runner():
    """Runs all coroutines and handles blocking task scheduling"""
    def __init__(self):
        self.coroutines = []
        self._cpu_pool = Pool()
        self.pending_tasks = []

    def add_coroutine(self, cr):
        self.coroutines.append(cr)

    def _add_task(self, coroutine, task):
        if task is not None:
            self.pending_tasks.append((coroutine, task))

    def run(self):
        running_tasks = []
        # prime all coroutines and fetch the first scheduled task
        for coroutine in self.coroutines:
            self._add_task(coroutine, next(coroutine))

        while self.pending_tasks or running_tasks:
            while self.pending_tasks:
                coroutine, (form, task) = self.pending_tasks.pop(0)
                if form is None:
                    pass
                elif form == 'cpu':
                    # run the cpu bound task in a separate process
                    running_tasks.append((coroutine, self._cpu_pool.apply_async(task)))
                elif form == 'io':
                    # run the i/o bound method in a background thread
                    t = AsyncThread(task)
                    running_tasks.append((coroutine, t))
                    t.run()

            # Check all pending results.  If a result has been returned by one
            # of the i/o threads or CPU processes, pass it back into the
            # coroutine which will then resume executing
            for coroutine, result in running_tasks[:]:
                if result.ready():
                    try:
                        self._add_task(coroutine, coroutine.send(result.get()))
                    except StopIteration:
                        pass # coroutine is finished, pass
                    running_tasks.remove((coroutine, result))
            time.sleep(0.001)



if __name__ == '__main__':
    def fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a

    def cpu_task(n, p):
        f = fib(n)
        return f % p

    def io_task(n):
        time.sleep(n)
        return n

    def example1(n, p=25):
        for i in range(7):
            a = (yield cpu_bound(cpu_task, n**i, p))
            print 'mod %d fib(%d): %d' % (p, n**i, a)

    def example2(n):
        r = (yield io_bound(io_task, n))
        print "I pretended to do I/O for %d seconds" % r

    r = Runner()
    r.add_coroutine(example1(10, 13))
    r.add_coroutine(example2(6))
    r.run()