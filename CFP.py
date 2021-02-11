import random


def readFile(path):
    with open(path) as f:
        m, p = [int(num) for num in f.readline().split()]
        matrix_mp = [[0] * p for i in range(m)]
        for i in range(m):
            list_parts = [int(num) for num in f.readline().split()]
            machine = list_parts[0]
            for part in list_parts[1:]:
                matrix_mp[machine - 1][part - 1] = 1
        return matrix_mp


def countOnes(matrix):
    zeroes = 0
    ones = 0
    for i in range(len(matrix)):
        for j in range(len([0])):
            if matrix[i][j] == 1:
                ones += 1
    return ones


class GeneralVND:

    def __init__(self, matrix, ones):
        self.matrix = matrix
        self.ones = ones
        self.solution = [[]]
        self.machines = len(matrix)
        self.parts = len(matrix[0])
        self.efficiency = 0.0
        self.cells = 0

    def countEfficiency(self):
        ones_in, zeroes_in = 0, 0
        for i in range(self.machines):
            for j in range(self.parts):
                if self.solution[0][i] == self.solution[1][j]:
                    if self.matrix[i][j] == 1:
                        ones_in += 1
                    else:
                        zeroes_in += 1
        self.efficiency = float(ones_in) / (self.ones + zeroes_in)

    def generateConfigsUniform(self):
        min_dimension = min(self.machines, self.parts)
        self.cells = random.randint(1, min_dimension)
        m_decomposition = self.decomposition(self.cells, self.machines)
        p_decomposition = self.decomposition(self.cells, self.parts)
        self.solution = [self.splitting(m_decomposition, self.machines), self.splitting(p_decomposition, self.parts)]

    # рандомно раскладываем по ячейкам станки/детали
    def splitting(self, decomp, length):
        cells_num = [0]*length
        for i in range(0, len(decomp)):
            for j in range(1, decomp[i] + 1):
                part = random.randint(0, length - 1)
                while cells_num[part] != 0:
                    part = random.randint(0, length - 1)
                cells_num[part] = i + 1
        return cells_num


    # разложение на terms_number числа number
    def decomposition(self, terms_number, number):
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


matrix = readFile('test.txt')
vnd = GeneralVND(matrix, countOnes(matrix))
vnd.generateConfigsUniform()
vnd.countEfficiency()
print(vnd.efficiency)