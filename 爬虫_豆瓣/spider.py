# 目的：在豆瓣上爬取Top250电影的资讯

from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error

# compile用来创建正则表达式对象
findLink = re.compile(r'<a href="(.*?)">')                          # 电影详情链接
findTitle = re.compile(r'<span class="title">(.*?)</span>')         # 电影名
findRating = re.compile(
    r'<span class="rating_num" property="v:average">(.*)</span>')   # 电影评分
findJudgeNumber = re.compile(r'<span>(\d*)人评价</span>')            # 评价人数
findInq = re.compile(r'<span class="inq">(.*)</span>', re.S)        # 一句话介绍
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)                 # 导演等信息
findImgSrc = re.compile(r'<img alt=.* class="" src="(.*?)"', re.S)  # 电影图片链接

baseUrl = "https://movie.douban.com/top250?start="


def main():
    dataList = getData()

    for i in range(250):
        print(dataList[i], "\n")


def getData():
    # 爬取网页,解析数据，存到dataList中返回
    dataList = []

    for i in range(10):
        url = baseUrl + str(i * 25)  # 每页25个，共10页
        html = askUrl(url)

        # 解析数据
        soup = BeautifulSoup(html, "html.parser")  # 用bs解析html

        # 在soup中，找到<div>...</div>，符合class="item"的标准
        # 在网页源码中，这个div里面储存了想要的数据
        # 在class后面加_，是为了不报错
        for item in soup.find_all('div', class_="item"):
            # print(item)
            data = []  # 这个列表保存一部电影的全部信息
            item = str(item)

            # 电影图片，如果有多张，只要第一张
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            # 电影名及第2个电影名
            title = re.findall(findTitle, item)
            if len(title) >= 2:
                data.append(title[0])  # 在data中添加第1个电影名
                # 在data中添加第2个电影名,添加前去除一些多余符号（外文名有些多余符号）
                title[1] = re.sub(r"/", "", title[1])
                title[1] = re.sub(r"\xa0", "", title[1])
                data.append(title[1])
            else:
                data.append(title[0])
                data.append("")  # 在data中添加空电影名占位

            # 评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)

            # 评价人数
            judgeNumber = re.findall(findJudgeNumber, item)[0]
            data.append(judgeNumber)

            # 一句话介绍。这个介绍可能有，可能没有，可能多个。只要第一个。
            inq = re.findall(findInq, item)
            if len(inq) > 0:
                data.append(inq[0])
            else:
                data.append("")

            # 导演等信息
            bd = re.findall(findBd, item)[0]
            bd = re.sub(r'<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub(r'/', " ", bd)
            bd = re.sub(r'\xa0', " ", bd)
            bd = re.sub("  *", " ", bd)
            bd = bd.strip()  # 去除前后空格
            data.append(bd)

            # 电影链接
            link = re.findall(findLink, item)[0]
            data.append(link)

            # print(data)
            dataList.append(data)

    return dataList


def askUrl(url):

    # head 用户代理，表示告诉豆瓣服务器，我是什么机器（伪装成浏览器）
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400"}

    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("e.code")
        if hasattr(e, "reason"):
            print(e.reason)

    return html


def saveData(savePath):
    pass


if __name__ == "__main__":
    main()
