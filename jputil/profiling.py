import time
from contextlib import contextmanager

# from http://dabeaz.blogspot.com/2010/02/function-that-works-as-context-manager.html
def timethis(what):
    """Used as either a decorator or as a context manager,
    timethis outputs the time taken for a function to run.
    
    >>> @timethis
    ... def blah():
    ...     [x for x in range(100000)]
    ...     
    >>> blah()
    
    >>> with timethis("spin idle"):
    ...     [x for x in range(100000)]
    """
    @contextmanager
    def benchmark():
        start = time.time()
        yield
        end = time.time()
        print("%s : %0.3f seconds" % (what, end-start))
    if hasattr(what, "__call__"):
        def timed(*args,**kwargs):
            with benchmark():
                return what(*args,**kwargs)
        return timed
    else:
        return benchmark()


