def ReadFile(path):
    with open(path) as f:
        m, p = [int(num) for num in f.readline().split()]
        matrix =[[0] * p for i in range(m)]
        for i in range(m):
            list_parts = [int(num) for num in f.readline().split()]
            machine = list_parts[0]
            for part in list_parts[1:]:
                matrix[machine - 1][part - 1] = 1


ReadFile('test.txt')