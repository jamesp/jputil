import time
from py_co import Runner, cpu_bound, io_bound

def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def cpu_task(n):
    f = fib(n)
    return f % 25

def io_task(n):
    time.sleep(n)
    return n

def example1(n):
    for i in range(6):
        a = (yield cpu_bound(cpu_task, n**i))
        print 'fib(%d): %d' % (n**i, a)

def example2(n):
    r = (yield io_bound(io_task, n))
    print "I slept for %d seconds" % r

r = Runner()
r.add_coroutine(example1(10))
r.add_coroutine(example2(6))
r.run()