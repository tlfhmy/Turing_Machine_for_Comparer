from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from math import log2

def find_n_root(x: int, y: int):

    step = 0

    a = 2
    min_a = 1
    max_a = 2
    s = 1


    step += 4

    while True:
        t = y
        s = 1
        tmp = a
        step += 3

        while t != 0:
            if t % 2 == 0:
                tmp *= tmp
                t /= 2
            else:
                s *= tmp
                t -= 1
            step += 3

        if s > x:
            a = (min_a + max_a) // 2
            max_a = a
            step += 3
            if a == min_a:
                return a, step, max(x, y)
        elif s == x:
            step += 1
            return a, step, max(x,y)
        else:
            min_a = a
            a *= 2
            max_a = a
            step += 4


test_all = True

if test_all:
    res = []
    for x in tqdm(range(1, 10000)):
        for y in range(1, 1000):
            res.append(find_n_root(x,y))

    x = [ele[1] for ele in res]
    y = [int(log2(ele[2]))+1 for ele in res]
    plt.scatter(y, x)

    v = np.linspace(0, max(y), 1000)
    f = 3*v*(3*v+4)
    plt.xlabel("bits of max(x, y)")
    plt.ylabel("Number of operations")
    plt.plot(v, f)
    plt.savefig("./find_n_root.png")


else:
    print(find_n_root(216,3))
