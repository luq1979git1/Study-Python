import xlwings as xw
import time
import sqlite3
from spider import getData

dataList = getData()
excelFile = r'E:\Python\爬虫_豆瓣\豆瓣电影Top250.xlsx'
dbFile = r'E:\Python\爬虫_豆瓣\豆瓣电影Top250.db'


def saveToExcel(dataList, excelFile):
    # 将数据保存到excel文件中

    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(excelFile)
    sht = wb.sheets["Top250"]

    sht.range("A2").value = '更新时间：'+time.strftime(
        '%Y年%m月%d日  %H:%M:%S', time.localtime(time.time()))
    sht.range("B4").value = dataList

    wb.save()
    wb.close()
    app.quit()

    print('已经导入到Excle文件')


def init_db(dbFile):
    # 初始化数据库

    # 建表sql语句
    sql = '''
        create table Top250
        (
            排名 integer primary key autoincrement,
            海报链接 text,
            中文名 text,
            外国名 text,
            豆瓣评分 numeric,
            评价人数 numeric,
            一句话介绍 text,
            导演等信息 text,
            影片链接 text
        );
    '''

    conn = sqlite3.connect(dbFile)  # 连接数据库
    cousar = conn.cursor()          #
    cousar.execute(sql)             # 执行sql语句
    conn.commit()                   # 提交
    conn.close()


def saveDataToSQL(dataList, dbFile):

    init_db(dbFile)

    conn = sqlite3.connect(dbFile)  # 连接数据库
    cousar = conn.cursor()  #

    for data in dataList:

        # 把data中的数据加引号用来拼接后面的sql语句
        for i in range(len(data)):
            data[i] = '"' + str(data[i]) + '"'

        sql = '''
            insert into Top250(
                海报链接,中文名,外国名,豆瓣评分,评价人数,一句话介绍,导演等信息,影片链接)
                values(%s) ''' % ",".join(data)

        # print(sql)

        cousar.execute(sql)
        conn.commit()

    conn.close()


if __name__ == "__main__":
    saveToExcel(dataList, excelFile)
    saveDataToSQL(dataList, dbFile)
