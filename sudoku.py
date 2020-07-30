import time


def frist_blank(sudoku):
    # 寻找第一个空白单元格，返回其坐标。
    # 如果没有空白单元格，返回-1，-1。代表没有空白格，数独已经完成。
    for row in range(9):
        for cloumn in range(9):
            if sudoku[row][cloumn] == 0:
                return row, cloumn
    return - 1, -1


def next_blank(soduku, row, cloumn,):
    # 从row,cloumn开始寻找下一个空白格，返回其坐标。
    # 如果没有下一个空白单元格，返回-1，-1。数独已经完成？

    # 如果在本行找到了下一个空白格，返回其坐标。
    for next_cloumn in range(cloumn + 1, 9):
        if soduku[row][next_cloumn] == 0:
            return row, next_cloumn

    if row == 8:
        return -1, -1

    # 如果在本行没找到了下一个空白格，从下行第一个开始搜索，返回其坐标。
    for next_row in range(row + 1, 9):
        for next_cloumn in range(9):
            if soduku[next_row][next_cloumn] == 0:
                return next_row, next_cloumn

    return - 1, -1


def possible_values(sudoku, row, cloumn):
    # 返回row,cloumn单元格可能的值，即1~9去除行、列、方块中已经存在的值。
    # 返回值为一个集合。

    grid_r = row // 3       # 方格第一个单元格行坐标，即方格行坐标
    grid_c = cloumn // 3

    p_v = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    # p_v = set([i for i in range(1, 10)])

    # 行中所有的数字形成一个列表，并转换成集合
    # 不需要去除0，因为p_v中本来就没有0
    row_value = set([sudoku[row][i] for i in range(9)])

    # 列中所有的数字形成一个列表，并转换成集合
    cloumn_value = set([sudoku[i][cloumn] for i in range(0, 9)])

    # 方块中所有的数字形成一个列表，并转换成集合
    grid_value = set([sudoku[grid_r*3+i][grid_c*3+j]
                      for i in range(0, 3) for j in range(0, 3)])

    # 返回可能的值，即1~9去除行、列、方块中已经有的值
    return p_v - row_value - cloumn_value - grid_value


def try_sudoku(sudoku, row, cloumn):

    # 遍历row,cloumn单元格所有可能的值
    for v in possible_values(sudoku, row, cloumn):

        # 当单元格值已经确定时，跳过这次循环
        if sudoku[row][cloumn] != 0:
            continue

        # 试算row,cloumn单元格为v值的情况
        sudoku[row][cloumn] = v
        # 当row,cloumn单元格为v值，下一个空白单元格的坐标
        next_row, next_cloumn = next_blank(sudoku, row, cloumn)

        # 如果不存在下一个空白单元格，说明已经算完了
        if next_row == -1:
            return True

        # 递归计算下一个空白单元格
        end = try_sudoku(sudoku, next_row, next_cloumn)  # 递归
        if end:
            return True

        sudoku[row][cloumn] = 0


def answer_sudoku(sudoku):
    row, cloumn = frist_blank(sudoku)
    try_sudoku(sudoku, row, cloumn)


def main():
    # sudoku = [[0, 0, 5, 3, 0, 0, 0, 0, 0],
    #           [8, 0, 0, 0, 0, 0, 0, 2, 0],
    #           [0, 7, 0, 0, 1, 0, 5, 0, 0],
    #           [4, 0, 0, 0, 0, 5, 3, 0, 0],
    #           [0, 1, 0, 0, 7, 0, 0, 0, 6],
    #           [0, 0, 3, 2, 0, 0, 0, 8, 0],
    #           [0, 6, 0, 5, 0, 0, 0, 0, 9],
    #           [0, 0, 4, 0, 0, 0, 0, 3, 0],
    #           [0, 0, 0, 0, 0, 9, 7, 0, 0]]

    # sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #           [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    sudoku = [[0, 2, 6, 1, 0, 0, 4, 0, 0],
              [5, 0, 7, 6, 3, 4, 1, 0, 2],
              [0, 0, 1, 0, 0, 5, 9, 7, 0],
              [0, 0, 0, 0, 5, 6, 2, 1, 9],
              [0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 7, 0, 3],
              [3, 0, 9, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 5, 0, 0, 0, 0, 0],
              [1, 6, 5, 2, 4, 0, 0, 0, 0]]

    time0 = time.time()

    answer_sudoku(sudoku)

    time_spent = time.time()-time0

    for i in range(9):
        print(sudoku[i])

    print(time_spent)


if __name__ == "__main__":
    main()

