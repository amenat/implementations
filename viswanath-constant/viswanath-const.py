# Numberphile/James Grimes Video: https://www.youtube.com/watch?v=ELA8gNNMHoU  
# Read more: https://en.wikipedia.org/wiki/Random_Fibonacci_sequence

from random import choice
from operator import add, sub
import gmpy2
gmpy2.get_context().precision=64


def exp_rand_fib_n(n: int, simcount: int) -> int:
    '''
    Returns list containing simulations of nth number in random fibonacci sequence.
    '''
    n = n-1
    ops = [add, sub]
    simulation = []
    for i in range(simcount):
        f_0, f_1 = 0, 1
        for j in range(n):
            op = choice(ops)
            tmp = op(f_0, f_1)
            f_0 = f_1
            f_1 = tmp
        simulation.append(abs(f_1))
    
    return simulation


if __name__ == "__main__":
    n = 200000
    simcount = 100
    fibn = exp_rand_fib_n(n, simcount)
    nthroot = lambda x: gmpy2.root(x, n)
    results = list(map(nthroot, fibn))
    print(sum(results) / len(results))

    # returned: 1.13199499293206857608