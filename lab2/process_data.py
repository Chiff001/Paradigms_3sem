import json
import sys
import random
import time


# Сделаем другие необходимые импорты
def print_result(func):
    def wrapper(arg):
        print(func.__name__)
        i = func(arg)
        print(i)

    return wrapper


class cm_timer_1():
    def __init__(self):
        self.start = 0.0
        self.end = 0.0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end = time.time()
        print('Время выполнения: {} секунд.'.format(self.end - self.start))


path = 'data_light.json'

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

with open(path, encoding="utf-8") as f:
    data = json.load(f)
    data = tuple(x["job-name"].lower() for x in data if "job-name" in x.keys())
    uniq_data = []
    for i in data:
        if i.lower() not in uniq_data:
            uniq_data.append(i)
    data = uniq_data


# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    return sorted(arg)


def f2(arg):
    return filter(lambda x: "программист" in x, arg)


def f3(arg):
    return tuple(map(lambda x: x + " с опытом Python", arg))


@print_result
def f4(arg):
    return zip(arg, [random.randint(100_000, 200_000)] * len(arg))


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))
