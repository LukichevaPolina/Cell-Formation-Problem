import random


def ReadFile(path):
    with open(path) as f:
        m, p = [int(num) for num in f.readline().split()]
        matrix_mp = [[0] * p for i in range(m)]
        for i in range(m):
            list_parts = [int(num) for num in f.readline().split()]
            machine = list_parts[0]
            for part in list_parts[1:]:
                matrix_mp[machine - 1][part - 1] = 1
        return matrix_mp


def Solve(matrix_mp):
    return 0


def GenerateConfigsUniform(min_dimension, machines, parts):
    cells_number = random.randint(1, min_dimension)
    m_decomposition = Decomposition(cells_number, machines)
    p_decomposition = Decomposition(cells_number, parts)
    solution = [Splitting(m_decomposition, machines), Splitting(p_decomposition, parts)]
    return solution


# рандомно раскладываем по ячейкам станки/детали
def Splitting(decomposition, length):
    cells_num = [0]*length
    for i in range(0, len(decomposition)):
        for j in range(1, decomposition[i] + 1):
            part = random.randint(0, length - 1)
            while cells_num[part] != 0:
                part = random.randint(0, length - 1)
            cells_num[part] = i + 1
    return cells_num


# разложение на terms_number числа number
def Decomposition(terms_number, number):
    size_configs = [number]
    for i in range(terms_number - 1):
        if max(size_configs) == 1:
            border = 1
        else:
            border = max(size_configs) - 1
        new_elem = random.randint(1, border)
        size_configs[size_configs.index(max(size_configs))] -= new_elem
        size_configs.append(new_elem)

    return size_configs


matrix = ReadFile('test.txt')
print(GenerateConfigsUniform(8, 8, 16))