import xlwings as xw
import math

app = xw.App(visible=False, add_book=False)
# 默认情况，可看到excel的操作，此处visible=False，不可见
# 默认情况，新建一个app会新建一个excel文件,此处add_book=False，不建

wb = app.books.open("F:/program/xlwings/城市发展潜能/数据.xlsx")
sht1 = wb.sheets["GDP"]
sht2 = wb.sheets["坐标面积"]
sht3 = wb.sheets["距离"]
sht4 = wb.sheets["市场潜能"]

# 读取各城市各年度GDP数据
data_GDP = sht1.range("B3:K28").value

# 读取各城市坐标及面积 coordinate坐标 area面积
data_c_a = sht2.range("B3:D28").value

# 计算各城市之间的距离
# 定义两个城市之间距离的列表
data_distance = [[0 for _ in range(26)] for _ in range(26)]
for i in range(26):
    for j in range(26):
        x1 = float(data_c_a[i][0])
        y1 = float(data_c_a[i][1])
        x2 = float(data_c_a[j][0])
        y2 = float(data_c_a[j][1])
        # 计算距离并写入列表
        data_distance[i][j] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
# 把距离列表写入excel
sht3.range("B3").value = data_distance

# 计算各城市发展潜能
# 定义各城市各年度潜能的列表
data_potential = [[0 for _ in range(10)] for _ in range(26)]

for k in range(10):      # 第k个年度
    for i in range(26):  # 第i个城市
        # MPi = 0
        Yi = data_GDP[i][k]  # 第i个城市第k年的GDP
        dii = (2 / 3) * (data_c_a[i][2] / math.pi) ** 0.5
        MPi = Yi / dii

        for j in range(26):  # 按公式累计其它城市
            if i != j:
                Yj = data_GDP[j][k]
                dij = data_distance[i][j]
                MPi += Yj / dij
        # 将潜能并写入列表
        data_potential[i][k] = MPi
# 把距离列表写入excel
sht4.range("B3").value = data_potential

wb.save()
wb.close()
app.quit()
