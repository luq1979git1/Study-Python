import xlwings as xw
import time
from spider import getData

saveFile = r'E:\Python\爬虫_豆瓣\豆瓣电影Top250.xlsx'

app = xw.App(visible=False, add_book=False)
wb = app.books.open(saveFile)
sht = wb.sheets["Top250"]

dataList = getData()

sht.range("A2").value = '更新时间：'+time.strftime(
    '%Y年%m月%d日  %H:%M:%S', time.localtime(time.time()))
sht.range("B4").value = dataList

wb.save()
wb.close()
app.quit()

print('已经导入到Excle文件')
