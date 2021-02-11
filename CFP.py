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


class GeneralVND:

    def __init__(self, path):
        self.matrix = readFile(path)
        self.zeroes = self.countZeroes()
        self.ones = self.countOnes()
        self.solution = [[]]
        self.machines = len(self.matrix)
        self.parts = len(self.matrix[0])

    def efficiency(self):
        zeroes = 0
        ones = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 1:
                    zeroes += 1
                else:
                    ones += 1
        return 0

    def generateConfigsUniform(self, machines, parts):
        min_dimension = min(machines, parts)
        cells_number = random.randint(1, min_dimension)
        m_decomposition = self.decomposition(cells_number, machines)
        p_decomposition = self.decomposition(cells_number, parts)
        solution = [self.splitting(self, m_decomposition, machines), self.splitting(self, p_decomposition, parts)]
        return solution

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


#print(GenerateConfigsUniform(len(matrix), len(matrix[0])))