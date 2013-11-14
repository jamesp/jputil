import numpy as np

def integrate(f, a, b, n=1000):
    """Calculate the approximate definite integral of a function
    over [a, b] with n intervals using the trapezium rule."""
    h  = float(b-a)/n
    xs = np.linspace(a, b, n+1)
    ys = f(xs)
    return np.sum(h*ys)

def integrate2(f, a, b, n=1000):
    """Integrate over the region but not using numpy lists."""
    h = float(b - a)/n
    xs = [x*h for x in range(n+1)]
    ys = [f(x) for xs in xs]
    return sum(0.5*h*(y1+y2) for y1, y2 in zip(ys[:-1], ys[1:]))
    
print integrate(np.sin, 0, np.pi)
    