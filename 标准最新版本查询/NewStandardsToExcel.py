import FindNewStandards
import re
import xlwings as xw
import time
import func_timeout


@func_timeout.func_set_timeout(10)
def getData(findContent):
    # 包装FindNewStandards.getData，使之具有超时退出功能。
    return FindNewStandards.getData(findContent)


# saveFile = r'D:\标准最新版本查询\标准最新版本.xlsx'
saveFile = r'F:\program\python\标准最新版本查询\标准最新版本.xlsx'


def saveToExcel(saveFile):

    # 打开Excel文件
    try:
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(saveFile)
        sht1 = wb.sheets["标准最新版本"]
    except Exception:
        print('\n>> 打开Excel文件失败')
        return
    print('\n>> 打开Excel文件成功')

    try:
        # 获取、整理待查标准
        lastRow = sht1.range('A302').end('up').row
        findContent = sht1.range((3, 1), (lastRow, 1)).value

        for i in range(len(findContent)):
            if type(findContent[i]) != type('a'):
                findContent[i] = '待查标准号必须包含字母、数字'
            elif re.findall('[a-z|A-Z]+.*[0-9]+', findContent[i]) == None:
                findContent[i] = '待查标准号必须包含字母、数字'
            else:
                findContent[i] = re.sub(' ', '', findContent[i])
                findContent[i] = re.sub('　', '', findContent[i])
                findContent[i] = re.sub('／', '/', findContent[i])
                findContent[i] = re.sub('－', '-', findContent[i])
        print('>> 已获取待查标准号')

        # 调用getData查找
        dataList = []
        for i in range(len(findContent)):

            if findContent[i] == '待查标准号必须包含字母、数字':
                dataList.append(['待查标准号必须包含字母、数字', '', '', '', ''])

            elif findContent[i] == '':
                dataList.append(['', '', '', '', ''])

            else:
                try:  # 超时判断
                    data, information = getData(findContent[i])
                    dataList.append(data)
                    print('>> 查询第%d条标准，%s' % (i + 1, information))

                except func_timeout.exceptions.FunctionTimedOut:
                    dataList.append(['查寻超时', '', '', '', ''])
                    print('>> 查询第%d条标准，超时' % (i + 1))

        # 将dataList数据输入到sht1
        sht1.range("A1").value = '更新时间：' + time.strftime(
            '%Y年%m月%d日  %H:%M:%S', time.localtime(time.time())) + \
            '   数据来自工标网 http://www.csres.com'

        print('>> 已完成全部查询')
        sht1.range("B3").value = dataList

        # 改色
        sht1.range('A3：F302').api.Font.Color = 0
        for i in range(len(dataList)):
            if (info := dataList[i][4]) == '作废' or info == '废止':
                sht1.range((i + 3, 1), (i + 3, 6)).api.Font.Color = 255  # 红
            elif info == '即将实施':
                sht1.range((i + 3, 1), (i + 3, 6)
                           ).api.Font.Color = 12611584  # 蓝
            elif dataList[i][0] == '未找到相关标准' or dataList[i][0] == '查询超时' \
                    or dataList[i][0] == '待查标准号必须包含字母、数字':
                sht1.range((i + 3, 1), (i + 3, 6)).api.Font.Color = 24704  # 棕

        wb.save()
        print('>> 已保存到Excel')

    except Exception as e:
        print('>> 查询过程出现错误，终止程序')
        print('>> 错误:', e)

    wb.close()
    app.quit()


def main():

    print('''
警告！
    本程序在工标网(http://www.csres.com)进行标准最新版次查询，
短时间大量查询可能造成工标网封禁IP！
    因此，本程序最多只查询Excel表前300条标准，并请勿频繁查询。
''')

    doIt = input('是否继续?(Y/N):')
    if doIt == 'Y' or doIt == 'y':
        saveToExcel(saveFile)


if __name__ == '__main__':
    main()
