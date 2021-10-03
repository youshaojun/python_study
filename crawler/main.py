"""
爬取豆瓣top250数据
"""
import re  # 正则
import xlwt  # 处理excel
import sqlite3  # 数据库
from urllib import request, error  # 获取网页数据
from bs4 import BeautifulSoup  # 网页解析


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    # filename = "豆瓣电影Top250"
    # saveData2Excel(datalist, filename)
    dbname = "movie.db"
    saveData2Sqlite(datalist, dbname)


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = getHtml(url)
        bs = BeautifulSoup(html, "html.parser")
        items = bs.find_all("div", class_="item")
        for item in items:
            data = []
            item = str(item)
            link = re.findall(re.compile(r'<a href="(.*?)">'), item)[0]
            data.append(link)
            image = re.findall(re.compile(r'<img.*src="(.*?)"', re.S), item)[0]
            data.append(image)
            title = re.findall(re.compile(r'<span class="title">(.*)</span>'), item)[0]
            data.append(title)
            score = re.findall(re.compile(r'property="v:average">(.*)</span>'), item)[0]
            data.append(score)
            comment_num = re.findall(re.compile(r'<span>(\d*)人评价</span>'), item)[0]
            data.append(comment_num)
            overview = re.findall(re.compile(r'<span class="inq">(.*)</span>'), item)
            data.append(overview[0] if len(overview) > 0 else "")
            content = re.findall(re.compile(r'<p class="">(.*?)</p>', re.S), item)[0]
            content = re.sub('<br(\s+)?/>(\s+)?', " ", content)
            content = re.sub('/', " ", content)
            data.append(content.strip())
            datalist.append(data)
    return datalist


def getHtml(baseurl):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.82 Safari/537.36 "
    }
    req = request.Request(baseurl, headers=headers)
    html = ""
    try:
        response = request.urlopen(req, timeout=30)
        html = response.read().decode("utf-8")
    except error.URLError as e:
        print("处理失败啦!!!")
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData2Excel(datalist, filename):
    wk = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = wk.add_sheet(filename, cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片名称", "评分", "评论数", "概况", "相关信息")
    for i in range(0, 7):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        for j in range(0, 7):
            data = datalist[i]
            sheet.write(i + 1, j, data[j])
    wk.save(filename + ".xlsx")


def saveData2Sqlite(datalist, dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 3 or index == 4:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into douban_movie
            (
            info_link,pic_link,movie_name,score,comment_num,overview,content
            )values(%s)''' % ",".join(data)
        cursor.execute(sql)
    conn.commit()
    conn.close()


def initSqlite(dbname):
    create_tab_sql = '''
        create table douban_movie 
        (
        id integer primary  key  autoincrement,
        info_link text,
        pic_link text,
        movie_name varchar ,
        score numeric ,
        comment_num numeric ,
        overview text,
        content text
        )
    '''
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(create_tab_sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # initSqlite("movie.db")
    main()
