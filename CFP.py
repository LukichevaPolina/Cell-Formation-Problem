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
    min_cells, max_cells = FindOptimalCellRange(matrix)


def  FindOptimalCellRange(matrix_mp):
    min_dimension = min(len(matrix), len(matrix[0]))
    configs_number = 500
    configs = GenerateConfigs(matrix_mp, 2, min_dimension, configs_number, len(matrix), len(matrix[0]))

    return[]


def GenerateConfigs(min_cells, max_cells, configs_number, machines, parts):
    configs = {}
    for cells_number in range(min_cells, max_cells + 1):
        generated = GenerateConfigsUniform(cells_number, configs_number)
    return[]


def GenerateConfigsUniform(min_dimension, cells_number, configs_number, machines, parts):
    configs_number = random.randint(1, configs_number)
    m_decomposition = Decomposition(cells_number, machines)
    p_decomposition = Decomposition(cells_number, parts)
    solution = [[0]*machines, [0]*parts]
    for i in range(cells_number):
        m = random.randint(0, machines)
        p = random.randint(0, parts)
        while solution[0][m] and solution[1][p]:
            m = random.randint(0, machines)
            p = random.randint(0, parts)
            print(m, p)
        solution[0][m] = i
        solution[1][p] = i
    return solution


def CMHeuristic():
    return[]


def ImproveSolution():
    return[]


# разложение на terms_number числа number
def Decomposition(terms_number, number):
    size_configs = [number]
    for i in range(terms_number):
        new_elem = random.randint(1, max(size_configs) - 1)
        size_configs[size_configs.index(max(size_configs))] -= new_elem
        size_configs.append(new_elem)

    return size_configs


matrix = ReadFile('test.txt')
print(GenerateConfigsUniform(5,3,10,5,4))