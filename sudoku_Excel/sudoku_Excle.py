import time
import xlwings as xw

from sudoku import answer_sudoku


app = xw.App(visible=False, add_book=False)

# 这里为什么相对路径找不到文件
wb = app.books.open(r"F:\program\python\xlwings\数独\sudoku_Excel\sudoku.xlsx")

sht = wb.sheets["Sudoku"]

sudoku = sht.range("A1:I9").value


for i in range(9):
    for j in range(9):
        try:
            # excel单元格从1开始计数，故需要+1
            sudoku[i][j] = int(sht.range(i + 1, j + 1).value)
            sht.range(i + 1, j + 1).api.Font.Color = 192.0       # 深红色
        except Exception:
            sudoku[i][j] = 0
            sht.range(i + 1, j + 1).api.Font.Color = 12611584.0  # 淡蓝色


time0 = time.time()
answer_sudoku(sudoku)
time_spend = time.time()-time0

for i in range(9):
    print(sudoku[i])
print("计算用时：", time_spend)

sht.range("A1").value = sudoku

wb.save()
wb.close()
app.quit()
