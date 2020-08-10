from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import time

# 在每个<tr></tr>中，有5个<td></td>，部分存有需要的数据
findData = re.compile(r'<font color=.*>(.*)</font>', re.S)
numbersAndDots = re.compile(r'(\d|\.)+')
baseUrl = 'http://www.csres.com/s.jsp?keyword=查找内容&pageNum=1'


def main():
    # 测试 getData()
    findContent = 'JB/t6166'
    print(getData(findContent))


def getData(findContent):
    # 把getAllData返回的值进行处理，找到需要的那一个data
    # 返回对某数据的查询结果data、情况
    # 情况包括：'工标网连接失败'、'完成'、'未找到相关标准'

    # 模拟查询延时(0~3.999秒)
    # sleep = random.random(0, 3) + random.random()
    # time.sleep(sleep)

    url = re.sub('查找内容', findContent, baseUrl)
    dataList, getAllData_OK = getAllData(url)

    if not getAllData_OK:
        return ['工标网连接失败', '', '', '', ''], '工标网连接失败'

    try:
        # 检查查到标准中的关键部分(数字+小数点)是否与想查的一致
        # 因为查找***122，***12221也会被查出来
        for data1 in dataList:
            standard_number = data1[0]
            standard_number = re.sub(' ', '', standard_number)
            standard_number = re.sub('　', '', standard_number)
            standard_number = re.sub('／', '/', standard_number)
            standard_number = re.sub('－', '-', standard_number)
            standard_number = re.search(numbersAndDots, standard_number)[0]
            findContent = re.search(numbersAndDots, findContent)[0]
            if findContent != standard_number:
                dataList.remove(data1)

        # 如果存在现行标准，则返回（第一个）现行标准
        for data1 in dataList:
            if data1[4] == '现行':
                return data1, '完成'

        # 如果不存在现行标准，返回发布时间最晚的标准
        if (lenDataList := len(dataList)) > 1:
            for i in range(1, lenDataList):
                if dataList[0][3] < dataList[i][3]:
                    dataList[0], dataList[i] = dataList[i], dataList[0]
        return dataList[0], '完成'

    except Exception:
        return ['未找到相关标准', '', '', '', ''], '未找到相关标准'


def getAllData(url):
    # 把搜索网页中的内容放到dataList中返回,同时返回url连接是否正确

    # gatAllData_OK = True
    dataList = []
    html, askUrl_OK = askUrl(url)
    if not askUrl_OK:
        return dataList, False

    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('tr', {'bgcolor': "#FFFFFF"}):
        data = []
        soup1 = BeautifulSoup(str(item), "html.parser")

        item1 = soup1.find_all('td')

        data.append((re.findall(findData, str(item1[0]))[0]))  # 标准号
        data.append((re.findall(findData, str(item1[1]))[0]))  # 名称

        data2 = str(re.findall(findData, str(item1[2]))[0])    # 发布单位
        data2 = re.sub('　', ' ', data2)
        data2 = re.sub('\r', '', data2)
        data2 = re.sub('\n', '', data2)
        data2 = re.sub(r'\.', '', data2)
        data2 = re.sub('  *', ' ', data2)
        data2 = re.sub('^ ', '', data2)
        data2 = re.sub(' $', '', data2)
        data.append(data2)

        data.append((re.findall(findData, str(item1[3]))[0]))  # 实施日期
        data.append((re.findall(findData, str(item1[4]))[0]))  # 现状

        dataList.append(data)

    return dataList, True


def askUrl(url):

    # head 用户代理，表示告诉服务器，我是什么机器（伪装成浏览器）
    head = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400'}

    request = urllib.request.Request(url, headers=head)
    html = ""
    askUrl_OK = True

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("GBK")
    except Exception:
        askUrl_OK = False

    return html, askUrl_OK


if __name__ == "__main__":
    main()
