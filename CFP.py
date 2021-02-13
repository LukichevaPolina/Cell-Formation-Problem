import random
from copy import copy, deepcopy


def read_file(path):
    with open(path) as f:
        m, p = [int(num) for num in f.readline().split()]
        matrix_mp = [[0] * p for i in range(m)]
        for i in range(m):
            list_parts = [int(num) for num in f.readline().split()]
            machine = list_parts[0]
            for part in list_parts[1:]:
                matrix_mp[machine - 1][part - 1] = 1
        return matrix_mp


def count_ones(matrix_):
    zeroes = 0
    ones = 0
    for i in range(len(matrix_)):
        for j in range(len(matrix_[0])):
            if matrix_[i][j] == 1:
                ones += 1
    return ones


class GeneralVNS:

    def __init__(self, matrix, ones):
        self.matrix = matrix
        self.ones = ones
        self.solution = [[]]
        self.machines = len(matrix)
        self.parts = len(matrix[0])
        self.efficiency = 0.0
        self.cells = 0

    def count_efficiency(self):
        ones_in, zeroes_in = 0, 0
        for i in range(self.machines):
            for j in range(self.parts):
                if self.solution[0][i] == self.solution[1][j]:
                    if self.matrix[i][j] == 1:
                        ones_in += 1
                    else:
                        zeroes_in += 1
        self.efficiency = float(ones_in) / (self.ones + zeroes_in)

    def generate_configs_uniform(self):
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

    def count_new_efficiency_p(self, part, cell):
        ones_in, zeroes_in = 0, 0
        new_solution = [[]]
        new_solution = deepcopy(self.solution)
        new_solution[1][part] = cell
        for i in range(self.machines):
            for j in range(self.parts):
                if new_solution[0][i] == new_solution[1][j]:
                    if self.matrix[i][j] == 1:
                        ones_in += 1
                    else:
                        zeroes_in += 1
        efficiency = float(ones_in) / (self.ones + zeroes_in)
        return efficiency

    def count_new_efficiency_m(self, machine, cell):
        ones_in, zeroes_in = 0, 0
        new_solution = [[]]
        new_solution = deepcopy(self.solution)
        new_solution[0][machine] = cell
        for i in range(self.machines):
            for j in range(self.parts):
                if new_solution[0][i] == new_solution[1][j]:
                    if self.matrix[i][j] == 1:
                        ones_in += 1
                    else:
                        zeroes_in += 1
        efficiency = float(ones_in) / (self.ones + zeroes_in)
        return efficiency

    def shaking(self):
        if self.cells == 1:
            self.divide()
        else:
            merge_or_divide = random.randint(0, 1)
            if merge_or_divide == 1:
                self.merge()
            else:
                self.divide()

    def divide(self):
        if self.cells == 1:
            boarder = 1
        else:
            boarder = self.cells - 1
        cell_to_divide = random.randint(1, boarder)
        m_in_cell = self.elementsInCell(self.machines, cell_to_divide, 0)
        p_in_cell = self.elementsInCell(self.parts, cell_to_divide, 1)
        if len(m_in_cell) == 1 or len(p_in_cell) == 1:
            return
        self.cells += 1
        machine_id_to_divide = random.randint(1, len(m_in_cell) - 1)
        part_id_to_divide = random.randint(1, len(p_in_cell) - 1)
        for i in m_in_cell[machine_id_to_divide:]:
            self.solution[0][i] = self.cells
        for i in p_in_cell[part_id_to_divide:]:
            self.solution[1][i] = self.cells

    def merge(self):
        cells_to_merge = sorted([random.randint(1, self.cells), random.randint(1, self.cells)])
        while cells_to_merge[0] == cells_to_merge[1]:
            cells_to_merge = sorted([random.randint(1, self.cells), random.randint(1, self.cells)])
        self.cells -= 1
        for i in range(self.machines):
            if self.solution[0][i] == cells_to_merge[1]:
                self.solution[0][i] = cells_to_merge[0]
        for i in range(self.parts):
            if self.solution[1][i] == cells_to_merge[1]:
                self.solution[1][i] = cells_to_merge[0]

    def elementsInCell(self, element, cell, id):
        list_elements = []
        for i in range(element):
            if self.solution[id][i] == cell:
                list_elements.append(i)
        return list_elements

    def improve_solution(self):
        self.count_efficiency()
        d_machine = 1
        d_parts = 1
        while d_machine > 0 and d_parts > 0:
            d_machine, d_parts = 0, 0
            part_from = 0
            part_to = 0
            for part in range(self.parts):
                flag = 0
                cell_of_part = self.solution[1][part]
                for cur_cell in self.solution[1]:
                    if cell_of_part == cur_cell:
                        flag += 1
                if flag == 1:
                    continue
                for cell in range(1, self.cells+1):
                    if cell_of_part == self.solution[1][cell]:
                        continue
                    new_eff = self.count_new_efficiency_p(part, cell)
                    if new_eff > self.efficiency:
                        d_parts = new_eff - self.efficiency
                        part_from = part
                        part_to = cell
            machine_from = 0
            machine_to = 0
            for machine in range(self.machines):
                flag = 0
                cell_of_machine = self.solution[0][machine]
                for cur_cell in self.solution[0]:
                    if cell_of_machine == cur_cell:
                        flag += 1
                if flag == 1:
                    continue
                for cell in range(1, self.cells+1):
                    if cell_of_machine == self.solution[0][cell]:
                        continue
                    new_eff = self.count_new_efficiency_m(machine, cell)
                    if new_eff > self.efficiency:
                        d_machine = new_eff - self.efficiency
                        machine_from = machine
                        machine_to = cell
            if d_machine == 0 and d_parts == 0:
                break
            elif d_parts > d_machine:
                self.solution[1][part_from] = part_to
            else:
                self.solution[0][machine_from] = machine_to
            self.count_efficiency()



matrix = read_file('carrie28.txt')
vns = GeneralVNS(matrix, count_ones(matrix))

vns.generate_configs_uniform()
vns.count_efficiency()
new_vns = GeneralVNS(matrix, count_ones(matrix))
for j in range(200):
    new_vns.generate_configs_uniform()
    new_vns.count_efficiency()
    if new_vns.efficiency > vns.efficiency:
        vns.solution = deepcopy(new_vns.solution)
        vns.cells = new_vns.cells
        vns.efficiency = new_vns.efficiency
vns.improve_solution()
vns.count_efficiency()
new_vns = deepcopy(vns)
for i in range(20):
    new_vns.shaking()
    new_vns.improve_solution()
    new_vns.count_efficiency()
    if new_vns.efficiency > vns.efficiency:
        vns = deepcopy(new_vns)
        print(vns.efficiency, vns.solution)