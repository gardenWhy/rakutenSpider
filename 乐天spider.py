#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import requests
from bs4 import BeautifulSoup


def spider(word):
    for i in range(1):
        url = 'https://search.rakuten.co.jp/search/mall/"%s"/?f=1&sf=1&s=2&grp=product' % word
        ret = requests.get(url)
        ret.encoding = ret.apparent_encoding
        if 'ご指定の検索条件に該当する商品はありませんでした。' in ret.text:
            print('没找到商品!!!\n')  # 自行删除
            break
        if 'ページを閲覧しにくい状態になっております' in ret.text:
            print('404页面!!!\n')
            break
        soup = BeautifulSoup(ret.text, 'html.parser')
        #print(soup)
        div = soup.find(name='div', attrs={'class': 'dui-container main'})
        #print(div);
        div_item = (
            div.find(name='div', attrs={'class': 'dui-container content'}).
                find(name='div', attrs={'class': 'dui-container searchresults'}).
                find(name='div', attrs={'class': 'dui-cards searchresultitems'}).
                find(name='div', attrs={'class': 'dui-card searchresultitem'})
        )
        print('=' * 30)
        # 下面是爬网址
        href = div_item.find(name='div', attrs={'class': 'image'}).find(name='a').get('href')
        print(href)
        # 下面是标题
        title = (
            div_item.find(name='div', attrs={'class': 'content title'}).
                find(name='h2').
                find('a').get('title')
        )
        print(title)
        # 下面是价格
        price = (
            div_item.find(name='div', attrs={'class': 'content price'}).
                find('span').text[:-1]
        )
        print(price)
        # 下面是简介
        item_info = requests.get(href)
        item_info_soup = BeautifulSoup(item_info.text, 'html.parser')
        product = (
            item_info_soup.find('div', attrs={'itemtype': 'http://schema.org/Product'}).
                find(attrs={'class': 'item_desc'})
        )
        for p in product:
            del_word(p)
            # print(p)
        print('=' * 30)


def del_word(soup):  # 删除指定字
    Zneed_del = ['発売元', 'メーカー', 'ブランド', 'メーカー名']  # 制造商
    Sneed_del = ['原産国または製造国', 'メーカーまたは輸入元', '製造国', '原産国']  # 生产地
    Cneed_del = ['柄の材質', '毛の材質', '除電繊維の材質', '材質', '生地', '中身']  # 材质
    Gneed_del = ['個装サイズ', '個装重量']  # 规格
    for i in range(1):#剔除生产商关键字，并输出
        for need in Zneed_del:
            if need in soup:
                soup = str(soup).replace(need,'')
                # soup.replace(need,'')
                print(soup)

def del_sp_word(soup):  # 删除特殊字符
    need_del = ['●', '【', '】', '・', ':', '。', '：', '、']


if __name__ == '__main__':
    spider("マイナスイオン スタイリングブラシL")
