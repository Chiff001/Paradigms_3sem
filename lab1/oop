import math


def sol(a, b, c):
    res = []
    D = b * b - 4 * a * c
    if D == 0:
        x = -b / (2 * a)
        if x >= 0:
            res.append(x)
    elif D > 0:
        x1 = ((-b + math.sqrt(D)) / (2 * a))
        x2 = ((-b - math.sqrt(D)) / (2 * a))
        if x1 >= 0:
            res.append(x1)
        if x2 >= 0:
            res.append(x2)
    return res


a = int(input())
b = int(input())
c = int(input())
if a != 0 and b != 0:
    res = sol(a, b, c)
elif a == 0:
    res = [-c / b]
elif b == 0:
    res = [math.sqrt(-c / a)]
if len(res) == 0:
    print("Решений нет")
if len(res) == 1:
    print("Решения:")
    print(math.sqrt(res[0]))
    print(-math.sqrt(res[0]))
if len(res) == 2:
    print("Решения:")
    print(math.sqrt(res[0]))
    print(-math.sqrt(res[0]))
    print(math.sqrt(res[1]))
    print(-math.sqrt(res[1]))
