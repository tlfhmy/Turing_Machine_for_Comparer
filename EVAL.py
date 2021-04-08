def pair(x, y) -> int:
    def sgn(n) -> int:
        if n <= 0:
            return 0
        return 1

    def add(a, b) -> int:
        return a + b

    def sub(a, b) -> int:
        if a <= b:
            return 0
        return a - b

    return sgn(sub(x, y)) * (x ** 2 + 2 * y + 1) + sgn(sub(add(1, y), x)) * (y ** 2 + 2 * x)


mat = []
for i in range(0, 10):
    for j in range(0, i+1):
        mat.append((j, i))
        if i != j:
            mat.append((i, j))

print(mat)

res = []
for ele in mat:
    res.append(pair(ele[0], ele[1]))

