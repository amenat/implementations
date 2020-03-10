# Numberphile/James Grimes Video: https://www.youtube.com/watch?v=ELA8gNNMHoU  
# Read more: https://en.wikipedia.org/wiki/Random_Fibonacci_sequence

from random import choice
import gmpy2
gmpy2.get_context().precision=256

def exp_rand_fib_n(n: int, simcount: int) -> int:
    '''
    Returns expected value for nth term in random fibonacci sequence.
    '''
    simulation = []
    for i in range(simcount):
        f_0, f_1 = 1, 1
        for j in range(n-2):
            tmp = f_0 + choice([-1,1]) * f_1
            f_0 = f_1
            f_1 = tmp
        simulation.append(f_1)
    
    return abs(sum(simulation) // simcount)



n = 100000
fibn = exp_rand_fib_n(n, 100)

print(gmpy2.root(fibn, n))