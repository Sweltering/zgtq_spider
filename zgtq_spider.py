# 爬取中国天气网最高气温的前10个城市

import requests

from bs4 import BeautifulSoup
from pyecharts import Bar


ALL_DATA = []  # 存放全国城市最高气温

# 解析页面信息
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    }
    # 请求网页数据
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8', 'ignore')

    # 解析网页数据
    soup = BeautifulSoup(html, 'html5lib')
    conMidtab = soup.find('div', class_='conMidtab')  # 华北地区所有的城市
    tables = conMidtab.find_all('table')  # 每一个城市
    for table in tables:
        trs = table.find_all('tr')[2:]  # 每一个地区
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]  # 城市td标签
            if index == 0:  # 省份的td标签放在了第一个城市的td标签的元素0上
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]  # 城市名
            temp_td = tds[-5]  # 温度td标签
            max_temp = list(temp_td.stripped_strings)[0]  # 最高温度

            ALL_DATA.append({'city': city, 'max_temp': int(max_temp)})  # 存储下来
            # print({'city': city, 'max_temp': max_temp})


def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]  # 全国的url
    for url in urls:
        parse_page(url)

    # 分析数据,根据最高气温排序
    ALL_DATA.sort(key=lambda data: data['max_temp'], reverse=True)
    data = ALL_DATA[0:10]  # 取气温最高的前10个

    cities = list(map(lambda x: x['city'], data))  # 城市名
    temps = list(map(lambda x: x['max_temp'], data))  # 温度

    # 数据可视化,pyecharts库
    chart = Bar('中国天气最高气温排行榜')  # Bar柱状图
    chart.add('', cities, temps)  # '': 名字，citite：x轴， temps：y轴
    chart.render('temperature.html')


if __name__ == '__main__':
    main()