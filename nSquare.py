'''
    采用试算的方法，计算n*n的宫格
    实际只能计算9宫格和16宫格，25宫格计算超时
'''

import time


n = int(input("n="))                                 # N宫格边长)
nn = n * n                                           # N宫格总格子数（即N）
n_square = [[0 for i in range(n)]for j in range(n)]  # N宫格值列表

svoes = 0
for i in range(1, nn + 1):
    svoes += i
svoes = int(svoes / n)  # Sum value of each side 每边（列、斜对角）的和值


def next_cell(row, cloumn):
    # 返回下一个格子的坐标
    if cloumn < n - 1:
        return row, cloumn + 1
    if row == n - 1:
        return - 1, -1
    return row + 1, 0


def judge(value, n_square, row, cloumn):
    # 如果在row,cloumn填入value，返回N宫格中是否有错误
    # 返回值之前，将row,cloumn恢复为0

    n_square[row][cloumn] = value

    # 每一行中是否有错误
    for i in range(n):
        count, sum = 0, 0  # 一行中的非0数字个数，一行中的数字之和
        for j in range(n):
            if n_square[i][j] != 0:
                count += 1
            sum += n_square[i][j]
        if sum > svoes:
            n_square[row][cloumn] = 0
            return False
        if count == n and sum != svoes:
            n_square[row][cloumn] = 0
            return False

    # 每一列中是否有错误
    for j in range(n):
        count, sum = 0, 0
        for i in range(n):
            if n_square[i][j] != 0:
                count += 1
            sum += n_square[i][j]
        if sum > svoes:
            n_square[row][cloumn] = 0
            return False
        if count == n and sum != svoes:
            n_square[row][cloumn] = 0
            return False

    # 判断左上右下对角线是否有错误
    count, sum = 0, 0
    for i in range(n):
        if n_square[i][i] != 0:
            count += 1
        sum += n_square[i][i]
    if sum > svoes:
        n_square[row][cloumn] = 0
        return False
    if count == n and sum != svoes:
        n_square[row][cloumn] = 0
        return False

    # 判断右上左下对角线是否有错误
    count, sum = 0, 0
    for i in range(n):
        if n_square[i][n-1-i] != 0:
            count += 1
        sum += n_square[i][n-1-i]
    if sum > svoes:
        n_square[row][cloumn] = 0
        return False
    if count == n and sum != svoes:
        n_square[row][cloumn] = 0
        return False

    n_square[row][cloumn] = 0
    return True


def possible_values(n_square, row, cloumn):
    # 返回row,cloumn单元格可能的值，即1~9去除所有已经存在的值。
    # 返回值为一个集合。
    possible_values = set()  # 定义一个空集合
    p_v = set([i for i in range(1, nn + 1)])
    existing_value = set([n_square[i][j] for j in range(n)for i in range(n)])
    p_v -= existing_value  # 此时p_v是N宫格中未出现过的值的集合

    for value in p_v:
        if judge(value, n_square, row, cloumn):
            possible_values.add(value)

    return possible_values


def try_n_square(n_square, row, cloumn):

    # 遍历row,cloumn单元格所有可能的值
    for v in possible_values(n_square, row, cloumn):

        # 当单元格值已经确定时，跳过这次循环
        if n_square[row][cloumn] != 0:
            continue

        # 试算row,cloumn单元格为v值的情况
        n_square[row][cloumn] = v
        # 当row,cloumn单元格为v值，下一个空白单元格的坐标
        next_row, next_cloumn = next_cell(row, cloumn)

        # 如果不存在下一个空白单元格，说明已经算完了
        if next_row == -1:
            return True

        # 递归计算下一个空白单元格
        end = try_n_square(n_square, next_row, next_cloumn)  # 递归
        if end:
            return True

        n_square[row][cloumn] = 0


time0 = time.time()

try_n_square(n_square, 0, 0)

time_spend = time.time()-time0

for i in range(n):
    print(n_square[i])

print("用时：", time_spend, "s")
