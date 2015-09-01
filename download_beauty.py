# -*- coding: utf-8 -*-

# 使用方法
# 請將要下載的PTT 表特版文章網址放到 input.txt 中
# 在終端機中輸入：python download_beauty.py input.txt
# 下載的圖片會以該表特文章標題作為資料夾名稱
#
# 尚未測試完畢項目：
# 1. multiprocessing, threading
# 2. 圖片儲存緩衝


import urllib
import urllib2
import re
import os
import sys
import multiprocessing

img_regex = re.compile(r'<img src="[^"]*(//[i|m].imgur.com/[^"]+jpg)" alt=')


def download_pic(pic_url, dir):
    # 尚未處理重複下載的問題
    urllib.urlretrieve(pic_url, dir + '/' + pic_url.split('/')[-1])


def get_pic_list(url_content):
    # 縮小 regex parse 的範圍
    # 爬的範圍不包含 推文
    parse_start = url_content.find('img src=')
    parse_end = url_content.find('<span class="f2">')
    img_url_list = img_regex.findall(url_content[parse_start-1:parse_end])

    # 將每一個 list 中的 element 都加上 'https' 但是不確定有沒有更適合的做法
    img_url_list = ['https:' + img_url for img_url in img_url_list]
    return img_url_list


def get_title(content):
    title_start = content.find(r'og:title" content')
    title_end = content[title_start:].find(r'" />')
    title = content[title_start+19:title_start+title_end]
    return title


def store_pic(url):

    # 在 content 方面沒有處理推文，而是全部讀入
    # 如果要處理不包含推文的圖片可以 parse 到該篇文章 url 的地方
    # 因為在推文的前一行有文章網址

    try:
        content = urllib2.urlopen(url).read()
    except urllib2.HTTPError as httperr:
        print httperr, url
        return

    # Get title as dir name
    title = get_title(content)
    if not os.path.exists(title):
        os.mkdir(title)

    # Download each picture from picture url. In other word, impur address.
    pic_url_list = get_pic_list(content)
    for pic_url in pic_url_list:
        p = multiprocessing.Process(target=download_pic, args=(pic_url, title,))
        p.start()
        # download_pic(pic_url, title)



def  main():
    beauty_article_urls = []
    # 從檔案中毒入 urls
    with open(sys.argv[1]) as fd:
        for url in fd:
            beauty_article_urls.append(url)

    for article_url in beauty_article_urls:
        # 下載該網頁的圖片
        store_pic(article_url)

if __name__ == '__main__':
    main()
