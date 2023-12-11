import unittest
from main import *


class test(unittest.TestCase):
    # CD-диски
    cd_disk = [
        CD_disk(1, 'Данные_1', 650, 1),
        CD_disk(2, 'Данные_2', 700, 2),
        CD_disk(3, 'Данные_3', 650, 2),
        CD_disk(4, 'Данные_4', 800, 3),
        CD_disk(5, 'Данные_5', 900, 3),
    ]

    # Библиотеки CD-дисков
    libraries = [
        Library_CD(1, 'CD-диски и точка'),
        Library_CD(2, 'Античные диски-CD'),
        Library_CD(3, 'Бесплатные CD-диски'),
        Library_CD(4, 'CD-диски с секретными данными'),
    ]

    connection = [
        CD_In_Library(1, 1),
        CD_In_Library(2, 2),
        CD_In_Library(2, 3),
        CD_In_Library(3, 3),
        CD_In_Library(3, 4),
        CD_In_Library(3, 5),
        CD_In_Library(4, 2),
        CD_In_Library(4, 3),
        CD_In_Library(4, 4),
        CD_In_Library(4, 5),
    ]

    def test_one(self):
        task_1 = []
        for i in libraries:
            for j in cd_disk:
                if i.Library_id == j.Library_id:
                    task_1.append((i.Library_name, j.CD_name))
        self.assertEqual(task1(task_1),
                         ['Данные_2',  'Данные_3'])

    def test_two(self):
        task_2 = []
        for i in libraries:
            for j in cd_disk:
                if i.Library_id == j.Library_id:
                    task_2.append((i.Library_name, j.CD_memory))
        self.assertEqual(task2(task_2),
                         [('Бесплатные CD-диски', 900),  ('Античные диски-CD', 700), ('CD-диски и точка', 650)])

    def test_three(self):
        task_3 = {}
        for i in connection:
            x = i.Library_id
            for j in libraries:
                if x == j.Library_id:
                    name = j.Library_name
                    if name not in task_3.keys():
                        task_3[name] = ''
            x = i.CD_id
            for j in cd_disk:
                if x == j.CD_id:
                    task_3[name] += j.CD_name + '\n'
        self.assertEqual(task3(task_3),
                         {'CD-диски и точка': ['Данные_1'],
                          'Античные диски-CD': ['Данные_2', 'Данные_3'],
                          'Бесплатные CD-диски': ['Данные_3', 'Данные_4', 'Данные_5'],
                          'CD-диски с секретными данными': ['Данные_2', 'Данные_3', 'Данные_4', 'Данные_5'],
                          })


if __name__ == '__main__':
    unittest.main()
