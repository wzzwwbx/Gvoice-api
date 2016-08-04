# coding=utf-8

import requests
import bs4
import re

def search(query):
    url = 'http://baike.baidu.com/search'
    params = {
        'word': query,
        'pn': 0,
        'rn': 0,
        'enc': 'utf-8'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

    response = requests.get(url, params=params, headers=headers)
    response.encoding='utf-8'
    return parse(response.text)


def parse(html_content):
    soup = bs4.BeautifulSoup(html_content, "lxml")

    result_num = soup.find_all(name='div', attrs={"class": "result-count"})
    # print(result_num[0].get_text())
    if not result_num:
        return ""

    result_links = soup.select('#body_wrapper  div.searchResult  dl dd a')
    url = soup.find(name='a', attrs={"class": "result-title"}).attrs.get('href')
    title = soup.find(name='a', attrs={"class": "result-title"}).get_text()
    content = soup.find(name='p', attrs={"class": "result-summary"}).get_text()
    # get picture id
    url_content = requests.get(url)
    url_content.encoding = 'utf-8'
    url_soup = bs4.BeautifulSoup(url_content.text, "lxml")
    # pictureUrl = url_soup.select('body div.body-wrapper div.content-wrapper div div.side-content div.summary-pic a img')[0].get('src')
    pictureUrl_list = url_soup.find_all(name = 'img', attrs={"src": re.compile(r'^http?://.+\.(jpg|png)')})
    pictureUrl = ''
    if pictureUrl_list:
        pictureUrl = pictureUrl_list[0].get('src')

    print(pictureUrl)
    return formResult(title, content, pictureUrl, url)

def formResult(title, content, pictureUrl, url):
    return {
        'title': title,
        'content': content,
        'pictureUrl': pictureUrl,
        'url': url
    }

if __name__ == '__main__':
    search('太阳')
