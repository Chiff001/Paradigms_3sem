def print_result(func):
    def f():
        print(func.__name__)
        x = func()
        if type(x) == type(dict()):
            for i, j in x.items():
                print(i, '=', j)
        elif type(x) == type(list()):
            for i in x:
                print(i)
        else:
            print(x)
    return f

@print_result
def test_1():
    return 1


@print_result
def test_2():
    return 'iu5'


@print_result
def test_3():
    return {'a': 1, 'b': 2}


@print_result
def test_4():
    return [1, 2]


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
